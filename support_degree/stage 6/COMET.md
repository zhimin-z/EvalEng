# Unbabel COMET - Stage 6 (SHIP) Evaluation

## Summary
COMET (Crosslingual Optimized Metric for Evaluation of Translation) is a neural framework for MT evaluation. While it excels at its core function of scoring translations, its communication capabilities are minimal. The framework lacks sophisticated artifact management, version control integration, stakeholder-specific reporting, and distribution channel features. Most outputs are basic scores with limited metadata capture and no automated reproducibility tracking.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 1 | Basic score output only, minimal metadata capture, no querying or packaging |
| S6F2: Version Control | 0 | No git integration, dependency tracking, or reproducibility manifests |
| S6F3: Report Generation | 1 | Single JSON output format, no templates, minimal visualization support |
| S6F4: Distribution Channels | 1 | Models published to HuggingFace Hub, but no CI/CD integration or notifications |

---

## Detailed Analysis

### S6F1: Evaluation Artifact Management
Rating: 1/3

Evidence:

1. Runtime Capture - Minimal (Basic scores only)
   
   From `comet/cli/score.py` lines 155-159:
   ```python
   outputs = model.predict(
       samples=data,
       batch_size=cfg.batch_size,
       gpus=cfg.gpus,
       progress_bar=(not cfg.quiet),
   ```
   
   The prediction output in `comet/models/base.py` lines 308-315 shows limited metadata:
   ```python
   def predict_step(
       self,
       batch: Dict[str, torch.Tensor],
       batch_idx: Optional[int] = None,
       dataloader_idx: Optional[int] = None,
   ) -> torch.Tensor:
       model_outputs = Prediction(scores=self(batch).score)
       if self.mc_dropout:
           mcd_outputs = torch.stack(
               [self(batch).score for _ in range(self.mc_dropout)]
           )
           model_outputs["metadata"] = Prediction(
               mcd_scores=mcd_outputs.mean(dim=0),
               mcd_std=mcd_outputs.std(dim=0),
           )
       return model_outputs
   ```
   
   Missing: Automatic capture of timestamps, config hashes, model IDs, execution logs, or detailed traces.

2. Querying - None
   
   No evidence of any querying capability. Results are returned as simple lists/dictionaries with no filtering or search functionality. From `comet/cli/score.py` lines 200-211:
   ```python
   for i in range(len(data[files[0]])):  # loop over (src, ref)
       for j in range(len(files)):  # loop of system
           data[files[j]][i]["COMET"] = seg_scores[j][i]
           if errors and errors[j] and errors[j][i]:
               data[files[j]][i]["errors"] = errors[j][i]
   ```
   
   Missing: No query API, no filtering by metadata, no search functionality.

3. Comparison - Minimal (Manual only)
   
   There's a separate `compare.py` CLI tool, but from `comet/cli/compare.py` (not included in snippet but referenced in README), it only provides basic statistical significance testing, not sophisticated comparison interfaces.
   
   Missing: No built-in diff tools, no side-by-side visualization, no comprehensive comparison UI.

4. Packaging - None
   
   Results are saved as simple JSON with no archival capabilities. From `comet/cli/score.py` lines 218-221:
   ```python
   if cfg.to_json != "":
       with open(cfg.to_json, "w", encoding="utf-8") as outfile:
           json.dump(data, outfile, ensure_ascii=False, indent=4)
       print("Predictions saved in: {}.".format(cfg.to_json))
   ```
   
   Missing: No bundling of results with configs, no compression, no selective packaging, no directory structure preservation.

Justification: The framework captures only basic prediction scores with minimal metadata (MC dropout stats for some models, error spans for XCOMET). There's no querying, no sophisticated comparison tools, and no packaging capabilities. Everything is manual file management.

---

### S6F2: Archival Version Control and Reproducibility Manifests
Rating: 0/3

Evidence:

1. Git Integration - None
   
   No evidence of git integration anywhere in the codebase. No commit tracking, no detection of uncommitted changes.

2. Dependency Pinning - Partial (poetry.lock exists but not tracked per-run)
   
   From `pyproject.toml` lines 32-51:
   ```toml
   [tool.poetry.dependencies]
   python = "^3.8.0"
   sentencepiece = "^0.2.0"
   pandas = ">=1.4.1"
   transformers = "^4.17"
   pytorch-lightning = "^2.0.0"
   jsonargparse = "3.13.1"
   torch = ">=1.6.0"
   numpy = "^1.20.0"
   torchmetrics = "^0.10.2"
   sacrebleu = "^2.0.0"
   scipy = "^1.5.4"
   entmax = "^1.1"
   huggingface-hub = ">=0.19.3,<1.0"
   protobuf = "^4.24.4"
   ```
   
   While `poetry.lock` exists (not shown), there's no evidence that dependency versions are captured per-evaluation run.

3. Environment Capture - None
   
   No capture of Python version, CUDA version, OS, environment variables, or random seeds during prediction.

4. Manifest Generation - None
   
   No reproducibility manifests generated. The only "manifest" is the model's `hparams.yaml` for the model itself, but not for evaluation runs. From `comet/models/__init__.py` lines 54-57:
   ```python
   parent_folder = checkpoint_path.parents[1]  # .parent.parent
   hparams_file = parent_folder / "hparams.yaml"

   if hparams_file.is_file():
       with open(hparams_file) as yaml_file:
   ```
   
   Missing: No per-run manifests capturing evaluation configuration, data versions, or environment state.

5. Container Packaging - None
   
   No Docker image export, no containerized reproducibility.

