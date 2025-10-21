# prometheus-eval/prometheus-eval - Stage 2 (PREPARE) Evaluation

## Summary
Prometheus-eval is primarily an evaluation framework focused on using LLMs to judge other LLMs' outputs, not a comprehensive data preparation toolkit. The repository contains evaluation benchmarks (BiGGen-Bench) and trained evaluator models, but lacks systematic data preparation, quality assessment, and infrastructure building capabilities expected in Stage 2.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Evidence: The repo focuses on evaluation, not data prep. The `BiGGen-Bench/run_api_inference.py` script loads pre-existing datasets from HuggingFace without preprocessing: `dataset = load_dataset("prometheus-eval/BiGGen-Bench", split="train")` (inferred from structure). The training README (`train/README.md`) mentions using `get_datasets()` function but provides no preprocessing utilities, caching mechanisms, or versioned splits. The `train/recipes/prometheus-v2.0/README.md` only shows `python prepare_dataset.py` without details on what preprocessing occurs. No evidence of tokenization pipelines, image/audio processing, or validation mechanisms. |
| S2F2: Quality Assessment | 0 | Evidence: No quality assessment tools found. Searched for duplicate detection, label noise detection, demographic analysis, or bias detection utilities. The evaluation scripts (`BiGGen-Bench/run_response_eval.py`) only evaluate model outputs against rubrics, not dataset quality. No code for inter-annotator agreement, outlier detection, or balance metrics. The task documentation mentions data annotators/reviewers but provides no tooling for quality checks. |
| S2F3: PII Detection | 0 | Evidence: No PII detection or anonymization features present. Grepped documentation and code for "PII", "privacy", "anonymization", "redact" with no results. The `README.md` mentions safety evaluation tasks (`BiGGen-Bench/tasks/safety/`) but these test model outputs for safety, not dataset privacy. No GDPR/CCPA compliance tooling mentioned. |
| S2F4: Infrastructure Building | 1 | Evidence: Minimal infrastructure support. The `libs/prometheus-eval/` package provides basic VLLM and LiteLLM wrappers for model inference (`prometheus_eval/vllm.py`, `prometheus_eval/litellm.py` inferred from README examples), but no retrieval system building (FAISS, BM25, Elasticsearch), database setup, or artifact versioning. The training recipes use standard HuggingFace/DeepSpeed configs (`train/recipes/accelerate_configs/`) but don't build custom infrastructure. No evidence of index persistence, vector DB integration, or cloud storage management. |
| S2F5: Model Validation | 1 | Evidence: Basic model loading via HuggingFace but no explicit validation. The README shows model loading: `model = AutoModelForCausalLM.from_pretrained("prometheus-eval/prometheus-7b-v2.0")` which uses HuggingFace's default validation. No custom checksum verification mentioned. The `train/scripts/run_sft.py` and `train/scripts/run_dpo.py` (referenced in `train/README.md`) likely validate configs but details not shown. No corruption detection, version compatibility checks beyond HuggingFace defaults, or test inference validation described. |
| S2F6: Scenario Generation | 1 | Evidence: Limited scenario generation through prompt templates. The `libs/prometheus-eval/README.md` shows `ABSOLUTE_PROMPT` and `RELATIVE_PROMPT` templates with variable substitution: `ABSOLUTE_PROMPT.format(instruction=..., response=..., rubric=...)`. However, this is basic string formatting, not sophisticated scenario generation. No parameter sweeps, multi-turn dialogue generation, edge case generators, or combinatorial generation. The BiGGen-Bench tasks are manually curated (as evidenced by task READMEs listing specific data annotators), not programmatically generated. No reproducibility mechanisms like seeded generation mentioned. |
| S2F7: Red-Teaming | 1 | Evidence: BiGGen-Bench includes safety evaluation tasks (`BiGGen-Bench/tasks/safety/` mentioned in `BiGGen-Bench/tasks/README.md`) but no automated red-teaming framework. The safety tasks test model responses to pre-defined scenarios, not generate adversarial inputs. No jailbreak library, prompt injection generators, or attack taxonomies found. The `BiGGen-Bench/tasks/safety/README.md` (not provided but referenced) likely contains static test cases. No evidence of escalating severity levels, multi-category safety testing automation, or attack success detection beyond manual scoring with rubrics. |
| S2F8: Contamination Detection | 0 | Evidence: No contamination detection capabilities found. No code for comparing eval data against training corpora, n-gram overlap detection, or semantic similarity checks. The papers cited (`README.md`: "Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models") focus on evaluation quality, not training data contamination. The training scripts (`train/scripts/run_sft.py`, `train/scripts/run_dpo.py`) don't mention contamination checks. No fingerprinting, embedding-based comparison, or contamination reporting tools present. |

## Key Observations

### Strengths
1. Clear evaluation framework: Well-documented process for using Prometheus models to evaluate other LLMs with absolute and relative grading
2. Rich benchmark: BiGGen-Bench provides 77 tasks across 9 capabilities with detailed rubrics and reference answers
3. Multiple inference modes: Supports local (VLLM) and API-based (LiteLLM) inference with various providers

### Limitations for Stage 2
1. Not a data preparation framework: Primary focus is on evaluation post-hoc, not preparing datasets for training/evaluation
2. Manual curation dependency: BiGGen-Bench tasks are manually created by annotators (see `BiGGen-Bench/tasks/README.md` attribution tables), not generated programmatically
3. Minimal preprocessing utilities: No evidence of sophisticated data loading, validation, caching, or splitting mechanisms
4. No quality/privacy tooling: Lacks automated quality assessment, PII detection, bias detection, or contamination checking
5. Limited infrastructure: Provides model wrappers but no retrieval systems, databases, or artifact management beyond HuggingFace defaults

### Evidence of Manual Process
From `BiGGen-Bench/tasks/README.md`:
```markdown
Name | Description | Data Annotator (Group A) | Data Reviewer (Group A) | Data Annotator (Group B)
---- | ----------- | -------------------- | -------------------- | -------------------- |
[instruction_following](instruction_following/) | ... | Chaeeun Kim, Guijin Son | Yejin Cho, Miyoung Ko, Hanseok Oh, Jinkyung Jo | ? |
```

This attribution system indicates manual data creation rather than automated preparation pipelines.

### Training Pipeline Gap
From `train/recipes/prometheus-v2.0/README.md`:
```shell
# Step 1 - Prepare Dataset
python prepare_dataset.py
```

The `prepare_dataset.py` script is referenced but not provided in the repository structure, and no documentation explains what preprocessing it performs (checksums, splits, validation, etc.).

## Conclusion

Prometheus-eval scores 8/24 (33%) on Stage 2 criteria. It's a specialized evaluation framework with minimal data preparation capabilities. The repository excels at model-based evaluation but lacks the comprehensive data preprocessing, quality assessment, privacy protection, infrastructure building, and contamination detection features needed for a full-fledged Stage 2 evaluation harness. Organizations seeking data preparation tooling would need to build these capabilities separately or use complementary frameworks.