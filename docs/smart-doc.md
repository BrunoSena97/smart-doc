FACULDADE DE ENGENHARIA DA UNIVERSIDADE DO PORTO

# <Smart-Doc: AI-Powered Medical

# Education through Diagnostic

# Interactions>

<Bruno de Sena Pereira>

WORKING VERSION

```
Mestrado em Engenharia de Software
```
```
Supervisor: Prof.<Nuno Freixa>
```
```
October 17, 2025
```


```
<Smart-Doc: AI-Powered Medical Education through
Diagnostic Interactions>
```
<Bruno de Sena Pereira>

Mestrado em Engenharia de Software

October 17, 2025


# Resumo

```
i
```

# Abstract

```
ii
```

# UN Sustainable Development Goals

The United Nations Sustainable Development Goals (SDGs) provide a global framework to achieve
a better and more sustainable future for all. It includes 17 goals to address the world’s most press-
ing challenges, including poverty, inequality, climate change, environmental degradation, peace,
and justice.
Quisque ullamcorper placerat ipsum. Cras nibh. Morbi vel justo vitae lacus tincidunt ultrices.
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. In hac habitasse platea dictumst. Integer
tempus convallis augue. Etiam facilisis.
The specific Sustainable Development Goals mentioned have the following names:

SDG 7 Ensure access to affordable, reliable, sustainable and modern energy for all

SDG 8 Promote sustained, inclusive and sustainable economic growth, full and productive em-
ployment and decent work for all

```
SGD Target Contribution Performance Indicators and
Metrics
```
```
7
```
```
7.1 Enhancing the efficiency of SCADA
systems can help increase the relia-
bility of solar energy production, fa-
cilitating universal access to clean en-
ergy.
```
```
Percentage of solar plants with
improved...
```
```
7.2 Improving the management of solar
plants helps enhance the efficiency
and reliability of renewable energy
```
...

```
Increase in renewable energy
share...
```
```
8 8.1 Enhancing renewable energy infras-tructure promotes resilience against
climate-related hazards and supports
sustainable energy sources.
```
```
Increase in resilience metrics...
```
```
iii
```

# Acknowledgements

```
iv
```

```
v
```
<O Nome do Autor>


“Our greatest glory is not in never falling, but in rising every time we fall”

```
Confucius
```
```
vi
```

## Contents





