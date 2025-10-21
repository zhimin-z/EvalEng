# VLMEvalKit (open-compass/VLMEvalKit) - Stage 2 (PREPARE) Evaluation

## Summary
VLMEvalKit is a comprehensive evaluation toolkit for Large Vision-Language Models (VLMs). Its preparation stage focuses heavily on inference and API integration rather than traditional data preprocessing. The framework excels at model configuration and API setup but lacks explicit data quality assessment, PII handling, and contamination detection features. Its strength lies in flexible model/dataset configuration and extensive benchmark support.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing utilities; relies on pre-processed TSV files |
| S2F2: Quality Assessment | 0 | No built-in dataset quality assessment tools |
| S2F3: PII Detection | 0 | No PII detection or anonymization features |
| S2F4: Infrastructure Building | 1 | Basic model loading, no specialized retrieval/DB infrastructure |
| S2F5: Model Validation | 1 | Basic model loading checks, no comprehensive validation |
| S2F6: Scenario Generation | 2 | Dataset-level prompt building with customization support |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial testing features |
| S2F8: Contamination Detection | 0 | No contamination detection capabilities |

---

## Detailed Analysis

### S2F1: Dataset Preprocessing and Physical Partitioning
Rating: 1/3

Evidence:

1. Data Format Requirements (README.md, docs/en/Development.md):
```markdown
Currently, we organize a benchmark as one single TSV file. During inference, 
the data file will be automatically downloaded from the definited DATASET_URL 
link to $LMUData file
```

The framework expects pre-processed TSV files with specific fields:
```python
# From docs/en/Development.md - Table 1
| Dataset Name \ Fields | index | image | image_path | question | hint | 
| multi-choice options | answer | category | l2-category | split |
```

2. Image Encoding/Decoding (docs/en/Development.md):
```markdown
- image: The base64 of the image, you can use APIs implemented in 
  `vlmeval/smp/vlm.py` for encoding and decoding:
  - Encoding: `encode_image_to_base64` (for PIL Image) / 
    `encode_image_file_to_base64` (for image file path)
  - Decoding: `decode_base64_to_image` (for PIL Image) / 
    `decode_base64_to_image_file` (for image file path)
```

3. No Explicit Preprocessing Pipeline:
- No code for tokenization, normalization, or augmentation
- No automated splitting utilities
- Data must be pre-split and uploaded as TSV

Limitations:
- Users must manually preprocess data before evaluation
- No caching mechanisms described for preprocessed data
- No stratified splitting or version control for splits
- Relies entirely on external data preparation

Rating Justification: The framework provides basic image encoding/decoding utilities but lacks comprehensive preprocessing pipelines. Data must arrive pre-processed in TSV format, earning only 1 point for minimal preprocessing support.

---

### S2F2: Dataset Quality and Bias Assessment
Rating: 0/3

Evidence:

1. No Quality Tools Found: Searching through the codebase reveals no:
   - Label quality checks
   - Demographic distribution analysis
   - Duplicate detection utilities
   - Bias detection mechanisms

2. Focus on Evaluation, Not Preparation:
From `run.py` and documentation, the workflow is:
```
Load TSV → Build Prompt → Model Inference → Evaluation
```

No intermediate quality assessment step exists.

3. Manual Quality Control Only:
From docs/en/Development.md:
```markdown
You can upload the prepared TSV file to a downloadable address (e.g., Huggingface) 
or send it to us at opencompass@pjlab.org.cn. We will assist in uploading the 
dataset to the server.
```

Quality is implicitly trusted after manual upload.

Rating Justification: Complete absence of automated quality assessment features warrants a 0 rating.

---

### S2F3: PII Detection and Anonymization
Rating: 0/3

Evidence:

1. No PII Handling Code: Searching for terms like "PII", "privacy", "anonymize", "redact" yields no results in:
   - `vlmeval/dataset/`
   - `vlmeval/smp/`
   - Documentation files

2. Environment Variables for API Keys Only (.env example):
```bash
# .env file, place it under $VLMEvalKit
# API Keys of Proprietary VLMs
DASHSCOPE_API_KEY=
GOOGLE_API_KEY=
OPENAI_API_KEY=
```

This handles API security, not dataset PII.

3. No Privacy Documentation:
- No GDPR/CCPA compliance mentions
- No data sanitization guides
- No audit trails for sensitive data

Rating Justification: Complete absence of PII detection, anonymization, or privacy features results in a 0 rating.

---

### S2F4: Task-Specific Infrastructure Building
Rating: 1/3

Evidence:

1. Model Loading Infrastructure (vlmeval/config.py):
```python
supported_VLM = {}
model_groups = [
    ungrouped, o1_apis, api_models, xtuner_series, qwen_series, llava_series,
    # ... 200+ models configured
]
for grp in model_groups:
    supported_VLM.update(grp)
```

Basic model registry exists, but no retrieval indices or databases.

2. API Configuration (vlmeval/api/):
Multiple API wrappers exist (GPT4V, Gemini, Claude, etc.), but these are for inference, not infrastructure building.

3. No Retrieval Systems:
- No FAISS/ColBERT/BM25 index building
- No vector database setup
- No specialized task environments

4. Video Processing (vlmeval/dataset/video_dataset_config.py):
Some frame extraction for video models:
```python
# Example from config
"MMBench_Video_8frame_nopack": {
    'class': 'MMBenchVideo', 
    'dataset': 'MMBench-Video', 
    'nframe': 8, 
    'pack': False
}
```

This is basic preprocessing, not infrastructure.

