import json
from smartdoc.utils.logger import sys_logger  # Use the singleton system logger
from smartdoc.config.settings import config
from smartdoc.utils.exceptions import KnowledgeBaseError

class KnowledgeBaseManager:
    """
    Manages loading and accessing patient case data from a JSON knowledge base.
    """
    def __init__(self, filepath=None):
        """
        Initializes the KnowledgeBaseManager by loading the JSON data from the given filepath.

        Args:
            filepath (str): The path to the JSON knowledge base file. Defaults to config value.
        """
        self.filepath = filepath or config.CASE_FILE
        self.kb = None

        try:
            self._load_knowledge_base()
        except Exception as e:
            sys_logger.log_system("error", f"Failed to initialize KnowledgeBaseManager: {e}")
            raise KnowledgeBaseError(f"Knowledge base initialization failed: {e}")

    def _load_knowledge_base(self):
        """Load and validate the knowledge base file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.kb = json.load(f)

            if self.kb is None:
                raise KnowledgeBaseError(f"Knowledge base at {self.filepath} is empty or could not be parsed correctly.")

            # Basic validation
            required_sections = ["caseId", "caseTitle", "patientProfile", "initialPresentation"]
            missing_sections = [section for section in required_sections if section not in self.kb]

            if missing_sections:
                sys_logger.log_system("warning", f"Knowledge base missing sections: {missing_sections}")

            sys_logger.log_system("info", f"Knowledge base loaded successfully from {self.filepath}")

        except FileNotFoundError:
            error_msg = f"Knowledge base file not found at {self.filepath}"
            sys_logger.log_system("error", error_msg)
            raise KnowledgeBaseError(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"Could not decode JSON from {self.filepath}. Check file format. Error: {e}"
            sys_logger.log_system("error", error_msg)
            raise KnowledgeBaseError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error loading knowledge base: {e}"
            sys_logger.log_system("error", error_msg)
            raise KnowledgeBaseError(error_msg)

    def is_loaded(self):
        """Checks if the knowledge base was loaded successfully."""
        return self.kb is not None

    def _get_nested_value(self, keys, default=None):
        """
        Safely retrieves a nested value from the knowledge base with enhanced error handling.

        Args:
            keys (list or str): A list of keys representing the path to the value,
                                or a single string key for top-level access.
            default: The value to return if the path is not found.

        Returns:
            The requested value, or the default if not found.
        """
        if not self.is_loaded():
            sys_logger.log_system("warning", "Attempted to access knowledge base before it was loaded")
            return default

        if isinstance(keys, str):
            keys = [keys] # Treat single string as a list with one key

        data = self.kb
        try:
            for key in keys:
                if isinstance(data, list): # Handle lists if a key is an index
                    data = data[int(key)]
                else:
                    data = data[key]
            return data
        except (KeyError, TypeError, IndexError, ValueError) as e:
            sys_logger.log_system("debug", f"Key path {keys} not found in knowledge base: {e}")
            return default
        except Exception as e:
            sys_logger.log_system("warning", f"Unexpected error accessing key path {keys}: {e}")
            return default

    # --- General Case Information ---
    def get_case_title(self):
        return self._get_nested_value("caseTitle", "Unknown Case Title")

    def get_case_id(self):
        return self._get_nested_value("caseId", "Unknown Case ID")

    # --- Patient Profile ---
    def get_patient_profile_item(self, item_key):
        """Gets a specific item from the patientProfile section."""
        return self._get_nested_value(["patientProfile", item_key])

    def get_past_medical_history(self):
        """Returns the list of past medical history items."""
        pmh = self._get_nested_value(["patientProfile", "pastMedicalHistory"], [])
        if pmh:
            return [f"{item['condition']}" + (f" ({item['details']})" if item.get('details') else "") for item in pmh]
        return ["No past medical history available."]

    def get_medical_record_access_info(self):
        return self._get_nested_value(["patientProfile", "medicalRecordAccess"])

    # --- Initial Presentation ---
    def get_source_of_history(self):
        return self._get_nested_value(["initialPresentation", "sourceOfHistory"])

    def get_chief_complaints(self):
        """Returns a formatted string of chief complaints."""
        complaints = self._get_nested_value(["initialPresentation", "chiefComplaints"], [])
        if complaints:
            return "; ".join([f"{c['complaint']}" + (f" ({c['details']})" if c.get('details') else "") for c in complaints])
        return "No chief complaints listed."

    def get_hpi_item(self, item_key, sub_key=None):
        """Gets a specific item from the historyOfPresentIllness section."""
        base_path = ["initialPresentation", "historyOfPresentIllness", item_key]
        if sub_key:
            return self._get_nested_value(base_path + [sub_key])
        return self._get_nested_value(base_path)

    def get_hpi_onset_and_duration(self):
        return self.get_hpi_item("onsetAndDuration")

    def get_hpi_associated_symptoms(self):
        symptoms = self.get_hpi_item("associatedSymptoms", [])
        if symptoms:
            return "; ".join([f"{s['symptom']} ({s.get('duration', 'duration not specified')}, reported by {s.get('reportedBy', 'N/A')})" for s in symptoms])
        return "No specific associated symptoms listed beyond chief complaints."

    def get_hpi_pertinent_negatives(self):
        negatives = self.get_hpi_item("pertinentNegatives", [])
        return ", ".join(negatives) if negatives else "No pertinent negatives listed."

    def get_hpi_recent_medical_care(self):
        care_info = self.get_hpi_item("recentMedicalCare")
        if care_info:
            return f"Visited PCP {care_info.get('event', '')}, prescribed {care_info.get('treatment', 'N/A')} with {care_info.get('outcome', 'N/A')}."
        return "No recent medical care information available."

    def get_medications_initial_known(self):
        meds = self._get_nested_value(["initialPresentation", "medicationsInitial", "knownMedications"], [])
        return [f"{med['name']} (dosage: {med.get('dosage', 'unknown')}, route: {med.get('route', 'unknown')})" for med in meds] if meds else ["No known medications listed."]

    def get_medications_initial_uncertainty(self):
        return self._get_nested_value(["initialPresentation", "medicationsInitial", "uncertainty"])

    def get_initial_response_for_ra_meds(self):
        return self._get_nested_value(["initialPresentation", "medicationsInitial", "initialResponseIfQueriedAboutRAMeds"])

    def get_initial_response_for_other_meds(self):
        return self._get_nested_value(["initialPresentation", "medicationsInitial", "initialResponseIfQueriedAboutOtherMeds"])

    # --- Physical Examination (Initial ED) ---
    def get_physical_exam_general_appearance_initial(self):
        return self._get_nested_value(["initialPresentation", "physicalExaminationInitialED", "generalAppearance"])

    def get_vital_signs_initial(self):
        vitals = self._get_nested_value(["initialPresentation", "physicalExaminationInitialED", "vitalSigns"])
        if vitals:
            return (f"Temperature: {vitals.get('temperatureCelsius')}°C ({vitals.get('temperatureFahrenheit')}°F), "
                    f"Heart Rate: {vitals.get('heartRateBPM')} BPM, "
                    f"Blood Pressure: {vitals.get('bloodPressureSystolicmmHg')}/{vitals.get('bloodPressureDiastolicmmHg')} mmHg, "
                    f"Respiratory Rate: {vitals.get('respiratoryRateBPM')} breaths/min, "
                    f"O2 Sat: {vitals.get('oxygenSaturationPercentRoomAir')}% on room air.")
        return "Vital signs not available."

    def get_physical_exam_system_initial(self, system_key):
        """Gets findings for a specific system from the initial physical exam."""
        findings = self._get_nested_value(["initialPresentation", "physicalExaminationInitialED", system_key])
        if isinstance(findings, dict): # If it's a sub-dictionary like 'cardiovascular'
            return "; ".join([f"{k.replace('_', ' ').title()}: {v}" for k,v in findings.items()])
        return findings # If it's a direct string like generalAppearance

    # --- Laboratory Data (Initial ED) ---
    def get_lab_results_initial_all(self):
        labs = self._get_nested_value(["initialPresentation", "laboratoryDataInitialED"], [])
        if labs:
            return [f"{lab['test']}: {lab['value']} ({lab.get('interpretation', 'N/A')})" + (f" [Ref: {lab.get('referenceRange', 'N/A')}]" if lab.get('referenceRange') else "") for lab in labs]
        return ["No initial lab results available."]

    def get_specific_lab_result_initial(self, lab_name_keyword):
        """Searches for a specific lab result by keyword in the test name."""
        labs = self._get_nested_value(["initialPresentation", "laboratoryDataInitialED"], [])
        for lab in labs:
            if lab_name_keyword.lower() in lab.get("test", "").lower():
                return f"{lab['test']}: {lab['value']} ({lab.get('interpretation', 'N/A')})" + (f" [Ref: {lab.get('referenceRange', 'N/A')}]" if lab.get('referenceRange') else "")
        return f"No initial lab result found matching '{lab_name_keyword}'."

    # --- Imaging (Initial ED) ---
    def get_imaging_results_initial_cxr(self):
        cxr = self._get_nested_value(["initialPresentation", "imagingInitialED", "chestXray"])
        if cxr:
            return f"Chest X-ray (source: {cxr.get('impressionSource', 'N/A')}): {cxr.get('findings', 'No specific findings noted.')}"
        return "Initial chest X-ray results not available."

    def get_initial_diagnosis_and_treatment_ed(self):
        info = self._get_nested_value(["initialPresentation", "initialDiagnosisAndTreatmentED"])
        if info:
            return f"Initial ED Working Diagnosis: {info.get('workingDiagnosisED', 'N/A')}. Treatment ordered in ED: {', '.join(info.get('treatmentOrderedED', ['N/A']))}."
        return "Initial ED diagnosis and treatment information not available."

    # --- Discoverable Information ---
    def get_discoverable_item_details(self, item_name_keyword):
        """
        Retrieves details for a critical discoverable item by keyword.
        Note: This only provides the info; DialogueManager controls *when* it's revealed.
        """
        discoveries = self._get_nested_value(["discoverableInformation", "criticalDiscoveries"], [])
        for item in discoveries:
            if item_name_keyword.lower() in item.get("item", "").lower():
                return item # Returns the whole dictionary for that item
        return None # Or a message like "No such discoverable item found."

    def get_timeline_events(self):
        """Returns the timeline of events in hospital."""
        return self._get_nested_value(["discoverableInformation", "timelineOfEventsInHospital"], [])

    def get_progression_and_outcome(self, key=None):
        if key:
            return self._get_nested_value(["discoverableInformation", "progressionAndOutcome", key])
        return self._get_nested_value(["discoverableInformation", "progressionAndOutcome"])

    def get_cognitive_bias_consideration(self, bias_name_key):
        return self._get_nested_value(["cognitiveBiasConsiderations", bias_name_key])

    def get_metacognitive_prompts(self):
        return self._get_nested_value("metacognitivePromptsFromPaper", [])


# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    # Assume case01.json is in the same directory or provide full path
    kb_manager = KnowledgeBaseManager(filepath="case01.json")

    if kb_manager.is_loaded():
        print(f"Case Title: {kb_manager.get_case_title()}")
        print(f"Patient Age Category: {kb_manager.get_patient_profile_item('ageCategory')}")
        print(f"Past Medical History: {kb_manager.get_past_medical_history()}")
        print(f"Chief Complaints: {kb_manager.get_chief_complaints()}")
        print(f"HPI Onset/Duration: {kb_manager.get_hpi_onset_and_duration()}")
        print(f"Initial Response for RA Meds query: {kb_manager.get_initial_response_for_ra_meds()}")
        print(f"Initial Vital Signs: {kb_manager.get_vital_signs_initial()}")
        print(f"Initial Respiratory Exam: {kb_manager.get_physical_exam_system_initial('respiratory')}")
        print(f"All Initial Lab Results: {kb_manager.get_lab_results_initial_all()}")
        print(f"Specific Lab (WBC): {kb_manager.get_specific_lab_result_initial('WBC')}")
        print(f"Initial CXR: {kb_manager.get_imaging_results_initial_cxr()}")
        print(f"Initial ED Dx & Tx: {kb_manager.get_initial_diagnosis_and_treatment_ed()}")

        infliximab_info = kb_manager.get_discoverable_item_details("Infliximab")
        if infliximab_info:
            print(f"\nDetails for Infliximab (if student discovers it):")
            print(f"  Item: {infliximab_info.get('item')}")
            print(f"  Details: {infliximab_info.get('details')}")
            print(f"  Importance: {infliximab_info.get('importance')}")

        print(f"\nMetacognitive Prompts: {kb_manager.get_metacognitive_prompts()}")
    else:
        print("Knowledge base could not be loaded. Check errors above.")
