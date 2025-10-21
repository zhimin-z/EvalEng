# OpenCompass - Stage 2 (PREPARE) Evaluation

## Summary
OpenCompass provides moderate data preparation capabilities focused on dataset loading and configuration. It excels at dataset management through configs but lacks comprehensive preprocessing pipelines, quality assessment tools, PII detection, contamination checking, and advanced infrastructure building features. Most preparation work relies on external preprocessing or manual setup.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Limited preprocessing utilities. The framework primarily loads datasets from HuggingFace/ModelScope with basic caching. Evidence: README mentions "Support for streaming large datasets" and ModelScope integration (`export DATASET_SOURCE=ModelScope`), but no preprocessing pipelines, tokenization, or data transformation APIs found in the codebase. Users must rely on upstream dataset formats. No examples of custom preprocessing, validation, or physical splitting beyond what HuggingFace provides. |
| S2F2: Quality Assessment | 0 | No quality assessment features. Extensive review of documentation and configs reveals no tools for label quality checking, demographic distribution analysis, duplicate detection, or bias assessment. The platform assumes datasets are already curated and validated. No quality metrics, inter-annotator agreement, or outlier detection capabilities mentioned or implemented. |
| S2F3: PII Detection | 0 | No PII handling capabilities. Documentation and codebase show no mention of PII detection, anonymization, or privacy features. No regex patterns, NER models, or redaction strategies. The framework focuses purely on evaluation, not data privacy compliance. |
| S2F4: Infrastructure Building | 1 | Minimal infrastructure support. While the platform supports various inference backends (LMDeploy, vLLM via `-a lmdeploy` flag in README), there's no evidence of retrieval index building (FAISS, ColBERT, BM25), database setup, or specialized environment creation. The "infrastructure" is limited to model serving backends, not evaluation-specific data structures. Example: `opencompass --models hf_internlm2_5_1_8b_chat --datasets demo_gsm8k_chat_gen -a lmdeploy` shows backend switching but no index/DB utilities. |
| S2F5: Model Validation | 1 | Basic validation only. The framework appears to rely on HuggingFace's model loading which includes basic integrity checks, but no explicit checksum validation, version compatibility checking, or corruption detection mentioned in docs. No examples of cryptographic verification or test inference validation. The `tools/test_api_model.py` suggests basic connectivity testing but not comprehensive validation. |
| S2F6: Scenario Generation | 2 | Limited scenario generation. The platform supports prompt templates and few-shot configuration (examples show "1shot", "5shot" variants in dataset names like `triviaqa_wiki_1shot_gen_20a989`), but no evidence of sophisticated variation generation, multi-turn dialogues, edge case generation, or combinatorial scenario creation. Config files define static prompts rather than dynamic generation. File structure shows extensive dataset configs but not scenario generators. |
| S2F7: Red-Teaming | 0 | No red-teaming capabilities. Despite extensive dataset support (270+ datasets per docs), no jailbreak libraries, adversarial generation, prompt injection tests, or safety boundary testing found. No attack taxonomies or red-team frameworks in `opencompass/datasets/` or examples. Evaluation is standard benchmark testing, not adversarial. |
| S2F8: Contamination Detection | 1 | Minimal contamination checking. The example `eval_contamination.py` in the file list suggests some contamination detection exists, but no documentation on methods (n-gram overlap, semantic similarity), configuration options, or detailed reporting. This appears to be a basic utility rather than comprehensive contamination analysis. No evidence of fingerprinting or multi-corpus comparison. |

## Detailed Analysis

### S2F1: Dataset Preprocessing and Physical Partitioning (1/3)

Evidence:
- README states datasets can be loaded from HuggingFace/ModelScope with automatic download: "We have supported download datasets automatic from the OpenCompass storage server"
- Installation shows ModelScope support: `pip install modelscope[framework]` + `export DATASET_SOURCE=ModelScope`
- However, no preprocessing APIs found. The `/configs/datasets/` contains 270+ dataset configs but these are primarily loading configurations, not transformation pipelines

Missing capabilities:
- No tokenization/normalization utilities beyond model-specific
- No image/audio preprocessing mentioned
- No custom transform definitions
- No stratified splitting or versioned splits
- Physical splitting relies on upstream dataset structure

Why 1 point: Loads and caches data but no preprocessing framework. Users must prepare data externally.

### S2F2: Dataset Quality and Bias Assessment (0/3)

Evidence:
- Extensive search through docs and structure reveals no quality tooling
- Dataset statistics page (referenced in README: "数据集统计章节") focuses on coverage, not quality
- No `quality/` or `bias/` directories in codebase
- No mention of label validation, demographic analysis, or duplicate detection in any documentation

