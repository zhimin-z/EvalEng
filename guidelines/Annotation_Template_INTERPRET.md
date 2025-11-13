# Stage 4: INTERPRET & RELEASE - Evaluation Harness Assessment Template
## Structured Evaluation Format with Coverage Analysis

---

## Evaluation Format

For each feature, you will complete this structure:

```
S4FX: [Feature Name]
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

## Feature 1: Stratified Performance Analysis

**Purpose:** Understand performance variations through flexible stratification enabling systematic investigation of model behavior. Stratify by task characteristics (task type, domain, difficulty level, input length, output length), metadata attributes (source, language, creation date, annotation quality), input properties (lexical diversity, syntactic complexity, semantic ambiguity) with hierarchical slicing support (nested stratifications: domain → task type → difficulty). Identify performance disparities via statistical significance testing accounting for multiple comparisons. Link variations to construct definition: do variations align with known sub-components (expected differential performance) or reveal unexpected patterns (potential confounds)? Compute Pareto frontiers for multi-objective tradeoffs (accuracy vs latency, performance vs cost, fairness vs accuracy).

**Essential Capabilities:**
1. **Task-based stratification** - Slicing by task type, domain, difficulty level, input length, output length requirements
2. **Metadata-based stratification** - Slicing by source, language, creation date, annotation quality with configurable attributes
3. **Input property stratification** - Analysis by lexical diversity, syntactic complexity, semantic ambiguity
4. **Hierarchical slicing** - Nested stratifications (domain → task type → difficulty) with drill-down capability
5. **Statistical significance testing** - Tests for performance disparities across subgroups with multiple comparison corrections
6. **Construct-aligned interpretation** - Links performance variations to construct definition sub-components
7. **Pareto frontier analysis** - Identifies efficient models on multi-objective tradeoffs (accuracy/latency, performance/cost, fairness/accuracy)
8. **Disparity visualization** - Heatmaps, scatter plots, or other visualizations showing performance across stratification dimensions

**Look for:**
- Stratification configuration options in documentation or code
- Examples of hierarchical slicing (nested drill-down)
- Statistical testing code for subgroup comparisons
- Multiple comparison correction implementation
- Construct definition integration in stratification interpretation
- Pareto frontier computation code or visualization examples
- Performance heatmaps or stratified performance tables
- Test cases showing stratification and statistical comparison
- Documentation linking performance patterns to construct validity
- Visualization examples for multi-dimensional stratifications

**Report template:**
```
S4F1: Stratified Performance Analysis
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Task-based stratification ✓/✗
  - Metadata-based stratification ✓/✗
  - Input property stratification ✓/✗
  - Hierarchical slicing ✓/✗
  - Statistical significance testing ✓/✗
  - Construct-aligned interpretation ✓/✗
  - Pareto frontier analysis ✓/✗
  - Disparity visualization ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to stratification options, hierarchical examples, statistical code, Pareto analysis examples]
