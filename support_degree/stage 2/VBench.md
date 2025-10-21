# VBench/Vchitect__VBench - Stage 2 (PREPARE) Evaluation

## Summary
VBench is a comprehensive video generation evaluation framework that focuses on runtime evaluation of pre-generated videos rather than data preparation infrastructure. The repository contains minimal data preprocessing capabilities, no quality assessment tools, no PII detection, and no infrastructure building utilities. It assumes videos are already generated and properly formatted, making it primarily an evaluation-only framework rather than a full data preparation suite.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing exists. Videos must be pre-generated and follow strict naming conventions (`prompt-index.mp4`). No data loading utilities, no caching, no validation. Only basic format requirements documented (e.g., competitions require PNG frames). Evidence: `prompts/README.md` states "Name the videos in the form of `$prompt-$index.mp4`" with no preprocessing pipeline. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment tools exist. The framework evaluates generated videos (output quality), not input data quality. No label quality checks, demographic analysis, duplicate detection, or bias detection for datasets. The quality dimensions evaluate model outputs, not data inputs. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features. The "safety" dimension in `vbench2_beta_trustworthiness` uses pre-trained models (NudeNet, SD Safety Checker) to evaluate generated content, not to detect/remove PII from training data. No audit trails or privacy features for data preparation. |
| S2F4: Infrastructure Building | 1 | Minimal infrastructure support. Downloads pre-trained models to `~/.cache/vbench` but no index building, database setup, or versioning. Evidence: `pretrained/` folders contain only `download.sh` scripts and `model_path.txt` files. No FAISS/ColBERT/BM25 support. The framework assumes all infrastructure exists. |
| S2F5: Model Validation | 1 | Basic model downloading with no explicit validation. Models downloaded via ModelScope/HuggingFace but no checksum verification, version compatibility checks, or integrity validation documented. Evidence: Installation instructions just say `pip install vbench` with no validation steps. |
| S2F6: Scenario Generation | 1 | Minimal prompt variations exist. Provides static prompt lists (e.g., `prompts/all_dimension.txt` with ~900 prompts) but no dynamic generation, templating, or parameterization. Evidence: `prompts/augmented_prompts/gpt_enhanced_prompts/README.md` uses GPT-4o externally to enhance prompts, not built-in generation. Users must manually create variations. |
| S2F7: Red-Teaming | 1 | Limited adversarial testing via trustworthiness module. `vbench2_beta_trustworthiness` evaluates bias/safety of generated videos but doesn't generate adversarial prompts. Evidence: `vbench2_beta_trustworthiness/README.md` describes evaluation of existing videos for "culture_fairness", "gender_bias", "safety" - no attack generation. |
| S2F8: Contamination Detection | 0 | No contamination detection capabilities. The framework evaluates generated videos against prompts but doesn't compare datasets or check for train/test leakage. No n-gram overlap, semantic similarity, or contamination reporting features exist. |

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (1/3)

Evidence of Minimal Preprocessing:

From `prompts/README.md`:
```markdown
Name the videos in the form of `$prompt-$index.mp4`, `$index` takes value of `0, 1, 2, 3, 4`. For example:
├── A 3D model of a 1800s victorian house.-0.mp4                                       
├── A 3D model of a 1800s victorian house.-1.mp4
```

From `competitions/README.md`:
```markdown
### 3. File Structure Requirements
- PNG requirement: All submissions must be in `png` format.
- Frame name: Name the `png` frames according to the frame order, in 5 digits, zero-filled.
```

Why 1 point:
- No data loading utilities - users must generate videos themselves
- No caching mechanisms documented
- No preprocessing pipelines for video normalization
- Only naming conventions and format requirements
- No validation of video properties (resolution, FPS checks are manual)
- No splitting/partitioning tools

What's Missing:
```python
# No equivalent of:
dataset = load_dataset("vbench/prompts", cache_dir="...")
preprocessed = dataset.map(lambda x: normalize_video(x))
train, val = dataset.split(test_size=0.2, stratify_by="category")
```

### S2F2: Dataset Quality and Bias Assessment (0/3)

Evidence of Evaluation-Only Focus:

From `vbench/aesthetic_quality.py`:
```python
def compute_aesthetic_quality(self, videos_path, name):
    # Evaluates generated videos, not input datasets
    score_sum = 0
    for video_path in video_list:
        images = load_video(video_path)[0]
        aesthetic_score = self.get_aesthetic_score(images)
```

The framework evaluates:
- Generated video quality (aesthetic, imaging quality)
- Model outputs (consistency, motion smoothness)
- Not input data quality

Why 0 points:
- No label noise detection
- No demographic distribution analysis of datasets
- No duplicate detection in training data
- No bias detection in source datasets
- All "quality" features evaluate model outputs, not input data

### S2F3: PII Detection and Anonymization (0/3)

Evidence from Safety Module:

From `vbench2_beta_trustworthiness/safety.py`:
```python
def evaluate_safety(video_path):
    # Evaluates generated content for NSFW, not PII in data
    frames = extract_frames(video_path)
    nude_detector = NudeDetector()
    sd_safety_checker = StableDiffusionSafetyChecker()
    # Returns safety scores for generated content
```

Why 0 points:
- No PII detection (names, emails, SSNs, etc.)
- No anonymization/redaction capabilities
- Safety evaluation focuses on NSFW content in generated videos
- No data privacy features for preparation stage
- No audit trails for data handling

### S2F4: Task-Specific Infrastructure Building (1/3)

