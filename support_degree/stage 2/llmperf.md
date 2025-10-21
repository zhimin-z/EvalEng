# LLMPerf - Stage 2 (PREPARE) Evaluation

## Summary
LLMPerf is a performance testing tool for LLM APIs, focused primarily on load testing and correctness verification. It has minimal data preparation capabilities, as it's designed for API testing rather than comprehensive evaluation. The tool generates synthetic prompts on-the-fly but lacks most Stage 2 preparation features like dataset management, quality assessment, PII detection, or infrastructure building.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Minimal preprocessing exists - only dynamic prompt generation from a single text file (sonnet.txt) with token-based sampling. No caching, no dataset loading/splitting, no multi-modal support. Code in `token_benchmark_ray.py` lines 48-74 shows prompts are generated fresh each time from Shakespeare sonnets with token counting via Llama tokenizer. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment capabilities. The tool only validates correctness of individual model responses against expected numerical outputs in `llm_correctness.py` lines 87-100, not dataset quality itself. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features present in the codebase. The tool works with pre-defined prompts (Shakespeare sonnets) that don't contain PII. |
| S2F4: Infrastructure Building | 0 | No infrastructure building capabilities. The tool assumes LLM APIs are already deployed and accessible. Ray is used for parallelization (`requests_launcher.py`) but not for building evaluation infrastructure like retrieval systems or databases. |
| S2F5: Model Validation | 0 | No model artifact validation. The tool only validates API availability by making requests. Environment variable checks exist (e.g., `vertexai_client.py` lines 33-47) but no checksum validation, version compatibility checks, or model integrity verification. |
| S2F6: Scenario Generation | 1 | Basic prompt variation exists through random sampling. `utils.py` lines 36-88 show `randomly_sample_sonnet_lines_prompt()` generates prompts with specified token lengths by randomly sampling Shakespeare lines. However, no multi-turn dialogues, edge cases, or systematic scenario generation. Seeds are set (`token_benchmark_ray.py` line 58) for reproducibility. |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial testing capabilities. The `llm_correctness.py` script tests basic arithmetic understanding but doesn't include jailbreak attempts, prompt injection, bias probing, or safety boundary testing. |
| S2F8: Contamination Detection | 0 | No contamination detection features. The tool doesn't compare evaluation data against training corpora or detect overlaps. |

## Detailed Analysis

### S2F1: Data Preprocessing and Physical Partitioning (Rating: 1)

Evidence:
The tool has minimal preprocessing limited to prompt generation:

```python
# token_benchmark_ray.py lines 48-74
def get_token_throughput_latencies(
    model: str,
    mean_input_tokens: int,
    stddev_input_tokens: int,
    # ... other params
):
    random.seed(11111)
    
    tokenizer = LlamaTokenizerFast.from_pretrained(
        "hf-internal-testing/llama-tokenizer"
    )
    get_token_length = lambda text: len(tokenizer.encode(text))
    
    # make up prompts outside of send loop for faster benchmarking loop
    num_output_tokens_list = []
    prompts = []
    for i in range(max_num_completed_requests):
        num_output_tokens = (sample_random_positive_int(
            mean_output_tokens, stddev_output_tokens
        ))
        num_output_tokens_list.append(num_output_tokens)
        
        prompts.append(randomly_sample_sonnet_lines_prompt(
            prompt_tokens_mean=mean_input_tokens,
            prompt_tokens_stddev=stddev_input_tokens,
            expect_output_tokens=num_output_tokens,
            tokenizer=tokenizer
        ))
```

The prompt generation function in `utils.py`:

```python
# utils.py lines 36-88
def randomly_sample_sonnet_lines_prompt(
    prompt_tokens_mean: int = 550,
    prompt_tokens_stddev: int = 250,
    expect_output_tokens: int = 150,
    tokenizer = LlamaTokenizerFast.from_pretrained(
        "hf-internal-testing/llama-tokenizer")
) -> Tuple[str, int]:
    """Generate a prompt that randomly samples lines from a the shakespeare sonnet at sonnet.txt."""
    
    get_token_length = lambda text: len(tokenizer.encode(text))
    
    prompt = (
        "Randomly stream lines from the following text "
        f"with {expect_output_tokens} output tokens. "
        "Don't generate eos tokens:\n\n"
    )
    # ... samples lines from sonnet.txt to reach target token count
```

Limitations:
- No dataset loading from external sources
- No caching mechanism (prompts regenerated each run)
- No data splitting functionality
- Only text preprocessing (tokenization)
- No validation or completeness checking
- Prompts generated on-the-fly rather than prepared in advance

### S2F2: Dataset Quality and Bias Assessment (Rating: 0)

Evidence:
The only quality checking is in the correctness test for validating model outputs:

```python
# llm_correctness.py lines 87-100
for out in completed_requests:
    metrics, generated_text, completed_request_config = out
    
    # if there were no errors when making request.
    if not metrics[common_metrics.ERROR_CODE]:
        try:
            commas_between_numbers_re = r"(\d+),(?=\d)"
            gen_text_commas_removed = re.sub(
                commas_between_numbers_re, r"\1", generated_text
            )
            nums = re.findall(r"\d+", gen_text_commas_removed)
            generated_text = gen_text_commas_removed.replace("\n", " ")
            
            assert str(completed_request_config.metadata['rnd_number"]) in nums
        except:
            num_mismatched_requests += 1
```

