# Chapter 4

# Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology

The gaps found during the scoping review, provided in Chapter 3, where the use of conver-sational tools in monitoring symptoms in oncology is minimal, were used to inspire this project. Although a number of digital solutions are suggested, the majority of these tools are based on static and form-based ways of monitoring the symptoms. Conversational systems are still quite uncommon. Only a a single study was found that used a chatbot. However it was a rule-based SMS system with no sophisticated reasoning or dynamic communication. To address these gaps, this project suggests the creation of a system consisting of a conversa-tional chatbot that would provide patients, a way to report and monitor their symptoms, according to CTCAE guidelines, dynamically. The system’s aim is to provide a more natural experience in reporting the symptoms, than the ones found in literature, while maintaining clinical rigor, by combining deterministic dialogue structure, ensuring protocol compliance, with LLM, for ques-tion generation, response evaluation, and symptom grading. The modern TOD frameworks found in Section 2.5 were analyzed to provide the architectural direction. The fully end-to-end architectures were not considered suitable in high-stakes medical settings since they are not transparent, do not limit the reasoning path, and it is hard to validate internal decision-making. In contrast, systems like SGP-TOD and the Script-Based AI Thera-pist proved that combining rule-based structure with LLM enables both linguistic flexibility and control, making hybrid approaches more suitable for medical dialogue systems. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 41

# 4.1 Part I: System Design

This first part presents the architectural principles of the system.

4.1.1 Overview

The system outlined in the current dissertation was inspired directly by the Script-Based AI Therapist [4]. A system that combines LLM with oriented dialogue structures, allowing patients to follow stipulated protocols. The present system also adopts a modular, rule-guided approach aligned with LLM. Each symptom is modeled as a predetermined path graph in which, each node represents a clinical dimension in agreement with CTCAE requirements. The dialogue advances deterministically through these nodes, ensuring that all these dimensions are always covered. At each step, the LLM is used in a modular way: to generate context appropriate questions in natural language, to evaluate whether the patient’s response satisfies the clinical objective and to produce summaries and justifications that support symptom grading. This architecture separates language generation from dialogue control, which enables natural and flexible interactions with the patients, while preserving control of the conversation’s direction. The system is composed of different modules, with the main one being the Dialogue Execu-tion Module , which manages the dialogue process, as it is in charge of walking the patient through the conversation. It’s composed of three components: 1. Node Controller : navigates the symptom’s path graph. It activates each node in the graph, which allows the conversation to flow. 2. Question Generator (LLM) : generates natural language questions based on the objective of the current node. 3. Response Assessor (LLM) : responsible for analyzing if the patient’s response is sufficient to fulfill the node’s objective or requires further clarification. Additional system modules support other key tasks in the workflow: • Symptom Identifier : maps additional patient-reported symptoms in free-text form to exist-ing symptoms present in the CTCAE. • Node Summarisation Module : produces a short clinical summary per node completed. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 42 • Grade Assigner : assigns a CTCAE grade to each of the symptoms reported. • Grade Validator : performs consistency check on the assigned grade. • Medical Report Generation : provides a concise summary of the reported symptoms and aligns the all the session output in a structured medical report.

4.1.2 Symptom Modeling

All clinical relevant dimensions with respect to CTCAE grading were covered by mmod-elingeach of the symptoms in the system as a path graph.

Symptom Modeling and Data Selection There are 837 adverse event terms defined in CTCAE v5.0 developed and maintained by the United States NCI. They represent a wide range of display forms, such as complaints that patients report, laboratory abnormalities, and clinical finding of healthcare professionals themselves. Grading and classification of every event can be based on one or more of these sources of information. Nevertheless, some CTCAE terms cannot be applied in a digital environment, where the pa-tient is responsible for reporting the symptom. A manual search of the entire CTCAE catalogue was carried out to select the subset of symptoms suitable to the structured and language-based reporting. Each AE term was individually evaluated according to two inclusion criteria: • Patient-observable: The symptom should be self-observable and reportable, requiring nei-ther clinical equipment nor clinical knowledge. • Language-expressible: The symptom should be expressible in ordinary, non-technical lan-guage. Symptoms that failed to meet either criterion were discounted. This screening produced 203

eligible symptoms, about 24% of the CTCAE catalog.

Structured Symptom Representation

In the following section, the internal structure of mapping each CTCAE symptom into a set of clinically meaningful information nodes is described. This scheme unites official grading defi-nitions and a detailed dissemination into discrete information nodes, which set up the systematic collection of clinically relevant information. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 43 For each symptom, the following data elements where directly retrieved from the CTCTAE catalog: • The official MedDRA code and SOC corresponding to the CTCAE term; • The definition of the symtpom • The full rubric of CTCAE grading, which include the textual definitions of each grade sever-ity level ( Grade 1 to Grade 4 ). This definitions cover several clinical dimensions of the symptoms, like the intensity, the impact on daily tasks and self-care. Grade 5 , which cor-responds to death does not appear in the representation since it is inapplicable to patient self-reporting; To transform each symptom to the system, every symptom is represented as:

S = ( N, G, M)