```

---

## Feature 2: Failure Mode Analysis

**Purpose:** Conduct qualitative and quantitative analysis of failure patterns revealing systematic model limitations. Automated error clustering using semantic similarity (embed errors, cluster with k-means/DBSCAN), error type categorization (factual errors, reasoning errors, format errors, refusal errors), outlier detection. Perform root cause analysis identifying performance bottlenecks: are failures concentrated in specific task types? Do failures correlate with input characteristics (length, complexity)? Examine failure examples: extract representative samples from each cluster, generate human-readable explanations, quantify failure frequencies. Reference construct definition to distinguish construct-related failures (model doesn't understand phenomenon) from confounds (failures driven by non-targeted factors). If failures correlate with confounding factors, document as evidence limiting construct validity. Extract patterns to guide model improvement priorities.

**Essential Capabilities:**
1. **Automated error clustering** - Semantic similarity embedding and clustering (k-means, DBSCAN) to group failures
2. **Error type categorization** - Classification of failures (factual errors, reasoning errors, format errors, refusal errors, custom types)
3. **Outlier detection** - Identifies unusual failure patterns distinct from main clusters
4. **Root cause analysis** - Correlates failures with task types, input characteristics (length, complexity), metadata
5. **Representative example extraction** - Selects and surfaces representative samples from each error cluster
6. **Failure quantification** - Counts and computes failure frequencies; distributes failures across categories
7. **Construct validity linking** - Distinguishes construct-related failures from confounds; documents validity threats
8. **Pattern-based insights** - Generates actionable hypotheses about model limitations and improvement priorities

**Look for:**
- Error clustering code or implementation (embedding + clustering algorithm)
- Error type categorization system or documentation
- Outlier detection methodology
- Root cause analysis code correlating failures with characteristics
- Representative example extraction logic (e.g., cluster centers or diversity sampling)
- Failure frequency tables or statistics
- Construct definition integration in failure interpretation
- Documentation distinguishing construct failures from confounds
- Visualization of error clusters (2D projections, confusion matrices, category distributions)
- Examples showing how failure analysis guides improvements

**Report template:**
```
S4F2: Failure Mode Analysis
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Automated error clustering ✓/✗
  - Error type categorization ✓/✗
  - Outlier detection ✓/✗
  - Root cause analysis ✓/✗
  - Representative example extraction ✓/✗
  - Failure quantification ✓/✗
  - Construct validity linking ✓/✗
  - Pattern-based insights ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to clustering code, error categorization examples, root cause analysis, construct linking documentation]
```

---

## Feature 3: Interactive Investigation & Exploration

**Purpose:** Enable hands-on result investigation through rich interactive interfaces supporting exploratory analysis. Sample browser with powerful filtering (by score ranges, error types, metadata attributes, model predictions), full-text search across inputs/outputs/rationales, drill-down navigation from aggregate metrics to individual samples with context preservation. On-the-fly custom metric computation with real-time visualization. Comparative sample views across models (side-by-side output comparison, difference highlighting, agreement/disagreement analysis). Annotation interfaces for qualitative analysis (tag samples, add notes, flag for investigation). Jupyter notebook integration for programmatic exploratory analysis (export filtered samples, custom analyses, publication-quality visualizations, statistical hypothesis testing). Enable validation of automated findings, discovery of unexpected patterns, ad-hoc hypothesis testing.

**Essential Capabilities:**
1. **Sample browser with filtering** - Browse results with filters: score ranges, error types, metadata attributes, model predictions
2. **Full-text search** - Search across inputs, outputs, rationales, metadata for sample discovery
3. **Drill-down navigation** - Navigate from aggregate metrics to individual samples with context preservation
4. **Custom metric computation** - Define metrics on-the-fly; apply to filtered samples; update visualizations dynamically
5. **Comparative sample views** - Side-by-side model output comparison, difference highlighting, agreement/disagreement patterns
6. **Annotation interface** - Tag samples with custom categories, add notes/explanations, flag for further investigation
7. **Jupyter integration** - Export filtered samples; programmatic analysis; hypothesis testing; publication visualization
8. **Interactive visualization** - Plots, heatmaps, distributions update dynamically as filters/selections change

**Look for:**
- Web interface screenshots or documentation showing sample browser
- Filtering options and configuration examples
- Search functionality examples (queries and results)
- Drill-down examples from metric to sample
- Custom metric definition interface or code
- Side-by-side comparison examples
- Annotation workflow or screenshot
- Jupyter notebook integration examples or documentation
- Interactive visualization implementation (e.g., Plotly, Altair, custom JS)
- Test cases or examples showing exploratory workflows
- Documentation showing intuitive result investigation patterns

**Report template:**
```
S4F3: Interactive Investigation & Exploration
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Sample browser with filtering ✓/✗
  - Full-text search ✓/✗
  - Drill-down navigation ✓/✗
  - Custom metric computation ✓/✗
  - Comparative sample views ✓/✗
  - Annotation interface ✓/✗
  - Jupyter integration ✓/✗
  - Interactive visualization ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to interface screenshots, filtering examples, search implementation, Jupyter integration examples]
