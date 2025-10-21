## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Retrieval Metrics Evaluation
- File: `docs/source/evaluate_metrics/retrieval.md`
- Code Reference:
```
Retrieval metrics (Precision, Recall, F1, MRR, MAP, NDCG)
```
AutoRAG implements comprehensive retrieval metrics that compare model-generated retrieval results against ground truth through direct comparison without execution. These metrics analyze retrieval output by calculating statistical measures like precision, recall, and F1 scores by comparing retrieved document IDs against ground truth IDs. For example, the documentation states: "retrieval_result must contain either 'test-1 or test-2' and test-3 for all answers to be accepted as correct" and then labels results as `[1, 0, 1, 0]` for correct/incorrect matches. This is pure static comparison of outputs.

Evidence 2: Token-Based Metrics
- File: `docs/source/evaluate_metrics/retrieval_contents.md`
- Code Reference:
```
Token Precision, Token Recall, Token F1
```
The framework performs token-level comparison between generated passages and ground truth answers. The documentation shows: "First, let's break up gt and result into tokens" and then counts overlapping tokens between the result and ground truth. This is syntactic analysis and pattern matching without any execution - just comparing tokenized strings. Example: "The first is that all six tokens overlap with GT, so the number of overlapping tokens is 6."

Evidence 3: Generation Metrics Evaluation
- File: `docs/source/test_your_rag.md`
- Code Reference:
```python
@evaluate_generation(metric_inputs=metric_inputs, metrics=["bleu", "meteor", "rouge"])
```
The evaluation decorator allows users to test their RAG generation outputs using text similarity metrics. The code shows: `@evaluate_generation(metric_inputs=metric_inputs, metrics=["bleu", "meteor", "rouge"])`. These metrics perform static text comparison between generated outputs and reference texts without executing any code. BLEU, METEOR, and ROUGE are all string-based similarity metrics.

Evidence 4: Metric Computation Modules
- File: `docs/source/api_spec/autorag.evaluation.metric.rst`
- Modules: `generation`, `retrieval`, `retrieval_contents`
- Code Reference:
```
Modules: generation, retrieval, retrieval_contents
```
The API documentation reveals separate modules for computing generation and retrieval metrics. These modules implement the static comparison logic for evaluating model outputs against ground truth through text/ID matching and statistical calculations.

Evidence 5: Evaluation Decorator Implementation
- File: `docs/source/test_your_rag.md`
- Code Reference:
```python
@evaluate_retrieval(
    metric_inputs=metric_inputs,
    metrics=["retrieval_f1", "retrieval_recall", "retrieval_precision",
             "retrieval_ndcg", "retrieval_map", "retrieval_mrr"]
)
def custom_retrieval(queries):
    return retrieved_contents, retrieved_ids, retrieve_scores
```
The decorator pattern shown here captures the outputs from custom retrieval functions and evaluates them against ground truth using static metrics. The evaluation happens after the retrieval completes by comparing the returned IDs and scores against the `retrieval_gt` field in MetricInput, without executing any of the retrieved content.

---

### Dynamic Execution

Evidence 1: Parser Module Execution
- File: `tests/autorag/test_parser.py`
- Class/Function: `Parser.start_parsing()`
- Code Reference:
```python
parser.start_parsing(yaml_path, all_files=False)
```
The Parser module executes parsing operations on various document types (PDF, CSV, JSON, HTML, XML, Markdown). Test code shows: `parser.start_parsing(yaml_path, all_files=False)` which dynamically processes files based on configuration. The execution results are stored as parquet files containing parsed text. This is clear dynamic execution of model-generated parsing strategies on input documents.

Evidence 2: Trial Execution in Evaluator
- File: `tests/autorag/test_evaluator.py`
- Class/Function: `evaluator.start_trial()`
- Code Reference:
```python
evaluator.start_trial(os.path.join(resource_dir, "simple.yaml"))
```
The evaluator dynamically executes entire RAG pipeline trials based on YAML configurations. Test shows: `evaluator.start_trial(os.path.join(resource_dir, "simple.yaml"))` which runs multiple node types (retrieval, reranking, generation) sequentially. The framework executes different module implementations (BM25, vector databases, hybrid retrievers) and measures their performance, storing execution results in parquet files.

Evidence 3: Node Execution Pipeline
- File: `tests/autorag/nodes/passagereranker/test_passage_reranker_run.py`
- Function: `run_passage_reranker_node()`
- Code Reference:
```python
best_result = run_passage_reranker_node(modules, module_params, previous_result, 
                                        node_line_dir, strategies)
```
The code executes passage reranker modules dynamically during evaluation: `best_result = run_passage_reranker_node(modules, module_params, previous_result, node_line_dir, strategies)`. Each module (MonoT5, etc.) is instantiated and executed with different parameters, and the execution results are captured and evaluated. This shows dynamic execution of model-generated reranking strategies.

Evidence 4: API Runner Execution
- File: `tests/autorag/test_deploy.py`
- Class/Function: `Runner` and `ApiRunner` classes
- Code Reference:
```python
answer = runner.run("What is the best movie in Korea?...")
```
The Runner classes execute complete RAG pipelines in deployment. Test code shows: `answer = runner.run("What is the best movie in Korea?...")` which dynamically executes the entire pipeline (query expansion, retrieval, reranking, generation) and returns results. The ApiRunner extends this to serve as an API endpoint, executing pipelines on incoming requests.

Evidence 5: VectorDB Ingestion and Query Execution
- File: `tests/autorag/nodes/retrieval/test_hybrid_base.py`
- Code Reference:
```python
loop.run_until_complete(vectordb_ingest_api(chroma, corpus_df))
```
The framework executes vector database ingestion operations: `loop.run_until_complete(vectordb_ingest_api(chroma, corpus_df))` which dynamically processes corpus data, generates embeddings, and stores them in vector databases. Subsequent retrieval operations execute queries against these databases, demonstrating dynamic execution of search operations based on the ingested data.

Evidence 6: Module Parameter Optimization
- File: `tests/autorag/test_evaluator.py`
- Code Reference:
```
Multiple module configurations tested in trials
```
The evaluator executes multiple configurations of each module type with different parameters (e.g., different BM25 tokenizers, vector database settings) and measures execution time and performance. For example, hybrid retrieval tests various weight combinations by actually executing the retrieval with each configuration. This is dynamic execution to find optimal parameters.

Evidence 7: LLM Generation Execution
- File: `docs/source/nodes/retrieval/retrieval.md` and test files
- Code Reference:
```python
@patch.object(OpenAI, "acomplete", mock_acomplete)
```
The framework executes LLM generation as part of the RAG pipeline. While mocked in tests, the actual implementation calls LLM APIs to generate responses based on retrieved context. The test setup with `mock_acomplete` shows that generation execution is a core component: `@patch.object(OpenAI, "acomplete", mock_acomplete)`.