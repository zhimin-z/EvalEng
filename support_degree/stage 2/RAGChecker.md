# RAGChecker - Stage 2 (PREPARE) Evaluation

## Summary
RAGChecker is a diagnostic framework for RAG systems that operates primarily at evaluation time rather than during data preparation. It has minimal data preparation capabilities, focusing instead on post-hoc analysis of RAG outputs. The framework lacks native preprocessing pipelines, quality assessment tools, and infrastructure building utilities that are core to Stage 2.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 0 | No preprocessing utilities exist. Users must provide pre-formatted JSON with `query`, `gt_answer`, `response`, and `retrieved_context` fields (`examples/checking_inputs.json`). The framework expects data to already be processed and retrieved. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment tools. The framework analyzes RAG system outputs (responses and retrieved contexts) but provides no utilities for checking label quality, demographics, duplicates, or bias in input datasets. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features present in the codebase. Data privacy handling is entirely the user's responsibility. |
| S2F4: Infrastructure Building | 2 | Limited retrieval infrastructure in `rag_baselines/` directory. Includes BM25, E5-Mistral, Cohere, and AOS Neural Sparse indexing via OpenSearch (`rag_baselines/indexing.py`). However, this is supplementary code for baseline RAG systems, not core framework functionality. Only supports vector/keyword indices, no databases or multi-agent environments. |
| S2F5: Model Validation | 0 | No model artifact validation. The framework uses LiteLLM for model invocation but performs no checksum validation, version compatibility checks, or corruption detection. |
| S2F6: Scenario Generation | 0 | No scenario generation capabilities. The framework expects pre-existing query-answer pairs. The `scripts/synthesize_benchmark.py` uses RAGAS for test generation but this is for benchmark creation, not integrated evaluation scenarios. |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial test generation features. The framework evaluates existing RAG outputs but doesn't generate adversarial inputs. |
| S2F8: Contamination Detection | 0 | No data contamination detection utilities. The framework doesn't compare evaluation data against training corpora or detect overlaps. |

## Detailed Analysis

### S2F1: Dataset Preprocessing and Physical Partitioning (0/3)

Evidence:
- Input format from `examples/checking_inputs.json`:
```json
{
  "results": [
    {
      "query_id": "0",
      "query": "What's the longest river in the world?",
      "gt_answer": "The Nile is a major north-flowing river...",
      "response": "The longest river in the world is the Nile...",
      "retrieved_context": [
        {
          "doc_id": "000",
          "text": "Scientists debate whether the Amazon or the Nile..."
        }
      ]
    }
  ]
}
```

Limitations:
- No data loading utilities from common formats (CSV, TSV, datasets library)
- No caching mechanisms for downloaded data
- No preprocessing pipelines (tokenization, normalization, etc.)
- Users must manually format their data into the expected JSON structure
- No train/val/test splitting functionality
- The `data/benchmark/` directory contains processing scripts (`process_bioasq.py`, `process_lotte.py`, etc.) but these are one-off scripts for benchmark creation, not reusable preprocessing utilities

Rating: 0 pts - No preprocessing utilities exist. The framework is evaluation-only.

### S2F2: Dataset Quality and Bias Assessment (0/3)

Evidence:
- No quality assessment code in `ragchecker/` core modules
- `ragchecker/evaluator.py` only performs claim extraction and entailment checking
- No label quality, demographic analysis, or duplicate detection features

Limitations:
- Cannot detect label noise or inconsistencies in ground truth answers
- No inter-annotator agreement metrics
- No demographic distribution analysis
- No duplicate detection (exact or fuzzy)
- No bias detection capabilities

Rating: 0 pts - The framework provides no dataset quality assessment tools.

### S2F3: PII Detection and Anonymization (0/3)

Evidence:
- No PII-related code in the repository
- `ragchecker/` modules contain no privacy-related functionality
- No documentation mentioning PII handling

Rating: 0 pts - No PII detection or anonymization features.

### S2F4: Task-Specific Infrastructure Building (2/3)

Evidence:
- `rag_baselines/indexing.py` supports multiple retrieval systems:
```python
parser.add_argument(
    "--retriever", type=str, default="bm25",
    choices=["bm25", "e5_mistral", "cohere", "aos_neural_sparse"]
)
```

- `rag_baselines/opensearch_client.py` provides OpenSearch integration:
```python
class OpenSearchClient:
    def __init__(self, config):
        self.client = OpenSearch(...)
        self.index_name = config["index_name"]
        self.retriever = config["retriever"]
```

