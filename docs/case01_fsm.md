# 1. Dialogue States

- **INTRODUCTION**
- **CHIEF_COMPLAINT_EXPLORATION**
- **HPI_GATHERING** (History of Present Illness)
- **PMH_GATHERING** (Past Medical History)
- **MEDICATION_REVIEW** (including allergies)
- **SOCIAL_HISTORY_GATHERING**
- **FAMILY_HISTORY_GATHERING**
- **REVIEW_OF_SYSTEMS (ROS)**
- **PHYSICAL_EXAM_QUERY**
- **INVESTIGATIONS_QUERY** (Labs, Imaging)
- **(Implicit) DIFFERENTIAL_DIAGNOSIS_FORMATION**
- **REASSESSMENT**
- **CLOSING/SUMMARY**

# 2. Dialogue State Descriptions

**1. INTRODUCTION State**
_ **Student Input Examples:** "Hello", "My name is Dr. X", "Can you tell me what brought you to the hospital?"
_ **Possible Intents:**
_ `greet`
_ `introduce_self`
_ `initiate_interview` (could overlap with querying chief complaint)
_ **Possible Entities:** (Student's name, if provided)

**2. CHIEF_COMPLAINT_EXPLORATION State**
_ **Student Input Examples:** "What's the main problem?", "Why did you come to the ED?", "Tell me about what's bothering you."
_ **Possible Intents:**
_ `query_chief_complaint`
_ **Possible Entities:** (None typically from student input here, the VSP provides them based on `case01.json`)

**3. HPI_GATHERING State**
_ **Student Input Examples:** "When did the shortness of breath start?", "Does anything make the cough worse?", "How severe is the dyspnea?", "Are you feeling tired?"
_ **Possible Intents:**
_ `query_symptom_onset` (Entity: specific symptom like `shortness of breath`)
_ `query_symptom_duration` (Entity: specific symptom)
_ `query_symptom_severity` (Entity: specific symptom)
_ `query_symptom_quality` (Entity: specific symptom)
_ `query_symptom_alleviating_factors` (Entity: specific symptom)
_ `query_symptom_aggravating_factors` (Entity: specific symptom)
_ `query_associated_symptoms` (e.g., "Any fever with the cough?")
_ **Possible Entities:** (Symptoms from `case01.json` like `shortness of breath`, `cough`, `decreased oral intake`, `weight loss`, `fever`, `chills`, `chest pain`)

**4. PMH_GATHERING State**
_ **Student Input Examples:** "Do you have any medical conditions?", "Have you ever been hospitalized?", "Any surgeries in the past?", "Are you diagnosed with diabetes?"
_ **Possible Intents:**
_ `query_past_medical_history`
_ `query_specific_condition` (Entity: `diabetes`, `hypertension`, `rheumatoid arthritis`)
_ `query_hospitalizations`
_ `query_surgeries` \* **Possible Entities:** (`diabetes`, `hypertension`, `rheumatoid arthritis`, `obesity`)

**5. MEDICATION_REVIEW State**
_ **Student Input Examples:** "What medications are you taking?", "Are you on lisinopril?", "Any allergies?", "What do you take for your arthritis?"
_ **Possible Intents:**
_ `query_medications`
_ `query_specific_medication` (Entity: `lisinopril`, `atenolol`, `infliximab`)
_ `query_medication_for_condition` (Entity: `rheumatoid arthritis`)
_ `query_allergies`
_ `query_medication_adherence`
_ **Possible Entities:** (Medication names from `case01.json`, `allergies`, names of conditions)

Okay, understood. We'll proceed by outlining the intents and entities for the remaining dialogue states, adhering to standard clinical interview practices.

Let's continue where we left off:

**6. SOCIAL_HISTORY_GATHERING State**
_ **Context from `case01.json`:** Elderly, Spanish-speaking, son provides history, morbid obesity.
_ **Student Input Examples:** "Who lives at home with you?", "Do you have support at home?", "Do you smoke or drink alcohol?", "What is your occupation?" (though less relevant for an elderly, acutely ill patient), "Can you describe your diet usually?".
_ **Possible Intents:**
_ `query_living_situation`
_ `query_social_support`
_ `query_tobacco_use`
_ `query_alcohol_use`
_ `query_drug_use` (illicit)
_ `query_occupation`
_ `query_dietary_habits`
_ **Possible Entities:** `home`, `family`, `support`, `smoking`, `cigarettes`, `alcohol`, `drinks`, `occupation`, `work`, `diet`, `food`.
_ **VSP Note:** For this case, information on social history is limited in the source PDF beyond the son's involvement. The VSP might respond with "Her son is her primary support and is with her now," or "She lives with her son," for relevant questions. For habits like smoking/alcohol, if not in the JSON, a response like "The son reports she does not smoke" or "That information isn't immediately available from the son" could be used for the prototype.

**7. FAMILY_HISTORY_GATHERING State**
_ **Student Input Examples:** "Any medical conditions run in your family?", "Does anyone in your family have heart problems or diabetes?", "Is there a family history of arthritis?"
_ **Possible Intents:**
_ `query_family_history_general`
_ `query_family_history_specific_condition` (Entity: `heart disease`, `diabetes`, `cancer`, `arthritis`)
_ **Possible Entities:** `family`, `mother`, `father`, `siblings`, `children`, `heart problems`, `diabetes`, `cancer`, `arthritis`, `stroke`, `hypertension`.
_ **VSP Note:** Family history is not detailed in the provided clinical scenario. The VSP would likely state, "The son does not have detailed information about her extended family history at this moment" or similar.

**8. REVIEW_OF_SYSTEMS (ROS) State**
_ **Context:** This is a systematic head-to-toe review for symptoms not already discussed. The son already denied chest pain, fevers, or chills.
_ **Student Input Examples:** (Students usually go system by system) "Any headaches or dizziness?" (Neurological), "Any nausea or vomiting?" (GI), "Any urinary problems?" (Genitourinary), "Any rashes or skin changes?" (Integumentary), "Any joint pain or swelling not already discussed?" (Musculoskeletal).
_ **Possible Intents:** (These can be broad or specific)
_ `query_ros_general` (e.g., "Are you having any other problems or symptoms we haven't talked about?")
_ `query_ros_constitutional` (Entities: `fever`, `chills`, `weight loss`, `fatigue` - weight loss already noted)
_ `query_ros_neurological` (Entities: `headache`, `dizziness`, `weakness`, `numbness`)
_ `query_ros_heent` (Head, Eyes, Ears, Nose, Throat - Entities: `vision changes`, `hearing loss`, `sore throat`, `nasal discharge`)
_ `query_ros_cardiovascular` (Entities: `chest pain`, `palpitations`, `edema` - chest pain denied, no edema noted)
_ `query_ros_respiratory` (Entities: `cough`, `shortness of breath`, `wheezing` - primary complaints)
_ `query_ros_gastrointestinal` (Entities: `nausea`, `vomiting`, `diarrhea`, `constipation`, `abdominal pain`, `decreased appetite` - decreased intake noted)
_ `query_ros_genitourinary` (Entities: `dysuria`, `frequency`, `hematuria`)
_ `query_ros_musculoskeletal` (Entities: `joint pain`, `swelling`, `muscle pain` - RA known, hand deformities noted)
_ `query_ros_integumentary` (Skin - Entities: `rash`, `lesions`, `itching`)
_ `query_ros_psychiatric` (Entities: `mood changes`, `anxiety`, `depression`)
_ **Possible Entities:** Names of any common symptoms related to each system.
_ **VSP Note:** The VSP should use information from `case01.json`. For example, if asked about chest pain again, reiterate "She denies chest pain." For new queries not covered, like "nausea," the VSP might respond, "Her son doesn't report any nausea."

**9. PHYSICAL_EXAM_QUERY State**
_ **Context:** The student isn't performing the exam but asking for the findings. Initial ED findings are in `case01.json`.
_ **Student Input Examples:** "What are her vital signs?", "What did you find on the lung exam?", "Are there any heart murmurs?", "Check her abdomen."
_ **Possible Intents:**
_ `request_vital_signs`
_ `request_general_appearance_exam`
_ `request_cardiac_exam_findings`
_ `request_pulmonary_exam_findings`
_ `request_abdominal_exam_findings`
_ `request_neurological_exam_findings`
_ `request_extremity_exam_findings`
_ `request_skin_exam_findings`
_ `request_specific_exam_finding` (Entity: `JVP`, `crackles`, `edema`, `hand deformities`)
_ **Possible Entities:** `vitals`, `temperature`, `heart rate`, `blood pressure`, `respiratory rate`, `oxygen saturation`, `heart sounds`, `murmur`, `JVP`, `lungs`, `crackles`, `wheezes`, `abdomen`, `tenderness`, `edema`, `skin`, `rash`, specific body parts or exam maneuvers.
_ **VSP Note:** VSP provides findings directly from `initialPresentation.physicalExaminationInitialED` in `case01.json`. If a finding isn't listed (e.g., detailed abdominal exam), the VSP can state, "That specific finding was not explicitly noted in the initial emergency department assessment," or "The focus was primarily on the cardiorespiratory system initially."

**10. INVESTIGATIONS_QUERY State**
_ **Context:** Student asks for results of tests. Initial ED labs and CXR are in `case01.json`. Later discoverable tests (Echo, CT chest) are also listed.
_ **Student Input Examples:** "What did the blood tests show?", "What's her white blood cell count?", "How was the chest x-ray?", "Have you done an echocardiogram?", "Any other imaging?"
_ **Possible Intents:**
_ `request_lab_results_general`
_ `request_specific_lab_result` (Entity: `WBC`, `hemoglobin`, `creatinine`, `pro-BNP`)
_ `request_imaging_results_general`
_ `request_specific_imaging_result` (Entity: `chest x-ray`, `echocardiogram`, `CT scan`)
_ `request_other_investigations` (e.g., ECG, sputum culture before it's done)
_ **Possible Entities:** Names of lab tests (`CBC`, `WBC`, `hemoglobin`, `creatinine`, `pro-BNP`), imaging modalities (`chest x-ray`, `echocardiogram`, `CT scan`), other tests (`ECG`, `sputum culture`, `bronchoscopy`).
_ **VSP Note:** VSP provides results from `initialPresentation.laboratoryDataInitialED` and `initialPresentation.imagingInitialED`. For discoverable tests like the echocardiogram or CT chest, the VSP should initially state they are not yet available or haven't been done, then reveal them if the `triggerForVSPRevelation` conditions (from `case01.json`) are met later in the interview. E.g., "An echocardiogram was ordered, but the results are not back yet."

**11. (Implicit) DIFFERENTIAL_DIAGNOSIS_FORMATION State**
_ **VSP Role:** The VSP does not form a differential but provides information. However, the system could later track student queries to see if they are narrowing down or broadening their differential appropriately. For the prototype, this is mainly for the student.
_ **Student Input Examples (might be self-talk or questions reflecting this):** "Could this be pneumonia?", "What about a PE?", "Is heart failure the most likely diagnosis?"
_ **Possible Intents (for more advanced VSP):**
_ `propose_differential`
_ `query_likelihood_of_diagnosis`
_ **VSP Note for Prototype:** Typically responds with "I can only provide you with the patient's history and findings" or "What are your thoughts?" or if later a metacognitive prompt: "What is your leading hypothesis now?"

**12. REASSESSMENT State**
_ **Context:** This state is entered if new information comes up (e.g., VSP reveals infliximab use or normal echo) or if the student wants to clarify previous points.
_ **Student Input Examples:** "Given the normal echo, what else could cause the dyspnea?", "Now that I know she's on infliximab, I'm more concerned about infection.", "Can you remind me of her vital signs?"
_ **Possible Intents:**
_ Many intents from previous states could be re-used (e.g., `query_symptom_details`, `request_lab_results`).
_ `clarify_previous_information`
_ `query_impact_of_new_finding` (Entity: new finding like `infliximab`, `normal echo`) \* **Possible Entities:** Any previously discussed entity or new critical finding.

**13. CLOSING/SUMMARY State**
_ **Student Input Examples:** "I think I have all the information I need.", "My assessment is X, and I'd like to order Y.", "Thank you."
_ **Possible Intents:**
_ `conclude_interview`
_ `summarize_findings` (student summarizes to VSP)
_ `propose_diagnosis_plan` (student states their leading diagnosis and plan)
_ `thank_patient` \* **VSP Note:** VSP can acknowledge, provide a closing statement ("Thank you for your thoroughness. This concludes the initial interview simulation.") or lead to a feedback module in later versions.
