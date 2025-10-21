# LLMPerf (ray-project__llmperf) - Stage 1 (CONFIGURE) Evaluation

## Summary
LLMPerf is a performance testing tool for LLM APIs that focuses on benchmarking rather than comprehensive evaluation. It has minimal configuration capabilities, primarily using CLI arguments for setup. The tool is designed for load testing and correctness testing of various LLM APIs (OpenAI, Anthropic, LiteLLM, etc.) but lacks the logical configuration abstractions expected in a full evaluation framework.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 0 | No dataset abstraction exists. The tool generates synthetic prompts programmatically using `randomly_sample_sonnet_lines_prompt()` from a hardcoded sonnet.txt file (src/llmperf/utils.py). There is no concept of dataset registration, schema definition, or versioning. Evidence: The `llm_correctness.py` generates random number conversion prompts on-the-fly, and `token_benchmark_ray.py` samples from Shakespeare sonnets - no dataset configuration layer exists. |
| S1F2: Model Configuration | 1 | Minimal model configuration via environment variables only. Models are specified via CLI `--model` argument, but backend configuration requires manual environment variable setup (e.g., `OPENAI_API_KEY`, `OPENAI_API_BASE`). Evidence from README.md shows multiple provider examples all requiring manual env var setup. The `construct_clients()` function in `common.py` supports multiple APIs (OpenAI, Anthropic, LiteLLM, SageMaker, VertexAI) but with no declarative configuration file - everything is hardcoded or passed via CLI. No validation, no config files, no unified auth management. |
| S1F3: Prompt Configuration | 1 | Basic string formatting only, no templating system. Prompts are constructed programmatically in Python code. For correctness tests: `prompt = f"Convert the following sequence of words into a number: {rnd_num_words}.\nPrint the number first."` (llm_correctness.py:60). For token benchmarks, prompts are generated via `randomly_sample_sonnet_lines_prompt()` which samples Shakespeare lines. No template versioning, no variable substitution system, no few-shot support. The `additional_sampling_params` CLI argument allows JSON params but no structured prompt management. |
| S1F4: Environment Setup | 2 | Basic dependency management with manual setup. Evidence: `pyproject.toml` defines dependencies (ray, transformers, litellm, etc.) with loose version constraints. `requirements-dev.txt` exists but only contains linting tools. Installation via `pip install -e .` is documented. However, no containerization (no Dockerfile found), no automated setup scripts, no environment validation. The README shows extensive manual setup requirements for different providers (gcloud auth, AWS credentials, etc.). No pinned versions = potential reproducibility issues. |
| S1F5: Security & Access | 1 | Environment variables only, no advanced security. All authentication uses plain environment variables (e.g., `OPENAI_API_KEY`, `AWS_ACCESS_KEY_ID`). Evidence from `openai_chat_completions_client.py:32-36`: simple `os.environ.get()` calls with no encryption, rotation, or vault integration. No RBAC, no audit logging, no enterprise integration features. Ray initialization does copy env vars (`ray.init(runtime_env={"env_vars": env_vars})` in token_benchmark_ray.py:296) but this is basic environment passing, not security management. |
| S1F6: Cost Estimation | 0 | No cost estimation capabilities. The codebase focuses purely on performance metrics (throughput, latency, TTFT) with no cost modeling. Token counting exists (`LlamaTokenizerFast` for approximation) but is used only for metrics reporting, not cost estimation. No pricing data, no budget tools, no cost projection features found in any files. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (Rating: 0)

Evidence of absence:
- No dataset abstraction layer: The tool generates test data procedurally rather than loading/configuring datasets
- Correctness test (llm_correctness.py:58-62):
  ```python
  rnd_number = random.randint(0, MAX_RANDOM_NUMBER)
  rnd_num_words = num2words.num2words(rnd_number)
  prompt = f"Convert the following sequence of words into a number: {rnd_num_words}.\nPrint the number first."
  ```
  This shows runtime generation, not dataset configuration.

- Token benchmark (token_benchmark_ray.py:51-59):
  ```python
  prompts.append(randomly_sample_sonnet_lines_prompt(
      prompt_tokens_mean=mean_input_tokens,
      prompt_tokens_stddev=stddev_input_tokens,
      expect_output_tokens=num_output_tokens,
      tokenizer=tokenizer
  ))
  ```
  Prompts are sampled from a hardcoded `sonnet.txt` file with no configuration layer.

What's missing:
- No dataset registration API
- No support for external data sources (JSON, CSV, HuggingFace, etc.)
- No schema definition
- No versioning
- No split strategies

### S1F2: Model and Backend Configuration (Rating: 1)

What exists:
- Multiple provider support via `llm_api` parameter (src/llmperf/common.py:8):
  ```python
  SUPPORTED_APIS = ["openai", "anthropic", "litellm"]
  ```