where: • N = {n1, n2, . . . , nk} is an ordered list of information nodes, which defines the path graph, where each node, ni, is defined as a tuple (label , description ). The label represent-ing the clinical aspect being assessed, such as “Impact on Self-Care”, and the description providing the semantic basis for question generation. • G = {g1, g2, g3, g4} the official CTCAE grading criteria; • M = ( MedDRA Code , MedDRA SOC , De f inition ) where the definition is what defines the symptom. Though each node is statically characterized by its label and description, it is related, at run time, to a state , either OPEN , CLOSED , or EXPAND , that shows its status of evaluation in the ongoing dialogue process. This state is managed by the Node Controller as the system traverses the symptom-specific path graph. In order to better visualize the inner composition of every symptom, Figure 4.1 illustrates how the symptom Fatigue is structured. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 44

> FIGURE 4.1: Structured Representation of the symptom Fatigue According to CTCAE Criteria.

The information nodes N are specific to symptoms and are defined manually and in line with a detailed decomposition of the CTCAE grading of each symptom. The construction process of N followed a systematic methodology: • Grade analysis: Grade definitions of the CTCAE ( g1 to g4) were analyzed separately in order to determine the clinical findings that correspond to the individual levels of the grades (e.g. response to rest, effects on daily activities, symptom intensity). • Concept extraction: The grading criteria was disaggregated into individual clinical con-cepts. Different grades may have one or several pertinent concepts as they are more or less complicated. • Node definition: One node per concept was defined. Figure 4.1 shows the symptom Fatigue along with the grading criteria G. These clinical re-quirements were broken down into specific conceptual units and related to specific information nodes. Grade 1 is associated with fatigue that is relieved by rest, and as a result it gave rise to the creation of the node Relief with rest where the description of the symptom helps to infer whether the symptom gets relieved by rest or not. Grade 2 refers to Instrumental Activities of Daily Liv-ing (IADLs) limitations which led to the formation of the node Impact on IADLs . Grade 3 is characterized by limitations in self-care, prompting the addition of the node Impact on Self-Care .Other nodes, however are not a direct outcome of the grading criteria but have significant func-tional or contextual roles. To give an example, the node Confirmation appears in each symptom as a technical prerequisite ensuring whether the symptom is present or not to continue with the assessment. In the same regard, the node Symptom Onset does not add an extra value to the CT-CAE grading, but rather provides a good clinical context in terms of capturing the duration and temporal pattern of the symptom. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 45

Protocol Assignment

The system includes pre-structured treatment protocols, each one linked with a curated set of symptoms. The lists of symptoms were retrieved from the official treatment documentation provided by the Instituto Português Oncologia do Porto , thus ensuring its conformity to the clinical monitoring requirements of each treatment protocol. Some of the protocols that are currently assessed in the system are: • CAPOX (Capecitabine + Oxaliplatin) • FOLFOX (Folinic Acid + Fluorouracil + Oxaliplatin) • FOLFIRI (Folinic Acid + Fluorouracil + Irinotecan)

4.1.3 Dialogue Execution: Node Controller, Question Generator, and Response As-sessor

The Dialogue Execution is responsible for the conversation flow. This module has three main components: • Node Controller : a deterministic part which manages the navigation through the symptom path graph, triggering each clinical node, controlling the state of its resolution. • Question Generator : a LLM based component which takes the clinical description of the node and generates a natural language question with the intent of retrieving the correspond-ing clinical information of the patient. • Response Assessor : a LLM based component that assesses the answer of the patient and provides a structured decision on whether the information given meets the clinical goal of the node. In each node ni, the Question Generator takes the description of the node and generates a natural language question, qi, that seeks to capture the clinical information that is represented by the node. The patient’s response, ri, is then evaluated by the Response Assessor , which returns a decision:

di = Decision (ri, qi) ∈ { PRUNE , EXPAND }Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 46 • PRUNE : the answer sufficiently covers the clinical aspect of a node and the Node Controller

updates the graph by marking the node as CLOSED .• EXPAND : the response is insufficient or ambiguous, and the Node Controller updates the state of the node as EXPAND . The Question Generator is responsible for rephrasing the question based of the node’s original description and the gap found, to allow a clarification question to be formulated. Every decision is followed by a justification produced by the Response Assessor that explains the rationale of the classification and, in the case of EXPAND , a short sentence providing the miss-ing details, to provide to the Question Generator to reformulate the follow-up question. The system uses a redundancy filtering mechanism before asking the follow-up question to the patient, where sentence embeddings are calculated using a pretrained embedding model and cosine sim-ilarity between the candidate follow-up and each of the previous questions within the same node is computed, to avoid redundancy between the questions. The dialogue continues only when the node is marked as CLOSED .This node-level decision process is summarised in Algorithm 1.

Algorithm 1 Node-Level Dialogue Execution

Require: Ordered list of information nodes N = {n1, n2, . . . , nk}

Ensure: Each node evaluated and marked as CLOSED when sufficient information is obtained

> 1:

for each node ni ∈ N do

> 2:

Generate question qi ← QuestionGenerator (ni)

> 3:

Present qi to the patient

> 4:

Receive response ri

> 5:

Evaluate decision di ← ResponseAssessor (ni, ri)

> 6:

if di = PRUNE then

> 7:

Mark ni as CLOSED

