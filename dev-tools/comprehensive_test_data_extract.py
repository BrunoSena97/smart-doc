#!/usr/bin/env python3
"""
Comprehensive Test Data Extract for SmartDoc Clinical Evaluator Testing

This script provides comprehensive data extraction for creating evaluator test scripts
with perfect and imperfect solutions. Contains all discovery blocks, intents, and
metacognitive questions used in the SmartDoc system.

Generated from intent_driven_case.json and system code analysis.
"""

import json
from typing import Dict, List, Any


class SmartDocTestDataExtract:
    """Complete test data for creating comprehensive evaluator validation scripts."""

    def __init__(self):
        """Initialize with all extracted data from SmartDoc system."""

        # ===== DISCOVERY BLOCKS (24 total, 6 critical) =====
        self.discovery_blocks = {
            # DEMOGRAPHICS (3 blocks)
            "demographics_basic": {
                "groupId": "Demographics",
                "level": 1,
                "content": "Patient Profile: Mrs. Chen is a 72-year-old Chinese-speaking woman presenting with her daughter as translator. She appears comfortable but mildly short of breath when speaking.",
                "is_critical": False,
                "prerequisites": []
            },
            "demographics_language": {
                "groupId": "Demographics",
                "level": 2,
                "content": "Language and Communication: Mrs. Chen primarily speaks Mandarin Chinese. Her daughter serves as translator and historian. Mrs. Chen nods appropriately to direct questions but prefers responding in Mandarin.",
                "is_critical": False,
                "prerequisites": ["profile_language"]
            },
            "demographics_records": {
                "groupId": "Demographics",
                "level": 3,
                "content": "Medical Records Access: Limited medical records available from previous healthcare visits. Patient has been seen at different clinics. Previous hospitalizations occurred at other facilities.",
                "is_critical": False,
                "prerequisites": ["profile_medical_records"]
            },

            # HISTORY OF PRESENT ILLNESS (6 blocks, 1 critical)
            "hpi_chief_complaint": {
                "groupId": "History",
                "level": 1,
                "content": "Chief Complaint: 'She has been having trouble breathing and feeling very tired for the past month. The breathing is getting worse, especially when she tries to walk or climb stairs.'",
                "is_critical": True,
                "prerequisites": ["hpi_chief_complaint"]
            },
            "hpi_onset_primary": {
                "groupId": "History",
                "level": 2,
                "content": "Onset and Duration: Symptoms began approximately 4-6 weeks ago, initially mild but progressively worsening. Patient first noticed shortness of breath during her usual daily activities like cooking and light housework.",
                "is_critical": False,
                "prerequisites": ["hpi_onset_duration_primary"]
            },
            "hpi_associated_symptoms": {
                "groupId": "History",
                "level": 2,
                "content": "Associated Symptoms: Patient reports progressive fatigue, decreased appetite, and unintentional weight loss (approximately 8-10 pounds over the past month). Denies chest pain but reports occasional 'pressure' sensation.",
                "is_critical": False,
                "prerequisites": ["hpi_associated_symptoms_general"]
            },
            "hpi_fever_chills": {
                "groupId": "History",
                "level": 3,
                "content": "Fever and Constitutional Symptoms: Patient reports intermittent low-grade fevers (feeling 'hot' but no measured temperatures) and occasional chills, particularly in the evenings. Night sweats reported 2-3 times per week.",
                "is_critical": False,
                "prerequisites": ["hpi_fever", "hpi_chills"]
            },
            "hpi_cough_details": {
                "groupId": "History",
                "level": 3,
                "content": "Cough Characteristics: Dry, non-productive cough present for approximately 3 weeks. Cough is more prominent at night and early morning. No hemoptysis or sputum production reported.",
                "is_critical": False,
                "prerequisites": ["hpi_cough"]
            },
            "hpi_recent_care": {
                "groupId": "History",
                "level": 3,
                "content": "Recent Medical Care: Seen at urgent care 2 weeks ago for similar symptoms. Given cough suppressant and told to 'rest.' Symptoms have not improved and patient feels they are worsening.",
                "is_critical": False,
                "prerequisites": ["hpi_recent_medical_care"]
            },

            # MEDICATIONS (3 blocks, 1 critical)
            "medications_basic": {
                "groupId": "Medications",
                "level": 1,
                "content": "Current Known Medications: Patient takes 'some pills for arthritis' - daughter uncertain about specific names or doses. Also takes 'vitamins' and occasionally acetaminophen for joint pain.",
                "is_critical": False,
                "prerequisites": ["meds_current_known"]
            },
            "medications_ra_specific": {
                "groupId": "Medications",
                "level": 2,
                "content": "Rheumatoid Arthritis Medications: Patient takes methotrexate 15mg weekly and prednisone 5mg daily for rheumatoid arthritis. Diagnosed approximately 8 years ago. Daughter thinks there might be 'other arthritis medications' but is uncertain.",
                "is_critical": False,
                "prerequisites": ["meds_ra_specific_initial_query"]
            },
            "medications_critical_infliximab": {
                "groupId": "Medications",
                "level": 3,
                "content": "Critical Medication History: INFLIXIMAB (Remicade) 5mg/kg IV infusions every 8 weeks for past 2 years. Last infusion 6 weeks ago. This TNF-alpha inhibitor significantly increases infection risk, particularly for tuberculosis and other granulomatous infections.",
                "is_critical": True,
                "prerequisites": ["meds_full_reconciliation_query"]
            },

            # PHYSICAL EXAMINATION (4 blocks, 1 critical)
            "exam_vitals": {
                "groupId": "PhysicalExam",
                "level": 1,
                "content": "Vital Signs: Temperature 99.8°F (37.7°C), Heart Rate 102 bpm, Blood Pressure 138/82 mmHg, Respiratory Rate 22/min, Oxygen Saturation 94% on room air",
                "is_critical": False,
                "prerequisites": ["exam_vital"]
            },
            "exam_general": {
                "groupId": "PhysicalExam",
                "level": 1,
                "content": "General Appearance: Elderly Chinese woman appearing mildly ill and fatigued. Alert and oriented. Mild respiratory distress with conversation. Weight loss apparent per daughter's report.",
                "is_critical": False,
                "prerequisites": ["exam_general_appearance"]
            },
            "exam_cardiovascular": {
                "groupId": "PhysicalExam",
                "level": 2,
                "content": "Cardiovascular Examination: Regular rate and rhythm, S1 and S2 present. No murmurs, rubs, or gallops appreciated. No peripheral edema. Peripheral pulses intact and equal bilaterally.",
                "is_critical": False,
                "prerequisites": ["exam_cardiovascular"]
            },
            "exam_respiratory": {
                "groupId": "PhysicalExam",
                "level": 2,
                "content": "Respiratory Examination: Bilateral fine crackles heard in lower lung fields. Decreased breath sounds at bilateral bases. No wheezing or rhonchi. Mild use of accessory muscles with inspiration.",
                "is_critical": True,
                "prerequisites": ["exam_respiratory"]
            },

            # LABORATORY RESULTS (4 blocks, 1 critical)
            "labs_basic": {
                "groupId": "Labs",
                "level": 1,
                "content": "Basic Laboratory Results: White Blood Cell Count: 12,800/μL (elevated), Hemoglobin: 9.8 g/dL (low), Platelet Count: 420,000/μL (elevated)",
                "is_critical": False,
                "prerequisites": ["labs_general", "labs_wbc", "labs_hemoglobin"]
            },
            "labs_inflammatory": {
                "groupId": "Labs",
                "level": 2,
                "content": "Inflammatory Markers: Erythrocyte Sedimentation Rate (ESR): 78 mm/hr (markedly elevated), C-Reactive Protein (CRP): 45 mg/L (elevated), suggesting significant systemic inflammation",
                "is_critical": False,
                "prerequisites": ["labs_general"]
            },
            "labs_cardiac": {
                "groupId": "Labs",
                "level": 2,
                "content": "Cardiac Biomarkers: Pro-BNP: 180 pg/mL (mildly elevated but not significantly elevated for age), Troponin I: <0.01 ng/mL (normal). Cardiac involvement not primary concern.",
                "is_critical": False,
                "prerequisites": ["labs_bnp"]
            },
            "labs_tb_testing": {
                "groupId": "Labs",
                "level": 3,
                "content": "Tuberculosis Testing: QuantiFERON-TB Gold: POSITIVE, TST (if performed): Would likely be positive. These results, combined with clinical presentation and immunosuppression, are highly suggestive of active tuberculosis.",
                "is_critical": True,
                "prerequisites": ["labs_general"]
            },

            # IMAGING STUDIES (4 blocks, 2 critical)
            "imaging_chest_xray": {
                "groupId": "Imaging",
                "level": 1,
                "content": "Chest X-ray: Bilateral diffuse micronodular opacities throughout both lung fields, more prominent in the upper lobes. This 'miliary' pattern consists of numerous small, well-defined nodules measuring 1-2mm each. Pattern highly suggestive of miliary tuberculosis.",
                "is_critical": True,
                "prerequisites": ["imaging_chest_xray"]
            },
            "imaging_ct_chest": {
                "groupId": "Imaging",
                "level": 2,
                "content": "CT Chest: Confirms extensive bilateral miliary nodules throughout both lungs. Random distribution of small nodules (1-3mm) in a classic miliary pattern. No significant lymphadenopathy. No pleural effusions. Findings virtually pathognomonic for miliary tuberculosis in this clinical context.",
                "is_critical": True,
                "prerequisites": ["imaging_ct_chest"]
            },
            "imaging_echo": {
                "groupId": "Imaging",
                "level": 2,
                "content": "Echocardiogram: Normal left ventricular function with ejection fraction 60%. No wall motion abnormalities. No pericardial effusion. Mild tricuspid regurgitation consistent with mild pulmonary hypertension secondary to lung disease.",
                "is_critical": False,
                "prerequisites": ["imaging_echo"]
            },
            "imaging_additional": {
                "groupId": "Imaging",
                "level": 3,
                "content": "Additional Imaging Considerations: Given the miliary pattern and clinical context, abdominal imaging might reveal hepatosplenomegaly or other extrapulmonary manifestations of disseminated tuberculosis, but chest findings are diagnostic.",
                "is_critical": False,
                "prerequisites": ["imaging_general"]
            }
        }

        # ===== CLINICAL INTENTS (30+ intents organized by category) =====
        self.clinical_intents = {
            # PROFILE AND DEMOGRAPHICS
            "profile_age": {
                "description": "Questions about patient's age",
                "examples": ["How old is the patient?", "What is the patient's age?", "Patient age?"],
                "category": "profile"
            },
            "profile_language": {
                "description": "Questions about language barriers or patient's spoken language",
                "examples": ["Does the patient speak English?", "Language barrier?", "What language?"],
                "category": "profile"
            },
            "profile_social_context_historian": {
                "description": "Questions about who is providing the history",
                "examples": ["Who is giving the history?", "Is the patient alone?", "Family member present?"],
                "category": "profile"
            },
            "profile_medical_records": {
                "description": "Questions about medical record access or availability",
                "examples": ["Do you have medical records?", "Previous records available?", "Medical record access?"],
                "category": "profile"
            },

            # HISTORY OF PRESENT ILLNESS
            "hpi_chief_complaint": {
                "description": "Questions about the main complaint or what brought patient to clinic",
                "examples": ["What brings you here?", "Chief complaint?", "Main problem?", "What's wrong?"],
                "category": "chief_complaint"
            },
            "hpi_onset_duration_primary": {
                "description": "Questions about when symptoms started and their duration",
                "examples": ["When did this start?", "How long have you had this?", "Duration of symptoms?"],
                "category": "history_present_illness"
            },
            "hpi_associated_symptoms_general": {
                "description": "Questions about associated symptoms",
                "examples": ["Any other symptoms?", "Associated symptoms?", "What else do you feel?"],
                "category": "history_present_illness"
            },
            "hpi_pertinent_negatives": {
                "description": "Questions about important symptoms that are absent",
                "examples": ["Any chest pain?", "Any fever?", "Pertinent negatives?"],
                "category": "history_present_illness"
            },
            "hpi_recent_medical_care": {
                "description": "Questions about recent medical care or treatments",
                "examples": ["Recent doctor visits?", "Any recent treatment?", "Medical care recently?"],
                "category": "history_present_illness"
            },
            "hpi_fever": {
                "description": "Questions about fever or temperature changes",
                "examples": ["Any fever?", "Temperature?", "Running a fever?"],
                "category": "history_present_illness"
            },
            "hpi_cough": {
                "description": "Questions about cough or sputum production",
                "examples": ["Any cough?", "Coughing?", "Sputum production?"],
                "category": "history_present_illness"
            },
            "hpi_shortness_of_breath": {
                "description": "Questions about dyspnea or breathing difficulty",
                "examples": ["Short of breath?", "Breathing problems?", "Dyspnea?"],
                "category": "history_present_illness"
            },
            "hpi_chest_pain": {
                "description": "Questions about chest pain or chest discomfort",
                "examples": ["Chest pain?", "Any chest discomfort?", "Pain in chest?"],
                "category": "history_present_illness"
            },
            "hpi_chills": {
                "description": "Questions about chills or feeling cold",
                "examples": ["Any chills?", "Feeling cold?", "Chills or rigors?"],
                "category": "history_present_illness"
            },
            "hpi_weight_changes": {
                "description": "Questions about weight loss or weight changes",
                "examples": ["Weight loss?", "Any weight changes?", "Has patient lost weight?"],
                "category": "history_present_illness"
            },

            # PAST MEDICAL HISTORY
            "pmh_general": {
                "description": "Questions about past medical history in general",
                "examples": ["Past medical history?", "Any previous conditions?", "Medical history?"],
                "category": "past_medical_history"
            },

            # MEDICATIONS (3 levels of escalation - SIMPLIFIED)
            "meds_current_known": {
                "description": "Questions about current medications (Level 1 - basic medication list)",
                "examples": ["What medications are you taking?", "Current meds?", "Any prescriptions?", "Any other medications?"],
                "category": "medications"
            },
            "meds_ra_specific_initial_query": {
                "description": "Specific questions about rheumatoid arthritis medications (Level 2 - RA meds)",
                "examples": ["What medications does she take for rheumatoid arthritis?", "RA medications?", "Arthritis drugs?", "Not sure about RA medications?"],
                "category": "medications"
            },
            "meds_full_reconciliation_query": {
                "description": "Complete medication reconciliation requests (Level 3 - reveals critical infliximab)",
                "examples": ["Complete medication reconciliation from previous hospitalizations", "Any biologics or immunosuppressive medications?", "What about infliximab or other biologics?"],
                "category": "medications"
            },

            # PHYSICAL EXAMINATION
            "exam_general_appearance": {
                "description": "General physical examination and appearance",
                "examples": ["Let me examine you", "Physical exam", "General appearance"],
                "category": "physical_exam_general"
            },
            "exam_vital": {
                "description": "Requests for vital signs",
                "examples": ["Check blood pressure", "Vital signs?", "Temperature?", "Heart rate?"],
                "category": "vital_signs"
            },
            "exam_cardiovascular": {
                "description": "Heart and cardiovascular examination",
                "examples": ["Listen to your heart", "Heart sounds", "Cardiovascular exam"],
                "category": "physical_exam_cardiovascular"
            },
            "exam_respiratory": {
                "description": "Lung and breathing examination",
                "examples": ["Listen to your lungs", "Breathing sounds", "Lung exam"],
                "category": "physical_exam_respiratory"
            },

            # LABORATORY TESTS
            "labs_general": {
                "description": "Questions about laboratory tests or results",
                "examples": ["Lab results?", "Blood tests?", "Laboratory findings?"],
                "category": "diagnostics"
            },
            "labs_bnp": {
                "description": "Questions about BNP or pro-BNP levels",
                "examples": ["BNP level?", "What's the pro-BNP?", "Brain natriuretic peptide?"],
                "category": "diagnostics"
            },
            "labs_wbc": {
                "description": "Questions about white blood cell count",
                "examples": ["White blood cell count?", "WBC?", "What's the white count?"],
                "category": "diagnostics"
            },
            "labs_hemoglobin": {
                "description": "Questions about hemoglobin levels",
                "examples": ["Hemoglobin level?", "What's the Hgb?", "Hematocrit?"],
                "category": "diagnostics"
            },

            # IMAGING STUDIES
            "imaging_chest_xray": {
                "description": "Questions about chest X-ray studies",
                "examples": ["Chest X-ray?", "Order a chest X-ray", "CXR results?", "Can I see the chest X-ray?"],
                "category": "diagnostics"
            },
            "imaging_echo": {
                "description": "Questions about echocardiogram studies",
                "examples": ["Echocardiogram?", "Order an echo", "Echo results?", "Heart ultrasound?"],
                "category": "diagnostics"
            },
            "imaging_ct_chest": {
                "description": "Questions about chest CT scan studies",
                "examples": ["Chest CT?", "CT chest?", "Order a chest CT", "What does the chest CT show?"],
                "category": "diagnostics"
            },
            "imaging_general": {
                "description": "General questions about imaging studies",
                "examples": ["Any imaging?", "Radiology results?", "Scan results?", "What imaging studies do we have?"],
                "category": "diagnostics"
            },

            # GENERAL COMMUNICATION
            "general_greeting": {
                "description": "General greetings and conversation starters",
                "examples": ["Hello", "Good morning", "How are you?"],
                "category": "general"
            },
            "clarification": {
                "description": "Asking for clarification or more details",
                "examples": ["Can you clarify?", "Tell me more", "What do you mean?"],
                "category": "clarification"
            }
        }

        # ===== METACOGNITIVE REFLECTION QUESTIONS =====
        self.metacognitive_questions = {
            "supporting_evidence": {
                "question": "What is the single most compelling piece of evidence that supports your chosen diagnosis?",
                "field_id": "supporting-evidence",
                "purpose": "Assess ability to identify strongest diagnostic evidence",
                "example_perfect_answer": "The bilateral miliary pattern on chest X-ray and CT combined with positive QuantiFERON-TB Gold in an immunocompromised patient on infliximab provides virtually pathognomonic evidence for miliary tuberculosis.",
                "example_poor_answer": "The patient has breathing problems and fever."
            },
            "contradicting_evidence": {
                "question": "What is one piece of evidence that might argue against your diagnosis?",
                "field_id": "contradicting-evidence",
                "purpose": "Evaluate critical thinking and bias awareness",
                "example_perfect_answer": "The relatively preserved oxygen saturation (94%) and absence of severe systemic illness might initially suggest a less aggressive process, but this can occur in early miliary TB before full dissemination.",
                "example_poor_answer": "Nothing really argues against it."
            },
            "alternative_diagnoses": {
                "question": "What else could this be? List at least two reasonable alternative diagnoses.",
                "field_id": "alternative-diagnoses",
                "purpose": "Test differential diagnosis generation",
                "example_perfect_answer": "1) Metastatic carcinoma with miliary lung metastases 2) Hypersensitivity pneumonitis from environmental exposure 3) Sarcoidosis with bilateral pulmonary involvement",
                "example_poor_answer": "Pneumonia or bronchitis."
            },
            "additional_testing": {
                "question": "For one of your alternative diagnoses, what specific information (test or question) would help rule it in or out?",
                "field_id": "additional-testing",
                "purpose": "Assess diagnostic reasoning and test selection",
                "example_perfect_answer": "For metastatic carcinoma: Order tumor markers (CEA, CA 19-9, PSA), obtain tissue biopsy if possible, and perform CT abdomen/pelvis to look for primary malignancy. The random distribution and lack of primary tumor make this less likely.",
                "example_poor_answer": "More blood tests."
            },
            "critical_conditions": {
                "question": "Have you considered and ruled out any potential 'must-not-miss' or life-threatening conditions?",
                "field_id": "critical-conditions",
                "purpose": "Evaluate safety and critical thinking",
                "example_perfect_answer": "Considered acute respiratory failure, pulmonary embolism, and acute heart failure. Ruled out by stable vital signs, normal cardiac biomarkers, and specific imaging findings. The immunocompromised state made disseminated infection the top priority.",
                "example_poor_answer": "I think I covered everything."
            }
        }

        # ===== GROUND TRUTH INFORMATION =====
        self.ground_truth = {
            "correct_diagnosis": "Miliary tuberculosis",
            "pathophysiology": "Hematogenous dissemination of Mycobacterium tuberculosis throughout the lungs and potentially other organs, facilitated by severe immunosuppression from infliximab therapy",
            "key_diagnostic_features": [
                "Bilateral miliary pattern on chest imaging (pathognomonic)",
                "Positive tuberculosis testing (QuantiFERON-TB Gold)",
                "Immunocompromised state (infliximab therapy)",
                "Constitutional symptoms (fever, weight loss, fatigue)",
                "Progressive respiratory symptoms"
            ],
            "critical_information_blocks": [
                "medications_critical_infliximab",  # Most critical - explains susceptibility
                "imaging_chest_xray",              # Diagnostic imaging pattern
                "imaging_ct_chest",                # Confirmatory imaging
                "labs_tb_testing",                 # Confirmatory laboratory
                "hpi_chief_complaint",             # Clinical presentation
                "exam_respiratory"                 # Physical findings
            ],
            "must_not_miss_differentials": [
                "Metastatic carcinoma with miliary lung metastases",
                "Acute respiratory failure",
                "Pulmonary embolism"
            ],
            "treatment_considerations": "Immediate anti-tuberculosis therapy, isolation precautions, discontinuation of immunosuppressive therapy, contact tracing"
        }

        # ===== BIAS TRIGGERS AND EDUCATIONAL COMPONENTS =====
        self.bias_triggers = {
            "anchoring_bias": {
                "description": "Initial focus on cardiac causes due to shortness of breath and age",
                "trigger_scenario": "Early focus on heart failure or cardiac issues",
                "educational_point": "Don't anchor on common presentations without considering the full clinical context"
            },
            "confirmation_bias": {
                "description": "Seeking only evidence that supports initial impression",
                "trigger_scenario": "Only ordering cardiac tests after initial cardiac impression",
                "educational_point": "Always consider alternative diagnoses and gather comprehensive information"
            },
            "availability_bias": {
                "description": "Focusing on common diagnoses (pneumonia, heart failure) while missing rare but serious conditions",
                "trigger_scenario": "Assuming common respiratory conditions without considering immunocompromised state",
                "educational_point": "Consider patient's unique risk factors and medication history"
            }
        }

    def get_perfect_information_gathering_scenario(self) -> Dict[str, Any]:
        """Generate a perfect information gathering scenario for evaluator testing."""
        return {
            "scenario_type": "perfect_information_gathering",
            "discovered_blocks": [block_id for block_id in self.discovery_blocks.keys()],
            "intents_used": [
                "hpi_chief_complaint",
                "profile_age",
                "profile_language",
                "meds_current_known",
                "meds_ra_specific_initial_query",
                "meds_full_reconciliation_query",  # CRITICAL
                "exam_vital",
                "exam_general_appearance",
                "exam_cardiovascular",
                "exam_respiratory",
                "labs_general",
                "labs_wbc",
                "labs_hemoglobin",
                "labs_bnp",
                "imaging_chest_xray",  # CRITICAL
                "imaging_ct_chest",    # CRITICAL
                "imaging_echo"
            ],
            "diagnosis": "Miliary tuberculosis",
            "metacognitive_responses": {
                question_key: data["example_perfect_answer"]
                for question_key, data in self.metacognitive_questions.items()
            },
            "expected_evaluation_score_range": {
                "information_gathering": 85-95,
                "diagnostic_accuracy": 90-100,
                "cognitive_bias_awareness": 80-95
            }
        }

    def get_poor_information_gathering_scenario(self) -> Dict[str, Any]:
        """Generate a poor information gathering scenario for evaluator testing."""
        return {
            "scenario_type": "poor_information_gathering",
            "discovered_blocks": [
                "demographics_basic",
                "hpi_chief_complaint",
                "exam_vitals",
                "labs_basic"
                # Missing all critical blocks: medications_critical_infliximab, imaging findings
            ],
            "intents_used": [
                "hpi_chief_complaint",
                "exam_vital",
                "labs_general"
                # Missing: medication reconciliation, imaging requests, systematic examination
            ],
            "diagnosis": "Pneumonia",  # Incorrect diagnosis
            "metacognitive_responses": {
                question_key: data["example_poor_answer"]
                for question_key, data in self.metacognitive_questions.items()
            },
            "expected_evaluation_score_range": {
                "information_gathering": 10-30,
                "diagnostic_accuracy": 5-25,
                "cognitive_bias_awareness": 5-20
            }
        }

    def get_biased_scenario(self) -> Dict[str, Any]:
        """Generate a biased reasoning scenario (anchoring on cardiac causes)."""
        return {
            "scenario_type": "biased_anchoring_cardiac",
            "discovered_blocks": [
                "demographics_basic",
                "hpi_chief_complaint",
                "exam_vitals",
                "exam_cardiovascular",
                "labs_cardiac",
                "imaging_echo"
                # Anchored on cardiac workup, missed TB-specific investigations
            ],
            "intents_used": [
                "hpi_chief_complaint",
                "hpi_shortness_of_breath",
                "exam_vital",
                "exam_cardiovascular",
                "labs_bnp",
                "imaging_echo"
                # Missed: medication history, chest imaging, comprehensive examination
            ],
            "diagnosis": "Heart failure with preserved ejection fraction",
            "metacognitive_responses": {
                "supporting_evidence": "Elevated pro-BNP and symptoms of dyspnea suggest heart failure",
                "contradicting_evidence": "Normal ejection fraction on echo doesn't rule out diastolic dysfunction",
                "alternative_diagnoses": "COPD exacerbation or pneumonia",
                "additional_testing": "More cardiac function tests",
                "critical_conditions": "Ruled out acute MI with normal troponins"
            },
            "expected_evaluation_score_range": {
                "information_gathering": 20-40,  # Limited, biased gathering
                "diagnostic_accuracy": 10-30,    # Incorrect diagnosis
                "cognitive_bias_awareness": 15-35 # Shows some reasoning but biased
            }
        }

    def get_comprehensive_test_dataset(self) -> Dict[str, Any]:
        """Get complete dataset for comprehensive evaluator testing."""
        return {
            "discovery_blocks": self.discovery_blocks,
            "clinical_intents": self.clinical_intents,
            "metacognitive_questions": self.metacognitive_questions,
            "ground_truth": self.ground_truth,
            "bias_triggers": self.bias_triggers,
            "test_scenarios": {
                "perfect_gathering": self.get_perfect_information_gathering_scenario(),
                "poor_gathering": self.get_poor_information_gathering_scenario(),
                "biased_reasoning": self.get_biased_scenario()
            },
            "intent_categories": {
                "profile": ["profile_age", "profile_language", "profile_social_context_historian", "profile_medical_records"],
                "history_present_illness": ["hpi_chief_complaint", "hpi_onset_duration_primary", "hpi_associated_symptoms_general", "hpi_fever", "hpi_cough", "hpi_shortness_of_breath", "hpi_chest_pain", "hpi_chills", "hpi_weight_changes"],
                "past_medical_history": ["pmh_general"],
                "medications": ["meds_current_known", "meds_ra_specific_initial_query", "meds_full_reconciliation_query"],
                "physical_exam": ["exam_general_appearance", "exam_vital", "exam_cardiovascular", "exam_respiratory"],
                "diagnostics": ["labs_general", "labs_bnp", "labs_wbc", "labs_hemoglobin", "imaging_chest_xray", "imaging_echo", "imaging_ct_chest", "imaging_general"],
                "general": ["general_greeting", "clarification"]
            }
        }


