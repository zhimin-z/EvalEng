<div align="center">

# 📊 Evalware Survey

### Towards Evaluation Engineering: An Empirical Study of ML Evaluation Harnesses in the Wild

*Studying 57 ML evaluation harnesses and 19,638 GitHub issues — establishing evaluation engineering as a distinct SE concern.*

[![arXiv](https://img.shields.io/badge/arXiv-2605.24213-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2605.24213)
[![TOSEM](https://img.shields.io/badge/ACM%20TOSEM-2025-0277bd?style=for-the-badge)](https://dl.acm.org/journal/tosem)
[![License](https://img.shields.io/badge/license-MIT-868e96?style=for-the-badge)](LICENSE)
[![Website](https://img.shields.io/badge/website-live-2e7d32?style=for-the-badge)](https://zhimin-z.github.io/Evalware-Survey)

</div>

---

```
Evalware-Survey/
│
├── data/
│   ├── rq0_harness_search.csv           ← Raw GitHub search results for harness candidates
│   ├── rq0_harness_metadata.csv         ← Curated 57-harness list with URLs, stars, and domain
│   ├── rq1_workflow.md                  ← Unified evaluation workflow: stages × steps × strategies × harnesses
│   ├── rq1_harness_feature_matrix.csv   ← Binary harness × 34-strategy support matrix
│   ├── rq1_cluster_ward.json            ← Ward hierarchical clustering output (6 raw clusters + LLM names)
│   ├── rq1_cluster_curated.json         ← Final 4-archetype assignment per harness
│   ├── rq2_issues.jsonl                 ← All GitHub issues mined from the 57 harness repos
│   ├── rq2_issues_annotated_sample.jsonl← 377-issue sample annotated by two authors for κ validation
│   └── rq2_issues_annotated_full.jsonl  ← Full corpus annotated with workflow stage + root cause
│
├── analysis/
│   ├── rq1_cluster_harnesses.py         ← Build feature matrix, run Ward clustering, name clusters via LLM
│   ├── rq1_curate_clusters.py           ← Remap 6 raw clusters → 4 archetypes; save curated JSON
│   ├── rq1_plot_workflow.py             ← Render the unified evaluation workflow diagram
│   ├── rq1_plot_heatmap.py              ← Strategy support heatmap (harnesses × strategies)
│   ├── rq1_plot_pca.py                  ← PCA scatter plot colored by archetype
│   ├── rq2_collect_issues.py            ← Mine GitHub issues with token rotation; save issues JSONL
│   ├── rq2_annotate_issue_workflow.py   ← LLM-classify issues by workflow stage/step/strategy
│   ├── rq2_annotate_issue_root_cause.py ← LLM-classify issues by root cause (10 categories)
│   ├── rq2_analyze_issue_labels.py      ← Print issue label coverage statistics
│   ├── rq2_workflow_cohen_kappa.py      ← Cohen's κ for workflow annotation inter-rater reliability
│   ├── rq2_root_cause_cohen_kappa.py    ← Cohen's κ for root cause annotation inter-rater reliability
│   ├── rq2_plot_root_cause_archetype.py ← Root cause × archetype heatmap
│   └── rq3_plot_root_cause.py           ← Root cause × workflow stage heatmap
│
├── docs/
│   └── index.html                       ← GitHub Pages project website (Vue 3 + Chart.js)
│
└── README.md
```

---

## Data

| File | Description |
|------|-------------|
| `rq0_harness_search.csv` | Raw candidates from GitHub keyword search (25 phrases, ≥500 stars filter) |
| `rq0_harness_metadata.csv` | Curated list of 57 harnesses with name, GitHub URL, star count, and ML domain |
| `rq1_workflow.md` | Hand-annotated workflow model: 5 stages, 9 steps, 34 strategies, with per-harness support flags |
| `rq1_harness_feature_matrix.csv` | Binary matrix (harnesses × strategies) derived from the workflow file |
| `rq1_cluster_ward.json` | Ward clustering output: 6 clusters with member lists, strategy coverage, and LLM-generated names |
| `rq1_cluster_curated.json` | Manually curated mapping of each harness to one of 4 final archetypes |
| `rq2_issues.jsonl` | All open and closed issues for all 57 harnesses (title, body, comments, labels, timestamps) |
| `rq2_issues_annotated_sample.jsonl` | 377-issue sample with human labels used to compute inter-rater agreement |
| `rq2_issues_annotated_full.jsonl` | Full LLM-annotated corpus: workflow stage, step, strategy, and root cause per issue |

---

## Quickstart

```bash
git clone https://github.com/zhimin-z/Evalware-Survey.git
cd Evalware-Survey
cp .env.example .env          # fill in GITHUB_TOKEN_* and ANTHROPIC_API_KEY
pip install -r requirements.txt
python analysis/rq2_collect_issues.py  # or any other script
```

## Analysis

All scripts run from the repo root with `python analysis/<script>.py` — no arguments needed. Credentials are loaded from `.env` (see `.env.example`).

### RQ1 — Workflow Model & Archetypes

| Script | What it does |
|--------|-------------|
| `rq1_cluster_harnesses.py` | Parses `rq1_workflow.md` → builds feature matrix → Ward clustering (k=6) → LLM-names clusters → saves `rq1_cluster_ward.json` and `rq1_harness_feature_matrix.csv` |
| `rq1_curate_clusters.py` | Remaps 6 raw clusters to 4 final archetypes via manual analysis → saves `rq1_cluster_curated.json` |
| `rq1_plot_workflow.py` | Renders the unified evaluation workflow diagram |
| `rq1_plot_heatmap.py` | Strategy support heatmap across all harnesses |
| `rq1_plot_pca.py` | PCA scatter plot of harnesses colored by archetype |

### RQ2 — Issue Classification

| Script | What it does |
|--------|-------------|
| `rq2_collect_issues.py` | Mines all GitHub issues from repos in `rq0_harness_metadata.csv`; supports multi-token rotation → saves `rq2_issues.jsonl` |
| `rq2_annotate_issue_workflow.py` | Classifies each issue into workflow stage/step/strategy via Claude Haiku; resumable → appends to `rq2_issues_annotated_full.jsonl` |
| `rq2_annotate_issue_root_cause.py` | Adds root cause labels to annotated issues → updates `rq2_issues_annotated_full.jsonl` |
| `rq2_analyze_issue_labels.py` | Prints label coverage stats for the mined issues |
| `rq2_workflow_cohen_kappa.py` | Computes Cohen's κ between two authors' workflow annotations on the sample |
| `rq2_root_cause_cohen_kappa.py` | Computes Cohen's κ between two authors' root cause annotations on the sample |

### RQ3 — Cross-cutting Analysis

| Script | What it does |
|--------|-------------|
| `rq2_plot_root_cause_archetype.py` | Root cause distribution across the 4 archetypes |
| `rq3_plot_root_cause.py` | Root cause distribution across workflow stages |

---

## Citation

```bibtex
@article{zhao2025evaleng,
      title={Towards Evaluation Engineering: An Empirical Study of ML Evaluation Harnesses in the Wild}, 
      author={Zhimin Zhao and Zehao Wang and Abdul Ali Bangash and Bram Adams and Ahmed E. Hassan},
      year={2026},
      eprint={2605.24213},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2605.24213}, 
}
```

---

## License

Code and scripts: [MIT License](LICENSE) · Data and figures: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
