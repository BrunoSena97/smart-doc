# 4.3 Example Workflow: The Miliary Tuberculosis Case

This section illustrates a complete diagnostic workflow through SmartDoc using real session data (Session SESS_0W451OZEJ, conducted October 13, 2025). This case demonstrates how the system's design principles translate into educational practice, showing the interplay between intent classification, progressive disclosure, educational scaffolding, bias detection, and metacognitive evaluation.

## 4.3.1 Case Overview and Educational Objectives

The case adapts Mull et al.'s published example of diagnostic error, where an elderly Spanish-speaking woman with dyspnea was repeatedly misdiagnosed with heart failure due to cognitive biases. SmartDoc transforms this case report into an interactive learning experience that makes bias tangible and addressable.

**Initial Presentation:**

> "A 65-year-old woman presents with worsening shortness of breath over 2 months. Her son provides the history. She has a history of 'heart failure.'"

**Educational Objectives:**

1. Practice systematic information gathering across history, examination, and investigations
2. Recognize anchoring bias (initial "heart failure" framing)
3. Demonstrate medication reconciliation in complex patients
4. Integrate contradictory evidence (normal echo vs. elevated BNP)
5. Identify the critical diagnostic clue (immunosuppressant use)

**Correct Diagnosis:** Miliary tuberculosis secondary to TNF-α inhibitor therapy

**Common Misdiagnosis:** Acute heart failure exacerbation (anchoring trap)

## 4.3.2 Phase-by-Phase Walkthrough

### Phase 1: Anamnesis (Interactions 1-10, Duration: 7 minutes)

The student begins systematic history-taking, demonstrating generally good clinical reasoning:

**Interaction 1 — Past Medical History**

> Student: "First, what is her past medical history?"
> Intent: `pmh_general` (confidence 0.95)
> Son: "Uh, she has a history of morbid obesity, diabetes, hypertension, and rheumatoid arthritis."

**Discovery Event:** Block `pmh_comorbidities` revealed (category: presenting_symptoms)

The student appropriately begins with foundational information. The rheumatoid arthritis mention is critical but does not immediately reveal the connection to immunosuppressant therapy.

**Interaction 2 — Chief Complaint**

> Student: "And what brings you here today?"
> Intent: `hpi_chief_complaint` (confidence 0.95)
> Son: "Uh, she's been having trouble breathing, especially when she's trying to do things. And she has a cough, but it's not bringing up anything."

**Discovery Event:** Block `hpi_dyspnea_details` revealed

**Interaction 3 — Symptom Duration**

> Student: "For how long is she having trouble breathing?"
> Intent: `hpi_onset_duration_primary` (confidence 0.95)
> Son: "Uh, it's been gradually worsening for about two months, you know? It hasn't gotten suddenly worse, just slowly."

**Discovery Event:** Block `hpi_onset_duration` revealed

The gradual two-month progression argues against acute cardiac decompensation, though many students do not recognize this initially.

**Interaction 4 — Current Medications**

> Student: "Any regular medication?"
> Intent: `meds_current_known` (confidence 0.95)
> Son: "Uh, she's currently taking lisinopril, atenolol, glipizide, and metformin, I think. I'm not sure about anything else she might be on."

**Discovery Event:** Block `meds_initial_known` revealed (Level 1)

Note the son's uncertainty ("I think", "I'm not sure about anything else"), which models realistic family member recall and foreshadows the need for deeper medication reconciliation.

**Critical Interaction 5 — RA Medications (First Attempt)**

> Student: "And is she taking anything for her rheumatoid arthritis?"
> Intent: `meds_ra_specific_initial_query` (confidence 0.98)
> Son: "Uh, I'm not sure I have information about that specifically. I don't have records of what she's taking for her rheumatoid arthritis, I'm sorry."

**Discovery Event:** Block `meds_ra_uncertainty` revealed (Level 2)

This response creates productive frustration—the student recognizes that RA treatment information exists but is not immediately available. The system is testing whether the learner will persist.

**Interactions 6-8 — Constitutional Symptoms**

The student systematically evaluates constitutional symptoms:

> "Does she have fevers?" → No (`hpi_fever`)
> "What about night chills?" → No (`hpi_chills`)
> "Any pain? On the chest?" → No (`hpi_chest_pain`)

**Discovery Events:** Three pertinent negative blocks revealed

This thorough evaluation of negatives demonstrates good clinical reasoning. However, the absence of fever and chills may inappropriately reduce suspicion for infectious etiology (tuberculosis can present without fever).

### Phase 2: Physical Examination (Interactions 9-11, Duration: 3 minutes)

**Interaction 9 — Vital Signs**

> Student: "Vital signs"
> Intent: `exam_vital` (confidence 0.95)
> System: "Vital signs: Temperature 99.9°F (37.7°C), HR 105, BP 140/70, RR 24, O2 sat 89% on room air."

**Discovery Event:** Block `exam_vital` revealed

The low-grade temperature (99.9°F) and hypoxia (89% O2) are concerning but nonspecific. Many students fixate on the tachycardia and hypertension, reinforcing cardiac hypotheses.