def main():
    """Main function to demonstrate usage and export test data."""
    extractor = SmartDocTestDataExtract()

    print("=== SmartDoc Comprehensive Test Data Extract ===\n")

    print(f"Discovery Blocks: {len(extractor.discovery_blocks)} total")
    critical_blocks = [bid for bid, data in extractor.discovery_blocks.items() if data.get('is_critical', False)]
    print(f"Critical Blocks: {len(critical_blocks)} - {critical_blocks}\n")

    print(f"Clinical Intents: {len(extractor.clinical_intents)} total")
    intent_categories = {}
    for intent_id, data in extractor.clinical_intents.items():
        category = data['category']
        if category not in intent_categories:
            intent_categories[category] = 0
        intent_categories[category] += 1

    for category, count in intent_categories.items():
        print(f"  {category}: {count} intents")

    print(f"\nMetacognitive Questions: {len(extractor.metacognitive_questions)}")
    for q_id, data in extractor.metacognitive_questions.items():
        print(f"  {q_id}: {data['question'][:60]}...")

    print(f"\nGround Truth Diagnosis: {extractor.ground_truth['correct_diagnosis']}")
    print(f"Critical Blocks for Diagnosis: {len(extractor.ground_truth['critical_information_blocks'])}")

    # Export complete dataset
    dataset = extractor.get_comprehensive_test_dataset()

    with open('/Users/bruno.sena/Projects/personal/masters/smart-doc/dev-tools/comprehensive_test_dataset.json', 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"\n✅ Complete test dataset exported to: comprehensive_test_dataset.json")
    print(f"   Dataset contains {len(dataset)} main categories")
    print(f"   Ready for evaluator test script generation!")

    return dataset


if __name__ == "__main__":
    main()
