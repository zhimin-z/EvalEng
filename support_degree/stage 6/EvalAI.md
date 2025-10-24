# EvalAI - Stage 6 (RELEASE) Evaluation

## Summary
EvalAI is a platform for hosting AI challenges with a web-based leaderboard system. It focuses on hosting competitions rather than being a standalone evaluation framework. Communication capabilities are primarily web-based (leaderboards, dashboards) with some artifact management through the database. It lacks sophisticated versioning, reproducibility manifests, and distribution channel integrations typically found in dedicated evaluation frameworks.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S6F1: Artifact Management | 2 | Basic metadata tracking exists in the database (submission model stores status, timestamps, files), but no sophisticated querying interface, comparison tools, or packaging utilities are documented |
| S6F2: Version Control | 1 | Minimal versioning - git commit tracking for challenges not submissions, no dependency pinning, no reproducibility manifests, no automated environment capture |
| S6F3: Report Generation | 2 | Leaderboard displays results in HTML format with configurable metrics, but no stakeholder-specific templates, no executive summaries, no automated PDF/report generation |
| S6F4: Distribution Channels | 1 | Manual web-based leaderboards only, no CI/CD integration for evaluations, no MLOps platform integrations, no notification systems documented |

---

## Detailed Analysis

### S6F1: Evaluation Artifact Management (Rating: 2/3)

Evidence of Basic Metadata Tracking:

From `docs/source/submission.md`:
```markdown
* After all these checks are complete, a submission object is saved. The saved submission object includes __participant team id__ and __challenge phase id__ and __username__ of the participant creating it.
```

From `apps/jobs/models.py` structure (referenced in docs):
- Submission model tracks: participant team, challenge phase, username, timestamps, status
- Files are stored: `stderr.txt`, `stdout.txt`

Evidence of Limited Querying:

From `docs/source/03-for-participants/visibility/public-submissions.md`:
```markdown
1. Go to `My Submissions` Tab of the challenge page, select the phase and scroll horizontally.
```

This shows basic UI-based filtering by phase, but no advanced query API is documented.

Lack of Comparison Tools:

No documentation for:
- Side-by-side submission comparison
- Config diff tools
- Run comparison interfaces

Lack of Packaging:

No evidence in documentation of:
- Artifact bundling into archives
- Selective packaging options
- Compression utilities
- Directory structure preservation

Why not 3 points: Missing powerful querying API, no comparison tools, no packaging utilities. Only basic metadata storage exists.

Why not 1 point: Does capture essential metadata (timestamps, status, configs, logs) and stores them in database. Has basic filtering by phase in UI.

---

### S6F2: Archival Version Control and Reproducibility Manifests (Rating: 1/3)

Evidence of Minimal Git Integration for Challenges:

From `docs/source/github_based_challenge_setup.md`:
```markdown
2. Generate your [github personal access token]...
3. Add the github personal access token in the forked repository's [secrets]...
```

This only tracks challenge configuration changes via GitHub, not individual submission versioning.

No Dependency Pinning for Submissions:

The evaluation script documentation in `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md` shows:
```python
def evaluate(test_annotation_file, user_annotation_file, phase_codename, kwargs):
    pass
```

No mechanism documented for capturing:
- Participant's pip freeze
- conda environments
- Lockfiles

No Environment Capture:

No documentation of:
- Python version tracking per submission
- CUDA version recording
- System library versions
- Environment variables
- Random seeds

No Reproducibility Manifests:

No evidence of generating manifests that include:
- Code version
- Dependencies
- Environment specs
- Execution parameters

No Container Packaging:

While Docker is used for the platform itself (from `README.md`):
```shell
docker-compose up --build
```

There's no documentation of exporting participant submissions as Docker images for reproducibility.

Why not 2 points: Only tracks git commits for challenge configs (not submissions), no dependency/environment capture, no manifests.

Why not 0 points: Does have basic git integration for challenge configuration management via GitHub Actions.

---

### S6F3: Stakeholder-Specific Report and Visualization Generation (Rating: 2/3)

Evidence of Format Support:

From `docs/source/02-for-challenge-hosts/templates/example-challenges.md`:
```yaml
leaderboard:
  - id: 1
    schema: {
      "labels": ["Metric1", "Metric2", "Metric3", "Total"],
      "default_order_by": "Total",
      "metadata": {
        "Metric1": {
          "sort_ascending": True,
          "description": "Metric Description",
        }
      }
    }
```

