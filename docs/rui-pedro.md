#### University of Minho

#### School of Engineering

### Rui Pedro Neto Reis

### AI in White Coat: Utilizing Large

### Language Models for Medical Interviews

october 2024



#### University of Minho

#### School of Engineering

### Rui Pedro Neto Reis

### AI in White Coat: Utilizing Large

### Language Models for Medical Interviews

#### Masters Dissertation

#### Integrated Master’s in Informatics Engineering

#### Dissertation supervised by

#### Pedro Rangel Henriques

#### Nuno Rodrigues

october 2024


**Copyright and Terms of Use for Third Party Work**

This dissertation reports on academic work that can be used by third parties as long as the internationally
accepted standards and good practices are respected concerning copyright and related rights.

This work can thereafter be used under the terms established in the license below.

Readers needing authorization conditions not provided for in the indicated licensing should contact the
author through the RepositóriUM of the University of Minho.

### License granted to users of this work:

##### CC BY-NC

https://creativecommons.org/licenses/by-nc/4.0/

```
i
```

**Acknowledgements**

I am deeply grateful to my wife, Romana Araújo, for her unwavering love and support throughout this
process. Her constant encouragement and patience have been a source of strength and inspiration, and
I am truly thankful for everything she has done for me.

I want to express my heartfelt thanks to my supervisor, Pedro Rangel Henriques, and my co-supervisor,
Nuno Rodrigues, for their invaluable guidance and expertise. Their wisdom and insights have been instru-
mental in shaping and refining my research, and I am deeply appreciative of their mentorship and support.

A special thanks to Joana Mesquita for her crucial contributions for helping develop the user interfaces
in Flutter. Her expertise was vital to the success of this project, and I am deeply grateful for her support.

I am also grateful to my friends, who have provided valuable support and encouragement throughout
this process. Thank you all for being there for me and for being such an important part of my life. I am
truly grateful for your friendship and support, and I could not have completed this project without you.

```
ii
```

**Statement of Integrity**

I hereby declare having conducted this academic work with integrity.

I confirm that I have not used plagiarism or any form of undue use of information or falsification of results
along the process leading to its elaboration.

I further declare that I have fully acknowledged the Code of Ethical Conduct of the University of Minho.

University of Minho, Braga, october 2024

Rui Pedro Neto Reis

```
iii
```

**Abstract**

Hospital emergency departments are often overwhelmed with patients, making it crucial for healthcare
professionalstoefficientlygatheraccuratepatientinformationduringtheanamnesisprocess. However, the
current system is time-consuming and prone to errors due to the high workload and stress levels faced by
medical staff. This Master’s thesis explores the development and implementation of an intelligent system
utilizing Large Language Models (LLMs), such as ChatGPT, to simulate the role of a medical professional
during anamnesis. By enhancing the patient-doctor interaction with AI-driven interviews, this system aims
to streamline the information collection process, reduce cognitive load on healthcare professionals, and
improve the quality of patient data gathered.
The proposed system leverages advanced dialogue management techniques and integrates text and
speech modalities to conduct comprehensive and contextually relevant anamnesis sessions. It employs
a graph-based task-oriented dialogue model to ensure the conversation remains focused and structured,
dynamically adapting to the patient’s responses. The system has been evaluated through a series of tests,
demonstrating its ability to extract critical patient information effectively and generate structured medical
reports, which can assist healthcare providers in making informed decisions more rapidly.
Preliminary results indicate that the AI-powered anamnesis system can significantly reduce the time
required for patient interviews while maintaining high levels of accuracy and completeness in the data
collected. By automating routine aspects of medical interviews, the system has the potential to alleviate
pressure on medical staff and improve patient care outcomes. This research contributes to the broader
field of AI in healthcare by showcasing a practical application of LLMs in a high-stakes environment,
highlighting the potential for future developments in AI-assisted clinical decision support systems.

**Keywords** Large Language Models, Medical Anamnesis Simulation, Patient-Doctor Interactions, Health-
care Technology, Clinical Decision Support, AI-Powered Clinical Interviews

```
iv
```

**Resumo**

Os serviços de urgência hospitalares estão frequentemente sobrecarregados com pacientes, tornando
crucial que os profissionais de saúde recolham de forma eficiente informações precisas dos pacientes
durante o processo de anamnese. No entanto, o sistema atual é demorado e suscetível a erros devido
à elevada carga de trabalho e aos níveis de stress enfrentados pela equipa médica. Esta dissertação
de Mestrado explora o desenvolvimento e implementação de um sistema inteligente que utiliza Modelos
de Linguagem de Grande Escala (LLMs), como o ChatGPT, para simular o papel de um profissional de
saúde durante a anamnese. Ao melhorar a interação entre paciente e médico com entrevistas conduzidas
por IA, este sistema visa otimizar o processo de recolha de informações, reduzir a carga cognitiva dos
profissionais de saúde e melhorar a qualidade dos dados recolhidos dos pacientes.
O sistema proposto utiliza técnicas avançadas de gestão de diálogo e integra modalidades de texto e
fala para conduzir sessões de anamnese abrangentes e contextualmente relevantes. Emprega um modelo
de diálogo orientado a tarefas baseado em grafos para garantir que a conversa se mantenha focada e
estruturada, adaptando-se dinamicamente às respostas do paciente. O sistema foi avaliado através de
uma série de testes, demonstrando a sua capacidade de extrair eficazmente informações críticas dos
pacientes e gerar relatórios médicos estruturados, que podem auxiliar os profissionais de saúde a tomar
decisões informadas de forma mais rápida.
Os resultados preliminares indicam que o sistema de anamnese assistido por IA pode reduzir significa-
tivamente o tempo necessário para as entrevistas com os pacientes, mantendo altos níveis de precisão e
completude nos dados recolhidos. Ao automatizar aspetos rotineiros das entrevistas médicas, o sistema
tem o potencial de aliviar a pressão sobre a equipa médica e melhorar os resultados dos cuidados ao
paciente. Esta pesquisa contribui para o campo mais amplo da IA na saúde ao apresentar uma aplicação
prática de LLMs num ambiente de alto risco, destacando o potencial para futuros desenvolvimentos em
sistemas de apoio à decisão clínica assistidos por IA.

**Palavras-chave** Modelos de Linguagem de Grande Escala, Simulação de Anamnese Médica, Inter-
ações Paciente-Médico, Tecnologia em Saúde, Suporte à Decisão Clínica, Entrevistas Clínicas com IA

```
v
```

## Contents




- I Introductory Material
- 1 Introduction
   - 1.1 Motivation
   - 1.2 Objectives
   - 1.3 Research Hypothesis
      - 1.3.1 Improved Accuracy and Efficiency in Anamnesis.
   - 1.4 Development Approach
   - 1.5 Document Structure.
- 2 Background
   - 2.1 Medical Anamnesis
      - 2.1.1 Medical Algorithms.
   - 2.2 Large Language Models.
      - 2.2.1 Fine-tuning.
      - 2.2.2 Soft Prompting.
      - 2.2.3 Hard Prompting
      - 2.2.4 Retrieval Augmented Generation
      - 2.2.5 Remarks
   - 2.3 Task Oriented Dialogue
      - 2.3.1 Key Terms in TOD Systems
      - 2.3.2 Distinctive Features of TOD
      - 2.3.3 Dialogue State Tracking (DST).
      - 2.3.4 Challenges in TOD
      - 2.3.5 Machine Learning in Task-Oriented Dialogue.
      - 2.3.6 Taking advantage of LLMs
- 3 AI in Anamnesis
   - 3.1 Task-Oriented Dialogue and Anamnesis
      - 3.1.1 Mental Health Applications
      - 3.1.2 Physical Health and Chronic Condition Management
      - 3.1.3 Knowledge-Graph-Driven Systems for Multi-Domain Dialogues
   - 3.2 Limitations of Current Task-Oriented Dialogue Systems.
   - 3.3 Advancements and Future Directions
- II Core of the Dissertation
- 4 System Design
   - 4.1 Introduction to the Task-Oriented Dialogue Framework
      - 4.1.1 Overview of Task-Oriented Dialogue in Anamnesis
      - 4.1.2 System Components and Modular Architecture
      - 4.1.3 Integration of Large Language Models for Medical Dialogue
   - 4.2 Graph State Tracking for Task-Oriented Dialogue
      - 4.2.1 Graph Structure
      - 4.2.2 Cold Start
      - 4.2.3 Decision-Making at Nodes
      - 4.2.4 Overview.
   - 4.3 Algorithmic Clustering for Initial Question Selection.
      - 4.3.1 Data Collection and Preprocessing
      - 4.3.2 Clustering Using Hierarchical K-Means
   - 4.4 Termination Logic.
      - 4.4.1 Calculating Termination Scores and Node Closure
      - 4.4.2 Adaptive Stop Criteria.
      - 4.4.3 Failsafe Mechanism
   - 4.5 Medical Report Generation
      - 4.5.1 Structuring the Report Using the DAG
      - 4.5.2 Grouping and Summarizing Patient Responses
      - 4.5.3 Generating a Symptomatic Summary
   - 4.6 Overview
- 5 Development
   - 5.1 Backend
      - 5.1.1 Large Language Models
      - 5.1.2 Database
      - 5.1.3 Storage
      - 5.1.4 Deployment
   - 5.2 User Interface
      - 5.2.1 Multi-Platform
      - 5.2.2 Interaction
      - 5.2.3 Deployment
- 6 Osler Apps, An Overview
   - 6.1 Patient
      - 6.1.1 Logging In and Account Registration
      - 6.1.2 Landing Screen: Choosing an Action
      - 6.1.3 Starting a New Medical Interview
      - 6.1.4 Reviewing Conversation History.
      - 6.1.5 Ending the Interaction
   - 6.2 Physician.
      - 6.2.1 Viewing Pending Medical Reports
      - 6.2.2 Editing Medical Reports
      - 6.2.3 Copying Medical Reports
      - 6.2.4 Submitting Medical Reports.
- 7 Results and Discussion
   - 7.1 Experiment Overview
      - 7.1.1 Tasks
      - 7.1.2 Evaluation Methods
      - 7.1.3 Participants
   - 7.2 Results for Each Application.
      - 7.2.1 Patient Application
      - 7.2.2 Physician Application.
   - 7.3 Discussion of Results
      - 7.3.1 Patient Application
      - 7.3.2 Physician Application.
   - 7.4 Limitations and Future Work.
- 8 Conclusion


**List of Figures**

```
1 LoRA reparametrization technique,Ais shapedd×r, whileBis shapedr×d, such
thatr≪d. [Hu et al., 2021]............................. 11
2 Comparison of Model Fine-tuning versus Prompt Tuning (Soft Prompting). [Lester et al.,
2021]........................................ 13
3 Chain-of-thought prompting enables LLMs to tackle complex arithmetic, commonsense,
and symbolic reasoning tasks. [Wei et al., 2023].................... 14
4 Ensemble Refinement (ER) involves conditioning a LLM on multiple generated reasoning
paths for improved answer refinement. [Singhal et al., 2023].............. 14
5 Intelligent agents operate and communicate system-wide using established subscription
and publication methods to interact with the environment. [Hong et al., 2023]..... 15
6 Pipeline from extracting and injecting factual medical knowledge from textbooks into
LLMs. [Wang et al., 2023b].............................. 16
7 Illustration of a Finite State Manager in Task-Oriented Dialogue Systems......... 18
8 Illustration of Output Generated by a Dialogue State Tracking-Trained Model....... 19
9 DiagGPT follows a four-stage workflow: Develop Thinking Topics, Maintain Topic Stack,
Enrich Each Topic, and Generate the Response. [Cao, 2023].............. 21
10 Dialogue Management System Diagram. [Mo et al., 2023]............... 22
11 Knowledge graph dialogue state enhanced with probabilistic logical programming, fol-
lowed by neural model scoring for effective response generation. [Walker et al., 2023]. 23
12 Domains of Research and Associated Subcategories for the Application of Task-Oriented
Dialogue in Healthcare. [Valizadeh and Parde, 2022]................. 25
13 Example of a Direct Acyclic Graph (DAG) generated by the system, illustrating the se-
quence of questions and their relationships....................... 43
14 Interaction Flow Diagram................................ 54
```
```
x
```

15 High-level system interaction flow between the Patient Application, Medical Report, and
Physician Application.................................. 56

16 The Login Screen for the Patient Application, where users can log in or register a new
account........................................ 68
17 The Registration Screen for new users signing up for the Patient Application....... 68
18 The Landing Screen, displaying the two main options: starting a new medical interview
or viewing the conversation history........................... 69
19 The Start Screen, where the Osler system initiates the medical interview with an audio
prompt......................................... 70
20 The Speak Screen, indicating that the system is recording the patient’s response during
the medical interview.................................. 71
21 The Conversation History Screen, displaying a list of the patient’s previous medical in-
terviews with the system................................ 72
22 The Conversation Details Screen, where the full message exchange from a previous med-
ical interview is displayed................................ 73
23 The Physician Application Landing Screen, displaying a list of all pending medical reports
awaiting review..................................... 74
24 The Edit Report Screen, where physicians can modify the contents of the medical report,
adding or removing details as needed.......................... 75
25 The Copy to Clipboard feature, allowing the physician to copy the contents of the edited
medical report for use in other systems......................... 76

26 Distribution of participants across different age groups and genders........... 83
27 Distribution of participants across different digital competence groups.......... 83

```
xi
```

**List of Tables**

```
1 NASA-TLX results for the patient application (0–100 scale; higher values indicate greater
workload)....................................... 84
2 SUS results for the patient application (1–5 scale for questions; final score 0–100, higher
final score is better).................................. 85
3 QUIS results for the patient application (1–9 scale; higher values indicate greater satis-
faction)........................................ 86
4 Additional feedback results for the patient application (1-5 scale)............. 87
5 NASA-TLX results for the physician application (0–100 scale; higher values indicate
greater workload).................................... 88
6 SUS results for the physician application (1–5 scale for questions; final score 0–100,
higher final score is better)............................... 89
7 QUIS results for the physician application (1–9 scale; higher values indicate greater
satisfaction)...................................... 90
8 Additional feedback results for the physician application (1-5 scale, higher is better)... 91
```
```
xii
```

xiii


# Part I

# Introductory Material


### Chapter 1

**Introduction**

As a new era of medical care unfolds, a confluence of informatics and advanced technologies, partic-
ularly Large Language Models (LLMs), is witnessed reshaping the foundational aspects of healthcare.
Anamnesis, a time-honored practice of collating patients’ medical histories, is at the epicenter of this
transformation. This Master’s work seeks to illuminate the intersections of anamnesis, informatics, and
LLMs, probing their collective potential in redefining contemporary healthcare. Through this exploration,
the project’s aim is to understand the prospects of employing specialized LLMs in medical interviews, a
pivotal initiative of the Osler project, and envisage a future of patient-centric and efficient anamnesis.
Anamnesis, or the gathering of a patient’s medical history, is pivotal for optimal patient care and
treatment. It enables healthcare providers to make informed decisions and can lead to improved patient
health outcomes. A structured approach to medical anamnesis is crucial to ensure the correctness of the
gathered information, as inaccuracies can lead to misdiagnoses and improper treatment plans [Sabin,
2022 ]. The importance of structured approaches is particularly evident in sensitive areas such as sexual
anamnesis, requiring specialized training and methodologies [Ruck et al., 2023 ]. Anamnesis is not merely
a procedural activity but a collaborative act, allowing the exploration and understanding of what counts as
illness [Zucchermaglio et al., 2016 ].

### 1.1 Motivation

Healthcare systems, particularly hospital emergency departments, are increasingly overwhelmed by the
volume of patients requiring attention. One critical bottleneck in this setting is the anamnesis process,
where medical professionals gather a patient’s history. The process, while essential for accurate diagnosis
and treatment, is time-consuming and prone to errors, particularly in high-stress, high-pressure environ-
ments. The key challenge addressed in this dissertation is how to enhance the efficiency and accuracy
of anamnesis without overburdening healthcare professionals. In an era where technology, specifically


artificial intelligence (AI), is revolutionizing various sectors, there is a need to explore its potential in as-
sisting medical staff with routine but essential tasks like anamnesis. This research focuses on how Large
Language Models (LLMs) can help streamline the collection of patient data, reducing cognitive load and
improving decision-making in emergency departments.
While there is a growing body of research on AI applications in healthcare, most existing studies focus
on diagnosis and treatment recommendations, with little attention paid to the critical, yet labor-intensive,
task of anamnesis. Current AI-based healthcare systems largely overlook the integration of dialogue man-
agement systems tailored for medical interviews, and there is a gap in literature that specifically addresses
the use of LLMs in this context. This dissertation seeks to bridge that gap by designing an AI-powered
system that can effectively simulate a medical interview, providing structured, relevant information for
healthcare providers.
The broader significance of this research lies in its potential to not only transform hospital emergency
departments but also contribute to a growing movement toward AI integration in healthcare. By automating
routine processes such as anamnesis, healthcare professionals can focus on more complex and critical
tasks, ultimately improving patient care and outcomes. Furthermore, the insights generated from this
study could lead to advancements in other areas of clinical decision support, extending the impact of this
work beyond its initial focus.
The objectives of this research are clear: to develop and implement an AI-based system capable of
conducting a structured medical interview, to evaluate its effectiveness in real-world settings, and to explore
its potential in improving the accuracy and efficiency of patient data collection. These objectives directly
align with the identified research problem, aiming to offer a solution that can be seamlessly integrated into
existing healthcare workflows.
To address these goals, this dissertation employs a task-oriented dialogue framework integrated with
LLMs, a novel approach in the medical domain. Unlike traditional AI applications that focus on static data
analysis, this approach emphasizes dynamic, real-time interactions with patients. The use of graph-based
models ensures the system remains focused and efficient, adapting to patient responses while avoiding
unnecessary or redundant questions. This innovative combination of dialogue management techniques
and LLMs represents a significant advancement over existing methods, justifying the chosen approach for
this research.


### 1.2 Objectives

The main goals of this thesis are to explore and develop Large Language Models (LLMs) designed for
medical interviews, with an emphasis on their adaptability and communication skills. The aim is to create
a model that can simulate natural, human-like interactions during anamnesis, aiding in the acquisition
of precise and comprehensive patient information. The synthesis of multimodal interactions and the ex-
haustive evaluation of the model in real-world settings are also paramount to ensure the model’s reliability,
effectiveness, and accessibility.
Building on the motivation presented earlier and aligned with the broader objective outlined, the spe-
cific goals are as follows:

- **Exploration of LLMs** : Investigate the potential applications of existing Large Language Models in
    medical interviews, focusing on their ability to facilitate natural, human-like interactions.
- **Model Development and Refinement** : Construct and refine a model specialized in performing
    anamnesis, capable of asking contextually relevant questions to gather crucial patient information.
- **Multimodal Interaction** : Incorporate textual and speech recognition and synthesis modalities to
    ensure more accessible and comprehensive interaction with patients.
- **Testing and Evaluation** : Conduct thorough assessments of the developed model with small
    groups of physicians to evaluate its effectiveness, accuracy, and interaction quality.

### 1.3 Research Hypothesis

This dissertation aims to explore the transformative role of Large Language Models (LLMs) in enhanc-
ing anamnesis within healthcare. The research will systematically test the following hypothesis through
empirical studies, qualitative analyses, and real-world applications.

#### 1.3.1 Improved Accuracy and Efficiency in Anamnesis.

It is hypothesized that integrating LLMs into the anamnesis process will significantly improve the accuracy
and efficiency of patient medical history collection compared to traditional methods. These improvements
are expected due to the advanced data processing and contextual understanding capabilities of LLMs.


### 1.4 Development Approach

The development approach was structured to ensure a progressive and coherent flow from conceptualiza-
tion to implementation. Initially, a thorough literature review and technology assessment were conducted
to lay the foundation for the creation of a specialized model. This model was carefully designed to facilitate
natural and context-aware interactions during anamnesis. The integration of various interaction modalities
broadened the model’s accessibility and enriched the interaction experience. Finally, extensive testing and
refinements were undertaken to ensure the model’s robustness and reliability in real-world settings, guided
by performance insights and feedback.
With that in mind, the development process was broken down into the following tasks:

