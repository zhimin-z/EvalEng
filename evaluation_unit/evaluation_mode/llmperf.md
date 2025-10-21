## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Text comparison and metrics collection
- File: `token_benchmark_ray.py`
- Lines: 100-110
- Code Reference:
```python
for out in outs:
    request_metrics, gen_text, _ = out
    num_output_tokens = get_token_length(gen_text)
```
The harness collects model-generated text and analyzes it without execution. The `get_token_length` function (line 72) uses a tokenizer to parse and count tokens in the generated text. This represents direct examination of outputs without running any generated artifacts.

Evidence 2: Token counting and format validation
- File: `token_benchmark_ray.py`
- Lines: 73-77
- Code Reference:
```python
tokenizer = LlamaTokenizerFast.from_pretrained(
    "hf-internal-testing/llama-tokenizer"
)
get_token_length = lambda text: len(tokenizer.encode(text))
```
Token counting is performed on model outputs using static tokenization. The harness validates text at the syntactic level by encoding and measuring token counts, which is a surface-level characteristic analysis that requires no execution.

Evidence 3: Pattern matching and text comparison
- File: `llm_correctness.py`
- Lines: 120-136
- Code Reference:
```python
commas_between_numbers_re = r"(\d+),(?=\d)"
gen_text_commas_removed = re.sub(
    commas_between_numbers_re, r"\1", generated_text
)
nums = re.findall(r"\d+", gen_text_commas_removed)
generated_text = gen_text_commas_removed.replace("\n", " ")

assert str(completed_request_config.metadata["rnd_number"]) in nums
```
The harness validates correctness by parsing and matching patterns in generated text without executing it. This uses regex-based structural analysis to extract and verify numbers, demonstrating validation through text inspection rather than functional testing.

Evidence 4: Statistical analysis of collected metrics
- File: `token_benchmark_ray.py`
- Function: `metrics_summary()`
- Lines: 156-250
- Code Reference:
```python
def metrics_summary(
    metrics: List[Dict[str, Any]], start_time: int, end_time: int
) -> Dict[str, Any]:
    df = pd.DataFrame(metrics)
    df_without_errored_req = df[df[common_metrics.ERROR_CODE].isna()]
    
    for key in [
        common_metrics.INTER_TOKEN_LAT,
        common_metrics.TTFT,
        common_metrics.E2E_LAT,
        ...
    ]:
        series = pd.Series(list(flatten(df_without_errored_req[key]))).dropna()
        quantiles = series.quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99]).to_dict()
```
Statistical analysis of collected metrics is performed using pandas without executing model outputs. The harness computes quantiles and aggregates performance characteristics, focusing on metadata analysis (latency, throughput) rather than semantic or functional validation.

Evidence 5: Response parsing and structure validation
- File: `src/llmperf/ray_clients/openai_chat_completions_client.py`
- Lines: 78-98
- Code Reference:
```python
for chunk in response.iter_lines(chunk_size=None):
    chunk = chunk.strip()
    if not chunk:
        continue
    stem = "data: "
    chunk = chunk[len(stem) :]
    if chunk == b"[DONE]":
        continue
    tokens_received += 1
    data = json.loads(chunk)
    
    if "error" in data:
        error_msg = data["error"]["message"]
        error_response_code = data["error"]["code"]
        raise RuntimeError(data["error"]["message"])
    
    delta = data["choices"][0]["delta"]
    if delta.get("content", None):
        generated_text += delta["content"]
```
JSON parsing and structure validation of API responses is performed to extract generated content and error information. The harness validates response format and extracts text fields without executing any generated code, demonstrating format-level inspection typical of static analysis.