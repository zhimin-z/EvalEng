# ranx - Stage 2 (PREPARE) Evaluation

## Summary
ranx is a fast evaluation library for information retrieval and recommender systems. It focuses on post-hoc evaluation of pre-computed runs against qrels (ground truth relevance judgments), not on data preparation or infrastructure building for evaluation tasks. The library has minimal Stage 2 capabilities as it's designed for the evaluation step (Stage 3), not the preparation phase.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Evidence: The library supports loading qrels/runs from multiple formats (TREC, JSON, Parquet, DataFrame) and basic format conversion (`ranx/data_structures/qrels.py`, `ranx/data_structures/run.py`). However, there is no preprocessing pipeline, no caching beyond basic file I/O, no validation beyond format parsing, and no versioned splits. The `from_file` and `save` methods just handle format conversion without any data quality checks or preprocessing transformations. Justification: Minimal data loading utilities exist, but no actual preprocessing or validation. |
| S2F2: Quality Assessment | 0 | Evidence: No quality assessment tools found in the codebase. Search through `ranx/` reveals only evaluation metrics (NDCG, MAP, etc.) for model performance, not dataset quality checks. No label consistency checks, demographic analysis, duplicate detection, or bias detection capabilities. Justification: Completely absent - this is an evaluation library, not a data quality framework. |
| S2F3: PII Detection | 0 | Evidence: No PII detection or anonymization features exist. Codebase search for "pii", "privacy", "anonymize", "redact" returns no results. The library works with pre-existing qrels/runs with arbitrary string IDs. Justification: No PII handling capabilities whatsoever. |
| S2F4: Infrastructure Building | 0 | Evidence: No infrastructure building features. The library doesn't build retrieval indices, databases, or specialized environments. It only evaluates pre-computed ranking results. From `README.md`: the library provides "evaluation metrics" and "fusion algorithms" - no mention of index building or infrastructure setup. Justification: Not applicable to this evaluation-focused library. |
| S2F5: Model Validation | 0 | Evidence: No model artifact validation. The library doesn't handle models at all - it only evaluates their outputs (runs). No checksum validation, version compatibility checks, or model integrity verification in the codebase. Justification: Not applicable - ranx works with ranking outputs, not models. |
| S2F6: Scenario Generation | 0 | Evidence: No scenario generation capabilities. The library evaluates existing qrels/runs, doesn't generate test scenarios or variations. Search for "generate", "variation", "scenario" in context of test creation yields no results. The notebooks show only loading existing data files. Justification: Completely absent. |
| S2F7: Red-Teaming | 0 | Evidence: No red-teaming or adversarial testing features. This is an IR evaluation library focused on metrics like NDCG/MAP, not safety testing. No jailbreak attempts, prompt injection tests, or bias probing in the codebase. Justification: Not applicable to this domain-specific evaluation library. |
| S2F8: Contamination Detection | 0 | Evidence: No contamination detection features. The library assumes qrels and runs are independent and doesn't check for data leakage. No n-gram overlap, semantic similarity, or training corpus comparison capabilities found. Justification: Completely absent. |

---

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (1/3)

Strengths:
- Multiple input formats supported (TREC, JSON, Parquet, DataFrame)
- Can load qrels from ir-datasets: `Qrels.from_ir_datasets("msmarco-document/dev")` (`docs/qrels.md`)
- Format conversion capabilities between JSON/TREC/Parquet

Evidence from code:
```python
# ranx/data_structures/qrels.py
def from_file(cls, path: str, kind: str = None):
    # Supports .json, .trec, .txt, .gz, .parq formats
    # But no preprocessing, just format parsing
```

Limitations:
- No data caching beyond basic file loading
- No preprocessing pipelines (tokenization, normalization, etc.)
- No validation (checksums, format consistency, completeness)
- No physical splitting functionality
- No versioning of splits

Why only 1 point: The library provides basic data loading but no actual preprocessing or preparation capabilities. It's designed to work with already-prepared evaluation data.

---

### S2F2-S2F8: All rated 0/3

These features are completely absent because ranx is an evaluation metrics library, not a data preparation framework. Its scope is:

1. Load pre-computed results: `Run.from_file()`, `Qrels.from_file()`
2. Compute evaluation metrics: `evaluate(qrels, run, ["ndcg@10", "map"])` 
3. Compare systems: `compare(qrels, [run1, run2], metrics=["ndcg@10"])`
4. Fuse rankings: `fuse(runs, method="rrf")`

Evidence from `README.md`:
> "ranx ([raŋks]) is a library of fast ranking evaluation metrics... It offers a user-friendly interface to evaluate and compare Information Retrieval and Recommender Systems."

The typical workflow (from `notebooks/1_overview.ipynb`):
```python
# 1. Load pre-existing data
qrels = Qrels.from_file("data/qrels.trec")
run = Run.from_file("data/run.trec")

# 2. Evaluate (Stage 3, not Stage 2)
evaluate(qrels, run, "ndcg@5")
```

No Stage 2 operations like:
- Quality assessment of datasets
- PII detection/removal
- Index building for retrieval
- Test scenario generation
- Adversarial testing
- Contamination checking

---

## Key Observations

### 1. Wrong Framework for Stage 2 Evaluation
ranx is fundamentally a Stage 3 (EXECUTE) framework. It assumes:
- Data is already prepared and clean
- Relevance judgments (qrels) exist
- System outputs (runs) are pre-computed
- No need for infrastructure setup

### 2. Domain-Specific Design
The library is narrowly focused on Information Retrieval evaluation, specifically:
- Computing ranking metrics (NDCG, MAP, MRR, etc.)
- Statistical significance testing (Fisher, t-test)
- Result fusion algorithms
- Comparison reporting

### 3. No Data Preparation Philosophy
From the FAQ (`docs/faq.md`):
> "Is ranx suited for evaluating classification tasks? No, it's not. ranx is meant for ranking tasks."

This philosophy extends to data preparation - the library expects you to handle that externally.

---

## Missing Critical Stage 2 Features

To be a Stage 2 framework, ranx would need to add:

1. Dataset preprocessing pipelines with validation
2. Quality assessment tools (label noise, balance, duplicates)
3. Split generation with versioning (train/val/test)
4. Index building for retrieval systems (FAISS, BM25, etc.)
5. Scenario generation for evaluation
6. Contamination detection between train and eval data

None of these exist because they're out of scope for a metrics-computation library.

---

## Conclusion

Total Score: 1/24 points

ranx scores extremely low on Stage 2 criteria because it's designed for a different purpose. It's an excellent evaluation execution framework (Stage 3) but not a data preparation framework (Stage 2). The 1 point comes solely from basic data loading utilities that happen to overlap slightly with preparation needs.

Recommendation: If evaluating ranx holistically, focus on its Stage 3 (EXECUTE) and Stage 4 (ANALYZE) capabilities where it excels. For Stage 2 needs, users should look at:
- Preprocessing: Standard NLP/IR libraries (spaCy, transformers)
- Quality assessment: Data validation frameworks (Great Expectations)
- Infrastructure: Retrieval frameworks (Pyserini, BEIR)

The low score reflects capability mismatch, not poor implementation - ranx does what it's designed to do very well.