# BEIR - Stage 2 (PREPARE) Evaluation

## Summary
BEIR is primarily an evaluation benchmark framework focused on zero-shot retrieval evaluation across diverse IR tasks. It provides minimal data preparation capabilities as it expects pre-formatted datasets. Most preparation features are absent or limited since BEIR's design philosophy centers on consuming pre-packaged datasets rather than supporting comprehensive data preparation pipelines.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Evidence: `beir/datasets/data_loader.py` provides only basic data loading from pre-formatted JSONL files. The `GenericDataLoader` class loads corpus/queries/qrels without preprocessing capabilities:<br>```python<br>def _load_corpus(self, corpus_path):<br>    with open(corpus_path, encoding='utf8') as fIn:<br>        for line in fIn:<br>            line = json.loads(line)<br>            corpus[line.get("_id")] = {<br>                "text": line.get("text"),<br>                "title": line.get("title"),<br>            }<br>```<br>No tokenization, normalization, or validation. No physical splitting - users must download pre-split datasets. No caching mechanism beyond manual file storage. |
| S2F2: Quality Assessment | 0 | Evidence: No code for dataset quality assessment in the repository. No label quality checks, demographic analysis, duplicate detection, or bias detection tools. The framework assumes datasets are already clean and validated. Users must perform all quality checks externally. |
| S2F3: PII Detection | 0 | Evidence: No PII detection or anonymization capabilities exist. Searched repository for privacy-related code - found none. The `examples/dataset/scrape_tweets.py` example removes emojis/links but has no PII handling:<br>```python<br>def preprocess(text):<br>    new_text = []<br>    for t in text.split(" "):<br>        t = 'http' if t.startswith('http') else t<br>        t = '@user' if t.startswith('@') and len(t) > 1 else t<br>        new_text.append(t)<br>```<br>No audit trail or compliance features. |
| S2F4: Infrastructure Building | 2 | Evidence: Limited infrastructure support exists:<br>1. Elasticsearch indexing via `beir/retrieval/search/lexical/bm25_search.py`:<br>```python<br>def index(self, corpus):<br>    self.es.indices.create(...)<br>    for doc_id in corpus:<br>        self.es.index(...)<br>```<br>2. FAISS index support in `examples/retrieval/evaluation/dense/evaluate_faiss_dense.py`:<br>```python<br>faiss_search.save(output_dir=output_dir, prefix=prefix, ext=ext)<br>faiss_search.load(input_dir=input_dir, prefix=prefix, ext=ext)<br>```<br>However, no database setup utilities, no versioning system for indices, and very limited retrieval system variety. Manual configuration required for most infrastructure. |
| S2F5: Model Validation | 1 | Evidence: Minimal validation exists. Models are loaded via HuggingFace/Sentence-Transformers without BEIR-specific validation:<br>```python<br># beir/retrieval/models/sentence_bert.py<br>def __init__(self, model_path):<br>    self.q_model = SentenceTransformer(model_path)<br>```<br>No checksum validation, version compatibility checks, or corruption detection. The framework relies entirely on underlying libraries (transformers, sentence-transformers) for model integrity. No BEIR-specific validation layer. |
| S2F6: Scenario Generation | 1 | Evidence: Very limited generation capability via `beir/generation/generate.py` for query generation (docT5query):<br>```python<br>def generate(self, corpus, ques_per_passage=3, max_length=64, ...):<br>    for start_idx in trange(0, len(corpus), batch_size):<br>        batch = self._prepare_input(...)<br>        outputs = self.model.generate(...)<br>```<br>Only supports synthetic query generation from documents. No prompt variation templates, no multi-turn dialogues, no edge case generators. No scenario versioning. Used in `examples/retrieval/evaluation/sparse/evaluate_anserini_docT5query.py` but very narrow use case. |
| S2F7: Red-Teaming | 0 | Evidence: No red-teaming, adversarial testing, prompt injection, bias probing, or safety boundary testing capabilities. Framework is designed for standard retrieval evaluation only. No security or safety testing features in codebase. |
| S2F8: Contamination Detection | 0 | Evidence: No contamination detection features. No n-gram overlap checking, semantic similarity comparison with training data, or deduplication across train/test splits. The README mentions datasets are "already-preprocessed" but provides no tools to verify data contamination. Users must perform contamination analysis externally. |

## Key Observations

### Strengths
1. Simple data loading: Clean interface for pre-formatted datasets
2. Basic infrastructure: Elasticsearch and FAISS integration exists
3. Clear examples: Well-documented retrieval evaluation examples

### Critical Gaps
1. No preprocessing pipeline: Framework expects data already prepared
2. Zero quality assurance: No tools for data validation or quality checks
3. No privacy features: Complete absence of PII detection/anonymization
4. Limited infrastructure: Only basic retrieval indices, no versioning
5. No security testing: No adversarial or red-team capabilities
6. No contamination checks: Cannot verify test/train data overlap

### Design Philosophy Impact
BEIR is explicitly designed as a benchmark consumption framework rather than a data preparation framework. From `README.md`:
```markdown
## Disclaimer
Similar to Tensorflow datasets or Hugging Face's datasets library, 
we just downloaded and prepared public datasets. We only distribute 
these datasets in a specific format...
```

The framework downloads pre-split, pre-validated datasets (17 benchmark datasets) and focuses on evaluation. This architectural choice explains why most Stage 2 features are absent - they're assumed to be done upstream by dataset creators.

### Evidence of Limited Scope
The `examples/dataset/README.md` shows manual instructions for dataset reproduction:
```markdown
## 1. TREC-NEWS
1. Fill up the application to use the Washington Post (WaPo) Corpus
2. Loop through your contents...
3. I used `html2text` python package...
```

Users must manually prepare non-public datasets with external tools - no built-in preparation support.

### Total Stage 2 Score: 5/24 (20.8%)

BEIR scores very low in Stage 2 because it's fundamentally not a data preparation framework. It's an evaluation harness that expects datasets to arrive already prepared, validated, and split. Organizations needing comprehensive data preparation capabilities would need to build them separately before using BEIR for evaluation.