- Basic client construction (src/llmperf/common.py:11-31):
  ```python
  def construct_clients(llm_api: str, num_clients: int) -> List[LLMClient]:
      if llm_api == "openai":
          clients = [OpenAIChatCompletionsClient.remote() for _ in range(num_clients)]
      elif llm_api == "sagemaker":
          clients = [SageMakerClient.remote() for _ in range(num_clients)]
      # ... etc
  ```

Critical limitations:
- No configuration files: All settings via CLI arguments
- Manual environment setup required (README.md:44-48):
  ```bash
  export OPENAI_API_KEY=secret_abcdefg
  export OPENAI_API_BASE="https://api.endpoints.anyscale.com/v1"
  ```
- No validation: Environment variables checked at runtime with basic ValueError (openai_chat_completions_client.py:32-36):
  ```python
  address = os.environ.get("OPENAI_API_BASE")
  if not address:
      raise ValueError("the environment variable OPENAI_API_BASE must be set.")
  ```
- No unified auth management: Each client handles its own auth differently
- No resource allocation: Concurrent requests specified via CLI `--num-concurrent-requests` but no GPU/CPU specification

### S1F3: Prompt Configuration (Rating: 1)

What exists:
- Basic sampling parameter passing via CLI (token_benchmark_ray.py:196-201):
  ```python
  args.add_argument(
      "--additional-sampling-params",
      type=str,
      default="{}",
      help="Additional sampling params to send with the each request"
  )
  ```
- Runtime prompt construction with f-strings

What's missing:
- No template engine: Prompts are hardcoded Python strings, not Jinja2/similar
- No variable substitution system: Direct string formatting only
- No few-shot support: No mechanism to inject examples
- No versioning: No way to track/manage prompt versions
- No template inheritance: Each test hardcodes its own prompts

The `RequestConfig` model (src/llmperf/models.py:6-18) is basic:
```python
class RequestConfig(BaseModel):
    model: str
    prompt: Tuple[str, int]  # Just (text, token_count)
    sampling_params: Optional[Dict[str, Any]] = None
    llm_api: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```
No prompt templating infrastructure.

### S1F4: Environment Setup (Rating: 2)

What exists:
- Dependency specification (pyproject.toml:13-24):
  ```toml
  dependencies = ["pydantic<2.5",
                  "ray", 
                  "pytest>=6.0", 
                  "seaborn>=0.11", 
                  # ... etc
  ```
- Basic installation (README.md:4-8):
  ```bash
  git clone https://github.com/ray-project/llmperf.git
  cd llmperf
  pip install -e .
  ```

Limitations:
- No version pinning: Dependencies use loose constraints (e.g., `"ray"` with no version)
- No containerization: No Dockerfile, no container support mentioned
- Manual setup required: Extensive provider-specific setup (README.md shows gcloud auth, AWS config, etc.)
- No automated validation: No setup script to verify environment correctness
- No hardware specs: No GPU/CUDA configuration despite being an LLM tool

### S1F5: Security and Access Control (Rating: 1)

What exists:
- Basic environment variable usage for credentials

Evidence of minimal security:
- OpenAI client (openai_chat_completions_client.py:32-38):
  ```python
  address = os.environ.get("OPENAI_API_BASE")
  if not address:
      raise ValueError("the environment variable OPENAI_API_BASE must be set.")
  key = os.environ.get("OPENAI_API_KEY")
  if not key:
      raise ValueError("the environment variable OPENAI_API_KEY must be set.")
  ```
- SageMaker client (sagemaker_client.py:23-29):
  ```python
  if not os.environ.get("AWS_ACCESS_KEY_ID"):
      raise ValueError("AWS_ACCESS_KEY_ID must be set.")
  if not os.environ.get("AWS_SECRET_ACCESS_KEY"):
      raise ValueError("AWS_SECRET_ACCESS_KEY must be set.")
  ```

What's missing:
- No credential encryption
- No rotation support
- No vault integration (HashiCorp Vault, AWS Secrets Manager, etc.)
- No RBAC
- No audit logging
- No SSO/enterprise auth
- No compliance certifications mentioned

### S1F6: Cost Estimation (Rating: 0)

Evidence of absence:
- Metrics focus exclusively on performance (src/llmperf/common_metrics.py):
  ```python
  INTER_TOKEN_LAT = "inter_token_latency_s"
  TTFT = "ttft_s"
  E2E_LAT = "end_to_end_latency_s"
  REQ_OUTPUT_THROUGHPUT = "request_output_throughput_token_per_s"
  # No cost-related metrics
  ```
- Token counting exists but only for throughput calculation, not cost estimation
- No pricing data, no budget features, no cost modeling anywhere in codebase

Conclusion:
LLMPerf is a specialized performance benchmarking tool, not a general-purpose evaluation framework. It lacks most Stage 1 configuration features expected in a comprehensive evaluation system. Its strength is in performance testing specific LLM APIs with minimal setup, but it requires significant manual configuration and provides no abstractions for datasets, prompts, security, or cost management.

Total Stage 1 Score: 5/18 (28%)

The tool would need substantial development to support logical configuration of evaluation components. Current design assumes users will write Python code directly rather than configure evaluations declaratively.