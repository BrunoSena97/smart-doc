# Chapter 4 Version Comparison: Full vs. Condensed

**Date:** 17 October 2025
**Analysis by:** GitHub Copilot
**Purpose:** Compare the full Chapter 4 (2,101 lines) with the condensed "possible" version (552 lines) to identify what was removed and what should be retained

---

## Executive Summary

### **Quick Statistics:**

| Metric | Full Chapter 4 | Possible Chapter 4 | Difference |
|--------|---------------|-------------------|------------|
| **Total Lines** | 2,101 lines | 552 lines | **-74% reduction** |
| **Estimated Words** | ~15,500 words | ~4,500 words | **-71% reduction** |
| **Tables** | 7 tables | 0 tables | **-7 tables** ❌ |
| **Figures** | 10+ figures | 10 figures | ✅ Same |
| **Sections** | 5 major sections | 5 major sections | ✅ Same structure |
| **Algorithms** | 2 pseudocode | 2 pseudocode | ✅ Same |
| **Depth Level** | 4 levels (subsubsection) | 3 levels (paragraph) | Flatter hierarchy |

### **Overall Assessment:**

**Condensed Version Quality:** 8.0/10
**Full Version Quality:** 9.0/10
**Recommended Action:** **Hybrid approach** - Use condensed as base, add back critical elements from full version

---

## 📊 Detailed Section-by-Section Comparison

### **1. Introduction (Opening Paragraphs)**

#### **Full Version:**
- 41 lines
- Detailed context from Ch 2 & 3
- Explains gaps in literature
- Justifies architectural choices (hybrid vs. pure neural)
- Explicit two-part structure preview

#### **Condensed Version:**
- 30 lines ✅
- Concise context
- **MISSING:** Explicit justification of why "fully end-to-end neural systems were deemed unsuitable" (important pedagogical point)
- **BETTER:** Cleaner roadmap, less repetitive

**Recommendation:** ✅ **Keep condensed**, but add ONE sentence about neural system limitations:
```latex
Fully neural approaches were rejected due to lack of transparency and
educational control, essential for high-stakes medical training.
```

---

### **2. System Design Section**

#### **Full Version (lines 42-545, ~500 lines):**
- Detailed subsections for EACH of 7 core components:
  - Intent Classifier (20 lines)
  - Discovery Processor (35 lines)
  - Simulation Engine (20 lines)
  - Bias Analyzer (30 lines)
  - Clinical Evaluator (30 lines)
  - Response Generation (15 lines)
  - Session Management (15 lines)

#### **Condensed Version (lines 31-157, ~125 lines):**
- **Single paragraph per component** (7 components in ~70 lines total)
- Much more compact, still covers all components
- **REMOVED:** Detailed inner workings of each component
- **RETAINED:** Core functionality descriptions

**What Was Lost:**
- Detailed explanation of dual-process theory integration
- Specific examples of bias detection thresholds
- Temperature settings per module (0.2 for intent, 0.5 for dialogue, 0.3 for evaluation)
- Dependency injection patterns

**Recommendation:** ⚠️ **Mostly keep condensed**, but ADD BACK:
1. **One table:** LLM temperature settings by module (critical technical detail)
2. **One sentence:** About dual-process theory mapping to architecture

---

### **3. Intent Classification - MAJOR DIFFERENCE**

#### **Full Version (lines 546-745, ~200 lines):**
✅ **Table 4.2: Intent Taxonomy** (33 intents organized by phase)
- Detailed 4-stage classification pipeline
- PMH vs. medications confusion problem + solution
- Cross-phase acceptance issue + fix
- **Table 4.3:** Classification accuracy improvements (57% → 95%)
- Keyword fallback mechanism with examples
- Logging and ambiguity handling

#### **Condensed Version:**
❌ **NO TABLE** for intent taxonomy
❌ **NO TABLE** for accuracy improvements
✅ Mentions 33 intents but doesn't visualize
✅ Mentions classification pipeline but less detail
✅ Brief mention of context filtering

