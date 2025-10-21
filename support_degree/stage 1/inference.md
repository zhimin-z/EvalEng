# mlcommons__inference - Stage 1 (CONFIGURE) Evaluation

## Summary
MLPerf Inference is a comprehensive benchmark suite focused on measuring inference performance across diverse deployment scenarios. The repository provides strong support for dataset/model configuration and environment setup, but shows moderate to limited support for advanced configuration features like schema definition, cost estimation, and security controls. The framework is primarily designed for reproducible performance benchmarking rather than full-featured evaluation workflow management.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | The framework supports multiple dataset sources (ImageNet, COCO, LibriSpeech, etc.) and preprocessing methods but lacks declarative schema definition and formal versioning. Evidence: Multiple dataset download scripts exist (`speech2text/utils/download_librispeech.py`, `text_to_image/tools/download-coco-2014.sh`), and datasets can be registered via CK (`ck install package --tags=dataset,imagenet`). Split strategies are handled manually rather than declaratively (e.g., `graph/R-GAT/tools/split_seeds.py` with hardcoded train/val splits). No formal versioning API exists, though calibration subsets are defined via text files (`calibration/IGBH/calibration.txt`). |
| S1F2: Model Configuration | 2 | Supports multiple providers (TensorFlow, PyTorch, ONNX, TFLite) with basic configuration via files/environment variables, but lacks centralized config API and advanced features. Evidence: Models are configured through environment variables set in shell scripts (`vision/classification_and_detection/run_local.sh` takes backend/model/device params) and CK packages (`ck install package --tags=model,tflite,mlperf,mobilenet`). Auth is basic env vars (`export CHECKPOINT_PATH=...`). No resource allocation validation or multi-region support found. Provider list includes tf, pytorch, onnx, tflite per README but requires manual backend selection. |
| S1F3: Prompt Configuration | 0 | Not applicable - this is an inference benchmark for vision, speech, and graph models, not LLMs requiring prompt templates. The LLM benchmarks (llama2-70b, gpt-j) that do exist focus on token-level metrics rather than prompt engineering. No templating system, parameter sweeps, or prompt versioning infrastructure exists. |
| S1F4: Environment Setup | 2 | Provides dependency specifications and Docker support but requires significant manual setup. Evidence: Multiple `requirements.txt` files exist (`speech2text/requirements.txt`, `text_to_image/requirements.txt`). Docker files are provided (`text_to_image/dockerfile.gpu`, `speech2text/Dockerfile`). LoadGen has build instructions (`loadgen/README_BUILD.md`) with CMake and setup.py. However, setup is fragmented across workloads - no unified environment manager. Dependencies are not consistently pinned (e.g., `pip install torch==2.1.0` in graph/R-GAT/README.md vs. generic `pip install tensorflow` elsewhere). No automated conda/venv management or hardware compatibility checks. |
| S1F5: Security & Access | 1 | Minimal security features - basic environment variable auth only, no RBAC, audit logs, or enterprise integration. Evidence: API keys managed via env vars (`export CK_ENV_TENSORFLOW_MODEL_...` in retired benchmarks). No vault integration, credential rotation, or access control systems found. The LON (LoadGen over Network) demo (`loadgen/demos/lon/README.md`) shows basic Flask client/server but no auth mechanisms. Compliance tests (`compliance/README.md`) focus on accuracy/performance validation, not security auditing. |
| S1F6: Cost Estimation | 0 | No cost estimation, budgeting, or resource projection features exist. The framework focuses purely on performance measurement (QPS, latency) and accuracy metrics. No pricing models, token counting for cost, budget limits, or optimization suggestions found in codebase. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration

Evidence of Dataset Source Support:
```bash
# From speech2text/README.md - LibriSpeech download
$ ./download_dataset.sh
python ${UTILS_DIR}/download_librispeech.py \
    ${UTILS_DIR}/inference_librispeech.csv \
    ${LIBRISPEECH_DIR}
```

```bash
# From text_to_image/tools/download-coco-2014.sh
wget http://images.cocodataset.org/zips/val2017.zip
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
```

```python
# From graph/R-GAT/tools/download_igbh_test.py
# Downloads IGBH dataset from S3
# Supports dataset registration via CK
```

Limited Schema Definition:
No formal schema API exists. Datasets are described informally in README files:
```markdown
# From README.md
| dataset | download link | 
| ---- | ---- | 
| imagenet2012 (validation) | http://image-net.org/challenges/LSVRC/2012/ | 
| coco (validation) | http://images.cocodataset.org/zips/val2017.zip |
```

