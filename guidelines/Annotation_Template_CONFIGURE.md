# Stage 1: CONFIGURE - Evaluation Harness Assessment Template
## Structured Evaluation Format with Coverage Analysis

---

## Evaluation Format

For each feature, you will complete this structure:

```
S1FX: [Feature Name]
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

## Feature 1: Benchmark Loading & Validation

**Purpose:** Harness must accept construct-valid benchmark specifications as input without establishing validity itself. Benchmark $B = (C, D, P, \mu, R_{ref})$ includes: construct definition $C$, dataset $D$, prompt specification $P$, measurement protocol $\mu$, and validity evidence $R_{ref}$ (sampling rationale, known limitations, confound analyses).

**Essential Capabilities:**
1. **Multiple format support** - Loads benchmarks from diverse sources (JSON, YAML, CSV, database queries, HuggingFace Datasets, REST APIs, cloud storage)
2. **Completeness validation** - Verifies all components of $B$ present before use; explicit error on missing fields
3. **Construct preservation** - Stores and preserves $C$ (phenomenon definition, scope, exclusions) throughout evaluation lifecycle
4. **Validity evidence retention** - Preserves $R_{ref}$ (sampling rationale, known limitations, confound analyses) accessible in final reports
5. **Multi-benchmark support** - Enables loading and evaluating on multiple benchmarks $\{B_j\}$ in single harness run
6. **Integrity verification** - Implements checksums or version hashing to detect data corruption/drift
7. **Clear validation errors** - Provides actionable error messages identifying which components failed validation
8. **Version consistency** - Maintains benchmark versions across runs for reproducibility

**Look for:**
- Benchmark specification documentation or code showing structure $B = (C, D, P, \mu, R_{ref})$
- Example benchmark files or configuration templates in multiple formats
- Validation code that explicitly checks component presence
- Error messages from failed validation attempts (screenshots/logs)
- Examples or tests demonstrating multi-benchmark loading
- Version tracking mechanism (e.g., checksums, version tags, metadata)
- Code showing how construct definition $C$ is preserved/stored
- Evidence that validity evidence $R_{ref}$ is integrated into output/reports

**Report template:**
```
S1F1: Benchmark Loading & Validation
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Multiple format support ✓/✗
  - Completeness validation ✓/✗
  - Construct preservation ✓/✗
  - Validity evidence retention ✓/✗
  - Multi-benchmark support ✓/✗
  - Integrity verification ✓/✗
  - Clear validation errors ✓/✗
  - Version consistency ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to benchmark spec code, example files, validation error examples, multi-benchmark test cases]
```

---

## Feature 2: System Under Test Specification

**Purpose:** Configure target system(s) $M = (f_\theta, V, \Lambda, \omega)$ where $f_\theta$ is model function, $V$ is version identifier, $\Lambda$ is inference configuration (temperature, top_p, top_k, max_tokens, stop sequences, sampling strategy), and $\omega$ is resource specification (GPU/CPU allocation, memory, batch sizes, timeouts, authentication). Maintains exact system lineage for reproducibility and enables comparative evaluation across multiple system configurations $\{M_i\}$.

**Essential Capabilities:**
1. **Multiple model provider support** - Supports 5+ providers (OpenAI, Anthropic, HuggingFace, local models, open-source frameworks, custom endpoints)
2. **Exact version specification** - Can unambiguously pin model versions (API release dates, checkpoint paths, specific model IDs)
3. **Inference parameter configuration** - All generation parameters configurable: temperature, top_p, top_k, max_tokens, stop sequences, sampling strategy
4. **Parameter validation** - Warns or validates parameter values against model constraints (e.g., temperature in [0, 2])
5. **Resource specification** - Controls compute allocation (GPU/CPU selection, memory limits, batch sizes, per-sample timeouts)
6. **Resource validation** - Prevents over-allocation or invalid configurations
7. **Multi-model comparative setup** - Enables 2+ systems in single run for head-to-head comparison, ablations, or baseline comparison
8. **Configuration reusability** - Can save/load/version system configurations for reproducible re-runs

**Look for:**
- List of supported model providers in documentation or code
- Example configurations for 2+ different model types
- Code showing version specification mechanism (e.g., model IDs, checkpoint paths, API versions)
- Parameter configuration options with validation/error checking
- Resource allocation code (GPU selection, memory specification, batch size config)
- Examples or tests showing multi-model evaluation setup
- Configuration serialization (YAML/JSON) for reproducibility
- Version control or history tracking for configurations

**Report template:**
```
S1F2: System Under Test Specification
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Multiple model provider support ✓/✗
  - Exact version specification ✓/✗
  - Inference parameter configuration ✓/✗
  - Parameter validation ✓/✗
  - Resource specification ✓/✗
  - Resource validation ✓/✗
  - Multi-model comparative setup ✓/✗
  - Configuration reusability ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to provider list, example configs, version spec code, multi-model examples]