> 8:

Proceed to the next node

> 9:

else if di = EXPAND then

> 10:

Mark ni as EXPLORE

> 11:

for each follow-up question q′

> i

∈ di.follow_ups do

> 12:

if q′

> i

/∈ PreviousQuestions (ni) then

> 13:

Present q′

> i

to the patient

> 14:

Receive updated response ri

> 15:

Re-evaluate di ← ResponseAssessor (ni, ri)

> 16:

Repeat from Step 6

> 17:

end if

> 18:

end for

> 19:

end if

> 20:

end for Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 47 Figure 4.2 illustrates the structured representation and dynamic evaluation of the symptom

Fatigue . The nodes, represenitng the clinical dimension in the illustration are defined as shown in the representation of the symptom in Figure 4.1. In the process of the dialogue, every node is updated dynamically based on the response provided by the patient. The colour of a node indicates its STATUS : where green is CLOSED , red is EXPAND and yellow is OPEN .

> FIGURE 4.2: Symptom graph traversal for fatigue.

In Panel (A) for the node Frequency , the system queries: “How is your fatigue? Is it constant, intermittent, or does it vary throughout the day?” , to which the patient responds as “I didn’t understand” , which in turn leads to an EXPAND decision with a justification indicating lack of comprehension. As a consequence the node is marked as EXPAND .The node Relief with Rest can be seen in panel (B), with the question: “Have you noticed whether rest helps reduce your fatigue?” . The patient replies: “It doesn’t help” . The response is considered sufficient, leading to a PRUNE decision. The node is then marked as CLOSED .

4.1.4 Symptom Identifier

The system has a specific module to support the reporting of the unexpected or additional symptoms that are not included in the treatment protocol of a patient. The architecture follows a multi-stage design that combines semantic search with LLM-based reasoning. When the patient reports another symptom, the system tries to match it with one of the Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 48 symptoms in the list of CTCAE v5.0 symptoms, manually curated as explained in Section 4.1.2 using both the symptom definitions and their respective MedDRA SOC. The identification pipeline starts with a coarse-grained classification narrowing down the search space to a specific SOC, and subsequent fine-grained semantic similarity search within the nar-rowed group to pick the most relevant symptom. In the event that the system cannot be confident that it found an appropriate match, a fallback mechanism is initiated: rather than attempting to assign an incorrect classification, the system instanciates a generic path graph, with pre-defined, information nodes. These generic nodes will be able to capture baseline clinical data applicable to any symptom which includes: • Symptom Onset : to determine when the symptom began. • Frequency : to understand how often the symptom occurs. • Impact on Daily Life : to assess whether the symptom interferes with instrumental activities of daily living. • Impact on Self-Care : to check if the symptom limits self-care.

4.1.5 Node Summarization

This module transforms the interaction history of each node into a concise clinical statement after all the nodes are marked as CLOSED .In summarization, the following is considered: • the node’s clinical intent; • the full dialogue history within that node (initial and follow-up questions + answers). The output is a short sentence, summarizing the answer given by the patient to the node, retaining the important information in relation to the node’s description . All these summaries are represented as si with i being the index of the associated information node ni.

4.1.6 Grade Assigner

The grading module operates only after all node-level summaries si have been generated by the Node Summarization module. The set of summaries for a given symptom S is represented as: Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 49

HS = {s1, s2, . . . , sk}

The LLM reasons over the collected data and the official CTCAE grading rubric of the symp-tom, which is given as: G = {g1, g2, g3, g4}, to arrive at the final grade. Instead of providing the whole interaction history for the symptom, the choice of using si

relies on the fact that the LLM would not benefit of having long text-input with possibly irrelevant dialogue history. For example, for the following node-level summaries si:• Relief with rest: “The patient reports moderate fatigue not relieved with rest.” • Impact on instrumental activities: “Needs to rest during daily chores but manages to com-plete them.” • Impact on self-care: “No difficulty with personal hygiene or dressing.” Given the CTCAE rubric for fatigue: • Grade 1 : Fatigue relieved by rest. • Grade 2 : Fatigue not relieved by rest; limits instrumental ADL. • Grade 3 : Fatigue severely limits self-care ADL. The model is expected to reason with the different grades and the summaries to conclude that the corresponding grade, in this case corresponds to Grade 2 .Other solutions were also discussed in the design phase such as fine-tuning or LoRA-based adaptation of a language model to directly classify symptom grades. Nevertheless, this methodol-ogy was soon disregarded because of the total lack of annotated data on patient-authored symptom descriptions that are tied to CTCAE levels. Creating such dataset would involve massive expert an-notation, which is associated with data privacy issues as well as significant resource requirements. Prompt-based reasoning was thus chosen as more viable option.

4.1.7 Grade Validator

This module is responsible for ensuring that the symptom specific assigned grade, ˆ g, is con-sistent with both: Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 50 • The grading criteria G;• The node-level summaries HS.The validation mechanism, impelemented using a LLM, produces a structured output that includes not only the validation status, but also a justification for the decision:

ValidateGrade ( ˆg, HS, G) ⇒



CONFIRMED , grade is accepted, with justification

