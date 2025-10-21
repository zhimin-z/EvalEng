# VBench/VBench-2.0 - Stage 1 (CONFIGURE) Evaluation

## Summary
VBench/VBench-2.0 is a comprehensive video generation evaluation benchmark framework that primarily focuses on automated evaluation of generated videos against predefined prompts and dimensions. The repository is NOT designed as a configurable evaluation harness for users to set up custom evaluations. Instead, it's a research artifact that provides standardized evaluation protocols with fixed prompt suites and metrics. Configuration capabilities are minimal and tightly coupled to the research methodology.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited dataset configuration; primarily uses fixed prompt lists from text files with no schema definition or versioning system |
| S1F2: Model Configuration | 0 | No model backend configuration - evaluates already-generated videos; no provider abstraction or resource allocation |
| S1F3: Prompt Configuration | 1 | Fixed prompt suites in text files; no templating system, versioning, or parameter sweeps; prompts are research artifacts, not configurable |
| S1F4: Environment Setup | 2 | Provides conda environment.yml and requirements.txt with pinned versions; manual setup required; no containerization provided |
| S1F5: Security & Access | 0 | No credential management, access control, audit logging, or enterprise integration features |
| S1F6: Cost Estimation | 0 | No cost modeling, resource projection, or budget tools - framework evaluates pre-generated videos |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (Rating: 1)

Evidence of Limited Capability:

The framework uses simple text-based prompt lists without sophisticated dataset abstraction:

```python
# From README.md - Sampling instructions
with open(f'./prompts/prompts_per_dimension/{dimension}.txt', 'r') as f:
    prompt_list = f.readlines()
prompt_list = [prompt.strip() for prompt in prompt_list]
```

Dataset Sources:
- Only supports local video files via `--videos_path`
- No built-in connectors for HuggingFace, databases, APIs, or cloud storage
- From `evaluate.py` usage:
```bash
vbench evaluate --videos_path $VIDEO_PATH --dimension $DIMENSION
```

Schema Definition:
- No schema API exists
- Video requirements documented in plain text (README.md):
```markdown
| Video Type | Prompt Count |Resolution | Duration | Frame Rate | Frame Count |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Short Videos |  200 | No Limit | 1.6-4.0s | 8-24 FPS | 16-96 |
```
- No programmatic validation of these constraints

Split Strategies:
- No declarative split configuration
- Fixed train/test splits hardcoded in JSONL files:
```python
# From VBench-2.0/vbench2/third_party/ViTDetector/readme.md
"face_train.jsonl"    # Face training set annotations
"face_test.jsonl"     # Face testing set annotations
```

Versioning:
- No dataset versioning system
- Prompt files have no version metadata
- From `prompts/README.md`:
```markdown
## Prompts per Dimension
`prompts/prompts_per_dimension`: For each VBench evaluation dimension, we carefully designed a set of around 100 prompts as the test cases.
```

Why not 0 points: The framework does provide a minimal abstraction via `VBench_full_info.json` that maps dimensions to prompt files, but this is barely above direct file handling.

---

### S1F2: Model and Backend Configuration (Rating: 0)

Critical Finding: VBench evaluates already-generated videos, not models directly. There is no model configuration system.

Evidence:

From the core usage pattern in README.md:
```python
# Users provide pre-generated videos
my_VBench.evaluate(
    videos_path = "sampled_videos/lavie/human_action",  # Pre-generated videos
    name = "lavie_human_action",
    dimension_list = ["human_action"],
)
```

From `prompts/README.md`:
```markdown
# How to Sample Videos for Evaluation
## Sample Some Dimensions
for prompt in prompt_list:
    # sample 5 videos for each prompt
    for index in range(5):
        # perform sampling with YOUR model
        video = sample_func(prompt, index)    
        cur_save_path = f'{args.save_path}/{prompt}-{index}.mp4'
```

Why 0 points:
- No provider abstraction (OpenAI, Anthropic, etc.)
- No model configuration API
- No authentication mechanisms for models
- Users must generate videos externally using their own pipelines
- The framework only evaluates the *outputs* of generation models

Note: There are references to inference backends in subdirectories (ms-swift), but these are third-party dependencies for internal metrics, not user-configurable model backends.