```

---

## Feature 3: Measurement Protocol Selection

**Purpose:** Select and configure measurement approach $\mu$ from benchmark-provided options. Must support diverse modalities (human judgment, LLM-as-judge, algorithmic metrics, ensembles) with standardized interface $\mu: O \rightarrow (S, U, R, M)$ mapping outputs to scores $S$, uncertainties $U$, rationales $R$, and metadata $M$. Harness operationalizes measurement without establishing construct validity (already established by benchmark).

**Essential Capabilities:**
1. **Human judgment support** - Integration with crowdsourcing platforms (rater qualification screening, attention checks, inter-rater reliability metrics, demographic documentation, gold standard samples)
2. **LLM-as-judge support** - Judge model selection, rubric design, chain-of-thought reasoning prompts, confidence calibration, bias mitigation (blinding, randomization)
3. **Algorithmic metrics support** - Diverse scoring functions (BLEU, ROUGE, BERTScore, exact match, semantic similarity, custom functions); parameter configuration for each
4. **Ensemble combinations** - Can mix measurement modalities (voting schemes, confidence weighting, disagreement resolution)
5. **Custom metric support** - Can define and integrate custom scoring functions with same interface
6. **Standardized measurement schema** - All modalities return $(S, U, R, M)$: score, uncertainty, rationale, metadata
7. **Aggregation of subjective judgments** - Preserves judgment variability rather than forcing single-point aggregation
8. **Measurement validation** - Can test/validate measurement on small dataset before full-scale execution

**Look for:**
- Documentation listing supported measurement modalities
- Examples for each measurement type (human, AI, algorithmic)
- Crowdsourcing integration code or documentation (MTurk, Prolific, Scale AI, etc.)
- Judge model configuration and prompt examples
- List of available metrics and custom metric examples
- Ensemble combination examples (voting, weighting, etc.)
- Measurement output schema showing $(S, U, R, M)$ structure
- Code showing aggregation approach for multiple ratings/judgments
- Test cases or examples showing measurement validation workflow

**Report template:**
```
S1F3: Measurement Protocol Selection
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Human judgment support ✓/✗
  - LLM-as-judge support ✓/✗
  - Algorithmic metrics support ✓/✗
  - Ensemble combinations ✓/✗
  - Custom metric support ✓/✗
  - Standardized measurement schema ✓/✗
  - Aggregation of subjective judgments ✓/✗
  - Measurement validation ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to modality examples, crowdsourcing integration, judge config examples, schema definition]
```

---

## Feature 4: Baseline Specification

**Purpose:** Explicitly designate baseline systems for meaningful comparative context: random baselines, majority baselines, well-tuned classical methods, state-of-the-art models, human performance. Fair comparison criteria ensure same data splits, measurement protocol, and hyperparameter tuning budget across systems. Enables convergent validity evidence (target outperforms simpler alternatives) and discriminant validity assessment (performance relative to human capability).

**Essential Capabilities:**
1. **Random baseline support** - Can configure uniform random and majority-class baseline systems
2. **Majority baseline support** - Most-frequent-class predictor with proper implementation
3. **Classical methods support** - Can specify/tune classical ML (logistic regression, SVM, decision trees) with controlled hyperparameter budget
4. **State-of-the-art baselines** - Can integrate published SOTA results or models
5. **Human performance baselines** - Can configure expert or crowd-worker consensus as ceiling
6. **Fair comparison enforcement** - Ensures same data splits, measurement protocol, and scoring function for all systems
7. **Hyperparameter budget equity** - All systems receive same optimization effort/budget
8. **Baseline context in results** - Results presentation shows target vs baselines with comparative interpretation

**Look for:**
- Documentation listing supported baseline types
- Example baseline configurations for each type
- Code showing fair comparison enforcement (identical data splits, measurement protocol, etc.)
- Budget specification and tracking (e.g., same grid search iterations for each method)
- Result presentation showing absolute performance and baseline context
- Examples demonstrating validity evidence (convergent/discriminant) from baselines
- Baseline configuration reusability and versioning

**Report template:**
```
S1F4: Baseline Specification
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Random baseline support ✓/✗
  - Majority baseline support ✓/✗
  - Classical methods support ✓/✗
  - State-of-the-art baselines ✓/✗
  - Human performance baselines ✓/✗
  - Fair comparison enforcement ✓/✗
  - Hyperparameter budget equity ✓/✗
  - Baseline context in results ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to baseline types, fair comparison code, budget tracking examples, result presentation]