Rating Justification: Only basic model loading and API configuration exist. No specialized retrieval systems, databases, or task environments, earning 1 point for minimal infrastructure support.

---

### S2F5: Model Artifact Validation
Rating: 1/3

Evidence:

1. Basic Model Check (docs/en/Quickstart.md):
```bash
# Make sure you can successfully infer with the VLM before starting the evaluation
vlmutil check {MODEL_NAME}
```

This exists but details are sparse.

2. Transformer Version Recommendations (README.md):
```markdown
Transformers Version Recommendation:
- Please use `transformers==4.33.0` for: `Qwen series`, `Monkey series`
- Please use `transformers==4.37.0` for: `LLaVA series`, `ShareGPT4V series`
```

Manual version management, not automated validation.

3. No Checksum Validation:
- No SHA256 verification code found
- No automatic integrity checks
- Users must manually ensure model correctness

4. Dataset MD5 Checks (docs/en/Development.md):
```python
# In dataset class
'DATASET_MD5' is the MD5 checksum for consistency checking of the dataset file.
```

Dataset validation exists, but model validation is minimal.

Rating Justification: Basic model loading checks and version warnings exist, but no cryptographic validation, corruption detection, or comprehensive integrity verification. Earns 1 point for minimal validation.

---

### S2F6: Evaluation Scenario Generation
Rating: 2/3

Evidence:

1. Dataset-Level Prompt Building (vlmeval/dataset/image_base.py concept from docs):
```python
def build_prompt(self, line):
    """
    Input: line (int or pd.Series) - sample index or raw record
    Output: multi-modal message list
    Example: [dict(type='image', value=IMAGE_PTH), 
              dict(type='text', value=prompt)]
    """
```

Each dataset class can customize prompts.

2. Model-Level Customization (docs/zh-CN/Quickstart.md):
```markdown
VLMEvalKit also supports customizing the prompt construction method at the 
model level through `model.build_prompt()`. 

Note: If both `model.build_prompt()` and `dataset.build_prompt()` are defined, 
`model.build_prompt()` will take precedence.
```

3. Configuration System (docs/en/ConfigSystem.md):
```json
{
    "data": {
        "Video-MME_16frame_subs": {
            "class": "VideoMME",
            "dataset": "Video-MME",
            "nframe": 16,
            "use_subtitle": true
        }
    }
}
```

Allows parameter sweeps (e.g., different frame counts).

4. Example Prompt Template (docs/en/Development.md):
```
HINT
QUESTION
Options:
A. Option A
B. Option B
Please select the correct answer from the options above.
```

Limitations:
- No multi-turn dialogue generation beyond inference
- No explicit edge case generators
- No adversarial input creation
- Reproducibility depends on dataset, not explicit seeds

Rating Justification: Solid prompt building with dataset/model customization and parameter sweeps, but lacks multi-turn generation, edge case automation, and explicit reproducibility mechanisms. Earns 2 points for basic variation generation with limited multi-turn support.

---

### S2F7: Red-Teaming and Adversarial Test Generation
Rating: 0/3

Evidence:

1. No Red-Teaming Code: Search for "jailbreak", "adversarial", "red-team", "attack" in:
   - `vlmeval/dataset/`
   - `vlmeval/vlm/`
   - Documentation

Returns no relevant results.

2. No Safety Testing Benchmarks: While 70+ benchmarks are supported (see README.md), none are explicitly red-teaming focused like:
   - Prompt injection tests
   - Bias probing suites
   - Safety boundary exploration

3. Evaluation Focus Only: The framework evaluates models on existing benchmarks but doesn't generate adversarial tests.

Rating Justification: Complete absence of red-teaming, adversarial generation, or safety testing features results in a 0 rating.

---

### S2F8: Data Contamination Detection
Rating: 0/3

Evidence:

1. No Contamination Tools: Searching for "contamination", "overlap", "leakage" yields no results in the codebase.

2. No Training Data Comparison: The framework has no mechanism to:
   - Compare eval data against training corpora
   - Detect n-gram overlaps
   - Identify semantic similarity with training data

3. Evaluation-Only Scope: From README.md:
```markdown
VLMEvalKit (the python package name is vlmeval) is an open-source evaluation 
toolkit of large vision-language models (LVLMs). It enables one-command evaluation 
of LVLMs on various benchmarks.
```

The toolkit evaluates, not validates contamination.

Rating Justification: No contamination detection features exist, warranting a 0 rating.

---

## Overall Assessment

Strengths:
1. Extensive Model Support: 200+ VLMs configured with flexible API integration
2. Rich Benchmark Coverage: 70+ image/video benchmarks supported
3. Flexible Configuration: JSON-based model/dataset configuration system (docs/en/ConfigSystem.md)
4. Prompt Customization: Dataset and model-level prompt building

Critical Gaps:
1. No Data Quality Tools: No label validation, bias detection, or duplicate checking
2. No Privacy Features: No PII detection or anonymization
3. No Security Testing: No red-teaming or adversarial generation
4. Minimal Preprocessing: Expects pre-processed TSV files, no pipelines
5. No Contamination Checks: No training data overlap detection

Use Case Alignment:
VLMEvalKit is designed for inference and evaluation, not comprehensive data preparation. Its Stage 2 focuses on:
- Loading pre-prepared data
- Configuring models/APIs
- Building evaluation prompts

It assumes data arrives clean and processed, making it suitable for researchers with pre-curated benchmarks but insufficient for practitioners needing end-to-end data preparation pipelines.

Recommendation:
For users requiring robust data preparation (quality checks, PII handling, contamination detection), VLMEvalKit should be paired with external tools. Its value lies in evaluation infrastructure, not data engineering.