Justification: Zero automation for versioning or reproducibility tracking. While the project uses poetry for dependency management, there's no capture of environment state, git commits, or dependency versions during evaluation runs. Users would need to manually track everything.

---

### S6F3: Stakeholder-Specific Report and Visualization Generation
Rating: 1/3

Evidence:

1. Format Support - Single Format (JSON only)
   
   From `comet/cli/score.py` lines 218-221:
   ```python
   if cfg.to_json != "":
       with open(cfg.to_json, "w", encoding="utf-8") as outfile:
           json.dump(data, outfile, ensure_ascii=False, indent=4)
       print("Predictions saved in: {}.".format(cfg.to_json))
   ```
   
   Missing: No HTML, PDF, CSV, Parquet, interactive dashboards, or notebooks. Only JSON and console output.

2. Stakeholder Templates - None
   
   No templates for different audiences (executives, technical teams, compliance, research). All outputs are identical.

3. Visualization - None Built-in
   
   No visualization capabilities. From the README.md line 13:
   ```md
   2) We now support [DocCOMET](https://statmt.org/wmt22/pdf/2022.wmt-1.6.pdf), 
   a document-level extension of COMET which can utilize contextual information.
   ```
   
   The framework focuses on scoring, not visualization. Users must create their own visualizations from the JSON output.
   
   Missing: No confusion matrices, calibration plots, ROC curves, error distributions, or comparison charts.

4. Automation - Minimal
   
   CLI provides basic automation, but no scheduled generation or templating. From `comet/cli/score.py` lines 72-76:
   ```python
   parser.add_argument(
       "--to_json",
       type=str,
       default="",
       help="Exports results to a json file.",
   )
   ```

Justification: Only JSON export available with basic segment and system scores. No visualization support, no stakeholder templates, no multiple output formats. Users must build their own reporting infrastructure.

---

### S6F4: Publication to Distribution Channels
Rating: 1/3

Evidence:

1. CI/CD Integration - None
   
   No evidence of CI/CD integration in the repository. No GitHub Actions workflows, no GitLab CI configs, no Jenkins files. The `.github/` directory only contains issue templates:
   ```
   .github/ISSUE_TEMPLATE/bug_report.md
   .github/ISSUE_TEMPLATE/typos-and-doc-fixes.md
   .github/ISSUE_TEMPLATE/questions-and-help.md
   .github/ISSUE_TEMPLATE/feature_request.md
   ```
   
   Missing: No automated evaluation on commits, no pass/fail gates based on metrics.

2. MLOps Platforms - Partial (Training only, not evaluation)
   
   From `comet/models/base.py` lines 321-343, the framework uses PyTorch Lightning which has integrations with MLOps platforms, but this is for model training, not evaluation distribution:
   ```python
   def on_validation_epoch_end(self, *args, kwargs) -> None:
       """Computes and logs metrics."""
       self.log_dict(self.train_metrics.compute(), prog_bar=False)
       self.train_metrics.reset()

       val_metrics = []
       for i in range(len(self.hparams.validation_data)):
           results = self.val_metrics[i].compute()
           self.val_metrics[i].reset()
           # Log to tensorboard the results for this validation set.
           self.log_dict(results, prog_bar=False)
   ```
   
   Missing: No explicit integration for publishing evaluation results to MLflow, W&B, Neptune, or Comet.ml.

3. Public Leaderboards - Partial (Models published, not evaluation results)
   
   From `comet/models/__init__.py` lines 27-34 and README.md:
   ```python
   def download_model(
       model: str,
       saving_directory: Union[str, Path, None] = None,
       local_files_only: bool = False,
   ) -> str:
       try:
           model_path = snapshot_download(
               repo_id=model, cache_dir=saving_directory, local_files_only=local_files_only
           )
   ```
   
   Models are published to HuggingFace Hub (e.g., `Unbabel/wmt22-comet-da`), but not evaluation results. From MODELS.md:
   ```md
   - Default Model: [`Unbabel/wmt22-comet-da`](https://huggingface.co/Unbabel/wmt22-comet-da)
   - Reference-free Model: [`Unbabel/wmt22-cometkiwi-da`](https://huggingface.co/Unbabel/wmt23-cometkiwi-da)
   - eXplainable COMET (XCOMET): [`Unbabel/XCOMET-XXL`](https://huggingface.co/Unbabel/XCOMET-XXL)
   ```
   
   Missing: No automatic publishing of evaluation results to Papers with Code, WMT leaderboards, or custom leaderboards.

4. Notifications - None
   
   No notification system. No Slack, email, or webhook integrations. No alerts on metric degradation.

Justification: While the framework publishes trained models to HuggingFace Hub, there's no infrastructure for distributing evaluation results. No CI/CD integration, no MLOps platform sync for evaluation runs, no notifications. Users must manually share results.

---

## Summary Assessment

Total Score: 3/12 (25%)

COMET is primarily designed as an evaluation metric, not a comprehensive evaluation framework with artifact management and distribution capabilities. Its strengths lie in:
- High-quality neural MT evaluation models
- Easy-to-use Python API and CLI
- Model sharing via HuggingFace Hub

However, for Stage 6 (SHIP) requirements, it's severely lacking:
- No artifact management: Just basic JSON output
- No version control: Zero git integration or reproducibility tracking
- No reporting: Single format, no templates, no visualizations
- Minimal distribution: No CI/CD, no MLOps integration, no notifications

The framework assumes users will handle all communication aspects manually, making it suitable for ad-hoc evaluation but insufficient for production ML pipelines requiring comprehensive result tracking, versioning, and distribution.