**What Was Lost (CRITICAL):**
- Intent taxonomy visualization (Table 4.2)
- Empirical accuracy data (57% → 95% improvement)
- Production refinement details
- Concrete examples of classification pipeline

**Recommendation:** 🔴 **MUST ADD BACK:**
1. **Table 4.2:** Intent taxonomy by phase (from full version lines 563-596)
2. **Table 4.3:** Classification accuracy improvements (from full version lines 705-720)
3. Keep condensed text but reference these tables

**Justification:** Both reference dissertations (Rui Pedro & Ana Guedes) visualize their taxonomies. This is critical technical documentation.

---

### **4. Technical Implementation Section**

#### **Full Version (lines 746-1587, ~840 lines):**
- Extensive subsections:
  - Execution Pipeline (100 lines)
  - **Technology Stack Table** (20 lines) ✅
  - LLM Integration details (150 lines)
  - **Temperature Settings Table** (20 lines) ✅
  - Response Generation with 3 responders (200 lines)
  - **Production Refinements Table** (30 lines) ✅
  - Database Architecture (150 lines)
  - **Database Entities Table** (30 lines) ✅
  - Deployment (100 lines)
  - Complete code examples throughout

#### **Condensed Version (lines 158-332, ~175 lines):**
- Algorithm 1: Progressive Disclosure ✅
- Algorithm 2: Bias Detection ✅
- Brief LLM integration paragraph
- Brief data architecture paragraph
- Brief deployment paragraph
- **NO TABLES** ❌
- **NO CODE EXAMPLES** (clean, but less technical)

**What Was Lost:**
- **ALL 4 TECHNICAL TABLES:**
  1. Technology Stack (Python 3.13, Flask, Ollama, etc.)
  2. Temperature Settings by module
  3. Production refinement metrics (40% reduction in clarifications, 89% reduction in strange responses)
  4. Database entities with descriptions

- Detailed response generation strategies
- Production refinement stories (3 concrete improvements)
- Database schema explanation
- Privacy and security considerations

**Recommendation:** ⚠️ **ADD BACK SELECTIVELY:**

**MUST ADD (Critical Technical Documentation):**
1. **Technology Stack Table** - Reviewers need to know exact versions
2. **Temperature Settings Table** - Important for reproducibility

**OPTIONAL BUT RECOMMENDED:**
3. **Production Refinements Table** - Shows iterative development (good for academic rigor)

**CAN SKIP:**
4. Database entities table (already have Figure 4.X with schema diagram)

---

### **5. Example Workflow Section**

#### **Full Version (lines 1588-1867, ~280 lines):**
- Complete phase-by-phase walkthrough
- 17 interaction-by-interaction transcripts
- Each with: Student query → Intent → Response → Discovery → Note
- **Table 4.7:** Discoveries by category and timing
- Diagnosis + Reflection (full excerpts)
- Evaluation results with scores
- Educational impact analysis

#### **Condensed Version (lines 333-384, ~50 lines):**
- High-level case overview ✅
- **Phase highlights only** (3 paragraphs for 3 phases)
- Outcome and reflection (1 paragraph)
- **NO TABLE** ❌
- **NO INTERACTION TRANSCRIPTS** ✅ (moved to Appendix C - smart!)
- **NO EDUCATIONAL IMPACT ANALYSIS** ❌

**What Was Lost:**
- Table 4.7: Discoveries timeline
- Detailed interaction-by-interaction walkthrough
- Educational impact analysis (progressive disclosure effectiveness, scaffolding, bias demonstration, metacognition, system performance)

**What Was Improved:**
- ✅ Reference to Appendix C for full transcript (excellent move!)
- ✅ Much more readable high-level narrative
- ✅ Focuses on key moments not every turn

**Recommendation:** ✅ **KEEP CONDENSED APPROACH** but ADD:
1. **Table 4.7:** Discoveries by category and timing (critical empirical data, only ~15 lines)
2. **One paragraph:** Educational impact summary (scaffolding worked, bias detected, reflection showed metacognition)