- **Literature Review and Technology Assessment** : Conduct a comprehensive study of LLMs
    and their applications, focusing on interaction capabilities and adaptability in medical contexts.
- **Model Development** : Develop a specialized model for anamnesis based on identified require-
    ments, with an emphasis on natural interactions and contextual questioning.
- **Integration of Multimodal Interactions** : Implement textual and speech interaction modalities,
    optimizing for broader accessibility and a richer interaction experience.
- **Testing and Evaluation** : Carry out extensive real-world testing and refine the model based on
    performance insights and feedback.

### 1.5 Document Structure.

The initial chapter of this dissertation provides a comprehensive exploration of the contextual framework
pertinent to this study. This involves elucidating the anamnesis process and imparting fundamental in-
sights into Large Language Models (LLMs), mentioning techniques such as fine-tuning, soft-prompting,
and hard-prompting employed to elicit desired responses from the LLM. Furthermore, key concepts are
introduced, encompassing Task Oriented Dialogue (TOD), Dialogue State Tracking (DST), and Knowledge-
Grounded Dialogue (KGD), which play a pivotal role in ensuring goal-oriented interactions coupled with
enhanced explainability, shedding light on the rationale behind the actions of the LLM.
Chapter 2 and Chapter 3 provide the necessary background to assure a self-contained reading of
the dissertation and delves into a comprehensive examination of the current state of the art within the
aforementioned concepts. This exploration encompasses an in-depth analysis of existing literature on


anamnesis, Large Language Models, fine-tuning methodologies, and the role of techniques such as soft-
prompting and hard-prompting. Additionally, the contemporary landscape of Task Oriented Dialogue (TOD),
Dialogue State Tracking (DST), and Knowledge-Grounded Dialogue (KGD) are scrutinized, evaluating their
contributions to the development of the system under consideration.
Chapter 4 introduces the exploratory system design, which includes a patient application and a physi-
cian application, both designed for the efficient collection of feedback from health professionals. At the
core of this framework is the Large Language Model (LLM) system, which features Task-Oriented Dia-
logue (TOD) and Dialogue State Tracking (DST) techniques, operating on a graph-guided, goal-oriented
foundation. Chapter 5 discusses the development of the core of the system, while Chapter 6 provides a
detailed overview of the developed user interfaces. Chapter 7 introduces and discusses the experiments
conducted. Finally, Chapter 8 concludes the dissertation by summarizing all the work completed, listing
the project outcomes, drawing conclusions, and discussing the research hypotheses. This chapter also
highlights directions for future research.


### Chapter 2

**Background**

### 2.1 Medical Anamnesis

Medical anamnesis, a cornerstone of the healthcare diagnostic process, involves a systematic and compre-
hensive collection of a patient’s medical history. This crucial step serves as the foundation for establishing
an accurate diagnosis and developing tailored treatment plans. During the anamnesis, healthcare pro-
fessionals inquire about the patient’s past and present medical conditions, medication history, familial
health background, lifestyle factors, and relevant symptoms. The intricate probing into these facets aims
to unearth valuable insights into the patient’s health trajectory, allowing practitioners to identify patterns,
risk factors, and potential underlying causes of current health concerns. By delving into the patient’s
medical narrative, medical anamnesis enables clinicians to holistically understand the individual, fostering
personalized and effective healthcare interventions.
The significance of medical anamnesis extends beyond its role as an information-gathering process;
it establishes a vital connection between the healthcare provider and the patient. Through thoughtful and
empathetic communication, healthcare professionals create an environment conducive to open dialogue,
encouraging patients to share pertinent details about their health experiences. This patient-centered ap-
proach not only contributes to a more accurate diagnosis but also promotes a collaborative and trust-based
relationship between the medical practitioner and the individual seeking care. In the evolving landscape
of healthcare, the art of medical anamnesis remains indispensable, representing a dynamic interplay of
clinical expertise, effective communication, and a commitment to understanding the unique context of
each patient’s health journey.


#### 2.1.1 Medical Algorithms.

It becomes evident that the integration of computational tools holds great promise for enhancing the
precisionandefficiencyofmedicalanamnesis. Medicalalgorithms, characterizedbytheirsystematic, data-
driven methodologies, can significantly contribute to the optimization of the anamnesis process. These
algorithms, when applied to the vast datasets generated by patient histories, can identify subtle patterns,
correlations, and risk factors that may escape conventional analysis. By leveraging machine learning and
artificial intelligence, these algorithms have the capacity to discern complex relationships within medical
data, aiding healthcare professionals in uncovering latent connections that might influence a patient’s
health status.

**Practical Example: Diagnosing Back Pain in Children**

To illustrate how medical algorithms can enhance anamnesis, consider the case of a pediatric patient
presenting with back pain. Back pain in children can have a variety of causes, ranging from muscle
strain to more serious conditions like scoliosis or infections. Using a medical algorithm designed for this
specific scenario, healthcare professionals can systematically evaluate the patient’s condition based on
predefined criteria. For example, as proposed in the algorithm by [Achar and Yamanaka, 2020 ], the
healthcare provider would first ask a series of targeted questions based on the patient’s age, activity
level, and symptom duration. The algorithm might then prompt the provider to consider additional red-flag
symptoms, such as fever or neurological deficits, which could indicate a more serious underlying condition
requiring urgent intervention.
Once the critical data is collected, the algorithm guides the clinician through a step-by-step diagnostic
process. This may include recommending imaging if certain high-risk factors are present, or suggesting
conservative treatment (e.g., rest and physical therapy) for more benign causes of back pain. By stream-
lining the decision-making process, the algorithm ensures that no important step is missed, reduces the
risk of diagnostic errors, and facilitates a more efficient and accurate treatment plan.

**Streamlining Anamnesis with Medical Algorithms**

Furthermore, medical algorithms offer the potential to streamline the anamnesis workflow, allowing for
more thorough and rapid information extraction. Through the intelligent processing of historical and
present medical information, these algorithms can assist clinicians in identifying critical areas of concern,
prompting targeted inquiries and investigations. This not only facilitates a more comprehensive under-


standing of a patient’s health background but also empowers healthcare providers to make well-informed
decisions in a timely manner. The synergy between medical algorithms and the traditional art of medical
anamnesis exemplifies a harmonious convergence of technological advancements and clinical expertise,
presenting a pathway towards more accurate, efficient, and patient-centric healthcare practices.
The main aim of medical algorithms is to enhance and standardize decision-making in medical care.
They provide a structured approach to selecting and applying treatment regimens, and automation within
these algorithms is meant to minimize the chance of errors [Johnson, 2002 ].
In the exploration of medical algorithms, well-organized information in the form of tables, flowcharts,
and calculators was encountered. These tools are designed to help understand the symptoms, causes, di-
agnosismethods, andtreatmentplansforspecificmedicalconditions. Forexample, [AcharandYamanaka,
2020 ] included tables that explained when urgent evaluation of back pain in children and adolescents is
necessary, the causes of back pain, and a systematic process for evaluating and treating it. Another study
[Keating et al., 2022 ] provided a comprehensive overview of alcoholic hepatitis, including its symptoms,
diagnostic criteria, and tailored treatment guidelines.
Research extended to exploring medical algorithms on platforms like ViDis [Jukan et al., 2020 ], MEDAL
[Med], and AFP [Ame]. Over20 papers fromtheAFP collection wereexamined, and an important discovery
was made — medical algorithms are closely tied to specific diseases. They are meticulously designed to
address the unique characteristics of individual medical conditions. This revelation led to a crossroads,
where innovative ways needed to be devised to effectively incorporate this specialized medical knowledge
into the project, especially since an universal framework or guideline suitable for developing the chatbot
does not exist.
A crucial juncture has been reached, where the challenge is to integrate this valuable medical infor-
mation into the Large Language Model (LLM). One promising solution is to create a system that can draw
on external information sources to carry out tasks. This approach is known as Retrieval Augmented Gen-
eration (RAG), where an information retrieval component works in harmony with a text generator model
[Lewis et al., 2021 ].

### 2.2 Large Language Models.

Large Language Models (LLMs) have made significant strides in natural language processing over the
past few years. These models can handle intricate interactions and parse nuanced information from vast
amounts of text. GPT-4 stands as a testament to these advancements, demonstrating exceptional skill in


understanding and generating human-like text [OpenAI, 2023 ]. Beyond GPT-4, the LLM arena has seen
the emergence of models like LLaMA, BLOOM, and the sector-specific BloombergGPT, each serving a
variety of applications [Touvron et al., 2023 ,Workshop et al., 2023 ,Wu et al.,2023a]. Notably, ChatGPT
is tailored for conversational scenarios, highlighting the breadth of LLM use-cases.
Tailoring LLMs for particular tasks or domains is a focal point of contemporary research. Methods,
including training models with human feedback, have been pivotal in making these models more attuned
to human preferences and versatile across a multitude of tasks [Ouyang et al., 2022 ].
Approaches like ”Chain of Thought Prompting” have been introduced to coax structured reasoning
from these models, improving their logical sequence construction [Wei et al., 2023 ]. The idea of zero-
shot learning demonstrates the flexibility of LLMs. Studies have shown that fine-tuned models can tackle
tasks they haven’t been explicitly trained for [Wei et al., 2022 ]. Additionally, techniques such as ”Multitask
Prompted Training” further amplify this adaptability, allowing LLMs to handle various tasks without direct
training [Sanh et al., 2022 ].
Driven by the imperative to enhance Large Language Model (LLM) performance for specific tasks, the
focus shifts to an exploration of pertinent research avenues. This investigation directs attention to the
efficacy of fine-tuning, soft-prompting, and hard-prompting techniques, aiming to discern their potential in
refining LLMs for optimal task-specific performance within natural language processing.

#### 2.2.1 Fine-tuning.

Fine-tuning Large Language Models (LLMs) is a complex and resource-intensive process. It involves adjust-
ing the weights of a pre-trained model using a specific dataset to better align it with a particular domain or
task. This typically requires substantial computational resources, such as high-end GPUs or TPUs, which
can be expensive and difficult to access for many organizations.
In addition to the hardware requirements, fine-tuning also demands a significant investment in data
collection and preparation. A high-quality dataset is essential for successful fine-tuning, as it needs to be
large, diverse, and accurately labeled to ensure the model performs well on new data. In the context of
medicalanamnesis, thischallengeisevengreater. Itrequirescollectingandannotatingdatathataccurately
reflects a wide range of medical conditions and patient interactions, which is time-consuming and requires
input from medical professionals.
Given these requirements, traditional fine-tuning of LLMs can be challenging for this project. The
process of collecting and preparing a comprehensive medical dataset would involve considerable effort
in gathering patient dialogues, ensuring data privacy, and cleaning the data to remove inconsistencies.


Moreover, the hardware needed to fine-tune a model of the necessary size and complexity would be difficult
to obtain without significant resources.
To address these challenges, techniques such as Low-Rank Adaptation (LoRA) have been developed to
reduce the computational burden of fine-tuning. LoRA introduces additional, low-rank trainable parameters
to the model while keeping most of the original parameters unchanged. This approach significantly reduces
the hardware requirements, making it a more feasible option for many applications. However, even with
LoRA, the need for a well-prepared dataset and domain expertise remains a challenge for this project. The
details of how LoRA works is presented below.

**Low Rank Matrix Adaptation (LoRA)**

One commonly used technique to finetune LLMs is LoRA [Hu et al., 2021 ], which takes advantage of the
intrinsic low dimensionality of the weight matrices [Aghajanyan et al., 2020 ]. By taking advantage of this
LoRA is able to decompose one big matrix into two much smaller counter parts, as illustrated inFigure 1.

Figure 1: LoRA reparametrization technique,Ais shapedd×r, whileBis shapedr×d, such that
r≪d. [Hu et al., 2021 ]

The original model’s weights continue to be utilized in a frozen state, overlaid with LoRA (Low-Rank
Adaptation) layers. This approach significantly reduces the number of trainable parameters by orders
of magnitude. Consequently, it leads to smaller training sizes and allows for increased batch sizes. This
efficiencystemsfromthefactthatmoredatacanbeallocatedin VRAM(VideoRandomAccessMemory), as
itisnolongerburdenedwiththebackpropagationcomponentsforeachoftheoriginaltrainableparameters,
but only with those related to LoRA.
There are more advanced techniques related to LoRA, which involve sophisticated mechanisms for
efficient matrix decomposition [Zhang et al., 2023 ,Kopiczko et al., 2023 ]. Further investigation into these
techniques would provide an opportunity to explore more complex approaches in this evolving area of
research, offering deeper insights into advanced methodologies.


#### 2.2.2 Soft Prompting.

Fine-tuning techniques, including methodologies like Low-Rank Matrix Adaptation (LoRA), have been ex-
plored extensively to tackle the limitations of traditional model tuning. These techniques allow for adjusting
a smaller subset of parameters, achieving performance comparable to full model fine-tuning but with re-
duced hardware requirements. This makes fine-tuning feasible for multiple specific tasks without the
need for maintaining an unique model for each one. Previously discussed in the context of parameter
efficiency, LoRA’s capabilities and other related techniques streamline the fine-tuning process, enabling
efficient task-specific adaptations.
Despite its advantages, LoRA and similar approaches are not without their own challenges, particularly
in managing task-switching during inference. The latency introduced by dynamically incorporating LoRA
layers can be significant, especially in scenarios with limited hardware resources or numerous diverse
tasks. This issue predominantly affects inference rather than the fine-tuning process itself, as switching
between LoRA configurations can delay the response time, contradicting the intended efficiency of low-rank
adaptations.
To further enhance task-switching flexibility and reduce hardware dependencies, the concept of soft
prompting has been developed. Unlike traditional fine-tuning, where the model’s parameters are altered,
soft prompting modifies the model’s behavior through carefully crafted prompts in the latent space. These
prompts act as task-specific guides, conditioning the model to produce desired responses based on the
prompt alone, without altering the underlying model weights. This is particularly useful for leveraging a
single model across multiple tasks without extensive retraining.
A detailed comparison between traditional fine-tuning and soft prompting is illustrated inFigure 2.
While traditional fine-tuning necessitates separate models or configurations for each task, soft prompting
utilizes a shared model framework, reducing the need for additional storage and computational overhead.
It’s important to clarify that soft prompting operates entirely within the embedding space, distinguishing it
from hard prompting, presented in the following section, which uses explicit textual inputs. This technique,
therefore, bypasses the need for natural language prompts and instead utilizes vectors that encode task-
specific information directly.


```
Figure 2: Comparison of Model Fine-tuning versus Prompt Tuning (Soft Prompting). [Lester et al., 2021 ]
```
#### 2.2.3 Hard Prompting

Prompts are pivotal in steering the responses and behavior of Large Language Models (LLMs). They
function as inputs or queries that users can provide to elicit particular responses from a model. Two
types of prompting are identified: hard prompting, which involves using text directly as queries, and soft
prompting, which operates in the embedding space, as utilized by [Lester et al., 2021 ]. Currently, the
focus is solely on hard prompts, as the available computational resources are insufficient to explore the
possibilities of soft prompting. Hard prompting techniques have shown the potential of improving models
at a specific task without further model fine-tuning [Brown et al., 2020 ].
Generally, hard prompting techniques employ text to attempt to mimic the human thought process
for dialogue. By loosely approximating the cognitive processes, the LLM can enhance its conditioning,
resulting in improved outcomes. One of these techniques is [Wei et al., 2023 ] which prompts the LLM to
output, along with the correct answer, the general thought process behind it,Figure 3sheds a light on this
behaviour.


Figure 3: Chain-of-thought prompting enables LLMs to tackle complex arithmetic, commonsense, and
symbolic reasoning tasks. [Wei et al., 2023 ]

There are alternative techniques that adopt a more divide-and-conquer approach. These methods
break down the original input into atomic problems and independently derive responses for each of those
atomic components. The final response is then crafted by merging the solutions to these atomic problems
into a comprehensive and content-rich prompt [Singhal et al., 2023 ,Saha et al., 2023 ], as illustrated by
Figure 4.

Figure 4: Ensemble Refinement (ER) involves conditioning a LLM on multiple generated reasoning paths
for improved answer refinement. [Singhal et al., 2023 ]

Additionally, these techniques can be used to create intelligent agents, each with a distinct goal and
mode of interaction with its environment [Park et al., 2023 ,Hong et al., 2023 ]. Figure 5illustrates an
example of an intelligent agent designed to embody a specific identity, in this case, an Engineer Agent
named Alex. The agent is defined by a unique profile, goal, and set of constraints that guide its actions
and interactions within the environment. It operates by subscribing to relevant messages, processing
information, and publishing responses based on its role. This highlights how intelligent agents can be


tailored to achieve specific objectives while communicating and coordinating effectively within a multi-
agent system through established subscription and publication methods.

Figure 5: Intelligent agents operate and communicate system-wide using established subscription and
publication methods to interact with the environment. [Hong et al., 2023 ]

#### 2.2.4 Retrieval Augmented Generation

LLMs often have a wrong perception of real world knowledge, or aren’t simply aware of it. Retrieval Ague-
mented Generation (RAG) [Lewis et al., 2021 ] tries to mitigate this via injecting external factual knowledge.
This external knowledge is gathered from vector databases, such as [Vec,Qdr,Johnson et al., 2017 ],
through text embedding similarity search. Matched documents are then injected to the LLM via prompting.
As illustrated inFigure 6, such mechanisms can also be extended with a more structured pipeline. The
process begins by augmenting the original query with additional relevant medical details. Next, the en-
hanced query is used to retrieve precise scientific evidence from textbooks using a combination of retrieval
methods. Finally, this retrieved evidence is integrated into the LLM’s response generation, ensuring that
the model produces accurate and well-informed answers. This approach not only supplements LLMs with
factual scientific knowledge but also enhances their reliability in specialized domains like medicine.


Figure 6: Pipeline from extracting and injecting factual medical knowledge from textbooks into LLMs.
[Wang et al.,2023b]

#### 2.2.5 Remarks

Despite the pivotal importance of fine-tuning, soft-prompting, and hard-prompting techniques, achieving an
intuitive understanding of the functioning of a comprehensive system guiding users through the anamnesis
process remains a challenging endeavor. In response to this challenge, the exploration extends to a more
in-depth analysis of Dialogue State Tracking (DST) and Task-Oriented Dialogue (TOD). Delving into these
topics, their nuances and potential contributions in elucidating the intricacies of a system designed to
facilitate and navigate the anamnesis process seamlessly are explored. By scrutinizing DST and TOD, light
is aimed to be shed on how these components synergize to enhance user guidance within the context of
a sophisticated anamnesis system.

### 2.3 Task Oriented Dialogue

Task-Oriented Dialogue (TOD) Systems represent a specialized field within the broader context of conver-
sational AI, focusing on assisting users in achieving specific goals through dialogue. Unlike open-ended
conversational systems, which might engage in a wide range of topics, TOD systems are designed with a
sharp focus on understanding user needs, tracking conversational states, and generating appropriate next


actions. A key objective in these systems is to minimize the number of dialogue turns, adhering to the
principle that fewer turns lead to a more efficient and user-friendly experience.

#### 2.3.1 Key Terms in TOD Systems

- **Domain Ontology** : This refers to the structured set of knowledge that defines the intentions a
    system can interpret from user sentences. It’s like a map of possible user intents specific to a given
    domain.
- **Domain** : In TOD context, a domain encompasses a collection of ’slots’. For example, in a travel
    booking system, domains might include flights, hotels, or car rentals.
- **Slot** : Each slot within a domain can take a range of values. For example, in a flight booking domain,
    slots might include ’departure city’, ’arrival city’, ’date’, and ’class of service’.

#### 2.3.2 Distinctive Features of TOD

- **Domain Specificity** : TOD systems are highly specialized, tailored to specific areas like travel
    booking, restaurant reservations, or customer service. This specialization often leads to challenges
    such as a scarcity of training data for more niche domains.