This validates model outputs, not dataset quality. There are no features for:
- Label quality analysis
- Demographic distribution checking
- Duplicate detection
- Bias detection in data

### S2F3: PII Detection and Anonymization (Rating: 0)

Evidence:
No PII-related code exists in the repository. The only data source is `sonnet.txt` containing Shakespeare text:

```
# src/llmperf/sonnet.txt (excerpt)
Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
...
```

This is public domain text with no PII concerns, but the framework provides no PII detection/handling capabilities for user-provided data.

### S2F4: Task-Specific Infrastructure Building (Rating: 0)

Evidence:
Ray is used for parallelization but not infrastructure building:

```python
# src/llmperf/requests_launcher.py lines 1-45
class RequestsLauncher:
    """Launch requests from LLMClients to their respective LLM APIs."""
    
    def __init__(self, llm_clients: List[LLMClient]):
        self._llm_client_pool = ActorPool(llm_clients)
    
    def launch_requests(self, request_config: RequestConfig) -> None:
        """Launch requests to the LLM API."""
        if self._llm_client_pool.has_free():
            self._llm_client_pool.submit(
                lambda client, _request_config: client.llm_request.remote(
                    _request_config
                ),
                request_config,
            )
```

This manages concurrent API requests, not evaluation infrastructure. No support for:
- Building retrieval indices (FAISS, ColBERT, BM25)
- Database setup
- Multi-agent environments
- Artifact versioning or persistence

### S2F5: Model Artifact Validation (Rating: 0)

Evidence:
Only environment variable checks exist:

```python
# src/llmperf/ray_clients/vertexai_client.py lines 33-47
def llm_request(self, request_config: RequestConfig) -> Dict[str, Any]:
    project_id = os.environ.get("GCLOUD_PROJECT_ID")
    region = os.environ.get("GCLOUD_REGION")
    endpoint_id = os.environ.get("VERTEXAI_ENDPOINT_ID")
    access_token = os.environ.get("GCLOUD_ACCESS_TOKEN").strip()
    if not project_id:
        raise ValueError("the environment variable GCLOUD_PROJECT_ID must be set.")
    if not region:
        raise ValueError("the environment variable GCLOUD_REGION must be set.")
```

No validation of:
- Model checksums
- Version compatibility
- Configuration schemas
- Model weight integrity
- Corruption detection

### S2F6: Evaluation Scenario Generation (Rating: 1)

Evidence:
Basic scenario generation with token-based variation:

```python
# utils.py lines 114-124
def sample_random_positive_int(mean: int, stddev: int) -> int:
    """Sample random numbers from a gaussian distribution until a positive number is sampled."""
    ret = -1
    while ret <= 0:
        ret = int(random.gauss(mean, stddev))
    return ret
```

Reproducibility through seeding:

```python
# token_benchmark_ray.py line 58
random.seed(11111)
```

Prompt templates exist but are simple:

```python
# llm_correctness.py lines 68-70
prompt = f"Convert the following sequence of words into a number: {rnd_num_words}.\nPrint the number first."
```

Limitations:
- No multi-turn dialogue support
- No edge case generators
- No adversarial input generation
- No combinatorial scenario generation
- Only simple token-length variations

### S2F7: Red-Teaming and Adversarial Test Generation (Rating: 0)

Evidence:
The correctness test is the closest thing to adversarial testing:

```python
# llm_correctness.py lines 64-70
rnd_number = random.randint(0, MAX_RANDOM_NUMBER)
rnd_num_words = num2words.num2words(rnd_number)

prompt = f"Convert the following sequence of words into a number: {rnd_num_words}.\nPrint the number first."
```

This tests basic arithmetic understanding but lacks:
- Jailbreak attempt generation
- Prompt injection tests
- Bias probing prompts
- Safety boundary testing
- Attack taxonomy
- Multi-category safety testing

### S2F8: Data Contamination Detection (Rating: 0)

Evidence:
No contamination detection code exists. The tool doesn't:
- Compare against training corpora
- Check n-gram overlaps
- Perform semantic similarity analysis
- Generate contamination reports

The tool is designed for API testing, not dataset preparation or contamination analysis.

## Key Observations

1. Performance Testing Focus: LLMPerf is designed for load testing and latency measurement, not comprehensive evaluation preparation.

2. Minimal Data Pipeline: Data preparation is limited to on-the-fly prompt generation from a single text file.

3. API-Centric Design: Assumes models are deployed as APIs; no model validation or infrastructure building.

4. Missing Core Features: 7 out of 8 Stage 2 features are completely absent, with only basic scenario generation present.

5. Appropriate for Use Case: While Stage 2 scores are low, the tool accomplishes its stated goal of performance benchmarking well. The low scores reflect that it's not designed for the full evaluation pipeline described in Stage 2.

## Recommendations for Improvement

If LLMPerf were to expand Stage 2 capabilities:

1. Add Dataset Management: Support loading standard datasets (HuggingFace, local files) with caching
2. Implement Preprocessing Pipeline: Add support for multi-modal preprocessing, validation, and versioned splits
3. Include Quality Tools: Basic duplicate detection and balance metrics
4. Add Red-Teaming: Library of adversarial prompts and jailbreak attempts
5. Support Infrastructure: Build retrieval indices for RAG testing
6. PII Detection: Basic regex-based PII detection for custom prompts