**Justification:** Ana Guedes' dissertation includes similar empirical tables showing system behavior. This validates the design.

---

### **6. User Interfaces Section**

#### **Full Version (lines 1868-2040, ~170 lines):**
- Detailed description of all 4 tabs
- Bias warning display with pedagogical rationale
- Diagnosis submission with 6 prompts explained
- Evaluation results interface
- **EXTENSIVE admin dashboard:** 6 functional areas with detailed descriptions
  - Database backup rationale
  - Bias warning toggle with research justification
  - User management details
  - LLM profile configuration use cases
  - Agent prompt management with versioning
  - Recent activity logs (though this wasn't in your text, it was in your earlier version)

#### **Condensed Version (lines 385-498, ~115 lines):**
- Simulation interface with 4 tabs ✅
- Bias warning display ✅
- Diagnosis submission ✅
- Evaluation results ✅
- **SIMPLIFIED admin dashboard:** Brief mention of "users, LLM profiles, and research configurations"
- All 10 figures properly referenced ✅

**What Was Lost:**
- Research rationale for bias warning toggle (A/B testing capability)
- Detailed admin features (6 specific areas)
- Database backup importance for reproducibility
- User management cohort tracking
- LLM profile use cases (A/B testing, cost optimization)
- Prompt versioning for research traceability

**What Was Improved:**
- ✅ Much more concise
- ✅ Focuses on pedagogical design philosophy
- ✅ Less technical detail, more user experience focus

**Recommendation:** ⚠️ **MOSTLY KEEP CONDENSED** but ADD:
1. **One paragraph:** Admin dashboard capabilities listing the 6 functional areas (database backup, system config, users, LLM profiles, prompts, activity logs)
2. **One sentence:** Research rationale for bias toggle (enables A/B testing without changing case difficulty)

**Justification:** Admin functionality shows system maturity and research capability. Brief mention adds credibility without bloat.

---

### **7. Summary Section**

#### **Full Version (lines 2041-2101, ~60 lines):**
- Key Contributions (conceptual + technical) ✅
- Design Principles Validated ✅
- Addressing Prior Gaps (Chapter 3 links) ✅
- Limitations (4 specific areas) ✅
- Bridge to Chapter 5 (detailed preview) ✅

#### **Condensed Version (lines 499-552, ~55 lines):**
- Key Contributions (conceptual + technical) ✅
- Design Principles Validated ✅
- Addressing Identified Gaps ✅
- Limitations (4 specific areas) ✅
- Bridge to Chapter 5 (briefer preview) ✅

**Differences:**
- **Full version:** More detailed Chapter 5 preview with bullet points
- **Condensed version:** Shorter but still clear bridge
- Content essentially equivalent, condensed version slightly tighter

**Recommendation:** ✅ **KEEP CONDENSED VERSION** - it's cleaner and still complete

---

## 📋 Critical Elements Missing from Condensed Version

### **🔴 MUST ADD BACK (Critical):**

1. **Table: Intent Taxonomy** (from full version lines 563-596)
   - Shows 33 intents organized by phase
   - Both reference dissertations have this
   - **Add at:** After "Context Classifier" paragraph in System Design
   - **Estimated lines:** +35 lines

2. **Table: Classification Accuracy Improvements** (from full version lines 705-720)
   - Shows PMH 57% → 95% improvement
   - Empirical validation of design decisions
   - **Add at:** End of Technical Implementation section
   - **Estimated lines:** +18 lines

3. **Table: Technology Stack** (from full version lines 1019-1041)
   - Python 3.13, Flask 3.0, Ollama, Gemma 3:4b
   - Essential for reproducibility
   - **Add at:** Beginning of Technical Implementation
   - **Estimated lines:** +25 lines

### **⚠️ SHOULD ADD BACK (Highly Recommended):**

4. **Table: LLM Temperature Settings** (from full version lines 1089-1105)
   - 0.2 for intent, 0.5 for dialogue, 0.3 for evaluation
   - Critical for reproducibility
   - **Add at:** After Technology Stack table
   - **Estimated lines:** +18 lines

5. **Table: Discoveries Timeline** (from full version lines 1718-1735)
   - 18 blocks, 2 critical findings, 18 minutes
   - Validates progressive disclosure mechanism
   - **Add at:** After Example Workflow phase highlights
   - **Estimated lines:** +20 lines

6. **Paragraph: Educational Impact Analysis** (from full version lines 1843-1867)
   - Validates that scaffolding worked, bias detected, reflection occurred
   - Shows system met pedagogical objectives
   - **Add at:** After workflow outcome paragraph
   - **Estimated lines:** +25 lines

### **ℹ️ NICE TO HAVE (Optional):**

7. **Table: Production Refinements** (from full version lines 1274-1289)
   - 40% fewer clarifications, 89% fewer strange responses
   - Shows iterative development maturity
   - **Add at:** End of Technical Implementation
   - **Estimated lines:** +18 lines

8. **Paragraph: Admin Dashboard Details** (from full version lines 1951-2020)
   - 6 functional areas listed
   - Research capability emphasis
   - **Add at:** End of User Interfaces section
   - **Estimated lines:** +30 lines

---

## 📏 Recommended Hybrid Chapter Structure

### **Target Metrics:**
- **Lines:** ~750-850 (up from 552, but down from 2,101)
- **Words:** ~6,500-7,500 (down from 15,500)
- **Tables:** 5 critical tables (up from 0, down from 7)
- **Readability:** Keep condensed's paragraph structure
- **Technical Depth:** Restore key empirical evidence

### **What to Keep from Condensed:**
✅ Shorter paragraphs (3-5 sentences)
✅ Flatter hierarchy (fewer subsubsections)
✅ Algorithm pseudocode as-is
✅ Example workflow high-level narrative with Appendix C reference
✅ User interfaces concise descriptions
✅ Summary section as-is

### **What to Add from Full:**
🔴 Intent taxonomy table
🔴 Classification accuracy table
🔴 Technology stack table
⚠️ Temperature settings table
⚠️ Discoveries timeline table
⚠️ Educational impact paragraph
ℹ️ Production refinements table (optional)
ℹ️ Admin dashboard details (optional)

---

## 🎯 Priority Action Plan

### **Phase 1: Critical Tables (MUST DO)** - 2-3 hours

#### **Action 1.1: Add Intent Taxonomy Table**
**Location:** After line 106 in condensed version (after "Context Classifier" paragraph)
**Source:** Full version lines 563-596
**Why:** Both reference dissertations visualize their taxonomies
**Estimated time:** 30 minutes

#### **Action 1.2: Add Classification Accuracy Table**
**Location:** After Technical Implementation section, before Example Workflow
**Source:** Full version lines 705-720
**Why:** Empirical validation of design (57% → 95%)
**Estimated time:** 20 minutes

#### **Action 1.3: Add Technology Stack Table**
**Location:** Beginning of Technical Implementation (after line 158)
**Source:** Full version lines 1019-1041
**Why:** Reproducibility requirement
**Estimated time:** 30 minutes

### **Phase 2: Supporting Evidence (SHOULD DO)** - 2-3 hours

#### **Action 2.1: Add Temperature Settings Table**
**Location:** After Technology Stack table
**Source:** Full version lines 1089-1105
**Why:** Critical for reproducibility
**Estimated time:** 20 minutes

#### **Action 2.2: Add Discoveries Timeline Table**
**Location:** After workflow phase highlights (line 370)
**Source:** Full version lines 1718-1735
**Why:** Validates progressive disclosure
**Estimated time:** 20 minutes

#### **Action 2.3: Add Educational Impact Paragraph**
**Location:** After workflow outcome (line 382)
**Source:** Condensed from full version lines 1843-1867
**Why:** Shows system met pedagogical objectives
**Estimated time:** 30 minutes

### **Phase 3: Optional Enhancements (NICE TO HAVE)** - 1-2 hours

#### **Action 3.1: Add Production Refinements Table**
**Location:** End of Technical Implementation
**Source:** Full version lines 1274-1289
**Why:** Shows iterative development
**Estimated time:** 20 minutes

#### **Action 3.2: Add Admin Dashboard Paragraph**
**Location:** End of User Interfaces section
**Source:** Condensed from full version lines 1951-2020
**Why:** Research capability emphasis
**Estimated time:** 20 minutes

---

## 📊 Quality Comparison

### **Condensed Version Strengths:**
1. ✅ **Excellent readability** - No paragraph over 5 sentences
2. ✅ **Clear structure** - Logical flow, easy to follow
3. ✅ **Good length** - Not overwhelming, focused
4. ✅ **Algorithm placement** - Pseudocode enhances understanding
5. ✅ **Smart appendix use** - Full transcript in Appendix C

### **Condensed Version Weaknesses:**
1. ❌ **No empirical tables** - Missing quantitative validation
2. ❌ **No intent taxonomy visualization** - Just lists count
3. ❌ **Limited technical specifications** - Hard to reproduce
4. ❌ **No temperature settings** - Critical detail missing
5. ❌ **Brief admin section** - Undersells research capability

### **Full Version Strengths:**
1. ✅ **Comprehensive technical docs** - Everything needed to reproduce
2. ✅ **7 empirical tables** - Strong quantitative evidence
3. ✅ **Detailed explanations** - Every component fully described
4. ✅ **Production refinements** - Shows iterative development
5. ✅ **Complete admin features** - Research maturity

### **Full Version Weaknesses:**
1. ❌ **Too long** - 15,500 words overwhelming
2. ❌ **Dense paragraphs** - Many 6-8 sentence paragraphs
3. ❌ **Deep hierarchy** - 4 levels (subsubsection) hard to navigate
4. ❌ **Repetitive in places** - Some concepts explained multiple times
5. ❌ **Example workflow too detailed** - 280 lines excessive

---

## 🎓 Recommendation: Hybrid Approach

### **Best Strategy:**
**Start with condensed version as BASE, selectively add back critical elements from full version**

### **Rationale:**
1. **Condensed has better readability** - Matches Ana Guedes' clarity
2. **Full has better technical depth** - Matches comprehensive documentation standard
3. **Tables are essential** - Both references use them extensively
4. **Hybrid balances both** - Readable + rigorous

### **Target Quality Score:**
- Condensed alone: 8.0/10 (good readability, missing evidence)
- Full alone: 9.0/10 (comprehensive, too long)
- **Hybrid: 9.5/10** (best of both worlds)

### **Expected Result:**
- **~800 lines** (45% shorter than full, 45% longer than condensed)
- **~7,000 words** (55% reduction from full, 55% increase from condensed)
- **5 critical tables** (supports all claims)
- **Readable paragraph structure** (from condensed)
- **Complete technical documentation** (from full)

---

## 📋 Implementation Checklist

### **Phase 1: Critical Additions** (MUST DO - 2-3 hours)
- [ ] Add Intent Taxonomy Table (Table 4.1 or 4.2)
- [ ] Add Classification Accuracy Table
- [ ] Add Technology Stack Table
- [ ] Verify all table references compile
- [ ] Check table numbering sequence

### **Phase 2: Supporting Evidence** (SHOULD DO - 2-3 hours)
- [ ] Add Temperature Settings Table
- [ ] Add Discoveries Timeline Table
- [ ] Add Educational Impact paragraph
- [ ] Verify flow with new additions
- [ ] Check word count (~7,000 target)

### **Phase 3: Optional Enhancements** (NICE TO HAVE - 1-2 hours)
- [ ] Add Production Refinements Table
- [ ] Add Admin Dashboard paragraph
- [ ] Polish transitions between sections
- [ ] Final readability check

### **Phase 4: Quality Assurance** (30-60 minutes)
- [ ] Compile LaTeX successfully
- [ ] All references resolve (no "??")
- [ ] All figures display correctly
- [ ] All tables formatted consistently
- [ ] Read full chapter for flow
- [ ] Check against reference dissertations

---

## 🎯 Final Verdict

### **Question: Which version should you use?**

**Answer: Neither as-is. Use HYBRID approach.**

### **Recommended Path:**

1. **Use condensed as your base** ✅
   - Keep all the improved readability
   - Keep the cleaner structure
   - Keep the smart Appendix C reference

2. **Add back 5 critical tables** 🔴
   - Intent taxonomy (comparative analysis requirement #3)
   - Classification accuracy (empirical validation)
   - Technology stack (reproducibility)
   - Temperature settings (reproducibility)
   - Discoveries timeline (validates progressive disclosure)

3. **Add 1 critical paragraph** ⚠️
   - Educational impact analysis (validates pedagogical objectives)

4. **Optional additions** ℹ️
   - Production refinements table (shows maturity)
   - Admin dashboard details (shows research capability)

### **Total Work Required:**
- **Critical (Phase 1):** 2-3 hours
- **Important (Phase 2):** 2-3 hours
- **Optional (Phase 3):** 1-2 hours
- **Total:** 5-8 hours to create optimal hybrid

### **Expected Outcome:**
- **Quality:** 9.5/10 (competitive with best dissertations)
- **Length:** ~7,000 words (balanced)
- **Readability:** Excellent (short paragraphs)
- **Technical depth:** Complete (all evidence present)
- **Defense-ready:** ✅ Yes

---

## 📝 Specific Text to Add Back

### **1. Intent Taxonomy Table** (After line 106 in condensed)

```latex
\begin{table}[h]
\centering
\caption{Intent categories by diagnostic phase (examples abbreviated).}
\label{tab:intent_taxonomy}
\setlength{\tabcolsep}{6pt}
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{p{2.5cm} p{3.2cm} p{6.7cm} c}
\toprule
\textbf{Phase} & \textbf{Category} & \textbf{Example intents} & \textbf{Count} \\
\midrule
Anamnesis & Past Medical History &
\texttt{pmh\_general}, \texttt{pmh\_family\_history}, \texttt{pmh\_surgical\_history} & 3 \\
Anamnesis & History of Present Illness &
\texttt{hpi\_chief\_complaint}, \texttt{hpi\_onset\_duration\_primary}, \texttt{hpi\_fever}, \texttt{hpi\_chills}, \texttt{hpi\_chest\_pain}, \texttt{hpi\_weight\_changes} & 9 \\
Anamnesis & Medications &
\texttt{meds\_current\_known}, \texttt{meds\_ra\_specific\_initial\_query}, \texttt{meds\_full\_reconciliation\_query} & 3 \\
Anamnesis & Social History &
\texttt{social\_smoking}, \texttt{social\_alcohol}, \texttt{social\_occupation} & 3 \\
Exam & General / System &
\texttt{exam\_vital}, \texttt{exam\_general\_appearance}, \texttt{exam\_cardiovascular}, \texttt{exam\_respiratory} & 4 \\
Investigations & Laboratory &
\texttt{labs\_general}, \texttt{labs\_specific\_cbc}, \texttt{labs\_specific\_bnp} & 5 \\
Investigations & Imaging &
\texttt{imaging\_chest\_xray}, \texttt{imaging\_ct\_chest}, \texttt{imaging\_echo} & 6 \\
\bottomrule
\end{tabular}
\end{table}
```

### **2. Classification Accuracy Table** (Before Example Workflow section)

```latex
\begin{table}[h]
\centering
\caption{Classification accuracy improvements (pilot summary).}
\label{tab:intent_accuracy}
\setlength{\tabcolsep}{6pt}
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{lccc}
\toprule
\textbf{Configuration} & \textbf{PMH vs.\ Meds} & \textbf{Cross-phase errors} & \textbf{Overall} \\
\midrule
Baseline (generic defs.) & 57\% & 23\% & 78\% \\
+ Enhanced definitions & 95\% & 18\% & 87\% \\
+ Strict context filtering & 95\% & 0\% & 96\% \\
\bottomrule
\end{tabular}
\end{table}

\noindent
These refinements demonstrate that intent classification evolved from moderate
accuracy to production-grade reliability through iterative design and negative
example integration.
```

### **3. Technology Stack Table** (Beginning of Technical Implementation)

```latex
\begin{table}[h]
\centering
\caption{Core technologies and versions.}
\label{tab:core_stack}
\setlength{\tabcolsep}{6pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabular}{p{3.2cm} p{4.0cm} p{2.0cm}}
\toprule
\textbf{Component} & \textbf{Technology} & \textbf{Version} \\
\midrule
Backend Framework & Flask & 3.0+ \\
Language & Python & 3.13+ \\
Dependency Mgmt & Poetry & 1.8+ \\
ORM \& Migrations & SQLAlchemy + Alembic & 2.0+ \\
Data Validation & Pydantic & 2.0+ \\
LLM Interface & Ollama & Latest \\
LLM Model & Gemma 3:4b-it-q4\_K\_M & 4B params \\
Frontend & HTML/CSS/JS & ES2020+ \\
Containerisation & Docker + Compose & 24.0+ \\
Prod Server & Gunicorn & 21.0+ \\
\bottomrule
\end{tabular}
\end{table}
```

### **4. Temperature Settings Table** (After Technology Stack)

```latex
\begin{table}[h]
\centering
\caption{LLM temperature settings by module.}
\label{tab:temps}
\setlength{\tabcolsep}{8pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabular}{l c p{7cm}}
\toprule
\textbf{Module} & \textbf{Temp.} & \textbf{Rationale} \\
\midrule
Intent Classification & 0.2 & High consistency; minimal variability \\
Clinical Evaluation & 0.3 & Reproducible scoring; fairness across sessions \\
Responders (dialogue) & 0.5 & Natural family dialogue with limited variability \\
Responders (labs) & 0.3 & Deterministic, professional reporting \\
\bottomrule
\end{tabular}
\end{table}
```

### **5. Discoveries Timeline Table** (After workflow phase highlights)

```latex
\begin{table}[h]
\centering
\caption{Discoveries by category and timing.}
\label{tab:discoveries_mtb}
\begin{tabular}{lccc}
\toprule
\textbf{Category} & \textbf{Count} & \textbf{Critical Findings} & \textbf{Timeline} \\
\midrule
Presenting symptoms & 6 & None & First 2 min \\
Current medications & 3 & Infliximab & min~\(\sim 7\) \\
Physical examination & 3 & None & 7--10 min \\
Imaging & 3 & Miliary nodules; normal echo & 10--15 min \\
Diagnostic results & 3 & None & 15--18 min \\
\midrule
\textbf{Total} & \textbf{18} & \textbf{2 critical} & \textbf{18 min} \\
\bottomrule
\end{tabular}
\end{table}
```

### **6. Educational Impact Paragraph** (After workflow outcome)

```latex
\paragraph{Educational impact.}
This session demonstrates SmartDoc's pedagogical mechanisms in practice.
Progressive disclosure required 17 targeted queries to reveal 18 information blocks,
showing active inquiry rather than passive reading.
The just-in-time hint ("check previous hospital records") successfully guided
medication reconciliation after two unsuccessful attempts.
Bias detection triggered appropriately when preliminary imaging suggested heart
failure, logging an anchoring warning.
Structured reflection responses showed explicit evidence integration
(infliximab $\rightarrow$ TB risk), acknowledgement of contradictions
(normal echo vs. elevated BNP), and systematic consideration of alternatives.
Intent classification achieved 100\% accuracy (17/17 correct), while median
response latency remained under 6 seconds per turn—confirming that the system
met both technical and pedagogical objectives in this authentic diagnostic scenario.
```

---

**Status:** Ready for implementation
**Next Steps:** Follow Phase 1-3 action plan
**Expected Timeline:** 5-8 hours total work
**Final Result:** 9.5/10 quality, defense-ready Chapter 4