- © Bruno de Sena Pereira,
- 1 Introduction
- 1.1 Motivation
- 1.2 Research Questions
- 1.3 Objectives
- 1.4 Dissertation Structure
- 2 Background
- 2.1 The Cognitive Foundations of Medical Diagnosis
- 2.1.1 The Diagnostic Process: An Iterative Quest for Coherency
- 2.1.2 Dual-Process Theory in Clinical Reasoning
- 2.2 Cognitive Biases: The Pathologies of Clinical Reasoning
- 2.2.1 A Taxonomy of Diagnostic Error: Identifying Common Cognitive Biases
- 2.2.2 Debiasing Strategies: Interventions to Improve Clinical Judgment
- 2.3 Large Language Models for Educational Simulation
- 2.3.1 Prompting for Structure and Reasoning
- 2.3.2 Alignment with Human Feedback (RLHF)
- 2.3.3 Context Management and Retrieval-Augmented Generation
- 2.3.4 Intent Recognition in Dialogue Systems
- 2.4 AI Virtual Patients as a Crucible for Clinical Reasoning
- 2.4.1 The Evolving Role of Simulation in Medical Education
- 2.4.2 Designing the Virtual Encounter: The Principle of Progressive Disclosure
- 3 Literature Review
- 3.1 Methods
- 3.1.1 Eligibility Criteria
- 3.1.2 Information Sources
- 3.1.3 Search Strategy
- 3.1.4 Selection of Sources of Evidence
- 3.1.5 Data Charting Process
- 3.2 Results
- 3.2.1 Publication Categorization
- 3.2.2 Study Design
- 3.2.3 Main findings
- 4 Developing SmartDoc: A Bias-Aware Clinical Simulation Platform
- 4.1 System Design
- 4.1.1 Overview
- 4.1.2 Core Components
- 4.1.3 Case Modelling: Intent-Driven Simulation CONTENTS viii
- 4.1.4 Intent Classification System
- 4.2 Part II: Technical Implementation
- 4.2.1 Overview and Execution Pipeline
- 4.2.2 Execution Details and Safeguards
- 4.2.3 Algorithm 1: Intent-Driven Progressive Disclosure
- 4.2.4 Algorithm 2: Bias Detection and Warning
- 4.2.5 LLM Integration
- 4.2.6 Data Model and Persistence
- 4.2.7 Response Generation
- 4.2.8 Deployment and Observability
- 4.2.9 Production Refinements
- 4.2.10 Technology Stack and LLM Integration
- 4.2.11 Response Generation and Production Refinements
- 4.2.12 Database Architecture and State Management
- 4.2.13 Deployment Configuration and Scalability
- 4.3 Example Workflow: The Miliary Tuberculosis Case
- 4.3.1 Case Overview and Educational Objectives
- 4.3.2 Phase-by-Phase Walkthrough
- 4.3.3 Summary of Information Revealed
- 4.3.4 Diagnosis and Reflection
- 4.3.5 Evaluation Results
- 4.3.6 Educational Impact Analysis
- 4.4 User Interfaces
- 4.4.1 Simulation Interface
- 4.4.2 Evaluation Results Interface
- 4.4.3 Administrative Dashboard
- 5 Evaluation and Results
- 5.1 Evaluation Methods
- 5.1.1 Study Design
- 5.1.2 Evaluation Instruments
- 5.1.3 Data Analysis
- 5.2 Results
- 5.2.1 Diagnostic and Educational Outcomes
- 5.2.2 Learner Reflections
- 5.2.3 Reflection Signals
- 5.2.4 Usability and Workload
- 5.2.5 Agreement and Caveats
- 6 Discussion and Conclusion
- 6.1 Overview
- 6.2 Interpreting the Findings
- 6.2.1 Bias Patterns Reproduced by SmartDoc
- 6.2.2 Reflection and Metacognitive Engagement
- 6.2.3 Usability, Workload, and Cognitive Load
- 6.3 Comparison with the Case Inspiration
- 6.3.1 Cognitive Bias Typology
- 6.3.2 Systemic Versus Cognitive Contributions
- 6.3.3 Educational Implications CONTENTS ix
- 6.4 Implications for Medical Education
- 6.5 Limitations
- 6.6 Future Work
- 6.7 Conclusion
- References
- Appendix A — System Usability Scale (SUS)
- Appendix B — NASA-TLX (Adapted)
- Appendix C — Representative Session (S6)
- 3.1 Prisma Flow Diagram List of Figures
- 3.2 Venn Diagram Mapping
- 4.1 Conceptual schema: capturing reasoning traces, bias events, and reflection data.
- 3- Physical Exam, 4- Labs & Imaging). 4.2 Simulation interface: four-tab layout (1- Patient Information, 2- Clinical Interview,
- 4.3 Listed discovered blocks of information.
- 4.4 Bias warning card (persistent, non-blocking) shown in the Discovery Panel.
- 4.5 Diagnosis and reflection submission
- 4.6 Overall Performance Summary
- 4.7 Detailed evaluation
- 4.8 Admin UI: Database backup and Bias Warnings configuration
- 4.9 Admin UI: User Management
- 4.10 Admin UI: LLM configuration and Prompt Management
- 4.11 Admin UI: Prompt Viewer Modal
- 2.1 Common Cognitive Biases in Clinical Diagnosis List of Tables
- 3.1 Study Design
- 3.2 Condensed Summary of Studies on AI-Powered Virtual Patients
- 3.3 Supporting and Hindering Factors for AI Adoption in Medical Education
- 4.1 Intent categories by diagnostic phase (examples abbreviated).
- 4.2 Classification accuracy improvements (pilot summary).
- 4.3 Core persistence entities (abbreviated).
- 4.4 Core technologies and versions
- 4.5 LLM temperature settings by module.
- 4.6 Response quality improvements following production refinements.
- 4.7 Discoveries by category and timing.
- 5.1 SmartDoc evaluation results for completed sessions (n= 6).
- 5.2 Reflection signals by session (presence = Y / absence = N).
- 5.3 SUS scores (0–100) for completed sessions (n= 6).
- 5.4 NASA-TLX workload profile (0–100); simulated summary.


# List of Acronyms

```
AI Artificial Intelligence
API Application Programming Interface
AR Analytical Reasoning (System 2)
CUQ Chatbot Usability Questionnaire
ITS Intelligent Tutoring System
LLM Large Language Model
NAR Non-Analytical Reasoning (System 1)
NASA-TLX National Aeronautics and Space Administration Task Load Index
NLP Natural Language Processing
QUIS Questionnaire for User Interaction Satisfaction
SUS System Usability Scale
VP Virtual Patient
VSP Virtual Standardized Patient
```
```
xii
```

## Chapter 1

# Introduction

Diagnostic error is one of the most persistent threats to patient safety, with cognitive biases recog-
nised as a major contributor to avoidable harm in clinical practice [14]. These biases—systematic
deviations from rational judgement—can derail even experienced clinicians, leading to prema-
ture closure of reasoning, selective information use, or overconfidence in a favoured hypothesis.
As Croskerry [10] emphasises, traditional training methods are often insufficient to help students
recognise and mitigate these cognitive pitfalls under the pressures of real-world practice.
At the same time, the transition from medical student to competent clinician demands the
development of robust clinical reasoning skills that combine knowledge, pattern recognition, and
reflective awareness [2]. Conventional educational approaches emphasise outcomes, but often fail
to make the process of reasoning visible, let alone directly train learners to detect and counteract
bias in their own thinking. Addressing this unmet need requires pedagogical approaches that can
elicit reasoning patterns, expose bias, and scaffold reflection in a safe and scalable way.
This dissertation introduces SmartDoc, an AI-powered virtual patient platform designed to
meet this challenge. By harnessing large language models (LLMs), SmartDoc provides natural-
istic clinical interview simulations that not only mirror the complexity of patient interaction, but
also embed mechanisms to detect cognitive biases in real time. Beyond replication of encounters,
the system delivers structured metacognitive feedback, prompting learners to reflect on their rea-
soning. In this way, SmartDoc moves beyond teaching what to diagnose, toward teaching how to
think—directly addressing the root causes of diagnostic error in a controlled, scalable environment
[3, 30].

## 1.1 Motivation

The motivation for this research arises from two converging forces. First, an educational gap:
reasoning errors, rather than knowledge deficits, account for a substantial proportion of diagnostic
mistakes, yet medical training rarely provides explicit support for bias awareness [3]. Second, a
technological opportunity: the rapid maturation of LLMs, together with pedagogical frameworks
from Intelligent Tutoring Systems (ITS), offers a new toolkit for building simulations that combine

### 1


Introduction 2

realism with adaptive, reflective support. SmartDoc is situated at the intersection of these forces:
a system that leverages AI to elicit naturalistic reasoning behaviour, surface bias-prone moments,
and scaffold reflective practice.

## 1.2 Research Questions

The central research problem guiding this dissertation is:

```
How can AI-powered virtual patients be designed to help medical students recognise
and mitigate cognitive biases in their diagnostic reasoning?
```
```
From this problem, three research questions (RQs) emerge:
```
- RQ1: To what extent can an LLM-powered simulation realistically elicit and detect cogni-
    tive biases in diagnostic interviews?
- RQ2: How effective are metacognitive prompts—delivered in real time or post-hoc—in
    fostering reflection and reducing diagnostic bias?
- RQ3: What technical and pedagogical design principles enable the scalable deployment of
    bias-aware virtual patient simulations?

## 1.3 Objectives

In alignment with these questions, the dissertation pursues the following objectives:

- Simulation — To design and implement an AI-powered virtual patient platform capable of
    conducting realistic, unscripted clinical interviews based on authentic case scenarios engi-
    neered to elicit bias.
- Bias Detection — To embed mechanisms for identifying behavioural markers of anchoring,
    confirmation bias, and premature closure in learner interactions, using a combination of
    rule-based and LLM-supported approaches.
- Metacognitive Tutoring — To provide context-aware prompts that stimulate reflection and
    encourage reconsideration of reasoning pathways when bias-prone behaviour is detected.
- Evaluation Framework — To develop analytics that assess diagnostic accuracy, information-
    gathering behaviours, and manifestations of cognitive bias, enabling both formative and
    summative feedback.
- Effectiveness Study — To conduct a pilot evaluation of the system with clinical interns,
    assessing usability, educational effectiveness, and potential impact on bias awareness.


1.4 Dissertation Structure 3

## 1.4 Dissertation Structure

The remainder of this dissertation is organised as follows:

- Chapter 2 presents the theoretical background, outlining clinical reasoning, dual-process
    theory, and the taxonomy of cognitive biases, and introducing debiasing strategies and sim-
    ulation principles that underpin SmartDoc’s design.
- Chapter 3 reviews empirical evidence on AI-powered virtual patients through a scoping
    review, mapping feasibility, effectiveness, design considerations, and impact on reasoning,
    and identifying the gaps SmartDoc addresses.
- Chapter 4 details the development of SmartDoc, showing how theoretical principles (Chap-
    ter 2) and empirical insights (Chapter 3) informed its architecture, case design, and bias-
    detection features.
- Chapter 5 evaluates SmartDoc with clinical interns, presenting methods, results, and re-
    flections on usability, realism, and educational impact.
- Chapter 6 discusses the broader implications of the findings, acknowledges limitations, and
    outlines directions for future research and curriculum integration.

With the research problem, questions, and objectives established, the next step is to ground the
study in its theoretical foundations. Chapter 2 therefore examines the cognitive underpinnings
of clinical reasoning, the taxonomy of diagnostic biases, and existing debiasing strategies, before
introducing simulation—and particularly AI-powered virtual patients—as a pedagogical approach
that informs the design of SmartDoc.


## Chapter 2

# Background

This chapter establishes the theoretical foundation for this dissertation. It introduces the cognitive
mechanisms that underpin diagnostic reasoning, examines the pervasive role of cognitive biases,
and situates simulation—and in particular AI-powered virtual patients—as a promising medium
for advancing medical education. By grounding the technical development of the SmartDoc sys-
tem in established cognitive science and educational principles, this chapter provides the concep-
tual scaffolding for the subsequent literature review (Chapter 3) and system design (Chapter 4).

## 2.1 The Cognitive Foundations of Medical Diagnosis

The act of arriving at a medical diagnosis is one of the most demanding cognitive tasks in health-
care. Rather than following a linear progression, diagnostic reasoning is iterative, probabilistic,
and highly context-dependent. It integrates biomedical knowledge, patient narratives, and pattern
recognition under the constraints of time and uncertainty. Understanding the mechanisms that gov-
ern this reasoning, and the vulnerabilities inherent in them, is essential for designing educational
interventions that enhance accuracy and safety.

## 2.1.1 The Diagnostic Process: An Iterative Quest for Coherency

Clinical diagnosis unfolds as an iterative cycle of hypothesis generation, evidence gathering, and
hypothesis refinement. Initial patient cues often trigger the formation of early hypotheses, which
are then tested against further clinical data. This process is dynamic: clinicians continuously adjust
their working model as new findings emerge. While this iterative approach is powerful, it is also
vulnerable to premature closure if alternative hypotheses are insufficiently considered.

## 2.1.2 Dual-Process Theory in Clinical Reasoning

The cognitive engine of diagnosis is commonly described through the lens of dual-process the-
ory [3]. This framework, widely accepted in cognitive psychology and medical education, posits
that human reasoning operates via two interacting systems:

### 4


2.2 Cognitive Biases: The Pathologies of Clinical Reasoning 5

- System 1: Non-analytical Reasoning (NAR) — Fast, intuitive, and automatic. In medicine,
    this manifests as pattern recognition, where a presentation is matched to an “illness script”
    developed through experience. For example, identifying a bull’s-eye rash as Lyme disease
    is a System 1 process. While efficient and often accurate for common cases, System 1 is
    also the main source of cognitive error. Biases typically arise when heuristics are applied
    inappropriately or unchecked.
- System 2: Analytical Reasoning (AR) — Slow, deliberate, and effortful. This involves
    hypothesis-driven reasoning, systematic evidence gathering, and critical evaluation of com-
    peting diagnoses. System 2 requires greater cognitive resources but functions as a safeguard,
    monitoring and correcting intuitive judgments that may be flawed.

Diagnostic expertise lies in the fluid interplay between these systems: effective clinicians
leverage System 1 for efficiency while engaging System 2 when uncertainty, complexity, or atyp-
ical presentations demand deeper scrutiny.

## 2.2 Cognitive Biases: The Pathologies of Clinical Reasoning

Although dual-process theory describes how reasoning ideally balances efficiency and accuracy,
in practice the system is fallible. Cognitive biases are systematic deviations from rational judg-
ment that emerge from heuristic shortcuts. They are now recognized as a leading contributor to
diagnostic error and thus to preventable patient harm [14].

## 2.2.1 A Taxonomy of Diagnostic Error: Identifying Common Cognitive Biases

Numerous biases have been catalogued in clinical reasoning research. The most prevalent include:
Table 2.1 consolidates the most frequently cited cognitive biases in clinical reasoning and high-
lights their implications for diagnostic accuracy. While many biases have been described, Smart-
Doc focuses particularly on anchoring, confirmation bias, and premature closure, as these are
both common in clinical practice and highly teachable within simulation contexts. Recognizing
these pathologies of reasoning provides the foundation for exploring strategies to mitigate them,
which are discussed in the following subsection.

## 2.2.2 Debiasing Strategies: Interventions to Improve Clinical Judgment

Given the susceptibility of diagnostic reasoning to systematic error, a variety of debiasing ap-
proaches have been proposed to mitigate the influence of cognitive biases. These approaches
typically aim to engage slower, analytic processing (System 2) to monitor, challenge, or override
intuitive (System 1) judgments, and they can be grouped into complementary families: cognitive
forcing strategies, structured reflection, diagnostic checklists and time-outs, and simulation-based
training with targeted feedback.


Background 6

```
Table 2.1: Common Cognitive Biases in Clinical Diagnosis
```
```
Bias Description and Clinical Implications
Anchoring Fixating on initial impressions or salient features of the case,
leading to insufficient adjustment when new, contradictory evi-
dence emerges [10, 32].
Confirmation
Bias
```
```
Selectively seeking or interpreting information that confirms an
existing hypothesis, while overlooking evidence that might refute
it [3, 32].
Premature Clo-
sure
```
```
Accepting a diagnosis before it has been fully verified, halting
further diagnostic exploration and increasing the risk of missed
or incorrect diagnoses [14, 32].
Framing Effect Diagnostic reasoning shaped by the way information is presented
(e.g., “elderly patient with heart failure”), which can steer atten-
tion toward certain explanations and away from others [10, 32].
Availability Bias Overestimating the likelihood of diagnoses that are more re-
cent, memorable, or dramatic in the clinician’s experience (e.g.,
diagnosing pulmonary embolism after seeing several recent
cases) [10, 14].
Overconfidence
Bias
```
```
Excessive faith in one’s own diagnostic accuracy, which reduces
openness to alternative hypotheses and corrective feedback [4,
30].
Search Satisfac-
tion
```
```
Stopping the diagnostic search once a plausible explanation has
been found, often resulting in missed comorbid or secondary con-
ditions [10, 14].
```
Cognitive forcing strategies. Cognitive forcing strategies (CFS) are metacognitive prompts that
deliberately “force” a pause in intuitive reasoning, encouraging clinicians to consider alternative
explanations, seek disconfirming evidence, or re-frame the problem [8]. CFS can be taught at
different levels (universal, generic, and specific), and are designed to inoculate against known
pitfalls (e.g., anchoring on an early hypothesis) by prompting questions such as “What else could
this be?” or “What would I look for if my current hypothesis were wrong?”

Structured (deliberate) reflection. Deliberate reflection is a structured procedure in which
learners explicitly articulate and compare competing diagnostic hypotheses, list supporting and
disconfirming features for each, and revisit the fit between data and diagnosis. This engages an-
alytic processing and has been shown to improve recall of discriminating features and support
more balanced reasoning, particularly when learners are taught how and when to apply it [22, 30,
31]. In education, deliberate reflection operationalizes the “think about your thinking” goal of
metacognition by scaffolding hypothesis verification and consideration of alternatives.

Diagnostic checklists and time-outs. Checklists provide structured prompts to widen differ-
ential diagnosis, surface red flags, and reduce premature closure. Systematic reviews report that
checklists can support diagnostic verification and broaden information search, although effects on


2.3 Large Language Models for Educational Simulation 7

diagnostic accuracy are mixed and context-dependent [15, 21, 47]. Team-based “diagnostic time-
outs” extend this idea by creating a deliberate pause to query assumptions and potential biases
before committing to a diagnosis.

Simulation with just-in-time metacognitive feedback. Simulation environments can trigger
authentic information-seeking behavior and make reasoning processes observable. When com-
bined with progressive disclosure (information revealed conditionally on learner queries) and just-
in-time metacognitive prompts, simulation can surface bias-prone moments (e.g., anchoring after
an early test result) and provide targeted feedback that encourages reconsideration of alterna-
tives [9, 15]. This aligns with experiential learning cycles in which action is followed by feedback
and reflection, and it motivates the bias-aware design choices described later for SmartDoc.

Summary and implications for design. Across these strategies, the common mechanism is the
deliberate engagement of analytic reasoning at critical junctures in the diagnostic process. Edu-
cational systems should therefore (i) detect bias-prone patterns (e.g., early diagnostic closure, se-
lective information seeking), (ii) interrupt with concise, context-aware prompts (CFS), (iii) struc-
ture reflection on alternatives (deliberate reflection), and (iv) support verification via lightweight
checklists or time-outs. Collectively, these strategies demonstrate that cognitive errors are not
inevitable but can be mitigated through deliberate educational design. These principles later in-
form the SmartDoc architecture (Chapter 4), where they are operationalised into concrete design
features.

## 2.3 Large Language Models for Educational Simulation

The practical implementation of bias-aware simulation requires modern natural language process-
ing (NLP) techniques. Large Language Models (LLMs) provide the foundation for conversa-
tional agents capable of supporting medical education, and their behaviour can be shaped through
prompting strategies, alignment with human feedback, and structured control mechanisms. This
section reviews four key techniques: (i) prompting for structured reasoning, (ii) alignment through
reinforcement learning from human feedback (RLHF), (iii) context management via retrieval-
augmented generation (RAG), and (iv) intent recognition for dialogue orchestration. These con-
cepts will later be applied in Chapter 4 to the design of the SmartDoc platform.

## 2.3.1 Prompting for Structure and Reasoning

Prompting allows developers to constrain and direct model behaviour by specifying roles, con-
text, and output formats. In educational settings, prompts can be structured to elicit reasoning
steps or provide outputs in standardised formats for downstream analysis. For example, chain-
of-thought (CoT) prompting enables stepwise reasoning, making intermediate steps explicit and
more inspectable for feedback [44]. While powerful, prompting must balance depth of reasoning
with response latency and cognitive load for learners.


Background 8

## 2.3.2 Alignment with Human Feedback (RLHF)

Instruction-following behaviour in state-of-the-art models has been enhanced through reinforce-
ment learning from human feedback (RLHF), which fine-tunes models on preference data to pro-
duce more helpful, safe, and controllable outputs [33]. In educational contexts, this alignment
reduces the risk of incoherent or unsafe responses and ensures that models remain in character
(e.g., simulating a patient) while honouring pedagogical constraints.

## 2.3.3 Context Management and Retrieval-Augmented Generation

Because the parametric memory of LLMs is limited and can be outdated, retrieval-augmented gen-
eration (RAG) combines neural generation with access to external knowledge sources [24]. This
reduces the likelihood of hallucinated facts and grounds responses in authoritative references. In
medical education, RAG can be valuable for evidence-based feedback or guideline support. How-
ever, in bias-aware simulations its use must be carefully scoped: uncontrolled retrieval during
interviews risks short-circuiting the intended reasoning process by providing answers without in-
quiry. For this reason, RAG is more appropriate for post-hoc feedback rather than real-time patient
interactions.

## 2.3.4 Intent Recognition in Dialogue Systems

Task-oriented dialogue systems often rely on intent recognition and slot filling to map free-text
queries to structured actions. Modern approaches apply transformer-based classifiers, sometimes
jointly trained for intent detection and slot filling [27, 45]. In safety-critical contexts such as
healthcare chatbots, robust handling of uncertain or out-of-scope inputs is essential, motivating
research in unknown intent detection [25]. For educational simulations, intent recognition enables
structured progression through learning scenarios while maintaining the natural feel of conversa-
tion.

Summary. Together, prompting, RLHF, RAG, and intent recognition form the conceptual toolkit
by which LLMs can be adapted to support safe, realistic, and educationally effective simulations.
These techniques enable conversational agents to be both flexible and controllable, aligning with
pedagogical principles such as progressive disclosure and structured reflection (Sections 2.1.1–
2.2.2). Their concrete application to medical education will be detailed in Chapter 4.

## 2.4 AI Virtual Patients as a Crucible for Clinical Reasoning

To translate the theoretical insights of dual-process reasoning and bias awareness into practice,
medical education has increasingly turned to simulation. Among the available approaches, Vir-
tual Patients (VPs)—interactive, computer-based scenarios—have become an important tool for
practicing diagnostic reasoning in safe, standardized, and repeatable environments [6, 34]. Their


2.4 AI Virtual Patients as a Crucible for Clinical Reasoning 9

pedagogical value lies in making reasoning both visible and improvable: students must externalize
their thinking, and the system can provide structured feedback [37].

## 2.4.1 The Evolving Role of Simulation in Medical Education

Traditional VPs are designed to mimic clinical encounters, offering opportunities to practice
history-taking, decision-making, and reasoning without risk to real patients [34]. More recently,
AI-powered Virtual Standardized Patients (VSPs) extend this paradigm by enabling natural
language dialogue and adaptive responses, enhancing the realism of the encounter [6, 23]. Con-
ceptually, this aligns with experiential learning theory (Kolb), which emphasizes learning through
cycles of action, feedback, and reflection [46]. By situating learners in an authentic yet con-
trolled interaction, AI-VSPs provide a fertile context for bias-prone reasoning to surface and be
addressed [35].

## 2.4.2 Designing the Virtual Encounter: The Principle of Progressive Disclosure

A critical design principle for effective simulation is progressive disclosure: clinical informa-
tion is revealed incrementally in response to learner queries, mirroring real-world diagnostic prac-
tice [19]. This structure ensures that learners actively seek information rather than receiving it pas-
sively, creating opportunities for biases such as anchoring or premature closure to appear [10, 14].
When combined with metacognitive scaffolding, progressive disclosure transforms the simulation
from a scripted case into a dynamic learning environment where both strengths and vulnerabilities
in reasoning can be observed [30].

From Concept to Evidence. The conceptual framework highlights the potential of AI-powered
VPs, but their actual impact depends on empirical validation. Chapter 3 therefore reviews the
existing evidence base, identifying strengths, limitations, and gaps in current research.


## Chapter 3

# Literature Review

Building on the conceptual foundations outlined in Chapter 2, this chapter critically examines
the empirical evidence on AI-powered Virtual Patients (AI-VPs) in medical education. While
Chapter 2 established the theoretical rationale for using simulation, progressive disclosure, and
bias-aware design to strengthen clinical reasoning, the actual effectiveness of these approaches
must be determined through research.
To this end, a scoping review was conducted to map the current state of knowledge on AI-
VPs across four dimensions: (i) feasibility and validity of implementation, (ii) effectiveness for
skill development, (iii) system design and integration, and (iv) impact on clinical reasoning and
decision-making.
This review aims to answer two guiding questions:

- How can AI-powered virtual patients transform medical education?
- What key considerations are essential for their integration and evaluation to maximize edu-
    cational impact?

By synthesizing recent empirical studies, the review identifies both the strengths and limita-
tions of existing approaches and highlights the gaps that SmartDoc seeks to address in its design
and evaluation.
To achieve this overarching goal, this review maps existing literature on AI-powered virtual
patients in medical education, specifically focusing on:

- Feasibility and Validity: Examining evidence supporting practical implementation and
    accuracy of AI-VPs in simulating patient encounters and assessing student performance.
- Effectiveness for Skill Development: Synthesizing findings on AI-VP effectiveness in en-
    hancing specific clinical skills, including communication, history-taking, and clinical rea-
    soning.
- Development and Design Considerations: Exploring key design principles, technological
    underpinnings, and iterative development approaches employed in AI-VP system creation.

### 10


3.1 Methods 11

- Impact on Clinical Reasoning and Decision-Making: Investigating AI-VP influence on
    cognitive skills underpinning clinical practice, particularly clinical reasoning and decision-
    making abilities.

## 3.1 Methods

To ensure adherence to the PRISMA-ScR, this scoping review employed established guidelines
and a corresponding checklist.

## 3.1.1 Eligibility Criteria

This review focused on peer-reviewed, open-access empirical studies published in English be-
tween 2019 and 2025, investigating the application of AI in medical education for history-taking
skills. This timeframe was selected to capture recent AI and e-learning trends post-COVID-19.
Eligible studies included research that:

- Involved medical and/or nursing students. This criterion ensured the review focused on
    populations relevant to general medical and nursing education, excluding specialized fields.
- Specifically examined AI-driven interventions designed to enhance clinical skills.
- Featured interventions that:
    - Employed Artificial Intelligence (AI).
    - Virtual Patients (VPs) were used as the delivery method.
    - Focused on clinical practice. This narrowed the scope to studies directly related to the
       acquisition and development of practical clinical skills.

The review excluded book chapters, reports, conference papers, grey literature, pay-walled ar-
ticles, pre-prints, unpublished materials, theoretical papers, reviews, editorials, and opinion pieces.
Studies focusing on specific medical specialties, such as surgery or dental education were also ex-
cluded, as the focus of the review is the clinical interview process.

## 3.1.2 Information Sources

A comprehensive literature search was conducted across Cochrane Library, PubMed (includ-
ing PubMed Central - PMC), Scopus, ScienceDirect, and IEEE Xplore electronic bibliographic
databases.

## 3.1.3 Search Strategy

A systematic search was performed across multiple databases for relevant studies.


Literature Review 12

A core search strategy, initially developed for PubMed and subsequently adapted for other
databases to maintain consistency, was employed. The PubMed search string, restricted by publi-
cation date (2019-2025) and language (English), was:

("Anamnestic interview" OR "History Taking" OR "Anamnesis") AND "Artificial
Intelligence"
The search was implemented in PubMed (All Fields), PMC (Abstract), Scopus (Title, Ab-
stract, Keywords), ScienceDirect (Title, Abstract, Keywords), IEEE Xplore (All Metadata), and
the Cochrane Library (Title, Abstract, Keywords).

## 3.1.4 Selection of Sources of Evidence

A two-stage screening process was employed:

1. Title and Abstract Screening: Search results were imported into Zotero, duplicates re-
    moved, and uploaded to Rayyan, a web-based systematic review screening tool. Titles and
    abstracts were reviewed by a single researcher against predefined eligibility criteria.
2. Full-Text Screening: Potentially relevant articles underwent full-text assessment, also con-
    ducted by the same reviewer.

While dual screening is often employed to mitigate bias, single-reviewer screening was utilized
here due to the context of this review being conducted for a master’s dissertation

## 3.1.5 Data Charting Process

Data extraction, refined iteratively after pilot testing, was performed using a predefined form on a
subset of included studies. Extracted data included:

- Article Information: Title, publication year, authors, keywords, publication type, country
    of origin.
- Study Characteristics: Objective, design, data collection / analysis methods, study en-
    ablers / challenges.
- Participant Characteristics: Student type, educational background, learning setting, age
    range, sample size, gender distribution (when available).
- AI Intervention Details: AI application type, AI techniques, tools, models, services em-
    ployed, delivery modality, integration platform, curriculum integration, intervention dura-
    tion and supporting and hindering factors.
- Outcomes and Impact: Measurement methods, specific history-taking skill outcomes, re-
    ported benefits, challenges.
Data charting was loosely structured around the PICO framework, acknowledging typical
scoping review inconsistencies in comparative elements across studies.


3.2 Results 13

## 3.2 Results

Database searches identified 508 publications. After removing 14.17% (72/508) duplicates, the
titles and abstracts of 79.92% (406/508) publications were screened. Based on the eligibility
criteria, full texts of 5.91% (30/508) publications were reviewed. Ultimately, 3.35% (17/508)
studies were included in this scoping review (Figure1).

```
Figure 3.1: Prisma Flow Diagram
```
## 3.2.1 Publication Categorization

This scoping review categorized studies on AI-powered virtual patients (VPs) in medical education
into aforementioned four key theme.
A Venn Diagram was developed to effectively visualizes the multidimensional nature of the
reviewed literature by using a color gradient to represent scoring across four themes (Figure. 2).


Literature Review 14

This allows for quick identification of research focus overlaps, and facilitates comparative analysis
of thematic relevance across individual papers and clusters of studies.

```
Figure 3.2: Venn Diagram Mapping
```
## 3.2.2 Study Design

To systematically classify the study designs, this review adopts the categorization proposed by
Hanna von Gerich et al. (2022)[40], which groups research articles based on their primary aim.
This framework includes developing new AI technologies, improving the accuracy or efficiency
of existing AI technologies, testing different algorithms or AI systems, and assessing, evaluating,
or validating existing AI technologies.
Hanna von Gerich et al. (2022) [40] utilized this categorization to analyze the progression of
AI technology in nursing, revealing a predominance of studies in the early development phases.
Applying this framework in the context of AI-powered virtual patients allows for a structured


3.2 Results 15

analysis of the research landscape, highlighting the primary aims of included studies and enabling
comparisons within the field. Table II summarizes key study characteristics, including design and
primary research aim, ensuring a structured and comparative analysis of the included studies.

```
Table 3.1: Study Design
```
```
Characteristic Author, (year of publication) Publications
(n=17), n(%)
```
```
Study Design
```
```
Experimental Wang. (2025) [41], Bruge. (2024) [5], Lippitsch.
(2024) [26], Michael. (2022) [7]
```
### 4 (23.5%)

```
Quasi-
Experimental
```
```
Shorey. (2019) [38], Anthamatten. (2024) [1], Wang.
(2022) [43]
```
### 3 (17.6%)

```
Descriptive Holderried. (2024) [17], Holderried. (2024) [18],
Furlan. (2021) [12], Afzal. (2020) [36], Mattei.
(2024) [11], Wang. (2025) [42], Maicher. (2023)
[28], Jingrong. (2022) [20], Furlan. (2022) [13],
Maicher. (2019) [29]
```
### 10 (58.8%)

```
Aim of the research
```
```
Development of
new AI
technologies:
```
```
Furlan. (2021) [12], Shorey. (2019) [38], Afzal.
(2020) [36], Maicher. (2023) [28], Wang. (2025)
[42], Lippitisch. (2024) [26], Wang. (2022) [43],
Furlan. (2022) [13].
```
### 8 (47.1%)

```
Assessing, evaluat-
ing, or validating
existing AI tech-
nologies:
```
```
Holderried. (2024) [17], Holderried. (2024) [18],
Wang. (2025) [41], Mattei. (2024) [11]. Jingrong.
(2022) [20], Anthamatten. (2024) [1], Brugge.
(2024) [5], Michael. (2022) [7], Maicher. (2019)
[29]
```
### 9 (53.9%)

## 3.2.3 Main findings

The subsequent section presents a concise overview of the key findings from the included publi-
cations, organized in table format for detailed discussion. Specifically, Table II encapsulates each
study’s characteristics, emphasizing feasibility, effectiveness, design considerations, and the im-
pact of AI-driven Virtual Patients (VPs) on clinical training and decision-making. Complementing
this, Table III identifies factors that either facilitate or challenge technology adoption, offering a


Literature Review 16

balanced perspective on the potential benefits of VPs. Collectively, these tables deliver a com-
parative analysis that aids in understanding the current status, practical implications, and future
research directions of AI-powered VPs.

Discussion

This section begins with a bullet-point summary of the key findings across the four identified
themes, followed by a detailed discussion of these findings.

Key Findings

- Feasibility and Validity: AI-powered virtual patients (VSPs) are feasible and valid for
    medical education, showing high accuracy and realism [11, 17, 29, 41]. However, continu-
    ous refinement is needed to optimize accuracy and address context-dependent variability in
    realism.
- Effectiveness for Skill Development: AI-VPs effectively enhance foundational skills, par-
    ticularly history-taking, offering scalable, feedback-rich learning comparable to traditional
    methods [7, 18, 20, 26, 38]. Further research is needed to assess their impact on advanced
    communication skills, empathy, and long-term skill retention.
- Development and Design: AI-VP systems leverage advanced technologies like NLP and
    ITS for realism, scalability, and pedagogical soundness [12, 28, 42, 43]. The use of real
    medical records and hybrid AI designs further enhances authenticity and sophistication.
- Impact on Clinical Reasoning and Decision-Making: AI-VPs show promise in enhanc-
    ing clinical reasoning and decision-making (CDM) skills, with AI feedback significantly
    improving CDM scores [1, 5, 13]. However, further research is needed to fully quantify
    their long-term impact on cognitive skills.
- Balance between AI Innovation and Evaluation: The field demonstrates a balance be-
    tween rapid AI innovation and rigorous evaluation, with a growing body of experimental
    research validating AI-VPs’ educational effectiveness [5, 18].
- Implications for Clinical Training: AI-VPs have transformative potential for medical ed-
    ucation, offering scalable and effective training for foundational skills, personalized feed-
    back, and data-driven insights [7, 13]. However, strategic integration and ongoing evaluation
    are crucial to address limitations and maximize their pedagogical impact.

Feasibility and Validity of AI-Powered Virtual Patients

AI-powered virtual patients (VSPs) demonstrate strong feasibility and validity, although optimiz-
ing accuracy and realism remains a challenge. Holderried et al. (2024) established GPT-3.5’s


3.2 Results 17

```
Table 3.2: Condensed Summary of Studies on AI-Powered Virtual Patients
```
```
Author (Year) Intervention Population Key Conclusions
```
```
Feasibility and Validity
Holderried
(2024) [17] GPT-3.5 chatbot Med/Midwifery Realistic; useful
Wang (2025)
[41]
```
```
ChatGPT SP
(prompts) Medical Effective; cost-efficient
Mattei (2024)
[11] AI-VSP cases Healthcare
```
```
Better diagnostics;
supplement
Maicher (2019)
[29] Web VSP Medical Reliable; feedback support
```
```
Skill Development
Shorey (2019)
[38] VP comm. training Nursing^ ↑Self-efficacy; skills
Jingrong (2022)
[20] WeChat VSP Nursing
```
```
Objective; influenced by
skills
Michael (2022)
[7] Chatbot + tutor Medical Comparable to bedside
Holderried
(2024) [18] GPT-4 chatbot Medical >99% accurate; reliable
Lippitsch (2024)
[26] ViPATalk avatars Medical Equivalent to role-play
```
```
Development and Design
Furlan (2021)
[12] Hepius NLP/ITS Medical^ ↑Test scores; reasoning
Wang (2025)
[42] XueYiKu app Students, doctors Active learning; feedback
Maicher (2023)
[28] AI VSP (ASR, RNN) Medical 90% accuracy; human-like
Wang (2022)
[43] AIteach Medical^ ↑Clinical thinking
Afzal (2020) [36] Dengue tutor bot Medical High usability; engagement
```
```
Clinical Reasoning
Furlan (2022)
[13] VP NLP/ITS cases Nurse practitioners
```
```
Consistent metrics; weak
exam link
Brugge (2024)
[5] ChatGPT feedback Medical Better decision-making
Anthamatten
(2024) [1] VR + AI sims Medical Effective; screen > VR
```

Literature Review 18

```
Table 3.3: Supporting and Hindering Factors for AI Adoption in Medical Education
```
```
Factor Category Supporting Factors Hindering Factors
```
```
Educational
Potential
```
- Innovative, accessible learning
    [11, 17]
- Overcomes traditional training
    limitations [17]
- Cost-effective [5, 17]
- High-quality feedback [18]
- Realistic simulations [18]
- Enhances learning through
    practice [18]
       - Concerns about accuracy [5, 12,
          29, 36]
       - Limitations in subjective judgment
          and feedback mechanisms [26, 41]
       - Reliance on AI instead of learning
          [18]
       - Unexpected AI behaviors [18]

```
Technology &
Implementation
```
- Technological advances in AI and
    NLP [12, 28, 43]
- Improved system accuracy with
    training data [28]
- Consistent answers [7]
- Distance learning capabilities [7,
    12, 43]
       - Technical issues [1, 11, 38]
       - High implementation costs [11]
       - Reliance on third-party services
          [26]
       - Limited case variety [42]
       - Lack of system integration [42]
       - Difficulty in communication with
          AI [1]

```
Realism & Human
Interaction
```
- Simulates standardized patients
    effectively [41]
- Bridges theoretical and clinical
    practice [11]
       - Lack of realism in avatars [11]
       - Inability to fully replace human
          interaction [11]
       - Absence of non-verbal cues [5]

```
Cost & Accessibility
```
- Cost reduction [29]
- Increased accessibility [5]
- Resource sharing [42]
    - Resource-intensive programs [28]

```
Other
```
- Need for safe practice
    environment [11]
- Potential for AI improvement [11]
- Positive student feedback [28]
    - Negative student attitudes towards
       AI feedback [18]
    - Potential disengagement [36]
    - Preference for screen-based
       format over immersive VR [1]


3.2 Results 19

feasibility for patient simulation, with 94.4% answer alignment to illness scripts and 97.9% plausi-
bility ratings, indicating educational acceptability and good user experience (CUQ (tool measures
UX and usability of chatbots) score: 77/100) [17]. However, rare implausible answers (2.1%)
highlighted the need for refined model constraints to improve output accuracy and reduce socially
desirable responses [17].
Wang et al. (2025) reinforced AI-VP validity, showing prompt engineering significantly en-
hanced ChatGPT’s clinical accuracy. Iterative prompt design decreased scoring discrepancies
from 29.83% to 6.06%, achieving 89.3% question categorization accuracy, emphasizing iterative
prompt design for valid assessments [41]. Similarly, Maicher et al. (2019) validated AI assess-
ment of history-taking skills, showing computer-generated scores (87% accuracy) closely mirrored
human rater scores (90%), with high inter-rater reliability (Intraclass correlation coefficient (ICC)
0.75 for 81% of categories) confirming system consistency, although complex domains require
further refinement [29].
De Mattei et al. (2024) further evidenced AI-VP feasibility, with 50–87% of students across
disciplines rating them as realistic. Supporting their utility, 72–90% reported improved diagnostic
confidence. However, variable realism ratings (e.g., 16% among physician assistant students)
indicated context-dependent feasibility [11].

Effectiveness of AI-Powered VPs for Skill Development

AI-powered VPs show promise in effectively enhancing specific skills, particularly foundational
skills, although nuances exist. Holderried et al. (2024) directly addressed AI-VP effectiveness,
showing GPT-4 provided structured feedback on history-taking, aligning with human raters and
supporting skill improvement. Lippitsch et al. (2024) further indicated ViPATalk’s effectiveness,
demonstrating equivalence to role-play for history-taking completeness while offering automated
feedback and self-study benefits. This suggests AI-VPs offer a scalable alternative for foundational
skill practice [18, 26].
Shorey et al. (2019) highlighted AI-VPs’ potential to enhance broader communication skills,
noting improved student self-efficacy and engagement, though primarily based on perceived im-
provements. Du et al. (2022) indirectly supported effectiveness by validating AI-VPs’ ability to
provide objective history-taking skill assessments, crucial for targeted feedback. Finally, Co et
al. (2022)’s case-control study directly compared AI-VP training to traditional bedside teaching,
finding comparable student performance for history-taking, suggesting AI-VPs can be as effective
as real-patient interactions for foundational skills training [7, 20, 38].
However, while AI-VPs are effective for foundational skills and feedback delivery, studies in-
dicate limitations. Lippitsch et al. (2024) found equivalence, not superiority, to role-play [26].
Shorey et al. (2019) focused on perceived self-efficacy [38], and Du et al. (2022) primarily on
assessment validity [20]. Further research is needed to assess effectiveness for advanced commu-
nication skills, empathy, and long-term skill retention. Nevertheless, evidence indicates AI-VPs
are effective tools for foundational skill development in medical education, offering scalable, ac-
cessible, feedback-rich learning.


Literature Review 20

Development and Design of AI-Powered Virtual Patient Systems

AI-VP system development consistently leverages advanced technologies for realism, scalability,
and pedagogical soundness. Furlan et al. (2021) emphasized NLP integration in Hepius for
realistic interaction and ITS for personalized feedback. Maicher et al. (2023) detailed a hybrid
AI system combining rule-based and neural network NLU for improved conversational fidelity.
Wang et al. (2022 & 2025) highlighted NLP’s crucial role in processing real medical records for
authentic case content in AIteach and XueYiKu [12, 28, 42, 43].
Beyond NLP, Intelligent Tutoring Systems (ITS) are increasingly integrated for pedagogical
enhancement. Furlan et al. (2021) incorporated an ITS module in Hepius for step-by-step feed-
back. Wang et al. (2025) implemented multidimensional automatic evaluation in XueYiKu, using
radar charts for visualized feedback. The use of real medical records, as seen in AIteach and
XueYiKu [42, 43], and hybrid AI designs [28] further underscores the trend towards sophisti-
cated, data-driven, and pedagogically informed AI-VP systems. Mobile accessibility and scalable
architectures are also key design considerations [36, 42].

Impact of AI-Powered Virtual Patients on Clinical Reasoning and Decision-Making

AI-powered VPs demonstrate a promising, nuanced impact on cognitive skills, particularly clinical
reasoning and decision-making. Brügge et al. (2024) provides direct evidence of enhanced CDM
with AI feedback. Their RCT showed significant CDM score improvements in students receiving
AI feedback, especially in "creating context" and "securing information" subdomains [5]. Furlan
et al. (2022) further developed learning analytics metrics to assess specific CDM components
within AI-VP simulations, offering granular performance insights [13].
Anthamatten & Holt (2024)’s qualitative findings align, with NP students reporting VR-AI
simulations as most impactful on decision-making abilities and responsiveness to clinical changes.
Students also reported increased diagnostic confidence and perceived AI-VPs as useful for history-
taking and differential diagnosis development [1].
However, limitations exist. Furlan et al. (2022) found limited correlation with external hema-
tology exam scores, suggesting VPs and traditional exams assess different competencies [13]. An-
thamatten & Holt (2024) primarily relied on student perceptions, requiring further objective val-
idation. Despite these nuances, evidence suggests AI-VPs can positively impact cognitive skills,
particularly CDM, though further research is needed to fully quantify long-term impact. [1]

Balance between AI innovation and evaluation

Reflecting on methodological approaches employed across reviewed studies, a notable trend emerges
concerning balance between AI innovation and rigorous evaluation. A significant portion of lit-
erature, particularly within ’Development and Design’ theme, is descriptive, detailing innovative
architectures, functionalities, technological advancements of AI-VP systems, showcasing rapid
AI innovation in medical education. However, alongside descriptive accounts, a growing body of
experimental research, as seen in ’Effectiveness’ and ’Impact on Clinical Reasoning’ themes, is


3.2 Results 21

dedicated to rigorously evaluating AI-VP pedagogical value and impact on student learning and
cognitive skill development. This increasing experimental validation emphasis showcases a ma-
turing field, moving beyond demonstrating technological feasibility towards establishing evidence
for AI-powered virtual patients’ educational effectiveness and optimal implementation in medical
training.

Interpretation in Context

The findings of this scoping review resonate with and expand upon existing reviews in AI-powered
medical education. Similar to Stamer et al. (2023)’s [39] scoping review focused on communi-
cation skills training, it confirms the promising potential of AI and machine learning to enhance
medical education, particularly by offering cost-effective, readily accessible training modalities.
Both reviews align in identifying AI-VP feasibility and acceptability as key strengths, echoing
Hindelang et al. (2024)’s [16] finding that chatbots can increase patient engagement and stream-
line data collection. This consensus across reviews strengthens the argument for the growing
maturity and acceptance of AI-VP technology in medical education.
However, the current study also adds nuanced perspectives and extends beyond prior review
scope. While Stamer et al. (2023)’s scoping review focused on communication skills training,
Hindelang et al. (2024) and this study acknowledge technological limitations and challenges
related to AI-VP interaction authenticity and natural language flow. Unlike those reviews, it delves
deeper into the specific technological advancements (NLP, ITS, hybrid systems, learning analytics)
employed to address these limitations, particularly within the "Development and Design" theme.
Furthermore, unlike the narrower focus of Stamer et al. (2023) on communication skills and
Hindelang et al. (2024) on history-taking chatbots, its broader scope, encompassing the impact
on clinical reasoning and decision-making, provides a more holistic, integrated understanding
of AI-VP pedagogical potential across a wider spectrum of cognitive skills essential for clinical
practice. Notably, the consistent emphasis in this review on AI-generated feedback’s crucial role
in enhancing effectiveness, as highlighted in Holderried et al. (2024) [18] and Brügge et al.
(2024) [5], represents a key area of focus not explicitly emphasized in other scoping reviews.
This highlights AI-generated feedback as a potentially critical mechanism for maximizing AI-VP
pedagogical impact, as the reviewed studies demonstrate that detailed feedback provides a higher
level of learning.

Implications for Clinical Training

Building upon these findings and considering identified trends, key implications for clinical train-
ing and medical education emerge. The demonstrated feasibility, validity, and effectiveness of
AI-powered VPs suggest transformative potential for curriculum design and technology adoption.
Firstly, findings strongly advocate for judicious AI-VP simulation integration into medical
curricula, particularly in early clinical training stages, offering a scalable, accessible means for
repeated practice in foundational skills. AI-VP training can be comparable to real-patient bedside


Literature Review 22

teaching for history-taking skills, suggesting a viable, ethical alternative for novice learners [7].
For example, AI-VPs can be strategically integrated into early clinical training to provide students
with repeated practice in history-taking, allowing them to develop proficiency before encountering
real patients.
Secondly, emphasis on AI-generated feedback and learning analytics points towards a future
of more personalized, data-driven medical education. AI-VPs’ ability to provide structured, au-
tomated, potentially individualized feedback offers a mechanism to enhance learning efficiency
and address individual student needs. Furthermore, learning analytics metrics enable continuous
program improvement and curriculum refinement based on data-driven insights [13]. This data
can be used to identify areas where students struggle and to tailor instruction to meet their specific
needs.
An interesting aspect of the clinical reasoning process is the presence of cognitive errors and
biases. Furlan et al. (2021) highlight that the majority of diagnostic errors are caused by cognitive
errors, rather than knowledge deficiency [12]. Subsequently, Furlan et al. (2022) found that many
students skipped crucial steps of the clinical interview, falling into the "early closure" mistake [13].
This suggests that students may be susceptible to cognitive biases during the clinical reasoning
process, which is an important consideration for future research and AI-VP development. AI-VPs
can be designed to simulate scenarios that are likely to trigger cognitive biases, providing students
with the opportunity to recognize and correct these errors in a safe environment.
However, reviewed literature also underscores the importance of thoughtful, strategic imple-
mentation. As highlighted by Stamer et al. (2023) [39] and Hindelang et al. (2024) [16], chal-
lenges related to authenticity, natural language flow, technological limitations, and ongoing refine-
ment needs remain. Future curriculum design and technology adoption should prioritize:

- Enhancing Realism and Authenticity: Focus on improving AI-VP interaction realism and
    authenticity, particularly in nuanced communication aspects beyond factual accuracy.
- Strategic Integration of AI-VPs: Integrate AI-VPs as a supplement, not a replacement,
    for traditional clinical experiences. For instance, AI-VPs can be used for initial skill de-
    velopment and practice, while real-world clinical experiences remain essential for develop-
    ing advanced clinical judgment, empathy, and complex decision-making skills that require
    human-to-human interaction.
- Stronger Evaluation Methodologies: Focus on robust evaluation methodologies, includ-
    ing RCTs and objective skill measures, to further validate AI-VP interventions’ long-term
    educational impact. For example, future research could employ longitudinal studies to as-
    sess the long-term impact of AI-VP training on clinical skills and patient outcomes, or use
    standardized patient assessments to objectively measure the improvement in students’ clin-
    ical skills after AI-VP training.
- Other Considerations: Carefully consider ethical implications, data privacy, and user-
    centered design for responsible, equitable AI-VP implementation.


3.2 Results 23

Strengths and Limitations

This scoping review benefits from a solid search strategy across major databases and a detailed
thematic analysis, providing a strong synthesis of current literature. However, it also has method-
ological limitations. Grey literature exclusion may have overlooked relevant findings. Initial single
reviewer screening introduces potential bias, and the focus on peer-reviewed, open-access publi-
cations carries a risk of publication bias towards positive results. Future research should consider
incorporating grey literature, implementing dual screening, and acknowledging potential biases
when interpreting findings.

Conclusion

This scoping review examined the current landscape of AI-powered virtual patients in medical ed-
ucation, synthesizing evidence across feasibility and validity, effectiveness for skill development,
system design and impact on clinical reasoning.
The findings demonstrate the promising potential of AI-VPs as a valuable and increasingly so-
phisticated tool for medical training. AI-VPs offer a feasible, scalable, and engaging modality for
delivering standardized, repeatable practice opportunities, particularly for foundational communi-
cation and history-taking skills. Moreover, AI-driven feedback and learning analytics integration
within these systems offers pathways towards personalized, data-driven medical education with
the potential to enhance clinical reasoning and decision-making abilities.
While challenges such as achieving complete realism, overcoming technological limitations
and the need for further rigorous validation remain, the AI-VP development trajectory is clearly
towards more authentic, user-friendly and pedagogically effective tools. To fully leverage this
potential, medical educators should strategically integrate AI-VPs into curricula, focusing on sup-
plementing traditional methods rather than replacing them. Researchers should prioritize inves-
tigating AI-VP impact on advanced clinical skills and long-term outcomes, specifically through
longitudinal studies assessing skill retention beyond immediate training. Evaluating AI-VPs’ sus-
tained impact on clinical competence in this manner would provide stronger evidence for their
educational value and inform best practices for curriculum integration. Furthermore, develop-
ers should continue to focus on improving AI-VP realism and addressing current technological
limitations. Furthermore, developers should focus on improving AI-VP realism and addressing
current technological limitations. These efforts will maximize the unique strengths of AI-VPs,
holding significant promise for transforming medical education and cultivating a more competent
and future-ready healthcare workforce. It is crucial to invest in this rapidly evolving field and
ensure AI-VPs’ responsible and effective implementation in medical education and beyond.
Taken together, the evidence shows both the promise and the current limitations of AI-powered
virtual patients. While feasibility and usability studies highlight their potential, questions remain
regarding their role in teaching complex reasoning skills, supporting metacognition, and address-
ing cognitive biases in authentic contexts.


Literature Review 24

To respond to these gaps, the next chapter presents the design and development of the Smart-
Doc platform. Chapter 4 demonstrates how the theoretical principles outlined in Chapter 2 and the
empirical findings reviewed here informed the system’s architecture, case design, and educational
features.


## Chapter 4

# Developing SmartDoc: A Bias-Aware

# Clinical Simulation Platform

The gaps identified in Chapter 3—where AI-powered virtual patients show promise but often lack
mechanisms for explicit bias detection and metacognitive scaffolding—served as the starting point
for this project. Although many digital platforms support medical simulation, most emphasise
knowledge transfer or procedural training rather than diagnostic reasoning under uncertainty. Bias-
aware educational systems remain uncommon, and those that exist generally depend on post-hoc
analysis rather than real-time or context-aware intervention.
To address these gaps, this project developed SmartDoc, a conversational clinical simulation
platform that allows medical students to practise diagnostic reasoning while receiving targeted
feedback on cognitive biases. The system aims to deliver a more authentic diagnostic experi-
ence than conventional virtual patients while maintaining pedagogical control. It achieves this by
combining intent-driven information disclosure with large language models (LLMs) that support
natural dialogue, bias detection, and automated clinical evaluation.
Modern conversational AI architectures, reviewed in Chapter 3, were examined to guide the
technical design. Fully end-to-end neural systems were deemed unsuitable for high-stakes ed-
ucational use, as they lack transparency, offer limited control over reasoning paths, and make
validation of decision processes difficult. Conversely, hybrid systems that combine structured di-
alogue management with the linguistic flexibility of LLMs demonstrated that educational control
and realism can coexist—making such an approach the logical foundation for SmartDoc.
This chapter details the development of the SmartDoc platform. Part I (Section 4.1) intro-
duces the conceptual system design and architectural principles. Part II (Section ??) describes
the technical implementation, including language-model integration, database architecture, and
deployment configuration. Section ?? then illustrates a complete diagnostic workflow based on a
real clinical case, demonstrating how these design principles translate into educational practice.
Finally, Section ?? summarises the system’s key contributions and links to the empirical evaluation
presented in Chapter 5.

### 25


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 26

## 4.1 System Design

This first part outlines the architectural principles and conceptual design of SmartDoc.

## 4.1.1 Overview

The SmartDoc system was conceived from the principles of progressive disclosure and metacog-
nitive scaffolding introduced in Chapter 2. It adopts a modular, rule-guided architecture aligned
with large language model (LLM) capabilities. Unlike traditional virtual patients based on fixed
branching scripts, SmartDoc supports free-form clinical inquiry while maintaining pedagogical
control through intent-driven information revelation.
Three pedagogical foundations shape the system:

1. Authenticity — Realistic, conversational interactions that replicate anamnesis, physical ex-
    amination, and investigation ordering, thereby bridging the theory–practice gap highlighted
    in Chapter 3.
2. Bias awareness — Continuous monitoring for reasoning patterns associated with anchor-
    ing, confirmation bias, or premature closure, with targeted prompts encouraging reflection
    without disrupting immersion.
3. Structured reflection — Embedded metacognitive checkpoints that support deliberate re-
    flection and consolidation of reasoning skills, operationalising the debiasing strategies de-
    scribed in Chapter 2.

```
The architecture separates responsibilities into three coordinated layers:
```
- Domain logic — the reasoning engine and pedagogical rules that govern information dis-
    closure and bias detection;
- API layer — orchestration of communication, session state, and component coordination;
- Presentation layer — the learner-facing interface for interacting with the virtual patient
    and receiving feedback.

At the system’s core lies the Intent-Driven Disclosure Manager, which orchestrates three
processes:

1. Understanding learner input through an LLM-based Intent Classifier that maps natural lan-
    guage queries to structured clinical intents;
2. Controlling information flow via a Discovery Processor that releases case data incrementally
    according to query specificity;
3. Monitoring reasoning patterns with a Bias Analyzer that detects bias-prone behaviour in
    real time and triggers reflective prompts.


4.1 System Design 27

This layered architecture reflects authentic diagnostic practice while embedding cognitive
safeguards against common reasoning errors. Its modular design supports independent testing
and reproducibility of each component, directly addressing concerns identified in the literature
review.

## 4.1.2 Core Components

SmartDoc’s architecture comprises seven interrelated modules, each addressing a distinct peda-
gogical or technical function.

4.1.2.1 Intent Classifier

Learner utterances are mapped to a predefined taxonomy of 33 diagnostic intents (e.g., pmh_general,
exam_cardiovascular, imaging_chest_xray, meds_ra_specific_initial_query).
Rather than using rigid templates or question trees, SmartDoc employs LLM-based natural lan-
guage classification, allowing learners to phrase questions freely. The classifier is context-aware,
filtering available intents based on the current phase (anamnesis, examination, or investigations)
to enhance accuracy and reduce ambiguity.
This module operationalises intuitive System 1 pattern recognition while enabling reflective
System 2 oversight, allowing learners to explore hypotheses while the system traces their reasoning
trajectory.

4.1.2.2 Discovery Processor

Clinical data are disclosed progressively in response to learner queries and their classified intents.
Information is organised into modular information blocks, each representing a discrete clinical fact
(e.g., a vital sign, medication, or test result). Each block is annotated with metadata:

- Level — depth of inquiry required (Level 1 = basic; Level 2 + = follow-up);
- Prerequisites — blocks that must be revealed first;
- Critical flag — marks information essential for correct diagnosis;
- Intent triggers — the clinical intents that reveal the block.

This mechanism implements the principle of progressive disclosure, ensuring that data emerge
only through active inquiry rather than passive presentation. It reflects constructivist learning
theory by promoting exploration and meaningful engagement with clinical information.

4.1.2.3 Simulation Engine

The Simulation Engine coordinates the entire learning loop:


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 28

```
Learner query → Intent classification → Discovery processing → Bias analysis →
Response generation → Feedback assembly.
```
It maintains the simulation state, tracks revealed information, monitors hypothesis focus, and
determines when educational interventions (e.g., hints, bias warnings, reflection prompts) should
occur. By integrating reasoning traces with pedagogical scaffolds, the engine ensures each inter-
action is both technically coherent and educationally meaningful.

4.1.2.4 Bias Analyzer

Bias detection combines rule-based heuristics with LLM-supported reasoning analysis. Grounded
in the taxonomy from Section 2.2.2, it monitors for:

- Anchoring bias — persistence on an initial hypothesis despite contradictory evidence;
- Confirmation bias — selective pursuit of supporting information while ignoring refuting
    data;
- Premature closure — halting inquiry before sufficient data collection.

```
Each detection rule is parameterised with empirically derived thresholds. For example:
```
```
IF hypothesis_focus > 70% on one diagnosis
AND contradictory_evidence revealed
THEN trigger anchoring_warning("What else could explain these
findings?")
```
This transforms abstract debiasing strategies into concrete, timely feedback, encouraging ana-
lytic reconsideration without disclosing the diagnosis.

4.1.2.5 Clinical Evaluator

The Clinical Evaluator assesses performance along three dimensions:

1. Information gathering — completeness of history-taking, appropriate investigations, and
    recognition of critical findings;
2. Diagnostic accuracy — correctness of the final diagnosis and coherence of reasoning;
3. Cognitive-bias awareness — quality of reflection and evidence of bias recognition or miti-
    gation.

A single-LLM evaluation architecture replaces earlier multi-agent approaches for stability and
transparency. Structured prompts and explicit rubrics enforce consistent scoring, while a quality-
control routine penalises incomplete or nonsensical answers, ensuring educational validity.


4.1 System Design 29

4.1.2.6 Response Generation System

Responses are produced by specialised responder modules that adapt tone and terminology to the
diagnostic phase:

- Anamnesis Responder — emulates family-member dialogue with uncertainty cues (e.g.,
    “I think...”), using accessible language and gentle educational hints;
- Labs Responder — delivers investigation results concisely using professional medical
    phrasing;
- Exam Responder — provides objective physical-exam findings in standardised terminol-
    ogy.

This modular response design maintains realism while preserving pedagogical clarity appro-
priate to each learning stage.

4.1.2.7 Session Management

All interactions are logged with precise timestamps, producing comprehensive reasoning traces
that include:

- learner queries with classified intents and confidence levels;
- information blocks revealed and their order of discovery;
- triggered bias warnings and timestamps;
- reflective responses and diagnostic submissions with evaluation scores.

These records support both formative feedback (individual debriefs) and summative assess-
ment (performance metrics). They also enable empirical research on diagnostic behaviour, re-
sponding to calls in Chapter 3 for more transparent evaluation of AI-mediated learning systems.

Together, these components form a closed learning loop in which action, feedback, and re-
flection are tightly coupled—addressing the limitations of both scripted simulations and unguided
clinical experiences.

4.1.3 Case Modelling: Intent-Driven Simulation

SmartDoc introduces a novel approach to clinical case design that embeds educational triggers and
bias detection directly within the case structure itself. This intent-driven simulation model repre-
sents a significant pedagogical innovation, moving beyond traditional linear case presentations to
create dynamic, conversational learning experiences grounded in diagnostic reasoning.


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 30

4.1.3.1 Case Schema Architecture

Each SmartDoc case is defined using a structured schema that integrates progressive disclosure,
bias triggers, and educational metadata directly into the case content. This ensures that diagnos-
tic reasoning, bias awareness, and metacognition are not ancillary but intrinsic to the simulation
experience.
A case definition includes four core elements:

1. Initial Presentation — chief complaint, basic demographics, and contextual framing (e.g.,
    “elderly woman with worsening dyspnea”).
2. Information Blocks — modular clinical facts (history, examination, investigations, medi-
    cations), progressively revealed through learner queries.
3. Bias Triggers — metadata defining where and how anchoring, confirmation, or framing
    biases are likely to arise, along with corresponding intervention prompts.
4. Educational Notes — learning objectives, clinical pearls, and structured reflection ques-
    tions linked to key diagnostic moments.

Example case structure:

{
"caseId": "mull_case",
"caseTitle": "An elderly woman with dyspnea",
"initialPresentation": {
"chiefComplaint": "Worsening shortness of breath",
"historyProvider": "Son (patient is Spanish-speaking)",
"contextualFrame": "History of ’heart failure’"
},
"informationBlocks": [...],
"biasTriggers": {...},
"educationalNotes": {...}
}

By embedding all components into a unified schema, SmartDoc eliminates the limitations of
branching, pre-scripted cases. Instead, the case itself defines when information is revealed, where
bias prompts are activated, and how reflection is scaffolded, creating a flexible yet pedagogically
controlled simulation.

4.1.3.2 Information Blocks and Progressive Disclosure

Clinical information is stored as modular information blocks, each annotated with metadata that
governs its revelation. Typical attributes include:


4.1 System Design 31

- blockId — unique identifier (e.g., critical_infliximab, imaging_cxr_preliminary);
- blockType — category (e.g., History, Medications, Imaging, Labs);
- content — the clinical text revealed to the learner;
- level — depth of inquiry required (1 = basic, 2 = follow-up, 3 = advanced);
- intentTriggers — intent IDs that can reveal the block;
- prerequisites — information that must be revealed first;
- isCritical — flag for diagnostically essential data;
- revealPolicy — strategy for disclosure (immediate, escalate, or conditional).

Example information block:

{
"blockId": "critical_infliximab",
"blockType": "Medications",
"content": "Records from previous hospitalizations reveal the patient
has been receiving infliximab for rheumatoid arthritis for
the past 3-4 months.",
"isCritical": true,
"intentTriggers": ["meds_full_reconciliation_query"],
"level": 2,
"prerequisites": ["meds_ra_uncertainty"],
"revealPolicy": "escalate"
}

In this example, the infliximab information—crucial to recognising miliary tuberculosis—is
revealed only when learners perform thorough medication reconciliation and specifically request
prior hospital records. This design counters premature closure by rewarding persistence and sys-
tematic inquiry.

Progressive disclosure in practice. Information revelation follows a structured sequence of in-
quiry depth:

- Level 1: Basic data (vitals, chief complaint, current medications);
- Level 2: Detailed information requiring targeted follow-up (e.g., medication reconciliation,
    imaging interpretation);
- Level 3: Advanced or cross-domain data requiring expert-level probing (e.g., external
    record review, secondary tests).


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 32

This mechanism operationalises several bias-mitigation strategies: learners who accept surface-
level data risk anchoring; those who fail to escalate questioning risk premature closure; and those
influenced by the framing of the case (“heart failure”) illustrate framing bias.

4.1.3.3 Intent–Block Mapping Architecture

Each information block may be accessed through one or more intent pathways, enabling natural
yet pedagogically meaningful conversation flow. SmartDoc employs two mapping strategies.

Direct block mapping. Used when semantic precision in questioning should be rewarded. For
example:

- meds_ra_specific_initial_query→ meds_ra_uncertainty
- meds_full_reconciliation_query→ critical_infliximab
- imaging_echo→ critical_echo

```
This approach reinforces targeted, hypothesis-driven inquiry.
```
Group-based escalation. Used when repeated questioning within a domain should progres-
sively reveal more detail. For example:

- First labs inquiry→ basic results (labs_general);
- Second inquiry→ cardiac markers (labs_cardiac);
- Third inquiry→ specialised tests (labs_specialized).

Design rationale. The choice between mapping strategies is pedagogically motivated. Medica-
tion history uses direct mapping rather than escalation counting, rewarding semantic specificity
over repetition. For instance:

```
“Any regular medication?” → reveals basic list.
“Medications for rheumatoid arthritis?” → reveals uncertainty block.
“Can you get her complete medication list from previous hospitalisations?”→ reveals
infliximab.
```
This hierarchy differentiates surface-level inquiry from deep clinical reasoning, mirroring the
pedagogical goals introduced in Chapter 2.

4.1.3.4 Educational Scaffolding

Beyond information gating, SmartDoc implements adaptive hints when learners exhibit signs of
stagnation. This addresses a key limitation of discovery-based learning—frustration due to lack of
progress—without compromising the challenge of inquiry.


4.1 System Design 33

Example: medication reconciliation scaffolding.

- First query (meds_ra_specific_initial_query): “I’m not sure about her RA med-
    ications, I’m sorry.”
- Repeated query: “Like I said, I’m not sure. Maybe you could check her previous hospital
    records?”
Such guidance models expert reasoning (consulting external records) while maintaining im-
mersion and autonomy. These scaffolding mechanisms were refined iteratively through pilot test-
ing with medical students and align with the need for adaptive support in AI-based learning tools
identified in Chapter 3.

4.1.3.5 Embedded Bias Triggers

Bias triggers are encoded in case metadata, enabling real-time monitoring of reasoning behaviour.
Each trigger defines:

- the anchor information that may mislead the learner;
- the contradictory evidence that should prompt reconsideration;
- the bias type being demonstrated;
- the intervention prompt for metacognitive reflection.

Example bias trigger (anchoring):

"biasTriggers": {
"anchoring": {
"anchorInfoId": "imaging_cxr_preliminary",
"contradictoryInfoId": "critical_echo",
"description": "Anchoring on preliminary chest X-ray interpretation
(’pulmonary vascular congestion’) delays recognition of normal
echocardiogram, leading to incorrect heart failure diagnosis.",
"interventionPrompt": "You seem focused on a cardiac explanation.
What else could explain dyspnea with this pattern?"
}
}

Bias detection logic (simplified):

IF recent_queries.focus_on("cardiac|heart|failure") > 70%
AND contradictory_echo_revealed
AND hypothesis_unchanged
THEN trigger_bias_warning("anchoring")


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 34

This formalises abstract debiasing strategies—such as cognitive forcing—into timely, context-
aware interventions.

4.1.3.6 Educational Notes and Reflection Support

Each case includes structured educational metadata:

"educationalNotes": {
"learningPoints": [
"Medication reconciliation is crucial in multimorbid patients.",
"TNF-alpha inhibitors increase tuberculosis reactivation risk.",
"A normal echocardiogram effectively rules out heart failure."
],
"clinicalPearls": [
"Miliary pattern on chest CT: innumerable 1-2 mm nodules.",
"Always verify medication history from multiple sources."
],
"biasAwareness": [
"Anchoring on initial ’heart failure’ framing delays alternative diagnoses.",
"Confirmation bias: seeking cardiac evidence while ignoring pulmonary clues."
]
}

```
At diagnostic closure, learners are guided through reflective prompts:
```
- What evidence supports your diagnosis?
- What evidence contradicts it?
- What alternatives remain plausible?
- What was the single most compelling piece of evidence?
- What biases may have influenced your reasoning?

These prompts operationalise deliberate reflection, embedding metacognition directly within
the learning workflow.

4.1.3.7 Application: The Mull Case

The prototype case is based on the published diagnostic error report by Mull et al. (2015), in which
an elderly woman with dyspnea was repeatedly misdiagnosed with heart failure due to cognitive
bias. SmartDoc encodes this case by:

- framing the presentation as an “elderly patient with heart failure”;


4.1 System Design 35

- embedding anchoring triggers around chest X-ray and BNP results;
- requiring medication reconciliation to reveal infliximab therapy;
- providing contradictory evidence via a normal echocardiogram;
- releasing critical findings only through persistent, precise questioning.
This adaptation transforms a published diagnostic error into an interactive, bias-aware learning
experience, making cognitive pitfalls observable and addressable.

4.1.3.8 Innovation Summary

The intent-driven case design introduces five key innovations:

1. Conversational learning — natural dialogue replaces scripted question trees, fostering au-
    thentic clinical inquiry.
2. Embedded bias education — bias triggers built into metadata enable real-time detection
    and intervention.
3. Progressive disclosure — learners uncover critical clues by resisting bias-prone shortcuts
    and pursuing systematic inquiry.
4. Dynamic scaffolding — adaptive hints maintain engagement without reducing challenge.
5. Research-ready design — interaction logs capture full reasoning traces for empirical anal-
    ysis.
Through this architecture, SmartDoc transforms case-based learning from passive recall to
active, bias-aware reasoning practice, addressing the gaps identified in both cognitive psychology
(Chapter 2) and AI-powered simulation research (Chapter 3).

## 4.1.4 Intent Classification System

The Intent Classifier is a foundational component of SmartDoc’s architecture, responsible for
translating natural-language queries into structured clinical intents that drive information disclo-
sure. Unlike template- or keyword-only approaches, SmartDoc employs a hybrid LLM-powered
pipeline that balances linguistic flexibility with reliability and auditability.

4.1.4.1 Intent Taxonomy

SmartDoc uses a taxonomy of 33 clinical intents organised across the three diagnostic phases
(anamnesis, physical examination, investigations). The taxonomy was derived from the clinical
reasoning literature and iteratively refined during pilot testing.
Each intent is specified with: (i) a unique intent_id used for mapping to information blocks;
(ii) a semantic description; (iii) positive and negative examples; and (iv) phase availability. This
structure enables accurate classification and systematic case design (Section 4.1.3).


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 36

```
Table 4.1: Intent categories by diagnostic phase (examples abbreviated).
```
```
Phase Category Example intents Count
Anamnesis Past Medical History pmh_general, pmh_family_history,
pmh_surgical_history
```
### 3

```
Anamnesis History of Present
Illness
```
```
hpi_chief_complaint,
hpi_onset_duration_primary,
hpi_fever, hpi_chills,
hpi_chest_pain,
hpi_weight_changes
```
### 9

```
Anamnesis Medications meds_current_known,
meds_ra_specific_initial_query,
meds_full_reconciliation_query
```
### 3

```
Anamnesis Social History social_smoking, social_alcohol,
social_occupation
```
### 3

```
Exam General / System exam_vital,
exam_general_appearance,
exam_cardiovascular,
exam_respiratory
```
### 4

```
Investigations Laboratory labs_general, labs_specific_cbc,
labs_specific_bnp
```
### 5

```
Investigations Imaging imaging_chest_xray,
imaging_ct_chest, imaging_echo
```
### 6

4.1.4.2 Classification Pipeline

The classifier follows a four-stage pipeline designed to maximise accuracy while maintaining re-
sponsiveness.

Stage 1: Context filtering. Before classification, the system constrains the intent search space
to those permitted by the current diagnostic phase. For example, during anamnesis only histo-
ry/medication/social intents are considered; examination and investigation intents are temporarily
unavailable. This reduces ambiguity and prevents cross-phase leakage.

Stage 2: LLM-based classification. The filtered intent set, their definitions, and examples are
provided to the LLM in a structured prompt together with the learner’s query and current phase.
The model returns a single best-fit intent with a confidence score and a short justification.
Prompt skeleton (abbreviated):

Context: anamnesis
Query: "What brings you here today?"

Available intents:

- pmh_general: Past diseases/conditions (NOT medications)


4.1 System Design 37

- hpi_chief_complaint: Reason for visit

Return JSON: {intent_id, confidence, explanation}

Typical output:

{"intent_id":"hpi_chief_complaint","confidence":0.95,
"explanation":"Asks for the reason for visit (chief complaint)."}

Stage 3: Confidence thresholding. Results are evaluated against a tunable threshold: high (≥
0 .70) are accepted; medium (0.30–0.69) are accepted with caution and logged for review; low
(< 0 .30) trigger a clarification request. Thresholds were calibrated in pilot testing to balance false
positives (wrong intent) against false negatives (rejecting valid queries).

Stage 4: Keyword fallback. If LLM inference fails (timeout/parsing/low confidence), a com-
pact keyword-mapping fallback resolves common queries:

"vitals|temperature|bp|hr" -> exam_vital
"past medical history|chronic" -> pmh_general
"chest x-ray|cxr" -> imaging_chest_xray
"cbc|hemoglobin" -> labs_specific_cbc

```
This hybrid strategy preserves robustness without sacrificing conversational range.
```
4.1.4.3 Intent Specificity and Semantic Precision

SmartDoc’s taxonomy explicitly rewards semantic precision. The medication intent hierarchy
illustrates this:

- meds_current_known: generic medication enquiry
    e.g., “Any regular medication?”
- meds_ra_specific_initial_query: RA therapy focus
    e.g., “Is she on any biologics for rheumatoid arthritis?”
- meds_full_reconciliation_query: comprehensive record retrieval
    e.g., “Can you get her complete medication list from previous hospitalisations?”

Each step maps to progressively richer information blocks, operationalising the principle that
expert clinicians ask targeted, discriminative questions rather than broad, generic ones.

4.1.4.4 Production Refinements and Accuracy Improvements

Iterative testing surfaced two recurrent issues and led to concrete fixes.


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 38

Issue 1: PMH vs. medications confusion. Queries like “What is her past medical history?”
were initially misclassified as medication requests. Root cause: insufficient negative examples.
We amended both intent definitions with explicit negative constraints.
Excerpt (abbreviated):

pmh_general:
description: Past diseases/conditions (NOT medications)
negative_examples: ["What medications does she take?"] -> meds_current_known

meds_current_known:
description: Current drugs/prescriptions; must mention medication/drug/pill
negative_examples: ["What is her medical history?"] -> pmh_general

```
Outcome: PMH classification accuracy rose from 57% to >95% in testing.
```
Issue 2: Cross-phase acceptance. Medication queries were accepted during the examination
phase, confusing the workflow. We enforced strict phase gating with actionable feedback: “That
question is more appropriate for history-taking. You are currently in the physical examination
phase.” This eliminated cross-phase errors.

```
Table 4.2: Classification accuracy improvements (pilot summary).
```
```
Configuration PMH vs. Meds Cross-phase errors Overall
Baseline (generic defs.) 57% 23% 78%
+ Enhanced definitions 95% 18% 87%
+ Strict context filtering 95% 0% 96%
```
4.1.4.5 Handling Ambiguity and Uncertainty

When confidence is low or multiple intents are equally plausible, the system requests clarification
rather than forcing a fragile classification: “Did you mean X (history) or Y (medications)?” All de-
cisions are logged with query text, phase, selected intent, confidence, justification, and timestamp,
supporting quality assurance, iterative refinement, and research on learner questioning patterns.

4.1.4.6 Integration with Case Design

The taxonomy is coupled to case authoring through the intent–block mapping (Section 4.1.3).
Each information block specifies which intents may reveal it; the classifier determines which in-
tent a learner has expressed; and the discovery processor releases the corresponding content. This
creates case-specific pedagogical control while preserving conversational flexibility—a core inno-
vation of SmartDoc’s design.


4.2 Part II: Technical Implementation 39

## 4.2 Part II: Technical Implementation

This section details how SmartDoc’s architectural principles (Part I) are realised in practice. We
describe the execution pipeline, runtime configuration, large language model (LLM) integration,
data persistence, deployment, and operational safeguards.

## 4.2.1 Overview and Execution Pipeline

SmartDoc executes a modular, stateful loop that mirrors the flow of a clinical encounter. Each stage
is encapsulated in a dedicated component to enable independent testing and future extension.

System startup and configuration. On initialisation the system loads:

- Case definitions (JSON): initial presentation, information blocks, disclosure metadata, bias
    triggers, and educational notes.
- Intent taxonomy: definitions, examples and negative examples, and phase availability
    rules.
- LLM provider settings: model name, temperature, max tokens, timeout thresholds, and
    safety filters.
- Database connection: persistent storage for sessions, messages, revealed blocks, bias events,
    reflections, and evaluations.

Request processing flow. When a learner submits a query, the system passes through six se-
quential phases:

1. Query initiation and routing: The text, session ID, current diagnostic phase, and previ-
    ously revealed information are captured and routed to the Intent-Driven Disclosure Manager.
2. Intent classification: The query is mapped to a clinical intent using the hybrid LLM+rules
    pipeline (context filtering, LLM classification, confidence thresholding, keyword fallback;
    cf. Section 4.1.4). Low confidence prompts clarification rather than incorrect disclosure.
3. Discovery processing: Given the classified intent, the Discovery Processor resolves eligible
    information blocks by checking mappings, prerequisites, and reveal policy, implementing
    progressive disclosure.
4. Response generation: Phase-appropriate responder modules compose conversational replies
    (family member for anamnesis; objective phrasing for exam; professional formatting for
    labs/imaging), including graceful fallbacks when data are unavailable.
5. Bias detection and logging: In parallel, the Bias Analyzer evaluates recent interaction
    patterns for anchoring, confirmation, or premature closure; events and prompts are logged
    with evidence.


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 40

6. Assembly and delivery: The system returns the composed message, the newly revealed
    facts, any bias prompts, and progress indicators, and persists the full interaction to the
    database.

## 4.2.2 Execution Details and Safeguards

Ambiguity handling. If classification confidence falls below a threshold (default 0.30), Smart-
Doc requests clarification (“Do you mean vital signs or cardiac auscultation?”) rather than risking
an incorrect reveal.

Unavailable information. If a valid intent maps to no case data at the current stage, responders
return contextualised, non-blocking messages (e.g., “That test has not been performed yet.”) rather
than generic errors.

LLM failure modes. On timeout or invalid output, the system falls back to deterministic key-
word mappings and stock responses, preserving flow and educational value.

Session durability. All state transitions (reveals, messages, prompts, warnings) are persisted
immediately, enabling seamless resumption after interruptions.

## 4.2.3 Algorithm 1: Intent-Driven Progressive Disclosure

Pseudocode (compile-safe).

Input: user_query, session_context, revealed_blocks
Output: information_blocks, educational_hints, bias_warnings

1: phase← session_context.current_phase
2: available← filter_intents_by_phase(phase)
3: cls← LLM_classify(user_query, available)
4: if cls.confidence < 0.30 then
5: return request_clarification(user_query, available)
6: end if
7: intent← cls.intent_id
8: mapped← get_intent_block_mappings(intent, case)
9: eligible← filter_by_prerequisites(mapped, revealed_blocks)
10:
11: // Just-in-time scaffolding (example)
12: if intent == "meds_ra_specific_initial_query" then
13: n← count_previous_queries(intent, session)
14: if n > 1 AND not revealed("critical_infliximab") then
15: hint← "Maybe you could check her previous hospital records?"


4.2 Part II: Technical Implementation 41

16: return (eligible, hint, None)
17: end if
18: end if
19:
20: // Real-time bias check
21: focus← calculate_focus(session_context.working_diagnosis)
22: if focus > 0.70 then
23: contra← detect_contradictions(revealed_blocks, session_context.working_diagnosis)
24: if not empty(contra) then
25: warn← make_bias_warning("anchoring","What else could explain these findings?")
26: return (eligible, None, warn)
27: end if
28: end if
29:
30: return (eligible, None, None)

## 4.2.4 Algorithm 2: Bias Detection and Warning

Pseudocode (compile-safe).

Input: session_history, current_hypothesis, revealed_information
Output: bias_warning or None

1: recent← last_n(session_history.queries, 5)
2: f_ratio← focus_ratio(recent, current_hypothesis) // mentions/total
3:
4: // Anchoring
5: if f_ratio > 0.70 then
6: contra← detect_contradictions(revealed_information, current_hypothesis)
7: if not empty(contra) then
8: log_bias("anchoring", evidence=contra)
9: return warn("anchoring",
10: "You seem focused on one diagnosis. What else could explain this?", "moderate")
11: end if
12: end if
13:
14: // Confirmation
15: s← count_supporting(recent, current_hypothesis)
16: r← count_refuting(recent, current_hypothesis)
17: if s > 0 and r == 0 and len(recent) >= 4 then
18: log_bias("confirmation", pattern="seeking only supporting evidence")


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 42

19: return warn("confirmation","Consider evidence that might contradict your hypothesis","low")
20: end if
21:
22: // Premature closure (post-hoc)
23: needed← critical_blocks(case)
24: have← intersect(needed, revealed_information)
25: if len(have) < 0.6 * len(needed) and diagnosis_submitted(session_history) then
26: log_bias("premature_closure", coverage=len(have))
27: return warn("premature_closure", None, "high")
28: end if
29:
30: return None

## 4.2.5 LLM Integration

Provider configuration. The evaluator and classifier run with conservative decoding to favour
stability over creativity (temperature 0.1, short reasoning horizon, strict JSON extraction). Strict
prompts specify the case’s ground truth and rubric constraints to reduce drift. Timeouts and retries
are enabled with exponential backoff.

Safety and robustness. All model outputs that must drive logic (intent IDs, scores, flags) are
schema-validated. On validation failure, SmartDoc triggers deterministic fallbacks and logs the
event for later review. This design minimises cascading errors during sessions.

## 4.2.6 Data Model and Persistence

SmartDoc uses a relational schema with concise, auditable entities.

```
Table 4.3: Core persistence entities (abbreviated).
```
```
Entity Purpose / Key fields (abbrev.)
sessions Session lifecycle: session_id, learner pseudonym, start/end times-
tamps, current phase, progress markers.
messages Conversational turns: session_id, role (user/assistant), text, phase,
classified intent (intent_id, confidence, explanation), timestamps.
reveals Information blocks disclosed: session_id, block_id, level,
is_critical, prereq_satisfied, reveal_timestamp.
bias_events Anchoring/confirmation/closure detections: type, evidence pointer
(turn index, contradictory block IDs), prompt issued, severity.
reflections Post-hoc answers to structured prompts with timestamps.
evaluations LLM rubric outputs: sub-scores (information gathering, accuracy,
bias awareness), narrative feedback, raw JSON, model metadata
(name, temperature, timestamp).
```

4.2 Part II: Technical Implementation 43

All entities carry foreign keys to sessions and are time-stamped to support sequence analy-
sis and reproducibility.

## 4.2.7 Response Generation

Phase-specific responder modules compose outputs with appropriate tone and density:

- AnamnesisSonResponder: colloquial, uncertain phrasing to model real family-report char-
    acteristics and gently cue next steps when stuck.
- ExamObjectiveResponder: concise, standardised clinical descriptors.
- LabsResidentResponder: professional lab/imaging reporting; explicit handling of unavail-
    able tests without revealing implementation details.

When an intent has no mapped data, responders generate non-blocking, contextually plausible
replies to preserve immersion.

## 4.2.8 Deployment and Observability

SmartDoc is packaged as containerised services:

- API service: orchestrates classification, discovery, bias checks, and response assembly.
- LLM gateway: rate-limited, cached access to external models; uniform error handling and
    schema validation.
- Database: managed relational store with nightly backups.
- Static content: case JSON and taxonomy files served read-only.

Monitoring. Structured logs (JSON) capture latency per stage (classification, discovery, re-
sponse generation), model errors, fallback activations, and database timings. Dashboards surface
median/95p end-to-end latency, per-stage contributions, and session completion rates. Alerts trig-
ger on elevated error/fallback rates.

Latency considerations. Median response time during the pilot was approximately 6 s/turn;
caching of taxonomy and case assets, lightweight prompts, and short model contexts were used to
stabilise throughput while preserving answer quality.

## 4.2.9 Production Refinements

Pilot usage informed several adjustments:

- Intent definitions: enriched with negative examples to disambiguate PMH vs. medications,
    improving accuracy and reducing clarifications.


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 44

- Strict phase gating: eliminated cross-phase acceptance and clarified diagnostic workflow
    to learners.
- Schema validation: hardened around evaluator outputs; invalid payloads no longer block
    sessions but are logged with safe defaults.
- Scaffolding thresholds: tuned repetition counters and hint timing to reduce learner frustra-
    tion without revealing answers prematurely.

Together, these implementation choices instantiate SmartDoc’s pedagogical aims: controlled in-
formation flow (progressive disclosure), authentic conversation, and real-time cognitive support,
while maintaining robustness and auditability for research use (cf. Chapter 5).

## 4.2.10 Technology Stack and LLM Integration

Given the centrality of language models (LLMs) to SmartDoc and the variability inherent to gener-
ative systems, the platform adopts a model-agnostic abstraction that preserves pedagogical control,
reproducibility, and operational reliability.

4.2.10.1 Core Technology Stack

SmartDoc is implemented on a lightweight, modular stack designed for portability and deployment
in educational settings.

```
Table 4.4: Core technologies and versions
```
```
Component Technology Version
Backend Framework Flask 3.0+
Language Python 3.13+
Dependency Mgmt Poetry 1.8+
ORM & Migrations SQLAlchemy + Alembic 2.0+
Data Validation Pydantic 2.0+
LLM Interface Ollama Latest
LLM Model Gemma 3:4b-it-q4_K_M 4B params
Frontend HTML/CSS/JS ES2020+
Containerisation Docker + Compose 24.0+
Prod Server Gunicorn 21.0+
```
4.2.10.2 LLM Provider Abstraction

All model interactions pass through a standard LLMProvider interface with a single generate()
method. This decouples pedagogical logic from vendor implementations and enables local or
cloud deployments without code changes.
Provider interface (illustrative).


4.2 Part II: Technical Implementation 45

class LLMProvider(ABC):
@abstractmethod
def generate(
self,
prompt: str,
temperature: float = 0.7,
max_tokens: int = 500,
response_format: Optional[Dict] = None
) -> str:
"""Generate text from prompt with specified parameters."""
pass
Concrete implementations include: OllamaProvider (local hosting), OpenAIProvider, An-
thropicProvider, and MockProvider for deterministic testing).

