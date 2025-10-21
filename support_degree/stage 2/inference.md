# mlcommons__inference - Stage 2 (PREPARE) Evaluation

## Summary
MLCommons Inference is a comprehensive benchmarking framework for measuring inference system performance across diverse deployment scenarios. Stage 2 (PREPARE) capabilities are highly limited. The framework primarily focuses on performance/accuracy testing with LoadGen, with minimal built-in support for dataset preparation, quality assessment, or infrastructure building. Most preparation tasks are left to reference implementations or external tools.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Reference implementations contain preprocessing (e.g., `speech2text/utils/convert_librispeech.py`, `text_to_image/tools/coco.py`), but these are scattered scripts, not a unified framework. No caching beyond manual file storage. Evidence: `vision/classification_and_detection/README.md` lists manual dataset preparation steps. No preprocessing API in LoadGen core. |
| S2F2: Quality Assessment | 0 | No dataset quality/bias assessment tools found. Accuracy evaluation scripts exist (e.g., `compliance/TEST01/verify_accuracy.py`), but only for post-run validation, not dataset quality analysis. No demographic distribution, duplicate detection, or bias probing capabilities. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features found in codebase. Search for "PII", "privacy", "anonymize" yields no relevant results. Dataset scripts assume pre-sanitized public datasets. |
| S2F4: Infrastructure Building | 1 | Limited retrieval system support for RGAT (DGL graph operations in `graph/R-GAT/tools/`). No general index building (FAISS, BM25, etc.). Database setup mentioned only in DLRM context without infrastructure utilities. Evidence: `graph/R-GAT/dataset.py` loads pre-built graphs, doesn't build indices. |
| S2F5: Model Validation | 2 | Basic checksum validation via R2 downloader (`tools/r2-downloader` references in READMEs). Model loading attempts serve as corruption detection. Version compatibility checks exist but are minimal. Example: `language/llama2-70b/README.md` shows manual SHA verification. No comprehensive integrity framework. |
| S2F6: Scenario Generation | 1 | LoadGen generates query patterns (SingleStream, Offline, Server, MultiStream) but not prompt variations or edge cases. Scenarios are fixed, not parameterized. Evidence: `loadgen/test_settings.h` defines scenarios but no variation generation. Compliance tests (e.g., `compliance/TEST04/`) use fixed `audit.config` overrides, not generated variations. |
| S2F7: Red-Teaming | 0 | No red-teaming, adversarial generation, or safety testing capabilities. Search for "jailbreak", "adversarial", "red-team" yields no results. Focus is on performance, not robustness testing. |
| S2F8: Contamination Detection | 0 | No contamination detection between training/eval data. Calibration datasets exist (e.g., `calibration/COCO/`) but no n-gram overlap or semantic similarity checks. No tooling to compare eval against training corpora. |

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (Rating: 1)

Evidence of minimal preprocessing utilities:
- Speech2text preprocessing (`speech2text/utils/convert_librispeech.py`):
```python
# Manual conversion script, not integrated framework
def convert_librispeech(input_dir, dest_dir, output_json):
    # Converts FLAC to WAV, creates manifest
```
- Vision preprocessing (`vision/classification_and_detection/README.md`):
```md
### Prepare the coco dataset 
The tool is [here](../../tools/upscale_coco).
You can run it for ssd-mobilenet like:
```
python upscale_coco.py --inputs /data/coco/ --outputs /data/coco-300 --size 300 300 --format png
```
```
This is a standalone script, not a reusable preprocessing pipeline.

- Text-to-image preprocessing (`text_to_image/tools/coco.py`):
```python
# Custom preprocessing per benchmark, no unified API
class Coco:
    def __init__(self, ...):
        # Loads and preprocesses COCO captions
```

Limitations:
- No caching mechanism beyond manual file writes
- No validation/checksum post-preprocessing
- Stratified splitting: Referenced in retired benchmarks (e.g., RNNT) but not in current benchmarks
- Example from `retired_benchmarks/speech_recognition/rnnt/README.md`: "We remove all samples with a length exceeding 15 seconds" - manual filtering, not automated

Why not 2 points: While preprocessing exists, it's fragmented across benchmarks with no unifying framework, no automatic caching, and minimal validation.

### S2F2: Dataset Quality and Bias Assessment (Rating: 0)

Search results for quality assessment:
- No files matching "label_quality", "demographic", "duplicate_detection", "bias_assessment"
- Accuracy evaluation exists (e.g., `tools/accuracy-imagenet.py`):
```python
def main():
    # Compares predictions to ground truth, computes Top-1/Top-5
    # No quality checks on dataset itself
```
- Compliance tests (`compliance/TEST01/README.md`) validate result accuracy, not dataset quality:
```md
The purpose of this test is to ensure that valid inferences are being performed in performance mode.
```

Why 0 points: No tools to analyze label noise, demographic distributions, or systematic biases in datasets. Framework assumes datasets are pre-validated.

### S2F3: PII Detection and Anonymization (Rating: 0)

Evidence of absence:
- Grep for "PII", "privacy", "anonymize", "redact": No relevant results
- Dataset READMEs (e.g., `text_to_image/README.md`) reference public datasets without PII handling:
```md
| dataset | download link | 
| ---- | ---- | 
| coco (validation) | http://images.cocodataset.org/zips/val2017.zip | 
```
- No GDPR/CCPA compliance mentions