- **End Goal Orientation** : The primary aim of a TOD system is to assist the user in accomplishing
    a task. This requires the model to not only understand what the user wants but also to possess a
    nuanced understanding of how dialogues progress towards that end goal.
- **Brevity and Efficiency Focus** : Efficiency is key in TOD systems. The system must deliver
    accurate results in the least number of steps possible, prioritizing brevity and directness.

#### 2.3.3 Dialogue State Tracking (DST).

DST is a critical subtask in dialogue management. It involves representing the system’s belief about the
user’s goals at any given point in the dialogue, considering the entire history of the conversation. This
representation is crucial for the system to make informed decisions about the next steps.


#### 2.3.4 Challenges in TOD

- **Defining the State Space** : Determining the range of states that a dialogue can encompass
    is complex and requires a deep understanding of both the domain and the nuances of human
    conversation.
- **Maintaining Dialogue State** : Keeping track of the dialogue state in a tractable manner is chal-
    lenging, especially in long or complex dialogues.
- **Action Determination** : Deciding on the most appropriate action for each state to steer the con-
    versation towards the user’s goal.
- **Handling Multi-domain, Multi-turn Conversations** : TOD systems often need to manage con-
    versations that span multiple domains (e.g., booking a flight and a hotel) and involve several turns,
    adding layers of complexity.

To visualize these concepts, considerFigure 7of a finite state dialogue manager, which provides a
structured representation of how TOD systems manage and progress through conversations.

```
Figure 7: Illustration of a Finite State Manager in Task-Oriented Dialogue Systems.
```
#### 2.3.5 Machine Learning in Task-Oriented Dialogue.

Modelssuchastheoneproposedby[Wuetal., 2019 ]aredesignedtospecificallyaddressthedialoguestate
tracking challenge in TOD systems. They achieve this by developing a model dedicated to progressively
extract the dialogue state. The operational mechanism of this model can be visualized inFigure 8.


```
Figure 8: Illustration of Output Generated by a Dialogue State Tracking-Trained Model.
```
Several researchers have explored the use of language models for improving domain and slot con-
textualization, an approach that is beneficial for enhancing explainability. By integrating domain-specific
contexts into language models, these researchers have succeeded in developing systems that are capable
of not only engaging in conversation but also effectively describing the evolving context through dialogue
state tracking [Lee et al., 2021 ].
However, a significant challenge persists in these scenarios: directing conversations toward specific,
predefined objectives. The critical issue involves managing the information provided by users and guiding
the conversation toward the intended goal, all while maintaining an empathetic tone. This balance of
direction and empathy in conversational AI remains a largely unexplored frontier.
The emergence of LLMs with human-like feedback, such as ChatGPT-4, has brought new perspectives
to this challenge. These models are designed for open-ended, adaptable conversations, making them
incredibly versatile. However, this flexibility often comes at a cost in task-oriented dialogues. These mod-
els tend to drift into unrelated topics, even when using tightly controlled system prompts, limiting their
effectiveness in focused, goal-oriented interactions.
Despite these limitations, the advantages of using LLMs in task-oriented dialogues are significant.
Their ability to understand and generate natural language is unparalleled. To harness these strengths
effectively in task-oriented settings, a tailored approach is needed. It involves refining these models to
maintain their open-ended, empathetic conversation capabilities while also integrating a stronger focus
on task completion and goal direction. This dual focus is key to advancing the field of conversational AI,
merging the strengths of LLMs with the specificity required for goal-oriented dialogues.


#### 2.3.6 Taking advantage of LLMs

Large language models (LLMs) have revolutionized task-oriented dialogue, offering unparalleled utility in
this domain. Their advanced natural language processing capabilities allow for the understanding and
generation of contextually relevant and coherent responses, which is essential in maintaining a fluid and
logical conversation flow. In task-oriented dialogues, where the objective is to achieve specific outcomes or
provide precise information, LLMs can analyze and respond to user queries with remarkable accuracy and
detail. Furthermore, they can learn from interactions to refine their understanding of user needs and pref-
erences, thereby personalizing and improving the conversational experience over time. This adaptability
makes them invaluable in various applications, from customer service bots to virtual personal assistants,
where they can handle complex tasks, resolve queries efficiently, and provide information or assistance
in an user-friendly manner. The integration of LLMs into dialogue systems represents a significant stride
towards more intelligent, responsive, and efficient communication technologies. To achieve these objec-
tives, researchers have explored the use of LLMs for functions like dialogue state tracking and managing
task-oriented dialogue. [Wu et al.,2023b]
Integrating a lookahead logic, akin to the anticipation of future user questions as explored in [Hu et al.,
2023 ], presents an interesting development in Task-Oriented Dialogue. This approach is instrumental in
informing the responses of LLMs, aiming to enhance the accuracy and relevance of each answer. By pre-
dicting potential future inquiries, this technique efficiently streamlines the dialogue, reducing the number of
conversational exchanges required for a comprehensive and user-friendly interaction. Such exploration in
the use of LLMs opens up intriguing possibilities for more nuanced and effective communication strategies.
In the evolving field of task-oriented dialogue, researchers are continuously developing new formatting
techniques to enhance dialogue state tracking and the effectiveness of AI-driven conversations. A recent
study [Das et al., 2023 ] proposes the use of an XML-based format for dialogue state tracking, introducing
a structured, hierarchical framework. This framework organizes conversations into distinct “turns,” where
each turn is labeled with specific attributes such as user intent, domain, and context. By structuring
the dialogue in this way, the system can track multiple intents across long, open-domain conversations,
while maintaining consistency and coherence. Moreover, the study introduces a Pre-Analytical Recollection
(PAR) technique, which ensures that the model summarizes and grounds the content of each turn before
making predictions. This allows the system to handle complex, multi-turn dialogues without losing track of
previous interactions or introducing errors through hallucination, ultimately improving both the accuracy
of state predictions and the overall flow of task-oriented dialogue systems.
The true advancement in this domain is showcased by a dynamic technique known as automatic topic


management, as discussed in [Cao, 2023 ]. This research moves beyond the foundational structuring of
dialogues by introducing a sophisticated method that sequences and manages dialogue topics through
a multi-agent framework. Specifically, DiagGPT leverages Topic Stack Management, where topics are
dynamically tracked, prioritized, and revisited as needed. This approach not only guides the conversation
but also progressively enriches the AI’s context understanding by refining the conversation flow with each
topicaddressed. By automating the control overdialogue states, thesystemeffectivelyaligns withthegoals
of task-oriented dialogue—achieving specific objectives through precise, contextually relevant interactions.
The system’s Topic Manager selects actions from a predefined list, such as creating new topics, fin-
ishing existing ones, or jumping back to previous ones, depending on the conversation’s progression. The
Topic Enricher enhances the topics by adding relevant context, which the Chat Agent uses to generate
informed and efficient responses. This layered process ensures a deeper exploration of user input, im-
proving both interaction quality and the AI’s ability to guide users toward task completion. This innovative
approach represents a significant leap forward in handling task-oriented dialogues, offering a more nu-
anced and methodical way to achieve conversational goals by effectively managing the flow of information
throughout the interaction.
Figure 9visually illustrates this architecture by depicting the four key stages of DiagGPT: thinking topic
development, maintaining the topic stack, enriching the current topic, and generating responses. The
figure highlights how the Topic Manager oversees and manages the conversational flow, ensuring smooth
transitions between topics and tailoring the dialogue to the user’s needs. This integrated approach allows
DiagGPT to proactively engage with users, enriching the interaction and better aligning with the goals of
task-oriented dialogue.

Figure 9: DiagGPT follows a four-stage workflow: Develop Thinking Topics, Maintain Topic Stack, Enrich
Each Topic, and Generate the Response. [Cao, 2023 ]

```
Innovative methods that incorporate complex dialogue management systems, including features like
```

intentional chit-chat, have been proposed by some researchers. The diagram inFigure 10[Mo et al., 2023 ]
illustrates a system that combines traditional dialogue management with advanced strategies to enhance
user engagement.
The system consists of three main modules: Task Search, Task Preparation, and Task Execution. In
the Task Search module, users can input queries into a search engine, explore a task catalog, and receive
recommended tasks based on their input. If needed, a task clarification stage helps refine ambiguous
queries. The Task Preparation module ensures that users are adequately prepared before proceeding,
with a confirmation step to verify readiness.
During Task Execution, the system provides detailed guidance through individual steps, while offering
chit-chat interactions for additional support and clarification. It also integrates a knowledge module to
provide tailored assistance. This design, with green elements representing user intents and orange for
system responses, showcases a flexible and interactive approach to dialogue management. It allows for
smooth transitions between structured queries and casual conversations, adapting to diverse user needs
and enhancing the overall interaction experience.

```
Figure 10: Dialogue Management System Diagram. [Mo et al., 2023 ]
```
Expanding on the aforementioned approach, several researchers have delved into the use of an explicit
graph structure for tracking dialogue states. This method effectively steers conversations towards their
desired goals. Following this line of inquiry, recent research has adopted this technique, keeping track of
essential information relevant to the dialogue. This collected data is then utilized to refine the responses in
future interactions. The process begins with expanding the knowledge graph using facts logically inferred
through probabilistic logical programming. As the conversation progresses, a neural model assesses the
relevance of each node and edge in this enhanced graph, ensuring that each turn in the dialogue is both


pertinent and informed [Walker et al., 2023 ].Figure 11visually demonstrates this mechanism, where it
can be clearly observed that the system begins with a dialogue state as a knowledge graph, enhanced
with derived facts using probabilistic logical programming, then a neural model is applied to score their
relevance for effective response generation.

Figure 11: Knowledge graph dialogue state enhanced with probabilistic logical programming, followed by
neural model scoring for effective response generation. [Walker et al., 2023 ]


### Chapter 3

**AI in Anamnesis**

The transformative integration of informatics within anamnesis is revolutionizing healthcare, breathing
new life into the way patient histories are collected and reshaping healthcare delivery. Electronic Medi-
cal Records (EMRs) stand at the forefront of this innovative shift, paving the way for more personalized,
accessible, and precise care through meticulous documentation and streamlined data retrieval [Lino and
Martins, 2021 ].
The synergy of Mobile Agent Applications and electronic anamnesis systems heralds a new era in data
managementandcollection, offeringuser-friendlyandefficientaccesstopatientinformation, acornerstone
for reliable medical histories and enlightened clinical decision-making [Liu et al., 2012 ]. Internet-Based
Anamnesis brings a collaborative dimension to healthcare, empowering patients to actively input their
medical information and become engaged participants in their healthcare journey [Emmanouil and Klein,
2001 ].
Innovative solutions like Medical Question-Answering Systems are extending the boundaries of patient-
centric care, providing a platform for real-time and accurate responses to medical inquiries and fostering
informed health-related decisions [Jacquemart and Zweigenbaum, 2003 ]. Additionally, the advent of data-
to-text summarization technologies emphasizes their paramount role in offering swift access to patient
histories, optimizing clinical workflows, and shaping future healthcare [Scott et al., 2013 ].
Conversational user interface applications such as “Talking to Ana” and tablet-based digital question-
naires are enhancing the self-anamnesis process, offering user-friendly platforms and reflecting high levels
of patient satisfaction, reinforcing the potential of digital tools in medical history collection [Denecke et al.,
2018 ,Melms et al., 2021 ]. Empathic anamnesis questionnaires in online clinics are offering profound
insights into the interplay between doctors’ empathy perceptions and patients’ subjective health status,
underscoring the critical role of emotional intelligence in healthcare delivery [Martikainen et al., 2022 ].
Self-assessment anamnesis questionnaires are shining a light on the incidental detection of diseases
like Von Willebrand Disease, playing a crucial role in protecting healthcare providers and minimizing com-


plications [Jorge et al., 2021 ]. These innovations are collectively illuminating the transformative and en-
lightening impact of informatics in refining anamnesis processes and elevating patient care outcomes,
making the field more vibrant and intriguing for both academia and the general populace.

### 3.1 Task-Oriented Dialogue and Anamnesis

The use of task-oriented dialogue systems in healthcare has expanded significantly in recent years, with
numerous research efforts focused on enhancing patient interactions, facilitating diagnosis, and improving
medical information extraction. These systems, which are designed to handle structured, goal-oriented
conversations, have demonstrated effectiveness in various healthcare domains, such as mental health,
physical health, and patient assistance. Each of these domains presents unique challenges that task-
oriented dialogue systems address through specific conversational flows aimed at achieving well-defined
objectives.
For instance, [Valizadeh and Parde, 2022 ] demonstrate the application of task-oriented dialogue sys-
tems in key areas such as mental health management, chronic disease monitoring, and patient support
services. These systems are often used to automate routine tasks, such as gathering patient information,
diagnosing conditions, and offering medical recommendations.Figure 12illustrates the various research
domains and associated subcategories for the application of task-oriented dialogue in healthcare, show-
casing its broad utility across sectors.

Figure 12: Domains of Research and Associated Subcategories for the Application of Task-Oriented Dia-
logue in Healthcare. [Valizadeh and Parde, 2022 ]


#### 3.1.1 Mental Health Applications

Task-oriented dialogue systems have seen significant use in mental health, where sensitive and structured
conversations are essential for accurate diagnosis and patient well-being. Systems tailored to mental
health aim to assess conditions such as depression, anxiety disorders, and Post-Traumatic Stress Disor-
der (PTSD). A notable example is the work of [Papangelis et al., 2013 ], who developed a dialogue system
specifically for assessing PTSD. This system employs a hierarchical Markov Decision Process (MDP) com-
bined with reinforcement learning to guide patients through structured conversations, gradually collecting
diagnostic information without overwhelming them.
The key feature of this system is its ability to adapt based on the patient’s responses and emotional
state, ensuring a personalized and empathetic interaction. The hierarchical structure allows the dialogue
to unfold gradually, with the system asking increasingly specific questions as it gathers more information.
This approach is critical in mental health, where maintaining patient trust and engagement is essential to
obtaining accurate and complete information. By using reinforcement learning, the system dynamically
adjusts its questioning strategy, ensuring a balance between information gathering and patient comfort.

#### 3.1.2 Physical Health and Chronic Condition Management

In the context of physical health, task-oriented dialogue systems are often used to manage chronic condi-
tions such as asthma, diabetes, cancer, and HIV/AIDS. These systems play a crucial role in automating
follow-up consultations, gathering patient-reported outcomes, and monitoring medication adherence. [Ali
et al., 2020 ] applied deep reinforcement learning (DRL) to optimize task-oriented dialogue systems for
managing such chronic conditions.
Their research highlights how DRL can dynamically optimize the dialogue flow in multi-turn conver-
sations, where the system must collect detailed information about the patient’s condition across multiple
dimensions. For example, a system managing a patient with diabetes would need to ask about blood glu-
cose levels, diet, and medication adherence across several interactions. By using DRL, the system learns
to prioritize the most critical questions while avoiding redundancy, ensuring that the conversation remains
efficient and relevant.

#### 3.1.3 Knowledge-Graph-Driven Systems for Multi-Domain Dialogues

Another major advancement in task-oriented dialogue systems is the integration of knowledge graphs
to handle complex, multi-domain conversations. [Sun et al., 2020 ] developed a system that leverages


a knowledge-graph-driven architecture, allowing it to manage conversations that span across different
medical domains. Knowledge graphs enable the system to model complex relationships between medical
concepts, such as symptoms, diseases, and treatments, and to adapt the dialogue flow accordingly.
This flexibility is particularly valuable in scenarios where the patient’s symptoms may relate to multiple
medical conditions. For instance, a conversation that begins with questions about respiratory symptoms
might seamlessly transition to questions about medication history or cardiac health, depending on how
the dialogue evolves. The knowledge graph provides the system with the necessary structure to make
these transitions smoothly, ensuring that all relevant medical areas are covered without overwhelming the
patient with unrelated questions. This approach allows for more open-ended, flexible dialogues compared
to traditional slot-filling models, which are more rigid and task-specific.

### 3.2 Limitations of Current Task-Oriented Dialogue Systems.

Despite the successes of task-oriented dialogue systems in healthcare, several limitations remain, partic-
ularly in terms of their domain specificity, flexibility, and scalability.

- **Narrow Domain Focus** : Many existing systems are built to handle specific tasks within narrowly
    defined medical domains, such as diagnosing a particular condition or managing medication adher-
    ence. While these systems perform well within their specific domains, they struggle to generalize
    across broader healthcare scenarios where multiple medical conditions or patient concerns may
    intersect. For instance, a system designed for asthma management might be ineffective in handling
    an emergency room consultation where the patient’s medical history is incomplete or unknown.
- **Slot-Filling Models and Their Rigidity** : Traditional dialogue systems often rely on slot-filling
    approaches, where predefined questions are asked to fill specific information slots, such as age,
    symptoms, or medications. While effective in structured, routine scenarios, this approach lacks
    the flexibility needed for more open-ended conversations, where the patient’s responses may not
    fit neatly into predefined categories. Slot-filling models struggle with handling unstructured patient
    inputs or branching conversations that span multiple medical domains, limiting their adaptability in
    complex dialogues.
- **Computational Complexity and Scalability** : Systems that rely on deep reinforcement learning
    or other machine learning approaches face significant challenges in terms of computational cost
    and scalability. For instance, [Ali et al., 2023 ] demonstrated that while reinforcement learning


```
improves dialogue flexibility, it also introduces challenges in terms of real-time performance and
generalization across multiple medical domains. These systems often require extensive retraining
and fine-tuning to adapt to new healthcare environments, making them less practical for widespread
deployment.
```
### 3.3 Advancements and Future Directions

Recent advancements in task-oriented dialogue systems have sought to address some of these limitations
by integrating more adaptive architectures such as knowledge graphs and dynamic dialogue management
techniques. These approaches allow systems to manage multi-domain dialogues more effectively, handling
unexpected patient inputs and transitioning smoothly between different medical topics.
However, significant challenges remain in creating systems that can handle open-ended, real-time
dialogues across a wide range of medical conditions. Future research should focus on developing more
scalable models that can dynamically adjust to the evolving needs of patients, particularly in complex
scenarios such as emergency room consultations or initial medical assessments where the system must
gather a comprehensive medical history in a limited time frame.
In conclusion, while task-oriented dialogue systems have made significant strides in specific healthcare
domains, there is still considerable work to be done in developing generalizable, adaptive systems that
can handle complex, multi-topic medical interviews. By overcoming these challenges, future systems will
be better equipped to provide comprehensive patient assessments, supporting healthcare professionals
in making more informed diagnostic and treatment decisions.


# Part II

# Core of the Dissertation


### Chapter 4

**System Design**

Building on the foundation set by previous researchers, the aim is to develop a platform that effectively com-
municates with patients and maximizes information extraction, while maintaining an empathetic approach.
The initial experiments explored two main techniques: training models using LoRA (Low-Rank Adaptation)
and soft prompting. However, these efforts encountered significant hardware limitations. Fine-tuning even
the most basic LLMs, such as LLaMA 7B, would require at least two off-the-shelf GPUs, each with around
48GB of VRAM. Moreover, to ensure scalability and reliability in a production environment, several more
GPUs and substantial infrastructure would be necessary to handle multiple users simultaneously.
In addition to hardware, fine-tuning requires a high-quality, domain-specific dataset—something that is
scarce in the field of medical anamnesis. Constructing such a dataset would be a time-intensive process,
involving careful curation, data collection, and annotation, which would delay development. Even with this
effort, smaller models like LLaMA 7B would still struggle with generalization and command adherence,
as noted in [Wei et al., 2023 ], diminishing the system’s overall performance and accuracy in real-world
applications.
To avoid these limitations, LLM APIs, such as ChatGPT, provide a significant advantage. These APIs
grant access to some of the most powerful and up-to-date models available, such as GPT-4, without requir-
ing the substantial investment in GPU clusters and the infrastructure needed to manage them. Moreover,
by utilizing high-performance LLMs through these APIs, the system can maintain accuracy and reliability
from the outset, allowing development efforts to focus on refining user interactions rather than addressing
the hardware and data constraints typically associated with local model fine-tuning.
Armed with this knowledge, three foundational pillars were established for the platform: high scalabil-
ity, high fidelity, and extensive customization. Given the hardware constraints, these features are largely
attainable through closed-source, cloud-hosted solutions, leading to the selection of ChatGPT, as outlined
in the technical report by OpenAI [OpenAI, 2023 ]. This choice is underpinned by ChatGPT’s proven ex-
cellence in Large Language Model (LLM) performance, surpassing both open and closed-source rivals,