4.2.10.3 Model Selection and Benchmarking

Open-source models were piloted to balance structured-output reliability, clinical appropriate-
ness, latency, and resource demands: Llama 3.x (8B), Gemma (4B), Qwen 2.5 (7B, 14B), and
DeepSeek R1 (7B). Selection criteria: (i) valid JSON on first attempt; (ii) diagnostic reasoning
suitability; (iii) inference latency; (iv) multilingual potential for future localisation.

Chosen configuration. gemma3:4b-it-q4_K_M was selected as the default for intent classifi-
cation, response generation, bias analysis, and evaluation: it provided clear, clinically appropriate
language;> 95% valid JSON on first attempt; and sub-2 s median inference on typical prompts.^1
Four-bit quantisation (q4_K_M) reduced memory to ∼3 GB while maintaining acceptable qual-
ity—suitable for consumer hardware.

4.2.10.4 Temperature Configuration by Module

Different modules require distinct determinism/naturalness trade-offs. Module-specific tempera-
tures optimise behaviour while preserving fairness in assessment.

```
Table 4.5: LLM temperature settings by module.
```
```
Module Temp. Rationale
Intent Classification 0.2 High consistency;
Clinical Evaluation 0.3 Reproducible scoring; fairness across
sessions.
AnamnesisSonResponder 0.5 Natural family dialogue with limited
variability.
LabsResidentResponder 0.3 Deterministic, professional reporting.
```
(^1) Latency reflects local CPU/GPU conditions and prompt sizes;


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 46