```

---

## Feature 4: Execution Artifact Management

**Purpose:** Package complete evaluation artifacts for reproducibility and traceability. Comprehensive runtime metadata capture (execution timestamps start/end, wall-clock time, compute time), complete configuration snapshot (all parameters serialized, nested configurations flattened, defaults explicit), model identification (model ID, version hash, checkpoint location, API version), environment details (OS version, Python version, library versions with dependency tree, GPU/CPU specs, memory allocation, batch settings). Data provenance tracking (dataset version hashes, splits used, preprocessing pipeline, normalization statistics). Execution logs (errors with stack traces, warnings/info messages, performance metrics, intermediate results). Git integration (track configuration changes via version control, commit hashes linking results to code). Enable external researchers to reproduce exactly. Support result queries and run comparisons.

**Essential Capabilities:**
1. **Runtime metadata capture** - Automatically records execution timestamps (start, end, duration), wall-clock time, compute time
2. **Configuration snapshot** - Serializes all parameters; flattens nested configurations; makes defaults explicit
3. **Model identification** - Records model ID, version hash, checkpoint location, API version, model lineage
4. **Environment specification** - OS version, Python version, complete library dependency tree, GPU/CPU specs, memory allocation
5. **Data provenance tracking** - Cryptographic hashes of datasets, split specifications (indices/seeds), preprocessing pipeline, normalization stats
6. **Execution logs** - Error logs with stack traces, warnings/info messages, performance metrics, intermediate results
7. **Git integration** - Tracks configuration changes via version control; commit hashes link results to code versions
8. **Artifact storage & integrity** - Results/logs/configs saved with compression; integrity verification via checksums

**Look for:**
- Metadata capture documentation listing tracked information
- Example metadata files (JSON/YAML format showing complete structure)
- Configuration serialization code or examples
- Model versioning mechanism with examples
- Environment specification formats (requirements.txt, environment.yml, Docker, setup.py)
- Data hashing and provenance code
- Execution log examples (errors, warnings, performance data)
- Git integration implementation or documentation
- Checksum or integrity verification code
- Complete artifact structure examples
- Run comparison or query utilities

**Report template:**
```
S4F4: Execution Artifact Management
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Runtime metadata capture ✓/✗
  - Configuration snapshot ✓/✗
  - Model identification ✓/✗
  - Environment specification ✓/✗
  - Data provenance tracking ✓/✗
  - Execution logs ✓/✗
  - Git integration ✓/✗
  - Artifact storage & integrity ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to metadata examples, config serialization code, model versioning, env specs, artifact structure examples]