making it an ideal fit for the platform’s objectives. Moreover, developing a custom model would require
a specially curated dataset tailored to specific end-goals. While such datasets exist, they often carry in-
herent biases related to their creation [Ben Abacha et al., 2023 ,Wang et al.,2023a]. Considering the
need for rapid integration of new features and behaviors, it was concluded that fine-tuning a model could
compromise the ability to efficiently expand the model’s capabilities.
Therefore, to expedite the prototyping process, the development of a test environment that enables
rapid collection of feedback on the model’s behavioral modifications and swift enhancements was pri-
oritized. It was found highly beneficial to construct a web application to facilitate user interaction with
the model. This strategy allowed for the deployment and rapid testing of multiple model versions with
research group members. In the subsequent subsections, the progressive development will be detailed,
representing the preliminary approach and its evolution based on feedback from research group members.

### 4.1 Introduction to the Task-Oriented Dialogue Framework

The development of a task-oriented dialogue framework is central to enabling structured and efficient pa-
tient anamnesis within the system. Unlike open-ended dialogue systems, which can wander across various
topics, task-oriented dialogue focuses on achieving specific goals—here, the goal is to gather comprehen-
sive and medically relevant patient information in a structured, conversational format. This framework
ensures that patient interviews remain focused, effective, and aligned with clinical objectives.

#### 4.1.1 Overview of Task-Oriented Dialogue in Anamnesis

In the context of medical anamnesis, task-oriented dialogue involves guiding patients through a predefined
set of medical questions designed to extract critical health information. The framework relies on a Directed
Acyclic Graph (DAG) to represent the flow of the conversation, with each node corresponding to a specific
medical inquiry. The system dynamically adjusts the conversation flow based on patient responses, en-
suring that no unnecessary or redundant questions are asked while still covering all essential medical
domains.
The implementation of this dialogue framework is geared towards maintaining relevance throughout
the conversation. By using dialogue state tracking and self-consistency checks, the system monitors
whether the patient’s responses are directly addressing the posed questions. If responses are off-topic or
insufficient, the system steers the conversation back on track by asking clarifying questions. This results
in a dialogue that is both task-driven and adaptable to individual patient interactions, striking a balance


between efficiency and thoroughness.

#### 4.1.2 System Components and Modular Architecture

The task-oriented dialogue framework is built using a modular architecture that separates the conversation
management, decision-making, and report generation processes. This modularity ensures that each com-
ponent operates independently, allowing the system to scale effectively and to be extended with additional
features as needed.
The core components of the framework include:

- **Dialogue Manager** : The central module responsible for handling the conversation flow, making
    decisions on when to ask follow-up questions, and determining when sufficient information has
    been gathered.
- **Decision Module** : Embedded within the dialogue manager, this module assesses patient re-
    sponses, deciding whether to continue probing on a particular topic or move on to a new subject.
    It utilizes the DAG structure to traverse the conversation in a logical and context-aware manner.
- **Report Generator** : At the end of the conversation, this component compiles the collected data
    into a structured medical report, ensuring that key insights from the dialogue are preserved and
    presented in a format that healthcare professionals can use for diagnosis and treatment planning.

By structuring the system into these distinct modules, the framework allows for efficient dialogue
management and facilitates the integration of external knowledge sources, such as medical guidelines or
algorithms, to further refine the conversation flow.

#### 4.1.3 Integration of Large Language Models for Medical Dialogue

To achieve natural, human-like interactions during patient anamnesis, the task-oriented dialogue frame-
work integrates advanced Large Language Models (LLMs), such as GPT-4, which have been fine-tuned
for medical dialogue. These models provide the conversational capability necessary for eliciting detailed
patient responses while maintaining contextual understanding and relevance.
The integration of LLMs enhances the system’s ability to handle complex medical terminology, inter-
pret diverse patient narratives, and ask follow-up questions that feel natural to the patient. The LLM is
not only tasked with generating conversational text but also with interpreting patient inputs in real time,
dynamically adapting the next steps in the dialogue based on the information received. This creates a


conversational experience that feels intuitive, while still adhering to the structured format necessary for
effective anamnesis.
The use of cloud-based APIs, such as those provided by OpenAI’s GPT-4, allows the system to by-
pass the hardware limitations typically associated with locally hosted models. This enables the system to
scale efficiently and handle multiple user interactions simultaneously without sacrificing performance or
accuracy.
In this framework, the LLM operates within predefined constraints, governed by the DAG structure
and the decision-making logic embedded in the system. This hybrid approach leverages the adaptability
of LLMs while ensuring that the conversation remains on task, resulting in a robust, medically relevant
dialogue system.

### 4.2 Graph State Tracking for Task-Oriented Dialogue

The ability to dynamically track the state of a conversation is fundamental to the success of task-oriented
dialogue systems, particularly in complex domains such as medical anamnesis. In this system, the con-
versation is modeled using a Directed Acyclic Graph (DAG), where nodes represent specific questions or
decision points, and edges define the possible transitions between these nodes. Graph State Tracking
refers to the continuous monitoring and updating of this conversation graph, ensuring that the dialogue
progresses logically and that no critical topics are overlooked.
This section outlines the design and implementation of the graph state tracking mechanism in the
task-oriented dialogue framework. The structure and traversal of the DAG are explored, along with how
decisions are made at each node. Additionally, the mechanisms ensuring that the dialogue remains
coherent, relevant, and task-focused are discussed in detail.

#### 4.2.1 Graph Structure

Influence was drawn from the works of [Cao, 2023 ,Hu et al., 2023 ], and [Walker et al., 2023 ], and
as a result at the heart of the task-oriented dialogue system is a Directed Acyclic Graph (DAG), which
structures the conversation into a network of nodes (questions) and edges (paths). Each node in the DAG
corresponds to a specific medical question or prompt relevant to the patient’s condition, and the edges
define the potential pathways the conversation can take depending on the patient’s responses.
The DAG provides greater flexibility and scalability compared to other structures, such as finite-state
machines or hierarchical trees. While trees enforce strictly hierarchical paths, a DAG allows multiple paths


to converge on the same node. This feature enables the reuse of common questions across different
branches of the dialogue, making the system especially useful in medical scenarios where different symp-
toms may lead to similar follow-up questions. For example, a query about chest pain might arise from
different starting points, such as cardiac or respiratory symptoms.
The system models the progression of a task-oriented dialogue as a Directed Acyclic Graph (DAG)
G= (V,E), where:

- Vis a finite set of vertices (nodes), where each nodev∈Vrepresents a specific medical inquiry
    or decision point in the dialogue.
- E⊆V×Vis a set of directed edges between pairs of nodes. An edge(vi,vj)∈Eindicates
    that nodevj was generated as a direct result of the patient’s response to the inquiry at nodevi.

The DAGGis used to structure the task-oriented dialogue such that it adheres to a logical progression,
with no possibility of cycles, ensuring that the dialogue does not revisit previous states. This structure is
particularly suitable for complex dialogues, such as those required in medical anamnesis, where questions
need to adapt to the evolving information provided by the patient.

**Node Definition**

Each nodev∈V in the DAG corresponds to a distinct medical inquiry, categorized based on predefined
medical topics that form the core structure of the dialogue. These topics cover all key areas of a patient’s
medical history and belong to a fixed set of categories. The available topics incorporate most of the
relevant medical areas and include the following predefined categories, which align closely with those
used in [Ben Abacha et al., 2023 ].

- **HistoryofPresentIllness** : Aimed at gaining an understanding of the patient’s current symptoms
    and the timeline of their development.
- **Review of Systems** : Assesses potential issues across various bodily systems including cardio-
    vascular, respiratory, gastrointestinal, neurological, and musculoskeletal.
- **Past Medical History** : Inquires about any chronic illnesses or past diagnoses to better under-
    stand the patient’s overall health history.
- **Medications** : Seeks information on the patient’s current medications, including prescription
    drugs, over-the-counter medications, and supplements.


- **ChiefComplaint** : Focuses on identifying the primary health issue or symptom that led the patient
    to seek medical attention.
- **Past Surgical History** : Gathers details about any previous surgical procedures the patient may
    have undergone.
- **Allergy** : Enquires about any known allergies, particularly to medications, food, or environmental
    factors.
- **Gynecologic History** (excluded for male patients): Covers aspects of the patient’s gynecological
    history, including menstrual history, pregnancies, and related procedures or conditions.
- **Family History** : Investigates the presence of significant medical conditions or diseases in the
    patient’s family history.
- **Social History** : Explores lifestyle factors such as smoking, alcohol consumption, exercise, and
    diet.
Each node is associated with a specific medical domain, ensuring logical structuring of the dialogue
and systematic coverage of the patient’s anamnesis.

**Node Attribute - Priority** P(v) Each nodev∈Vis assigned a priority, which is dynamically gener-
ated by the Large Language Model (LLM) during the conversation. The priority values reflect the relative
importance of each question and are defined as:

- P(v) =Low
- P(v) =Intermediate
- P(v) =High
- P(v) =Urgent
    The LLM determines the priority based on the patient’s responses and the overall context of the
conversation, ensuring that more critical inquiries are addressed first. This dynamic prioritization allows
the system to adapt to the patient’s evolving medical narrative, guiding the conversation through the most
relevant topics in an optimal order. The priority dictates the order in which nodes are visited during
graph traversal, ensuring that urgent or contextually significant questions are handled before lower-priority
inquiries.


**NodeAttribute-State** S(v) Eachnodeischaracterizedbyastate, whichreflectswhetherthequestion
has been addressed and whether it has led to the generation of follow-up inquiries. The possible states
are:

- S(v) =Open: The node represents a question that has not yet been posed or answered.
- S(v) =Explore: The node has been answered and has generated follow-up questions, leading to
    the expansion of the graph.
- S(v) = Closed: The node has been answered, and no further follow-up questions have been
    generated, marking the end of that line of inquiry.

The dynamic nature of both the priority and the state allows the system to adapt to the patient’s
responses and focus on the most critical aspects of the anamnesis as the conversation evolves. The
LLM’s dynamic assignment of priority ensures that urgent medical concerns are tackled first, while the
system’s use of predefined node categories ensures that all relevant areas of the patient’s medical history
are systematically covered.

**Edge Definition**

Each directed edgee= (vi,vj)∈Erepresents a logical transition between two nodesviandvj. The
existence of an edge implies that the inquiry atvjwas dynamically generated in response to the patient’s
answer atvi. These edges are created based on the evolving context of the conversation, ensuring that
follow-up questions are logically connected to the patient’s previous responses. For example, if the patient
mentions shortness of breath, the system might dynamically transition to questions related to recent
physical activity or respiratory infections. The edges, while directed to avoid cycles and ensure forward
progression, are not pre-defined, allowing for flexibility as the conversation unfolds.
Edges can originate from multiple source nodes, enabling different symptoms or conditions to lead to
the same follow-up question. This flexibility ensures that the system does not impose a rigid, deterministic
flow where each response leads to a single outcome. Instead, the DAG supports multiple paths, adapting
dynamically based on the patient’s responses. The edges do not necessarily reflect whether a question
has already been asked or the completeness of responses, but rather how medical inquiries are logically
connected, enhancing the system’s adaptability and efficiency.


**Traversal Strategy**

Traversal through the DAG is governed by predefined strategies that dictate the sequence in which nodes
are visited. The system implements both Depth-First Search (DFS) and Breadth-First Search (BFS), but
it opts for DFS due to its ability to maintain a focused conversation by minimizing context switching. In
contrast, BFS, while available, can cause frequent transitions between unrelated medical topics, leading
to cognitive load on the patient and potentially disrupting the flow of dialogue.

- **Depth-FirstSearch(DFS)** : DFS is the preferred traversal method in this system because it allows
    the conversation to delve deeply into one specific topic before transitioning to another. This strategy
    is especially well-suited for medical dialogues, where maintaining the context of the conversation is
    critical. With DFS, the system follows a single line of questioning, moving through related questions
    sequentially. For instance, if the dialogue focuses on cardiac symptoms, the system will continue
    to explore all relevant follow-up questions within that domain before moving on to other systems
    like respiratory or gastrointestinal concerns. This minimizes cognitive strain on the patient, as they
    remain engaged in one topic area for a more extended period without being asked about unrelated
    issues in quick succession.
- **Breadth-First Search (BFS)** : BFS is also implemented as an alternative strategy and may be
    appropriate in certain scenarios where a broad, high-level assessment across multiple medical do-
    mains is required early in the dialogue. In BFS, the system asks overarching questions across
    different medical systems before diving deeper into any particular area. While this can provide a
    general overview of the patient’s condition, it comes with the drawback of increased context switch-
    ing, which can disrupt the flow of the conversation. Jumping from cardiovascular to respiratory,
    then gastrointestinal systems may lead to fragmented dialogue and cause the patient to lose focus
    or provide incomplete information. Therefore, although BFS is available, it is generally avoided in
    favor of DFS to maintain a coherent and contextually relevant dialogue flow.

#### 4.2.2 Cold Start

At the beginning of the interaction with the patient, there is no prior information available. Therefore, a set
of foundational nodes must be established to initiate the conversation. These nodes enable the system to
begin with general questions and gradually transition into more specific topics. As a result, the DAG Gis
initially populated with vertices that are not connected by any edges, more specifically, the following:


- **History of Present Illness** : ”Can you describe the symptoms you are currently experiencing
    and when they started?” (P(v) =High) and ”Have you had any recent illnesses or infections?”
    (P(v) =Intermediate)
- **Review of Systems** : ”Have you experienced any recent weight loss?” (P(v) =High)
- **Past Medical History** : ”Do you have any chronic illnesses or conditions that you have been
    diagnosed with in the past?” (P(v) =Intermediate)
- **Medications** : ”Are you currently taking any medications?” (P(v) =High)
- **Chief Complaint** : ”What is the primary health issue or symptom that prompted you to seek
    medical attention today?” (P(v) =Urgent)
- **Past Surgical History** : ”Have you had any recent surgeries or medical procedures?” (P(v) =
    Intermediate)
- **Allergy** : ”Do you have any known allergies to medications?” (P(v) =High)
- **Gynecologic History** : ”Are you currently pregnant or planning to become pregnant?” (P(v) =
    Intermediate)
- **Family History** : ”Is there a history of any significant medical conditions or diseases in your fam-
    ily?” (P(v) =Intermediate)
- **Social History** : ”Do you consume alcohol or use recreational drugs?” (P(v) =Low)

The method used to derive the specific initial nodes is outlined in the ”Algorithmic Clustering for Initial
Question Selection” section.
Additionally, the priority of each question was manually set to ensure that the most informative and
relevant questions are asked first in the interview process. This manual prioritization guarantees that the
questions addressing urgent concerns and providing critical diagnostic information are posed early on,
ensuring an efficient and focused interview.
Themanual assignmentof prioritiesensuresthattheinterviewbegins withthemostcriticalandbroadly
informative questions. For instance, questions related to chief complaints and current medications are
given urgent or high priority, as they provide essential diagnostic information early in the interview. Ques-
tions about lifestyle choices or social history are assigned a lower priority, ensuring they are asked only
after more urgent medical information has been gathered.


#### 4.2.3 Decision-Making at Nodes

Intask-orienteddialoguesystems, particularlyinmedicaldomains, oneofthekeychallengesisdetermining
when a line of questioning has been adequately explored or whether additional follow-up questions are
needed. This decision-making process takes place at each node within the Directed Acyclic Graph (DAG),
which structures the conversation. At each node, the system evaluates the patient’s response to decide
whether to prune the conversation—indicating that no further questions are necessary—or to expand the
conversation by generating and asking additional follow-up questions. This process is facilitated by a Large
Language Model (LLM) that dynamically generates decisions in real-time based on the current question,
the patient’s response, and the conversation history.
The system must balance thoroughness with efficiency, ensuring that all necessary information is
collected without overburdening the patient with redundant or irrelevant questions. The LLM evaluates
the completeness and relevance of responses and determines whether to move forward or seek further
details.

**Prune**

Pruningoccurswhenthesystemdeterminesthatthepatienthasprovidedasatisfactoryresponse, meaning
that no further questions are needed for that topic. The system closes the current node and transitions to
the next relevant node in the DAG. The decision to prune is based on several key factors. First, the LLM
assesses whether the response adequately answers the posed medical question. If the patient’s response
provides the necessary details, the system proceeds to prune the node. Additionally, the LLM evaluates
whether the patient’s response is relevant to the initial question, ensuring that any extraneous information
is filtered out. Finally, the system checks for redundancy, determining whether any further questions would
merely repeat information that has already been gathered.
Once the LLM determines that the node can be pruned, it signals the system to mark the node as
complete and transition to the next part of the conversation.

**Expand**

Conversely, expansion occurs when the patient’s response is incomplete, ambiguous, or introduces new
concerns that require further exploration. In this case, the LLM generates follow-up questions, tailored to
extract the additional information needed. The system’s decision to expand is driven by several consider-
ations. If the patient’s response lacks clarity or sufficient detail, the LLM identifies gaps in the information


and generates follow-up questions. For instance, if a patient mentions discomfort without specifying the
nature or duration of the symptom, the system will expand the inquiry to gather those specific details.
Moreover, new concerns may arise from the patient’s response that were not anticipated in the original
question. For example, a mention of chest pain during a question about shortness of breath could prompt
the system to generate additional questions about the nature and triggers of the chest pain. Expansion
also occurs if the response lacks certain critical details that are necessary to understand the patient’s
condition fully.

**Node Decision-Making Process**

The system ensures that repeated questions are avoided by incorporating a node decision-making process
that recursively evaluates the state of each question within the Directed Acyclic Graph (DAG). Questions
that have already been answered or deemed irrelevant are pruned, preventing them from being presented
to the patient again. This is achieved by a decision-making function that evaluates the current node’s state,
following a traversal strategy that systematically identifies unanswered questions ready to be asked.
This node decision-making process, which includes the mechanism to avoid repeated questions, is
formalized in Algorithm 1. The process is structured as follows:

- **Integrating the Decision** : When the patient provides a response to a question, the system uses
    the LLM to evaluate the response and update the status of the current nodev. Based on the
    evaluation, the node can either be fully answered or flagged for further inquiry.
- **Pruning of Answered Questions** : If the LLM determines that the current nodevhas been fully
    addressed, it triggers a prune decision, marking the node as closed. The system then moves to the
    next node in the DAG where the stateS(v) =open, following the defined traversal strategy. This
    ensures that only unanswered questions are considered in the subsequent steps.
- **RecursiveFunction Call to Handle Next Question** : After pruning, the system recursively calls
    the decision-making function to process the next node. If the next node is also marked as closed,
    the function continues to recursively evaluate subsequent nodes until it finds an expand decision,
    ensuring that only relevant and unanswered questions are presented to the patient.
- **ExpandDecisionforNewQuestions** : When a node is evaluated and found to require additional
    follow-up, the LLM generates a set of follow-up questions. These follow-up questions are added to
    the DAG as new nodes with their own priorities and state. If new nodes are generated, the current
    node’s state is updated to explore, reflecting the expansion of the dialogue.


This recursive process ensures that all previously addressed or redundant questions are efficiently
pruned before they reach the patient, streamlining the conversation and preventing unnecessary repetition.
For instance, if the patient has already provided full details about their medications, the system detects
that this question has been answered, prunes it, and moves to the next unanswered question.