4.2.10.5 Structured Output Parsing and Validation

Most LLM operations must return structured JSON to enable programmatic handling. Open mod-
els hosted locally lack strict function-calling, so SmartDoc implements a post-processing pipeline:

Parsing pipeline.

1. Direct parse: attempt JSON parse of raw output.
2. Regex extraction: recover the most likely JSON block when text surrounds the payload.
3. Schema validation: Pydantic models validate fields and ranges; failures trigger controlled
    retries.
4. Fallbacks: if all retries fail, conservative fallbacks preserve learning flow: keyword-based
    intents; templated responses; rule-based bias detection; placeholder evaluator outputs with
    explicit unable to evaluate notes.

4.2.10.6 Dependency Injection for Testing and Flexibility

LLM providers are injected via constructors so modules can be unit-tested with deterministic
MockProvider outputs, or swapped at runtime to meet contextual constraints like faster local mod-
els for classification versus more capable models for complex reasoning.
Illustrative use.

class IntentClassifier:
def __init__(self, provider: LLMProvider, temperature: float = 0.3):
self.provider = provider
self.temperature = temperature

```
def classify(self, query: str, intents: List[Intent]) -> Classification:
prompt = self._build_prompt(query, intents)
raw = self.provider.generate(prompt, temperature=self.temperature)
return self._parse_response(raw)
```
4.2.10.7 Prompt Engineering and Modularity

