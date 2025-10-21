## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Gold Label Paths in Configuration
- File: `docs/ares-doc/docs/rag_eval.md`
- Code Reference: Lines showing gold label configuration
```
"gold_label_path": "nq_labeled_output.tsv"
```
The configuration explicitly requires a `gold_label_path` parameter that points to a TSV file containing ground truth labels. This file is used as the reference standard for evaluating model outputs on RAG benchmarks. The documentation states: "Specify the file path for the gold label dataset, which contains the true labels for the evaluation dataset."

Evidence 2: Label Columns in Evaluation
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Code Reference: Lines 1391-1396
```
if label_column in test_set.columns:
    test_set = test_set[test_set[label_column].notna()]
```
The code filters evaluation datasets based on the presence of label columns (`Context_Relevance_Label`, `Answer_Faithfulness_Label`, `Answer_Relevance_Label`). These labels are explicit annotations that serve as ground truth for benchmark evaluation.

Evidence 3: Ground Truth Label Usage in PPI
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Code Reference: Lines 1702-1704
```
# Convert predictions and labels to integer type
Y_labeled = Y_labeled_dataset[label_column].values.astype(int)
Yhat_labeled = Y_labeled_dataset[prediction_column].values.astype(int)
```
The system extracts ground truth labels from the labeled dataset and uses them to compute accuracy metrics and confidence intervals. These are explicit reference answers for RAG task evaluation.

Evidence 4: Accuracy Calculation Against Gold Labels
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Code Reference: Lines 19-37
```
def calculate_accuracy(predictions, ground_truth) -> float:
    """
    Calculate the accuracy percentage between predictions and ground truths.
    """
    if len(predictions) != len(ground_truth):
        print(f"Predictions count: {len(predictions)}")
        print(f"Ground truth count: {len(ground_truth)}")
        raise ValueError("Input lists must have the same length")

    correct_count = sum(1 for pred, truth in zip(predictions, ground_truth) if pred == truth)
    total_count = len(predictions)

    accuracy = round(correct_count * 100 / total_count, 2)
    return accuracy
```
This function directly compares model predictions against ground truth labels, confirming that explicit labels are used as the comparison criterion for benchmark evaluation.

Evidence 5: Ground Truth Performance Reporting
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Code Reference: Lines 1731-1736
```
# Compute Ground Truth Performance
ground_truth_available = False
if label_column in Yhat_unlabeled_dataset.columns and not Yhat_unlabeled_dataset[label_column].isnull().all():
    ground_truth_performance = round(Yhat_unlabeled_dataset[label_column].tolist().count(1) / len(Yhat_unlabeled_dataset), 3)
    validation_set_ratios.append(ground_truth_performance)
    ground_truth_available = True
```
The system computes ground truth performance metrics directly from labeled data, demonstrating that explicit labels are available and used as reference outputs for RAG benchmark evaluation.

---

### None

Evidence 1: LLM Judge Scoring Without External References
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Code Reference: Lines 39-110 (Context Relevance Scoring)
```
def few_shot_context_relevance_scoring(
    system_prompt: str, query: str, document: str, gpt_model: str, 
    query_id: str, debug_mode: bool, request_delay: int, 
    failed_extraction_count: Dict[str,int] = {'failed': 0}, 
    few_shot_examples=None
) -> int:
    """
    Evaluates the relevance of a query given a document using few-shot examples.
    """
```
The LLM judge scoring functions evaluate model outputs based on intrinsic quality measures (relevance, faithfulness) without requiring external reference answers for each instance. The few-shot examples guide the evaluation format but don't provide instance-specific reference answers—the LLM makes independent judgments about output quality.

Evidence 2: Self-Contained Quality Assessment
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Code Reference: Lines 142-210 (Answer Faithfulness Scoring)
```
def few_shot_answer_faithfulness_scoring(
    system_prompt: str, query: str, document: str, answer: str, gpt_model: str, 
    query_id: str, debug_mode: bool, request_delay: int, 
    failed_extraction_count: Dict[str,int] = {'failed': 0}, 
    few_shot_examples=None
) -> int:
    """
    Evaluates the faithfulness of an answer given a document and a query using few-shot examples.
    This function constructs a user prompt with few-shot examples (if provided) and the current query,
    document, and answer. It then queries an OpenAI model to determine if the answer is faithful.
    """
```
The faithfulness scoring evaluates whether an answer is consistent with the document without comparing to a predetermined correct answer. This is an intrinsic quality measure that assesses the internal coherence between the answer and its source document.

Evidence 3: Answer Relevance Evaluation
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Code Reference: Lines 212-280 (Answer Relevance Scoring)
```
def few_shot_answer_relevance_scoring(
    system_prompt: str, query: str, document: str, answer: str, gpt_model: str, 
    query_id: str, debug_mode: bool, request_delay: int, 
    failed_extraction_count: Dict[str,int] = {'failed': 0}, 
    few_shot_examples=None
) -> int:
    """
    Evaluates the relevance of an answer given a document and a query using few-shot examples.
    """
```
The relevance scoring measures how well an answer addresses the query without comparing it to a reference answer. This is a reference-free evaluation that judges the answer's appropriateness based on its relationship to the query and document.

Evidence 4: UES/IDP Scoring Configuration
- File: `README.md`
- Code Reference: Lines showing UES/IDP configuration
```
ues_idp_config = {
    "in_domain_prompts_dataset": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "unlabeled_evaluation_set": "nq_unlabeled_output.tsv", 
    "model_choice" : "gpt-3.5-turbo-0125"
} 

ares = ARES(ues_idp=ues_idp_config)
results = ares.ues_idp()
# {'Context Relevance Scores': [Score], 'Answer Faithfulness Scores': [Score], 'Answer Relevance Scores': [Score]}
```
The UES/IDP (Unlabeled Evaluation Set / In-Domain Prompts) scoring operates on unlabeled data, generating quality scores without requiring ground truth labels for each instance. The LLM judge assesses outputs based on intrinsic properties rather than comparison to reference answers.

Evidence 5: System Prompts for Intrinsic Quality Measures
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Code Reference: Lines 1084-1145
```
def filter_dataset(rag_type: str = "question_answering") -> tuple[str, str, str]:
    if rag_type == "question_answering":
        context_relevance_system_prompt = (
            "Given the following question and document, you must analyze the provided document and determine whether it is sufficient for answering the question. "
            "In your evaluation, you should consider the content of the document and how it relates to the provided question. "
            'Output your final verdict by strictly following this format: "[[Yes]]" if the document is sufficient and "[[No]]" if the document provided is not sufficient. '
            "Do not provide any additional explanation for your decision.\n\n"
        )
```
These system prompts instruct the LLM to make intrinsic quality judgments about outputs (sufficiency, faithfulness, relevance) without reference to external gold standards. The evaluation is based on the model's assessment of output properties, not comparison to predetermined correct answers.