Split Strategies:
Splits are computed via manual scripts rather than declarative config:
```python
# From graph/R-GAT/tools/split_seeds.py
def split_seeds(path, dataset_size, test_ratio=0.01, calibration=False):
    # Manual train/val split generation
    # No declarative split configuration
```

Versioning:
Version tracking exists informally through model version strings but lacks API:
```bash
# From compliance tests - version specified in filenames
mobilenet_v1_1.0_224_quant_2018_08_02
# No programmatic versioning like dataset_v1.2
```

### S1F2: Model and Backend Configuration

Provider Support:
```bash
# From vision/classification_and_detection/README.md
backend is one of [tf|onnxruntime|pytorch|tflite]
model is one of [resnet50|mobilenet|ssd-mobilenet|ssd-resnet34]
```

```python
# From text_to_image/backend.py
class BackendPytorch(Backend):
    def __init__(self):
        # PyTorch backend implementation
        
class BackendDebug(Backend):
    def __init__(self):
        # Debug backend
```

Configuration Method:
```bash
# From vision/classification_and_detection/run_local.sh
export MODEL_DIR=YourModelFileLocation
export DATA_DIR=YourImageNetLocation
./run_local.sh tf resnet50 gpu
```

Authentication:
Environment variables only:
```bash
# From language/gpt3/megatron/README.md
gcloud auth login
gsutil cp gs://mlperf-llm-public2/vocab/...
# No vault integration or credential rotation
```

### S1F3: Evaluation Parameters and Prompt Configuration

Not Applicable: The benchmark suite focuses on vision (ResNet, MobileNet), speech (Whisper, RNN-T), recommendation (DLRM), and graph (R-GAT) models. While LLM benchmarks exist (llama2-70b, gpt-j), they measure token generation performance rather than prompt engineering:

```python
# From language/llama2-70b/main.py
# No prompt template system - direct token generation
settings.scenario = mlperf.TestScenario.Server
settings.mode = mlperf.TestMode.PerformanceOnly
```

### S1F4: Environment Setup and Dependency Management

Dependency Specification:
```python
# From speech2text/requirements.txt
torch==2.7.0
pandas==2.2.2
sox==1.5.0
```

```python
# From text_to_image/requirements.txt (no version pinning)
torch
diffusers
transformers
```

Containerization:
```dockerfile
# From speech2text/Dockerfile
FROM python:3.12
RUN pip install torch==2.7.0 torchaudio==2.7.0
RUN apt-get install -y ffmpeg sox
```

No Unified Setup:
Each workload requires manual setup with different dependencies. No global environment manager or hardware validation exists.

### S1F5: Security and Access Control

Minimal Security:
```python
# From loadgen/demos/lon/sut_over_network_demo.py
# Flask server with no authentication
@app.route('/predict/', methods=['POST'])
def predict():
    return process_query(query_samples)
```

No RBAC, audit logging, or enterprise SSO found in any configuration files.

### S1F6: Cost Estimation and Budget Planning

No Cost Features:
The framework measures performance metrics (QPS, latency, accuracy) but provides no cost estimation:

```python
# From loadgen/test_settings.h
struct TestSettings {
  Scenario scenario = Scenario::SingleStream;
  double target_qps = 0;
  uint64_t target_latency_ns = 0;
  // No cost-related fields
};
```

## Strengths
1. Multi-source dataset support: Handles ImageNet, COCO, LibriSpeech, IGBH from various sources
2. Multiple backend support: TensorFlow, PyTorch, ONNX, TFLite with consistent interface
3. Docker containerization: Dockerfiles provided for reproducibility
4. Preprocessing flexibility: Multiple methods (OpenCV, Pillow, TensorFlow) with accuracy trade-offs documented

## Weaknesses
1. No schema definition API: Dataset constraints defined informally in docs
2. Manual environment setup: Fragmented across workloads, no unified config system
3. Basic authentication: Only env vars, no secrets management
4. No cost features: Pure performance benchmark, no resource estimation
5. Limited versioning: Informal through filenames, no programmatic API
6. No split configuration: Train/val splits computed manually rather than declaratively

## Conclusion
MLPerf Inference scores 7/18 for Stage 1 (CONFIGURE). It provides adequate but not excellent support for dataset/model configuration (2+2 points) and basic environment setup (2 points). However, it completely lacks prompt configuration (N/A for this domain), security/access features (1 point), and cost estimation (0 points). The framework excels at reproducible benchmarking but was not designed as a full configuration management system for evaluation workflows.