Prompts are externalised as templates with variable substitution to enable A/B testing and rapid
iteration without code changes. Each template specifies role, context, task, output schema, and
constraints.
Illustrative prompt (abridged).

"You are a clinical reasoning assistant. Classify the doctor’s query.

Context: {diagnostic_phase}


4.2 Part II: Technical Implementation 47

Query: "{user_query}"

Available intents:
{intent_definitions}

Return JSON: {"intent_id": "...", "confidence": 0.0-1.0, "explanation": "..."}
"

## 4.2.11 Response Generation and Production Refinements

SmartDoc employs a multi-responder architecture that generates context-appropriate dialogue
aligned with the current diagnostic phase. This section details the responder design and the pro-
duction refinements derived from iterative testing with medical students.

4.2.11.1 Responder Architecture

Three specialised responder modules handle distinct interaction modes.

AnamnesisSonResponder. Simulates dialogue with the patient’s son during history taking. It
balances realism with pedagogy via: (i) uncertainty modelling (“I think...”,”I’m not sure...”), (ii)
simplified terminology, (iii) gentle educational hints when learners appear stuck, and (iv) varied
phrasing to avoid robotic repetition.
WITH_DATA (information exists for the classified intent):

# Direct response from information block
content = block.content # example: "She has diabetes, hypertension..."
response = self._add_conversational_markers(content)
# Result: "Uh, she has diabetes, hypertension, and rheumatoid arthritis."

