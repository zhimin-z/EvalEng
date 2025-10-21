# Speech-to-Text Benchmark - Stage 1 (CONFIGURE) Evaluation

## Summary
The speech-to-text-benchmark framework is a minimalist benchmarking tool focused on comparing STT engines. It has hardcoded dataset and model configurations with minimal abstraction layers. Configuration is primarily done through CLI arguments rather than declarative files, with no versioning, schema definition, or cost estimation capabilities. The framework is highly specialized for its specific use case but lacks general-purpose evaluation configuration features.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited dataset support hardcoded in enum, no schema definition, manual file handling |
| S1F2: Model Configuration | 1 | Engine selection via CLI enum only, hardcoded credentials, no resource allocation |
| S1F3: Prompt Configuration | 0 | Not applicable - STT benchmark with no prompt/template system |
| S1F4: Environment Setup | 2 | Basic requirements.txt provided, manual dependency setup, no containerization |
| S1F5: Security & Access | 1 | Environment variables only for credentials, no RBAC or audit logging |
| S1F6: Cost Estimation | 0 | No cost estimation or budgeting features |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (Rating: 1/3)

Evidence:

The framework has a hardcoded enum of supported datasets in `dataset.py`:
```python
class Datasets(Enum):
    COMMON_VOICE = "COMMON_VOICE"
    FLEURS = "FLEURS"
    LIBRI_SPEECH_TEST_CLEAN = "LIBRI_SPEECH_TEST_CLEAN"
    LIBRI_SPEECH_TEST_OTHER = "LIBRI_SPEECH_TEST_OTHER"
    MLS = "MLS"
    TED_LIUM = "TED_LIUM"
    VOX_POPULI = "VOX_POPULI"
```

Limitations:
1. No Schema Definition: Datasets are accessed directly through file paths with no schema API. Each dataset class hardcodes how to parse its specific format:
```python
# dataset.py, CommonVoiceDataset
with open(os.path.join(folder, "test.tsv")) as f:
    reader: csv.DictReader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        if int(row["up_votes"]) > 0 and int(row["down_votes"]) == 0:
            # ... hardcoded logic
```

2. No Split Strategies: No declarative split configuration - datasets use fixed pre-defined splits (e.g., "test.tsv", "test-clean", "test-other")

3. No Versioning: No dataset versioning system. Results are cached based on file extensions (`.aws`, `.ggl`, etc.) but no version tracking:
```python
# engine.py
cache_path = path.replace(".flac", ".aws")
if os.path.exists(cache_path):
    with open(cache_path) as f:
        res = f.read()
```

4. Limited Sources: Only supports 7 predefined audio datasets, all requiring manual download and local file paths

Rating Justification: The framework has 7 hardcoded dataset sources but no abstraction layer. Adding a new dataset requires forking and modifying the Dataset enum and creating a new class. No schema API, versioning, or flexible split strategies exist - earning it a 1-point rating.

---

### S1F2: Model and Backend Configuration (Rating: 1/3)

Evidence:

Engine/model selection is done through a hardcoded enum in `engine.py`:
```python
class Engines(Enum):
    AMAZON_TRANSCRIBE = "AMAZON_TRANSCRIBE"
    AMAZON_TRANSCRIBE_STREAMING = "AMAZON_TRANSCRIBE_STREAMING"
    AZURE_SPEECH_TO_TEXT = "AZURE_SPEECH_TO_TEXT"
    # ... 15 total engines
    PICOVOICE_LEOPARD = "PICOVOICE_LEOPARD"
```

Configuration Method:
All configuration is done via CLI arguments in `benchmark.py`:
```python
parser.add_argument("--engine", required=True, choices=[x.value for x in Engines])
parser.add_argument("--aws-profile")
parser.add_argument("--aws-location")
parser.add_argument("--azure-speech-key")
parser.add_argument("--azure-speech-location")
parser.add_argument("--google-application-credentials")
```

Limitations:

1. No Config Files: No YAML/JSON configuration system - all parameters must be passed as CLI arguments

2. Hardcoded Authentication: Credentials are passed via CLI or environment variables only:
```python
# benchmark.py
if engine_name in [Engines.AMAZON_TRANSCRIBE, Engines.AMAZON_TRANSCRIBE_STREAMING]:
    if args.aws_profile is None or args.aws_location is None:
        raise ValueError("`aws-profile` and `aws-location` is required")
    os.environ["AWS_PROFILE"] = args.aws_profile
```

3. No Resource Allocation: Fixed threading config hardcoded in `engine.py`:
```python
NUM_THREADS = 1
os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
os.environ["MKL_NUM_THREADS"] = str(NUM_THREADS)
torch.set_num_threads(NUM_THREADS)
```

4. No Runtime Override: Once an engine is initialized, parameters cannot be changed without rerunning the entire benchmark

Provider Support: 
- Supports 7+ providers (Amazon, Azure, Google, IBM Watson, OpenAI Whisper, Picovoice)
- But each requires manual credential setup with different CLI arguments

Rating Justification: Multiple providers supported (7+) but configuration is entirely through CLI arguments with no file-based config system, no resource allocation API, and hardcoded credential handling. This barely meets the threshold for functionality, earning a 1-point rating.

---

### S1F3: Prompt Configuration (Rating: 0/3)

Evidence:

This framework is for speech-to-text benchmarking, not LLM evaluation. There is no concept of prompts, templates, or parameter configuration for generation.

