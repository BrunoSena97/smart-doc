# 4.2.2 Technology Stack and LLM Integration

Given the critical role of language models in SmartDoc and the variability inherent in LLM behavior, the system employs a carefully designed abstraction architecture to remain model-agnostic while ensuring reproducibility and educational reliability.

## Core Technology Stack

SmartDoc was implemented on a lightweight and modular technology stack focused on reproducibility, portability, and ease of deployment for educational settings.

**Table 4.3: Core Technologies and Versions**

| Component             | Technology              | Version       | Rationale                                                           |
| --------------------- | ----------------------- | ------------- | ------------------------------------------------------------------- |
| Backend Framework     | Flask                   | 3.0+          | Lightweight, flexible routing, excellent for educational prototypes |
| Language              | Python                  | 3.13+         | Ecosystem maturity, AI/ML library support                           |
| Dependency Management | Poetry                  | 1.8+          | Reproducible environments, lockfile-based versioning                |
| ORM & Database        | SQLAlchemy + Alembic    | 2.0+          | Database-agnostic, migration support, research portability          |
| Data Validation       | Pydantic                | 2.0+          | Type-safe schemas, automatic validation, JSON serialization         |
| LLM Interface         | Ollama                  | Latest        | Local model hosting, no external API dependencies                   |
| LLM Model             | Gemma 3:4b-it-q4_K_M    | 4B parameters | Balance of quality, speed, and resource requirements                |
| Frontend              | HTML/CSS/JavaScript     | ES2020+       | No build step, static serving, maximum compatibility                |
| Containerization      | Docker + Docker Compose | 24.0+         | Reproducible deployments, environment isolation                     |
| Production Server     | Gunicorn                | 21.0+         | WSGI serving, concurrent request handling                           |

## LLM Provider Abstraction

All language model interactions are mediated through a standardized `LLMProvider` interface with a single `generate()` function. This design:

- **Decouples pedagogical logic** from vendor-specific implementations, allowing the educational architecture to evolve independently of model choices.
- **Enables diverse deployment contexts**: local models for research reproducibility and data privacy, cloud-based models for production scale.
- **Supports model substitution** as the field evolves, a key concern raised in Chapter 3 regarding sustainability of AI-powered educational systems.

Example provider interface:

```python
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
```

Concrete implementations exist for:

- **OllamaProvider** — local model hosting via Ollama
- **OpenAIProvider** — cloud API for GPT models
- **AnthropicProvider** — cloud API for Claude models
- **MockProvider** — deterministic responses for testing

## Model Selection and Benchmarking

Several open-source models were evaluated to determine the optimal balance of generation quality, inference speed, structured output reliability, and resource requirements:

**Candidates evaluated:**

- `llama3.1:8b`, `llama3.2:latest`
- `gemma3:4b-it-q4_K_M`, `gemma2:9b`
- `qwen2.5:7b`, `qwen2.5:14b`
- `deepseek-r1:7b`

Evaluation criteria:

1. **Structured output consistency** — ability to reliably produce valid JSON
2. **Clinical reasoning quality** — appropriateness of diagnostic inferences
3. **Inference latency** — response time for typical prompts
4. **Portuguese language support** — though SmartDoc is English-focused, multilingual capability was considered for future localization

The model `gemma3:4b-it-q4_K_M` was ultimately selected for all core reasoning tasks including intent classification, response generation, bias analysis, and clinical evaluation. It demonstrated the best tradeoff between generation quality (clear, clinically appropriate language), runtime performance (<2s for typical inferences), and structured output reliability (>95% valid JSON on first attempt).

The 4-bit quantization (`q4_K_M`) reduces memory requirements to ~3GB while maintaining acceptable output quality, enabling deployment on consumer-grade hardware without dedicated GPU infrastructure.

## Temperature Configuration by Module

Different modules require different levels of determinism versus creativity. SmartDoc employs module-specific temperature settings to optimize each component's behavior:

**Table 4.4: LLM Temperature Settings by Module**

| Module                 | Temperature | Rationale                                                                 |
| ---------------------- | ----------- | ------------------------------------------------------------------------- |
| Intent Classification  | 0.3         | Consistency and reliability; same query should yield same intent          |
| Clinical Evaluation    | 0.3         | Reproducible scoring; similar performance should receive similar grades   |
| Bias Analysis          | 0.3         | Reliable pattern detection; consistent identification of reasoning errors |
| AnamnesisSonResponder  | 0.5         | Natural family dialogue with some variability, but maintains consistency  |
| LabsResidentResponder  | 0.3         | Professional, deterministic medical reporting                             |
| ExamObjectiveResponder | 0.3         | Standardized clinical examination findings                                |
| Node Summarization     | 0.4         | Stylistic variation while preserving clinical accuracy                    |

