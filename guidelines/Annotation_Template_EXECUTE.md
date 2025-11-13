# Stage 2: EXECUTE - Evaluation Harness Assessment Template
## Structured Evaluation Format with Coverage Analysis

---

## Evaluation Format

For each feature, you will complete this structure:

```
S2FX: [Feature Name]
Grade: [Absent/Partial/Present] (XX% coverage)
Supports: [Sub-capability 1] ✓/✗, [Sub-capability 2] ✓/✗, ...
Documentation: [Quality assessment: Minimal/Moderate/Comprehensive]
Evidence: [Specific links, code examples, or behavioral observations supporting each ✓/✗]
```

**Coverage calculation:** `number of ✓ / (number of ✓ + number of ✗)`

**Grade mapping:**
- **Absent (0-30%)**: Feature missing, non-functional, or <2 sub-capabilities present
- **Partial (30-80%)**: Feature functional for common cases with significant gaps; 2-4 sub-capabilities present
- **Present (80-100%)**: Production-ready with comprehensive support; 5+ sub-capabilities present and well-integrated

---

## Feature 1: Data Loading & Preprocessing

**Purpose:** Load evaluation dataset $D = \{(x_i, y_i, m_i)\}_{i=1}^N$ from diverse sources with format flexibility (structured: JSON, JSONL, CSV, Parquet; databases: SQL, NoSQL; repositories: HuggingFace Datasets, TensorFlow Datasets; APIs: REST, GraphQL; cloud: S3, GCS, Azure Blob). Multi-modal support: text (plain, markdown, HTML), images (JPEG, PNG, TIFF), audio (WAV, MP3, FLAC), video, structured data, combinations. Apply preprocessing transformations specified by benchmark (tokenization, normalization, augmentation, format conversion). Support streaming for large datasets exceeding memory. Reproduce exact dataset splits across runs for deterministic evaluation.

**Essential Capabilities:**
1. **Multiple format support** - Loads 5+ formats: JSON, JSONL, CSV, Parquet, database queries, APIs, cloud storage
2. **Multi-modal data support** - Handles text, images, audio, video, structured data, mixed modalities
3. **Streaming support** - Can process datasets larger than memory via streaming/batching
4. **Preprocessing pipeline** - Applies tokenization, normalization, augmentation, format conversion per benchmark spec
5. **Schema standardization** - Automatic format normalization ensuring consistent schema across sources
6. **Split reproducibility** - Exact dataset splits reproduced across runs via deterministic partitioning
7. **Data validation** - Checks dataset accessibility, version consistency, sample counts, basic integrity
8. **Preprocessing configuration** - Preprocessing parameters documented and reproducible; can disable/customize transformations

**Look for:**
- List of supported formats in documentation or code
- Multi-modal example datasets (text, image, audio combinations)
- Streaming implementation or references (e.g., iterative loading, batching)
- Preprocessing code showing tokenization, normalization, augmentation
- Data format standardization logic
- Split reproducibility mechanism (seed-based or explicit indices)
- Data validation code (type checking, accessibility, counts)
- Preprocessing configuration files or examples
- Tests demonstrating loading/preprocessing with various format combinations
- Version tracking for datasets

**Report template:**
```
S2F1: Data Loading & Preprocessing
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Multiple format support ✓/✗
  - Multi-modal data support ✓/✗
  - Streaming support ✓/✗
  - Preprocessing pipeline ✓/✗
  - Schema standardization ✓/✗
  - Split reproducibility ✓/✗
  - Data validation ✓/✗
  - Preprocessing configuration ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to format list, multi-modal examples, streaming code, preprocessing pipeline, reproducibility mechanism]
```

---

## Feature 2: Schema Validation & Consistency

**Purpose:** Enforce dataset schema ensuring structural correctness BEFORE expensive inference. Type checking (field types match specification), structure validation (required fields present, nested structures correct), statistical property verification (value ranges reasonable, distributions match expectations, null patterns acceptable, cardinality constraints satisfied). Validate training-serving consistency critical for fairness evaluation—same preprocessing pipeline, same feature engineering, same data representation. Track schema evolution, enforce backward compatibility. Flag schema drift that could invalidate measurement comparisons or violate benchmark assumptions.

