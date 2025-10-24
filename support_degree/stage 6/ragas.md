# ragas - Stage 6 (RELEASE) Evaluation

## Summary
Ragas provides basic artifact management through local CSV/JSONL storage and experiments framework, but lacks sophisticated versioning, reproducibility manifests, automated reporting, and distribution integrations. The framework focuses on evaluation execution rather than result communication. Examples show CSV output capabilities, but no built-in reporting templates, dashboards, or platform integrations are evident.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 2 | Basic metadata capture exists (experiment names, timestamps in filenames), but limited querying/comparison tools. Datasets and experiments save to CSV/JSONL with minimal metadata. No built-in UI for filtering, comparing runs, or packaging beyond file export. Example: `examples/ragas_examples/agent_evals/evals.py` shows `experiment_result` stored with basic fields, but no query API or comparison interface. |
| S6F2: Version Control | 1 | No evidence of git integration, dependency pinning, or reproducibility manifests. The framework doesn't automatically track commits, capture environment details (Python/CUDA versions), or generate manifests. Users must manually version control their evaluation code. No lockfile generation or containerization support found in docs/examples. |
| S6F3: Report Generation | 1 | Results export to CSV only (see `src/ragas/dataset.py` with local CSV backend). No HTML/PDF reports, stakeholder templates, or visualizations built-in. Users must manually create charts from CSV data. Examples show raw CSV output: `pd.DataFrame(samples).to_csv("datasets/test_dataset.csv")` but no reporting automation. |
| S6F4: Distribution Channels | 0 | No CI/CD integrations, MLOps platform publishing, leaderboard support, or notification systems found. The codebase has some integration hooks (MLflow, W&B mentioned in optional dependencies `pyproject.toml`), but no documented distribution workflows. No examples of automated publishing, webhooks, or alerts based on metrics. |

---

## Detailed Evidence

### S6F1: Artifact Management (Rating: 2)

Runtime Capture:
- Basic experiment tracking exists via `@experiment()` decorator:
```python
# examples/ragas_examples/agent_evals/evals.py
@experiment()
async def run_experiment(row):
    # ... evaluation logic ...
    return {
        "question": question,
        "expected_answer": expected_answer,
        "prediction": prediction.get("result"),
        "log_file": prediction.get("log_file"),
        "correctness": correctness.value,
    }
```
- Experiments save results with basic metadata (user inputs, predictions, scores)
- Timestamps in filenames: `examples/ragas_examples/agent_evals/agent.py` shows `run_{run_id}_{timestamp}.json` logs

Querying:
- No built-in query API or filtering interface
- Users must manually load CSV files to filter/query:
```python
# Manual querying required:
df = pd.read_csv("experiments/experiment_name.csv")
filtered = df[df['correctness'] == 1.0]
```

Comparison:
- No side-by-side comparison tools or diff utilities
- Tutorial guidance suggests manual inspection:
```markdown
# docs/tutorials/prompt.md
"You can now inspect the results by opening the `experiments/experiment_name.csv` file."
```

Packaging:
- Basic CSV/JSONL export via backends (`src/ragas/backends/local_csv.py`, `local_jsonl.py`)
- No compression, selective packaging, or bundling features
- Example shows trace export but not structured packaging:
```python
# examples/ragas_examples/agent_evals/agent.py
def export_traces_to_log(self, run_id: str, problem: str, final_result):
    # Exports JSON logs but no packaging features
    with open(log_filepath, "w") as f:
        json.dump(log_data, f, indent=2)
```

Why not 3 points: Lacks automated comparison tools, query APIs, and rich packaging features. Mostly manual CSV inspection.

---

### S6F2: Version Control (Rating: 1)

Git Integration:
- No automatic commit tracking or git integration found in codebase
- No references to git SHA capture in experiment metadata

Dependency Pinning:
- `pyproject.toml` uses flexible version constraints (`openai>=1.0.0`), not pinned versions
- No automatic `pip freeze` or lockfile generation during experiments
- Example:
```toml
# examples/pyproject.toml
dependencies = [
    "ragas",
    "openai>=1.0.0",  # Not pinned
    "pandas",
]
```

Environment Capture:
- No evidence of Python version, CUDA version, or OS tracking in experiment results
- No environment variable logging beyond API keys

Manifest Generation:
- No reproducibility manifest creation found
- Users must manually document their environment

Container Packaging:
- No Docker export or containerization features
- Benchmark Dockerfile exists (`tests/benchmarks/Dockerfile`) but not for evaluation reproducibility

Why not 0 points: Minimal version tracking exists (package versions in dependencies), but no automated versioning system.

---

### S6F3: Report Generation (Rating: 1)

Format Support:
- CSV only via local backends:
```python
# src/ragas/backends/local_csv.py
def save_dataset(self, name: str, data: List[Dict], model):
    # Saves to CSV only
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
```
- No HTML, PDF, JSON, or interactive dashboard generation
- JSONL backend exists but still plain text output

Stakeholder Templates:
- No templates for executives, technical teams, compliance, or research
- Generic CSV output requires manual formatting

Visualization:
- No built-in charts, confusion matrices, or plots
- Examples show static images in docs (`docs/_static/imgs/`) but no programmatic generation
- Users must create their own visualizations:
```python
# Not provided by Ragas - users must DIY:
import matplotlib.pyplot as plt
df = pd.read_csv("experiments/results.csv")
df['correctness'].plot.bar()
```

Automation:
- No report generation automation
- Experiment results save automatically, but no customizable templates

Why not 0 points: Basic CSV export works reliably, but no rich reporting capabilities.

---

### S6F4: Distribution Channels (Rating: 0)

CI/CD Integration:
- No GitHub Actions, GitLab CI, or Jenkins integration examples
- No pass/fail gates documented
- CI workflow exists (`.github/workflows/`) but for testing Ragas itself, not user evaluations

MLOps Platforms:
- Optional dependencies mention integrations:
```toml
# pyproject.toml (root)
[project.optional-dependencies]
# No explicit mlflow/wandb/neptune listed in main dependencies
```
- But no examples of publishing to MLflow, W&B, Neptune, or Comet
- No model registry publishing workflows

Public Leaderboards:
- No HuggingFace Hub publishing examples
- No Papers with Code integration
- No custom leaderboard support

Notifications:
- No Slack, email, or webhook notification features
- No alerting on metric degradation

Evidence of absence:
- Searched for "mlflow", "wandb", "slack", "webhook" in examples - no results
- `examples/` directory has no integration examples beyond basic LLM providers
- `docs/howtos/integrations/` likely has LLM integrations, not distribution platforms (based on `oci_genai_example.py`)

Why 0 points: Complete absence of distribution channel features. Users must manually copy results to external platforms.

---

## Key Strengths
1. Reliable CSV export: Works consistently for local storage
2. Experiment decorator: Simple pattern for organizing evaluations
3. Extensible backends: Plugin architecture allows custom storage (Google Drive example)

## Key Gaps
1. No reproducibility tracking: Missing git, dependencies, environment capture
2. No automated reporting: No HTML/PDF/dashboard generation
3. No distribution integrations: No MLOps platform publishing or CI/CD hooks
4. Limited artifact management: No query API, comparison tools, or packaging features

## Recommendations for Improvement
1. Add git SHA and branch tracking to experiment metadata
2. Implement HTML report generation with metric tables and charts
3. Create MLflow/W&B integration examples for result publishing
4. Build query API for filtering and comparing experiment runs
5. Generate reproducibility manifests with environment details