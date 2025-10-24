# Quantus - Stage 6 (RELEASE) Evaluation

## Summary
Quantus is an XAI evaluation toolkit with minimal communication capabilities. It focuses on programmatic evaluation without dedicated artifact management, versioning, or distribution features. Results are returned as Python objects/lists with no built-in persistence, comparison, or reporting infrastructure.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 0 | No artifact management system exists. Results are returned as Python lists/arrays with no automatic capture, storage, or querying capabilities |
| S6F2: Version Control | 0 | No version control integration, dependency tracking, or reproducibility manifests are implemented |
| S6F3: Report Generation | 1 | Basic matplotlib plotting exists but no stakeholder-specific templates, automated reporting, or multiple output formats |
| S6F4: Distribution Channels | 0 | No CI/CD integrations, MLOps platform connections, or notification systems are present |

---

## Detailed Analysis

### S6F1: Evaluation Artifact Management (Rating: 0/3)

Evidence:

1. No Runtime Capture System: The base metric class only stores results in memory as Python lists:
   ```python
   # quantus/metrics/base.py
   class Metric(Generic[R]):
       def __init__(self, ...):
           self.evaluation_scores = []
           self.all_evaluation_scores = []
       
       def __call__(self, ...):
           # Results are just appended to lists
           self.all_evaluation_scores.extend(self.evaluation_scores)
           return self.evaluation_scores
   ```

2. No Metadata Capture: There's no automatic capture of:
   - Timestamps
   - Model configurations
   - Hyperparameters used
   - Execution environment details
   
   The `get_params` property only returns current metric parameters, not execution metadata:
   ```python
   # quantus/metrics/base.py
   @property
   def get_params(self) -> Dict[str, Any]:
       """List parameters of metric."""
       attr_exclude = [
           "args", "kwargs", "all_evaluation_scores",
           "evaluation_scores", "default_plot_func",
       ]
       return {k: v for k, v in self.__dict__.items() if k not in attr_exclude}
   ```

3. No Querying Capability: Results are stored as simple Python lists with no:
   - Filtering by metadata
   - Query API
   - Database or structured storage
   - Run comparison interface

4. No Packaging: The library provides no functionality to:
   - Bundle results with configurations
   - Create archives of evaluation runs
   - Export results in structured formats (beyond raw Python objects)

Conclusion: Quantus has zero artifact management infrastructure. Users must manually save, organize, and track their evaluation results.

---

### S6F2: Archival Version Control and Reproducibility Manifests (Rating: 0/3)

Evidence:

1. No Git Integration: Searching the codebase reveals no git-related functionality:
   - No commit tracking
   - No detection of uncommitted changes
   - No linking of runs to git commits

2. No Dependency Tracking: The library doesn't capture:
   - Package versions (pip freeze, conda list)
   - System dependencies
   - Python version used during evaluation
   
   The `pyproject.toml` defines dependencies but doesn't track what's installed at runtime:
   ```toml
   # pyproject.toml
   dependencies = [
       "numpy>=1.19.5",
       "pandas>=1.5.3",
       # ... other deps
   ]
   ```

3. No Environment Capture: There's no recording of:
   - CUDA version
   - OS details
   - Environment variables
   - Random seeds (users must manage this themselves)

4. No Reproducibility Manifests: The library doesn't generate:
   - Comprehensive reproducibility documents
   - Machine-readable configuration files for re-execution
   - Container definitions

5. No Container Support: No Docker or containerization features for reproducibility.

Conclusion: Quantus provides zero versioning or reproducibility infrastructure. All reproducibility management is left to the user.

---

### S6F3: Stakeholder-Specific Report and Visualization Generation (Rating: 1/3)

Evidence:

1. Minimal Plotting Support: Basic matplotlib plotting exists but is rudimentary:
   ```python
   # quantus/metrics/base.py
   def plot(self, plot_func: Optional[Callable] = None, show: bool = True,
            path_to_save: Optional[str] = None, *args, kwargs) -> None:
       """Basic plotting functionality for Metric class."""
       if plot_func is None:
           plot_func = self.default_plot_func
       
       asserts.assert_plot_func(plot_func=plot_func)
       plot_func(*args, kwargs)
       
       if show:
           plt.show()
       if path_to_save:
           plt.savefig(fname=path_to_save, dpi=400)
   ```