---

### S1F3: Evaluation Parameters and Prompt Configuration (Rating: 1)

Prompt System:

Prompts are static text files, not configurable templates:

From `prompts/prompts_per_dimension/human_action.txt`:
```text
A person is playing a piano
A person is playing a cello
A person is playing a flute
```

No templating engine exists. The code simply reads lines:
```python
# From README.md sampling code
with open(f'./prompts/prompts_per_dimension/{dimension}.txt', 'r') as f:
    prompt_list = f.readlines()
```

Prompt "Enhancement":

There is limited prompt augmentation in `prompts/augmented_prompts/gpt_enhanced_prompts/README.md`:
```bash
# Using GPT-4o to enhance prompts (NOT a built-in template system)
API_KEY="your-openai-api-key"
sh convert_vbench_prompt.sh
```

This is a one-time preprocessing step using external API, not a runtime templating system.

Parameter Configuration:

From `competitions/README.md`:
```markdown
### 2. Video Requirement
| Video Type | Frame Rate | 
| :---: | :---: |
| Short Videos | 8-24 FPS |
```

These are documentation requirements, not configurable parameters. No API exists to set temperature, top_p, etc.

Metric Configuration:

Dimensions are fixed and hardcoded. From `VBench-2.0/vbench2/VBench2_full_info.json`:
```json
{
    "Human_Anatomy": {
        "prompt_file": "prompts/meta_info/Human_Anatomy_info.json",
        "func": "check_human_anatomy",
        "dimension_type": "human_centric"
    }
}
```

Users cannot define custom metrics programmatically - they would need to fork the codebase.

Why 1 point: Basic string-based prompts exist with minimal post-hoc augmentation capability, but no real templating, parameter sweeps, or metric configuration.

---

### S1F4: Environment Setup and Dependency Management (Rating: 2)

Dependency Specification:

Multiple dependency files provided:

From `VBench-2.0/requirement.txt`:
```text
torch>=2.0
torchvision
opencv-python
pandas
pyiqa
[... extensive list ...]
```

From `VBench-2.0/environment.yml`:
```yaml
name: vbench2
channels:
  - defaults
dependencies:
  - python=3.10
  - pip:
    - torch==2.5.1
    - torchvision==0.20.1
```

Pinned Versions: Partially pinned (e.g., `torch==2.5.1`) but many dependencies use ranges (`>=2.0`).

Containerization:

No Docker support found. From search through repository:
- No `Dockerfile` in root or subdirectories
- No container-related documentation
- From README.md installation:
```bash
conda create -n vbench2 python=3.10 -y
conda activate vbench2
pip install -r requirement.txt
```

Environment Automation:

Manual setup required:
```bash
# From VBench-2.0/README.md
conda create -n vbench2 python=3.10 -y
conda activate vbench2
conda install psutil
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu118
python -m pip install ninja
python -m pip install git+https://github.com/Dao-AILab/flash-attention.git
pip install -r requirement.txt
pip install retinaface_pytorch==0.0.8 --no-deps
```

No `make setup` or automated scripts - users must run multiple commands.

Hardware Configuration:

Documentation acknowledges hardware needs:
```markdown
# From README.md
- cuda: cuda12 (No need to install if using CPU, NPU, MPS)
- torch: >=2.0
```

But no programmatic hardware specification or compatibility checks on startup.

Why 2 points: Dependencies are documented with partial version pinning, but setup is manual, no containerization exists, and hardware specs are informal documentation.

---

### S1F5: Security and Access Control (Rating: 0)

Credential Management:

No built-in credential management. The only security-related code is in third-party subdirectories for external APIs:

From `prompts/augmented_prompts/gpt_enhanced_prompts/convert_vbench_prompt.sh`:
```bash
API_KEY="your-openai-api-key"  # User-provided plaintext
HTTP_PROXY="http://your-proxy-server:port/"
```

This is for optional prompt enhancement, not framework configuration.

Access Control:

No RBAC, user/group systems, or access restrictions. From core evaluation code structure:
```python
# Anyone with file access can run evaluation
from vbench2 import VBench2
my_VBench = VBench2(device, "vbench2/VBench2_full_info.json", "evaluation_results")
my_VBench.evaluate(videos_path="...", dimension_list=["..."])
```

