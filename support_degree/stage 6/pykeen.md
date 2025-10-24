# PyKEEN - Stage 6 (RELEASE) Evaluation

## Summary
PyKEEN is a Python library for knowledge graph embedding models. While it excels at model training and evaluation computation, its communication and distribution capabilities are minimal. The framework has no built-in artifact management system, no versioning/reproducibility manifests, no stakeholder-specific reporting, and extremely limited distribution channels. Results are returned as Python objects with some integration with external trackers like MLflow and W&B, but these require manual setup and don't provide comprehensive artifact management out-of-the-box.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 1 | Minimal artifact capture with manual management required. No querying, comparison, or packaging features. |
| S6F2: Version Control | 0 | No git integration, no dependency manifests, no reproducibility tracking beyond random seeds. |
| S6F3: Report Generation | 1 | Single format (Python objects), no templates, basic metric storage only. |
| S6F4: Distribution Channels | 1 | Optional tracker integrations exist but require manual configuration, no native distribution features. |

### S6F1: Evaluation Artifact Management

Rating: 1/3

Runtime Capture:
PyKEEN captures basic metadata during training but lacks comprehensive artifact management:

```python
# From src/pykeen/pipeline/__init__.py
class PipelineResult(NamedTuple):
    """A container for results from running :func:`pipeline`."""
    
    random_seed: int
    model: Model
    training: TriplesFactory
    training_loop: TrainingLoop
    losses: List[float]
    stopper: Stopper | None
    metric_results: MetricResults
```

The `PipelineResult` captures the model, training data, losses, and evaluation metrics, but this is only stored in memory. Evidence from `docs/source/tutorial/checkpoints.rst`:

```rst
To show how to use the checkpoint functionality without the pipeline, we define a KGEM first:

>>> losses = training_loop.train(
...     num_epochs=1000,
...     checkpoint_name='my_checkpoint.pt',
...     checkpoint_frequency=5,
... )
```

Checkpoints save model state but are limited:
- Only saves during training (not evaluation)
- Manual checkpoint naming required
- No automatic metadata capture beyond model state

Querying:
No built-in querying capabilities. Results are Python objects with no database or filtering system. From `docs/source/tutorial/understanding_evaluation.rst`:

```python
# Results are accessed directly from objects
results = evaluator.evaluate(
    model=model,
    mapped_triples=dataset.testing.mapped_triples,
)
```

No API to query past runs, filter by metadata, or search evaluation history.

Comparison:
No comparison interface. Users must manually compare results. The documentation shows no examples of built-in comparison tools or diff utilities.

Packaging:
Checkpoints exist but are minimal:

```python
# From docs/source/tutorial/checkpoints.rst
>>> checkpoint = torch.load(PYKEEN_CHECKPOINTS.joinpath('my_checkpoint.pt'))
>>> checkpoint.keys()  # Contains basic state only
dict_keys(['model_state_dict', 'entity_to_id_dict', 'relation_to_id_dict'])
```

No comprehensive artifact packaging, no bundling of configs/logs/results, no selective packaging options.

Evidence of limitations:
From `docs/source/tutorial/checkpoints.rst`:

```rst
Currently, PyKEEN only supports checkpoints for training loops, implemented in the class
:class:`pykeen.training.TrainingLoop`. When using the :func:`pykeen.pipeline.pipeline` function as defined above, the
pipeline actually uses the training loop functionality. Accordingly, those checkpoints save the states of the
training loop and not the pipeline itself. Therefore, the checkpoints won't contain evaluation results that reside in
the pipeline.
```

### S6F2: Archival Version Control and Reproducibility Manifests

Rating: 0/3

Git Integration:
No git integration found in the codebase. No automatic commit tracking, no detection of uncommitted changes.

Dependency Pinning:
No dependency capture system. The repository has standard Python dependencies in `pyproject.toml` but no runtime capture of the actual environment used for experiments:

```toml
# From pyproject.toml - project dependencies, not runtime capture
dependencies = [
    "pystow>=0.5.1",
    "click",
    "click_default_group",
    ...
]
```

No evidence of `pip freeze`, conda environment export, or lockfile generation during training/evaluation.

Environment Capture:
Random seed is captured (`PipelineResult.random_seed`) but no systematic environment recording:
- No Python version capture
- No CUDA version tracking
- No OS information
- No environment variables

Manifest Generation:
No reproducibility manifests. Checkpoints contain model state but not environment information:

```python
# From checkpoints documentation - only model and mapping state
checkpoint = {
    'model_state_dict': ...,
    'entity_to_id_dict': ...,
    'relation_to_id_dict': ...,
}
```