```

---

## Feature 5: Statistical Analysis Protocol

**Purpose:** Pre-specify complete statistical analysis plan $\Sigma$ BEFORE evaluation execution, preventing p-hacking and selective reporting. Includes sample size specification with power analysis (detect effect size $\delta$ with power $1-\beta$ at significance $\alpha$), primary/secondary metrics, significance thresholds, multiple comparison corrections (Bonferroni, Benjamini-Hochberg FDR, Holm-Bonferroni), uncertainty quantification method (bootstrap CIs with resampling specification or parametric CIs with documented assumptions), and stratification variables (demographics, task characteristics, difficulty).

**Essential Capabilities:**
1. **Plan pre-specification requirement** - Harness requires or strongly supports specifying $\Sigma$ before execution
2. **Sample size justification** - Power analysis with effect size assumptions and achieved power reporting
3. **Primary/secondary metric specification** - Clear designation of main objectives vs exploratory analyses
4. **Significance thresholds** - Configurable $\alpha$ levels with Bonferroni or other per-test adjustment
5. **Multiple comparison corrections** - 3+ methods available (Bonferroni, Benjamini-Hochberg FDR, Holm-Bonferroni, others)
6. **Uncertainty quantification method** - Multiple CI approaches (bootstrap percentile, BCa, parametric with assumption checking)
7. **Stratification variables** - Can specify demographics, task types, difficulty levels for subgroup analysis
8. **Plan adherence enforcement** - Harness follows pre-specified plan; deviations documented

**Look for:**
- Documentation showing required/supported pre-specification workflow
- Power analysis examples with effect size assumptions
- Code showing plan storage and versioning
- Examples of correction method specification
- Bootstrap CI or parametric CI code with parameter documentation
- Stratification variable configuration examples
- Evidence that harness enforces plan adherence (or documents deviations)
- Test cases showing plan specification and enforcement

**Report template:**
```
S1F5: Statistical Analysis Protocol
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Plan pre-specification requirement ✓/✗
  - Sample size justification ✓/✗
  - Primary/secondary metric specification ✓/✗
  - Significance thresholds ✓/✗
  - Multiple comparison corrections ✓/✗
  - Uncertainty quantification method ✓/✗
  - Stratification variables ✓/✗
  - Plan adherence enforcement ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to plan spec code, power analysis examples, correction methods list, CI methodology]
```

---

## Feature 6: Cross-Validation Strategy

**Purpose:** Define evaluation structure BEFORE model exposure to data. Select CV approach based on characteristics (k-fold for general, stratified k-fold for class imbalance, leave-one-out for small datasets, time-series forward chaining for temporal data, nested CV for simultaneous tuning/evaluation). Specify split preservation mechanism ensuring deterministic partitions across runs (fixed seed or explicit indices). Supports rigorous statistical comparison and prevents data leakage/optimistic bias.

**Essential Capabilities:**
1. **Multiple CV methods** - Supports 4+ approaches: k-fold, stratified k-fold, leave-one-out, time-series forward chaining, nested CV
2. **Deterministic split generation** - Can reproduce identical splits across runs via fixed seed or explicit indices
3. **Stratification control** - Can enforce balanced class distributions or other stratification across folds
4. **Temporal respect** - Time-series aware splitting that respects temporal ordering
5. **Leakage prevention** - Enforces test set isolation; prevents data leakage between train/validation/test
6. **Split specification** - Can explicitly specify fold indices or seeds for reproducibility
7. **Integration with statistics** - CV structure properly reflected in uncertainty estimates and aggregation
8. **Split reusability** - Can save/load CV splits for reproducible re-runs

**Look for:**
- Documentation listing supported CV methods with appropriate use cases
- Code showing deterministic split generation with seed control
- Stratification options and examples
- Time-series forward chaining implementation
- Explicit leakage prevention checks (documentation or code)
- Split indices or seed serialization for reproducibility
- Test cases showing CV reproducibility
- Integration with statistical aggregation (e.g., per-fold results aggregated correctly)

**Report template:**
```
S1F6: Cross-Validation Strategy
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Multiple CV methods ✓/✗
  - Deterministic split generation ✓/✗
  - Stratification control ✓/✗
  - Temporal respect ✓/✗
  - Leakage prevention ✓/✗
  - Split specification ✓/✗
  - Integration with statistics ✓/✗
  - Split reusability ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to CV methods documentation, split generation code, leakage prevention examples, reproducibility tests]