REJECTED , grade is flagged for review, with justification This validation module helps in checking whether each grade assigned is in line with the information gathered in the dialogue and the grading criteria. By explicitly comparing the ˆ g against the set of ( HS) and ( G), the system can detect discrepancies or unsupported classifications. In conflict scenarios, the grade is flagged to review. This module enhances the transparency of the system since all the inputs and decisions made in the grading process are retained and traceable. It acts as a second line of defense to determine whether the grade first set by the grading module is clinically consistent with the data obtained. It does not ensure the validation result to be always accurate, but it gives an additional chance to identify possible inconsistencies or unreasonable grading decisions.

4.1.8 Medical Report

Once the grading and validation of each symptom is completed, this module is responsible for generating a medical report, which includes: • the name of the symptom; • the final grade (from the grading module); • the validation status ( CONFIRMED or REJECTED ); • a clinical summary (one sentence or two sentendes) capturing the patient’s overall symptom complaints; • a set of bullet points highlighting key clinical facts; • the justification for the validation decision. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 51 The system generates the narrative component of the report (summary and bullet points), using a LLM as well as incorporates structured outputs of the grading and validation modules for each of the symptoms. The node-level summaries serve as the basis for generating concise, symptom-level descriptions and bullet points. The grade, validation result and the respective justification are retrieved and added to achieve complete traceability. The report provides an interpretable and clinically meaningful overview of the session as it brings together portions of data that are contained in separate modules providing a clear picture of the session and allowing monitoring downstream clinical decision-making and auditability.

# 4.2 Part II: Technical Implementation

This section presents the technical implementation of the system. While Part I focused on the architectural principles and modular design, this section details how the components were exe-cuted in practice, including runtime configuration, large language model integration, data man-agement, local deployment and data privacy.

4.2.1 Overview and Execution Pipeline

Upon run-time, the system initiates by loading the patient’s protocol (e.g., FOLFOX), which contains a list of symptoms that are supposed to be evaluated (e.g., fatigue, nausea). Each of these symptoms is associated with a predetermined path graph, defined manually consisting of clinically relevant information nodes (see Section 4.1.2). Although the full graph structure is defined statically in JSON, nodes are instantiated dynamically at runtime by the Node Controller ,which loads and activates each node sequentially as the dialogue progresses. The first interaction with the patient occurs in the Dialogue Execution module, when the de-scription of the first node is passed to the Question Generator component. This component will then generate, using a LLM, a natural question that is presented to the patient, aiming to infer the patient’s experience within the clinical dimension of the node. When the patient provides an answer, the Response Assessor is then used to evaluate whether the information given is suffi-cient to fulfill the clinical dimension of the node or if clarification is required. If so, the LLM provides the missing detail, which is used, aligned with the initial node’s description, to prompt the Question Assessor to generate a follow-up question. This process happens iteratively until the response is satisfactory, which is when the Node Controller closes the node. This guarantees that each dimension of the symptom is evaluated, having the desired information for CTCAE grading. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 52 Once all nodes are traversed, the Node Summarization module generates a set of structured summaries (one per node), which will be used to infer the severity grade, by using the Grade Assigner . This module, using the LLM, is instructed to match the summaries of each node to the CTCAE rubric. When all protocol symptoms have been processed, the system prompts the patient to report any additional symptoms in free-text form. Using the Symptpom Identifier , the system either retrieves an identified symptom from the manually curated list along with its nodes or a fallback structure is employed, and the generic nodes to collect relevant clinical information are instanci-ated. In case no other symptoms are to be reported, the Grade Validator is run as a last step prior to the generation of reports. If any of the symptoms, which were additionally reported by patients, but weren’t identified, are present, they don’t undergo the process of grading or validation, as there’s no grading criteria predefined for that symptom. Once all of the validation is performed, the medical report is then generated, with a concise summary, and bullet points for each symptom, as well as the grade and its validation.

Handling of Uncertainty and Indeterminate Responses

In some cases, where patients may be unable to provide an answer to a question (e.g., “I don’t know”, “I can’t remember”). The Response Assessor is designed to treat such uncertain responses as acceptable. In these cases, it issues a PRUNE decision with a justification explaining that no further clarification is feasible under the circumstances. The system acknowledges that uncertainty and memory limitations are inherent to patient self-reporting. Excessive probing in such cases would not enhance data quality and may instead lead to patient fatigue or frustration.

4.2.2 Node Instantiation

All the symptoms have predetermined sets of information nodes, which are stored in structured JSON files.The ordered list of nodes of a certain symptom is presented in each JSON file. As the conversation continues the system loads and instantiates each node dynamically creat-ing a symptom-specific path graph .During runtime, each node has the form of a Python object of the Node class, which is defined with Pydantic to achieve structure and type safety. This selection allows a smooth and secure Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 53 transformation of the predetermined node data, initially saved as JSON, into fully validated Python objects, making the dialogue running chain consistent. A node consists of an identifier, a label , a

description and a state (OPEN , EXPLORE , or CLOSED ) which keeps track of its progress in the dialogue. The label and description are extracted from the JSON file. The state tracks the node’s progress in the dialogue depending on the outcome of the textbfResponse Assessor. The full path graph is thus a sequential, dynamically constructed list of such node objects, which is supervised by the Node Controller module.

