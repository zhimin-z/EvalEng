# beir-cellar__beir - Stage 1 (CONFIGURE) Evaluation

## Summary
BEIR is a heterogeneous benchmark for information retrieval models with a focus on zero-shot evaluation. It provides basic dataset download/loading capabilities and model configuration through code, but lacks dedicated configuration abstractions, environment management, security features, and cost estimation capabilities. The framework is primarily designed for evaluation rather than comprehensive configuration management.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Evidence: Basic dataset loading exists via `GenericDataLoader` and `HFDataLoader` (see `beir/datasets/data_loader.py` and `beir/datasets/data_loader_hf.py`), supporting JSON/JSONL and HuggingFace datasets. However, there's no dataset registration system, no schema definition API, no declarative split strategies, and no versioning system. Users must manually download datasets via URLs (`util.download_and_unzip()`) or provide paths. Example from `examples/retrieval/evaluation/dense/evaluate_sbert.py`:<br>`url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"`<br>`data_path = util.download_and_unzip(url, out_dir)`<br>`corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")`<br>The `load()` method only accepts hardcoded split names ("test", "dev", "train") with no declarative configuration. |
| S1F2: Model Configuration | 1 | Evidence: Model configuration is done entirely through Python code with no external config files. Examples show hardcoded initialization:<br>From `examples/retrieval/evaluation/dense/evaluate_sbert.py`:<br>`dense_model = models.SentenceBERT("msmarco-distilbert-base-tas-b")`<br>`model = DRES(dense_model, batch_size=128)`<br>Supports 3-4 model types (SentenceBERT, DPR, HuggingFace, APIs) but no YAML/JSON configuration system. Authentication is handled via environment variables only (`os.getenv("COHERE_API_KEY")`). No validation before execution, no multi-region support. Resource allocation (batch_size, GPU) is specified as function parameters, not in a config file. |
| S1F3: Prompt Configuration | 0 | Evidence: No prompt templating system exists. Prompts are hardcoded strings in Python:<br>From `examples/retrieval/evaluation/dense/evaluate_huggingface.py`:<br>`query_prompt = "Instruct: Given a question, retrieve relevant documents that answer the question\nQuery: "`<br>`passage_prompt = ""`<br>`prompts={"query": query_prompt, "passage": passage_prompt}`<br>No template engine (no Jinja2), no variable substitution beyond dict keys, no few-shot support, no prompt versioning, no metric configuration system. The framework focuses on evaluation metrics hardcoded in `EvaluateRetrieval` class. |
| S1F4: Environment Setup | 2 | Evidence: Has basic dependency management via `pyproject.toml` with dependencies listed:<br>`dependencies = ["sentence-transformers>=2.2.0", "pytrec-eval", "faiss-cpu>=1.6.1", ...]`<br>Docker examples exist for Pyserini integration (`examples/beir-pyserini/Dockerfile`). However, no pinned versions in most dependencies (uses `>=` instead of `==`), no setup scripts beyond pip install, no virtual environment management built-in, no hardware compatibility checks. Installation is straightforward: `pip install beir` or `pip install -e .` from source. No conda environment files provided in main repo. |
| S1F5: Security & Access | 0 | Evidence: Minimal security features. Only environment variables for API keys:<br>From `examples/retrieval/evaluation/apis/evaluate_cohere.py`:<br>`cohere_api_key = os.getenv("COHERE_API_KEY")`<br>No vault integration, no RBAC, no access control system, no audit logging, no encryption at rest, no SSO/LDAP support. The framework is designed for research/benchmarking, not production deployment with security requirements. |
| S1F6: Cost Estimation | 0 | Evidence: No cost estimation capabilities exist. The framework doesn't track token counts, API pricing, or provide budget tools. Examples show batch_size configuration for performance but no cost modeling:<br>`model = DRES(dense_model, batch_size=128)`<br>No resource projection, no budget limits, no cost optimization suggestions. Users must manually calculate costs based on API usage from external providers. |

## Additional Observations

### Strengths
1. Simple data loading: Straightforward API for loading BEIR benchmark datasets
2. Multiple model support: Examples cover dense, sparse, lexical, and API-based retrievers
3. Evaluation focus: Strong on metrics computation (NDCG, MAP, Recall, etc.)

### Weaknesses
1. No configuration abstraction: Everything is hardcoded in Python scripts
2. No environment isolation: Users must manage their own environments
3. Limited to evaluation: Not designed as a full-featured ML pipeline framework
4. No declarative configuration: Cannot specify experiments via YAML/JSON

### Example of Configuration Pattern
```python
# From examples/retrieval/evaluation/dense/evaluate_huggingface.py
model_name_or_path = "intfloat/e5-mistral-7b-instruct"
max_length = 512
pooling = "eos"
normalize = True
append_eos_token = True

dense_model = models.HuggingFace(
    model_path=model_name_or_path,
    max_length=max_length,
    append_eos_token=append_eos_token,
    pooling=pooling,
    normalize=normalize,
    prompts={"query": query_prompt, "passage": passage_prompt},
    attn_implementation="flash_attention_2",
    torch_dtype="bfloat16",
)
```

This imperative approach lacks the configuration management features expected in Stage 1 of a comprehensive evaluation framework.

Total Stage 1 Score: 4/18 (22.2%)

The BEIR framework is purpose-built for benchmarking information retrieval models with minimal configuration overhead, which explains its low score in configuration capabilities. It prioritizes ease of use for researchers over enterprise-grade configuration management.