**Algorithm 1** Node Decision-Making Algorithm with Repeated Question Handling
**Require:** Current nodev∈V, GraphG= (V,E), Patient responser
**Ensure:** Updated DAGGwith stateS(v)modified, avoiding repeated questions
decision←LLM.evaluate(v,r) ▷LLM returns decision on nodevwith responser
**if** decision.type=prune **then**
SetS(v)←closed ▷Mark node as closed
vnext←next node in DAGGsuch thatS(vnext) =open ▷Following the traversal strategy
Call Node Decision-Making Algorithm on(vnext,G,r) ▷Re-evaluate the next node recursively
**else if** decision.type=expand **then**
SetS(v)←explore ▷Node has generated follow-up questions
**for** each questionqin decision.follow_up_questions **do
if** S(q)̸=closed **then** ▷Avoid adding previously answered questions
Add nodeqtoV
Add edge(v,q)toE
SetS(q)←open
**end if
end for
end if**
Output the updated DAGG= (V,E)

#### 4.2.4 Overview.

The ability to dynamically track the state of a conversation is fundamental to the success of task-oriented
dialogue systems, particularly in complex domains such as medical anamnesis. The system presented
here models the conversation using a Directed Acyclic Graph (DAG), where nodes represent specific ques-
tions or decision points, and edges define potential paths the conversation can take based on the patient’s
responses. Graph State Tracking refers to the continuous monitoring and updating of this conversation
graph, ensuring that the dialogue remains coherent, relevant, and task-focused while avoiding unnecessary
or redundant questions.


Each interaction with the patient involves moving from one node to another within the DAG. The system
makes real-time decisions on whether to prune or expand a node based on the patient’s answers. If a
node is pruned, it signifies that no further follow-up questions are needed for that topic, and the system
moves to the next relevant node. If a node is expanded, the system generates follow-up questions, allowing
a deeper exploration of that topic.
The DAG structure offers significant advantages over traditional dialogue management systems, such
asfinite-statemachinesorhierarchicaltrees, asitallowsmultiplepathstoconvergeonthesamenode. This
flexibility is essential in medical settings, where certain symptoms may require similar follow-up questions
from different starting points. Additionally, the system avoids repetition by tracking which questions have
alreadybeen answeredandpruningthemfromthedialogue. Thisensuresthattheconversationprogresses
logically without asking the patient redundant or irrelevant questions.

**Traversal and Decision-Making in the DAG**

At each step of the interaction, the system evaluates whether to prune or expand the current node based
on the completeness of the patient’s response. Pruning occurs when the system determines that enough
information has been gathered to close the current topic, while expansion occurs when further follow-up
questions are required. The Large Language Model (LLM) is responsible for generating these follow-up
questions and determining their priority based on the patient’s responses.
Nodes in the DAG are color-coded to reflect their state:

- **Green nodes** indicate questions that have been fully answered. If a green node is also a leaf
    node, it signifies that the topic has been pruned, and no more follow-up questions are needed. If a
    green node is not a leaf node, it indicates that the node has been expanded with further follow-up
    questions.
- **Yellow nodes** represent questions that have not yet been answered. These nodes are always leaf
    nodes, meaning that the system has not yet made a decision about whether to prune or expand
    them.

The dynamic traversal of the DAG ensures that the system efficiently gathers information while avoiding
unnecessary repetition. As shown inFigure 13, the diagram illustrates a DAG where answered questions
(green nodes) and unanswered questions (yellow nodes) are visually distinguished. The progression from
node to node is driven by the patient’s responses, and the system continually updates the state of the
graph to reflect the current state of the dialogue.


Figure 13: Example of a Direct Acyclic Graph (DAG) generated by the system, illustrating the sequence of
questions and their relationships.

### 4.3 Algorithmic Clustering for Initial Question Selection.

In this system, patient interactions always begin with no prior medical data available, making each session
a cold start. The system must collect essential information from scratch during the interaction, starting
with broad questions and dynamically adjusting based on the patient’s responses. To ensure the most
effective diagnostic process, the system strategically prioritizes the initial questions, focusing on gathering
critical information early in the interaction without overwhelming the patient. This section outlines how
the system handles patient interactions and how the initial set of questions is selected and prioritized to
optimize the interview process.
Since the system operates with no prior knowledge of the patient’s medical history, it must manage
patient interactions carefully, asking appropriate questions that gather essential information while main-
taining a natural and patient-friendly flow. Without any prior medical data to rely on, the system begins
by focusing on general, broad questions before moving to more specific inquiries as necessary, based on
patient responses.
The system initiates the interview by asking broad, high-priority questions that are applicable to most
patients, irrespective of their medical background. These questions were selected through a clustering pro-
cess and manually prioritized to ensure they provide the most critical health data early on in the interview.
The initial questions aim to identify the patient’s current health concerns and symptoms.
As the patient answers these initial broad questions, the system dynamically adjusts its questioning


based on the information provided. For example, if a patient reports chest pain, the system might follow
up with more specific questions related to cardiovascular health:

- ”Do you have a history of heart disease?”
- ”Have you experienced shortness of breath or discomfort in your chest?”

Alternatively, if the patient mentions fatigue and fever, the system may shift focus toward assessing
possible infections or recent illnesses. This dynamic adaptation ensures that the system remains respon-
sive to the patient’s condition and directs the interview to gather the most relevant information.
The goal of clustering is to identify the most general questions to begin a medical interview, focusing on
prioritizing questions that are broadly applicable across multiple scenarios. To achieve this, a comprehen-
sive dataset was created using diagnostic and treatment algorithms from the American Family Physician
(AFP) collection, covering topics such as dermatology, hematology, and neurology. The process works as
follows:

#### 4.3.1 Data Collection and Preprocessing

Using web scraping, 1,020 diagnostic and treatment algorithms were extracted from the American Family
Physician (AFP) repository, which have been published since 1998. These algorithms cover a wide range
of medical specialties, including dermatology, neurology, hematology, and topics like asthma, back pain,
and anemia. Each algorithm was stored in JSON, encapsulating detailed clinical decision-making steps
aimed at guiding medical professionals through diagnosis and treatment processes.
The first step in transforming these algorithms into a usable sequence of questions was to parse their
structure. Each algorithm contains various elements such as titles, authors, abstracts, and the actual
medical guidance broken down into sections with headers and subheadings. These sections represent
the logical steps involved in making a diagnosis or recommending treatment. To simplify the extraction
process, each algorithm was converted from JSON to Markdown, which is easier to read and work with.
This conversion kept the original hierarchy and decision points, making it simpler for the system to process.
To ensure that each question extracted from the algorithms could be categorized and understood
within a clinical context, the content was labeled based on predefined node types. These nodes represent
key categories in patient interviews, such as History of Present Illness, Review of Systems, Medications,
Chief Complaint, and Family History. Labeling the content with these node types allowed us to organize
the extracted questions in a meaningful way that aligns with medical best practices.


With the Markdown-formatted algorithms ready, a prompt-based approach was employed using Chat-
GPT and LangChain to generate questions from the structured medical logic. Each algorithm was fed into
a language model with specific instructions to extract concise and clear questions that mirrored the steps
in the algorithm. For example, in an asthma algorithm, the system might extract questions like ”Do you
experience shortness of breath?” to assess symptoms, or ”Are you currently using an inhaler?” to check
ongoing treatment.
For every question extracted, the system generated a corresponding justification. These justifica-
tions explain why the question is relevant based on the medical logic of the algorithm. For instance, the
justification for asking about shortness of breath in an asthma-related interview would be linked to the
algorithm’s symptom assessment process. While these justifications are not displayed to patients, they
provide valuable insight for clinicians or developers looking to understand how each question ties back to
the decision-making flow.
Once the questions were extracted and paired with their justifications, they were converted into text em-
beddings using OpenAI’stext-embedding-ada-002model. Text embeddings transform each ques-
tion into a high-dimensional vector that captures the semantic meaning of the text. This allows us to
compare questions based on their meaning, grouping similar questions together and enabling us to orga-
nize them for later use.
By the end of this process, a total of 13,069 questions were generated from the 1,020 algorithms.
These questions vary in specificity, from general questions like ”Are you pregnant?” to highly specific
questions like ”Do you have a history of hereditary nonpolyposis colorectal cancer or BRCA1 mutations?”
Each question directly ties back to a step in its respective algorithm, ensuring that the diagnostic interview
process adheres to established medical guidelines.

#### 4.3.2 Clustering Using Hierarchical K-Means

Once the questions are embedded in a high-dimensional vector space based on their semantic meaning,
the next step is to cluster them into meaningful groups using Hierarchical K-Means. This approach allows
us to start by creating broad clusters of questions and then progressively refine those clusters into more
specific subgroups, mirroring the way diagnostic questioning unfolds in medical practice—from general
inquiries to more focused, condition-specific questions.


**Initial Clustering (First Level)**

In the first step of Hierarchical K-Means, the embedded questions are grouped into broad clusters. This
is achieved by applying the K-Means algorithm, which partitions the dataset into a pre-defined number of
clusters (k). The goal of this phase is to identify large, general groupings of questions that share similar
high-level objectives or diagnostic functions.
At this stage, broad medical categories emerge, such as:

- **Pregnancy-Related Questions** : These might include questions like ”Are you pregnant?” or
    ”Have you experienced any pregnancy complications?”
- **Infection-RelatedQuestions** : Thisgroupcouldincludequestionsaboutcommoninfectionsymp-
    toms like ”Do you have a fever?” or ”Are you feeling fatigued?”
- **Cardiovascular Questions** : These might involve general inquiries like ”Do you experience chest
    pain?” or ”Do you have a family history of heart disease?”
At this top level, the finer nuances between questions are not yet a concern. Instead, the focus is
on grouping them into large categories that reflect major areas of medical concern. This clustering helps
ensure that the system can efficiently navigate through the main topics of a patient interview, whether it
be pregnancy, infection, or heart disease.

**Refining Clusters (Subsequent Levels)**

Once these broad clusters are formed, the next phase involves refining each cluster further. K-Means is
applied again within each cluster to break down the broad groups into more specific subgroups. This step
captures finer distinctions between questions, enabling more targeted inquiries by the system.
For example, within the Pregnancy-Related Questions cluster, the algorithm might form subgroups
such as:

- **General Pregnancy Status** : This could include questions like ”Are you pregnant?” and ”When
    did you confirm your pregnancy?”
- **Symptoms and Complications** : Questions like ”Do you experience nausea?” or ”Have you had
    any unusual bleeding during pregnancy?” might fall into this subgroup.
- **Trimester-SpecificQuestions** : This group could contain questions like ”Which trimester are you
    in?” or ”Have you felt the baby move?”


This hierarchical refinement allows the system to navigate from general diagnostic inquiries to more
specific details as needed. For instance, after determining that a patient is pregnant, the system can
quickly zoom in on trimester-specific questions or check for common complications.

**Hierarchical Structure and Depth**

The depth of the hierarchy depends on the desired granularity of the final question groupings. At each
level, the number of clusters (k) is empirically determined based on the data. For example:

- In the first iteration,k= 10might be defined to split the dataset into 10 broad categories.
- In the next iteration, within each of those categories,k= 5might be applied to further refine them
    into 5 subgroups.
This process continues until the desired level of specificity is reached. As a result, the system achieves
multiple levels of granularity, ensuring it can handle both general and highly specific questioning in a
medical interview. The clustering captures broad categories at the top and refines them as the interaction
with the patient progresses.

**Measuring Similarity and Reassigning Questions**

At each stage of K-Means clustering, the algorithm minimizes the Euclidean distance, which is equivalent to
maximizing the cosine similarity when the vectors are normalized, between each question and its assigned
centroid—the calculated center of the cluster. Questions that are semantically similar (i.e., have a small
distance from the centroid) are grouped together. The algorithm iteratively adjusts the clusters to ensure
that each question is assigned to the cluster where it fits best.
For example, in the Cardiovascular Questions cluster, questions like ”Do you have chest pain?” may
be close to the centroid, while questions like ”Have you ever had a heart attack?” might end up in a slightly
more specific sub-cluster related to cardiac events.

**Filtering Out Specific Clusters**

After refining the clusters to a sufficient depth, a filtering step is applied to remove clusters containing very
specific questions. The goal is to focus on clusters that are broadly applicable to the general population,
particularly for use in cold-start scenarios where the system lacks prior patient data.
For example, a cluster with fewer than 50 questions—such as one focused on rare genetic conditions
like BRCA1 mutations—may be discarded since it is too narrow to be used in the initial stages of a medical


interview. In contrast, clusters containing questions like ”What medications are you currently taking?” or
”Do you have any chronic health conditions?” are retained because they are relevant in almost all patient
interactions.

**Final Clusters**

At the conclusion of the Hierarchical K-Means clustering process, the system has generated a set of broad
clusters that span a wide range of medical conditions and diagnostic inquiries. These clusters form the
basis for the initial questions that will be asked during a patient interview, ensuring that the system starts
with general questions before diving into more specific areas based on the patient’s responses. The
questions within these clusters cover various aspects of the patient’s medical history, current condition,
and potential risks.
For example:

- **ClusterA** : General questions about the patient’s medical history, such as ”Do you have any chronic
    illnesses?”
- **Cluster B** : Medication-related questions like ”Are you currently taking any prescription medica-
    tions?”
- **Cluster C** : Chief complaint questions such as ”What is the primary reason for seeking medical
    attention today?”
By clustering the questions, the system ensures that the initial phase of the medical interview begins
with widely applicable, high-priority inquiries that are relevant across different medical scenarios. As the
interview progresses, the system can dynamically adjust and drill down into more specific areas, ensuring
an adaptive and personalized questioning approach. To further refine this process, the initial questions
were selected based on the clustering and their clinical relevance.

### 4.4 Termination Logic.

In a medical dialogue system, it is essential to ensure that the conversation concludes naturally while col-
lecting comprehensive information. The system is designed to avoid repetitive or unnecessary questions,
but a dedicated termination mechanism is required to ensure that the interaction eventually stops after
gathering sufficient data. The termination logic is implemented to guarantee that the conversation covers
all relevant medical areas while avoiding unnecessarily prolonged interactions.


```
The system uses two key mechanisms to determine when to stop the conversation:
```
- **TerminationScore** : A calculated score that measures how much of the predefined set of medical
    topics (represented as node labels) has been addressed.
- **Failsafe Mechanism** : A limit on the number of exchanged messages to ensure that the conver-
    sation ends after a reasonable amount of interaction.

#### 4.4.1 Calculating Termination Scores and Node Closure

The termination score is the primary measure for determining when to end the conversation. This score
reflects how much of the conversation has covered the complete set of predefined node labels, which
represent distinct medical topics. These labels are a fixed set, defined earlier in the thesis, and cover
all relevant areas of inquiry, such as medications, surgical history, family history, and other key medical
categories.
Because the system cannot terminate the conversation prematurely by focusing on only a subset of
these labels, it must ensure that the dialogue addresses as many of these predefined topics as possible.
The termination score is calculated using the following formula:

Termination Score=# Unique Node Labels Answered# Unique Node Labels (4.1)
Each node label corresponds to a specific medical category, and a node label is considered answered
once the system has asked at least one question related to that label and received a response. As the
system moves through the dialogue, it tracks how many node labels have been closed (i.e., answered) in
relation to the total number of unique labels.
The system ends the conversation when the termination score meets or exceeds a predefined thresh-
old. In the current configuration, this threshold is set to a high value, such as 0.99, meaning that nearly
all of the predefined medical topics must be covered before the conversation can conclude.

#### 4.4.2 Adaptive Stop Criteria.

While the system’s default termination threshold ensures comprehensive coverage of most medical topics,
there is a need for flexibility in adjusting the threshold based on the specific medical context of each
interaction. For instance, in some scenarios, such as routine medical visits or follow-up consultations,
gathering detailed information on every single medical topic may not be necessary.


In these cases, the system can use a lower termination threshold, such as 0.80, which allows the
conversation to end after addressing the most critical medical topics, without requiring exhaustive coverage
of all labels. The lower threshold allows the system to adapt the depth of the conversation based on the
medical situation, while still ensuring that the key areas are covered.
On the other hand, in more complex or critical cases—such as in emergency care or in-depth diagnostic
interviews—a higher termination threshold (such as the default 0.99) ensures that nearly every possible
medicalareais exploredbeforeconcluding theconversation. This is especiallyimportant whendealing with
patients who present with ambiguous symptoms or complex medical histories, where gathering detailed
information from all relevant categories is necessary for accurate medical assessment.

#### 4.4.3 Failsafe Mechanism

In addition to the termination score, the system employs a failsafe mechanism to ensure that the con-
versation does not continue indefinitely, even in cases where the termination score is not reached within
a reasonable number of interactions. The failsafe mechanism limits the total number of messages ex-
changed between the system and the patient, providing a safeguard against potential issues such as
unexpected loops in the dialogue flow or overly long conversations.
The failsafe mechanism sets a maximum limit on the number of patient responses that can be pro-
cessed during the conversation. Once this limit is reached, the system automatically terminates the in-
teraction, regardless of the termination score. This ensures that the conversation concludes within a
reasonable time frame and prevents any risk of an infinite conversation loop or prolonged interactions.
While this mechanism is rarely triggered in practice, it acts as a safety net to ensure that the dialogue
always comes to an end, even in unusual or edge-case scenarios. The primary criterion for terminating
the conversation remains the termination score, but the failsafe provides an additional layer of protection
to guarantee that the patient interaction does not extend unnecessarily.

### 4.5 Medical Report Generation

The medical dialogue system is designed to collect and synthesize all relevant information from a patient
interaction into a comprehensive medical report. This report serves as a structured and concise sum-
mary, facilitating the work of healthcare professionals by providing them with an organized overview of the
patient’s health status. The system leverages the Directed Acyclic Graph (DAG) structure to categorize and
organize patient responses, ensuring that all necessary medical topics are covered and presented clearly.


#### 4.5.1 Structuring the Report Using the DAG

The system’s Directed Acyclic Graph (DAG) is fundamental to the structure of the medical report. Each
node in the DAG corresponds to a specific medical question, and the associated node labels represent
distinct medical categories (such as ”Medications,” ”Symptoms,” or ”Family History”). As the conversation
progresses, the system tracks which nodes have been closed, meaning that the patient has provided a
complete answer, and groups these closed nodes by their labels.
This structure mirrors the way professional medical notes are typically organized, ensuring that the
information is sortedby relevant categories. The node labels provide natural sections for the report, making
it easy to group related questions and responses. This approach helps ensure that the report covers all
necessary medical areas while maintaining a clear and logical flow.

#### 4.5.2 Grouping and Summarizing Patient Responses

Once the nodes are grouped by their respective labels, the system processes the responses to generate
concise summaries for each medical category. These bullet-point summaries focus on the key information
provided by the patient during the conversation. For each node, the system captures both the question
asked and the patient’s response, and then uses a LLM to distill these interactions into brief but informative
bullet points.
For example, if the system collects responses about the patient’s medication use, the summary might
include bullet points such as:

- Patient is currently taking lisinopril for hypertension.
- No known drug allergies reported.
- No recent changes to prescribed medications.
    This method ensures that the information is presented clearly and concisely, helping healthcare pro-
fessionals quickly grasp the most important details. The report generation process guarantees that all
relevant medical categories are covered by including summaries for all closed node labels. Even if a par-
ticular category contains minimal information, such as a single question answered, it is still included in the
report. This approach ensures that the report provides a comprehensive overview of the patient’s health,
covering all necessary topics while avoiding any gaps in the data.
To enhance the report’s usability, the system also organizes the information by priority. Categories that
contain more critical information, such as Medications or Chief Complaint, are presented first, ensuring


that healthcare professionals can quickly access the most important data.
The process of generating the medical report is formalized in Algorithm 2 , which outlines how the
system organizes the responses and produces a comprehensive report:

**Algorithm 2** Medical Report Generation Using DAG
**Require:** DAGG= (V,E), Patient gender
**Ensure:** Medical report with bullet points and symptomatic summary
Vvisitable←{}
**for** eachv∈V **do
if** S(v) =closed orS(v) =explore **then** ▷nodes that have received a decision
AddvtoVvisitableunderv.category
**end if
end for**
Generate bullet-point summaries per category and symptomatic summary using LLM
Order summaries per category by average priorityP(v)and number of nodes
Return MedicalReport with prioritized summaries and symptomatic summary

This algorithm reflects how the system identifies the relevant nodes (those in a closed or explore state),
organizes them by their category, and uses an LLM to generate concise summaries. These summaries are
then prioritized based on the average priorityP(v)and the number of nodes in each category, ensuring
that critical information is presented first.

#### 4.5.3 Generating a Symptomatic Summary

In addition to the bullet-point summaries for each medical category, the system generates a symptomatic
summary. This is a high-level overview of the patient’s overall health, condensed into one or two sen-
tences. The symptomatic summary provides a quick snapshot of the patient’s primary concerns and most
significant symptoms, making it easy for medical professionals to understand the critical aspects of the
patient’s condition at a glance.
For instance, the symptomatic summary might state:

- ”The patient reports controlled hypertension managed with lisinopril, with no significant changes
    in their condition. No drug allergies or recent surgeries were reported.”
This brief summary complements the detailed bullet-point sections by providing an immediate under-
standing of the patient’s health status.


### 4.6 Overview

The overall architecture and flow of the medical dialogue system are designed to ensure that patient
interactions are efficiently managed while collecting comprehensive medical data. The system uses a
Directed Acyclic Graph (DAG) structure to guide the flow of the conversation, with nodes representing
specific medical questions, and node labels categorizing these questions under different medical topics
(such as ”Medications,” ”Symptoms,” or ”Family History”). This structure allows the system to dynamically
adapt the conversation based on the patient’s responses while ensuring that all relevant medical areas are
covered.
At the start of the interaction, the patient is prompted with a question (represented as ”Patient Begins
Interaction” inFigure 14). From there, the patient’s responses drive the decision-making process within
the system, which determines whether to expand the conversation by adding new nodes or prune already
covered topics by selecting the next relevant question. This decision-making process is the central mech-
anism for managing the dialogue and is based on the patient’s conversation history, ensuring that the
system avoids asking repeated or irrelevant questions.
The decision module is responsible for making this choice. When the system expands, new nodes
are added to the DAG, allowing for a deeper exploration of the patient’s medical history. When the system
prunes, it skips redundant questions and moves forward by selecting the next relevant topic. In cases
where there are no more nodes to explore, the system transitions to report generation to create a final
medical report summarizing the patient’s responses.
The interaction does not stop immediately after a new node is added or pruned. Before presenting
the next question to the patient, the system checks whether any predefined stop criteria have been met.
These stop criteria ensure that the system can terminate the conversation once enough information has
been gathered. If the criteria have not been met, the system proceeds by selecting the next question. The
patient is then asked this question, and the process repeats, with the system continually adapting based
on the patient’s responses.
However, once the stop criteria are satisfied—meaning the system has collected enough relevant
information—the conversation ends, and a final medical report is generated. This report organizes the
patient’s responses into sections based on the medical categories defined by the DAG’s node labels. The
final output is a comprehensive summary of the patient’s medical history, which is structured to be clear
and concise for healthcare professionals.


```
Figure 14: Interaction Flow Diagram.
```
```
InFigure 14, the flowchart illustrates the key components and flow of the dialogue system:
```
- **Patient Begins Interaction** : The patient opens the app and starts the interaction. The system
    then greets the patient and presents the first question to begin the conversation.
- **Decision Module** : The system decides whether to expand or prune based on the patient’s re-
    sponses. This process involves either expanding the DAG with new nodes or pruning the conversa-
    tion to avoid repeating previously answered questions.


- **Stop Criteria Check** : The system continually checks whether it has met the conditions to stop
    the conversation and generate the final report. If the criteria have not been met, the system selects
    the next question and continues the dialogue.
- **Generate Medical Report** : Once the stop criteria are met, the system generates a structured
    medical report based on the collected data.
- **Interaction End** : After the report is generated, the system concludes the interaction.

This diagram illustrates how the system balances the need for thorough data collection with efficiency,
ensuring that redundant questions are avoided and the interaction stops at an appropriate point once
enough information has been gathered.
The flow diagram emphasizes the system’s capacity for real-time decision-making and adaptability,
reflecting its ability to dynamically manage patient interactions while optimizing for comprehensive med-
ical data collection. The final outcome is a highly structured medical report that provides healthcare
professionals with a complete and well-organized summary of the patient’s responses.
From a high-level perspective, the system operates as shown inFigure 15. The patient begins the inter-
action through the Patient Application, where their responses are processed using a Directed Acyclic Graph
(DAG) structure to guide the conversation. The system dynamically adapts based on these responses, de-
ciding whether to expand the dialogue by asking more relevant questions or to prune unnecessary ones.
Once sufficient information is gathered, a structured Medical Report is generated, summarizing the pa-
tient’s data.
The Physician Application enables healthcare professionals to access and review these reports. Physi-
cians can select, view, and modify reports as needed, with any updates applied directly to the original
report. This flow ensures efficient management of patient interactions and physician evaluations. Further
exploration of the Patient Application and Physician Application is provided in the following chapter.


Figure 15: High-level system interaction flow between the Patient Application, Medical Report, and Physi-
cian Application.


### Chapter 5

**Development**

This chapter explores the development of the system and how different technologies were combined to
build the anamnesis platform. It provides a detailed breakdown of each component and explains how they
work together to create the final solution.
The system was designed with flexibility and scalability in mind to ensure smooth user testing and
interaction. A RESTful API backend was developed to support both the physician and patient applications.
Built using Python 3.8 and FastAPI, the backend serves as the core of the system, facilitating communi-
cation between the two apps. FastAPI was selected for its modern, asynchronous capabilities, allowing for
efficient data exchange and real-time interaction between users and the system.
Both the Physician Application and the Patient Application were developed using Flutter, a cross-
platform development framework. Flutter enables the applications to function seamlessly across multiple
platforms, including web, Android, and iOS. By using a single codebase, development is streamlined,
ensuring a consistent user experience across devices while making future updates easier to manage.
Together, these technologies form a cohesive solution, with the backend ensuring smooth communi-
cation and the front-end delivering a user-friendly interface on various platforms.

### 5.1 Backend

The backend is built on four key pillars: LLMs, database access, storage, and cloud deployment. It was de-
signed to support multiple working environments, ensuring clear independence between the database and
storage systems. The current deployment architecture allows for the creation of isolated system replicas,
which has been leveraged to establish distinct development, staging, and production environments. This
separation adds an essential layer of security and stability when working on different stages of the appli-
cation. The cloud infrastructure is hosted on Google Cloud Platform (GCP), providing scalability, reliability,
and seamless integration with the other backend components.


#### 5.1.1 Large Language Models

Currently, ChatGPT is the only LLM employed within the anamnesis system, with variations in the specific
versions used depending on the functional requirements of each module. Interaction with the LLM is
facilitated through LangChain, a software framework designed to streamline the integration of LLMs into
applications. LangChain provides modular development capabilities for LLM-enabled systems, offering a
simple and flexible Python syntax to manage and fine-tune different aspects of the model.
In the context of the anamnesis system, LangChain enables the creation of modules, each serving a
distinct purpose. This modularity allows for granular control over key parameters, such as the version of
the LLM used and the temperature setting. LLM temperature is a critical parameter, ranging from 0 to 1,
which influences the creativity and variability of the model’s output. Higher temperatures encourage more
diverse and imaginative responses, while lower temperatures produce more consistent and predictable
answers.
Balancing LLM temperature is crucial when working with language models, as different tasks demand
varying degrees of creativity and control. For instance, some modules benefit from highly controlled and
deterministic outputs, while others may require more flexibility and nuance in response generation. Tem-
perature can be thought of as a faucet: the more it’s opened (higher temperature), the more creativity and
diversity flow from the model. Conversely, a lower temperature provides a more focused and constrained
response. The system dynamically adjusts the temperature based on the specific goals of each module.
The current implementation of the anamnesis system is divided into the following modules:

- DagScreener: Thismoduleisresponsibleforcontinuingtheinteractionwiththepatientbytravers-
    ing through the DAG (Directed Acyclic Graph) of questions. As the patient provides answers, the
    system progresses to the next question in the sequence and poses follow-up questions as needed.
    Since this module primarily serves to ask questions, it utilizes a lighter, less resource-intensive
    version of ChatGPT—specifically,gpt-3.5-turbo. Given that the space of possible question for-
    mulations is large, and the system must relate previous answers to current questions, a temperature
    setting of 0.5 is used. This strikes a balance between predictability and creativity, ensuring that the
    questions are neither too rigid nor overly creative.
- Decision: AsexplainedintheSystemDesignchapter, theDecisionmoduledetermineswhether
    a topic requires further exploration with follow-up questions or whether the current question can be
    pruned if the patient’s responses are sufficient. Unlike theDagScreener, this module requires
    a deeper understanding of the entire conversation to make informed decisions. Therefore, it uses


```
a more advanced model,gpt-4o, which offers a good balance between complexity and latency.
Although this is not the most powerful version available, it provides an optimal tradeoff between
performance and speed—essential for maintaining near real-time interaction with the patient. The
temperature is set to 0.2 in this module to prioritize predictable outputs and minimize unnecessary
creativity, which is crucial for making accurate decisions in a medical context.
```
- MedicalReport: This module generates a comprehensive medical report based on the entire
    DAG of questions and answers accumulated during the interaction. The report consolidates all
    the relevant medical findings into a single document, requiring the LLM to have a sophisticated
    understanding of the dialogue and its nuances. Given the complexity of summarizing key medical
    takeaways, thismoduleutilizesgpt-4-turbo, themostpowerfulandperformantversioncurrently
    employed. Since latency is not a critical factor in this phase (as the patient interaction has already
    concluded), the report generation can occur asynchronously. Like theDecisionmodule, the
    temperature is set to 0.2 to ensure the report is accurate, structured, and free from unnecessary
    creative interpretation.

**Working with a DAG**

The logic for managing a Directed Acyclic Graph (DAG) within the current system is not directly tied to LLMs,
but it is an essential component of the overall process. As more follow-up questions are generated, they
need to be traversed in a structured and logical sequence. To achieve this, a custom graph implementation
was developed in Python, enabling the seamless addition of new nodes and their traversal in a predefined
order.
For traversing the questions in the DAG, depth-first search (DFS) was selected. This method is more
intuitive when considering the relationship between questions and their follow-ups. When a question is
posed, it is expected that the follow-up will be directly related to the context of the previous question. DFS
helps maintain this logical flow by exploring each branch of the graph fully before moving to the next,
ensuring that the system stays within the same context until all related questions are addressed.
The key difference between DFS and breadth-first search (BFS) lies in how they navigate through the
graph. In a BFS traversal, the system would explore all questions at the same level of the graph before
moving deeper into the next level. This means that even if a follow-up question is generated from the
current question, BFS might select an unrelated question from a different branch of the graph next. For
instance, if the system is asking about pregnancy, a BFS approach might jump to a completely different
topic—such as a question about allergies—before returning to the relevant pregnancy-related follow-ups.


This can disrupt the natural flow of the conversation and make it seem disjointed.
In contrast, when a follow-up question is generated, it becomes a node with a direct edge connecting
it to the original question. By using DFS, the traversal remains focused on the same branch of the graph,
ensuring that all questions within the same context are explored before moving to another topic. This
maintains a smoother, more contextually coherent interaction, which is crucial for systems designed to
simulate logical, human-like conversations.

**Structured Output**

In most cases, raw text generation is sufficient to meet the intended goal. This is especially true for the
DagScreenermodule, where the expected output is a straightforward text message that the patient can
read directly as a standalone response.
However, theDecisionandMedicalReportmodules have more specific requirements. For in-
stance, when a decision is made, the system needs to identify whether it’s a prune or expansion decision.
In the case of an expansion, follow-up questions must be added as nodes in the DAG. Similarly, the gener-
ated medical report requires a structured format. Physicians expect clear takeaways with properly labeled
sections in the user interface. Therefore, the outputs from these modules need to be more structured and
easier to manipulate than simple text.
The main challenge is that LLMs are typically trained to generate plain text, but in these cases, a more
structured format is required. Ideally, the model should produce output in JSON format, adhering to a
specific schema, which would allow for easier manipulation and integration into the system.
Drawing inspiration from context-free grammars, it’s possible to constrain the output of an LLM to
ensure it follows a specific grammar or format [Willard and Louf, 2023 ]. Using ChatGPT and OpenAI
Functions, it’s feasible to enforce the model’s output to follow a predefined JSON schema. OpenAI Func-
tions allow you to define the target schema for the model to generate. Additionally, Pydantic, a widely-used
data validation library, is employed to automatically generate JSON schemas from Python classes and to
convert JSON data into Python objects. This enables the LLM to generate a valid Python class from its
output, ensuring compatibility and ease of use.
For example, when theDecisionmodule produces an output, it is represented as a Python class
that contains an enum to indicate whether the decision is to prune or expand, along with a list of follow-up
questions in case of expansion. This structured approach ensures the output is seamlessly integrated into
the system’s workflow.


#### 5.1.2 Database

Firestore was chosen to accelerate the development process due to its cloud-native design, low mainte-
nance requirements, and NoSQL structure, making it an ideal solution for the system. Firestore allows for
the creation of multiple collections, which are used to store system results efficiently. It serves a dual pur-
pose, managing both the dialogue state and application-specific data, such as access control for certain
features.
Whenever a new conversation is initiated, the system creates a document in Firestore to store it. As the
patient or user provides responses, the document is continuously updated. The same process is applied
to medical report generation—each time a report is created, it is saved as a document within Firestore,
ensuring all data is organized and easily retrievable.

#### 5.1.3 Storage

The system supports audio communication, which necessitates hosting audio files that are delivered to
the patient. Whenever a patient expects an audio response, the LLM first generates the output text, which
is then converted into speech using OpenAI’s Text-to-Speech model. For the patient to access and listen to
the audio, the file must be stored in a location that is easily accessible externally. To address this, Google
Cloud Storage, a managed service for storing unstructured data, was utilized.
A dedicated bucket was created within Cloud Storage to host the audio files. Each time an audio
response is generated, it is stored in this bucket. The patient application then uses signed URLs to securely
retrieve and play the audio file for the patient, ensuring smooth and efficient access to the generated
content.

#### 5.1.4 Deployment

The deployment of the system is centered around containerization and infrastructure as code to ensure
scalability, reliability, and ease of maintenance. The core of this process involves building a Docker image
that contains the serving code, which includes the necessary configurations for running the system. This
containerized approach allows for a consistent runtime environment across development, staging, and
production, ensuring that the system behaves the same in all environments.
Once the Docker image is built, it is deployed to Google Cloud Run, a fully managed service that
automatically scales the application based on incoming traffic. Cloud Run is an ideal choice for handling
the dynamic nature of the system, as it abstracts the underlying infrastructure, allowing focus on the


application logic without worrying about managing servers.
For infrastructure management, Terraform is used. Terraform is an infrastructure-as-code tool that
enables defining and provisioning cloud infrastructure in a declarative manner. By using Terraform, the
system’s infrastructure, including Cloud Run services, Firestore databases, and Cloud Storage buckets,
is codified, versioned, and easily reproducible. This approach reduces human error and enhances the
system’s ability to scale and adapt to changes in demand.
In addition to the core infrastructure, Cloud Tasks is utilized to allow asynchronous tasks within the
system, such as generating a medical report 15 minutes after the patient sends the last message. This
ensures that reports are generated without requiring the patient to be actively engaged, maintaining system
responsiveness while efficiently handling background processes.

### 5.2 User Interface

A core aspect of this system lies in how patients interact with it. The system must be versatile enough to
function in a varietyof settings, such as hospitals, homes, or remotelocations. Moreimportantly, it must be
extremely easy to use to accommodate a broad range of users, regardless of their technological proficiency.
Achieving this requires leveraging generalizable frameworks and designing intuitive, minimalistic interfaces
that are optimized for usability.

- **The Physician Application** is intentionally designed to be as simple as possible. Its main func-
    tions include listing, viewing, and editing medical reports generated through the system’s interac-
    tions with patients. The application’s primary goal is to support physicians in utilizing the insights
    obtained from the patient’s dialogue with the system. The interface is straightforward, allowing
    physicians to efficiently review and manage patient data without unnecessary complexity, thus im-
    proving their workflow and decision-making process.
- **The Patient Application** , on the other hand, is tailored specifically to simplify the patient’s in-
    teraction with the system. Given the diverse range of potential users—from those in hospital en-
    vironments to patients using the system at home—the design focuses on making communication
    as seamless and intuitive as possible. The user interface prioritizes accessibility, ensuring that
    patients can easily navigate and interact with the system, whether through text or hands-free voice
    commands.
Both applications were developed with usability at their core, featuring simple screens that guide users
through their respective tasks without overwhelming them with technical details. Detailed examples of the


user interfaces for both applications are presented in the ”User Interface” chapter, illustrating how design
choices were made to enhance the overall user experience.

#### 5.2.1 Multi-Platform

With the first objective of cross-platform compatibility in mind, the system was developed using Flutter, an
open-source UI software development kit. Flutter allows for the creation of applications across multiple
platforms from a single codebase, enabling efficient deployment on the web, Android, iOS, Linux, macOS,
and Windows. This approach significantly reduces development overhead while maintaining a consistent
user experience across devices.
To meet the distinct needs of the two user groups—patients and physicians—two separate Flutter
projects were created: the Patient Application and the Physician Application. Each project is indepen-
dent, allowing for flexibility in design and functionality, while still benefiting from the shared advantages of
Flutter’s cross-platform capabilities.

- **ThePatientApplication** is fully functional across multiple platforms, including web, Android, and
    iOS. This broad compatibility ensures that patients can access the application on their preferred
    device, providing greater accessibility and ease of use. The decision to support these platforms
    stems from the need for patients to have seamless access to the system, whether at home or on
    the go.
- **The Physician Application** , while developed using the same underlying Flutter framework, is
    currently available only as a web application. The choice to limit this application to the web is
    based on the specific workflow requirements of physicians, who often access such tools from desk-
    tops or laptops within clinical settings. Given the nature of physician tasks, the web platform has
    been deemed sufficient to meet their needs. Nevertheless, the system’s architecture allows for the
    possibility of extending the Physician Application to other platforms like Android or iOS in the future
    if required.
In summary, by leveraging Flutter’s cross-platform capabilities, the system achieves its goal of broad
accessibility for patients while ensuring a streamlined, purpose-built experience for physicians on the web.

#### 5.2.2 Interaction

The interaction with the system can be divided into two key components: interaction with the physician
and interaction with the patient. This Master’s project focused on ensuring the following objectives for


physician interaction:

- **Seamless integration with existing hospital software** : To minimize friction in the workflow,
    medical reports generated by the system should be easily transferable to other hospital systems.
    With this in mind, the application includes a ”Copy to Clipboard” feature that allows physicians to
    quickly copy the full contents of any medical report. This enables straightforward export to other
    medical software, such as Electronic Health Record (EHR) systems, without requiring complex file
    formats or additional steps, ensuring compatibility with the tools already in use.
- **Simplicity and clear objectives** : The design of the physician’s interface emphasizes simplic-
    ity and ease of use. The application is structured around two main screens. The first screen
    provides an overview, listing all medical reports that are waiting for physician review. This allows
    the physician to quickly identify outstanding tasks. The second screen is where the actual review
    and editing of individual medical reports occur. All necessary information is presented in a clean,
    organized manner, making it easy for the physician to access and modify data as needed. The
    interface is designed to reduce cognitive load, allowing physicians to focus on patient care rather
    than navigation.