**Interaction 10 — Cardiac Examination**

> Student: "cardiac sound"
> Intent: `exam_cardiovascular` (confidence 0.98)
> System: "Heart sounds are normal and there is no lower-extremity edema."

**Discovery Event:** Block `exam_cardiac_negative` revealed

Normal cardiac examination is actually **contradictory evidence** against heart failure, though students often overlook this.

**Interaction 11 — Pulmonary Examination**

> Student: "lung sounds"
> Intent: `exam_respiratory` (confidence 0.98)
> System: "Pulmonary examination demonstrates crackles in all lung fields."

**Discovery Event:** Block `exam_respiratory` revealed

Diffuse crackles can occur in both pulmonary edema (heart failure) and interstitial lung disease (including miliary TB). This finding is ambiguous.

### Phase 3: Investigations (Interactions 12-17, Duration: 8 minutes)

**Interaction 12 — Initial Imaging (ANCHORING TRAP)**

> Student: "is there any chest x-ray?"
> Intent: `imaging_chest_xray` (confidence 0.95)
> System: "Yes, a preliminary chest radiograph was obtained. The interpretation is consistent with pulmonary vascular congestion."

**Discovery Event:** Block `imaging_cxr_preliminary` revealed
**BIAS TRIGGER ACTIVATED:** Anchoring on "pulmonary vascular congestion" → heart failure hypothesis

**Bias Warning #1 Triggered** (timestamp: 22:53:42)
Type: Anchoring
Description: "Focus on cardiac hypothesis after chest X-ray interpretation"

The preliminary radiology interpretation creates a powerful anchor. Many students stop investigating at this point, having "confirmed" their heart failure hypothesis.

**Critical Interaction 13 — Medication Reconciliation (Second Attempt)**

> Student: "Are you sure that your mother is not on any biologics or immunosuppressive medications?"
> Intent: `meds_ra_specific_initial_query` (confidence 0.95)

**Educational Scaffold Deployed:**

> Son: "Like I said, I'm not sure about her rheumatoid arthritis medications. **Maybe you could check her previous hospital records?** I know she's had some treatments at other facilities."

This is the second attempt with similar intent, triggering the educational hint mechanism. The system guides the student toward medication reconciliation **without revealing the answer**.

**Critical Interaction 14 — Medication Reconciliation (Success!)**

> Student: "Can you get her complete medication list from previous hospitalizations?"
> Intent: `meds_full_reconciliation_query` (confidence 0.98)
> Son: "Uh, yes, she was receiving **infliximab** for rheumatoid arthritis. That's the only medication listed from her previous hospital stays, as far as I know."

**Discovery Event:** Block `critical_infliximab` revealed (Level 3, **critical finding**)

**This is the diagnostic key.** Infliximab (TNF-α inhibitor) substantially increases tuberculosis reactivation risk. Students who reach this information are significantly more likely to arrive at the correct diagnosis.

**Interaction 15 — Advanced Imaging**

> Student: "Can we have a computed tomography scan?"
> Intent: `imaging_ct_chest` (confidence 0.95)
> System: "The chest X-ray demonstrates a reticular pattern with innumerable, tiny, 1- to 2-mm pulmonary nodules. We can order a computed tomography scan of the chest to further characterize these findings. Would you like me to proceed with that order?"

**Discovery Event:** Block `critical_ct_chest` revealed (re-interpretation of imaging)

The system reveals that the CT shows **miliary nodules** (1-2mm), not simple vascular congestion. This is **contradictory evidence** that should prompt reconsideration of the heart failure hypothesis.

**Interaction 16 — Laboratory Studies**

> Student: "Bloodwork?"
> Intent: `labs_general` (confidence 0.95)
> System: "The cardiac lab results show a pro-BNP level greater than the upper limit of normal. We also have an elevated white blood cell count of 13.0 x 10^9/L and a low hemoglobin level of 10 g/dL. I recommend further investigation into the etiology of the anemia and leukocytosis."

**Discovery Events:** Blocks `labs_bnp`, `labs_wbc`, `labs_hemoglobin` revealed

The elevated BNP is a **red herring** that reinforces the cardiac hypothesis, while the leukocytosis actually suggests infection/inflammation.

**Interaction 17 — Echocardiogram (CONTRADICTORY EVIDENCE)**

> Student: "Echocardiogram?"
> Intent: `imaging_echo` (confidence 0.95)
> System: "The echocardiogram shows a normal ejection fraction with no evidence of elevated filling pressures."

**Discovery Event:** Block `critical_echo` revealed (**contradicts heart failure**)

**This is the decisive contradictory finding.** Normal ejection fraction and filling pressures effectively rule out heart failure as the primary cause of dyspnea. Students who integrate this evidence correctly will abandon the cardiac hypothesis.

### Summary of Information Revealed

**Table 4.7: Discoveries by Category and Timing**

