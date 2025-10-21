## Comparison Criteria Categories

[Explicit Labels]

## Detailed Analysis

### Explicit Labels

Evidence 1: Qrels Ground Truth Structure
- File: `beir/retrieval/evaluation.py`
- Code Reference: Lines defining EvaluateRetrieval.evaluate() method
```
@staticmethod
def evaluate(
    qrels: dict[str, dict[str, int]],
    results: dict[str, dict[str, float]],
    k_values: list[int],
    ignore_identical_ids: bool = True,
) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float]]:
```
The `qrels` parameter contains explicit relevance labels that serve as ground truth for evaluation. The format is `dict[query_id][doc_id] = relevance_score` where relevance_score is an integer (typically 0 or 1+). These labels represent predetermined correct answers for query-document relevance judgments that are used as the comparison criterion for all metrics.

Evidence 2: Ground Truth Data Loading
- File: `beir/datasets/data_loader.py`
- Code Reference: GenericDataLoader.load() method implementation
```
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")
```
The data loader explicitly loads three components: the document corpus, query collection, and qrels (relevance labels). The qrels are stored in `qrels/test.tsv` files within BEIR benchmark datasets and contain the ground truth relevance judgments that serve as the reference standard for evaluation.

Evidence 3: Qrels File Format Specification
- File: `examples/retrieval/evaluation/custom/evaluate_custom_dataset_files.py`
- Code Reference: Documentation of qrels file structure
```
# Qrels file structure: (Keep 1st row as header)
# query-id  corpus-id   score
# q1    doc1    1
# q2    doc2    1
```
The qrels file format explicitly defines ground truth labels with a simple three-column structure: query ID, corpus/document ID, and relevance score. This TSV format contains static, pre-annotated relevance judgments that represent the correct answers against which model retrieval results are compared.

Evidence 4: PyTREC Evaluation with Ground Truth
- File: `beir/retrieval/evaluation.py`
- Code Reference: Evaluator initialization and scoring
```
evaluator = pytrec_eval.RelevanceEvaluator(
    qrels, 
    {map_string, ndcg_string, recall_string, precision_string}
)
scores = evaluator.evaluate(results)
```
The PyTREC evaluator is initialized with the qrels (relevance labels) as the ground truth reference. The evaluator compares model retrieval results against these explicit labels to compute standard IR metrics including MAP, NDCG, Recall, and Precision. This direct comparison against static labels is the core evaluation mechanism.

Evidence 5: Custom Metrics Using Explicit Labels
- File: `beir/retrieval/custom_metrics.py`
- Code Reference: MRR metric implementation
```
def mrr(
    qrels: dict[str, dict[str, int]], 
    results: dict[str, dict[str, float]], 
    ...
):
    for query_id in top_hits:
        query_relevant_docs = set([
            doc_id for doc_id in qrels[query_id] 
            if qrels[query_id][doc_id] > 0
        ])
```
All custom metrics (MRR, Recall_cap, Hole, Top-K Accuracy) extract relevant documents from the qrels parameter by checking which documents have positive relevance scores. These explicit labels define the set of correct answers for each query, and the metrics measure how well the retrieval results match these predetermined ground truth judgments.