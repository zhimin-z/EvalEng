# ranx - Stage 6 (COMMUNICATE) Evaluation

## Summary
ranx is a Python library for ranking evaluation and comparison in Information Retrieval. It provides strong artifact management through saved run results and scores, but lacks comprehensive versioning/reproducibility features and has minimal distribution capabilities. Reporting is present but basic, with limited stakeholder-specific formats.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 2 | Run metadata capture exists but is limited; comparison/querying capabilities are minimal |
| S6F2: Version Control | 1 | No git integration, dependency tracking, or reproducibility manifests |
| S6F3: Report Generation | 2 | Basic HTML/LaTeX/JSON reports with statistical tests, but no stakeholder templates or rich visualizations |
| S6F4: Distribution Channels | 1 | Manual save/load only; no CI/CD, MLOps platform integrations, or notifications |

## Detailed Analysis

### S6F1: Evaluation Artifact Management (Rating: 2/3)

Evidence of Basic Artifact Management:

1. Runtime Capture - Partial: Run objects store scores but limited metadata
   ```python
   # From ranx/data_structures/run.py (implied from usage)
   # Runs store mean_scores and per-query scores
   run.mean_scores  # Stores metric scores
   run.scores       # Stores per-query scores
   ```

2. Saved Results: Results can be persisted to multiple formats
   ```python
   # From docs/run.md
   run.save("path/to/run.json")     # Save as JSON file
   run.save("path/to/run.trec")     # Save as TREC-Style file
   run.save("path/to/run.lz4")      # Save as lz4 file
   run.save("path/to/run.parquet")  # Save as Parquet file
   ```

3. No Querying Interface: No evidence of filtering runs by metadata, date ranges, or complex queries. Files must be manually loaded.

4. No Comparison Tools: While statistical comparison exists (`compare` function), there's no artifact-level comparison of configurations or metadata.

5. Basic Packaging: Supports compression (LZ4) but no selective packaging or directory structure preservation
   ```python
   # From ranx/io.py
   def save_lz4(content: dict, path: str) -> None:
       path = Path(path)
       path.parent.mkdir(parents=True, exist_ok=True)
       with lz4.frame.open(path, mode="wb") as f:
           f.write(lz4.frame.compress(cbor2.dumps(content), compression_level=16))
   ```

Limitations:
- No automatic timestamp tracking
- No execution logs or traces captured
- No metadata query API
- No run comparison interface beyond statistical tests
- No bundled archives with configs

Rating Justification: Basic metadata through scores storage and multiple save formats warrant 2 points, but lack of querying, comprehensive metadata capture, and comparison tools prevent a 3.

---

### S6F2: Archival Version Control and Reproducibility Manifests (Rating: 1/3)

Evidence:

1. No Git Integration: No automatic commit tracking or detection of uncommitted changes
   - Searched codebase: no git-related functionality found

2. No Dependency Pinning: No capture of pip freeze, conda list, or lockfiles
   - `requirements.txt` exists for the library itself, but no user experiment dependency tracking

3. No Environment Capture: No recording of Python version, CUDA, OS, environment variables, or random seeds
   - Users must manually track these

4. Minimal Run Metadata: Only run name is tracked
   ```python
   # From docs/qrels.md and docs/run.md
   qrels = Qrels(qrels_dict, name="MSMARCO")
   run = Run(run_dict, name="bm25")
   ```

5. No Manifest Generation: No reproducibility manifests or container packaging support

6. ranxhub Metadata: The ranxhub feature includes YAML-based run cards, but this is for sharing pre-computed runs, not reproducibility
   ```python
   # From ranx/ranxhub.py
   def save(run: Run, runcard_path: str, path: str) -> None:
       with open(runcard_path, "r") as f:
           runcard = yaml.load(f, Loader=yaml.Loader)
       # Adds metric scores to runcard
   ```
   This is more about documentation than reproducibility.

Limitations:
- No automated versioning of any kind
- Users must manually track all environment details
- No reproducibility guarantees

Rating Justification: The complete absence of git integration, dependency tracking, environment capture, and reproducibility manifests results in a 1. The manual run name is insufficient for reproducibility.

---

### S6F3: Stakeholder-Specific Report and Visualization Generation (Rating: 2/3)

Evidence of Reporting Capabilities:

1. Format Support - Limited:
   ```python
   # From ranx/data_structures/report.py (implied from docs)
   # Supports: plain text (print), LaTeX, JSON, dict
   print(report)  # Tabular text format
   report.to_latex()  # LaTeX table
   report.to_dict()   # Python dict
   report.save("report.json")  # JSON file
   ```
   No HTML dashboards, PDF, CSV, or interactive notebooks.

2. No Stakeholder Templates: Single generic report format for all audiences
   ```python
   # From docs/compare.md and notebooks/4_comparison_and_report.ipynb
   report = compare(
       qrels=qrels,
       runs=[run_1, run_2, run_3, run_4, run_5],
       metrics=["map@100", "mrr@100", "ndcg@10"],
       max_p=0.01,
   )
   ```
   Output is the same regardless of audience (executive vs. technical vs. compliance).