Similarly, the patient application is built with a user-friendly design that focuses on guiding the patient
through their interaction with the system. Upon launching the app, the patient is immediately directed to
a screen where they can begin engaging with the system. The interaction process is simple: patients can
choose between two modes of communication.
- **Text-based interaction** : In this mode, the patient sends messages to the system in a familiar
chat format, typing out their responses.
- **Hands-free interaction** : This mode offers a fully automated experience, leveraging the device’s
microphone to capture the patient’s speech. The system utilizes OpenAI’s Whisper model to convert
the audio into text, which is then fed to a Large Language Model (LLM) for processing. The system’s
response is converted back into speech and played through the patient’s speakers. This process is
continuous, with the system handling the conversation flow without the patient needing to manually
operate the app. By default, the system starts in hands-free mode, offering maximum convenience,
although this setting can be changed in the app’s configuration menu.
Additionally, the system is designed to automatically stop listening after detecting 5 seconds of silence
from the patient. However, in noisy environments, continuous background noise may prevent the system


from detecting silence. To address this, a manual stop feature has been implemented. If necessary, the
patient can tap the screen while the app is recording, immediately halting the audio capture and sending
the recorded audio to the backend for processing. This eliminates the need to wait for the automatic 5-
second silence threshold, improving the overall user experience in environments where background noise
might otherwise disrupt the interaction.

#### 5.2.3 Deployment

The deployment of both the Patient and Physician Applications was implemented with an emphasis on
accessibility, security, and maintainability. Both applications use Firebase Authentication to ensure secure
access with shared credentials across the platforms. However, specific permissions are required to access
the Physician Application, which are granted manually by an authorized member of the research team.
This role-based access control ensures that only physicians and authorized personnel can view and edit
sensitive medical data.
The applications are hosted using cPanel, a widely adopted web hosting control panel, and are de-
ployed as subdomains under hci4h.org. This solution was chosen for its user-friendly interface and robust
management features, which simplify the deployment process and provide a stable platform for the appli-
cations. The URLs for accessing the applications are:

- **Patient Application** : https://osler.hci4h.org/
- **Physician Application** : https://osler-reports.hci4h.org/
By using cPanel for hosting, updates and maintenance can be efficiently managed, ensuring that the
system remains available and responsive. Additionally, this setup allows for potential future scalability, as
the hosting environment can easily accommodate growth in the number of users or additional features
without requiring significant changes to the underlying infrastructure.


### Chapter 6

**Osler Apps, An Overview**

The user interfaces (UIs) developed for this system serve as the bridge between patients and healthcare
providers, facilitating seamless and effective interactions throughout the medical anamnesis process. The
system consists of two distinct applications—the Patient Application and the Physician Application—each
with unique design goals that cater to the specific needs of their respective users. Both applications
prioritize usability and accessibility, ensuring that users can efficiently navigate the system, regardless of
their technical proficiency.
The Patient Application is designed to guide patients through a medical interview, collecting critical
health information in a structured yet user-friendly manner. Given the diverse user base, which may include
individuals of varying technological skills, the interface is simple and intuitive. Whether the system is being
used in hospitals, at home, or in remote settings, the focus is on ease of interaction, with options for both
text-based and hands-free voice communication. The interface is dynamic, adjusting in real-time to the
patient’s responses, creating a personalized experience that smoothly adapts to the evolving conversation.
On the other hand, the Physician Application is optimized for healthcare professionals who need to
review, edit, and manage the data collected during patient interviews. Its design emphasizes clarity and
simplicity, allowing physicians to quickly access, review, and modify patient reports generated from the
dialogue with the system. The interface supports medical workflows by providing organized summaries
of patient data, helping physicians make informed decisions efficiently. Features such as real-time data
access, report editing, and easy integration with existing hospital software ensure that the application fits
seamlessly into the physician’s clinical routine.
This chapter provides a detailed walkthrough of the user interfaces for both applications, accompanied
by screenshots that demonstrate key features and design decisions. Each application will be explored in its
own section, where the focus will be on explaining how the UI elements support the specific functionalities
required by patients and physicians. These screenshots highlight how the interface components were
developed with a focus on improving user experience, guiding patients through the interview process, and


enabling physicians to manage patient data effectively.

### 6.1 Patient

The Patient Application serves as the gateway for patients to interact with the Osler system, an AI-driven
platform designed to automate the medical history-taking process. This application is focused on providing
a seamless and user-friendly experience for patients, allowing them to easily participate in a medical
interview by voice and navigate through their past interactions with the system. The interface is designed
to be intuitive, making it accessible to users of all technological backgrounds.
Upon accessing the application, patients can log in, initiate a new medical interview, or view their
previous interview history. The interface uses a conversational, voice-driven approach that enables patients
to interact with the system in a hands-free manner, streamlining the anamnesis process and reducing the
need for manual input. The following sections provide an overview of the key screens and functionalities
within the Patient Application, with screenshots referenced to highlight the main features.

#### 6.1.1 Logging In and Account Registration

The first screen patients encounter is the Login Screen (Figure 16). Here, users are prompted to enter
their credentials to access the system. If the user does not have an account, they can register by selecting
the Sign Up option, which takes them to the Registration Screen (Figure 17). Both screens are designed
to ensure a straightforward login and registration process, minimizing the barriers to entry and ensuring
that patients can quickly access the medical interview system.


Figure 16: The Login Screen for the Patient Application, where users can log in or register a new account.

```
Figure 17: The Registration Screen for new users signing up for the Patient Application.
```
#### 6.1.2 Landing Screen: Choosing an Action

Once logged in, the patient is directed to the Landing Screen (Figure 18). This screen presents two main
options:


- **Start a New Medical Interview** : This option allows the patient to begin a new medical interview
    with the Osler system, starting the voice-driven anamnesis process.
- **See Medical Interview History** : This option enables patients to view the full history of their past
    interactions with the system.

The landing page is designed to be minimalistic and accessible, guiding the user effortlessly toward
their desired action. Whether they are starting a new interaction or reviewing past conversations, the
patient can easily navigate through the available options without unnecessary complexity.

Figure 18: The Landing Screen, displaying the two main options: starting a new medical interview or
viewing the conversation history.

#### 6.1.3 Starting a New Medical Interview

When the patient selects the ”Start a New Medical Interview” option, they are taken to the Start Screen
(Figure 19), where the system begins the conversation by greeting the patient with an audio response
and initiating the anamnesis process. The interaction proceeds in a fully voice-driven manner, where the
system asks questions, and the patient responds by speaking into the device.


Figure 19: The Start Screen, where the Osler system initiates the medical interview with an audio prompt.

Once the system has completed its audio prompt, the Speak Screen (Figure 20) is displayed, indicating
that the system is waiting for the patient’s response. The patient’s audio is recorded until they stop
speaking or press the screen to end the recording. This seamless flow allows the system to capture
the necessary information without requiring the patient to navigate through text-based forms or multiple
screens. The hands-free functionality prioritizes accessibility and ease of use, making the interaction
natural and intuitive.


Figure 20: The Speak Screen, indicating that the system is recording the patient’s response during the
medical interview.

#### 6.1.4 Reviewing Conversation History.

After completing an interaction, the patient can review their previous conversations with the system by
selecting the ”See Medical Interview History” option on the Landing Screen. This leads to the Conversation
History Screen (Figure 21), where all past interactions are listed in chronological order. Each entry contains
essential details, such as the date and time of the interview, enabling patients to quickly identify and select
the relevant conversation they wish to revisit.


Figure 21: The Conversation History Screen, displaying a list of the patient’s previous medical interviews
with the system.

By clicking on any of the previous interactions, the user is directed to the Conversation Details Screen
(Figure 22), which displays the full message exchange between the patient and the system. Here, patients
can see a written record of the dialogue, including both the system’s questions and their own responses.
This feature allows patients to review important medical information discussed during previous interviews,
providing them with a comprehensive overview of their medical history as captured by the system.


Figure 22: The Conversation Details Screen, where the full message exchange from a previous medical
interview is displayed.

#### 6.1.5 Ending the Interaction

The Osler system automatically determines when enough information has been gathered during the in-
terview. Once the system concludes that it has collected sufficient data, the interaction ends, and the
patient is directed to a brief survey to provide feedback on their experience. This feedback is essential
for improving the system and ensuring that it continues to meet the needs of users. After submitting the
survey, the patient can either review their previous interactions or begin a new one, completing the user
journey.

### 6.2 Physician.

The Physician Application is designed to streamline the process of reviewing, editing, and approving med-
ical reports generated by the system based on patient interviews. The interface is built with simplicity and
efficiency in mind, allowing physicians to quickly access pending reports, make necessary adjustments,
and finalize their conclusions with minimal friction. This section provides a detailed walkthrough of the
key screens and functionalities of the Physician Application.
After authentication, the physician is taken directly to the application’s core functionalities, which


include viewing the list of pending medical reports, editing individual reports, and copying report content
for use in other systems. Each of these features is critical to the physician’s workflow, as they help
facilitate the review and submission of comprehensive, well-structured medical reports. The following
sections explore these functionalities in detail, with screenshots referenced to highlight key elements.

#### 6.2.1 Viewing Pending Medical Reports

Upon entering the Physician Application, the user is presented with a landing screen that lists all pending
medical reports awaiting review and approval. This Landing Screen (Figure 23) acts as a dashboard where
physicians can quickly see a summary of all medical reports that require their attention. The reports are
organized in a queue format, allowing physicians to prioritize and select the reports they wish to review
first. Each report entry includes essential metadata, such as the patient’s name and the time since the
report was generated, providing physicians with enough information to manage their workflow efficiently.

Figure 23: The Physician Application Landing Screen, displaying a list of all pending medical reports
awaiting review.

#### 6.2.2 Editing Medical Reports

Once a report is selected, the physician is taken to the Edit Report Screen (Figure 24). This screen displays
a detailed summary of the medical report generated from the patient’s interaction with the system. The
report is organized into sections, such as Chief Complaint, History of Present Illness, Medications, and


Family History, reflecting the structure of the dialogue. The system’s automated conclusions are presented
in editable fields, allowing the physician to:

- Modify any section of the report as necessary, ensuring the content aligns with the physician’s
    clinical judgment.
- Add additional notes or clarifications based on the patient’s condition or responses that may not
    have been fully captured by the system.
- Remove any irrelevant or incorrect details that may have been included during the patient dialogue.

The Edit Report Screen is designed to make the editing process as intuitive as possible, with clearly
labeled sections and an easy-to-use text-editing interface. This ensures that physicians can efficiently make
changes without being overwhelmed by a complex UI.

Figure 24: The Edit Report Screen, where physicians can modify the contents of the medical report, adding
or removing details as needed.

#### 6.2.3 Copying Medical Reports

One of the critical features of the Edit Report Screen is the ability to quickly copy the contents of the
medical report using the Copy to Clipboard feature (Figure 25). This functionality allows physicians to
transfer the report into other hospital systems, such as Electronic Health Record (EHR) platforms, with


ease. Instead of exporting reports as files or navigating through multiple steps, the physician can simply
click the Copy button to copy the entire report. This feature significantly reduces the time required to
integrate the medical report with other tools and ensures compatibility with the hospital’s existing software
infrastructure.

Figure 25: The Copy to Clipboard feature, allowing the physician to copy the contents of the edited medical
report for use in other systems.

#### 6.2.4 Submitting Medical Reports.

After reviewing and making any necessary changes, the physician can submit the finalized medical report
by clicking the Submit button at the top right of the Edit Report Screen. Upon submission, the physician is
prompted to fill out a brief survey evaluating the system’s performance during the dialogue with the patient.
This feedback mechanism is crucial for improving the system over time, ensuring that it continues to meet
the needs of physicians and patients alike. Once the report is submitted, the physician can return to the
Landing Screen to review other pending reports, continuing the workflow seamlessly.


### Chapter 7

**Results and Discussion**

This chapter presents the results and discussion of the experiment conducted to evaluate the patient
and physician applications developed during this research. The chapter begins by outlining the usability
and workload results for both applications, using metrics from NASA-TLX, SUS, and QUIS to provide a
detailed analysis of cognitive load, ease of use, and overall satisfaction. Each application’s performance is
discussed separately, highlighting key strengths and areas for improvement based on user feedback. The
chapter then delves into additional feedback provided by participants, offering insights into specific aspects
of the applications, such as question relevance, report generation efficiency, and system responsiveness.
Finally, the results are discussed in the broader context of the system’s usability and potential impact on
clinical workflows, identifying limitations and suggesting directions for future work.

### 7.1 Experiment Overview

The following experiment was designed to evaluate the usability, workload, and overall user satisfaction of
both the patient and physician applications. A total of five practicing physicians participated, each tasked
with completing a series of predefined actions in both applications. After interacting with the systems,
participants provided feedback through structured surveys, allowing for a comprehensive analysis of their
experiences. Thegoalofthisexperimentwastoassesstheeffectivenessandeaseofuseoftheapplications
in a real-world medical context, ensuring that the design aligns with the needs of healthcare professionals
and patients.

#### 7.1.1 Tasks

Each participant was tasked with performing a set of sequential actions on both applications, followed by
completing a survey regarding their experience.
Participants were instructed to follow the provided steps with minimal external assistance, ensuring


an unbiased perception of the system.
For the patient application, participants were asked to:

- Access the patient application website
- Create an account
- Log in to the application
- Start a new medical interview
- Answer the questions during the interview
- Exit the conversation
- Review the conversation history
- Restart a conversation from the conversation history

For the physician application, participants were informed that the same credentials were used across
both applications, so creating a new account was unnecessary. They were asked to perform the following
actions:

- Access the physician application website
- Log in to the application
- Open one of the pending medical reports
- Add missing information to the report
- Remove information from the report
- Copy the report to the clipboard
- Submit the completed medical report

After testing each application, participants completed a survey reflecting their experience with the
tasks performed.


#### 7.1.2 Evaluation Methods

To comprehensively assess the patient and physician applications developed during this research, three
distinct evaluation methods were employed: the NASA Task Load Index (NASA-TLX), the System Usability
Scale (SUS), and the Questionnaire for User Interaction Satisfaction (QUIS). Additionally, specific questions
tailored to each application were included to capture more detailed insights. Each method addresses a
different aspect of user interaction, ranging from cognitive workload to usability and overall user satisfac-
tion. Together, these tools provide a holistic view of the applications’ performance as experienced by the
physicians and the simulated patient use cases.

**NASA Task Load Index (NASA-TLX)**

The NASA Task Load Index (NASA-TLX) was used to measure the perceived workload of the physicians
when interacting with the applications. NASA-TLX is a widely used tool for assessing the cognitive and
physical demands placed on users during task execution. It typically evaluates six dimensions of workload:
Mental Demand, Temporal Demand, Effort, Frustration, Performance, and Physical Demand. However, in
this study, Physical Demand was excluded as the tasks were conducted in a virtual environment, where
physical exertion was not relevant.
Participants were asked to rate the remaining five dimensions on a scale from 1 to 10, where higher
scores indicate greater workload. These scores were then scaled by a factor of 10 to fit the standard
NASA-TLX 0–100 range. The five dimensions rated were:

1. **Mental Demand** : How mentally demanding was the task?
2. **Temporal Demand** : How hurried or rushed was the pace of the task?
3. **Effort** : How hard did you have to work to accomplish your level of performance?
4. **Frustration** : How insecure, discouraged, irritated, or stressed did you feel during the task?
5. **Performance** : How successful do you think you were in accomplishing the goals of the task?
These adjusted ratings were then averaged to compute an overall workload score for each participant,
providing insights into the cognitive load experienced while using both applications. The overall workload
score is calculated using the following formula:

```
Workload Score=^15 × 10 ×
```
##### ∑^5

```
i=1
```
```
Dimensioni (7.1)
```

Where Dimensionirepresents the participant’s rating for each of the five dimensions (Mental Demand,
Temporal Demand, Effort, Frustration, and Performance), and the result is scaled by 10 to align with the
standard NASA-TLX range.

**System Usability Scale (SUS)**

TheSystemUsabilityScale(SUS)wasusedtoevaluatetheoverallusabilityofboththepatientandphysician
applications. SUS is a standardized tool that measures perceived ease of use across ten statements, with
responses provided on a 5-point Likert scale, ranging from 1 (strongly disagree) to 5 (strongly agree). The
statements asked were:

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to be able to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.
To calculate the final SUS score, the individual item scores are adjusted, summed, and multiplied by
a constant to generate a score between 0 and 100, where higher scores indicate better usability. SUSi
corresponds to the response to the i-th question in the SUS questionnaire. The scoring process works as
follows:
1. For the odd-numbered items (statements 1, 3, 5, 7, 9), subtract 1 from the scale value (transforming
the score from 1–5 to 0–4).
2. For the even-numbered items (statements 2, 4, 6, 8, 10), subtract the scale value from 5 (trans-
forming the score from 1–5 to 4–0).


3. Sum the adjusted scores for all items, resulting in a value between 0 and 40.
4. Multiply the sum by 2.5 to obtain the final SUS score, which will be between 0 and 100.
    The formula for calculating the final SUS score is expressed as:

```
SUS Score= 2. 5 ×
```
##### 

#####  ∑

```
i∈{ 1 , 3 , 5 , 7 , 9 }
```
```
(SUSi−1) +
```
##### ∑

```
i∈{ 2 , 4 , 6 , 8 , 10 }
```
```
(5−SUSi)
```
##### 

#####  (7.2)

**Questionnaire for User Interaction Satisfaction (QUIS)**

The Questionnaire for User Interaction Satisfaction (QUIS) was used to measure satisfaction with specific
aspects of the applications’ interfaces. Physicians rated the following nine questions on a scale from 1
(very dissatisfied) to 9 (very satisfied):

1. **Ease of Learning** : How satisfied are you with the ease of learning to use the application?
2. **Response Time** : How satisfied are you with the system’s response time?
3. **Navigation** : How satisfied are you with the navigation of the application?
4. **Visual Layout** : How satisfied are you with the visual layout of the application?
5. **Interface Consistency** : How satisfied are you with the consistency of the application’s interface?
6. **Clarity of Messages** : How satisfied are you with the clarity of the messages and warnings in the
application?
7. **General Functionality** : How satisfied are you with the overall functionality of the application?
8. **Accessibility** : How satisfied are you with the accessibility features of the application?
9. **Error Recovery** : How satisfied are you with the error messages and recovery options in the
application?
The responses were averaged to generate an overall satisfaction score for each participant, providing
detailed feedback on the user experience of both applications. The overall QUIS score is calculated using
the following formula:

```
QUIS Score=^19 ×
```
##### ∑^9

```
i=1
```
```
Questioni (7.3)
```

where Questionirepresents the participant’s rating for each of the nine questions. The result reflects
the participant’s overall satisfaction with the application.

**Additional Application-Specific Questions**

In addition to the standardized questions from NASA-TLX, SUS, and QUIS, application-specific questions
were included to capture more detailed feedback on each system’s functionality.

**Patient Application**

- **Irritation** : Did you find the number of questions asked by the application to be irritating?
- **Effectiveness** : Did you find the questions appropriate and effective in addressing your medical
    needs?
- **Relevance** : Did you feel the questions were not very relevant to your medical needs?

**Physician Application**

- **Efficiency** : Is the process of reviewing and using the generated medical reports efficient and
    straightforward?
- **Detail** : Do the reports contain comprehensive and relevant information needed for patient diagno-
    sis and treatment?
- **Compatibility** : Is the format of the medical reports compatible and easy to integrate with other
    medical software used during consultations?

#### 7.1.3 Participants

User testing was conducted with a total of five participants, all of whom were practicing physicians in Por-
tugal and had no prior exposure to the application. Each participant was provided with a formal document
containing instructions on how to access both the patient and physician applications, as well as guidelines
on creating an account in the system.
In terms of age distribution, one participant (20%) was in the 18-30 age group, while the remaining
four participants (80%) were in the 30-50 age group. Regarding gender, one participant (20%) was male,
and the remaining four (80%) were female. This distribution is illustrated inFigure 26.


##### 20%

##### 80%

##### 18-30

##### 30-50

```
(a) Age Distribution.
```
##### 20%

##### 80%

