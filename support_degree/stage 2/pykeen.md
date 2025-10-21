# PyKEEN - Stage 2 (PREPARE) Evaluation

## Summary
PyKEEN is a knowledge graph embedding library, not an evaluation harness. However, it does include data preparation functionality for knowledge graph embedding tasks. The framework focuses on dataset loading, splitting, and preprocessing for training and evaluating KG embeddings, but lacks features specific to the PREPARE stage of a general evaluation framework (e.g., PII detection, red-teaming, contamination detection).

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 2 | Evidence: PyKEEN has dataset loading and preprocessing capabilities through `pykeen.triples.TriplesFactory`. The code shows entity/relation ID mapping (`entity_label_to_id`, `relation_label_to_id` in `docs/source/tutorial/performance.rst`) and caching of mapped triples (`mapped_triples`). The framework includes 37 built-in datasets (README.md) with automatic loading. However, preprocessing is limited to triple mapping and splitting - no general text/image/audio preprocessing pipelines. The splitting functionality (`docs/source/tutorial/splitting.rst`) supports coverage-based, cleanup (deterministic/randomized) methods with configurable ratios, which is more advanced than basic splits. Missing: comprehensive preprocessing for different modalities, validation/checksum features. |
| S2F2: Quality Assessment | 1 | Evidence: The repository includes dataset statistics and analysis tools in `src/pykeen/datasets/` but no systematic quality assessment features. The documentation mentions "entity and relation to ID mapping" (`docs/source/tutorial/performance.rst`) but no tools for detecting label noise, duplicates, or bias. The evaluation module (`src/pykeen/evaluation/`) focuses on model performance metrics rather than dataset quality. Missing: label quality checks, demographic analysis, duplicate detection, bias detection tools. |
| S2F3: PII Detection | 0 | Evidence: No PII detection or anonymization features found in the codebase. The documentation does not mention any privacy-related preprocessing. The datasets module (`src/pykeen/datasets/`) loads data directly without privacy checks. This is expected as PyKEEN focuses on knowledge graph embeddings where entities are typically already anonymized IDs or public knowledge. Missing: All PII detection and anonymization capabilities. |
| S2F4: Infrastructure Building | 2 | Evidence: PyKEEN has some infrastructure capabilities for knowledge graph tasks. The repository includes checkpointing functionality (`docs/source/tutorial/checkpoints.rst`) with automatic saving/loading of model states: `checkpoint_name='my_checkpoint.pt'`, `checkpoint_frequency=5`. The triples factory (`pykeen.triples.TriplesFactory`) manages entity/relation mappings and can persist them. However, there's no support for building retrieval systems (FAISS, BM25), databases, or general task-specific infrastructure beyond KG embedding training. The inductive LP tutorial (`docs/source/tutorial/inductive_lp.rst`) shows some graph infrastructure management for disjoint train/inference graphs. Missing: Retrieval index building, database setup, versioned artifact management for general evaluation. |
| S2F5: Model Artifact Validation | 1 | Evidence: PyKEEN has basic checkpoint validation through configuration hashing (`docs/source/tutorial/checkpoints.rst`): "PyKEEN makes a hash-sum comparison of the configurations of the checkpoint and the one of the current configuration at hand." However, this is limited to configuration matching, not comprehensive model validation. The checkpoint system stores model state dicts but doesn't validate integrity beyond preventing configuration mismatches. From checkpoints tutorial: "When these don't match, PyKEEN won't accept the checkpoint and raise an error." Missing: Cryptographic checksums, version compatibility checks, corruption detection, comprehensive model validation. |
| S2F6: Scenario Generation | 0 | Evidence: PyKEEN does not include scenario generation capabilities. The framework focuses on fixed knowledge graph datasets and evaluation protocols. While it supports different evaluation modes (filtered vs unfiltered, from `docs/source/tutorial/understanding_evaluation.rst`), these are not generative scenarios but rather different filtering settings. The inductive LP setup (`docs/source/tutorial/inductive_lp.rst`) defines fixed train/test splits, not generated scenarios. Missing: Prompt variations, multi-turn dialogues, edge case generation, scenario versioning. |
| S2F7: Red-Teaming | 0 | Evidence: No red-teaming or adversarial test generation features found. PyKEEN is designed for knowledge graph embedding evaluation, not safety testing. The evaluation module (`src/pykeen/evaluation/`) implements rank-based metrics (MRR, Hits@K) but no adversarial or safety testing. Missing: All red-teaming, jailbreak testing, bias probing, safety boundary testing capabilities. |
| S2F8: Contamination Detection | 1 | Evidence: PyKEEN implements a "filtered evaluation" setting (`docs/source/tutorial/understanding_evaluation.rst`) that removes known training triples from evaluation to avoid inflated metrics: "the filtered evaluation setting ignores for a given triple (h, r, t) the scores of all other *known* true triples (h, r, t')". This is implemented through index-based masking (Section "Filtering with Index-based Masking" in performance.rst). However, this is filtering during evaluation, not contamination *detection*. The framework doesn't compare evaluation data against training corpora to detect leakage - it just filters known triples at evaluation time. Missing: N-gram overlap detection, semantic similarity comparison, contamination scoring, proactive detection tools. |