3. Basic Visualization: Only one plot type (Interpolated Precision-Recall Curve)
   ```python
   # From docs/report.md and notebooks/7_plot.ipynb
   from ranx import plot
   plot(qrels, runs, graph="iprec_at_recall", figsize=(8, 5))
   ```
   No confusion matrices, ROC curves, error distributions, or custom visualizations.

4. Statistical Test Integration: Reports include significance markers
   ```
   # From docs/compare.md
   #    Model    MAP@100     MRR@100     NDCG@10
   ---  -------  ----------  ----------  ----------
   a    model_1  0.3202ᵇ     0.3207ᵇ     0.3684ᵇᶜ
   b    model_2  0.2332      0.2339      0.239
   ```
   Superscripts denote statistical significance.

5. Limited Customization:
   ```python
   # From docs/compare.md
   report.rounding_digits = 4
   report.show_percentages = True
   ```
   Only rounding and percentage display can be controlled.

6. No Automation: No scheduled report generation or template customization beyond basic formatting.

Positive Aspects:
- LaTeX export for academic papers
- Statistical significance clearly marked
- Multiple output formats (text, LaTeX, JSON, dict)

Limitations:
- Only 1 visualization type
- No stakeholder-specific templates
- No rich dashboards or interactive reports
- No automated report generation

Rating Justification: Multiple formats (LaTeX, JSON, text) and statistical test integration warrant 2 points, but lack of stakeholder templates, limited visualization, and no automation prevent a 3.

---

### S6F4: Publication to Distribution Channels (Rating: 1/3)

Evidence:

1. No CI/CD Integration: No GitHub Actions, GitLab CI, or Jenkins support
   - No examples or documentation for pass/fail gates
   - No automated evaluation on commits

2. No MLOps Platform Integration: No support for MLflow, W&B, Neptune, or Comet
   - No model registry publishing
   - No experiment tracking platform sync

3. ranxhub - Limited Public Leaderboard:
   ```python
   # From notebooks/6_ranxhub.ipynb
   runs = [
       Run.from_ranxhub("msmarco-passage/trec-dl-2020/ranxhub/ance"),
       Run.from_ranxhub("msmarco-passage/trec-dl-2020/ranxhub/bm25-pyserini"),
   ]
   ```
   This is for downloading pre-computed runs, not publishing user results to a leaderboard.

   Sharing Process (from `notebooks/6_ranxhub.ipynb`):
   ```python
   # Users must manually:
   # 1. Build YAML run card
   # 2. Convert run to LZ4 format
   run.save("save/to/run.lz4")
   # 3. Submit via Google Form
   ```
   This is fully manual with no API or automation.

4. No Notifications: No Slack, email, or webhook notifications for metric degradation or completion.

5. Manual Distribution Only: Users must manually save and share files
   ```python
   # From docs/run.md
   run.save("path/to/run.json")
   ```

ranxhub Details (from `docs/index.md` and `notebooks/6_ranxhub.ipynb`):
- Centralized repository for sharing pre-computed runs
- Requires manual YAML metadata card creation
- Manual submission via web form
- No automated publishing or API
- Download-only for most users

Limitations:
- No automated distribution
- No MLOps integrations
- ranxhub is manual and limited to pre-computed runs
- No CI/CD support
- No notifications

Rating Justification: The complete absence of CI/CD integration, MLOps platform support, and automated publishing results in a 1. ranxhub provides minimal manual sharing capability but no true distribution automation.

---

## Summary of Strengths

1. Multiple Save Formats: JSON, TREC, LZ4, Parquet for runs and qrels
2. Statistical Testing: Fisher's, Student's t-test, Tukey's HSD with clear reporting
3. LaTeX Export: Useful for academic publications
4. ranxhub: Community repository for sharing pre-computed runs (though manual)

## Summary of Weaknesses

1. No Versioning: No git integration, dependency tracking, or reproducibility manifests
2. Limited Artifact Management: No querying, filtering, or metadata-rich storage
3. Basic Reporting: No stakeholder templates, limited visualizations, no dashboards
4. No Distribution: No CI/CD, MLOps integrations, or automated publishing
5. Manual Workflows: Most operations require manual file handling

## Recommendations for Improvement

1. Add Version Control:
   - Git commit tracking
   - Automatic dependency capture (pip freeze, conda env export)
   - Environment metadata (Python version, OS, CUDA)
   - Random seed tracking

2. Enhance Artifact Management:
   - SQLite/DuckDB backend for querying runs
   - Rich metadata capture (timestamps, configs, hyperparameters)
   - Run comparison interface beyond statistical tests

3. Expand Reporting:
   - Stakeholder-specific templates (executive, technical, compliance)
   - More visualizations (confusion matrices, ROC curves, error analysis)
   - HTML dashboard generation
   - Automated report generation

4. Add Distribution Channels:
   - MLflow/W&B/Neptune integration
   - CI/CD examples (GitHub Actions, GitLab CI)
   - Webhook notifications
   - API for ranxhub publishing

## Conclusion

ranx provides basic communication capabilities suitable for manual research workflows. It excels at statistical comparison and academic reporting (LaTeX) but lacks the versioning, automation, and distribution features expected of modern evaluation frameworks. The library is best suited for researchers conducting ad-hoc experiments who manually track reproducibility details, rather than production ML systems requiring automated evaluation pipelines.

Overall Stage 6 Score: 6/12 (50%)