Why 0 points: Completely absent. Platform assumes pre-validated datasets.

### S2F3: PII Detection and Anonymization (0/3)

Evidence:
- No privacy-related files or modules
- README sections on dataset preparation make no mention of PII
- No GDPR/CCPA compliance features
- No redaction or anonymization utilities

Why 0 points: Not a concern for this benchmark evaluation platform. Users responsible for data privacy before submission.

### S2F4: Task-Specific Infrastructure Building (1/3)

Evidence:
- Inference backend support: "OpenCompass now supports one-click switching between inference acceleration backends" (LMDeploy, vLLM)
- Command: `opencompass --models hf_internlm2_5_1_8b_chat --datasets demo_gsm8k_chat_gen -a lmdeploy`
- But no retrieval systems (FAISS, BM25, Elasticsearch) or database setup tools
- No agent environment or simulation infrastructure beyond model serving

Missing:
- No index building for RAG systems
- No vector DB integration
- No specialized evaluation environments
- No artifact versioning beyond model configs

Why 1 point: Supports inference backends but lacks evaluation-specific infrastructure like retrieval indices or custom environments.

### S2F5: Model Artifact Validation (1/3)

Evidence:
- `tools/test_api_model.py` suggests basic API testing
- Relies on HuggingFace's model loading which includes basic checks
- No explicit validation documentation or examples
- No checksum databases or version compatibility matrices

Why 1 point: Basic model loading validation via upstream libraries, but no comprehensive validation framework.

### S2F6: Evaluation Scenario Generation (2/3)

Evidence:
- Dataset naming shows shot-based variations: `mmlu_ppl_ac766d`, `triviaqa_wiki_1shot_gen_20a989`, `winogrande_5shot_ll_252f01`
- Config files define prompt templates (referenced but not shown in provided excerpts)
- `opencompass/openicl/icl_prompt_template.py` exists in structure
- However, no multi-turn dialogue generation or edge case generators visible

Capabilities present:
- Few-shot configuration (0-shot, 1-shot, 5-shot variations)
- Prompt template system
- Multiple dataset variants (ppl vs gen evaluations)

Missing:
- Dynamic scenario generation
- Combinatorial test creation
- Adversarial edge cases
- Multi-turn conversation scenarios

Why 2 points: Supports prompt templates and shot-based variations but lacks advanced generation capabilities. Static configuration-based rather than dynamic generation.

### S2F7: Red-Teaming and Adversarial Test Generation (0/3)

Evidence:
- `examples/eval_attack.py` in file list suggests some attack evaluation
- But no documentation, no red-team libraries, no jailbreak collections
- No safety benchmarks like ToxicGen or adversarial prompt datasets
- Focus is on standard academic benchmarks (MMLU, GSM8K, etc.)

Why 0 points: Despite an attack example file, no comprehensive red-teaming framework. Basic evaluation only.

### S2F8: Data Contamination Detection (1/3)

Evidence:
- `examples/eval_contamination.py` exists in file structure
- But no documentation on methodology, configuration, or usage
- No n-gram overlap tools, semantic similarity checking, or reporting mentioned
- Appears to be a basic utility without comprehensive features

Why 1 point: Has a contamination detection script but no documentation or evidence of sophisticated detection methods. Likely a minimal implementation.

## Key Strengths
1. Extensive dataset coverage - 270+ benchmark datasets pre-configured
2. Multiple inference backends - Easy switching between HuggingFace, LMDeploy, vLLM
3. Configuration-driven - Well-structured configs for reproducible evaluation
4. Shot-based variations - Supports different few-shot configurations

## Key Weaknesses
1. No preprocessing framework - Relies entirely on pre-processed datasets
2. No quality assurance tools - No bias detection, duplicate checking, or label validation
3. No privacy features - No PII handling or anonymization
4. Limited infrastructure - No retrieval systems, DBs, or custom environments
5. No red-teaming - Standard benchmarking only, no adversarial testing
6. Minimal validation - Basic model loading checks, no comprehensive validation

## Recommendations for Improvement
1. Add preprocessing pipelines for text normalization, tokenization, format validation
2. Implement quality assessment tools (duplicate detection, label consistency checks)
3. Provide contamination detection with n-gram overlap and semantic similarity
4. Support retrieval index building for RAG evaluation
5. Add red-team prompt libraries and adversarial test generation
6. Create scenario generation APIs for dynamic test case creation

## Overall Stage 2 Score: 6/24 (25%)

OpenCompass is primarily an evaluation execution platform rather than a data preparation framework. It assumes datasets arrive pre-processed and validated, focusing its efforts on running benchmarks efficiently across models. For comprehensive data preparation, users need external tools and manual preprocessing workflows.