**Essential Capabilities:**
1. **Type checking** - Validates all fields have correct types (strings, integers, floats, objects, arrays)
2. **Structure validation** - Checks required fields present, nested structures correct, no extra unvalidated fields
3. **Range/bound checking** - Validates numerical values in expected ranges, categorical values from valid sets
4. **Null/missing handling** - Acceptable null patterns documented and enforced (which fields can be null?)
5. **Cardinality constraints** - Validates field cardinality (e.g., labels from finite set, IDs unique where required)
6. **Training-serving consistency** - Same preprocessing pipeline applied; feature engineering identical; data representation matches
7. **Schema evolution tracking** - Detects and reports schema changes across benchmark versions
8. **Drift detection** - Flags distribution shifts or schema changes that could invalidate comparisons

**Look for:**
- Schema specification files (JSON Schema, Protobuf, Pydantic models, dataclass definitions)
- Type checking code with error messages for mismatches
- Required field validation
- Range/bound checking examples
- Null/missing value handling specification
- Training-serving consistency check code or documentation
- Schema versioning mechanism
- Distribution drift detection (statistical tests or heuristics)
- Test cases showing schema validation failures and error handling
- Integration with data loading (validation before preprocessing)

**Report template:**
```
S2F2: Schema Validation & Consistency
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Type checking ✓/✗
  - Structure validation ✓/✗
  - Range/bound checking ✓/✗
  - Null/missing handling ✓/✗
  - Cardinality constraints ✓/✗
  - Training-serving consistency ✓/✗
  - Schema evolution tracking ✓/✗
  - Drift detection ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to schema specs, type checking code, training-serving consistency code, drift detection examples]
```

---

## Feature 3: Pipeline Orchestration

**Purpose:** Coordinate evaluation workflow through directed acyclic graph (DAG) based dependency management. Define task dependencies (which tasks must complete before others), enable parallel execution where tasks independent. Route task execution by type with specialized handlers: question-answering (extract question/context, format prompt, parse answer), summarization (apply length constraints, format requirements), classification (handle label spaces, multi-class vs multi-label), generation (apply length limits, sampling strategies). Apply multiple evaluation protocols with conditional branching: zero-shot (no examples), few-shot (select/format examples), chain-of-thought (reasoning prompt engineering), variations testing (robustness to perturbations). Manage task batching for efficiency, implement dynamic load balancing. Capture complete execution order for debugging/reproducibility.

**Essential Capabilities:**
1. **DAG-based dependency management** - Task dependencies formalized; parallel execution where independent
2. **Task type routing** - Specialized handlers for QA, summarization, classification, generation, custom tasks
3. **Protocol variations** - Supports zero-shot, few-shot, chain-of-thought, prompt variations, perturbation testing
4. **Few-shot example handling** - Selects, formats, and manages examples for few-shot protocols
5. **Prompt templating** - Flexible prompt templates with variable substitution, formatting options
6. **Task batching** - Efficient grouping of tasks; configurable batch sizes; dynamic batching by input length
7. **Dynamic load balancing** - Distributes task execution across compute resources; load-aware scheduling
8. **Execution order tracking** - Complete record of task order, dependencies, completion status for debugging/reproducibility

**Look for:**
- DAG definition and visualization (e.g., Airflow, Prefect, or custom DAG implementation)
- Task dependency specification examples
- Parallel execution demonstration (tasks running concurrently)
- Task type handler implementations (QA, summarization, classification, generation)
- Protocol variation examples (zero-shot, few-shot, CoT configs)
- Few-shot example selection and formatting code
- Prompt template system with variable substitution
- Batching logic with dynamic sizing
- Load balancing implementation or documentation
- Execution trace/logs showing task order and completion
- Test cases showing DAG execution and dependency correctness

**Report template:**
```
S2F3: Pipeline Orchestration
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - DAG-based dependency management ✓/✗
  - Task type routing ✓/✗
  - Protocol variations ✓/✗
  - Few-shot example handling ✓/✗
  - Prompt templating ✓/✗
  - Task batching ✓/✗
  - Dynamic load balancing ✓/✗
  - Execution order tracking ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to DAG examples, task handlers, protocol configs, batching code, execution traces]
```

---

## Feature 4: Inference Execution

**Purpose:** Execute model $f_\theta$ on dataset $D$ with prompts $P$ and configuration $\Lambda$ to generate outputs: $f_\theta(D; P, \Lambda) \rightarrow O = \{o_i\}_{i=1}^N$. Implement efficient batching strategies (dynamic batch sizing based on input length/memory; static batching for uniform inputs). Apply rate limiting for API compliance (requests/second limits, concurrent request limits, exponential backoff on errors). Timeout handling (per-sample, global, graceful degradation). Capture comprehensive generation metadata: latency per sample, token counts for cost tracking, API errors/retries, truncation events. Respect model-specific constraints: context window limits, modality support, API versioning.

