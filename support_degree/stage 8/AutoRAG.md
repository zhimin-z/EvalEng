# Marker-Inc-Korea__AutoRAG - Stage 8 (MONITOR) Evaluation

## Summary
AutoRAG is primarily a RAG pipeline optimization framework focused on offline evaluation and experimentation. It has minimal post-deployment monitoring capabilities. The framework excels at finding optimal RAG configurations through systematic evaluation but lacks dedicated production monitoring features, online evaluation infrastructure, automated feedback loops, or improvement recommendation systems.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring capabilities found. Searched extensively through documentation (`docs/source/`), configuration files (`sample_config/`), and codebase structure. No mention of: distribution shift detection, drift scores, performance degradation tracking, behavioral monitoring, or alerting systems. The framework focuses entirely on offline optimization with pre-collected datasets. Evidence: `docs/source/tutorial.md` shows evaluation workflow with static parquet files; `docs/source/optimization/optimization.md` describes node-by-node offline testing; no monitoring-related modules in `autorag/` structure. |
| S8F2: Online Evaluation | 0 | No online or streaming evaluation support. The architecture is strictly batch-based using parquet files. Documentation (`docs/source/deploy/api_endpoint.md`, `api/README.md`) shows API deployment capabilities but no A/B testing, shadow deployment, or streaming evaluation features. All evaluation happens during optimization phase with fixed datasets: "You must prepare an evaluation dataset for your RAG pipeline" (`docs/source/tutorial.md`). The `autorag.evaluator` module (`autorag/evaluator.py`) only supports offline evaluation. No evidence of traffic splitting, gradual rollout, or automated rollback mechanisms. |
| S8F3: Feedback Integration | 0 | No feedback loop integration exists. Examined all data creation documentation (`docs/source/data_creation/`), evaluation code, and API structure. The system uses static QA datasets (`qa.parquet`, `corpus.parquet`) for evaluation. No mechanisms for: production log parsing, user feedback collection, failure mining, or closed-loop automation. The workflow is: create dataset → optimize → deploy, with no feedback path back to optimization. Evidence: `docs/source/data_creation/data_format.md` describes fixed dataset format; no mention of production data ingestion anywhere in docs. |
| S8F4: Improvement Planning | 1 | Minimal improvement support through result analysis only. The framework provides `summary.csv` files showing comparative module performance (`docs/source/optimization/folder_structure.md`: "Contains the best modules and settings selected from each node"). Users can manually analyze which components performed better, but there's no automated root cause analysis, hyperparameter recommendations, or roadmap generation. The `dashboard` command (`autorag dashboard --trial_dir`) visualizes results for manual inspection. Limited to raw comparison data without actionable recommendations. No evidence of sensitivity analysis, gap analysis, or automated improvement suggestions in codebase or documentation. |

---

## Detailed Evidence

### S8F1: Drift Monitoring (0 points)
Search conducted across:
- Documentation: `docs/source/tutorial.md`, `docs/source/optimization/`, `docs/source/deploy/`
- Configuration: `autorag/sample_config/rag/`, `projects/tutorial_1/configs/`
- Code structure: Repository overview shows no monitoring-related directories

Key absences:
1. No statistical tests mentioned (KS test, chi-square, MMD)
2. No drift detection in API server code (`api/app.py`, `api/src/`)
3. No alerting infrastructure in codebase
4. No production monitoring integrations

Evidence of batch-only design:
```yaml
# From docs/source/tutorial.md
autorag evaluate --config your/path/to/default_config.yaml \
  --qa_data_path your/path/to/qa.parquet \
  --corpus_data_path your/path/to/corpus.parquet
```
All evaluation requires pre-existing parquet files with no live monitoring.

### S8F2: Online Evaluation (0 points)
Deployment capabilities but no online evaluation:
```python
# From docs/source/tutorial.md - API deployment
from autorag.deploy import ApiRunner
runner = ApiRunner.from_trial_folder('/your/path/to/trial_dir')
runner.run_api_server()
```
This deploys a fixed pipeline with no A/B testing or online metrics.

API structure analysis (`api/README.md`, `api/app.py`):
- Provides REST endpoints for querying
- No traffic splitting logic
- No real-time evaluation endpoints
- No shadow deployment support

Architecture limitation:
From `docs/source/structure.md`: "Node Line: A Collection of Nodes... Nodes are currently arranged temporarily"
The pipeline is static post-optimization with no dynamic evaluation.

### S8F3: Feedback Integration (0 points)
Data creation is one-way only:
```python
# From docs/source/data_creation/tutorial.md
corpus_instance.sample(random_single_hop, n=3) \
    .batch_apply(factoid_query_gen, llm=llm) \
    .batch_apply(make_basic_gen_gt, llm=llm)
```
All data generation happens offline before optimization.

No production data paths:
- `docs/source/data_creation/data_format.md` specifies fixed parquet schemas
- No mention of log parsing, feedback collection, or production metrics
- `api/database/project_db.py` stores trial results, not production feedback
- No closed-loop automation in `autorag/evaluator.py`

### S8F4: Improvement Planning (1 point)
What exists - manual result analysis:
```csv
# From docs/source/optimization/folder_structure.md - summary.csv format
node, selected_module, file, parameters, time
```
Users can see which modules performed best and compare metrics.

Dashboard for visualization:
```bash
autorag dashboard --trial_dir /your/path/to/trial_dir
```
From `docs/source/tutorial.md`: "You can run a dashboard to easily see the result."

What's missing:
- No automated root cause analysis of failures
- No hyperparameter sensitivity analysis
- No suggested next experiments
- No gap analysis identifying underrepresented scenarios
- No impact vs effort estimates
- Users must manually interpret results to plan improvements

Evidence of manual process:
From `docs/source/optimization/optimization.md`:
"Now, you can make your custom config file, write a better config YAML file, and evaluate it again and again for the better result."
Improvement is entirely user-driven based on manual result inspection.