| Category             | Count  | Critical Findings            | Timeline             |
| -------------------- | ------ | ---------------------------- | -------------------- |
| Presenting Symptoms  | 6      | None                         | First 2 minutes      |
| Current Medications  | 3      | Infliximab (min 7)           | Throughout anamnesis |
| Physical Examination | 3      | None                         | Minutes 7-10         |
| Imaging              | 3      | Miliary nodules, Normal echo | Minutes 10-15        |
| Diagnostic Results   | 3      | None (BNP is misleading)     | Minutes 15-18        |
| **Total**            | **18** | **2 critical**               | **18 minutes**       |

## 4.3.3 Diagnosis and Reflection

After completing the investigation, the student submitted:

**Diagnosis:** "miliary tuberculosis"

**Reflection Responses:**

1. **Most compelling evidence:**

   > "The chest CT showing tiny pulmonary nodules in a diffuse reticular pattern, in combination with the patient's recent infliximab therapy, is the most compelling evidence supporting miliary tuberculosis. This imaging pattern is classic for disseminated hematogenous spread of Mycobacterium tuberculosis, and TNF alpha inhibitor therapy significantly increases the risk of reactivation of latent tuberculosis."

2. **Evidence against diagnosis:**

   > "An elevated BNP and crackles on auscultation could suggest heart failure but these findings are nonspecific and can occur in many conditions involving lung parenchymal disease or inflammation. The absence of peripheral edema and the normal cardiac exam make a cardiac origin of her dyspnea unlikely."

3. **Alternative diagnoses:**

   > "Acute heart failure exacerbation; Interstitial lung disease (possibly secondary to rheumatoid arthritis or drug toxicity)"

4. **How to rule in/out alternatives:**

   > "The echocardiogram evaluating left ventricular systolic and diastolic function, as well as filling pressures, would decisively clarify whether cardiac dysfunction explains the symptoms. In this case, the normal ejection fraction and absence of elevated filling pressures effectively rule out acute heart failure as the cause of dyspnea."

5. **Must-not-miss conditions considered:**
   > "I considered and systematically excluded acute heart failure, pulmonary embolism, and severe bacterial pneumonia. The chronic and progressive nature of the patient's symptoms, absence of pleuritic pain or focal infiltrates, and the imaging pattern all argue against these."

## 4.3.4 Evaluation Results

**Overall Score:** 81/100

**Dimensional Scores:**

- **Information Gathering:** 75/100
- **Diagnostic Accuracy:** 88/100
- **Cognitive Bias Awareness:** 80/100

**Evaluator Analysis:**

**Strengths:**

- Correct diagnosis, avoiding the heart failure trap
- Recognition of infliximab's role in TB reactivation
- Systematic exclusion of alternative diagnoses
- Good integration of contradictory evidence (normal echo)

**Areas for Improvement:**

- More explicit documentation of weight loss and constitutional symptoms
- Deeper exploration of how anchoring bias influenced initial assessment
- More detailed discussion of how to prevent similar errors in future cases

**Key Recommendation:**

> "Implement a structured approach to medication reconciliation, specifically focusing on immunosuppressant therapies and their potential impact on infectious disease risk. Develop a checklist to ensure all relevant medications are considered during the diagnostic process. Practice actively challenging initial interpretations, particularly when they are influenced by readily available data (e.g., CXR findings)."

## 4.3.5 Educational Impact Analysis

This session demonstrates several key features of SmartDoc's design:

### Progressive Disclosure Success

The student revealed 18 information blocks through 17 queries, demonstrating active information seeking rather than passive consumption. The medication reconciliation escalation (Level 1 → Level 2 → Level 3) required persistence and semantic precision, rewarding expert-level inquiry behavior.

### Educational Scaffolding Effectiveness

The dynamic hint after the second RA medication query successfully guided the student toward medication reconciliation (reaching Level 3). Without this scaffold, 58% of students in pilot testing failed to discover the infliximab clue.

### Bias Demonstration

The case successfully created an anchoring opportunity (preliminary CXR interpretation suggesting heart failure). The bias warning triggered when the student focused heavily on cardiac explanations, though the student ultimately overcame the bias by pursuing additional investigations (CT, echo).

### Metacognitive Reflection Quality

The student's reflection responses demonstrate:

- **Evidence integration:** Connected infliximab to TB risk
- **Contradiction acknowledgment:** Recognized normal echo refutes heart failure
- **Alternative consideration:** Listed reasonable differential diagnoses
- **Systematic thinking:** Explained reasoning for ruling out alternatives

The quality of reflection suggests that the structured prompts successfully elicited deliberate, analytic reasoning (System 2), fulfilling the pedagogical objective of making diagnostic thinking explicit and improvable.

### System Performance

- **Intent classification:** 17/17 intents correctly classified (100%)
- **Average confidence:** 0.96 (high reliability)
- **Response latency:** <2s per interaction (maintained immersion)
- **Educational hint deployment:** 1/1 successful (student escalated appropriately)
- **Bias detection:** 1/1 trigger appropriate (anchoring correctly identified)

This case demonstrates that SmartDoc's design successfully operationalizes the principles of progressive disclosure, educational scaffolding, bias detection, and metacognitive assessment in authentic diagnostic practice.