## Key Strengths

1. Advanced Splitting Methods: PyKEEN implements sophisticated splitting algorithms (coverage-based, cleanup methods) that ensure transductive constraints are met while preserving data.

2. Checkpoint System: The checkpoint functionality is well-designed with frequency control, automatic resume, and configuration validation to prevent mismatches.

3. Efficient Preprocessing: Entity/relation ID mapping with caching (`mapped_triples`) optimizes repeated access. The tuple broadcasting technique (Section "Tuple Broadcasting" in performance.rst) shows performance optimization.

4. Inductive Setup Support: The framework supports inductive link prediction with proper separation of training/inference graphs (`InductiveDataset` class).

## Key Gaps

1. No General Evaluation Framework: PyKEEN is a knowledge graph embedding library, not a general evaluation harness. Most PREPARE stage features (PII detection, red-teaming, contamination detection, scenario generation) are not applicable.

2. Limited Quality Assessment: While datasets are well-curated, there are no systematic tools for detecting label noise, duplicates, or biases in custom datasets.

3. No Multi-Modal Preprocessing: Despite mentioning multi-modal support in README, the preprocessing focuses on triples. No image/text/audio preprocessing pipelines found.

4. No Safety Features: No PII detection, adversarial test generation, or red-teaming capabilities - appropriate for KG tasks but limiting for broader evaluation use cases.

5. Limited Artifact Management: Beyond checkpoints, there's no infrastructure for building retrieval systems, managing multiple artifact versions, or validating model integrity comprehensively.

## Recommendations for PyKEEN (if extending to general evaluation)

1. Add Quality Assessment Tools: Implement duplicate detection, label consistency checks, and distribution analysis for custom datasets.

2. Expand Validation: Add cryptographic checksums for model artifacts, version compatibility checks beyond config hashing.

3. Document Dataset Curation: Provide tools and guidelines for assessing bias and representativeness in knowledge graphs.

4. Contamination Detection: Extend the filtered evaluation concept to proactive contamination detection between train/test splits.

## Overall Assessment

PyKEEN scores 7/24 across Stage 2 features. This low score primarily reflects that PyKEEN is a specialized KG embedding library, not a general evaluation framework. For its intended domain (knowledge graph embeddings), it has solid data preparation capabilities including advanced splitting, efficient preprocessing, and checkpointing. However, it lacks most features expected in a general evaluation harness's PREPARE stage (PII handling, red-teaming, scenario generation, comprehensive quality assessment). The framework does what it's designed to do well, but was not built for the broader evaluation use cases that Stage 2 anticipates.