**Essential Capabilities:**
1. **Batch processing** - Dynamic or static batching; configurable batch sizes; memory-aware batching
2. **Rate limiting** - Respects API rate limits; requests/second throttling; concurrent request limits; exponential backoff
3. **Timeout handling** - Per-sample timeouts; global evaluation timeout; graceful degradation on timeout
4. **Metadata capture** - Records latency (wall-clock, GPU time), token counts (input, output, total), API errors, retries
5. **Error handling** - Captures detailed error diagnostics; distinguishes transient vs permanent failures
6. **Context window management** - Handles model context limits; truncates or splits long inputs; reports truncation
7. **Model constraint respect** - Verifies modality support; checks API version compatibility; respects generation limits
8. **Generation configuration** - Applies inference parameters (temperature, top_p, top_k, max_tokens, stop sequences, sampling strategy)

**Look for:**
- Batching implementation with batch size configuration
- Rate limiting code with configurable limits
- Exponential backoff implementation for retries
- Timeout handling with graceful degradation
- Metadata capture code recording latency, tokens, errors
- Error classification (transient vs permanent)
- Context window handling code
- Model constraint validation
- Generation parameter application code
- API version/deprecation handling
- Test cases showing batch execution, rate limiting, timeouts
- Performance benchmarks (throughput, latency)

**Report template:**
```
S2F4: Inference Execution
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Batch processing ✓/✗
  - Rate limiting ✓/✗
  - Timeout handling ✓/✗
  - Metadata capture ✓/✗
  - Error handling ✓/✗
  - Context window management ✓/✗
  - Model constraint respect ✓/✗
  - Generation configuration ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to batching code, rate limiting impl, timeout handling, metadata capture, error classification]
```

---

## Feature 5: Error Recovery & Resilience

**Purpose:** Handle execution disruptions ensuring evaluation completion despite failures. Automatic retry logic with exponential backoff (wait times: 1s, 2s, 4s, 8s, ...), configurable maximum retry attempts, configurable timeouts, circuit breakers with fallback strategies (pause and alert after N consecutive failures). Implement graceful degradation—continue evaluation on remaining samples when individual samples fail; mark failed samples for investigation. Capture detailed error diagnostics for root cause analysis: error types (API errors, timeouts, parsing, OOM), frequencies/patterns, failure correlation with input characteristics, stack traces/context. Distinguish recoverable errors (transient API failures) from unrecoverable (malformed inputs, incompatibility). Prevent silent failures—all errors logged and aggregated.

**Essential Capabilities:**
1. **Automatic retry logic** - Exponential backoff with configurable wait times and max attempts
2. **Retry strategy configuration** - Different strategies for different error types; per-error-type retry budgets
3. **Circuit breaker pattern** - Pauses and alerts after N consecutive failures; prevents cascading failures
4. **Timeout configuration** - Per-sample, per-batch, and global timeout options with graceful handling
5. **Error classification** - Distinguishes transient (recoverable) from permanent (unrecoverable) errors
6. **Graceful degradation** - Continues evaluation on remaining samples; marks failed samples
7. **Error aggregation** - Comprehensive error logs with counts, patterns, stack traces, execution context
8. **Failure correlation analysis** - Analyzes whether failures correlate with input characteristics (length, complexity)

**Look for:**
- Retry logic implementation with exponential backoff code
- Retry configuration examples (attempts, backoff timing, per-error-type budgets)
- Circuit breaker implementation or documentation
- Timeout specification and handling
- Error type classification logic (transient vs permanent)
- Graceful degradation code (continue on failure)
- Error logging and aggregation code
- Root cause analysis utilities
- Correlation analysis between failures and input properties
- Test cases showing retry behavior, circuit breaking, graceful degradation
- Error report examples with statistics and patterns

**Report template:**
```
S2F5: Error Recovery & Resilience
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Automatic retry logic ✓/✗
  - Retry strategy configuration ✓/✗
  - Circuit breaker pattern ✓/✗
  - Timeout configuration ✓/✗
  - Error classification ✓/✗
  - Graceful degradation ✓/✗
  - Error aggregation ✓/✗
  - Failure correlation analysis ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to retry code, circuit breaker impl, timeout handling, error classification, correlation analysis]
```

---

## Feature 6: Execution Checkpointing

**Purpose:** Enable recovery from interruptions through automatic state persistence at configurable intervals. Checkpoint frequency specification (every N samples, every M minutes, on-demand), complete execution state preservation (results generated so far, RNG state for reproducibility, data cursor position for resumption, partial batch state, execution metadata). Support incremental resumption without recomputation—restart from last checkpoint, skip completed work, continue with remaining samples. Essential for long-running evaluations: large datasets (millions of samples), expensive models (slow inference, high cost), unreliable infrastructure (spot instances, preemption). Maintain reproducibility—resumed runs produce identical results to uninterrupted runs given same seed. Checkpoint storage with compression and integrity verification.

