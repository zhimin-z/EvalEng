# Ragas - Stage 7 (VALIDATE) Evaluation

## Summary
Ragas provides minimal pre-deployment validation capabilities focused on evaluation workflows rather than deployment gates. The framework emphasizes experiment-driven testing with custom metrics but lacks dedicated quality gate mechanisms, compliance validation features, and ensemble decision-making tools. Most validation is done through manual inspection of experiment results saved to CSV files.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S7F1: Quality Gates | 1 | Manual gate evaluation only through experiment result inspection. No configurable thresholds, automated pass/fail decisions, or deployment recommendations. Users must manually review CSV outputs. |
| S7F2: Compliance Validation | 0 | No compliance features present. No fairness testing, model cards, privacy validation, or regulatory compliance checks. Framework is focused purely on evaluation metrics. |
| S7F3: Ensemble Decisions | 0 | No ensemble capabilities. Framework evaluates single models/systems only. No multi-model orchestration, voting mechanisms, or comparative deployment recommendations. |

---

## Detailed Evidence

### S7F1: Quality Gate Application - Rating: 1/3

Evidence of Manual-Only Gates:

The framework requires manual inspection of experiment results to make deployment decisions. From `docs/tutorials/prompt.md`:

```python
@experiment()
async def run_experiment(row):
    response = run_prompt(row["text"])
    score = my_metric.score(
        prediction=response,
        actual=row["label"]
    )
    experiment_view = {
        row,
        "response":response,
        "score":score.value,
    }
    return experiment_view
```

Results are saved to CSV files for manual review:
```markdown
Voila! You have successfully run your first evaluation using Ragas. You can now inspect the results by opening the `experiments/experiment_name.csv` file.
```

No Automated Quality Gates:

The experiment framework in `src/ragas/experiment.py` only saves results, with no built-in gate evaluation:

```python
# From examples showing workflow
dataset = load_dataset()
experiment_result = await run_experiment.arun(dataset)
print("Experiment_result: ", experiment_result)
```

No Threshold Configuration:

Metrics define scoring logic but not deployment thresholds. From `examples/ragas_examples/agent_evals/evals.py`:

```python
@numeric_metric(name="correctness", allowed_values=(0.0, 1.0))
def correctness_metric(prediction: float, actual: float):
    """Calculate correctness of the prediction."""
    if isinstance(prediction, str) and "ERROR" in prediction:
        return 0.0
    result = 1.0 if abs(prediction - actual) < 1e-5 else 0.0
    return MetricResult(
        value=result, reason=f"Prediction: {prediction}, Actual: {actual}"
    )
```

This defines scoring but provides no threshold for pass/fail deployment decisions.

No Safety or Regression Checks:

No automated safety validation or baseline comparison features exist. The framework focuses on calculating metrics without providing quality gate infrastructure.

Why Not 0 Points:

Users can manually implement gates by inspecting CSV results and comparing scores, but this requires significant custom code outside the framework.

---

### S7F2: Regulatory Compliance Validation - Rating: 0/3

No Compliance Features:

Extensive search through the codebase reveals no fairness testing, explainability tools, privacy validation, or regulatory compliance features.

No Fairness Metrics:

The `src/ragas/metrics/` directory contains only task-specific metrics (faithfulness, answer_relevancy, etc.) with no demographic parity, equalized odds, or other fairness tests.

No Model Cards:

No model card generation capability. The framework focuses on evaluation metrics only.

No Privacy Validation:

No GDPR, CCPA, data minimization, or consent tracking features present in the codebase.

No Certification Support:

No EU AI Act, NIST AI RMF, or ISO/IEC standards support. From the documentation structure in `docs/`, there are no sections on compliance or regulatory validation.

Framework Scope:

The README clearly positions Ragas as an evaluation toolkit, not a compliance framework:
```markdown
Ragas is your ultimate toolkit for evaluating and optimizing Large Language Model (LLM) applications.
```

---

### S7F3: Model Ensemble Decision-Making - Rating: 0/3

Single Model Evaluation Only:

The experiment framework evaluates one model/system at a time. From `examples/ragas_examples/text2sql/evals.py`:

```python
@experiment()
async def text2sql_experiment(
    row,
    model: str,
    prompt_file: Optional[str],
):
    """Experiment function for text-to-SQL evaluation."""
    # Create text-to-SQL agent with single model
    openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    agent = Text2SQLAgent(
        client=openai_client,
        model_name=model,  # Single model parameter
        prompt_file=prompt_file
    )
```

No Multi-Model Orchestration:

The experiment decorator in `src/ragas/experiment.py` processes datasets for a single configuration:

```python
@experiment()
async def run_experiment(row):
    # Evaluates single model/system
    response = agent.query(row["query"])
    return results
```

No Voting or Cascade Mechanisms:

No evidence of voting, cascade strategies, or mixture-of-experts routing. Each experiment run tests one model configuration.

No Comparative Deployment Recommendations:

While users could manually run multiple experiments with different models, the framework provides no built-in comparison or recommendation features.

Manual Model Comparison:

Users must manually compare results from separate experiment runs by inspecting different CSV files - no automated ensemble decision support exists.

---

## Conclusion

Ragas is an evaluation-focused framework that provides minimal Stage 7 (VALIDATE) capabilities. It lacks:

1. Automated quality gates - only manual CSV inspection
2. All compliance validation features - no fairness, privacy, or regulatory tools
3. Any ensemble decision capabilities - single model evaluation only

The framework excels at generating evaluation metrics but does not provide pre-deployment validation infrastructure, compliance checking, or multi-model decision support. Organizations would need to build these capabilities externally using Ragas metrics as inputs.