4.2.3 Symptom Identifier Pipeline: Embeddings and LLM Verification

A hybrid RAG pipeline was implemented in case the patient wishes to report additional symp-toms. It is not a usual RAG application. The solution consists of semantic similarity search (sentence embedding) and reasoning (LLM) to ensure proper identification of the symptoms. The identification of the additional symptom is performed over the manually curated list, where they are organized by its SOC (e.g., “Gastrointestinal disorders” or “Nervous system dis-orders”). To allow similarity-based retrieval, semantic embeddings are calculated through the

nomic-embed-text model.

Embedding Index Construction

Two FAISS-based semantic indices were created: • SOC Embedding Index: The MedDRA SOC names were appended with their respective symptoms names. Thus, generating compound strings, which represent the semantic asso-ciation between individual SOC and its symptoms. • Symptom Embedding Index: The CTCAE symptoms were all embedded through concate-nation of the name, the clinical definition, and the grading criteria (Grades 1-4).

Pipeline Execution

The end-to-end pipeline consists of the following steps, which put together semantic retrieval with structured LLM verification and fallback reasoning: Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 54 1. FAISS Embedding Search: A top-k = 4 similarity search is applied to symptom embedding index to retrieve the most semantically relevant candidate symptoms for the free-form input of the patient. 2. LLM-Based Verification: A large language model is used to verify each candidate by means of a structured prompt. The LLM gives an output of YES only when the given symp-tom is clinically compatible with the description. 3. Fallback: SOC-Based LLM Classification:

• The LLM is prompted with a shorter list of MedDRA SOC that have not been tried. • It picks the most suitable SOC according to the free-text description of the patient. • The symptoms of that SOC are passed to the LLM which identifies the most likely candidate. • The selected symptom is then verified again through the same YES/NO process. • This loop repeats and updates the list of available SOCs, until a verified symptom is found, or all SOCs are done. 4. Final Decision: If no match is verified, the system concludes that no suitable candidate was found and returns "not found" as the outcome.

4.2.4 Evaluation of Symptom Retrieval System

A large language model was used to generate a tailored collection of 450 free-text patient descriptions in order to aid the analysis of symptom retrieval and recognition. These descriptions were obtained in order to represent the variability of the natural language and to mimic realistic oncological symptoms descriptions. All entries were then manually checked to ensure clinical plausibility, linguistic variation, and congruency to expected symptom terms. Three versions of the system were tested: • Embedding-Only Baseline: Similarity search over pre-computed symptom embeddings using FAISS, without any LLM reasoning during retrieval. • LLM-Only (SOC + Symptom Selection): A pipeline relying solely on LLM-based rea-soning to first narrow down to a System Organ Class (SOC), and then to select a symptom, without using semantic embeddings. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 55 • Hybrid Ensemble (Final Pipeline): The multi-stage pipeline described, which combines embedding retrieval, SOC-based narrowing, and LLM-based verification.

Performance Results

> TABLE 4.1: Accuracy comparison across retrieval strategies

Pipeline Version Accuracy (%)

FAISS Embedding-Only 25.06 LLM Only 47.20 Hybrid Ensemble (Final Pipeline) 57.27 The hybrid pipeline reached the best test accuracy of 57.27% thus validating the use of inte-grating semantic similarity retrieval with LLM-based reasoning in symptom identification. It was through empirical testing that the choice was made to make the symptom identification process based on SOC. Experiments done on earlier versions without usinc SOC, just using all the available symptoms, tended to give false positives as the system tended to equate certain similar symptoms with respect to meaning but clinically very different (e.g. abdominal pain vs. chest pain). Additionally, the retrieving of the symptom was also longer. Regardless of the retrieval path, embeddings or fallback, all candidate symptoms undergo a final LLM verification step using the patient’s original description, decreasing the chance of false positives.

4.2.5 LLM Integration

All LLM inference is performed locally using Ollama .A number of open-source models were benchmarked to evaluate their applicability to the sys-tem needs, which requires structured output, natural phrasing in portuguese from Europe and good reasoning skills. The candidates tested were: • llama3.1:8b , llama3.2:latest

• deepseek-r1:latest , deepseek-r1

