# speech-to-text-benchmark - Stage 6 (COMMUNICATE) Evaluation

## Summary
This framework is a minimalist speech-to-text benchmarking tool with basic result storage and visualization capabilities. It provides simple file-based artifact storage and generates static comparison plots, but lacks comprehensive versioning, reproducibility manifests, and distribution channel integrations. The framework is primarily designed for publishing static benchmark results rather than for production evaluation workflows.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 1 | Minimal logging with manual artifact management |
| S6F2: Version Control | 0 | No versioning features |
| S6F3: Report Generation | 2 | Basic templates with standard plots, limited format support |
| S6F4: Distribution Channels | 1 | Manual publishing, no integrations |

### S6F1: Evaluation Artifact Management (1/3 points)

Runtime Capture:
The framework provides minimal metadata capture:
- Results are saved to simple text files (`.log` extension) with basic metrics
- No structured metadata about execution context, timestamps, or configuration
- Cache files store intermediate transcripts but not comprehensive run information

Evidence from `benchmark.py` (lines 189-198):
```python
results_log_path = os.path.join(RESULTS_FOLDER, language.value, dataset_name.value, f"{str(engine_name)}.log")
os.makedirs(os.path.dirname(results_log_path), exist_ok=True)
with open(results_log_path, "w") as f:
    for metric_name, metric_results in metric_results.items():
        num_errors = sum(x.num_errors for x in metric_results)
        num_tokens = sum(x.num_tokens for x in metric_results)
        error_rate = 100 * float(num_errors) / num_tokens

        f.write(f"{metric_name}: {str(error_rate)}\n")
```

Querying:
- No querying capabilities
- No API or interface for filtering/searching runs
- Results are stored in flat file hierarchy: `results/{language}/{dataset}/{engine}.log`

Comparison:
- No built-in comparison interface or diff tools
- Manual comparison requires parsing log files or viewing generated plots
- `plot_results.py` creates comparison visualizations but no interactive tools

Packaging:
- No bundling of results, logs, or configs into archives
- Each result is a standalone file with no relationship metadata
- No compression or efficient storage mechanisms

Evidence from directory structure:
```
results/
└── plots/
    ├── WER.png
    ├── WER_FR.png
    └── ...
```

### S6F2: Archival Version Control and Reproducibility Manifests (0/3 points)

Git Integration:
- No automatic commit tracking
- No linkage between runs and git commits
- No detection of uncommitted changes

Dependency Pinning:
- Has `requirements.txt` but no automatic capture during runs
- No lockfile generation or version tracking
- No system library version tracking

Evidence from `requirements.txt`:
```txt
amazon-transcribe==0.6.4
azure-cognitiveservices-speech
boto3
editdistance
...
```
(Static file, not generated per-run)

Environment Capture:
- No recording of Python version, CUDA version, or OS
- No environment variable capture
- Random seed handling not present (no seed management visible in code)

Manifest Generation:
- No reproducibility manifests
- No machine-executable reproduction information
- Configuration is passed via command-line arguments only

Example from `benchmark.py` showing CLI-only configuration:
```python
parser.add_argument("--engine", required=True, choices=[x.value for x in Engines])
parser.add_argument("--dataset", required=True, choices=[x.value for x in Datasets])
parser.add_argument("--dataset-folder", required=True)
parser.add_argument("--language", required=True, choices=[x.value for x in Languages])
```

Container Packaging:
- No Docker support
- No containerized reproducibility

### S6F3: Stakeholder-Specific Report and Visualization Generation (2/3 points)

Format Support:
- PNG images for plots
- Plain text `.log` files for metrics
- No HTML, PDF, JSON, CSV export for results
- No interactive dashboards or notebooks

Evidence from `plot_results.py` (line 149):
```python
plt.savefig(save_path)
print(f"Saved plot to `{save_path}`")
```

Stakeholder Templates:
- No explicit stakeholder templates
- README provides basic result tables (could be considered a basic template)
- Results are hardcoded in Python dictionaries in `results.py` for static display

Evidence from `results.py` showing hardcoded results:
```python
WER_EN = {
    Engines.AMAZON_TRANSCRIBE: {
        Datasets.COMMON_VOICE: 6.4,
        Datasets.LIBRI_SPEECH_TEST_CLEAN: 2.3,
        ...
    },
    ...
}
```

Visualization:
- Good variety of plot types: WER comparisons, latency comparisons, CPU usage, scatter plots
- Standard matplotlib visualizations (bar charts, scatter plots)
- Customizable colors and labels for different engines
- No confusion matrices, calibration plots, or ROC/PR curves (not applicable for STT)

Evidence from `plot_results.py` showing visualization types (lines 48-118):
```python
def _plot_error_rate(...):
    # Bar chart visualization
    for i, (engine, error_rate) in enumerate(sorted_error_rates, start=1):
        color = ENGINE_COLORS[engine]
        ax.bar([i], [error_rate], 0.4, color=color)
```

```python
def _plot_error_rate_latency_grid(...):
    # Scatter plot visualization
    ax.scatter(error_rates, latencies, color=colors, s=150, alpha=0.8, ...)
```

Automation:
- Script-based plot generation (`plot_results.py`)
- No automated report generation on benchmark completion
- No scheduled report generation
- Manual invocation required

Evidence from `plot_results.py` main function:
```python
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    
    save_folder = os.path.join(RESULTS_FOLDER, "plots")
    _plot_error_rate(WER_EN, save_path=os.path.join(save_folder, "WER.png"), ...)
```

### S6F4: Publication to Distribution Channels (1/3 points)

CI/CD Integration:
- No GitHub Actions, GitLab CI, or Jenkins integration
- No pass/fail gates based on metrics
- No automated evaluation on commits

MLOps Platforms:
- No MLflow, W&B, Neptune, or Comet integration
- No model registry publishing
- No experiment tracking platform sync

Public Leaderboards:
- Results are published manually to README
- No HuggingFace Hub integration
- No Papers with Code integration
- No automated leaderboard updates

Evidence from README showing manual result tables:
```md
#### Batch Engines Word Error Rate

|             Engine             | LibriSpeech test-clean | ... |
|:------------------------------:|:----------------------:|:---:|
|       Amazon Transcribe        |          2.3%          | ... |
```

Notifications:
- No Slack, email, or webhook notifications
- No configurable notification rules
- No alerts on metric degradation

Manual Distribution:
The framework appears designed for manual result publication:
1. Run benchmarks → generates `.log` files
2. Run `plot_results.py` → generates PNG plots
3. Manually update README with results
4. Commit and push to GitHub

Evidence: No automation scripts or CI configuration files present in repository.

## Summary Assessment

Strengths:
1. Clean visualization generation with good plot variety
2. Simple, understandable result storage structure
3. Effective for static benchmark publication

Weaknesses:
1. No structured artifact management or querying
2. Complete absence of versioning and reproducibility features
3. No integration with modern MLOps or CI/CD tools
4. Manual workflow throughout - no automation
5. No stakeholder-specific reporting capabilities
6. Results hardcoded in Python rather than dynamically generated

Overall Stage 6 Score: 4/12 points

This framework is suitable for one-time benchmark publication but inadequate for iterative evaluation workflows, team collaboration, or reproducible research. It lacks the infrastructure needed for professional evaluation management.