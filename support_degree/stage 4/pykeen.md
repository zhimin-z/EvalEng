# PyKEEN - Stage 4 (EVALUATE) Evaluation

## Summary
PyKEEN is a knowledge graph embedding library focused on training and evaluating models for link prediction tasks. While it has a sophisticated rank-based evaluation system for knowledge graph embeddings, it lacks general-purpose metric computation capabilities for text generation, classification, or multi-modal tasks typical of LLM evaluation frameworks.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Evidence: PyKEEN focuses on knowledge graph embeddings and does not provide general output validation for LLM tasks. The codebase shows validation is limited to triple format checking (`src/pykeen/triples/`) and internal data structure validation. No JSON/XML validation, policy compliance checks, or general normalization capabilities are present. The evaluation module (`src/pykeen/evaluation/`) focuses exclusively on ranking metrics for link prediction, not output validation. |
| S4F2: Metric Computation | 1 | Evidence: PyKEEN implements 44 metrics according to README (`### Metrics` section), but they are exclusively rank-based metrics for link prediction (MRR, Hits@K, MR, etc.) and classification metrics (accuracy, F1, AUC-ROC) for triple classification. From `docs/source/tutorial/understanding_evaluation.rst`: "Knowledge graph embedding are usually evaluated on the task of link prediction." No text generation metrics (BLEU, ROUGE, METEOR, BERTScore) or retrieval metrics (P@k, NDCG) typical of LLM evaluation. The metrics are domain-specific to KG embeddings, not general-purpose. |
| S4F3: Evaluator Models | 0 | Evidence: No LLM-as-judge or evaluator model integration exists. The codebase shows evaluators like `RankBasedEvaluator` and `ClassificationEvaluator` (`src/pykeen/evaluation/`) that compute metrics based on model scores, not using separate evaluator models. No references to judge prompts, multi-aspect scoring with LLMs, or frameworks like RAGAS/G-Eval/Prometheus are found in the documentation or code. |
| S4F4: Multi-Modal Scoring | 1 | Evidence: While PyKEEN supports multi-modal representations (text, visual features per README: "TextRepresentation", "VisualRepresentation", "WikidataVisualRepresentation"), these are input features for training models, not multi-modal evaluation metrics. From README: "PyKEEN (<b>P</b>ython <b>K</b>nowl<b>E</b>dge <b>E</b>mbeddi<b>N</b>gs) is a Python package designed to train and evaluate knowledge graph embedding models (incorporating multi-modal information)." No vision-language metrics (CIDEr, SPICE, CLIP score), audio-text metrics (WER), or video metrics are implemented. Evaluation remains rank-based for link prediction regardless of input modality. |
| S4F5: Aggregate Statistics | 2 | Evidence: PyKEEN provides basic rank-based aggregation statistics. From `docs/source/tutorial/understanding_evaluation.rst`: metrics include mean, median, percentiles, and confidence intervals for ranks. The tutorial mentions "optimistic/pessimistic/realistic rank" variants showing statistical sophistication. However, limited model comparison features exist - no built-in pairwise significance testing, bootstrap confidence intervals for differences, or ranking systems (Elo, TrueSkill) are mentioned. The evaluation focuses on single-model metrics rather than comparative analysis tools. Some statistical depth exists but lacks comprehensive comparison infrastructure. |

## Key Findings

### Strengths
1. Specialized Evaluation Excellence: PyKEEN has a sophisticated rank-based evaluation system for knowledge graph embeddings with 44 metrics including adjusted variants (AAMR, AGMRI, z-scored metrics)
2. Statistical Depth: Implements multiple ranking types (optimistic, pessimistic, realistic) and filtered evaluation protocols
3. Reproducibility Features: Strong checkpoint system and deterministic evaluation

### Limitations for General LLM Evaluation
1. Domain-Specific Focus: All evaluation infrastructure is designed exclusively for knowledge graph link prediction, not general LLM tasks
2. No Text Generation Metrics: Missing standard metrics like BLEU, ROUGE, METEOR, BERTScore, exact match
3. No LLM-as-Judge: No integration with evaluator models or judge prompts
4. Limited Output Validation: No JSON/XML/schema validation or policy compliance checks
5. No Multi-Modal Evaluation Metrics: While models can use multi-modal inputs, evaluation remains rank-based prediction only

### Evidence of Scope Mismatch

From `docs/source/tutorial/understanding_evaluation.rst`:
```rst
Understanding the Evaluation
============================
This part of the tutorial is aimed to help you understand the evaluation of knowledge graph embeddings.
In particular it explains rank-based evaluation metrics reported in :class:`pykeen.evaluation.RankBasedMetricResults`.

Knowledge graph embedding are usually evaluated on the task of link prediction.
```

This clearly shows PyKEEN is designed for a different evaluation paradigm than general LLM evaluation frameworks.

## Conclusion

PyKEEN is an excellent framework for evaluating knowledge graph embeddings but does not fit the Stage 4 evaluation criteria for general LLM evaluation frameworks. It lacks:
- General-purpose metric computation for text generation, retrieval, and classification
- Output validation and normalization for LLM outputs
- LLM-as-judge and evaluator model integration
- Multi-modal evaluation metrics (vision-language, audio-text)
- Comprehensive model comparison tools

The framework excels in its specific domain (KG link prediction) but is not applicable to the 8-stage framework's Stage 4 requirements focused on LLM evaluation.