No comprehensive manifests with all information needed to reproduce results.

Container Packaging:
No Docker image export or containerization features mentioned anywhere in documentation or code.

### S6F3: Stakeholder-Specific Report and Visualization Generation

Rating: 1/3

Format Support:
Results are Python objects only. From `src/pykeen/pipeline/__init__.py`:

```python
class PipelineResult(NamedTuple):
    """A container for results from running :func:`pipeline`."""
    
    model: Model
    training: TriplesFactory
    metric_results: MetricResults
```

No HTML, PDF, CSV export built-in. Users must manually serialize results.

Stakeholder Templates:
No templates. All results have the same format regardless of audience. No executive summaries, technical deep-dives, compliance reports, or research report templates.

Visualization:
Minimal visualization support. From the repository structure, there's a `notebooks/results_plots/results_plots.ipynb` notebook but it's user-created, not framework-provided. The tutorial in `docs/source/tutorial/understanding_evaluation.rst` shows how to access results:

```python
from pykeen.predict import predict_target

df = predict_target(
    model=result.model,
    head="belgium",
    relation="locatedin",
    triples_factory=result.training,
)
```

This returns a DataFrame but no automatic visualization generation. No confusion matrices, ROC curves, calibration plots, or error distributions built-in.

Automation:
No automated report generation. Results must be manually processed and visualized.

Evidence:
The tracker system (`src/pykeen/trackers/`) shows basic logging only:

```python
# From src/pykeen/trackers/base.py
class ResultTracker:
    """Base class for result trackers."""
    
    def log_metrics(self, metrics: Dict[str, float]) -> None:
        """Log metrics."""
        raise NotImplementedError
```

Trackers log scalar metrics but don't generate comprehensive reports.

### S6F4: Publication to Distribution Channels

Rating: 1/3

CI/CD Integration:
No built-in CI/CD integration. The repository has GitHub Actions (`.github/workflows/common.yml`) but these are for development/testing, not for experiment result publishing or automated evaluation pipelines.

MLOps Platforms:
Optional integrations exist but require manual setup. From `src/pykeen/trackers/`:

```
├── trackers
│   ├── console.py
│   ├── csv.py
│   ├── json.py
│   ├── mlflow.py
│   ├── neptune.py
│   ├── tensorboard.py
│   └── wandb.py
```

These trackers exist but from the documentation they're not comprehensive artifact management systems. From README:

```markdown
### Trackers

The following 8 trackers are implemented in PyKEEN.

| Name        | Reference                                                                                   | Description                                               |
|-------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| console     | [`pykeen.trackers.ConsoleResultTracker`]                                                    | A class that directly prints to console.                  |
| csv         | [`pykeen.trackers.CSVResultTracker`]                                                        | Tracking results to a CSV file.                           |
| mlflow      | [`pykeen.trackers.MLFlowResultTracker`]                                                     | A tracker for MLflow.                                     |
| wandb       | [`pykeen.trackers.WANDBResultTracker`]                                                      | A tracker for Weights and Biases.                         |
```

These are basic metric loggers, not full distribution systems. No evidence of:
- Model registry publishing
- Automated experiment tracking platform sync
- Pass/fail gates based on metrics
- Automated evaluation on commits

Public Leaderboards:
No HuggingFace Hub publishing, no Papers with Code integration, no custom leaderboard support mentioned.

Notifications:
No Slack, email, or webhook notifications. No configurable notification rules, no alerts on metric degradation.

Evidence of manual setup:
Users must manually configure trackers. No automated distribution or publication features. The trackers simply forward metrics to external platforms but don't provide comprehensive artifact management or distribution workflows.

## Overall Assessment

PyKEEN is a well-designed research library for training and evaluating knowledge graph embeddings, but it provides minimal communication and distribution capabilities. The framework assumes researchers will handle result management, versioning, and distribution manually or through external tools. 

Strengths:
- Comprehensive evaluation metrics (44+ metrics)
- Rich evaluation protocols (filtered, macro, etc.)
- Basic checkpoint system for training recovery

Critical Gaps:
- No artifact management or querying system
- No reproducibility manifests or version control integration
- No stakeholder-specific reporting or visualization generation
- No automated distribution channels beyond basic external tracker logging
- Results exist only as in-memory Python objects with no structured storage

Recommendation for Users:
PyKEEN is excellent for running experiments but requires significant additional tooling (MLflow, W&B, custom scripts) to manage, version, and distribute results effectively. Organizations would need to build their own artifact management, reporting, and distribution systems around PyKEEN's core training/evaluation capabilities.