• qwen2.5:14b , qwen2.5:7b Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 56 The model qwen2.5:7b was ultimately selected for all core reasoning tasks including question generation, node decision-making, grading and validation. It was shown to have the best tradeoffs in the quality of generation, run-time performance and structure output consistency. Specifically, the 7B version consistently produced valid and structured JSON outputs, responded within accept-able latency thresholds (<2 seconds handled Portuguesedling portuguese reliably. Only open-source LLM were considered, as they can be deployed locally without the use of an API, thus they are not dependent on external servers.

Prompting Framework and Configuration

The entirety of language model interactions was executed through the LangChain framework, which features modular templates of prompts, and temperature parameter control per module, which determines how random or deterministic the output of the model can be. The lower the value of the temperatures (e.g., 0.0), the more deterministic the model will be, and it will promote similar and reproducible results. With increased values (e.g. 0.7 or greater), there is added variability and more diverse answers can be generated. This parameter is of great importance in this system, as each module require different behaviours: • Grading and Validation: low temperature ( 0.1 ) to ensure reproducibility. • Question Generation: high temperature ( 0.7 ) for more natural, conversational phrasing. • Summarisation and Reporting: moderate temperature ( 0.3 ) to allow stylistic variation while preserving accuracy.

Structured Output Parsing

Due to the use of open-source models used locally the system did not benefit from function calling or strict output schema enforcement. As a result, a dedicated post-processing and validation pipeline was implemented to extract structured outputs from raw model outputs. 1. Direct Parsing Attempt: The raw output of the model is firstly parsed in raw shape as JSON. In case of success, no subsequent measures are needed. 2. Regex Pre-Extraction: If parsing fails, then regular expressions may be used to extract the most probable JSON block out of the text, compensating the possible extraneous ex-planations, formatting artifacts, or incomplete bracket closure which sometimes may be introduced by generative models. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 57 3. Pydantic Schema Validation: That data is then validated against a Pydantic schema, that is specific to the particular structured output needed by the task. 4. Retry Mechanism: In case any of the preceding steps fail, the system will automatically re-populate model with identical data and this can be done several times (4 retries) to achieve a compliant structured answer. 5. Failure Mechanism: In worst case scenarios when all parsing and recovery fails, the system implements conservative fall back mechanisms in order to achieve stability of the dialog and clinical safety. Regarding the node-level decision modules, a fallback EXPAND is issued when the node should not be closed immediately, but the system should rather keep on collecting informa-tion of the patient. In modules like grading, validating, summaries and bullet point extraction, safe place hold-ers are shown (e.g. summary unavailable, grade: not available), so that no clinical conclu-sions are made based on a missing valid structured data source. In free-form symptom description cases, in the case of any parsing failure in the process of candidate extraction, the instantiation of generic information nodes is triggered directly, so that the structured collection of data is also an option.

Lexical Normalisation Layer for PT-PT Compliance

A lexical post-processing layer has been deployed in order to guarantee linguistic adherence to european portuguese. All the outputs generated by the LLM are intercepted prior to presentation, and are the subject of specific replacements of frequent brazilian- portuguese derived lexical items. It is a rule-based system with a manually created dictionary of replacements which includes many common regionalisms and clinical terms. These could be seen in the replacement of "abdô-men" by "abdómen" , and "banheiro" by "casa de banho" .

4.2.6 Deployment and Runtime Environment

The whole system is implemented on a lightweight and modular stack that is focused on local execution and data privacy along with ease of deployment. It is implemented as a web application using the Flask framework, with SQLite for structured data persistence, and containerised via Docker for portability and reproducibility. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 58

Flask and Database Backend

The application logic is realized withFlask, a lightweight Python web framework which is suitable to rapid development and flexible deployment in web systems. Flask routes are used to control user interactions at every user level (patients, clinicians and administrators). The session state and conversation history is maintained in memory at run time but regularly written back into the database. The permanent storage of data is implemented with local SQLite database.

Containerisation and Local Execution

The system is packaged in a single Docker container built on the python:3.10-slim base image. This container combines all the in order to run the application as explained in Table 4.2.

> TABLE 4.2: Main functional components within the application container

Component Role within the Container

Gunicorn Serves the Flask application with multiple worker pro-cesses, enabling concurrent sessions

Ollama Executes the local LLM and embedding models with GPU acceleration

SQLite For storing data

Cron Handles scheduled tasks such as automated backups and log rotation

Startup Sequence and Hosting Infrastructure

The system is hosted on a dedicated Ubuntu 24.04.2 LTS production server with GPU support enabled via the NVIDIA Container Toolkit. The startup process involves the following two steps to ensure all components are operational before any user session begins: 1. Model Services: Starts Ollama serve in the background and loads both qwen2.5:7b and

nomic-embed-text into GPU memory. 2. Backend Launch: Runs the Flask application via Gunicorn to expose the web interface. The container exposes the Flask server internally on port 5000 , externally mapped to 8000 .Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 59

Persistent Storage and Operational Logging

Two persistent Docker volumes are mounted: • Database Volume: This stores the complete SQLite database file that the system has inte-grated. • Logs Volume: Gathers multiple-level time-stamped logs that logs detailed events and traces of the system operations. This includes:

– Server errors and flask backend runtime errors.

– Failures in routes when interacting with the different users.

– Failure traces and inference responses of the LLM.

– Ollama server diagnostics and LLM runtime messages.

– Errors on transcription services and failure in voice synthesis (from Edge TTS and Whisper models). This ensures the safety of the data associated with patients and all other events of the opera-tions as they are stored securely in case the container restarts, and enables detailed debugging of inference processes and route handling.

4.2.7 Database Architecture and Data Persistence

Based on the simplicity and native file-based persistence support, SQLite was selected to be used as the database.

Relational Structure

Every patient is singularly mapped with the one physician. This forms a firm one-to-many relationship. Every session which is stored under the table sessions is specific to a patient. The table session \_symptoms is also connected directly to sessions, and it will keep infor-mation about each symptom that was assessed in the conversation with the chatbot. The entire trace of dialogue of each symptom is kept in the field info_json , which includes the complete dialog history for the symptom, grade assigned, node-level interaction history (including the de-cision/justification/ given by the LLM), structure of the executed dialogue path, the validation of the grade given by the LLM, and the generated clinical summary including bullet points. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 60 The patient_protocols table contains the assigned treatment protocol, which links a par-ticular patient with a protocol. Automatically assigned grades which are subsequently changed manually are saved in the

grade_overrides table, along with a justification. Administrative users are stored separately from clinical users. Authentication credentials are securely hashed and stored in the password_hash field within all the users. The Figure 4.3 represents the schema of the database.

> FIGURE 4.3: Relational database schema.

Persistence Mechanisms The system uses a form of incremental persistence in an active ses-sion: everything on dialogue state, symptom history and decisions is written to the database after each patient input. This guarantees that all information relating to the reporting of the symptoms is safely saved in case of system failure.

4.2.8 Data Protection, Security and Clinical Safety

The system was developed based on main principles of data protection that have been pro-vided by General Data Protection Regulation (GDPR) [130] mainly focusing on privacy, access controls, auditability, and clinical safety. Although there is no regulatory certification, the fol-lowing mechanisms are used to assure proper processing of sensitive clinical data within scope of GDPR, including Article 5(1)(f) (integrity and confidentiality), Article 5(2) (accountability), and Article 32(1) (security of processing). Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 61

Privacy and Access Control The Personal health information (PHI) such as patient identity, clinical history, and the information on symptoms are visible to users who passed the authenti-cation and authorization procedure based on their role (patient, clinician, administrator). Hashed passwords using bcrypt are stored so that the risks to credential exposure are limited.

Local Data Storage The entire data is saved locally on a SQLite database wrapped within a Docker container. LLM use is local, so there is no use of API. Web Speech API has however been employed on the frontend interface which is a browser-native API for speech recognition and speech synthesis. This element can internally use third-party services (based on the browser and device settings of the user), but the backend application won’t store or share any audio record of any kind.

Auditability and System Logging A logging subsystem stores the timestamps of operational events within the system. This allows traceability of the system’s execution and behaviour .

Clinical Safety with Human in the Loop Oversight Any symptom classification that the LLM produces is validated in a two-tier process. Firstly, the system uses consistency checks through re-analysis with the LLM of the grading results. Then, clinicians can check and validate all clas-sifications through the medical review dashboard and have access to the LLM justifications and session history. Any grade override is justified by the clinicician and stored for future auditing and accountability.

Session Timeout due to Inactivity As a counter measure against unauthorized access within unattended sessions, an inactivity timeout mechanism has been incorporated. The system will automatically log out a user and send him to the authentication page in case of the absence of user interaction (with a keyboard, mouse, or touch) in 8 minutes. This guarantees that sensitive data concerning remains secure.

4.2.9 User Interfaces and Interaction Design

This section shows the graphical user interfaces that have been designed and the different functions integrated. The system has three main parts that consist of patient, medical and admin-istrator interface. Flask is used as the backend organization of all the components, and frontend Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 62 logic was developed with the help of HTML, Bootstrap, CSS and JavaScript. All the patients that are mentioned are ficticious.

Authentication and Access Control

Users are required to undertake a secure log in before they can access the patient, medical, or administrative interfaces. Every user has to use valid credentials that are a combination of unique identifier (the national health number in the case of patients, predetermined identifiers for clinicians and administrators), and a password. The login screen is shown in Figure 4.4. Since the login process is the same in any user role, only the medical view is shown.

> FIGURE 4.4: Log in screen.

The system provides password reset function, through the link "Esqueceu-se da password?" to aid account recovery. This process is identical for all user roles and consists of the following steps, as illustrated in Figure 4.5. • Step 1: After clicking in the link, the user will then be asked to type in their identifier; • Step 2: A code will be sent to user’s email, which has a 6 digit verification code, valid for 5 min; • Step 3: The user has to enter the code to the interface; Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 63 • Step 4: After the code verification, the user can change the password and is then redirected to the login screen.

> FIGURE 4.5: Password recovery process: (1) request with identifier, (2) email with 6-digit code, (3) code verification screen, (4) password reset form.

Users are only redirected to their respective interfaces (patient, clinician, or administrator) after a successful authentication and can then communicate with the system.

Patient Interface

The patient interface was designed to support a natural and accessible dialogue experience, enabling symptom reporting through both text and voice. The design of the interface is based on the classic structure of a conversational chatbot with alternating system inquiries followed by patient answers as they occur in natural dialogue. Patients are only able to enter one response at a time, and only after the system has issued the following question. Besides the primary conversation flow, the chat interface has a floating action button in a corner of the screen. By clicking on it, a menu will be opened that allows access to standard actions: • Create new chat : instantly ends the current session and opens a new one; • Historic : opens a modal window history of sessions, where it’s possible to see past interac-tions; • Logout : logs the patient out of the system. This interface can be seen in Figure 4.6. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 64

Voice Interaction Flow To make the system more accessible and natural to communicate with, it has an integrated voice interaction functionality. This aspect is adopted through Web Speech API and enables the patients to interact with the chatbot by responding verbally instead of using a text response. For patients that are marked with visual dificulties, the session starts with the voice mode activated. It only works when supported by the user’s device and browser. When voice mode is activated, shown by element 2 in Figure 4.6, the system follows a struc-tured loop: 1. The question on hand is read by the system through speech synthesis; 2. Once the utterance completes, it automatically switches to speech recognition and waits to hear a response; 3. When the patient speaks, the reply is transcribed and processed just like it has been typed; 4. In the event that no response is given or detected, the system restates the question maximum 4 times before returning to typing mode; Also, the system gives clear auditory and visual feedback to indicate the voice mode, by, when enabled, anouncing “voice mode activated”, and shows on the lower corner of the screen a message informing the user that he can now speak, as illustrated by the element 3 in Figure 4.6. Likewise, turning off the voice mode does the same but announces "voice mode deactivated" and removes the visual message. An example of the interface during active voice mode is shown in Figure 4.6.

> FIGURE 4.6: Patient interface: symptom reporting session. (1) Menu of actions; (2) voice mode button; (3) voice mode status.

Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 65

Session History Access Patients also have access to a session history interface which displays a chronological log of previous sessions, and upon selecting one, the history is shown. This allows users to revisit past answers. The following Figure 4.7 represents the session history (A) and chat history (B).

> FIGURE 4.7: Patient interface: session history.

Post-Session Redirect and Main Menu Interface After completing a session, the patient is automatically redirected to the main menu interface. This interface provides access to the same features of the floating action button in the patient’s chat interface.

Medical Interface

The medical interface provides a dashboard to go through the patient sessions and confirm the symptom grading. When they log in, the healthcare professionals are shown a list of all patients. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 66 A visual alert badge is shown on each patient card when any sessions are unreviewed, with the number of sessions that lack review, and a second alert displayed when the grade is >2. The interface can be observed in Figure 4.8.

FIGURE 4.8: Medical interface. (1) Patient panel with badges where sessions are still unreviwed. (2) Patient card with a session still unreviwed and with se-vere symptoms. (3) Sesssions panel with date and symptoms filter. Session 102 presents a badge meaning it is still unreviwed. (4) Symptoms panel with all of the symptoms tested during the dialog with the patient, along with the validation results. The button "Editar Graus" enables the grade’s override. (5) Summary and bullet points of the symptoms. (6) This section enables the exportation of the med-ical report including the PDF and also enables the option to copy to clipboard.

On the top of the page is a red notification bell, as seen in Figure 4.8 that highlights new or pending sessions. Clicking on it a drop down menu appears, consisting of the session information and the symptoms. The following Figure 4.9 showcases the notification bell. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 67

> FIGURE 4.9: Notification bell.

Session Navigation and Symptom Overview When a session is chosen, a structured summary of the all reported symptoms appears in the right panel, shown in Figure 4.8(4). Every symptom consists of: • The CTCAE grade assigned by the LLM; • A summary of the conversation; • A list of bullet points; Clinicians have access to the full dialogue history rendered in the same format used in the patient interface. There is an edit button through which they can automatically override the suggested grade and a reason as to why it is being changed. This is shown in Figure 4.10.

> FIGURE 4.10: Editing the grade and justification provider.

Clinical Analytics View The analytics panel is also involved in the dashboard, through which clinicians have an overview of statistical symptom frequency and grade distribution. They are shown in form of charts which can be seen in the Figure 4.11. This includes: Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 68 • Bar chart : frequency of each grade for the selected symptom; • Line chart : symptom severity evolution across sessions.

> FIGURE 4.11: Bar and line charts.

Structured Summary and Export Options For each symptom, the summary includes the final CTCAE grade, a concise summary, bullet-pointed facts extracted from the dialogue, the LLM validation status, and an explanatory justification for the grade validation. Whenever the status is DISAGREEMENT a warning icon appears next to the symptom, prompting the clinician to review, and when the status is CONFIRMED a validating icon also appears, as shown in Figure 4.8. Clinicians can export this structured information in two ways: • A report exported in PDF :• Clipboard Copy: A modal interface that allows copying the report via two formats:

– Plain text : readable information for direct review;

– JSON : structured data format suitable for integration with external systems. An example of the medical report is shown in the Appendix B, and the copy functionality is illustrated in the Figure 4.12. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 69

> FIGURE 4.12: Copy to clipboard functionality.

Administrator Interface

The administrator interface allows complete access to the patient’s and medical’s management, as shown in Figure 4.13.

> FIGURE 4.13: Administrator panel.

After selecting one of the options, the administrator is present with list of all registered users. After that the available functionalities include: • Registration: Create new patients and physicians. • Editing and Deletion: Edit or delete patients and physicians by clicking in the user. • Search and Filtering: Search and filter patients and physicians by name, health number (for patients), medical code (for physicians) or email. • Physician and protocolAssignment: Associate the physician and protocol to the patient when creating a patient. Chapter 4. Developing a Clinical Chatbot for Structured Symptom Reporting in Oncology 70 The patient’s and physician’s management interface is alike, therefore only the patient’s man-agement interface will be displayed in Figure 4.14.

FIGURE 4.14: Patient’s management.interface. (1) List of all the patients, includ-ing a search bar and an add patient button. (2) Patients’ registration form, where the demographic and also the clinical information is entered. It’s in this process that the physician and protocol are assigned. (3) Patients’ edit form. (4) Continu-ation of the edit form with the option to delete de user. 71