```

---

## Feature 5: Comparative Report Generation

**Purpose:** Generate multi-format reports tailored to diverse stakeholder needs. Executive summaries emphasizing key findings (which model performs best? by how much? is difference significant?) and critical limitations (validity caveats from benchmark, evaluation scope restrictions, known confounds). Technical deep-dives with complete statistical details (full metric tables with uncertainties, significance test results with p-values and effect sizes, fairness analyses with subgroup breakdowns, failure mode analyses with examples, stratified performance). Compliance documentation for regulated domains (audit trails, provenance chains, validation evidence, fairness certifications). Research paper format for publication (methods with complete specification, results with tables/figures, discussion of validity evidence). Rich visualizations (confusion matrices with normalized/raw counts, ROC curves with AUC CIs, performance distributions via violin plots, fairness heatmaps, failure clusters, scatter plots for tradeoffs). Integrate benchmark's validity evidence: include construct definition, sampling rationale, limitations from validity evidence, explicitly state validity scope. Reports include caveats about construct validity boundaries.

**Essential Capabilities:**
1. **Executive summary generation** - High-level findings, key decisions, critical limitations, actionable recommendations
2. **Technical deep-dive reports** - Complete statistical details: metric tables with uncertainties, significance tests, effect sizes, fairness breakdowns, failure analyses
3. **Compliance documentation** - Audit trails, provenance chains, validation evidence, fairness/bias certifications for regulated domains
4. **Research paper format** - Methods section with complete specification, results with tables/figures, discussion of validity
5. **Benchmark validity integration** - Includes construct definition, sampling rationale, known limitations, explicitly states validity scope
6. **Rich visualizations** - Confusion matrices, ROC curves with CIs, performance distributions (violin/box plots), fairness heatmaps, error clusters, tradeoff scatter plots
7. **Multi-format output** - HTML (interactive), PDF (shareable), Markdown (version-controllable), JSON (machine-readable)
8. **Validity caveat integration** - Reports explicitly state what claims are supported vs not supported; discuss construct validity boundaries

**Look for:**
- Example report outputs in multiple formats (HTML, PDF, Markdown)
- Executive summary examples
- Technical report examples with statistics and visualizations
- Compliance documentation format or examples
- Research paper format examples
- Visualization library usage (Matplotlib, Plotly, Seaborn, etc.)
- Benchmark validity evidence integration in reports
- Caveats and limitations sections in examples
- Report generation code or templates
- Table and figure examples with proper formatting
- Integration of fairness/bias results in reports

**Report template:**
```
S4F5: Comparative Report Generation
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Executive summary generation ✓/✗
  - Technical deep-dive reports ✓/✗
  - Compliance documentation ✓/✗
  - Research paper format ✓/✗
  - Benchmark validity integration ✓/✗
  - Rich visualizations ✓/✗
  - Multi-format output ✓/✗
  - Validity caveat integration ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to report examples, visualization samples, benchmark integration examples, multi-format output]
```

---

## Feature 6: Reproducibility Package

**Purpose:** Bundle all components required for exact reproduction enabling external validation. Complete evaluation code (harness implementation, measurement protocols, statistical analysis scripts) with pinned dependencies (requirements.txt, conda environment.yml, Poetry lock file, Docker container), configuration files (YAML/JSON configs, command-line arguments, environment variables), dataset versions or access instructions (download scripts, API access details, preprocessing code, checksums), model identifiers (HuggingFace model IDs, OpenAI versions, custom checkpoints with download links), random seeds (all stochastic seeds documented), execution environment specifications (OS details, hardware specs, library versions, compiler versions), complete results with provenance (raw outputs, intermediate results, final metrics, execution logs). Package enables independent verification by external researchers. Supports scientific peer review: reviewers verify methodology and results. Enables regulatory audit: demonstrate evaluation rigor. Include checksum verification for data integrity (SHA-256 hashes). Document aspects preventing perfect reproduction (proprietary models, restricted datasets, non-deterministic operations).

**Essential Capabilities:**
1. **Complete code packaging** - Harness implementation, measurement protocols, statistical analysis scripts, utilities
2. **Pinned dependencies** - requirements.txt, conda environment.yml, Poetry lock file, or Docker container specification
3. **Configuration files** - YAML/JSON configs, command-line argument specifications, environment variables
4. **Dataset accessibility** - Download scripts, API access details, preprocessing code, checksums for verification
5. **Model identifiers** - HuggingFace model IDs, OpenAI model versions, custom model checkpoints with download links
6. **Random seed documentation** - All stochastic process seeds explicitly documented and reproducible
7. **Environment specifications** - OS details, hardware specs (GPU/CPU), complete library versions, compiler versions
8. **Results with provenance** - Raw outputs, intermediate results, final metrics, execution logs, complete run metadata

**Look for:**
- Example reproducibility package structure or documentation
- Complete requirements.txt or environment.yml examples
- Docker container specifications or examples
- Configuration file examples (YAML/JSON)
- Download scripts or API access documentation
- Model identifier documentation with examples
- Random seed specification examples
- Environment specification documentation
- Results package structure with metadata
- Checksum verification implementation
- README documenting reproduction workflow
- Example of external researcher reproducing results

**Report template:**
```
S4F6: Reproducibility Package
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Complete code packaging ✓/✗
  - Pinned dependencies ✓/✗
  - Configuration files ✓/✗
  - Dataset accessibility ✓/✗
  - Model identifiers ✓/✗
  - Random seed documentation ✓/✗
  - Environment specifications ✓/✗
  - Results with provenance ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to package examples, dependency specs, config examples, model ID formats, environment specs]
