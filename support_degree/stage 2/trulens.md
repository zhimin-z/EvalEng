# TruLens (truera__trulens) - Stage 2 (PREPARE) Evaluation

## Summary
TruLens is primarily an evaluation and observability framework for LLM applications, not a data preparation or dataset evaluation framework. It focuses on tracing app execution, computing feedback metrics, and visualizing results. Most Stage 2 (PREPARE) features are absent or minimal because they fall outside the framework's core mission. The framework assumes users bring pre-prepared data/apps and provides tools to evaluate them, rather than tools to prepare evaluation artifacts themselves.

---

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 0 | No preprocessing utilities found. Framework expects users to provide ready-to-use datasets/apps. No loaders, caching, or splitting mechanisms for evaluation data. |
| S2F2: Quality Assessment | 0 | No dataset quality tools. Framework focuses on app output quality (via feedback functions), not input dataset quality assessment. |
| S2F3: PII Detection | 0 | PII detection entirely absent. `database_redact_keys=True` flag exists for database storage (redacting API keys in stored records), but no PII detection/anonymization for evaluation data. Evidence: `src/core/trulens/core/session.py` shows `database_redact_keys` only affects DB writes, not data processing. |
| S2F4: Infrastructure Building | 1 | Minimal support. Users can create indices (e.g., FAISS via LlamaIndex) outside TruLens, then wrap apps. Framework provides no index-building utilities itself. Evidence: Examples like `examples/expositional/vector_stores/faiss/` show external FAISS setup. |
| S2F5: Model Validation | 0 | No model artifact validation. Framework wraps pre-loaded models/apps and traces their execution. No checksum verification, version checks, or integrity validation. |
| S2F6: Scenario Generation | 1 | Basic test set generation via `GenerateTestSet` (experimental). Generates question categories and prompts from an app callable. No multi-turn dialogues, edge cases, or reproducibility controls. Evidence: `examples/experimental/generate_test_set.ipynb` shows limited breadth/depth parameters. |
| S2F7: Red-Teaming | 0 | No red-teaming features. Framework evaluates app responses but doesn't generate adversarial inputs. Users must provide jailbreak attempts manually. |
| S2F8: Contamination Detection | 0 | No contamination detection. Framework has no corpus comparison or n-gram overlap tools. |

---

## Detailed Analysis

### S2F1: Dataset Preprocessing and Physical Partitioning
Rating: 0/3

Evidence:
- No data loaders: Search across `src/` reveals no dataset loading utilities. Users must provide data as DataFrames or manual inputs.
  ```python
  # examples/experimental/web-search-agent-evaluation-snowflake-evals.ipynb:1238
  queries_df = pd.DataFrame({"query": queries})
  ```
  Users create DataFrames themselves; no TruLens helpers.

- No preprocessing pipelines: Framework provides feedback functions (e.g., `openai.relevance`) to evaluate outputs, not preprocess inputs. No tokenization, normalization, or augmentation tools.

- No physical splitting: Records are ingested individually via `add_record()` or batch via `run.start(input_df=...)`. No train/val/test split utilities.
  ```python
  # src/core/trulens/core/app/base.py:1067
  def add_record(self, record: Record, ...) -> Record:
      """Add the given record to the database."""
  ```

- No caching: Framework traces app execution in real-time. No dataset caching layer.

Conclusion: TruLens is not a data preparation framework. Users must handle all preprocessing externally (e.g., using Pandas, LangChain loaders).

---

### S2F2: Dataset Quality and Bias Assessment
Rating: 0/3

Evidence:
- No label quality tools: Framework evaluates app outputs (e.g., groundedness, relevance), not dataset labels.
  ```python
  # examples/experimental/generate_test_set.ipynb:156
  f_qa_relevance = Feedback(openai.relevance).on_input_output()
  ```
  This checks if an app's output is relevant to its input, not if a dataset's labels are correct.

- No demographic analysis: No utilities to compute demographic distributions or identify underrepresented groups in datasets.

- No duplicate detection: Framework has no text similarity or semantic matching tools for datasets.

- No bias detection in data: Feedback functions detect bias in app responses (e.g., via custom metrics), not in input datasets.

Conclusion: Framework assumes datasets are pre-validated. Quality assessment focuses on app behavior, not data quality.

---

### S2F3: PII Detection and Anonymization
Rating: 0/3

Evidence:
- Database redaction only: The `database_redact_keys` flag redacts API keys in stored records, not PII in data.
  ```python
  # src/core/trulens/core/session.py:75
  database_redact_keys: bool = False
  """Redact secrets before writing to database."""
  ```
  This affects storage (e.g., removing `OPENAI_API_KEY` from JSON), not data processing.

- No PII detection: Search for "PII", "anonymize", "redact" in `src/` yields only DB-related code. No regex, NER, or hybrid detection.

- No audit trails: No logging of detected/handled PII in evaluation data.

Conclusion: Framework prioritizes observability (tracing apps), not data privacy tools. Users must handle PII externally.

---

### S2F4: Task-Specific Infrastructure Building
Rating: 1/3

Evidence:
- No index builders: Framework wraps existing apps (e.g., LlamaIndex with FAISS). Users create indices outside TruLens:
  ```python
  # examples/expositional/vector_stores/faiss/TruLens_with_FAISS.ipynb
  from llama_index.vector_stores.faiss import FaissVectorStore
  faiss_index = faiss.IndexFlatL2(d)
  vector_store = FaissVectorStore(faiss_index=faiss_index)
  ```
  TruLens then wraps the query engine for tracing, but doesn't build the index.