```

---

## Feature 7: Resource Budget Planning

**Purpose:** Project evaluation costs and establish operational constraints $\rho$ (compute budget: GPU/CPU hours, memory; cost limits: API token costs, cloud compute; time constraints: wall-clock deadlines, throughput requirements). Cost estimation via token-based modeling (input tokens × output tokens × samples × price per token) and API pricing structures. Enables tradeoff decisions: sample sizes vs statistical power, measurement protocol selection (human expensive vs LLM-judge cheaper), baseline scope, CV fold count. Prevents runs from exceeding resource limits.

**Essential Capabilities:**
1. **Compute budget specification** - GPU hours, CPU hours, memory allocation configurable
2. **Cost limit specification** - API token costs, cloud compute expenses, annotation budgets
3. **Time constraint specification** - Wall-clock deadlines, throughput requirements
4. **Cost estimation before run** - Predicts total cost given current configuration
5. **Token-based cost modeling** - Understands API pricing: (input tokens × output tokens × samples × price)
6. **Tradeoff analysis** - Can suggest: "With $100, evaluate X samples" or "Human judge costs 3× LLM judge"
7. **Budget enforcement** - Prevents run from exceeding limits; alerts on approaching limits
8. **Cost reporting** - Breakdown of costs by component in results; compares actual vs estimated

**Look for:**
- Budget specification documentation and examples
- Cost estimation code or utility functions
- Token-based pricing model implementation or documentation
- Tradeoff analysis examples (sample size vs cost, protocol choice vs cost)
- Budget enforcement logic (warnings, stopping conditions)
- Cost reporting in output or results
- Test cases showing cost estimation accuracy
- Integration with statistical power analysis (budget → sample size implications)

**Report template:**
```
S1F7: Resource Budget Planning
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Compute budget specification ✓/✗
  - Cost limit specification ✓/✗
  - Time constraint specification ✓/✗
  - Cost estimation before run ✓/✗
  - Token-based cost modeling ✓/✗
  - Tradeoff analysis ✓/✗
  - Budget enforcement ✓/✗
  - Cost reporting ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to budget config examples, cost model code, tradeoff analysis examples, cost reporting samples]
```

---

## Feature 8: Provenance Configuration

**Purpose:** Define comprehensive execution metadata capture strategy for complete reproducibility. Specify metadata tracking scope: timestamps (temporal tracking), model versions (exact system identification), configuration parameters (deterministic execution), random seeds (stochastic process control), data version hashes (input integrity), environment details (platform dependencies). Establishes requirements ensuring complete lineage from inputs $(M, B, \Sigma, \rho)$ to outputs $(O, R, A)$. Enables bit-by-bit reproducibility for external validation and regulatory compliance.

**Essential Capabilities:**
1. **Runtime metadata capture** - Timestamps (start, end, duration), wall-clock time, compute time automatically recorded
2. **Configuration snapshot** - All parameters serialized; nested configs flattened; defaults made explicit
3. **Model identification** - Model IDs, version hashes, checkpoint locations, API versions documented
4. **Environment specification** - OS version, Python version, library versions (complete dependency tree), GPU/CPU specs
5. **Data provenance** - Dataset version hashes (cryptographic), splits used (indices/seeds), preprocessing pipeline, normalization stats
6. **Execution logs** - Error logs with stack traces, warnings/info messages, performance metrics, intermediate results
7. **Git integration** - Configuration changes tracked; commit hashes link results to code versions
8. **Artifact storage** - Results, logs, configs saved with compression, integrity verification (checksums)

**Look for:**
- Metadata capture documentation listing what gets tracked
- Example metadata files (JSON/YAML format)
- Configuration serialization code or examples
- Model versioning mechanism
- Environment specification (requirements.txt, environment.yml, Docker, etc.)
- Data hashing and versioning code
- Execution log examples showing errors, warnings, performance
- Git integration for tracking configuration changes
- Checksum or integrity verification implementation
- Complete dependency pinning examples

**Report template:**
```
S1F8: Provenance Configuration
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Runtime metadata capture ✓/✗
  - Configuration snapshot ✓/✗
  - Model identification ✓/✗
  - Environment specification ✓/✗
  - Data provenance ✓/✗
  - Execution logs ✓/✗
  - Git integration ✓/✗
  - Artifact storage ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to metadata capture code, example files, env specs, dependency pinning examples, git integration]
```