The only "configuration" is normalizer settings for text processing:
```python
# normalizer.py
class Normalizer(object):
    def __init__(self, keep_punctuation: bool, punctuation_set: str = SUPPORTED_PUNCTUATION_SET) -> None:
        self._keep_punctuation = keep_punctuation
        self._punctuation_set = punctuation_set
```

Rating Justification: Not applicable to this STT benchmark framework - no prompt system exists. Rating 0 as this feature is completely absent.

---

### S1F4: Environment Setup and Dependency Management (Rating: 2/3)

Evidence:

Dependency Specification:
The framework provides a `requirements.txt`:
```txt
amazon-transcribe==0.6.4
azure-cognitiveservices-speech
boto3
editdistance
google-cloud-speech==2.23.0
huggingface-hub
ibm_watson
inflect
matplotlib
numpy
openai-whisper
psutil
pvcheetah==2.3.0
pvleopard==2.0.1
pytube
requests
soundfile
```

Pros:
1. Dependencies are pinned to specific versions (good practice)
2. Clear installation instructions in README:
```console
pip3 install -r requirements.txt
```

3. External dependency documented:
```markdown
- Install [FFmpeg](https://www.ffmpeg.org/)
```

Limitations:

1. No Containerization: No Dockerfile or container support provided

2. Manual Setup Required: FFmpeg must be manually installed, no automated setup script

3. No Environment Automation: No `setup.py`, `Makefile`, or automated virtual environment creation

4. Platform Specific: README states "This benchmark has been developed and tested on `Ubuntu 22.04`" - no cross-platform testing or documentation

5. No Hardware Configuration: No GPU/CPU specification system. Threading is hardcoded:
```python
# engine.py
NUM_THREADS = 1
os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
```

Rating Justification: Has a requirements.txt with pinned dependencies and basic setup instructions, but lacks containerization, automated setup, and hardware configuration. Manual steps required for FFmpeg and platform-specific warnings indicate this is a 2-point implementation.

---

### S1F5: Security and Access Control (Rating: 1/3)

Evidence:

Credential Management:
The framework only supports environment variables and CLI arguments:

```python
# benchmark.py
elif engine_name in [Engines.GOOGLE_SPEECH_TO_TEXT, ...]:
    if args.google_application_credentials is None:
        raise ValueError("`google-application-credentials` is required")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.google_application_credentials
```

Usage example from README:
```console
python3 benchmark.py \
--engine GOOGLE_SPEECH_TO_TEXT \
--google-application-credentials ${GOOGLE_APPLICATION_CREDENTIALS}
```

Limitations:

1. No Secret Management: No support for HashiCorp Vault, AWS Secrets Manager, or any secure credential storage

2. No Access Control: No RBAC, user management, or permission system whatsoever

3. No Audit Logging: No logging of credential access or sensitive operations

4. Credentials in CLI: Passing credentials via command-line arguments can expose them in process lists and shell history

5. No Encryption: Cached results are stored in plaintext:
```python
# engine.py
with open(cache_path, "w") as f:
    f.write(res)  # No encryption
```

6. No Enterprise Integration: No SSO, LDAP, or compliance features

Rating Justification: Only supports basic environment variable credential passing with no security features, access control, or audit logging. This is the bare minimum for credential handling, earning a 1-point rating.

---

### S1F6: Cost Estimation and Budget Planning (Rating: 0/3)

Evidence:

The framework has no cost estimation capabilities whatsoever. There is performance tracking via RTF (Real-Time Factor):

```python
# benchmark.py
rtf = sum(x.process_sec for x in results) / sum(x.audio_sec for x in results)
f.write(f"RTF: {str(rtf)}\n")
```

But this only measures computational efficiency, not monetary cost.

What's Missing:

1. No Cost Modeling: No API pricing data or cost calculation for cloud STT services
2. No Token/Request Counting: No pre-execution estimation of API calls needed
3. No Budget Tools: No budget limits or cost tracking
4. No Optimization Suggestions: No cost-aware recommendations

The results are purely accuracy-focused (WER, PER) and performance-focused (RTF, latency), with no financial considerations.

Rating Justification: Complete absence of cost estimation or budgeting features. This is a pure accuracy/performance benchmark with no financial tracking, earning 0 points.

---

## Summary Table

| Feature | Score | Key Gap |
|---------|-------|---------|
| Dataset Discovery | 1 | No schema API, versioning, or flexible split strategies |
| Model Configuration | 1 | CLI-only config, no declarative files or resource allocation |
| Prompt Configuration | 0 | Not applicable (STT benchmark, not LLM) |
| Environment Setup | 2 | No containerization or automated setup |
| Security & Access | 1 | Environment variables only, no RBAC or audit logging |
| Cost Estimation | 0 | No cost tracking or budgeting features |

Overall Stage 1 Score: 5/18 (27.8%)

## Key Observations

1. Highly Specialized: This is a purpose-built STT benchmarking tool, not a general evaluation framework
2. Minimal Abstraction: Most configuration is hardcoded in enums and classes
3. CLI-Driven: All configuration via command-line arguments, no declarative config files
4. Research Tool: Designed for comparative benchmarking research, not production evaluation pipelines
5. Missing Enterprise Features: No security, versioning, cost tracking, or advanced configuration management

The framework excels at what it was designed for (comparing STT engines) but lacks the configuration flexibility and features expected of a general-purpose evaluation framework.