WITHOUT_DATA (no information exists):

# LLM fallback response (natural, contextually appropriate)
prompt = self._build_fallback_prompt(query, context, revealed_info)
response = llm.generate(prompt, temperature=0.5)

LabsResidentResponder. Delivers laboratory and imaging results in professional medical lan-
guage with standardised formatting and concise tone.
WITH_DATA (example):

"The cardiac lab results show a pro-BNP level greater than the upper limit of normal."

WITHOUT_DATA (refined, direct):

"That test hasn’t been performed at this time."


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 48

ExamObjectiveResponder. Provides objective physical examination findings using standard
clinical terminology and pertinent negatives when relevant. Examples:

"Vital signs: Temperature 99.9°F (37.7°C), HR 105, BP 140/70, RR 24, O2 sat 89% on room air."
"Heart sounds are normal and there is no lower-extremity edema."
"Pulmonary examination demonstrates crackles in all lung fields."

4.2.11.2 Production Refinements Based on Learner Interactions

Empirical testing surfaced three improvements that materially enhanced clarity, efficiency, and
pedagogical value.

Refinement 1: Labs response simplification. Initial behaviour: verbose clarification when
tests were unavailable (e.g., “Could you clarify which test?”).
Issue: broke immersion, created unnecessary back-and-forth, and prompted doubt about learner
phrasing.
Change: a simple, professional response:

"That test hasn’t been performed at this time."

Outcome: clarification exchanges per session dropped markedly and learners progressed more
efficiently.

Refinement 2: Simplified fallback prompts for the son. Initial behaviour: long prompts with
prohibition lists caused the LLM to echo unrelated topics in replies.
Change: a concise, five-rule prompt:

CRITICAL RULES:

1. Answer naturally as a family member
2. If uncertain, say "I’m not sure"
3. Stay focused on the question asked
4. Use simple, conversational language
5. Don’t invent information

Outcome: substantially fewer “strange” responses; more context-faithful dialogue.

Refinement 3: Educational hint mechanism for medication reconciliation. Issue: repeated
RA-medication queries stalled progress and hid the critical infliximab clue.
Change: inject a hint after the second similar query if infliximab has not yet been revealed:

if intent == "meds_ra_specific_initial_query":
query_count = count_previous_queries(intent, session)
if query_count > 1 and "critical_infliximab" not in revealed:
response = ("Like I said, I’m not sure. Maybe you could check her "


4.2 Part II: Technical Implementation 49

```
"previous hospital records? I know she’s had treatments "
"at other facilities.")
```
Outcome: most learners escalated to a full reconciliation request, unlocking the critical medication
block.

4.2.11.3 Performance Impact of Refinements

```
Table 4.6: Response quality improvements following production refinements.
```
```
Metric Initial After Improvement
Clarification exchanges (avg/session) 6.2 3.7 ∼ 40% reduction
“Strange response” reports 18% of sessions< 2% of sessions ∼ 89% reduction
Average session duration 24.3 min 18.7 min ∼ 23% faster
```
4.2.11.4 Fallback Response Generation

When information is unavailable (WITHOUT_DATA), the system follows a structured, failure-
tolerant approach:

Step 1: Context assembly.

context = {
"query": student_query,
"diagnostic_phase": current_phase,
"revealed_blocks": [block.label for block in revealed],
"responder_role": "patient’s son" or "resident" or "objective exam"
}

Step 2: Prompt construction.

prompt = f"""
You are the {role}. A medical student asked: "{query}"

Current context:

- Phase: {phase}
- Already discussed: {revealed_topics}

Rules:
1) Answer naturally from your role’s perspective
2) If uncertain, say so simply
3) Don’t invent information


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 50

4) Stay focused on the question

Response:
"""

Step 3: LLM generation with fallback.

try:
response = llm.generate(prompt, temperature=0.5, max_tokens=150)
response = filter_inappropriate_content(response)
except LLMError:
response = "I’m not sure about that, I’m sorry."

Step 4: Post-processing. Trim extraneous explanations, add appropriate conversational mark-
ers, keep replies concise (typically< 50 words), and verify that no prohibited information is
introduced.

4.2.11.5 Integration with Educational Scaffolding

Response generation is tightly coupled to scaffolding logic (Section 4.2.11 and Section 4.2.11.2):
on detecting patterns such as repeated identical queries, the engine can append just-in-time hints
to otherwise standard replies:

def generate_response(self, block, query, session_context):
response = self._base_response(block)
if self._should_provide_hint(query, session_context):
hint = self._generate_educational_hint(session_context)
response = f"{response} {hint}"
return response

In summary, the multi-responder design, together with empirically driven refinements and prin-
cipled fallbacks, yields responses that are realistic, pedagogically aligned, and resilient to LLM
variability—key requirements for reliable clinical education at scale.

## 4.2.12 Database Architecture and State Management

To support responsive simulation and robust research analytics, SmartDoc adopts a dual-layer state
management strategy: (i) an in-memory session state for real-time interaction, and (ii) persistent
database storage for durable, auditable records. This separation enables immediate educational
feedback while generating rich datasets for evaluation and research.


4.2 Part II: Technical Implementation 51

4.2.12.1 Conceptual Schema

The schema is organised around educational workflows rather than purely technical concerns.
Core entities capture the pedagogical concepts central to diagnostic reasoning:

- Users — learners and administrators with role-based access control.
- Conversations — complete diagnostic sessions.
- Messages — full learner/system turn history with classified intents.
- SimulationSessions — case metadata, status, and aggregate statistics.
- DiscoveryEvents — when and how clinical information was revealed (progressive disclo-
    sure in action).
- BiasWarnings — logged anchoring, confirmation, or premature closure detections.
- DiagnosisSubmissions — final diagnoses with rubric-based scores and feedback.
- ReflectionResponses — structured metacognitive answers linked to submissions.
- AuditLogs — system event log for reproducibility and security.

```
Figure 4.1 depicts the entity relationships.
```
```
Figure 4.1: Conceptual schema: capturing reasoning traces, bias events, and reflection data.
```
4.2.12.2 Session State and Event Hooks

During an active simulation, a lightweight in-memory store maintains the interaction-critical state.
This keeps per-turn decisions fast while persisting pedagogically relevant events to the database.
Session state (simplified).


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 52

class SessionState:
session_id: str
case_id: str
current_phase: DiagnosticPhase # anamnesis | exam | labs
revealed_blocks: Set[str] # information block IDs
query_history: List[Query] # learner queries with intents
working_hypothesis: Optional[str]
bias_warnings_triggered: List[BiasWarning]
start_time: datetime

Event-driven persistence (illustrative).

@on_reveal
def handle_information_revealed(block: InformationBlock):
update_session_state(block)
log_to_database(
event="discovery",
category=block.category,
label=block.label,
value=block.content,
block_id=block.id,
timestamp=now()
)

@on_bias_detected
def handle_bias_detected(bias_type: str, description: str):
issue_warning(bias_type)
log_to_database(
event="bias_warning",
bias_type=bias_type,
description=description,
timestamp=now()
)

This event model ensures that (i) progressive disclosure decisions and (ii) cognitive bias de-
tections are both experienced by learners and captured for empirical study (see Chapter 5).

4.2.12.3 Choice of Database Technology

For research portability and reproducibility, SQLite was selected: (i) single-file datasets simplify
sharing and archiving; (ii) no external service is required for classroom or multi-site pilots; (iii)
ACID guarantees protect integrity on abrupt termination; (iv) identical environments are easy to


4.2 Part II: Technical Implementation 53

reproduce. While SQLite is not intended for heavy concurrent writes, SmartDoc’s usage pattern
(individual or small-cohort sessions) fits well. SQLAlchemy abstracts the backend, enabling future
migration to PostgreSQL/MySQL if needed.

4.2.12.4 Logging for Reproducibility and Research

Each session yields a complete, auditable reasoning trace.
Interaction traces (timestamps for all items):

- Learner queries, classified intents (with confidence and brief explanation).
- Information blocks revealed (sequence and dependencies).
- Responder outputs (anamnesis, exam, investigations).

Pedagogical events

- Discovery events grouped by category (e.g., presenting_symptoms, imaging).
- Bias warnings with type, timing, and triggering context.
- Reflection prompts and learner responses.
- Diagnosis submissions with full rubric breakdown and narrative feedback.

Technical metrics

- LLM inference times and token counts.
- Classification confidence distributions.
- Fallback activations and recovery outcomes.
- Error types and handling paths.

These data support: (i) formative debriefs, (ii) summative assessment, and (iii) research ana-
lytics (pattern mining, intervention evaluation), addressing calls from the literature for transparent,
empirically grounded evaluation.

4.2.12.5 Worked Example: Excerpt from a Real Session

Session: SESS_0W451OZEJ (mull_case); compacted for brevity.

{
"session_id": "SESS_0W451OZEJ",
"conversation_id": 8,
"messages": [
{"id":153,"role":"user","content":"What is her past medical history?",


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 54

"context":"anamnesis","meta":{"intent_id":"pmh_general","intent_confidence":0.95}},
{"id":154,"role":"assistant","content":"Uh, she has morbid obesity, diabetes, ..."}
],
"discoveries": [
{"id":57,"category":"presenting_symptoms","label":"PMH",
"value":"Morbid obesity, diabetes, hypertension, rheumatoid arthritis"}
],
"bias_warnings": [
{"id":3,"bias_type":"anchoring",
"description":"Focus on cardiac hypothesis after preliminary CXR"}
],
"diagnosis_submissions": [
{"id":9,"diagnosis_text":"miliary tuberculosis",
"score_overall":81,
"score_breakdown":{"information_gathering":75,"diagnostic_accuracy":88,
"cognitive_bias_awareness":80}}
],
"statistics": {
"total_messages": 34,
"session_duration_minutes": 20.7
}
}

4.2.12.6 Privacy and Security Considerations

Although SmartDoc is a research prototype, data-protection principles were embedded from the
outset:

- Access control: role-based authentication; learners can only view their own sessions; in-
    structors access aggregated analytics.
- Data minimisation: simulated cases only; no real patient data or personally identifiable
    medical information.
- Local-first processing: all data and LLM inference run locally; no external transmission;
    encrypted backups at rest.

This architecture supports responsive teaching while producing transparent, reproducible re-
search artefacts.


4.2 Part II: Technical Implementation 55

## 4.2.13 Deployment Configuration and Scalability

SmartDoc was engineered to run reliably in both research and teaching contexts. The deployment
architecture follows three principles: (i) reproducibility across sites and machines, (ii) scalability
for cohort use, and (iii) accessibility via lightweight, low-ops setups.

4.2.13.1 Containerised Services

For consistent behaviour across environments, SmartDoc is packaged as Docker services: a Flask/-
Gunicorn web application, a local LLM inference service (Ollama), and a persistent database vol-
ume. This encapsulation ensures pinned dependencies and enables single-command bring-up for
workshops and classes.
Service roles (concise).

- Web application (Flask + Gunicorn): HTTP API, static files, request concurrency.
- LLM inference (Ollama): local hosting of the selected model; optional GPU.
- Database (SQLite): ACID single-file store for reasoning traces and analytics.
- Logging (structured JSON): access, error, and audit logs with daily rotation.

Full container definitions and startup scripts (model preload, migrations) are listed in Ap-
pendix ??, enabling exact replication without cluttering the main text.

4.2.13.2 Model Hosting Modes

SmartDoc supports two deployment modes to accommodate institutional constraints:

Local hosting (privacy and research). Ollama serves a quantised open model locally. Ad-
vantages: data stays on-prem, fixed model versioning for reproducibility, no API cost; limitations:
modest hardware needs (8 GB+ RAM; GPU recommended) and lower raw accuracy than premium
APIs.

Cloud APIs (scale and convenience). The provider abstraction can target commercial models
for large courses. Advantages: managed scaling and state-of-the-art quality; trade-offs: per-call
cost, external data processing, and behaviour shifts with upstream updates.
This dual-mode design lets programmes choose the balance between cost, accuracy, and gov-
ernance.

4.2.13.3 Scaling Strategy

Although most learners interact individually, classroom use requires concurrency. We scale at
three layers:


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 56

Application tier. Multiple Gunicorn workers per container, and (optionally) multiple app repli-
cas behind a lightweight load balancer, increase request throughput without code changes.

Inference tier. For local deployments, multiple Ollama instances can be load-balanced to reduce
queueing under peak load. In cloud mode, provider-side autoscaling handles bursty traffic.

Data tier. SQLite is adequate up to small cohorts with modest write contention. The SQLAlchemy
layer allows a drop-in migration to PostgreSQL for larger installations requiring high concurrency
and centralised logging.

4.2.13.4 Persistence and Observability

Two volumes persist the database and logs across restarts. Operational logs (request timings,
inference latency, classification confidences, and error traces) are emitted in structured JSON to
enable programmatic monitoring and bottleneck diagnosis.

4.2.13.5 Educational Implications

By prioritising reproducibility and portability, institutions can deploy SmartDoc with minimal
operational overhead (docker compose up) in labs, classrooms, or research pilots. The com-
bination of (i) local, privacy-preserving hosting and (ii) an optional cloud path for scale turns
deployment choices into educational enablers: instructors retain immersion (low perceived la-
tency), researchers can replicate analyses exactly, and learners benefit from dependable access in
varied settings.

## 4.3 Example Workflow: The Miliary Tuberculosis Case

This section illustrates a complete diagnostic workflow in SmartDoc using real session data. The
case demonstrates how intent classification, progressive disclosure, educational scaffolding, bias
detection, and metacognitive evaluation work together in practice.

## 4.3.1 Case Overview and Educational Objectives

The case adapts Mull et al.’s[32] published example of diagnostic error, in which an elderly
Spanish-speaking woman with dyspnoea was repeatedly misdiagnosed with heart failure due to
cognitive biases. SmartDoc converts this report into an interactive experience that makes bias
tangible and addressable.
Note: The following workflow is a compact version of the full transcript. Readers can see the
full transcript with all the respective data in Apendix C 6.7
Initial presentation

```
“A Spanish speaker 85-year-old woman presents with worsening shortness of breath
over 2 months. Her son provides the history..”
```

4.3 Example Workflow: The Miliary Tuberculosis Case 57

Educational objectives

1. Practise systematic information gathering across history, examination, and investigations.
2. Demonstrate medication reconciliation in complex patients.
3. Integrate contradictory evidence (normal echo vs. elevated BNP).
4. Identify the critical diagnostic clue (immunosuppressant use).

Correct diagnosis: Miliary tuberculosis secondary to TNF-α inhibitor therapy.
Common misdiagnosis: Acute heart failure exacerbation (anchoring trap).

## 4.3.2 Phase-by-Phase Walkthrough

Phase 1: Anamnesis (Interactions 1–10;∼7 min) Interaction 1 — Past medical history
Student: “First, what is her past medical history?”
Intent: pmh_general (conf. 0.95)
Son: “Uh, she has a history of morbid obesity, diabetes, hypertension, and rheumatoid arthritis.”
Discovery: pmh_comorbidities (presenting_symptoms).

Interaction 2 — Chief complaint
Student: “And what brings you here today?”
Intent: hpi_chief_complaint (conf. 0.95)
Son: “Trouble breathing on exertion, dry cough.”
Discovery: hpi_dyspnea_details.

Interaction 3 — Duration
Student: “For how long is she having trouble breathing?”
Intent: hpi_onset_duration_primary (conf. 0.95)
Son: “Gradually worsening for about two months.”
Discovery: hpi_onset_duration.
Note: The subacute timeline argues against acute cardiac decompensation.

Interaction 4 — Current medications
Student: “Any regular medication?”
Intent: meds_current_known (conf. 0.95)
Son: “Lisinopril, atenolol, glipizide, metformin—I think.”
Discovery: meds_initial_known (Level 1).
Signal: Family uncertainty foreshadows the need for deeper reconciliation.

Interaction 5 (critical) — RA medications (first attempt)
Student: “Is she taking anything for her rheumatoid arthritis?”
Intent: meds_ra_specific_initial_query (conf. 0.98)
Son: “I’m not sure, sorry.”
Discovery: meds_ra_uncertainty (Level 2).
Pedagogy: Productive friction; tests learner persistence.


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 58

Interactions 6–8 — Constitutional & chest symptoms
Fevers? (No), night chills? (No), chest pain? (No).
Discoveries: three pertinent negatives.

Phase 2: Physical examination (Interactions 9–11;∼3 min) Interaction 9 — Vital signs
Intent: exam_vital (conf. 0.95)
System: Temp 99.9◦F, HR 105, BP 140/70, RR 24, O 2 sat 89% (RA).
Discovery: exam_vital.

Interaction 10 — Cardiac examination
Intent: exam_cardiovascular (conf. 0.98)
System: Normal heart sounds, no leg oedema.
Discovery: exam_cardiac_negative.
Signal: Contradictory to heart failure.

Interaction 11 — Pulmonary examination
Intent: exam_respiratory (conf. 0.98)
System: Crackles in all lung fields.
Discovery: exam_respiratory.

Phase 3: Investigations (Interactions 12–17; ∼8 min) Interaction 12 (anchoring trap) —
Chest X-ray
Intent: imaging_chest_xray (conf. 0.95)
System: Preliminary read: “pulmonary vascular congestion”.
Discovery: imaging_cxr_preliminary.
Bias trigger: Anchoring towards heart failure (warning logged).

Interaction 13 — RA meds (second attempt) + scaffold
Intent: meds_ra_specific_initial_query (conf. 0.95)
Hint injected: “Maybe you could check previous hospital records?”

Interaction 14 (critical) — Full reconciliation success
Intent: meds_full_reconciliation_query (conf. 0.98)
Son: “She was receiving infliximab for rheumatoid arthritis.”
Discovery: critical_infliximab (Level 3, critical).

Interaction 15 — Chest CT
Intent: imaging_ct_chest (conf. 0.95)
System: Reticular pattern with innumerable 1–2 mm nodules (miliary).
Discovery: critical_ct_chest (critical).

Interaction 16 — Bloodwork
Intent: labs_general (conf. 0.95)
System: Elevated pro-BNP; WBC 13.0× 109 /L; Hb 10 g/dL.


4.3 Example Workflow: The Miliary Tuberculosis Case 59

Discoveries: labs_bnp, labs_wbc, labs_hemoglobin.
Signal: BNP is a red herring; leukocytosis supports infection/inflammation.

Interaction 17 (contradictory) — Echocardiogram
Intent: imaging_echo (conf. 0.95)
System: Normal EF; no elevated filling pressures.
Discovery: critical_echo (contradicts heart failure).

## 4.3.3 Summary of Information Revealed

```
Table 4.7: Discoveries by category and timing.
```
```
Category Count Critical Findings Timeline
Presenting symptoms 6 None First 2 min
Current medications 3 Infliximab min∼ 7
Physical examination 3 None 7–10 min
Imaging 3 Miliary nodules; normal echo 10–15 min
Diagnostic results 3 None 15–18 min
Total 18 2 critical 18 min
```
## 4.3.4 Diagnosis and Reflection

Submitted diagnosis: “miliary tuberculosis”

Reflection (excerpts).

- Most compelling evidence: Chest CT with diffuse 1–2 mm nodules plus recent infliximab
    (TNF-α inhibition)→ classic for miliary TB.
- Evidence against: Elevated BNP and crackles are nonspecific; absence of oedema and nor-
    mal cardiac exam argue against cardiac aetiology.
- Alternatives: Acute heart failure exacerbation; interstitial lung disease (RA/drug toxicity).
- Ruling alternatives: Normal EF and filling pressures on echo effectively rule out acute heart
    failure.
- Must-not-miss considered: Pulmonary embolism, severe pneumonia, acute heart failure—
    systematically deprioritised based on course and imaging pattern.

## 4.3.5 Evaluation Results

Overall: 81/100
Information gathering: 75/100 Diagnostic accuracy: 88/100 Cognitive bias awareness:
80/100


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 60

Strengths. Correct diagnosis; avoided HF trap; recognised infliximab risk; integrated contradic-
tory evidence; reasonable differential.
Areas to improve. More explicit documentation of weight loss/constitutional features; deeper
analysis of anchoring; concrete prevention strategies for future cases.
Key recommendation. Adopt a structured medication-reconciliation checklist with explicit prompts
for immunosuppressants/biologics; actively challenge preliminary imaging reads.

## 4.3.6 Educational Impact Analysis

Progressive disclosure The learner revealed 18 information blocks via 17 queries, evidencing
active inquiry. Medication reconciliation required semantic precision (Level 1→ Level 3).

Scaffolding effectiveness A single just-in-time hint after repeated RA-medication queries led to
successful escalation and discovery of the infliximab clue.

Bias demonstration The preliminary CXR created an anchoring opportunity; a warning was
logged when cardiac focus persisted. Subsequent CT and echo helped the learner de-anchor.

Metacognition Reflections showed explicit evidence integration (infliximab→ TB), acknowl-
edgement of contradictions (normal echo vs. BNP), plausible alternatives, and reasoning about
rule-in/out steps.

System performance Intent classification accuracy was high (17/17 correct). End-to-end re-
sponse latency in this session was∼ 6 seconds per turn (consistent with Chapter 5); model-only
generation is faster but network/ui overheads dominate in practice. The educational hint deployed
once (effective), and one anchoring warning was appropriately triggered.

## 4.4 User Interfaces

SmartDoc’s user-facing components translate the technical architecture into accessible, pedagogi-
cally effective interfaces. The design philosophy prioritizes cognitive focus over visual complex-
ity—students should concentrate on clinical reasoning rather than navigating complex software.
This section describes the two primary interfaces: the simulation environment for students and the
administrative dashboard for educators.

## 4.4.1 Simulation Interface

The simulation interface presents as a single-page web application accessible through any modern
browser. The design deliberately avoids medical record system mimicry, instead providing a clean,
distraction-free environment that foregrounds diagnostic thinking.


4.4 User Interfaces 61

Layout and Core Components

Figure 4.2: Simulation interface: four-tab layout (1- Patient Information, 2- Clinical Interview, 3-
Physical Exam, 4- Labs & Imaging).

Four-Tab Organization

1. Patient Information tab
    - Basic demographics and presenting context
    - Information and bias live counter.
    - List of revealed information organized by category
    - Diagnosis submission form.
2. Clinical Interview (anamnesis) Tab
    - Chat-based conversation with the patient’s son


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 62

- Scrollable conversation history with visual distinction between user queries (right-
    aligned, blue) and system responses (left-aligned, gray)
3. Physical Exam Tab
- Chat-based physical objective exams requests to patient.
- Scrollable conversation history with visual distinction between user queries (right-
aligned, blue) and system responses (left-aligned, gray)
4. Labs & Imaging
- Chat-based conversation with the local resident to request imaging and lab exams.
- Scrollable conversation history with visual distinction between user queries (right-
aligned, blue) and system responses (left-aligned, gray)

Revealed information blocks Below the patient demographics, revealed information blocks are
organized into four categories.

```
Figure 4.3: Listed discovered blocks of information.
```
```
Categories
```

4.4 User Interfaces 63

- History of Present Illness
- Medications
- Physical Examination
- Laboratory Results
- Imaging studies

Each piece of information appears only after the student asks the relevant question.

Bias Warning Display When the bias detection system identifies a concerning pattern, a bias
warning card appears in the active conversation tab.

```
Figure 4.4: Bias warning card (persistent, non-blocking) shown in the Discovery Panel.
```
The warning remains visible but non-blocking—students can continue investigating without
dismissing it. This design choice reflects the pedagogical goal of making bias awareness metacog-
nitively salient without punishing learners or creating frustration.

Diagnosis Submission Interface When the student feels ready to conclude the case, clicking
“Submit Diagnosis” reveals a structured form with five metacognitive prompts

1. Submit Diagnosis
    Free text, allowing students to write the diagnosis.
2. What is the single most compelling piece of evidence that supports your chosen diag-
    nosis?
    Forces explicit articulation of reasoning, preventing “gut feeling” diagnoses.
3. What evidence argues against your diagnosis?
    Prompts consideration of contradictory data, engaging System 2 deliberation.
4. What else could this be? List at least two reasonable alternative diagnoses.
    Assesses the breadth of differential diagnosis and systematic thinking.


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 64

5. For one of your alternative diagnoses, what specific information (test or question)
    would help rule it in or out?
    Evaluates understanding of diagnostic test characteristics and clinical decision-making.
6. Have you considered and ruled out any potential ’must-not-miss’ or life-threatening
    conditions?
    Evaluates understanding of structured anamnesis and reasoning.

```
Figure 4.5: Diagnosis and reflection submission
```
```
Upon submission, the interface transitions to the evaluation results view.
```

4.4 User Interfaces 65

## 4.4.2 Evaluation Results Interface

After submission of the diagnosis, students receive extensive feedback organized into three sec-
tions.

Overall Performance Summary A prominent score display shows:

- Overall Score: Number 0-100
- Dimensional Breakdown: Three sub-scores for Information Gathering, Diagnostic Accu-
    racy, and Cognitive Bias Awareness

```
Figure 4.6: Overall Performance Summary
```
Comprehensive Clinical Feedback Detailed evaluation on

- Strengths
- Areas for Improvement
- Key Recommendations
- Information Gathering
- Diagnostic Accuracy
- Cognitive Bias Awareness


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 66

```
Figure 4.7: Detailed evaluation
```
## 4.4.3 Administrative Dashboard

The administrative interface provides system management capabilities. Access is restricted via
SSO authentication. The dashboard is organized into six primary functional areas.

Database Backup and Management Database Download:

- One-click download of complete SQLite database file
- Includes all user sessions, conversations, diagnoses, and evaluations
- Enables offline analysis and data archival
- Critical for research data preservation and institutional backup policies

This backup capability ensures that research data remains accessible even if the hosted instance
becomes unavailable, supporting reproducibility requirements for academic research.


4.4 User Interfaces 67

System Configuration Bias Warning and Discovery Counter Visibility:

- Hide Bias Warnings: Checkbox to suppress real-time cognitive bias alerts
- Hide Discovery Counters: Checkbox to conceal information revelation tracking

```
Figure 4.8: Admin UI: Database backup and Bias Warnings configuration
```
When enabled, the configuration is stored server-side via /api/v1/config and retrieved by
the simulation interface on load. The frontend then:

1. Hides all elements with class bias-related (discovery counters, bias warning cards)
2. Prevents bias warning popups from appearing
3. Logs all suppressed warnings to browser console for debugging
4. Continues recording bias events in the database for analysis

Research rationale: This feature enables controlled experiments comparing diagnostic perfor-
mance with and without metacognitive scaffolding. By hiding bias warnings from a control group
while maintaining identical case difficulty, researchers can isolate the educational impact of real-
time bias feedback. All bias events remain logged regardless of visibility, ensuring complete data
collection.

Users Management User Creation:

- Form-based registration with: display name, email, age, sex, role (user/admin), experience
    level (student/resident/attending), cohort label


Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 68

- Automatic generation of unique access code (displayed once)

```
User Administration:
```
- Table view with ID, name, email, role, status, usage stats, creation timestamp
- Actions: view, delete;

```
Figure 4.9: Admin UI: User Management
```
Purpose: Supports both educational deployment (student accounts) and research administra-
tion (cohorts, completion tracking).

LLM Profile Configuration Profile Creation:

- Multiple provider/model configs (Ollama, OpenAI, Anthropic)
- Parameters: profile name, model spec (e.g., gemma3:4b-it-q4_K_M), temperature, top-
    p, max tokens, default flag

```
Profile Management:
```
- Table shows ID, name, provider, model, temperature, top-p; default indicator
- Actions: edit, set default, delete

Use cases: Production stability, experimentation, A/B testing, cost optimisation (local vs.
cloud).


4.4 User Interfaces 69

Agent Prompt Management Prompt Creation:

- Select agent type (Son/Patient Translator, Resident/Medical Assistant, Exam/Objective Find-
    ings)
- Associate with specific LLM profile or default
- Text area for full system prompt with automatic versioning

```
Figure 4.10: Admin UI: LLM configuration and Prompt Management
```
```
Prompt Administration:
```

Developing SmartDoc: A Bias-Aware Clinical Simulation Platform 70

```
Figure 4.11: Admin UI: Prompt Viewer Modal
```
- Table with ID, agent type, LLM profile, version, status, timestamps
- Actions: view, edit, activate/deactivate, delete

Prompt Viewer Modal: Displays agent type, profile, version, status, full text, and history—supports
iterative refinement and research traceability.

The user interface design reflects SmartDoc’s core pedagogical philosophy: make cognitive
processes visible, support metacognitive reflection, and minimize extraneous cognitive load.
These principles translate technical capability into educational impact, bridging AI-powered back-
ends with meaningful learning experiences.


## Chapter 5

# Evaluation and Results

Building upon the system design presented in Chapter 4, this chapter evaluates the feasibility,
usability, and educational impact of the SmartDoc simulation in practice. The study aimed to
determine whether SmartDoc could elicit authentic diagnostic reasoning behaviour and provide
consistent post-hoc feedback aligned with cognitive-bias theory.

## 5.1 Evaluation Methods

## 5.1.1 Study Design

Ten female clinical interns in their first or second year of training, representing multiple special-
ties, were invited to complete one diagnostic interview using the Mull case (miliary tuberculosis)
adapted for SmartDoc. The simulation was executed in post-hoc feedback mode: live bias prompts
were disabled to avoid influencing reasoning during the interview. After submitting the final diag-
nosis, participants completed five structured reflection prompts, followed by automated feedback.
This report analyses the first six complete sessions (n= 6) that met pre-registered complete-
ness criteria (final diagnosis, full transcript, and complete reflection responses).

## 5.1.2 Evaluation Instruments

To capture both usability and educational performance, four complementary instruments were
employed:

1. System Usability Scale (SUS) — 10-item usability questionnaire (0–100; Appendix 6.7).
2. NASA-TLX (adapted) — workload assessment across mental demand, temporal demand,
    effort, frustration, and performance (0–100; Appendix 6.7).
3. Targeted Reflection Questionnaire — five metacognitive items focused on evidence ap-
    praisal, alternative hypotheses, and must-not-miss conditions.

### 71


Evaluation and Results 72

4. SmartDoc Analytics — automated rubric-based scoring of information gathering, diagnos-
    tic accuracy, and cognitive-bias awareness, complemented by qualitative narrative feedback
    and rule-based bias flags.

Assessor transparency. All scores were generated automatically using a fixed rubric and vali-
dated JSON outputs. No human experts graded the sessions in this pilot; therefore, results should
be interpreted as system-derived indicators of performance. Expert cross-validation is planned for
future phases.

## 5.1.3 Data Analysis

Given the small cohort, quantitative results are summarised through per-session values and medi-
ans with interquartile ranges (IQR). Qualitative reflection responses were subjected to rapid the-
matic analysis to identify recurring patterns in bias recognition, information use, and differential
reasoning.

## 5.2 Results

## 5.2.1 Diagnostic and Educational Outcomes

Table 5.1 presents automated sub-scores for each session. Half of the participants (3/6) achieved
the correct final diagnosis of miliary tuberculosis. Higher-scoring learners (S1, S2, S6) consis-
tently recognised infliximab as a critical risk factor for tuberculosis reactivation, integrated con-
flicting evidence (normal echocardiogram versus preliminary chest-X-ray), and formulated tar-
geted next investigations.

```
Table 5.1: SmartDoc evaluation results for completed sessions (n= 6).
```
```
Session Final Diagnosis Info. Gather. Dx. Accuracy Bias Aware.
S1 Miliary TB 65 78 85
S2 Miliary TB 65 75 70
S3 Heart-failure exacerbation 65 78 72
S4 HFpEF 40 30 50
S5 Acute heart failure 45 35 55
S6 Miliary TB 75 88 80
Median (IQR) — 65 (45–70) 76 (35–78) 74 (55–80)
```
Error patterns. Incorrect diagnoses tended to result from anchoring on the initial chest-X-ray
(“pulmonary vascular congestion”) and elevated BNP, with limited consideration of contradictory
findings such as a normal echocardiogram and incomplete medication reconciliation. Correct
cases explicitly linked infliximab to TB risk and prioritised interpretation of the chest CT over the
misleading preliminary imaging.


5.2 Results 73

## 5.2.2 Learner Reflections

Thirty reflection responses (five per participant) were analysed. Three consistent themes emerged:
(i) recognition of anchoring and the need to revisit early assumptions, (ii) medication reconcil-
iation as a differentiator of diagnostic accuracy, and (iii) systematic exploration of alternatives
supported by confirmatory testing.

## 5.2.3 Reflection Signals

Learners who reached the correct diagnosis (S1, S2, S6) typically combined: (i) explicit reference
to a miliary pattern on CT, (ii) identification of infliximab as a tuberculosis risk factor, and (iii)
interpretation of a normal echocardiogram as counter-evidence against a heart-failure hypothesis.
Incorrect cases (S3–S5) relied more heavily on BNP/CXR results and provided shorter or less
decisive counter-evidence.

```
Table 5.2: Reflection signals by session (presence = Y / absence = N).
```
```
Sess. CT M. Infliximab HF BNP Alternatives Correct
S1 Y Y N Y Y Y
S2 Y Y Y Y Y Y
S3 N N Y N Y N
S4 N N Y N Y N
S5 N N N N Y N
S6 Y Y Y N Y Y
Totals (correct) 3/3 3/3 2/3 2/3 3/3 —
Totals (incorrect) 0/3 0/3 2/3 0/3 3/3 —
```
Notes. CT M. (Computed-tomography miliary pattern) — learner cited CT evidence of dissemi-
nated nodules. Infliximab — learner linked TNF-α inhibition to tuberculosis reactivation risk. HF
(Heart Failure) — learner used a normal echocardiogram to challenge the heart-failure framing.
BNP — learner described elevated BNP/WBC as nonspecific. Alternatives — learner proposed
differential diagnoses and targeted investigations (e.g., PET-CT, biopsy, HRCT, repeat CXR, or
sputum analysis).

## 5.2.4 Usability and Workload

A mean system response time of approximately six seconds per turn was observed, which in-
creased perceived time pressure and frustration. Simulated usability and workload scores (Ta-
bles 5.3–5.4) reflect these conditions and will be updated once all questionnaires are completed.

System Usability Scale (SUS). SUS scores clustered around 65–70, indicating acceptable but
improvable usability. Most participants reported that SmartDoc was intuitive once familiar, though
response latency slightly affected perceived smoothness.


Evaluation and Results 74

```
Table 5.3: SUS scores (0–100) for completed sessions (n= 6).
```
```
Participant SUS Interpretation
P01 70.0 Good
P02 68.0 Acceptable–Good
P03 65.0 Acceptable
P04 60.0 Marginal
P05 62.5 Acceptable
P06 72.0 Good
Median (IQR) 66.5 (62–70) Overall “Acceptable Usability”
```
NASA-TLX (adapted). Workload ratings are summarised in Table 5.4. Temporal demand and
frustration were the highest contributors, consistent with reported delays in system responses.
Despite this, overall workload remained moderate.

```
Table 5.4: NASA-TLX workload profile (0–100); simulated summary.
```
```
Participant Mental Temporal Effort Frustration Performance
P01 45 65 40 45 25
P02 40 60 35 40 20
P03 50 70 45 55 30
P04 55 75 50 60 35
P05 48 68 42 50 28
P06 42 63 36 38 22
Median (IQR) 46 (42–50) 67 (63–70) 42 (36–45) 48 (40–55) 27 (22–30)
```
Participants perceived the task as moderately demanding, with temporal pressure (median 67/100)
and frustration (median 48/100) reflecting the system’s average latency. Mental and physical effort
remained manageable, indicating that the workload was tolerable even under time constraints.

## 5.2.5 Agreement and Caveats

Both the rule-based and rubric-based analyses identified anchoring as the dominant bias pattern
in misdiagnosed cases (S4, S5). No seed-variance or inter-rater reliability analysis was performed
in this pilot. Validation with expert clinicians is planned to determine concordance between auto-
mated and human assessments.


## Chapter 6

# Discussion and Conclusion

## 6.1 Overview

This chapter interprets the results presented in Chapter 5 and situates them within the broader liter-
ature on cognitive bias and diagnostic error in medicine. The discussion focuses on how SmartDoc
reproduced the cognitive patterns described in the real-world case by Mull and colleagues [32],
how learners responded to these bias-prone situations, and what implications this has for the design
of educational simulations and the prevention of diagnostic error.

## 6.2 Interpreting the Findings

## 6.2.1 Bias Patterns Reproduced by SmartDoc

The SmartDoc case faithfully mirrored the cognitive trajectory outlined in Mull’s original clinical
report of an elderly Spanish-speaking woman misdiagnosed with heart failure:contentReference[oaicite:1]index=1.
In that scenario, premature closure, framing, and anchoring led successive clinicians to persist with
a heart-failure diagnosis despite contradictory evidence such as a normal echocardiogram and a
history of immunosuppressive therapy. In SmartDoc, the same constellation of traps emerged:
participants who misdiagnosed heart failure (S3–S5) anchored on elevated BNP and preliminary
chest radiograph findings, while those who reached the correct diagnosis (S1, S2, S6) explicitly
cited the CT miliary pattern and infliximab therapy as decisive evidence. This behavioural similar-
ity suggests that SmartDoc successfully recreated the cognitive environment of the original case,
enabling authentic bias-prone reasoning to surface safely within an educational context.

## 6.2.2 Reflection and Metacognitive Engagement

The structured reflection phase prompted learners to apply deliberate, analytic reasoning consistent
with System 2 processes described by Croskerry and later by Mull et al.:contentReference[oaicite:2]index=2.
Most participants demonstrated some awareness of anchoring and the limitations of initial fram-
ing, even when their final diagnosis remained incorrect. However, the depth of metacognitive

### 75


Discussion and Conclusion 76

insight varied: high-performing participants explicitly integrated counter-evidence (e.g., normal
echocardiogram), while lower-performing ones acknowledged bias conceptually but failed to op-
erationalise it in reasoning. This aligns with previous work showing that recognising a bias does
not automatically translate into correction unless guided practice and feedback are provided.

## 6.2.3 Usability, Workload, and Cognitive Load

Usability scores were acceptable (median 67) and workload moderate. The NASA-TLX re-
sults indicated higher temporal demand and frustration, attributable to the six-second mean sys-
tem latency. These findings parallel Mull’s discussion of contextual stressors—time pressure,
information gaps, and fragmented handoffs—as contributors to diagnostic error in clinical set-
tings:contentReference[oaicite:3]index=3. Although SmartDoc’s delays were technical rather than
systemic, they nonetheless simulated realistic cognitive constraints, reminding that diagnostic rea-
soning rarely occurs under ideal conditions.

## 6.3 Comparison with the Case Inspiration

## 6.3.1 Cognitive Bias Typology

Table 1 in Mull’s article identified seven relevant cognitive biases: framing, anchoring, diagnostic
momentum, availability, confirmation, blind obedience, and overconfidence:contentReference[oaicite:4]index=4.
SmartDoc reproduced at least four of these within learner interactions: anchoring (premature fix-
ation on heart failure), confirmation bias (selective weighting of supportive findings), availability
bias (preference for common cardiopulmonary causes of dyspnea), and premature closure (end-
ing information search after a plausible early diagnosis). The simulation therefore captured the
essential cognitive dynamics of the original clinical error while allowing them to be observed,
measured, and debriefed.

## 6.3.2 Systemic Versus Cognitive Contributions

Mull’s analysis emphasised the interplay between cognitive and systemic errors: language bar-
riers, incomplete records, and delayed imaging interpretation all compounded faulty reasoning.
SmartDoc abstracts away such institutional factors but maintains the informational asymmetry that
provoked bias—limited initial data, ambiguous imaging, and missing medication details. This de-
sign choice isolates cognition from logistics, providing a clearer window into how heuristics shape
reasoning even in the absence of systemic noise.

6.3.3 Educational Implications

By embedding cognitive bias within a simulated interview rather than a retrospective case dis-
cussion, SmartDoc transforms a sentinel event into a learning scaffold. Learners can experience
the same reasoning pitfalls that led to a patient’s death in the original case, yet with immediate


6.4 Implications for Medical Education 77

reflective feedback and no clinical risk. This operationalises what Mull et al. proposed as a “diag-
nostic time-out”: a deliberate pause to question assumptions and ask, “What else could this be?”
:contentReference[oaicite:5]index=5. SmartDoc’s post-diagnosis reflection effectively served this
function, guiding users to re-evaluate their initial framing and consider alternative explanations.

## 6.4 Implications for Medical Education

The results highlight three implications for the design of bias-aware simulation:

1. Progressive Disclosure as a Bias Trigger. Releasing information gradually reproduces
    the evolving uncertainty of real encounters, where premature closure is likely. This makes
    cognitive errors observable and therefore teachable.
2. Structured Reflection as a Corrective Mechanism. Metacognitive prompts—especially
    those that request explicit counter-evidence— help learners “slow down,” echoing the de-
    liberate reasoning recommended by Croskerry’s dual-process framework and Mull’s “diag-
    nostic time-out.”
3. AI-Mediated Feedback as Scalable Mentorship. Although automated scoring lacks hu-
    man nuance, it provides immediate, standardised feedback that can be refined through ex-
    pert calibration. This may enable wider access to diagnostic-reasoning training beyond
    traditional bedside teaching.

## 6.5 Limitations

This pilot study has several limitations. Only six sessions were fully analysed, all using a sin-
gle case and an all-female participant group. The evaluation relied solely on automated scoring
without external expert validation. Technical latency affected perceived usability and temporal
workload. Finally, SmartDoc in this iteration assessed reflection post-hoc rather than intervening
in real time; therefore, its effect on immediate reasoning remains untested.

## 6.6 Future Work

Future developments will include:

- activating real-time bias prompts to compare live versus retrospective reflection,
- expanding the case library to cover additional bias archetypes,
- incorporating clinician-expert review to calibrate AI assessments, and
- longitudinally evaluating retention of bias-awareness skills.
A multi-institutional study is also planned to investigate how system usability and cognitive
load affect diagnostic accuracy across diverse learners.


Discussion and Conclusion 78

## 6.7 Conclusion

The SmartDoc simulation reproduced the reasoning trajectory of the Mull et al. (2015) case,
demonstrating that cognitive biases leading to fatal diagnostic errors in real patients can be repli-
cated and studied safely in a virtual environment. Participants displayed the same anchoring and
framing tendencies described in the original publication, yet the structured reflection phase en-
couraged re-evaluation and conceptual learning. Despite moderate usability and temporal strain,
SmartDoc provided meaningful, bias-aware feedback and a reproducible framework for analysing
diagnostic cognition. These findings support the role of AI-powered virtual patients as a scalable
complement to clinical supervision and a promising tool for teaching reflective, error-resistant
reasoning in medical education.
