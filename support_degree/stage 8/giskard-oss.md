# Giskard - Stage 8 (MONITOR) Evaluation

## Summary
Giskard is an open-source testing and evaluation framework for ML models (tabular to LLMs) that focuses primarily on pre-deployment scanning and testing. The framework has minimal native support for production monitoring and continuous improvement features typical of Stage 8 (MONITOR). While it provides excellent vulnerability detection and testing capabilities, it lacks dedicated infrastructure for drift monitoring, online evaluation, feedback loops, and automated improvement recommendations in production environments.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S8F1: Drift Monitoring | 0 | No drift monitoring capabilities found. The framework focuses on pre-deployment scanning rather than production monitoring. No statistical drift tests, performance degradation tracking, or alerting systems are present in the codebase. |
| S8F2: Online Evaluation | 0 | No online or streaming evaluation support. All evaluation is offline/batch-based. No A/B testing, shadow deployment, or automated rollback features exist. The MLflow integration (`docs/integrations/mlflow/index.md`) only supports batch evaluation via `mlflow.evaluate()`. |
| S8F3: Feedback Integration | 1 | Minimal feedback support. The framework can generate test suites from scan results (`scan_results.generate_test_suite()`), but there's no automatic production feedback ingestion, failure mining from production logs, or closed-loop automation. The integration is manual and requires developer intervention. |
| S8F4: Improvement Planning | 1 | Basic improvement recommendations via scan reports. The scan generates vulnerability reports with examples (`giskard/scanner/common/examples.py`), but lacks automated root cause analysis, hyperparameter recommendations, or structured roadmap generation. Recommendations are descriptive rather than actionable. |

## Detailed Analysis

### S8F1: Production Drift Monitoring (Rating: 0)

Evidence of absence:

1. No drift detection modules: Searching the codebase shows no drift monitoring functionality:
   - No statistical tests (KS test, chi-square, MMD) for distribution shift detection
   - No drift scoring or per-feature drift analysis
   - The `giskard/scanner/` directory contains various detectors but none for drift monitoring

2. Focus on pre-deployment: From `README.md`:
```markdown
Giskard is an open-source Python library that automatically detects performance, 
bias & security issues in AI applications. The library covers LLM-based applications 
such as RAG agents, all the way to traditional ML models for tabular data.
```

3. No production monitoring infrastructure: 
   - No logging infrastructure integration
   - No streaming data support
   - No alerting mechanisms for production metrics
   - The CI/CD integration (`docs/integrations/cicd/index.md`) only runs scans on commits, not continuous production monitoring

4. Test framework nature: The core architecture shows testing rather than monitoring:
   - `giskard/core/suite.py` - Test suite execution
   - `giskard/scanner/scanner.py` - Scan execution (offline)
   - No time-series tracking or trend analysis

Rating Justification: 0 points - No drift monitoring capabilities exist. The framework is designed for pre-deployment testing, not production monitoring.

---

### S8F2: Online and Streaming Evaluation (Rating: 0)

Evidence of absence:

1. No streaming support: All evaluation is batch-based:
   - From `giskard/datasets/base/__init__.py`, datasets are loaded as pandas DataFrames
   - No streaming data pipelines or real-time evaluation infrastructure
   - No sliding window analysis or low-latency evaluation

2. No A/B testing capabilities:
   - No traffic splitting functionality
   - No multi-variant testing support
   - No gradual rollout mechanisms
   - The CI/CD example (`docs/integrations/cicd/pipeline.ipynb`) shows binary pass/fail, not A/B comparison:
```python
if scan_results.has_vulnerabilities:
    print("Your model has vulnerabilities")
    exit(1)
```

3. No shadow deployment support:
   - No infrastructure to run candidate models alongside production
   - No side-by-side comparison in production
   - All model evaluation is offline via `giskard.scan(wrapped_model, wrapped_dataset)`

4. No automated rollback:
   - No metric-based rollback triggers
   - No automatic fallback mechanisms
   - Manual intervention required for all deployment decisions

5. MLflow integration limitations: From `docs/integrations/mlflow/index.md`:
```python
with mlflow.start_run(run_name="my_run") as run:
  model_uri = mlflow.sklearn.log_model(..., pyfunc_predict_fn="predict_proba").model_uri
  mlflow.evaluate(model=model_uri,
                  model_type="classifier",
                  data=df_sample,  # Offline data only
                  evaluators="giskard",
                  evaluator_config=evaluator_config)
```
This is clearly offline batch evaluation, not online/streaming.

Rating Justification: 0 points - No online or streaming evaluation capabilities. All evaluation is offline and batch-based.

---

### S8F3: Feedback Loop Integration (Rating: 1)

Limited feedback support found:

1. Test suite generation from scan results: From `README.md`:
```python
# Can generate test suite from scan results
test_suite = scan_results.generate_test_suite("My first test suite")
```