This shows HTML leaderboards are the primary format. The documentation states:
```markdown
The above leaderboard schema will look something like this on leaderboard UI:
![](_static/img/leaderboard.png "Random Number Generator Challenge - Leaderboard")
```

No Multi-Format Support:
No documentation for:
- PDF generation
- JSON/CSV export
- Interactive dashboards beyond web UI
- Jupyter/Observable notebooks

No Stakeholder Templates:

The system provides a single leaderboard view for all users. From `docs/source/03-for-participants/visibility/public-submissions.md`:
```markdown
2. Now, to make the first submission public, click on the checkbox under the column `Show on Leaderboard`.
```

No evidence of:
- Executive summary templates
- Technical deep-dive reports
- Compliance reports with audit trails
- Research methodology reports

Basic Visualization:

The leaderboard shows metrics in tabular format. From the schema configuration, it supports:
- Multiple metrics columns
- Sorting by different columns
- Decimal precision control

But no documentation of:
- Confusion matrices
- ROC/PR curves
- Calibration plots
- Error distributions
- Custom visualizations

No Automation:

No documentation of:
- Automated report generation on submission
- Template customization beyond YAML config
- Scheduled reporting

Why not 3 points: Only single format (HTML leaderboards), no stakeholder-specific templates, no rich visualizations beyond tables, no automation.

Why not 1 point: Does have configurable leaderboard with multiple metrics, decimal precision, and sorting - more than just a single generic output format.

---

### S6F4: Publication to Distribution Channels (Rating: 1/3)

Evidence of Manual Web Distribution Only:

From `README.md`:
```markdown
Our ultimate goal is to build a centralized platform to host, participate and collaborate in AI challenges
```

The primary distribution is through the web platform leaderboard. From `docs/source/participate.md`:
```markdown
### 4. Challenge Page
After reading the challenge instructions on the challenge page, you can participate in the challenge.
```

No CI/CD Integration:

While GitHub Actions are used for challenge setup (from `docs/source/github_based_challenge_setup.md`):
```markdown
8. Commit the changes and push the `challenge` branch in the repository and wait for the build to complete.
```

This is for challenge configuration, not for:
- Automated evaluation on code commits
- Pass/fail gates based on metrics
- Continuous evaluation workflows

No MLOps Platform Integration:

No documentation for integrations with:
- MLflow
- Weights & Biases
- Neptune.ai
- Comet.ml
- Model registries

No Public Leaderboard Integration:

While EvalAI itself is a leaderboard platform, there's no documentation of:
- HuggingFace Hub publishing
- Papers with Code integration
- Export to external leaderboards

No Notification System:

No documentation of:
- Slack notifications (despite example in evaluation script showing how hosts could manually add this)
- Email alerts
- Webhook notifications
- Configurable notification rules
- Metric degradation alerts

From `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md`, hosts can manually add notifications:
```python
if score > 90:
    webhook_url = "Your slack webhook url comes here"
    response = requests.post(webhook_url, ...)
```

But this is manual custom code, not a built-in distribution feature.

Why not 2 points: No built-in integrations with any external platforms, no notification system, no CI/CD evaluation triggers.

Why not 0 points: Does provide web-based leaderboard distribution (the core platform feature) and GitHub-based challenge configuration workflow.

---

## Key Evidence Summary

### Strengths:
1. Database-backed submission tracking with essential metadata (timestamps, status, files)
2. Web-based leaderboard with configurable metrics and visibility controls
3. GitHub integration for challenge configuration management
4. Flexible evaluation scripts that can be updated without full redeployment

### Gaps:
1. No reproducibility manifests - no automated capture of environment, dependencies, or execution context
2. No comparison/diff tools - cannot easily compare multiple runs or submissions
3. No multi-format reporting - only HTML leaderboards, no PDFs, CSVs, or stakeholder-specific reports
4. No external integrations - no MLOps platforms, no CI/CD triggers, no automated notifications
5. No artifact packaging - no bundling of results + configs + logs into distributable archives

### Overall Assessment:
EvalAI is optimized for hosting competitive challenges with web leaderboards, not for comprehensive evaluation result management and distribution. It's more of a competition platform than an evaluation framework. Communication features are adequate for its intended use case (challenge leaderboards) but limited compared to dedicated evaluation harnesses.