import json
import os
from smartdoc.utils.logger import sys_logger
from smartdoc.config.settings import config

def load_canonical_question_mappings(filepath=None):
    """Load canonical question mappings from JSON file."""
    filepath = filepath or config.CANONICAL_MAPPINGS_FILE
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        mappings = data.get("canonical_question_mappings", [])
        sys_logger.log_system("info", f"Loaded {len(mappings)} canonical question mappings from {filepath}")
        return mappings
    except Exception as e:
        sys_logger.log_system("error", f"Failed to load canonical question mappings from {filepath}: {e}")
        sys_logger.log_system("info", "Falling back to hardcoded mappings")
        return _get_hardcoded_mappings()

def _get_hardcoded_mappings():
    """Fallback hardcoded mappings for when JSON file is not available."""
    return [
    # === Patient Profile ===
    {
        "id": "profile_age",
        "canonical_question": "How old is the patient?",
        "variations": ["What is the patient's age category?", "Tell me the patient's age."],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_patient_profile_item", "args": ["ageCategory"]},
        "expected_dialogue_state": ["INTRODUCTION", "PMH_GATHERING"]
    },
    {
        "id": "profile_language",
        "canonical_question": "What language does the patient speak?",
        "variations": ["Is there a language barrier with the patient?", "Does the patient speak English?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_patient_profile_item", "args": ["language"]},
        "expected_dialogue_state": ["INTRODUCTION"]
    },
    {
        "id": "profile_social_context_historian",
        "canonical_question": "Who is providing the history for the patient?",
        "variations": ["Is the patient alone or with someone?", "Who is giving information about the patient?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_patient_profile_item", "args": ["socialContext"]},
        "expected_dialogue_state": ["INTRODUCTION"]
    },
    {
        "id": "pmh_general",
        "canonical_question": "What is the patient's past medical history?",
        "variations": ["Does the patient have any pre-existing medical conditions?", "Tell me about her previous illnesses."],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_past_medical_history"},
        "expected_dialogue_state": ["PMH_GATHERING"]
    },
    # Add specific PMH conditions if you want direct SBERT matching for them, e.g.:
    # {
    #     "id": "pmh_diabetes",
    #     "canonical_question": "Does the patient have diabetes?",
    #     "action_type": "check_condition_in_pmh", # DM would call get_past_medical_history then check
    #     "target_details": {"condition_keyword": "Diabetes Mellitus"}
    # },
    {
        "id": "profile_medical_records",
        "canonical_question": "Are the patient's full medical records available?",
        "variations": ["Do we have access to her previous medical files?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_medical_record_access_info"},
        "expected_dialogue_state": ["INTRODUCTION", "MEDICATION_REVIEW", "PMH_GATHERING"]
    },

    # === Initial Presentation: HPI ===
    {
        "id": "hpi_source_of_history",
        "canonical_question": "Who is the source of the patient's history?",
        "variations": [],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_source_of_history"},
        "expected_dialogue_state": ["INTRODUCTION", "CHIEF_COMPLAINT_EXPLORATION"]
    },
    {
        "id": "hpi_chief_complaint",
        "canonical_question": "What is the patient's chief complaint?",
        "variations": ["Why did the patient come to the emergency department?", "What's the main problem today?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_chief_complaints"},
        "expected_dialogue_state": ["CHIEF_COMPLAINT_EXPLORATION"]
    },
    {
        "id": "hpi_onset_duration_primary",
        "canonical_question": "When did the main problem start and how long has it been going on?",
        "variations": ["Tell me about the onset of the shortness of breath.", "How long has the cough been present?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_hpi_onset_and_duration"},
        "expected_dialogue_state": ["HPI_GATHERING"]
    },
    {
        "id": "hpi_associated_symptoms_general",
        "canonical_question": "Are there any other symptoms associated with the main complaint?",
        "variations": ["What other symptoms has the patient experienced recently?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_hpi_associated_symptoms"},
        "expected_dialogue_state": ["HPI_GATHERING", "REVIEW_OF_SYSTEMS"]
    },
    # Specific associated symptoms (can be added for more direct mapping if needed):
    # {
    #     "id": "hpi_decreased_intake",
    #     "canonical_question": "Has the patient had decreased oral intake?",
    #     "action_type": "check_associated_symptom", # DM logic
    #     "target_details": {"symptom_keyword": "Decreased oral intake"}
    # },
    {
        "id": "hpi_pertinent_negatives",
        "canonical_question": "What symptoms does the patient deny?",
        "variations": ["Has the patient had any chest pain, fevers, or chills recently?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_hpi_pertinent_negatives"},
        "expected_dialogue_state": ["HPI_GATHERING", "REVIEW_OF_SYSTEMS"]
    },
    {
        "id": "hpi_recent_medical_care",
        "canonical_question": "Has the patient sought any medical attention for these complaints recently?",
        "variations": ["Did she see her primary care physician recently?", "Any recent treatments for these symptoms?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_hpi_recent_medical_care"},
        "expected_dialogue_state": ["HPI_GATHERING", "PMH_GATHERING"]
    },
    {
        "id": "hpi_travel_contacts",
        "canonical_question": "Has the patient traveled recently or had any known sick contacts?",
        "variations": ["Any recent travel history?", "Exposure to infectious diseases?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_hpi_item", "args": ["travelAndContactHistory"]},
        "expected_dialogue_state": ["HPI_GATHERING", "SOCIAL_HISTORY_GATHERING"]
    },

    # === Initial Presentation: Medications ===
    {
        "id": "meds_current_known",
        "canonical_question": "What medications is the patient currently taking?",
        "variations": ["Can you list her current medications?", "Is she on any regular pills?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_medications_initial_known"},
        "expected_dialogue_state": ["MEDICATION_REVIEW"]
    },
    {
        "id": "meds_uncertainty", # For student to probe if list is complete
        "canonical_question": "Is the medication list provided by the son complete?",
        "variations": ["Are there any other medications the patient might be taking that the son is unsure about?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_medications_initial_uncertainty"},
        "expected_dialogue_state": ["MEDICATION_REVIEW"]
    },
    {
        "id": "meds_ra_specific_initial_query", # This will trigger the scripted uncertain response
        "canonical_question": "What specific medications is the patient taking for her rheumatoid arthritis?",
        "variations": ["How is her rheumatoid arthritis being treated?", "Is she on any medication for RA?"],
        "action_type": "fetch_from_kb", # Fetches the scripted response
        "target_details": {"method": "get_initial_response_for_ra_meds"},
        "expected_dialogue_state": ["MEDICATION_REVIEW", "PMH_GATHERING"]
    },
    {
        "id": "meds_other_meds_initial_query", # This also triggers a scripted uncertain response
        "canonical_question": "Is the patient taking any other medications apart from the known ones?",
        "variations": ["Are there any other pills or treatments she receives?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_initial_response_for_other_meds"},
        "expected_dialogue_state": ["MEDICATION_REVIEW"]
    },
    # Allergies are part of MEDICATION_REVIEW state in FSM, need mapping:
    {
        "id": "meds_allergies",
        "canonical_question": "Does the patient have any allergies?",
        "variations": ["Is she allergic to any medications or substances?"],
        "action_type": "provide_scripted_response", # Assuming not in case01.json initially
        "target_details": {"response_key": "allergies_unknown_or_none_reported_by_son"},
        "expected_dialogue_state": ["MEDICATION_REVIEW"]
    },


    # === Initial Presentation: Physical Exam ===
    {
        "id": "exam_general_appearance",
        "canonical_question": "What is the patient's general appearance on examination?",
        "variations": ["How does the patient look generally?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_physical_exam_general_appearance_initial"},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },
    {
        "id": "exam_vital_signs",
        "canonical_question": "What are the patient's vital signs?",
        "variations": ["Tell me her vitals.", "What were her temperature, heart rate, blood pressure, respiratory rate, and oxygen saturation?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_vital_signs_initial"},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },
    {
        "id": "exam_cardiovascular",
        "canonical_question": "What were the findings on the cardiovascular exam?",
        "variations": ["How was her heart exam?", "Any murmurs or abnormal heart sounds?", "Was JVP assessed?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_physical_exam_system_initial", "args": ["cardiovascular"]},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },
    {
        "id": "exam_respiratory",
        "canonical_question": "What did the respiratory or lung exam show?",
        "variations": ["Any findings on auscultation of the lungs?", "Were there crackles or wheezes?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_physical_exam_system_initial", "args": ["respiratory"]},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },
    {
        "id": "exam_extremities",
        "canonical_question": "What did the examination of her extremities reveal?",
        "variations": ["Was there any edema in the lower extremities?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_physical_exam_system_initial", "args": ["extremities"]},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },
    {
        "id": "exam_musculoskeletal",
        "canonical_question": "Were there any musculoskeletal findings on exam?",
        "variations": ["Did the exam show any joint deformities related to rheumatoid arthritis?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_physical_exam_system_initial", "args": ["musculoskeletal"]},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },
     # Abdominal/Neuro exam not detailed in initial findings, VSP should indicate this.
    {
        "id": "exam_abdominal_query",
        "canonical_question": "What were the abdominal exam findings?",
        "action_type": "provide_scripted_response",
        "target_details": {"response_key": "abdominal_exam_not_detailed_initially"},
        "expected_dialogue_state": ["PHYSICAL_EXAM_QUERY"]
    },


    # === Initial Presentation: Labs & Imaging ===
    {
        "id": "labs_initial_general",
        "canonical_question": "What were the results of the initial blood tests?",
        "variations": ["Can you summarize the initial lab findings?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_lab_results_initial_all"},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY"]
    },
    {
        "id": "labs_wbc",
        "canonical_question": "What was the patient's white blood cell count?",
        "variations": ["Tell me the WBC count."],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_specific_lab_result_initial", "args": ["White Blood Cell Count"]},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY"]
    },
    {
        "id": "labs_hemoglobin",
        "canonical_question": "What was her hemoglobin level?",
        "variations": ["Tell me the Hgb."],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_specific_lab_result_initial", "args": ["Hemoglobin"]},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY"]
    },
    {
        "id": "labs_creatinine",
        "canonical_question": "What was the serum creatinine?",
        "variations": [],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_specific_lab_result_initial", "args": ["Serum Creatinine"]},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY"]
    },
    {
        "id": "labs_pro_bnp",
        "canonical_question": "What was the pro-BNP level?",
        "variations": ["Was a pro-BNP measured?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_specific_lab_result_initial", "args": ["Pro-Brain-Type Natriuretic Peptide"]},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY"]
    },
    {
        "id": "imaging_cxr_initial",
        "canonical_question": "What did the initial chest X-ray show?",
        "variations": ["What were the findings on the first chest film?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_imaging_results_initial_cxr"},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY"]
    },
    {
        "id": "initial_ed_diagnosis_treatment",
        "canonical_question": "What was the initial working diagnosis and treatment in the ED?",
        "variations": ["What did the ED team think was going on and what did they do?"],
        "action_type": "fetch_from_kb",
        "target_details": {"method": "get_initial_diagnosis_and_treatment_ed"},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY", "REASSESSMENT"]
    },

    # === Discoverable Information (SBERT match triggers DM to check conditions for reveal) ===
    {
        "id": "discoverable_infliximab_query",
        "canonical_question": "Is the patient on any specific treatments for rheumatoid arthritis like biologics or Infliximab?",
        "variations": ["What is the exact medication for her RA?", "Can we find out about her RA treatment from old records?"],
        "action_type": "trigger_discoverable", # DM will check triggers from case01.json for 'Infliximab use'
        "target_details": {"discoverable_item_key": "Infliximab use"},
        "expected_dialogue_state": ["MEDICATION_REVIEW", "REASSESSMENT", "INVESTIGATIONS_QUERY"]
    },
    {
        "id": "discoverable_echo_query",
        "canonical_question": "Was an echocardiogram performed and what were its results?",
        "variations": ["Did the patient get an echo?", "What did the cardiac ultrasound show?"],
        "action_type": "trigger_discoverable",
        "target_details": {"discoverable_item_key": "Echocardiogram result"},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY", "REASSESSMENT"]
    },
    {
        "id": "discoverable_ct_chest_query",
        "canonical_question": "Given the ongoing symptoms, was a CT scan of the chest done?",
        "variations": ["What did the chest CT reveal?", "Any advanced lung imaging?"],
        "action_type": "trigger_discoverable",
        "target_details": {"discoverable_item_key": "CT Chest findings"},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY", "REASSESSMENT"]
    },
    {
        "id": "discoverable_final_cxr_details_query",
        "canonical_question": "What was the attending radiologist's final interpretation of the chest X-ray?",
        "variations": ["Were there any subtle findings on the formal CXR report besides congestion?"],
        "action_type": "trigger_discoverable",
        "target_details": {"discoverable_item_key": "Final CXR interpretation details"},
        "expected_dialogue_state": ["INVESTIGATIONS_QUERY", "REASSESSMENT"]
    },

    # === General Interview Control / Other ===
    {
        "id": "general_greet",
        "canonical_question": "Hello",
        "variations": ["Hi", "Good morning"],
        "action_type": "generic_response_or_state_change",
        "target_details": {"response_key": "greeting_response", "next_state_suggestion": "CHIEF_COMPLAINT_EXPLORATION"},
        "expected_dialogue_state": ["INTRODUCTION"]
    },
    {
        "id": "general_thank_you_conclude",
        "canonical_question": "Thank you, I have all the information I need.",
        "variations": ["I think I'm done with the interview.", "Thanks for your time."],
        "action_type": "generic_response_or_state_change",
        "target_details": {"response_key": "acknowledgement_and_closing", "next_state_suggestion": "CLOSING"},
        "expected_dialogue_state": ["REASSESSMENT", "INVESTIGATIONS_QUERY", "PHYSICAL_EXAM_QUERY", "REVIEW_OF_SYSTEMS"]
    }
]

# Load canonical question mappings from JSON file with fallback to hardcoded
canonical_question_mappings = load_canonical_question_mappings()

