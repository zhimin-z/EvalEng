# ranx - Stage 1 (CONFIGURE) Evaluation

## Summary
ranx is a Python library for ranking evaluation and fusion, primarily focused on Information Retrieval metrics. It provides limited configuration capabilities as it's designed as an evaluation tool rather than a full evaluation framework. Most configuration is done programmatically via Python dictionaries, with some support for file-based data sources.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited dataset abstraction. Supports loading from JSON/TREC files, Pandas DataFrames, and Parquet. No schema definition, versioning, or declarative splits. Evidence: `docs/qrels.md` shows `Qrels.from_file()`, `from_df()`, `from_parquet()`, and `from_ir_datasets()`, but no schema/version APIs. |
| S1F2: Model Configuration | 0 | No model configuration system. ranx evaluates pre-computed runs, not models. No provider support, authentication, or resource allocation. Evidence: README shows evaluation of `Run` objects (pre-computed results), not model configuration. |
| S1F3: Prompt Configuration | 0 | Not applicable. ranx is a ranking evaluation library, not an LLM evaluation framework. No prompt templates or parameter configuration. Evidence: Repository focuses on IR metrics (MAP, NDCG, MRR) in `ranx/metrics/`. |
| S1F4: Environment Setup | 2 | Good dependency management with pinned versions. Provides requirements.txt, setup.py, and dev environment. No containerization (Dockerfile mentioned in Makefile but not provided). Evidence: `requirements.txt` lists dependencies, `setup.py` specifies `python>=3.8`, `Makefile` has setup commands. |
| S1F5: Security & Access | 0 | No security features. Downloads from ranxhub use plain HTTP requests. No authentication, access control, or audit logging. Evidence: `ranx/downloader.py` uses basic `requests.get()`, no credential management in codebase. |
| S1F6: Cost Estimation | 0 | No cost estimation features. Library evaluates pre-computed results, doesn't make API calls. Evidence: No cost-related code in repository; focuses on metric computation from existing runs. |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (1/3)

Evidence of Support:

ranx provides basic data source support through the `Qrels` class:

From `docs/qrels.md`:
```python
# Load from files
qrels = Qrels.from_file("path/to/qrels.json")  # JSON file
qrels = Qrels.from_file("path/to/qrels.trec")  # TREC-Style file
qrels = Qrels.from_file("path/to/qrels.gz")    # Gzipped TREC-Style file

# Load from ir-datasets
qrels = Qrels.from_ir_datasets("msmarco-document/dev")

# Load from Pandas DataFrames
qrels = Qrels.from_df(df=qrels_df, q_id_col="q_id", doc_id_col="doc_id", score_col="score")

# Load from Parquet files
qrels = Qrels.from_parquet(path="/path/to/parquet/file", q_id_col="q_id", doc_id_col="doc_id", score_col="score")
```

From `ranx/data_structures/qrels.py` (inferred from structure):
- Supports 4-5 different sources (JSON, TREC, Parquet, ir-datasets, DataFrames)
- No schema definition API - data is loaded as-is
- No validation rules or type constraints
- No versioning system

Missing Features:
- No schema definition or validation
- No split strategies (data is loaded as a complete set)
- No versioning or dataset version tracking
- Limited to query-document relevance judgments format

Rating: 1/3 - Provides basic file loading from multiple sources but lacks schema definition, splits, and versioning. Only rates what exists, not what could be implemented.

---

### S1F2: Model and Backend Configuration (0/3)

Evidence:

From `README.md`:
```python
# ranx evaluates pre-computed runs
run_dict = {
    "q_1": {"d_12": 0.9, "d_23": 0.8, "d_25": 0.7},
    "q_2": {"d_12": 0.9, "d_11": 0.8, "d_25": 0.7}
}
run = Run(run_dict)
evaluate(qrels, run, "ndcg@5")
```

From `docs/faq.md`:
```markdown
## Is `ranx` suited for evaluating classification tasks?
No, it's not. `ranx` is meant for ranking tasks.
```

Analysis:
- ranx evaluates pre-computed ranking results (`Run` objects), not models
- No provider abstraction (OpenAI, Anthropic, etc.)
- No model configuration API
- No authentication or resource allocation
- The library computes metrics on already-generated results

Rating: 0/3 - No model configuration system exists. This is by design - ranx is a post-hoc evaluation tool for ranking tasks.

---

### S1F3: Evaluation Parameters and Prompt Configuration (0/3)

Evidence:

From `docs/metrics.md`:
```python
# Metric computation, not prompt configuration
evaluate(qrels, run, "ndcg@5")  # Single metric with cutoff
evaluate(qrels, run, ["map@5", "mrr"])  # Multiple metrics
```

From repository structure:
- `ranx/metrics/` contains metric implementations (MAP, NDCG, MRR, etc.)
- No prompt templates or LLM-related configuration
- No parameter sweeps for temperature, top_p, etc.

Analysis:
- ranx is an Information Retrieval evaluation library, not an LLM evaluation framework
- Focuses on ranking metrics (NDCG, MAP, MRR) for pre-computed results
- No prompt system, few-shot support, or LLM parameters
- Metrics are computed via Python function calls, not declarative configuration

Rating: 0/3 - Not applicable to this library's domain. ranx evaluates IR/ranking tasks, not generative AI models.

