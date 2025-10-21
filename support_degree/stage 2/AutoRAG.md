# AutoRAG - Stage 2 (PREPARE) Evaluation

## Summary
AutoRAG provides comprehensive data preparation capabilities including parsing, chunking, and QA dataset creation, but lacks specialized infrastructure building, PII detection, and contamination detection features. The framework emphasizes evaluation dataset preparation through synthetic data generation and schema-based data management (Raw, Corpus, QA), with strong support for preprocessing pipelines and quality assessment through manual validation workflows.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 3 | Strong multi-stage preprocessing with caching and validation. AutoRAG provides comprehensive parsing (`autorag/parser.py`), chunking (`autorag/chunker.py`), and data creation pipelines. Multiple preprocessing methods supported: LlamaIndex (Token, Sentence, Window, Semantic) and LangChain (Character, RecursiveCharacter) chunkers. Automatic file name addition to prevent hallucination. Results cached in project directories with automatic saving (`cache_batch` parameter in `make_single_content_qa`). Schema validation through `Raw`, `Corpus`, and `QA` classes ensuring data format consistency. Example: `docs/source/data_creation/chunk/llama_index_chunk.md` shows `chunk_method: [Token, Sentence]` with configurable `chunk_size` and `chunk_overlap`. |
| S2F2: Quality Assessment | 2 | Basic quality checks through validation workflow, but limited automated assessment. Manual QA validation required per `docs/source/data_creation/legacy/tutorial.md`: "you have to clarify the retrieval_gt is right. If retrieval_gt is not relevant, you have to remove it from the dataset." Schema validation ensures required columns (`qid`, `query`, `retrieval_gt`, `generation_gt`) exist in `docs/source/data_creation/data_format.md`. Duplicate detection through unique `doc_id` enforcement with warnings: "Do not make a duplicate doc id." No automated bias detection, inter-annotator agreement metrics, or demographic distribution analysis found in codebase. |
| S2F3: PII Detection | 0 | No PII detection or anonymization capabilities. Searched across all documentation and configuration files for terms like "PII", "anonymization", "redaction", "privacy", "GDPR", "personally identifiable" with no results. No modules in `autorag/data/` directory handle sensitive data detection. No mention in data creation tutorials (`docs/source/data_creation/`) or API specifications. |
| S2F4: Infrastructure Building | 1 | Limited to vector database setup, missing broader infrastructure. VectorDB configuration in `docs/source/local_model.md` shows support for Chroma, Milvus, Pinecone, Qdrant, Weaviate with embedding models: `vectordb: - name: chroma_openai, db_type: chroma, embedding_model: openai_embed_3_large`. BM25 indices created automatically (`resources/bm25.pkl` in `docs/source/optimization/folder_structure.md`). No support for ColBERT, Elasticsearch, or specialized task environments. No artifact versioning or cloud storage integration beyond local persistence. Missing database schema creation for knowledge-intensive tasks. |
| S2F5: Model Validation | 1 | Minimal validation limited to configuration checks. Validator class in `autorag/validator.py` performs basic YAML validation per `docs/source/tutorial.md`: `validator.validate('your/path/to/config.yaml')`. Warning for passage augmenter: "The passage augmenter is not supporting a validation process now" in `docs/source/troubleshooting.md`. No checksum verification, cryptographic validation, or model weight integrity checks. Version compatibility checking absent - only Python version requirement specified (≥3.10). No corruption detection or test inference validation. |
| S2F6: Scenario Generation | 2 | Basic query generation with limited variation support. QA creation supports multiple prompt templates via `prompts_ratio` dictionary in `docs/source/data_creation/legacy/tutorial.md`: `{'prompt1.txt': 1, 'prompt2.txt': 2}`. Query evolution through RAGAS integration with types: simple, reasoning, multi_context, conditional (`docs/source/data_creation/legacy/ragas.md`). Query expansion modules (hyde, query_decompose, multi_query_expansion) per `docs/source/api_spec/autorag.nodes.queryexpansion.rst`. No explicit multi-turn dialogue support, edge case generators, or adversarial input generation. Reproducibility via LLM temperature control but no seed management for deterministic generation. |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial testing capabilities. Searched documentation for "red team", "jailbreak", "adversarial", "prompt injection", "safety", "bias probing" with no results. No modules in `autorag/nodes/` or `autorag/data/` directories handle security testing. Evaluation metrics (`docs/source/evaluate_metrics/`) focus only on retrieval and generation quality, not safety boundaries or attack detection. |
| S2F8: Contamination Detection | 0 | No contamination detection features. No mentions of "contamination", "training corpus comparison", "n-gram overlap", "fingerprint", "semantic similarity detection" in documentation or codebase. `docs/source/data_creation/data_format.md` focuses on QA/corpus format requirements without addressing data leakage. No tools for comparing evaluation data against training corpora or identifying paraphrases. |

## Key Strengths

1. Comprehensive Preprocessing Pipeline: Three-stage pipeline (Parse → Chunk → QA) with 10+ parsing methods and 8+ chunking strategies
2. Schema-Based Data Management: Strongly typed `Raw`, `Corpus`, `QA` classes ensuring data integrity throughout pipeline
3. Multi-Modal Parser Support: PDF (pdfminer, pypdf), web (clova), tables (table_hybrid_parse) with extensible architecture
4. Automatic Metadata Handling: File names, paths, timestamps, prev/next chunk IDs automatically tracked
5. Batch Processing with Auto-Save: `cache_batch` parameter prevents data loss during long-running QA generation

## Key Gaps

1. No Security Features: Missing PII detection, anonymization, or data privacy tools despite handling potentially sensitive documents
2. Limited Quality Automation: Relies heavily on manual validation rather than automated quality metrics or bias detection
3. Missing Advanced Infrastructure: No ColBERT, BM25 persistence options, or multi-index support beyond basic VectorDB
4. No Adversarial Testing: Complete absence of red-teaming, safety testing, or robustness evaluation capabilities
5. No Contamination Safeguards: Cannot detect if evaluation data overlaps with training corpora

## Evidence-Based Observations

Strength Example (`autorag/chunker.py`):
```python
def start_chunking(self, yaml_path: str):
    # Auto-saves results with configurable batch size
    # Tracks all chunk parameters in summary.csv
    # Validates output schema automatically
```

Gap Example (Missing from entire codebase):
- No `autorag/security/` or `autorag/privacy/` modules
- No contamination detection in `autorag/evaluation/` despite having retrieval/generation metrics
- No adversarial testing in `autorag/nodes/` despite comprehensive node coverage

Documentation Quality: High - extensive Markdown docs with examples, but focused narrowly on evaluation dataset creation rather than broader preparation needs.