This fine-grained control addresses a key finding from Chapter 3: AI-powered educational systems must balance naturalness with reproducibility. Lower temperatures ensure fairness in assessment and consistent pedagogical behavior, while moderate temperatures in dialogue generation maintain engagement without compromising educational goals.

## Structured Output Parsing and Validation

SmartDoc requires structured outputs (JSON) from most LLM operations to enable programmatic processing. However, open-source models hosted locally do not support strict schema enforcement (unlike commercial APIs with function calling). Consequently, a dedicated post-processing and validation pipeline was implemented:

### Parsing Pipeline

**1. Direct JSON Parsing Attempt**

The raw model output is first parsed directly as JSON. If successful, no further processing is required.

**2. Regex Pre-Extraction**

If parsing fails, regular expressions extract the most probable JSON block from the text, compensating for common model behaviors such as:

- Extraneous explanations before or after the JSON
- Incomplete bracket closure
- Embedded code fence markers (`json ... `)

Example extraction pattern:

```python
json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
matches = re.findall(json_pattern, raw_output, re.DOTALL)
```

**3. Pydantic Schema Validation**

Extracted data is validated against task-specific Pydantic schemas:

```python
class IntentClassification(BaseModel):
    intent_id: str
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str

# Validation
try:
    result = IntentClassification.model_validate_json(json_text)
except ValidationError as e:
    # Proceed to retry mechanism
```

**4. Retry Mechanism**

If any preceding step fails, the system automatically re-queries the model with identical inputs. This can occur up to 4 times before triggering fallback mechanisms. Retries often succeed because of the stochastic nature of LLM generation.

**5. Fallback Mechanisms**

When all parsing and recovery attempts fail, the system implements conservative fallbacks to maintain session stability and clinical safety:

- **Intent classification** — falls back to keyword matching against a curated dictionary
- **Response generation** — uses deterministic templates based on information block content
- **Bias analysis** — relies on rule-based heuristics only
- **Clinical evaluation** — returns placeholder scores with "unable to evaluate" justification

These fallbacks ensure that LLM unreliability does not compromise the educational experience, a critical design principle for high-stakes learning environments.

## Dependency Injection for Testing and Flexibility

Rather than hardcoding model usage, LLM providers are injected into each component through constructor parameters:

```python
class IntentClassifier:
    def __init__(self, provider: LLMProvider, temperature: float = 0.3):
        self.provider = provider
        self.temperature = temperature

    def classify(self, query: str, available_intents: List[Intent]) -> Classification:
        prompt = self._build_prompt(query, available_intents)
        response = self.provider.generate(prompt, temperature=self.temperature)
        return self._parse_response(response)
```

This enables:

- **Isolated unit testing** with mock providers that return predetermined responses
- **Configuration flexibility** tailored to educational scenarios (fast models for classification, more capable models for complex reasoning)
- **Consistent software engineering practices** that ensure reliability and maintainability

## Prompt Engineering and Modularity

All prompts are modular and externally configurable, stored as template strings with variable substitution. This allows experimentation without modifying code:

```python
INTENT_CLASSIFICATION_PROMPT = """
You are a clinical reasoning assistant. Classify the doctor's query into the most appropriate clinical intent.

Context: {diagnostic_phase}
Query: "{user_query}"

Available intents:
{intent_definitions}

Return JSON: {"intent_id": "...", "confidence": 0.0-1.0, "explanation": "..."}
"""
```

Each prompt defines:

- **Role** — the perspective the LLM should adopt (e.g., "clinical reasoning assistant")
- **Context** — current state (diagnostic phase, revealed information, hypothesis status)
- **Task** — specific objective (classify intent, generate response, detect bias)
- **Output format** — required structure (JSON schema, specific fields)
- **Constraints** — behavioral rules (clinical appropriateness, language level)

This structure supports A/B testing of pedagogical strategies (e.g., different ways of framing reflection questions), linking directly to the literature's call for rigorous evaluation of design choices.

## Robustness and Validation

Robustness is ensured through comprehensive testing that simulates diverse model behaviors:

- **Normal responses** — typical, well-formatted outputs
- **Malformed JSON** — incomplete brackets, extra text, formatting errors
- **Timeouts** — slow inference or unavailable services
- **Unexpected content** — outputs that don't match expected schemas
- **Empty responses** — model returns nothing

Each failure mode triggers specific recovery strategies, ensuring graceful degradation rather than system failure. This directly addresses concerns in Chapter 3 regarding reproducibility and reliability of AI-powered virtual patient systems.

The combination of provider abstraction, temperature control, structured validation, retry mechanisms, and comprehensive fallbacks creates a robust LLM integration architecture that balances educational quality with technical reliability.