```

---

## Feature 7: Model Ranking & Leaderboard

**Purpose:** Enable systematic comparison across multiple models through rigorous statistical and ranking frameworks. Pairwise statistical testing comparing model performance via t-tests (paired for within-dataset, independent for between-dataset), Wilcoxon signed-rank tests (non-parametric), permutation tests (non-standard metrics), with pre-specified multiple comparison corrections (Bonferroni, Benjamini-Hochberg FDR). Effect size computation: Cohen's d (standardized mean difference), Hedges' g (bias-corrected for small samples), confidence intervals on effect sizes. Multi-objective comparison supporting tradeoff analysis: accuracy vs latency (Pareto frontier), performance vs cost (cost-efficiency frontier), accuracy vs fairness (fairness-accuracy tradeoff curves). Probabilistic ranking systems for robust model ordering: Elo ratings (chess-style ranking with uncertainty), TrueSkill (Bayesian skill rating), Bradley-Terry model (pairwise comparison). Comparative leaderboards aggregating results: time-stamped rankings tracking evolution, confidence intervals on rankings, filtering by benchmark/task/domain. Support multi-metric aggregation with explicit weighting: specify metric weights, aggregate with uncertainty propagation, handle Pareto-incomparable models transparently.

**Essential Capabilities:**
1. **Pairwise statistical testing** - t-tests (paired and independent), Wilcoxon signed-rank, permutation tests with multiple comparison correction
2. **Effect size computation** - Cohen's d, Hedges' g, confidence intervals on effect sizes quantifying practical significance
3. **Multi-objective comparison** - Pareto frontier analysis (accuracy/latency, performance/cost, accuracy/fairness tradeoffs)
4. **Probabilistic ranking systems** - Elo ratings, TrueSkill, Bradley-Terry model for robust model ordering
5. **Confidence intervals on rankings** - Uncertainty quantification in model rankings reflecting statistical variability
6. **Comparative leaderboards** - Time-stamped rankings, evolution tracking, filtering by benchmark/task/domain
7. **Multi-metric aggregation** - Explicit metric weighting, aggregate scoring with uncertainty propagation
8. **Pareto-incomparable handling** - Transparent representation of models on efficiency frontiers with no clear winner

**Look for:**
- Statistical testing code for pairwise comparisons
- Multiple comparison correction implementation (Bonferroni, FDR, etc.)
- Effect size computation examples
- Pareto frontier computation and visualization
- Ranking system implementation (Elo, TrueSkill, Bradley-Terry)
- Leaderboard examples with time-stamped data
- Confidence interval examples on rankings
- Multi-metric aggregation code or examples
- Uncertainty propagation through aggregation
- Visualization of multi-objective tradeoffs
- Handling of incomparable models (Pareto surfaces)
- Test cases showing ranking robustness

**Report template:**
```
S4F7: Model Ranking & Leaderboard
Grade: [Absent/Partial/Present] (XX% coverage)
Supports:
  - Pairwise statistical testing ✓/✗
  - Effect size computation ✓/✗
  - Multi-objective comparison ✓/✗
  - Probabilistic ranking systems ✓/✗
  - Confidence intervals on rankings ✓/✗
  - Comparative leaderboards ✓/✗
  - Multi-metric aggregation ✓/✗
  - Pareto-incomparable handling ✓/✗
Documentation: [Minimal/Moderate/Comprehensive]
Evidence: [Link to statistical testing code, effect size examples, Pareto analysis, ranking system impl, leaderboard examples]
```