2. Example extraction: The framework can extract failure examples from scan results (`giskard/scanner/common/examples.py`):
```python
class ExampleExtractor:
    def __init__(self, issue: Issue, filter_fn: Optional[Callable] = None, 
                 sorting_fn: Optional[Callable] = None):
        self.issue = issue
        self.filter_fn = filter_fn
        self.sorting_fn = sorting_fn

    def get_examples_dataframe(self, n=3, with_prediction: Union[int, bool] = 1):
        # Returns examples of failures
```

3. Manual feedback integration: The framework allows manual incorporation of issues into test suites, but this requires developer action:
   - No automatic production log parsing
   - No automatic failure mining from production
   - No real-time feedback ingestion
   - No closed-loop automation

4. No metric updates: From the scan configuration (`docs/integrations/mlflow/mlflow-llm-example.ipynb`):
```python
evaluator_config = {
    "model_config": {"classification_labels": ["no", "yes"]},
    "dataset_config": {"name": "Articles"},
    "scan_config": {"params": {"text_perturbation": {"num_samples": 1000}}}
}
```
These are static configurations, not dynamically updated based on production feedback.

5. CI/CD integration: From `docs/integrations/cicd/index.md`, the integration is reactive (on commits) not proactive (continuous production monitoring):
```markdown
Adding Giskard to your CI/CD pipeline will allow you to run the test or 
scan on every commit to your repository
```

Rating Justification: 1 point - Minimal feedback support exists through manual test suite generation from scan results, but no automatic production feedback ingestion, failure mining, or closed-loop automation. All integration is manual and requires developer intervention.

---

### S8F4: Iteration Planning and Improvement Recommendations (Rating: 1)

Basic recommendation capabilities:

1. Scan reports with examples: From `giskard/scanner/common/examples.py`:
```python
def get_examples_dataframe(self, n=3, with_prediction: Union[int, bool] = 1):
    issue = self.issue
    dataset = issue.dataset.slice(issue.slicing_fn) if issue.slicing_fn else issue.dataset
    
    # Filter if needed
    if self.filter_fn:
        dataset = self.filter_fn(issue, dataset)
    
    examples = dataset.df.copy()
    
    # Keep only interesting columns
    cols_to_show = issue.features
```
This provides examples of failures but not actionable recommendations.

2. Issue categorization: From `giskard/scanner/issues.py`:
```python
@dataclass
class Issue:
    model: BaseModel
    dataset: Dataset
    group: IssueGroup
    level: IssueLvel
    description: str
    # ... metadata about the issue
```
Issues are categorized but no automated recommendations are generated.

3. AVID taxonomy integration: From `docs/integrations/avid/index.md`:
```markdown
By default, all Giskard scan reports indicate the AVID taxonomy categories 
that are relevant to the detected vulnerabilities.
```
This provides standardized categorization but not improvement recommendations.

4. No automated root cause analysis:
   - No causal analysis tools
   - No error pattern analysis beyond examples
   - No bottleneck identification

5. No hyperparameter recommendations:
   - No sensitivity analysis
   - No suggested search spaces
   - No impact estimates

6. No prompt optimization: For LLMs, from `README.md`:
```python
# Scan can detect issues like:
# - Hallucinations
# - Harmful content generation  
# - Prompt injection
# - Sensitive information disclosure
```
But no automated prompt modification suggestions or A/B test recommendations.

7. No roadmap generation:
   - No structured experiment plans
   - No prioritized improvement lists
   - No impact vs effort estimates
   - The scan reports are descriptive, not prescriptive

8. Manual test customization: From `docs/open_source/customize_tests/test_model/index.md` (referenced in docs):
```markdown
Customizable Tests: Giskard generates tailored tests based on the detected 
vulnerabilities. You can further customize these tests by defining 
domain-specific data slicers and transformers.
```
This requires manual intervention, not automated recommendations.

Rating Justification: 1 point - The framework provides basic error analysis through scan reports with failure examples and categorization, but lacks automated root cause analysis, hyperparameter recommendations, prompt optimization suggestions, or structured improvement roadmaps. All recommendations are descriptive (what failed) rather than prescriptive (how to fix).

---

## Summary Assessment

Giskard is fundamentally a pre-deployment testing and evaluation framework, not a production monitoring solution. Its strengths lie in:

- Automated vulnerability detection before deployment
- Comprehensive test suite generation
- Integration with ML platforms (MLflow, W&B, HuggingFace)
- CI/CD integration for pre-deployment gates

However, for Stage 8 (MONITOR) requirements, it has critical gaps:

- No drift monitoring infrastructure or statistical tests
- No online/streaming evaluation - all evaluation is offline batch
- Minimal feedback integration - manual test suite generation only
- Basic recommendations - descriptive issue reports without actionable improvement plans

The framework is better suited for Stages 4-7 (TEST/EVALUATE) rather than Stage 8 (MONITOR). Organizations would need to integrate Giskard with separate production monitoring tools (Prometheus, Grafana, custom dashboards) to achieve comprehensive Stage 8 capabilities.

Total Score: 2/12 points