```
Male
Female
```
```
(b) Gender Distribution.
Figure 26: Distribution of participants across different age groups and genders.
```
In terms of digital competence, which participants self-assessed, three users (60%) rated their digital
competence as moderate, while the remaining two users (40%) rated it as high. This distribution is shown
inFigure 27. All participants are employed in hospitals, and as a prerequisite, all possess higher education.

##### 40%

##### 60%

```
High
Moderate
```
```
Figure 27: Distribution of participants across different digital competence groups.
```
### 7.2 Results for Each Application.

#### 7.2.1 Patient Application

**NASA Task Load Index (NASA-TLX)**

The average workload across all participants was 15.6, indicating that the workload associated with the
patient application was minimal. The best-performing indicator was Temporal Demand, averaging 8, which
suggests that participants did not feel rushed while using the system. This indicates that the pace of
interaction with the application was comfortable and manageable for most participants.
The lowest-rated indicator was Performance, with an average score of 22. This suggests that there
is room for improvement in how confident participants feel in their performance when using the system.


While the application is generally seen as low-effort and not frustrating, enhancing the system’s ability to
make participants feel more successful and confident in their tasks would be beneficial.
Overall, these NASA-TLX results highlight that the patient application creates a minimal cognitive load,
making it user-friendly. However, addressing areas related to performance confidence would help optimize
the user experience further.

Table 1: NASA-TLX results for the patient application (0–100 scale; higher values indicate greater work-
load).

```
Physician Mental Demand Temporal Demand Performance Effort Frustration Workload Score
P1 10 10 10 20 10 12
P2 20 0 20 20 10 14
P3 30 0 20 20 20 18
P4 20 10 50 20 10 22
P5 10 20 10 10 10 12
Average 18 8 22 18 12 15.6
```
**System Usability Scale (SUS)**

The best-performing indicator for the patient application was SUS10, where all participants rated it with a
1, suggesting that they did not feel the need to learn much in order to use the system. Similarly, SUS03
performed well, with most participants agreeing that the system is easy to use, reinforcing the application’s
user-friendly design.
The lowest-performing indicator was SUS01, with an average score of 4. This suggests that some par-
ticipants might not enjoy using the system frequently. However, as discussed in the limitations and future
work section, it is important to note that this application is primarily designed for patients, not physicians,
which may explain why participants (physicians) expressed lower interest in using the application regularly.
Overall, the SUS score of 86 reflects an excellent usability rating, indicating that users found the system
to be very user-friendly and easy to navigate.


Table 2: SUS results for the patient application (1–5 scale for questions; final score 0–100, higher final
score is better).

```
Question P1 P2 P3 P4 P5 Average
SUS01 5 2 5 3 5 4
SUS02 1 2 1 2 1 1.4
SUS03 4 5 5 4 5 4.6
SUS04 1 2 1 2 1 1.4
SUS05 5 4 4 4 5 4.4
SUS06 1 1 2 2 1 1.4
SUS07 3 5 4 4 4 4
SUS08 1 2 2 2 1 1.6
SUS09 5 4 5 3 4 4.2
SUS10 1 1 1 1 1 1
SUS 92.5 80.0 90.0 72.5 95.0 86.0
```
**Questionnaire for User Interaction Satisfaction (QUIS)**

The best-performing indicator for the patient application was Ease of Learning, Visual Layout, Interface
Consistency, Clarity of Messages, General Functionality, and Accessibility, all averaging 8.4. These results
suggest that participants found the application intuitive, visually appealing, and consistent in its design and
messaging, allowing them to easily understand and use the features without confusion. This consistency
across several key dimensions reflects a strong overall user experience.
On the other hand, the worst-performing indicator was Response Time, with an average score of 7.2.
While this still represents a relatively positive score, it suggests that participants occasionally encoun-
tered delays that detracted from their overall experience. Improving the speed and responsiveness of the
application could further enhance user satisfaction.
Overall, the average QUIS score of 8.1 reflects a high level of user satisfaction with the patient applica-
tion, indicating that most physicians were pleased with its usability and functionality. While there are areas
for improvement, particularly in response time, the system is largely considered effective and user-friendly.


```
Table 3: QUIS results for the patient application (1–9 scale; higher values indicate greater satisfaction).
```
```
Question P1 P2 P3 P4 P5 Average
Ease of Learning 9 8 9 7 9 8.4
Response Time 7 8 9 3 9 7.2
Navigation 8 9 9 3 9 7.6
Visual Layout 9 9 9 6 9 8.4
Interface Consistency 9 9 9 6 9 8.4
Clarity of Messages 9 8 9 7 9 8.4
General Functionality 9 8 9 7 9 8.4
Accessibility 9 8 9 7 9 8.4
Error Recovery 5 8 9 6 9 7.4
QUIS Score 8.2 8.3 9 5.8 9 8.1
```
**Additional Feedback**

The additional feedback from the participants regarding the patient application provided valuable insights
into its performance across several key indicators. The annoyance factor, which measured whether the
number of questions asked by the application was irritating, received an average score of 2. This relatively
low score indicates that participants generally did not find the application’s questioning process to be overly
annoying or burdensome, with most feeling that the number of questions was acceptable.
Intermsofhowappropriatethequestionswereinaddressingmedicalneeds, theapplicationperformed
well, with an average score of 4.4. This suggests that participants largely agreed that the questions were
relevant and effective in addressing patient needs, making the system a helpful tool in facilitating the
anamnesis process.
The relevance of the questions, measured by how many participants felt the questions were not aligned
with their medical needs, received the lowest average score of 1.4. A lower score here is positive, as it
indicates that most participants found the questions to be highly relevant and appropriate for the context.


```
Table 4: Additional feedback results for the patient application (1-5 scale).
```
```
Physician Irritation Effectiveness Relevance
P1 1 5 1
P2 3 4 1
P3 1 4 2
P4 4 4 2
P5 1 5 1
Average 2 4.4 1.4
```
#### 7.2.2 Physician Application.

**NASA Task Load Index (NASA-TLX)**

The best-performing indicator for the physician application was Effort, with an average score of 18. This
suggests that participants generally found it relatively easy to complete tasks with the application, requiring
minimal effort to perform effectively.
The worst-performing indicators were Mental Demand and Performance, both averaging 34. A high
score in Mental Demand indicates that the application required significant cognitive effort from the physi-
cians, suggesting that interacting with the system may have been mentally taxing. Similarly, a higher
Performance score reflects lower perceived success in accomplishing the tasks, meaning physicians were
not fully confident in the outcomes they achieved with the system.
Overall, the average Workload Score of 26 reflects a low to moderate workload for the physicians when
usingtheapplication. Whiletheapplicationperformedwellintermsofeffort, thereisroomforimprovement
in reducing mental demand and increasing user confidence in their performance when using the system.


Table 5: NASA-TLX results for the physician application (0–100 scale; higher values indicate greater work-
load).

```
Physician Mental Demand Temporal Demand Performance Effort Frustration Workload Score
P1 30 10 20 10 10 16
P2 20 10 10 10 10 12
P3 80 10 30 30 30 36
P4 30 20 100 30 60 48
P5 10 50 10 10 10 18
Average 34 20 34 18 24 26
```
**System Usability Scale (SUS)**

Thephysicianapplicationreceivedstrongoverallfeedback, withseveralquestionstiedforthebest-performing
indicators. SUS01, SUS02, SUS06, SUS09, and SUS10 all performed exceptionally well, indicating that
physicians found the system easy to use, not overly complex, and effective at reducing frustration. These
scores reflect a general consensus that the system is intuitive and user-friendly, requiring minimal effort
to navigate and accomplish tasks.
The lowest-performing indicator was SUS04, with an average score of 1.8. While still relatively positive,
this suggests that there is some room for improvement in simplifying certain aspects of the system, as
some users may have found it slightly more complex than ideal.
Overall, the SUS score averaged 88.5, which indicates an excellent level of usability. The system was
well-received by physicians, who found it efficient and easy to use with minimal complexity or frustration,
though there are minor areas that could benefit from further refinement.


Table 6: SUS results for the physician application (1–5 scale for questions; final score 0–100, higher final
score is better).

```
Question P1 P2 P3 P4 P5 Average
SUS01 5 4 5 4 5 4.6
SUS02 1 1 1 2 1 1.2
SUS03 5 4 4 4 5 4.4
SUS04 1 1 4 2 1 1.8
SUS05 5 4 5 4 5 4.6
SUS06 1 2 1 2 1 1.4
SUS07 4 5 5 4 5 4.6
SUS08 2 1 1 2 1 1.4
SUS09 4 5 4 3 5 4.2
SUS10 1 1 1 2 1 1.2
SUS 92.5 90 87.5 72.5 100 88.5
```
**Questionnaire for User Interaction Satisfaction (QUIS)**

The physician application received consistently high scores across multiple dimensions in the QUIS survey.
The best-performing indicators were Ease of Learning and General Functionality, both averaging 8.6. These
scores indicate that physicians found the system intuitive and easy to learn, with its functionality effectively
supporting their tasks. This reflects positively on the application’s design and user experience, making it
accessible and efficient for its intended users.
The lowest-performing indicator was Response Time, with an average of 8. While still a strong score,
it suggests that there may be some room for improvement in optimizing the application’s responsiveness,
as a few users may have noticed occasional delays.
Overall, the QUIS score averaged 8.3, reflecting a high level of satisfaction among physicians. This
indicates that the application was generally well-received, offering a user-friendly experience with solid
functionality and consistency. Although theresultssuggest some minor areas forimprovement, particularly
in response time, the overall experience was very positive for the majority of users.


Table 7: QUIS results for the physician application (1–9 scale; higher values indicate greater satisfaction).

```
Question P1 P2 P3 P4 P5 Average
Ease of Learning 9 9 9 7 9 8.6
Response Time 7 9 9 6 9 8.0
Navigation 9 9 9 6 9 8.4
Visual Layout 9 9 7 7 9 8.2
Interface Consistency 9 8 9 7 9 8.4
Clarity of Messages 9 9 8 6 9 8.2
General Functionality 9 9 8 8 9 8.6
Accessibility 9 9 8 6 9 8.2
Error Recovery 9 9 8 6 9 8.2
QUIS Score 8.8 8.9 8.3 6.6 9 8.3
```
**Additional Feedback**

The additional feedback from the physicians regarding the application was highly positive across all eval-
uated indicators. The efficiency of the process for reviewing and using the generated medical reports
scored an average of 4.6. This suggests that the majority of physicians found the system efficient and
straightforward, enabling them to quickly access and utilize the reports without any significant obstacles
or delays.
In terms of relevance, the reports were also rated highly, with an average score of 4.6. This indicates
that the information provided in the reports was considered comprehensive and relevant for supporting
patient diagnosis and treatment, aligning well with the physicians’ needs during consultations.
The formatting of the medical reports received the highest average score of 4.8, reflecting that the
format was compatible and easy to integrate with other medical software used during consultations. Physi-
cians found the reports well-organized and seamless to work with, enhancing their workflow without intro-
ducing compatibility issues.


```
Table 8: Additional feedback results for the physician application (1-5 scale, higher is better).
```
```
Physician Efficiency Detail Compatibility
P1 5 5 5
P2 5 5 5
P3 4 4 4
P4 4 4 5
P5 5 5 5
Average 4.6 4.6 4.8
```
### 7.3 Discussion of Results

#### 7.3.1 Patient Application

TheresultsoftheNASATaskLoadIndex(NASA-TLX)suggestthatthepatientapplicationimposesaminimal
cognitive load, with an average workload score of 15.6. The Temporal Demand was the best-performing
indicator, averaging 8, indicating that users did not feel rushed and found the interaction pace manageable.
However, the Performance score, which averaged 22, highlights an area for improvement—users did not
feel fully confident in their task performance. Despite this, the overall results point to a user-friendly
experience with room for improvement in boosting user confidence through more intuitive feedback or
guidance mechanisms.
TheSystemUsabilityScale(SUS)scoreof86reinforcesthepositivereceptionofthepatientapplication,
withparticipantsagreeingthatthesystemwaseasytouse, particularlyevidentinthehighscoresforSUS03
(ease of use) and SUS10 (low need for additional learning). The lowest score, SUS01 (average 4), suggests
that users, who were physicians rather than the intended patient audience, may not see the application
as something they would use frequently. This underscores the importance of including actual patients in
future tests for more representative feedback.
The Questionnaire for User Interaction Satisfaction (QUIS) results, with an average score of 8.1, indi-
cate high user satisfaction, particularly in areas such as Ease of Learning and Visual Layout, both averaging
8.4. However, the Response Time was rated lower, at 7.2, signaling that some users experienced delays.
Optimizing the system’s responsiveness would likely elevate the overall user experience. Additional feed-
back shows that the questions posed by the system were appropriate, with a low Irritation score (2) and a


high Effectiveness score (4.4), indicating the system’s relevance in addressing medical needs.
Overall, the patient application demonstrates a user-friendly design and high usability, but improve-
ments can be made in the area of user confidence and system responsiveness. Addressing these aspects
through better feedback mechanisms and performance optimization could further enhance the applica-
tion’s effectiveness and make it even more suitable for patient use.

#### 7.3.2 Physician Application.

The results for the NASA Task Load Index (NASA-TLX) for the physician application show an average
workload score of 26, indicating a low to moderate cognitive load. The Effort score was the best-performing
indicator, averaging 18, suggesting that physicians found the system relatively easy to use. However, both
MentalDemandandPerformancewereratedsignificantlyhigher, eachaveraging34. Theseresultssuggest
that the system was mentally taxing for users and that they lacked confidence in their task performance.
To reduce cognitive load and improve performance perception, simplifying workflows and offering more
robust feedback could be beneficial.
The System Usability Scale (SUS) score of 88.5 reflects the physician application’s strong usability.
Physicians found the system intuitive, with high scores for SUS01, SUS02, and SUS10, showing that the
system was easy to learn and navigate. The lowest score, SUS04 (1.8), suggests that certain features
might still feel overly complex to some users, pointing to areas where simplification of the interface could
improve the experience.
The Questionnaire for User Interaction Satisfaction (QUIS) results, with an overall score of 8.3, confirm
high satisfaction, especially in Ease of Learning and General Functionality, both averaging 8.6. However,
similar to the patient application, Response Time was rated lower, at 8, suggesting occasional delays that
could be improved. The additional feedback provided highlights the system’s efficiency and compatibility,
with high scores for the Efficiency (4.6), Detail (4.6), and Compatibility (4.8) of medical reports, suggesting
that physicians found the report generation process highly functional and easy to integrate with existing
software.
While the physician application shows excellent usability and functionality, the mental demand and
performance-related concerns highlight the need for a more streamlined and supportive experience. Fo-
cusing on reducing complexity and improving the speed of interactions will help create a more efficient
and satisfying tool for physicians, ultimately improving the workflow during medical consultations.


### 7.4 Limitations and Future Work.

Evaluating the system presents significant complexities. While datasets featuring patient-doctor dialogues
and corresponding medical notes are available, using them for assessment is challenging due to the
disparity in output distributions. The system’s output structure differs from those in the datasets, making
it difficult to directly compare outputs. Unlike traditional fine-tuning, the aim here is not to replicate the
dataset’s distribution but to ensure the system delivers information of similar quality. This challenge is
compounded by the reliance on a closed-source model.
Given these difficulties, the system was assessed based on perceived utility, with both patients and
physicians providing feedback on its effectiveness. The results demonstrate the system’s value in automat-
ing and improving anamnesis, but there are several limitations that should be addressed.
One of the key limitations of this study is the relatively small participant pool, with only five physicians
testing the applications. While their insights have been valuable, this sample size may not be sufficiently
representative of the broader medical community. Larger-scale studies would be beneficial to gather a
more comprehensive range of feedback and increase the reliability of the findings. Additionally, while it
is important for physicians to test the patient application to assess the appropriateness of the questions,
future iterations of the study should include non-physicians in the participant pool to better simulate real
patient experiences. This would help ensure the questions are not only clinically appropriate but also clear
and comprehensible to patients.
Another significant limitation is the absence of an appropriate dataset related to anamnesis. Without
such a dataset, it is difficult to quantify how closely the system’s anamnesis mimics a real-world medical
interview or how well the generated reports align with those a physician would create. Future work could
leverage the development of such datasets and employ reconstruction metrics to evaluate how accurately
the system can recreate medical reports. This would enable a more robust qualitative analysis of the
model’s outputs, improving the system’s validity.
Latency in the patient application has also emerged as a key area for improvement, particularly in
hands-free mode. The delay caused by processing user responses, generating a model output, converting
that to audio, and then sending the response back to the user creates an inefficient experience. Optimizing
these steps would greatly enhance the system’s usability and could mitigate some of the negative feedback
regarding response delays.
Finally, the physician application could benefit from a more flexible approach to generating medical
reports. The current format, which uses bullet points to organize atomic pieces of information, may not be


ideal for all physicians. Some participants found this format intuitive, while others struggled with it. Future
work should explore the possibility of a more adaptable report structure that accommodates different
note-taking styles, ensuring it remains user-friendly for a wider range of medical professionals.


### Chapter 8

**Conclusion**

This dissertation explored the development and evaluation of AI-driven applications designed to enhance
the medical anamnesis process through the integration of Large Language Models (LLMs). The research
hypothesis, which proposed that integrating LLMs into the anamnesis process would significantly improve
the accuracy and efficiency of patient medical history collection compared to traditional methods, has
been verified through the findings of this study. Both the patient and physician applications demonstrated
notable potential in streamlining medical interviews and improving the quality of information gathered,
thereby supporting healthcare professionals in making faster, more informed decisions.
The patient application exhibited strong usability, with participants reporting low cognitive load and
minimal frustration. The clear and accessible interface made it easy for users to navigate, although
some improvements are needed to boost user confidence and enhance system responsiveness. These
enhancements would further contribute to the hypothesized increase in efficiency, as the system already
shows promise in reducing the time and effort required for accurate patient history collection.
The physician application also performed well, particularly in its integration with existing medical work-
flows and the ease of reviewing generated medical reports. Physicians found the system intuitive and
efficient, supporting the hypothesis that LLMs can facilitate a more streamlined process. However, the
application did place a significant cognitive demand on users, suggesting that further simplification of the
interface and improved real-time feedback would help to further optimize performance and reduce mental
strain.
Overall, the results confirmed the hypothesis by demonstrating that the integration of LLMs improved
both the accuracy and efficiency of the anamnesis process, particularly in terms of data collection and
the structuring of medical reports. The advanced contextual understanding capabilities of LLMs enabled
more precise and relevant questioning, which is a key factor in improving the quality of patient data.
Limitations of the study included the small participant group and the need for a more diverse user
base, particularly for the patient application. Additionally, the lack of a large-scale anamnesis dataset


limited the ability to test the system across a broader range of medical conditions. Technical challenges,
such as delays in the patient application’s hands-free mode, also need to be addressed to ensure the
system performs optimally in real-world settings.
Future work should prioritize expanding the scope of testing by including a more diverse set of par-
ticipants, particularly non-physician users, to ensure that the applications are robust across various de-
mographics. Addressing latency issues in the patient application, especially in hands-free mode, will be
critical to enhancing real-world usability. Additionally, refining the user interfaces of both applications to re-
duce cognitive load and improve user experience will further optimize performance. Adaptive question sets
tailored to individual patient responses and enhancements in the speed and format of medical reports are
also essential areas for development. These improvements will help maximize the system’s effectiveness
in clinical practice, making AI-driven anamnesis systems not only more efficient but also more accurate
and user-friendly.
Moreover, a key direction for future research involves the creation and utilization of large-scale, diverse
anamnesis datasets. Such datasets would enable more rigorous validation of the system’s performance
across a broader range of medical conditions and patient profiles. This would also provide the opportunity
to fine-tune the LLMs for specific medical domains, further increasing their relevance and accuracy.
In conclusion, this this Master’s project confirms that the integration of LLMs into the anamnesis
process can significantly improve both the accuracy and efficiency of patient medical history collection,
fulfilling the initial research hypothesis. While the results are promising, continuous improvements and
broader testing will be critical to ensuring that these systems deliver substantial real-world value in clinical
environments.
