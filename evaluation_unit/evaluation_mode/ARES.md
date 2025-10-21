## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Multiple scoring functions for context relevance, faithfulness, and answer relevance
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Functions: `few_shot_context_relevance_scoring()`, `few_shot_answer_faithfulness_scoring()`, `few_shot_answer_relevance_scoring()`
- Code Reference:
```python
yes = r"\[\s*\[?\s*Yes\s*\]?\s*\]"
no = r"\[\s*\[?\s*No\s*\]?\s*\]"

if re.search(yes, final_response): 
    return 1
elif re.search(no, final_response):
    return 0
```
These functions evaluate model-generated outputs by comparing them against reference examples without executing generated code. The evaluation process involves text comparison and pattern matching using regular expressions to extract labels from LLM responses. Additionally, format validation ensures that model outputs conform to expected patterns (`[[Yes]]` or `[[No]]`) and issues warnings for incorrect formats. The framework uses LLM judges (GPT, Claude, TogetherAI, vLLM) to score relevance, faithfulness, and other dimensions by examining query-document-answer triples without execution.

Evidence 2: Accuracy calculation through static comparison
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Function: `calculate_accuracy()`
- Code Reference:
```python
def calculate_accuracy(predictions, ground_truth) -> float:
    if len(predictions) != len(ground_truth):
        raise ValueError("Input lists must have the same length")
    
    correct_count = sum(1 for pred, truth in zip(predictions, ground_truth) if pred == truth)
    total_count = len(predictions)
    accuracy = round(correct_count * 100 / total_count, 2)
    return accuracy
```
This function performs static comparison of predictions against ground truth labels through pure comparison logic with no execution of generated artifacts. It validates input lengths, counts correct predictions, and computes percentage accuracy entirely through analytical operations.

Evidence 3: Model evaluation using pre-trained classifiers
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Function: `evaluate_model()`
- Code Reference:
```python
metric = evaluate.load("accuracy")
# ... later in code
results = metric.compute(references=total_references, predictions=total_predictions)
```
The evaluation process involves loading pre-trained classifiers to score model outputs, applying tokenization and classification without executing generated content, and computing metrics through statistical analysis. The framework uses transformer models (DeBERTa, RoBERTa, etc.) to classify responses as relevant/faithful without running the generated content.

Evidence 4: Statistical inference through Prediction-Powered Inference
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Function: `calculate_ppi()`
- Code Reference:
```python
def calculate_ppi(Y_labeled: np.ndarray, Yhat_labeled: np.ndarray, 
                  Yhat_unlabeled: np.ndarray, alpha: float, num_trials: int) -> tuple:
    # Statistical inference calculations
    output = pp_mean_iid_asymptotic(y, f, Yhat_unlabeled, alpha)
    ci[j, i, :] = output
```
This function performs statistical analysis on labeled and unlabeled predictions using Prediction-Powered Inference. It conducts purely analytical work on model outputs through asymptotic statistical methods, computing confidence intervals and estimates without any execution of generated content.

Evidence 5: Documentation of static evaluation methodology
- Files: `docs/ares-doc/docs/rag_eval.md`, `docs/ares-doc/docs/rag_eval_params.md`
- Code Reference:
```python
ppi_config = { 
    "evaluation_datasets": ['nq_ratio_0.6.tsv'], 
    "few_shot_examples_filepath": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "checkpoints": ["...Context_Relevance_Label_joint_datasets_2024-04-30_01:01:01.pt"], 
    "labels": ["Context_Relevance_Label"], 
    "gold_label_path": "nq_labeled_output.tsv"
}
```
The documentation confirms ARES evaluates RAG systems by assessing context relevance, answer faithfulness, and answer relevance using fine-tuned classifiers and synthetic data. The configuration demonstrates a static evaluation approach that performs comprehensive evaluation through scoring rather than execution, relying on pre-trained checkpoints and labeled datasets for assessment.

Evidence 6: Text preprocessing and cleaning functions
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Functions: `combine_query_document()`, `clean_document()`, `clean_query()`
- Code Reference:
```python
def clean_document(document: str) -> str:
    cleaned_document = re.sub(r'\n+', '\n', document.replace("\r", " ").replace("\t", " ")).strip()
    cleaned_document = cleaned_document.replace("=", " ").replace("-", " ")
    cleaned_document = re.sub(r'\s+', ' ', cleaned_document).strip()
    return cleaned_document
```
These functions perform syntactic text transformations using regular expressions and string operations to normalize whitespace, remove special characters, and standardize formatting. They prepare text for analysis without executing any generated code, focusing purely on textual preprocessing for subsequent static evaluation steps.