---

### S1F4: Environment Setup and Dependency Management (2/3)

Evidence:

From `requirements.txt`:
```txt
cbor2
fastparquet
ir_datasets
lz4
numba
numpy
orjson
pandas
rich
scipy>=1.8.0
seaborn
tabulate
tqdm
```

From `setup.py`:
```python
install_requires=[
    "numpy",
    "numba>=0.54.1",
    "pandas",
    "tabulate",
    "tqdm",
    "scipy>=1.8.0",
    "ir_datasets",
    "rich",
    "orjson",
    "lz4",
    "cbor2",
    "seaborn",
    "fastparquet",
],
python_requires=">=3.8",
```

From `Makefile`:
```makefile
.venv:  ## Set up virtual environment and install requirements
	python3 -m venv $(VENV)
	$(MAKE) requirements

.PHONY: requirements
requirements: .venv  ## Install/refresh all project requirements
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements-dev.txt
	$(VENV_BIN)/pip install -r requirements.txt
```

From `dev_env.yml`:
```yml
name: ranx
dependencies:
  - black
  - numba=0.54.1
  - numpy
  - pandas
  - python>=3.8
  - scipy>=1.8
```

Strengths:
- Multiple dependency specifications (requirements.txt, setup.py, dev_env.yml)
- Some version pinning (numba>=0.54.1, scipy>=1.8.0, python>=3.8)
- Makefile automation for setup
- Both development and production dependencies separated

Weaknesses:
- No official Dockerfile (referenced in Makefile but not provided)
- Not all dependencies have pinned versions
- No hardware requirement specifications (GPU/CPU)
- No compatibility checks on startup

Rating: 2/3 - Good dependency management with multiple specifications and some automation, but lacks containerization and hardware specifications. Not full 3 points due to missing Docker support and incomplete version pinning.

---

### S1F5: Security and Access Control (0/3)

Evidence:

From `ranx/downloader.py`:
```python
def downloader(url: str, path: str, file_size: int, resume_byte_pos: int = None):
    # Append information to resume download
    resume_header = (
        {"Range": f"bytes={resume_byte_pos}-"} if resume_byte_pos else None
    )
    
    # Establish connection
    r = requests.get(url, stream=True, headers=resume_header)
```

From `ranx/ranxhub.py`:
```python
base_url = "https://ranxhub.s3.eu-central-1.amazonaws.com"

def get_url(id: str):
    return f"{base_url}/{quote(id)}.rh"
```

Analysis:
- No credential management system
- Downloads use plain HTTP requests without authentication
- No access control mechanisms
- No audit logging
- No user/role system
- No encryption at rest for cached files
- Public S3 bucket access for ranxhub

Rating: 0/3 - No security features implemented. All data access is unauthenticated and unencrypted.

---

### S1F6: Cost Estimation and Budget Planning (0/3)

Evidence:

Repository search shows:
- No cost-related code in any files
- No API call tracking or token counting
- No budget limits or cost modeling
- Library evaluates pre-computed results, doesn't make API calls

From `README.md`:
```python
# Evaluation of pre-computed results
evaluate(qrels, run, "ndcg@5")
```

Analysis:
- ranx evaluates pre-computed ranking results
- No API calls are made during evaluation
- Metrics are computed locally using Numba-optimized code
- No cost estimation needed for this use case

Rating: 0/3 - Not applicable to this library's design. ranx doesn't make API calls or incur usage costs.

---

## Calibration Check

### Why not higher scores?

S1F1 (Dataset Discovery): Could be rated 2/3 if it had schema definition, but lacks this critical feature. No split strategies or versioning. Current functionality is basic file I/O.

S1F2 (Model Configuration): Could be 1/3 if we counted "Run" as a model abstraction, but it's really just pre-computed results. No actual model configuration exists.

S1F4 (Environment Setup): Could be 3/3 with official Docker support and complete version pinning. Missing containerization prevents full score.

### Why not lower scores?

S1F1: Rated 1/3 not 0/3 because it does provide multiple data source connectors (5 formats) which partially meets requirements.

S1F4: Rated 2/3 not 1/3 because it has good dependency specifications, separation of dev/prod dependencies, and Makefile automation. Only lacks containerization.

---

## Key Observations

1. Domain Mismatch: ranx is an Information Retrieval evaluation library, not an LLM evaluation framework. Many Stage 1 features (model configuration, prompts) are not applicable.

2. Post-Hoc Evaluation: The library evaluates pre-computed results (`Run` objects), not live model outputs. This design choice eliminates needs for model configuration, API management, and cost tracking.

3. Strengths: Good environment management and multiple data format support for loading qrels/runs.

4. Weaknesses: No security features, no schema definition, no versioning, no containerization.

5. Use Case Alignment: ranx is designed for researchers who already have ranking results and want to compute metrics, not for orchestrating end-to-end evaluation pipelines.

---

## Final Checklist

- [x] All 6 features rated (S1F1 through S1F6)
- [x] Every rating has evidence (code snippets, doc links, file paths)
- [x] Justifications are concise (2-4 sentences max)
- [x] Consistent rating standards across features
- [x] Evidence-based ratings, not documentation claims alone
- [x] Avoided rating potential/future features
- [x] Considered domain appropriateness (IR evaluation vs LLM evaluation)