2. No Stakeholder Templates: There are no pre-built templates for:
   - Executive summaries
   - Technical deep-dives
   - Compliance reports
   - Research reports

3. No Format Diversity: The library only supports:
   - Matplotlib plots (saved as images)
   - Raw Python objects/lists as output
   
   No support for:
   - HTML reports
   - PDF generation
   - CSV/Parquet export
   - Interactive dashboards
   - Jupyter notebook integration (beyond manual usage)

4. No Automation: There's no automated report generation system. The `interpret_scores()` method only prints docstring text:
   ```python
   # quantus/metrics/base.py
   def interpret_scores(self):
       """Get an interpretation of the scores."""
       print(self.__init__.__doc__.split(".")[1].split("References")[0])
   ```

5. Limited Visualization Helper: The `quantus/helpers/plotting.py` file exists but provides only basic utilities:
   ```python
   # From file structure - no implementation shown in provided code
   # ├── helpers
   # │   ├── plotting.py
   ```

Conclusion: While basic plotting exists, there are no comprehensive reporting features, templates, or automated generation capabilities.

---

### S6F4: Publication to Distribution Channels (Rating: 0/3)

Evidence:

1. No CI/CD Integration: The repository has test infrastructure (pytest, tox) but no evaluation distribution features:
   ```toml
   # pyproject.toml - only test infrastructure
   [project.optional-dependencies]
   tests = [
       "pytest<=7.4.4",
       "pytest-cov>=4.0.0",
       # ... testing deps only
   ]
   ```

2. No MLOps Platform Integration: Searching the codebase reveals:
   - No MLflow integration
   - No Weights & Biases support
   - No Neptune.ai connection
   - No Comet.ml integration
   
   The library focuses solely on local computation.

3. No Model Registry Publishing: There's no functionality to:
   - Publish results to model registries
   - Sync with experiment tracking platforms
   - Integrate with deployment pipelines

4. No Leaderboard Support: The library doesn't support:
   - HuggingFace Hub publishing
   - Papers with Code integration
   - Custom leaderboard creation

5. No Notification System: There's no support for:
   - Slack notifications
   - Email alerts
   - Webhook integrations
   - Metric degradation alerts

6. GitHub Actions Present: The README mentions GitHub Actions badges:
   ```md
   # README.md
   [![Python package](https://github.com/...)]
   [![Code coverage](https://github.com/...)]
   ```
   However, these are for library development (testing, coverage), not for evaluation distribution.

Conclusion: Quantus has zero distribution capabilities. It's purely a local computation library with no integrations for publishing or sharing results.

---

## Key Observations

### What Quantus Does Well:
1. Programmatic Evaluation: Clean Python API for running evaluations
2. Extensibility: Well-structured base classes for custom metrics
3. Documentation: Good API documentation and tutorials (but not for communication features)

### Critical Gaps:
1. No Persistence: Results exist only in memory during execution
2. No Experiment Tracking: Users must manually track all evaluation runs
3. No Collaboration Features: No built-in way to share or compare results
4. Manual Reproducibility: All reproducibility concerns are user responsibility

### User Experience Impact:
From `tutorials/Tutorial_Getting_Started.ipynb`, users manually manage everything:
```python
# Users must manually save results
scores = metric(model=model, x_batch=x_batch, y_batch=y_batch, ...)

# No automatic saving, versioning, or reporting
# Users must implement their own:
# - pd.DataFrame(scores).to_csv("results.csv")
# - Custom plotting
# - Manual comparison of runs
```

### Total Stage 6 Score: 1/12

Quantus is a computation-focused library with virtually no communication infrastructure. It excels at calculating metrics but provides no support for artifact management, versioning, reporting, or distribution. Users must build their own infrastructure for tracking, comparing, and sharing evaluation results.