<div align="center">

# 📊 Evalware Survey

### Towards Evaluation Engineering: An Empirical Study of ML Evaluation Harnesses in the Wild

*An empirical analysis of 57 evaluation harnesses and 19,638 GitHub issues — establishing evaluation engineering as a distinct software engineering concern.*

[![arXiv](https://img.shields.io/badge/arXiv-2605.24213-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2605.24213)
[![License](https://img.shields.io/badge/license-MIT-868e96?style=for-the-badge)](LICENSE)
[![Website](https://img.shields.io/badge/website-live-2e7d32?style=for-the-badge)](https://sailresearch.github.io/Evalware-Survey)

</div>

---

## What is Evalware Survey?

ML evaluation harnesses — software systems that orchestrate model invocation, data loading, metric computation, and result reporting — are central to AI research infrastructure. Yet no prior SE work had studied them as software products.

This study analyzes **57 evaluation harnesses** and **19,638 GitHub issues** to derive a unified workflow model, identify where challenges concentrate, and categorize root causes. We introduce **Evaluation Engineering (EvalEng)** as the SE concerns arising when evaluation is operationalized. Full findings and interactive visualizations are on the [project website](https://sailresearch.github.io/Evalware-Survey).

---

## Repository Layout

```
Evalware-Survey/
│
├── data/
│   ├── harnesses.csv                ← 57 harnesses with metadata (stars, domain, archetype)
│   ├── issues_classified.csv        ← 16,560 issues with workflow stage + root cause labels
│   └── strategy_matrix.csv          ← 57 × 9 binary strategy support matrix
│
├── figures/
│   ├── intro/                       ← Motivation figure (ad-hoc vs. harness workflow)
│   ├── method/                      ← Study workflow diagram
│   ├── rq1/                         ← Workflow model, strategy heatmap, PCA archetype clusters
│   ├── rq2/                         ← Root cause × archetype heatmap
│   └── rq3/                         ← Root cause × workflow stage heatmap
│
├── scripts/
│   ├── collect_harnesses.py         ← Harness collection via GitHub search + curated sources
│   ├── mine_issues.py               ← GitHub issue retrieval (open + closed)
│   ├── classify_issues.py           ← LLM-based issue classification (Claude Haiku 4.5)
│   ├── extract_pdf_comments.py      ← PDF annotation extraction utility
│   └── figures/                     ← Figure generation scripts (per RQ)
│
├── docs/
│   └── index.html                   ← GitHub Pages project website (Vue 3 + Chart.js)
│
└── README.md
```

---

## Data

### `data/harnesses.csv`

| Column | Description |
|--------|-------------|
| `name` | Harness name |
| `url` | GitHub repository URL |
| `stars` | GitHub star count at collection time |
| `domain` | ML domain (LLM, vision, RL, general) |
| `archetype` | One of four archetypes (see below) |

### `data/issues_classified.csv`

| Column | Description |
|--------|-------------|
| `harness` | Source harness |
| `issue_id` | GitHub issue number |
| `title` | Issue title |
| `workflow_stage` | S0–S4 (Provisioning → Reporting) |
| `workflow_step` | S0-A through S4-A (9 steps) |
| `root_cause` | One of ten root cause categories |
| `is_workflow_relevant` | Boolean — whether issue affects evaluation operations |

### `data/strategy_matrix.csv`

Binary matrix: rows = harnesses, columns = 34 implementation strategies. `1` = strategy supported, `0` = not supported.

---

## Scripts

### Issue Classification (`scripts/classify_issues.py`)

Uses Claude Haiku 4.5 with a calibrated prompt (Cohen's κ > 0.87 against human consensus) to classify issues by workflow stage and root cause at scale.

```bash
python scripts/classify_issues.py \
  --input data/issues_raw.jsonl \
  --output data/issues_classified.csv \
  --task workflow          # or: root_cause
```

### Harness Collection (`scripts/collect_harnesses.py`)

Searches GitHub using 25 keyword phrases seeded from the Awesome Production ML List, then filters by star count (≥500) and evaluation-primary purpose.

```bash
python scripts/collect_harnesses.py \
  --keywords configs/search_keywords.txt \
  --output data/harnesses.csv
```

### Issue Mining (`scripts/mine_issues.py`)

Retrieves all open and closed GitHub issues for each harness repository.

```bash
python scripts/mine_issues.py \
  --harnesses data/harnesses.csv \
  --output data/issues_raw.jsonl \
  --token $GITHUB_TOKEN
```

### Figure Generation (`scripts/figures/`)

| Script | Output |
|--------|--------|
| `rq1_workflow.py` | Workflow model diagram (`figures/rq1/`) |
| `rq1_heatmap.py` | Strategy support heatmap |
| `rq2_archetype.py` | Root cause × archetype heatmap |
| `rq3_stage.py` | Root cause × stage heatmap |

---

## Harness Archetypes

The 57 harnesses cluster into four archetypes by workflow strategy coverage:

| Archetype | Count | Avg. Coverage |
|-----------|------:|:-------------:|
| Standardized LLM Benchmark Suites | 23 (40.4%) | ~45% |
| Narrow-Domain Metric Libraries | 12 (21.1%) | ~28% |
| Task-Specific Capability Probes | 12 (21.1%) | ~37% |
| Full-Stack LLM Evaluation Platforms | 10 (17.5%) | ~70% |

---

## Citation

```bibtex
@article{zhao2025evaleng,
  title     = {Towards Evaluation Engineering: An Empirical Study of {ML} Evaluation Harnesses in the Wild},
  author    = {Zhao, Zhimin and Wang, Zehao and Bangash, Abdul Ali and Adams, Bram and Hassan, Ahmed E.},
  journal   = {ACM Transactions on Software Engineering and Methodology},
  year      = {2025},
  publisher = {ACM},
  url       = {https://arxiv.org/abs/2605.24213}
}
```

---

## License

Code and scripts are licensed under the [MIT License](LICENSE).  
Data and figures are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