- Index building with persistence (`indexing.py:49-51`):
```python
client = OpenSearchClient(config)
client.load_encoder(rank)
client.build_index(chunks)
```

Strengths:
- Supports 4 retrieval methods (BM25, E5-Mistral, Cohere, AOS Neural Sparse)
- Index persistence via OpenSearch
- Multi-process indexing with `num_workers` parameter

Limitations:
- Infrastructure code is in `rag_baselines/`, not core framework functionality
- No database setup utilities beyond vector indices
- No multi-agent simulation environments
- No artifact versioning or management
- Limited to retrieval systems; no support for knowledge graphs, SQL databases, etc.

Rating: 2 pts - Basic retrieval infrastructure exists but as supplementary code, not integrated framework features. No versioning or advanced infrastructure support.

### S2F5: Model Artifact Validation (0/3)

Evidence:
- Model invocation in `ragchecker/evaluator.py:93-99`:
```python
self.extractor = LLMExtractor(
    model=extractor_name, 
    batch_size=batch_size_extractor,
    api_base=extractor_api_base
)
```

- Uses `litellm` for model calls but no validation layer
- Dependencies in `pyproject.toml`:
```toml
refchecker = "^0.2"
```

Limitations:
- No checksum validation for model weights
- No version compatibility checks
- No configuration validation schemas
- No corruption detection
- Relies on external libraries (litellm, refchecker) without validation

Rating: 0 pts - No model validation features.

### S2F6: Evaluation Scenario Generation (0/3)

Evidence:
- `scripts/synthesize_benchmark.py` uses RAGAS for test generation:
```python
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context, conditional

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)
```

Limitations:
- This is a standalone script for benchmark creation, not integrated scenario generation
- Not part of the evaluation workflow
- No prompt variation utilities
- No multi-turn dialogue generation
- No edge case generators
- Users must create scenarios manually before using RAGChecker

Rating: 0 pts - No scenario generation features. The benchmark script is separate from core functionality.

### S2F7: Red-Teaming and Adversarial Test Generation (0/3)

Evidence:
- No red-teaming code in the repository
- No jailbreak attempts, prompt injection, or safety testing
- Tutorial (`tutorial/ragchecker_tutorial_en.md`) mentions evaluation only, not adversarial generation

Rating: 0 pts - No red-teaming features.

### S2F8: Data Contamination Detection (0/3)

Evidence:
- No contamination detection in the codebase
- `ragchecker/computation.py` contains metric calculations but no n-gram overlap or semantic similarity for contamination
- No tools to compare eval data against training corpora

Rating: 0 pts - No contamination detection capabilities.

## Overall Stage 2 Assessment

Total Score: 2/24 (8.3%)

### Strengths:
1. Basic retrieval infrastructure via OpenSearch integration in baseline code
2. Multi-process indexing for efficiency
3. Clear input format specification for evaluation data

### Critical Gaps:
1. No data preprocessing - Users must pre-format all data
2. No quality assessment - Cannot validate datasets before evaluation
3. No privacy handling - No PII detection or anonymization
4. No model validation - No checks on model integrity or compatibility
5. No scenario generation - Cannot create test variations
6. No red-teaming - No adversarial testing capabilities
7. No contamination detection - Cannot check for data leakage

### Design Philosophy:
RAGChecker is fundamentally an analysis framework rather than a preparation framework. It operates on the assumption that:
- Data is already collected and formatted
- RAG systems are already built and running
- Retrieval and generation have already occurred

This makes it excellent for post-hoc diagnosis but unsuitable for Stage 2 (PREPARE) tasks. The framework should be positioned as Stage 4 (EXECUTE) evaluation tool.

### Recommendations for Users:
If you need Stage 2 capabilities:
1. For preprocessing: Use separate tools like Hugging Face datasets, pandas, or custom scripts
2. For quality assessment: Use dedicated data quality libraries (Great Expectations, Deequ)
3. For infrastructure: Build indices separately using tools in `rag_baselines/` or LlamaIndex
4. For scenario generation: Use RAGAS (as shown in `scripts/synthesize_benchmark.py`) or similar tools
5. For contamination: Implement custom n-gram overlap or use dedicated tools

RAGChecker excels at fine-grained RAG evaluation but requires significant external tooling for preparation tasks.