Why 0 points: Framework provides no PII detection or anonymization capabilities.

### S2F4: Task-Specific Infrastructure Building (Rating: 1)

Limited infrastructure support:
- RGAT graph loading (`graph/R-GAT/dataset.py`):
```python
class Dataset_DGL:
    def __init__(self, ...):
        # Loads pre-built DGL graphs
        self.graph = dgl.load_graphs(...)
```
This loads existing graphs, doesn't build indices.

- No retrieval system builders: Search for "FAISS", "ColBERT", "BM25" yields no results
- No database setup utilities: DLRM references databases but no setup tools:
```md
# recommendation/dlrm_v2/pytorch/README.md
- Criteo Terabyte dataset requires preprocessing (not provided)
```

Why not 0: Graph benchmark has some infrastructure code, but it's domain-specific and doesn't build indices. Why not 2: No general retrieval/database utilities.

### S2F5: Model Validation (Rating: 2)

Checksum validation via R2 downloader:
- Example from `language/gpt-j/README.md`:
```bash
# R2 downloader verifies checksums during download
bash <(curl -s https://raw.githubusercontent.com/mlcommons/r2-downloader/refs/heads/main/mlc-r2-downloader.sh) \
  https://inference.mlcommons-storage.org/metadata/gpt-j-model.uri
```
R2 downloader (external tool) handles SHA256 verification.

- Version compatibility: Minimal checks in LoadGen (`loadgen/version.h`):
```cpp
#define MLPERF_LOADGEN_VERSION "v3.1"
// Version logged but no enforcement of model compatibility
```

- Corruption detection via load attempts: Models fail to load if corrupted, but no explicit integrity checks:
```python
# Example from language/llama2-70b/main.py
model = torch.load(args.model_path)  # Fails if corrupted
```

Why 2 points: Basic checksum validation exists via external tool, version tracking present, but no comprehensive integrity verification framework.

### S2F6: Evaluation Scenario Generation (Rating: 1)

LoadGen scenario handling:
- `loadgen/test_settings.h` defines fixed scenarios:
```cpp
enum class TestScenario {
  SingleStream,
  MultiStream,
  Server,
  Offline
};
```
No parameterized variation generation.

- Compliance test scenarios (`compliance/TEST04/audit.config`):
```
*.Server.target_qps = 1
# Fixed override, not generated variations
```

- No prompt variation support: Language models use fixed prompts from datasets (e.g., `language/gpt-j/dataset.py`):
```python
def load_samples(self):
    # Loads fixed prompts from CNN-DailyMail
    for item in dataset:
        self.samples.append(item['article'])
```

Why not 0: LoadGen does generate query patterns (timing, batching), but no semantic variations. Why not 2: No edge case generation or parameterized prompt templates.

### S2F7: Red-Teaming and Adversarial Test Generation (Rating: 0)

Evidence of absence:
- No files matching "jailbreak", "adversarial", "red-team", "safety"
- Compliance tests focus on performance/accuracy, not robustness:
```md
# compliance/README.md
The purpose of compliance testing is to ensure a basic level of compliance with a subset of the MLPerf rules.
```
- No bias probing or attack generation in LLM benchmarks

Why 0 points: Framework provides no adversarial testing or safety boundary exploration.

### S2F8: Data Contamination Detection (Rating: 0)

Evidence of absence:
- Calibration datasets exist (`calibration/COCO/coco_cal_images_list.txt`) but no contamination checks:
```
# List of image IDs for calibration
000000397133
000000037777
```
No tools to compare against training data.

- No n-gram overlap detection: Search yields no results
- No semantic similarity checks: No embedding-based contamination detection

Example from `retired_benchmarks/speech_recognition/rnnt/README.md` shows manual filtering:
```md
We remove all samples with a length exceeding 15 seconds.
```
This is manual, not automated contamination detection.

Why 0 points: No contamination detection capabilities provided.

## Key Strengths
1. Model validation via checksums: R2 downloader provides SHA256 verification
2. Preprocessing examples: Reference implementations include preprocessing scripts
3. Version tracking: LoadGen logs version information for reproducibility

## Key Weaknesses
1. No unified preprocessing framework: Each benchmark has custom scripts
2. No quality/bias assessment: Assumes pre-validated datasets
3. No PII handling: No privacy-preserving utilities
4. No infrastructure builders: No tools to build retrieval indices or databases
5. No contamination detection: No overlap checking between train/eval
6. No adversarial testing: Focus on performance, not robustness

## Recommendations for Improvement
1. Create unified preprocessing API with caching and validation (like Hugging Face Datasets)
2. Add dataset quality checks: Duplicate detection, label consistency, demographic analysis
3. Implement contamination detection: N-gram overlap and semantic similarity checks for LLM benchmarks
4. Add infrastructure builders: Generic utilities for FAISS/BM25 index creation
5. Integrate red-teaming: Jailbreak libraries and bias probing for safety-critical models

## Conclusion
MLCommons Inference excels at Stage 3 (EXECUTE) with LoadGen, but Stage 2 (PREPARE) is underdeveloped. The framework treats preparation as a pre-requisite handled externally, providing only scattered reference scripts rather than reusable utilities. For official benchmarking, this is acceptable given the focus on reproducibility of inference measurement. However, expanding PREPARE capabilities would improve usability for practitioners.