**Essential Capabilities:**
1. **Checkpoint frequency control** - Configurable frequency: every N samples, every M minutes, on-demand triggering
2. **Complete state preservation** - Results so far, RNG state, data cursor position, partial batch state, metadata
3. **Incremental resumption** - Restart from checkpoint, skip completed work, continue with remaining samples
4. **Reproducibility guarantee** - Resumed runs produce identical results given same seed
5. **Checkpoint storage** - Persistent storage with compression options and integrity verification (checksums)
6. **State serialization** - Robust serialization of complex state (tensors, random states, iterators)
7. **Recovery mechanism** - Automatic detection and recovery from checkpoint on restart
8. **Resumption transparency** - Results identical whether run interrupted/resumed or run uninterrupted

**Look for:**
- Checkpoint frequency configuration examples
- State serialization code (how RNG state, data cursor, results are saved)
- Resumption logic implementation
- Checkpoint storage mechanism (local/cloud filesystem)
- Compression and checksum code
- Test cases showing checkpoint/resume behavior
- Reproducibility verification (interrupted vs uninterrupted runs produce same results)
- Performance metrics on checkpointing overhead
- Recovery mechanism for corrupted/missing checkpoints
- Documentation of checkpoint format and compatibility

**Report template:**
```
S2F6: Execution Checkpointing
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Checkpoint frequency control ✓/✗
  - Complete state preservation ✓/✗
  - Incremental resumption ✓/✗
  - Reproducibility guarantee ✓/✗
  - Checkpoint storage ✓/✗
  - State serialization ✓/✗
  - Recovery mechanism ✓/✗
  - Resumption transparency ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to checkpoint config, state serialization code, resumption logic, reproducibility tests]
```

---

## Feature 7: Contamination Detection

**Purpose:** Monitor for data leakage during execution that would invalidate comparative conclusions. Verify held-out sets remain isolated (test set never used for training/hyperparameter tuning, validation set not leaked). Implement benchmark material detection in model training data using exact match detection via hashing (SHA-256 of samples vs training data manifest), fuzzy matching for near-duplicates (MinHash, Jaccard similarity), n-gram overlap analysis. Track whether model has seen evaluation samples: query model provenance for training data sources, check public dataset inclusion (Common Crawl, C4, Wikipedia, GitHub), analyze model behavior on held-out vs previously-seen samples. Alert on contamination with confidence levels: high (exact match found), medium (high similarity), low (suspicious patterns). Maintain contamination logs. Support ongoing monitoring.

**Essential Capabilities:**
1. **Held-out set isolation** - Verification that test/validation sets never used for training/tuning
2. **Exact match detection** - SHA-256 hashing of samples compared against training data manifest
3. **Fuzzy matching** - Near-duplicate detection via MinHash, Jaccard similarity, locality-sensitive hashing
4. **N-gram analysis** - Overlap detection at token/phrase level for paraphrase detection
5. **Model provenance tracking** - Queries model sources for training data information
6. **Public dataset checking** - Checks if evaluation data included in Common Crawl, C4, Wikipedia, GitHub, other public sources
7. **Behavior analysis** - Compares model behavior on held-out vs previously-seen samples for leakage indicators
8. **Confidence-based alerting** - Classifies contamination risk: high/medium/low confidence with evidence

**Look for:**
- Held-out set tracking and isolation code
- Exact match detection implementation (hashing, comparison)
- Fuzzy matching implementation (MinHash, Jaccard, LSH)
- N-gram overlap analysis code
- Model provenance querying (API calls to model documentation, training data disclosure)
- Public dataset checking (Common Crawl, C4, etc.)
- Behavior comparison analysis (performance on contaminated vs clean samples)
- Contamination logging with confidence levels
- Test cases showing contamination detection
- Documentation of contamination detection methodology
- Reporting of contamination results and confidence

**Report template:**
```
S2F7: Contamination Detection
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Held-out set isolation ✓/✗
  - Exact match detection ✓/✗
  - Fuzzy matching ✓/✗
  - N-gram analysis ✓/✗
  - Model provenance tracking ✓/✗
  - Public dataset checking ✓/✗
  - Behavior analysis ✓/✗
  - Confidence-based alerting ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to isolation code, exact match impl, fuzzy matching, provenance tracking, public dataset checking]
```

