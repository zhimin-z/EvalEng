# jitsi__jiwer - Stage 6 (COMMUNICATE) Evaluation

## Summary
JiWER is a minimalist evaluation library focused exclusively on computing ASR metrics (WER, MER, WIL, WIP, CER). It is a pure calculation library with no evaluation orchestration capabilities. As such, it has virtually no Stage 6 communication features—no artifact management, no versioning integration, no reporting generation, and no distribution channel support. Users must build all communication infrastructure themselves.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 0 | No artifact management exists. The library returns Python objects (`WordOutput`, `CharacterOutput`) that users must manually save. No automatic metadata capture, no querying capabilities, no comparison tools, and no packaging features. Evidence: Core API in `src/jiwer/process.py` only returns dataclass objects with no persistence logic. |
| S6F2: Version Control | 0 | No version control integration whatsoever. No git tracking, no dependency pinning, no environment capture, no reproducibility manifests, and no container support. Evidence: `pyproject.toml` shows a simple package config with no versioning hooks; no code references version control systems. |
| S6F3: Report Generation | 1 | Minimal text-based visualization only. Has `visualize_alignment()` and `visualize_error_counts()` functions that generate ASCII art alignment displays to stdout, but no stakeholder-specific reports, no multiple formats (only text), no templates, and no automation. Evidence: `src/jiwer/alignment.py` lines 55-159 show single visualization function returning plain strings. |
| S6F4: Distribution Channels | 0 | No distribution capabilities. No CI/CD integration, no MLOps platform connections, no leaderboard publishing, and no notification system. Evidence: GitHub Actions workflow (`.github/workflows/pythonpackage.yml`) only runs tests, does not publish results. CLI (`src/jiwer/cli.py`) only prints WER/CER to stdout. |

## Detailed Analysis

### S6F1: Evaluation Artifact Management (0/3)

Runtime Capture:
The library provides no automatic artifact capture. When you run an evaluation, you simply get a Python object back:

```python
# From src/jiwer/process.py
@dataclass
class WordOutput:
    references: List[List[str]]
    hypotheses: List[List[str]]
    alignments: List[List[AlignmentChunk]]
    wer: float
    mer: float
    wil: float
    wip: float
    hits: int
    substitutions: int
    insertions: int
    deletions: int
```

No timestamps, no run IDs, no automatic logging—just the raw computation results. Users must manually serialize if they want to save results.

Querying:
No querying capabilities exist. There's no database, no storage layer, no metadata tracking.

Comparison:
No built-in comparison tools. The library can compute metrics for multiple sentences at once, but provides no interface for comparing runs or generating diff reports.

Packaging:
No packaging functionality. The library doesn't bundle results, logs, or configs into archives.

Evidence: The entire codebase is focused on computation. No file I/O except for the CLI reading input files (`src/jiwer/cli.py` lines 65-71):
```python
with reference_file.open("r") as f:
    reference_sentences = [ln.strip() for ln in f.readlines() if len(ln.strip()) > 1]
```

### S6F2: Archival Version Control and Reproducibility Manifests (0/3)

Git Integration:
No git integration. The library doesn't track commits, detect uncommitted changes, or link runs to repository state.

Dependency Pinning:
While `pyproject.toml` has dependencies listed, there's no automatic capture of the runtime environment:
```toml
# From pyproject.toml
dependencies = [
    "click>=8.1.8",
    "rapidfuzz>=3.9.7",
]
```
This is just standard package metadata, not reproducibility tracking.

Environment Capture:
No environment capture. The library doesn't record Python version, CUDA version, OS, environment variables, or random seeds at runtime.

Manifest Generation:
No reproducibility manifests are generated. Users get computation results only.

Container Packaging:
No Docker or container support.

Evidence: Searching the entire codebase for "git", "commit", "environment", "manifest", "docker" yields no relevant results. The library is purely focused on metric calculation.

### S6F3: Stakeholder-Specific Report and Visualization Generation (1/3)

Format Support:
Only plain text/ASCII art output. The visualization functions return strings:

```python
# From src/jiwer/alignment.py lines 55-159
def visualize_alignment(
    output: Union[WordOutput, CharacterOutput],
    show_measures: bool = True,
    skip_correct: bool = True,
    line_width: Optional[int] = None,
) -> str:
    """
    Visualize the output...
    Returns:
        (str): The visualization as a string
    """
```

Example output from docs:
```txt
=== SENTENCE 1 ===

REF:    # short one here
HYP: shoe order one    *
        I     S        D

=== SENTENCE 2 ===

REF: quite a bit of  #    #  longer sentence    #
HYP: quite * bit of an even longest sentence here
           D         I    I       S             I
```

No HTML, PDF, JSON, CSV, or interactive formats.

Stakeholder Templates:
No templates. The visualization is generic for all audiences—there's no executive summary mode vs. technical deep-dive.

Visualization:
Only ASCII-based alignment visualization and error count tables. No charts, graphs, confusion matrices, ROC curves, or any graphical output. The `visualize_error_counts()` function (lines 333-419) produces text tables:

```txt
=== SUBSTITUTIONS ===
short   --> order   = 1x
longer  --> longest = 1x

=== INSERTIONS ===
shoe    = 1x
```

Automation:
No automation. Visualization must be manually called and printed.

Justification for 1 point: While the visualization is basic, it does provide human-readable alignment and error analysis that can be useful for technical debugging. This minimal capability warrants 1 point rather than 0, but it's far from comprehensive reporting.

### S6F4: Publication to Distribution Channels (0/3)

CI/CD Integration:
The GitHub Actions workflow only runs tests, doesn't publish evaluation results:

```yaml
# From .github/workflows/pythonpackage.yml
- name: Test with pytest
  run: |
    uv run python --version
    uv run pytest
```

No pass/fail gates based on WER thresholds, no automated evaluation on commits.

MLOps Platforms:
No integrations with MLflow, W&B, Neptune, Comet, or any tracking platform. The library is completely standalone.

Public Leaderboards:
No HuggingFace Hub integration, no Papers with Code integration, no leaderboard support.

Notifications:
No notification system. The CLI only prints to stdout:

```python
# From src/jiwer/cli.py lines 111-116
if show_alignment:
    print(jiwer.visualize_alignment(out, show_measures=True), end="")
else:
    if compute_cer:
        print(out.cer)
    else:
        print(out.wer)
```

No Slack, email, webhooks, or any other notification mechanism.

Evidence: The entire distribution mechanism is PyPI package publication (`pyproject.toml` and `.github/workflows/pythonpublish.yml`), which is for distributing the library itself, not evaluation results.

## Key Observations

1. Pure Computation Library: JiWER is designed solely for calculating ASR metrics. It's a utility library, not an evaluation framework. Users must build all orchestration, tracking, and communication infrastructure themselves.

2. No State Management: The library is stateless—it takes inputs, computes metrics, returns results. No persistence layer exists.

3. Minimal Visualization: The 1 point for reporting comes from basic ASCII visualization functions that at least provide human-readable alignment output for debugging.

4. Documentation Focus: The documentation (`docs/`) explains how to use the library for computations but makes no mention of artifact management, versioning, or distribution because these features don't exist.

5. Appropriate Scope: This isn't a failing of the library—it's intentionally scoped as a metric computation tool, not a full evaluation framework. Users wanting Stage 6 features would need to combine jiwer with other tools.

## Recommendation

For users needing Stage 6 capabilities, jiwer should be used as a metric computation component within a larger evaluation framework (like Gantry, PromptTools, etc.) that provides artifact management, versioning, reporting, and distribution features. It excels at its narrow purpose but offers essentially nothing for result communication and distribution.