- No database setup utilities: Framework stores traces in SQLite/Postgres/Snowflake but doesn't help users set up knowledge bases for RAG apps.

- Artifact management via Snowflake: The Snowflake connector (`src/connectors/snowflake/`) stores traces in Snowflake, but this is for results, not for managing retrieval indices or app artifacts.

Justification for 1 point: Framework integrates with tools that build infrastructure (LlamaIndex, LangChain) and can trace their usage, but provides no infrastructure-building utilities itself. Minimal support via integration only.

---

### S2F5: Model Artifact Validation
Rating: 0/3

Evidence:
- No checksum validation: Framework wraps pre-loaded models (e.g., OpenAI API, HuggingFace) and traces their calls. No cryptographic verification.
  ```python
  # src/providers/openai/provider.py:75
  class OpenAI(Provider):
      model_engine: str = "gpt-3.5-turbo"
  ```
  Model name specified as string; no validation of model integrity.

- No version compatibility checks: Framework has `app_version` metadata but no enforcement:
  ```python
  # examples/experimental/web-search-agent-evaluation-snowflake-evals.ipynb:1205
  APP_VERSION = "V1"
  ```
  This is a user-defined label, not a compatibility check.

- No corruption detection: Framework assumes models/apps are functional when provided.

Conclusion: Framework focuses on tracing model usage, not validating model artifacts.

---

### S2F6: Evaluation Scenario Generation
Rating: 1/3

Evidence:
- Basic generation exists: `GenerateTestSet` class generates question categories and prompts:
  ```python
  # examples/experimental/generate_test_set.ipynb:45
  test = GenerateTestSet(app_callable=rag_chain.invoke)
  test_set = test.generate_test_set(test_breadth=3, test_depth=2)
  ```
  Generates categories (breadth) and prompts per category (depth).

- No multi-turn support: Only single-turn prompts generated. No conversation state or branching.

- No edge cases: No adversarial, boundary, or stress test generation.

- No reproducibility controls: No seed-based determinism mentioned in docs.

- Experimental feature: Marked as "experimental" in `src/benchmark/trulens/benchmark/generate/` (see `src/benchmark/README.md`).

Justification for 1 point: Feature exists but is minimal and experimental. No advanced scenario capabilities.

---

### S2F7: Red-Teaming and Adversarial Test Generation
Rating: 0/3

Evidence:
- No red-teaming tools: Search for "jailbreak", "adversarial", "red-team" in `src/` yields no results (except general mentions in docs).

- Manual adversarial testing: Users can create custom feedback functions to check for safety issues, but must provide adversarial inputs themselves:
  ```python
  # examples/quickstart/all_tools.ipynb (hypothetical)
  f_harmfulness = Feedback(openai.harmfulness).on_output()
  ```
  Framework evaluates responses but doesn't generate adversarial prompts.

- No attack libraries: No pre-built jailbreak attempts or injection tests.

Conclusion: Framework is a passive evaluator. It measures app behavior but doesn't actively probe for vulnerabilities.

---

### S2F8: Data Contamination Detection
Rating: 0/3

Evidence:
- No corpus comparison: Framework has no utilities to compare evaluation data against training corpora.

- No n-gram overlap: No text similarity or fingerprinting tools.

- No semantic similarity checks: While feedback functions compute embeddings (e.g., for relevance), they're not designed for contamination detection.

Conclusion: Contamination detection is outside the framework's scope. Users must handle this externally.

---

## Summary of Strengths and Weaknesses

### Strengths
1. Clear focus: Framework excels at app evaluation (tracing, feedback, visualization), not data preparation.
2. Extensibility: Users can create custom feedback functions for domain-specific quality checks (e.g., bias detection in outputs).
3. Integration: Works with existing tools (LangChain, LlamaIndex) that handle infrastructure.

### Weaknesses
1. No data preparation tools: Users must preprocess, split, and validate datasets externally.
2. No privacy features: PII detection absent; only API key redaction for stored traces.
3. Minimal scenario generation: Basic test set generation (experimental) lacks reproducibility and edge case support.
4. No adversarial testing: Framework evaluates app responses but doesn't generate adversarial inputs.

---

## Recommendations for Improvement

1. Add dataset loaders (S2F1): Integrate with HuggingFace Datasets or provide utilities to load/cache common benchmarks (MMLU, TruthfulQA).
2. Provide quality checks (S2F2): Add utilities to detect duplicates, check label consistency, or compute demographic distributions in datasets.
3. Integrate PII detection (S2F3): Partner with libraries like Presidio or build regex-based detectors for common PII types.
4. Expand scenario generation (S2F6): Add multi-turn dialogue support, edge case generators (long inputs, special chars), and seed-based reproducibility.
5. Red-teaming support (S2F7): Provide a library of adversarial prompts (jailbreaks, injections) or integrate with tools like Garak.

---

## Final Notes

TruLens is not designed for Stage 2 (PREPARE) tasks. It assumes users have pre-prepared apps and datasets and focuses on Stage 3 (EXECUTE) and Stage 4 (EVALUATE) instead. The low ratings reflect this design choice, not poor execution within the framework's intended scope. For data preparation, users should use complementary tools (Pandas, HuggingFace Datasets, custom scripts) before feeding data to TruLens for evaluation.