No authentication or authorization layers.

Audit Logging:

No audit logging system. Standard Python logging exists for debugging but no tamper-proof or compliance-focused logging.

Enterprise Integration:

No SSO, LDAP, or enterprise authentication support documented or implemented.

Why 0 points: Completely absent security features. This is a research evaluation tool, not an enterprise system.

---

### S1F6: Cost Estimation and Budget Planning (Rating: 0)

Cost Modeling:

No cost estimation exists because VBench evaluates pre-generated videos, not API calls.

Evidence:

From the workflow in `README-FAQ.md`:
```markdown
Q: For option 2️⃣ - how should I organize the sampled videos for submission?
A: You can place all sampled videos in a single folder.
```

Users generate videos externally using their own resources/APIs, then submit videos for evaluation.

Resource Projection:

No token counting or API call projection - the framework processes video files:

From `vbench2/utils.py` (example metric):
```python
def calculate_metric(video_path):
    video = load_video(video_path)
    # Process frames, no API calls
    return metric_score
```

Budget Tools:

No budget limits, cost breakdowns, or optimization suggestions. The framework is free to run once videos are generated (only compute costs for metric computation).

Why 0 points: Cost estimation is irrelevant to the framework's design - it evaluates artifacts, not generates them.

---

## Key Findings

### Strengths
1. Clear Documentation: Extensive README files explaining the research methodology
2. Dependency Transparency: Requirements files provided with version information
3. Reproducibility: Fixed prompt suites enable reproducible research comparisons

### Critical Limitations
1. Not a Configuration Framework: VBench is a standardized evaluation protocol, not a flexible evaluation harness
2. Fixed Evaluation Dimensions: Users cannot easily add custom metrics without code modification
3. Pre-Generated Video Requirement: No model integration - users must generate videos externally
4. No Security/Enterprise Features: Designed for academic research, not production deployment
5. Minimal Abstraction: Direct file I/O, no provider/backend abstractions

### Use Case Mismatch
The evaluation guidelines assume a framework where users configure:
- Different model providers (OpenAI, Anthropic, etc.)
- Custom prompts with templating
- Budget limits and cost estimation

VBench is fundamentally different: It's a research benchmark where:
- Researchers generate videos using their own models/APIs
- Videos are evaluated against fixed prompt suites
- Metrics are predefined research contributions
- Results are submitted to a leaderboard for comparison

### Evidence of Research Artifact Nature

From `README-FAQ.md`:
```markdown
Q: How can I join VBench Leaderboard?
Option | Sampling Party | Evaluation Party |
| 1️⃣ | VBench Team | VBench Team | (Ideal for closed-source models with API access)
| 2️⃣ | Your Team | VBench Team | Submit video samples via Google Form
| 3️⃣ | Your Team | Your Team | Submit eval_results.zip to leaderboard
```

This is a benchmark leaderboard submission system, not a configurable evaluation framework.

---

## Recommendations

If VBench were to be adapted as a configurable evaluation harness, it would need:

1. S1F1 Improvements: 
   - Add dataset connectors (HuggingFace, S3, etc.)
   - Implement schema validation API
   - Create versioned prompt management system

2. S1F2 Additions:
   - Integrate model backends (vLLM, LMDeploy already referenced but not user-configurable)
   - Add provider abstraction layer
   - Implement resource allocation configs

3. S1F3 Enhancements:
   - Create Jinja2-based template system
   - Enable runtime parameter configuration
   - Allow custom metric definitions via plugins

4. S1F4 Improvements:
   - Provide official Docker images
   - Create `make setup` automation
   - Add hardware compatibility checks

5. S1F5 & S1F6: 
   - Add these only if targeting enterprise/production use cases

---

## Final Assessment

Total Configuration Score: 4/18 (22%)

VBench/VBench-2.0 is a valuable research contribution providing standardized video generation evaluation, but it is NOT designed as a configurable evaluation framework. The low score reflects this fundamental design choice, not poor implementation. For its intended purpose (academic benchmarking with fixed protocols), it succeeds. For configurable evaluation workflows, it would require substantial architectural changes.