Evidence of Minimal Infrastructure:

From `pretrained/raft_model/download.sh`:
```bash
# RAFT optical flow
if [ ! -f raft-things.pth ]; then
    wget -c https://modelscope.cn/api/v1/models/iic/cv_raft_video-stabilization_base/repo?FilePath=raft-things.pth
fi
```

From `pretrained/README.md`:
```markdown
[Optional] Please download the pre-trained weights according to the guidance in the `model_path.txt` file for each model in the `pretrained` folder to `~/.cache/vbench`.
```

Why 1 point:
- Simple model downloading to cache directory
- No index building (FAISS, ColBERT, BM25)
- No database setup utilities
- No versioning or artifact management
- Pre-trained models assumed to exist, not built

What's Missing:
- No retrieval system setup
- No vector database integration
- No index persistence/loading
- No artifact versioning

### S2F5: Model Artifact Validation (1/3)

Evidence of Basic Downloading:

From `README.md`:
```markdown
## Installation
pip install vbench

## Pretrained Models
[Optional] Please download the pre-trained weights according to the guidance in the `model_path.txt` file
```

From `pretrained/clip_model/model_path.txt`:
```
modelscope: iic/cv_clip_openai
```

Why 1 point:
- Models downloaded via ModelScope/HuggingFace APIs
- No explicit checksum validation shown
- No version compatibility warnings
- No corruption detection
- No test inference validation

What's Missing:
```python
# No validation like:
def validate_model(model_path):
    assert check_sha256(model_path, expected_hash)
    assert check_version_compatibility(model_path, framework_version)
    assert test_inference_successful(model_path)
```

### S2F6: Evaluation Scenario Generation (1/3)

Evidence of Static Prompts:

From `prompts/all_dimension.txt`:
```
A 3D model of a 1800s victorian house.
A beautiful coastal beach in spring, waves lapping on sand by Hokusai
...
```

From `prompts/augmented_prompts/gpt_enhanced_prompts/README.md`:
```markdown
We follow CogVideoX, and use GPT-4o to enhance VBench prompts, making them longer and more descriptive without altering their original meaning.
```

Why 1 point:
- Provides 900+ static prompts across dimensions
- Prompt enhancement requires external GPT-4o API
- No built-in templating or variable substitution
- No multi-turn dialogue generation
- No edge case generators

What's Missing:
```python
# No built-in generation like:
generator = PromptGenerator(
    template="A {adjective} {object} in {location}",
    variables={"adjective": [...], "object": [...]}
)
prompts = generator.generate_variations(num_samples=1000)
```

### S2F7: Red-Teaming and Adversarial Test Generation (1/3)

Evidence from Trustworthiness Module:

From `vbench2_beta_trustworthiness/README.md`:
```markdown
### Safety
- This dimension evaluates whether the generated videos contain unsafe content.
- Implemented based on an ensemble of NudeNet, SD Safety Checker and Q16 Classifier
```

From `vbench2_beta_trustworthiness/gender_bias.py`:
```python
def evaluate_gender_bias(videos, prompts):
    # Evaluates existing videos for bias, doesn't generate adversarial prompts
    for video in videos:
        gender_detected = detect_gender(video)
        bias_score = compute_bias(gender_detected, prompt)
```

Why 1 point:
- Evaluates bias in generated content
- Uses pre-defined prompt lists for bias testing
- No adversarial prompt generation
- No jailbreak attempt library
- No automated attack generation

What's Missing:
- No red-team prompt generator
- No escalating severity levels
- No attack taxonomy
- Manual prompt engineering required

### S2F8: Data Contamination Detection (0/3)

Evidence of Absence:

Searching through the repository:
- No `contamination` files
- No `n-gram` overlap utilities
- No train/test comparison tools
- No fingerprinting methods

The evaluation compares generated videos to prompts, not training data to evaluation data.

From `evaluate.py`:
```python
def evaluate(videos_path, dimension_list):
    # Evaluates videos against prompts, not contamination
    for dimension in dimension_list:
        results = dimension_func(videos_path)
```

Why 0 points:
- No contamination detection features
- No dataset comparison tools
- No overlap detection
- Framework design doesn't address this problem

## Key Observations

### Framework Design Philosophy

VBench is fundamentally an evaluation harness, not a data preparation framework. From the documentation:

```markdown
# From README.md
VBench is a comprehensive benchmark suite for video generative models. You can use VBench to evaluate video generation models from 16 different ability aspects.
```

The workflow assumes:
1. User already has a trained video generation model
2. User generates videos using their model
3. User evaluates those videos with VBench

### Missing Preparation Infrastructure

The repository lacks:
- Data loading/preprocessing utilities
- Dataset quality tools
- PII/privacy features
- Infrastructure building (indexes, databases)
- Scenario/prompt generation
- Contamination detection

### What VBench Does Well (Not in Stage 2)

VBench excels at:
- Stage 4 (EXECUTE): Running evaluations on generated videos
- Stage 5 (ANALYZE): Computing metrics across multiple dimensions
- Pre-defining comprehensive prompt suites
- Providing evaluation scripts

### Conclusion

VBench scores 5/24 (21%) in Stage 2 (PREPARE) because it's designed for post-generation evaluation, not data preparation. Users must handle all preparation externally:

1. Generate videos themselves
2. Name files correctly
3. Download models manually
4. Create prompts manually
5. Handle any data quality/privacy concerns outside VBench

This is not a criticism - it's by design. VBench focuses on standardized evaluation, assuming preparation is complete.