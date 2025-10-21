## Evaluator Categories

[ML-based, Algorithmic]

## Detailed Analysis

### ML-based

Evidence 1: LLM-as-Judge Evaluation
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Functions: `few_shot_context_relevance_scoring()`, `few_shot_answer_faithfulness_scoring()`, `few_shot_answer_relevance_scoring()`, and their variants for different APIs (Azure, TogetherAI, Claude, vLLM)
- Code Reference:
```python
def few_shot_context_relevance_scoring(
    system_prompt: str, query: str, document: str, gpt_model: str, 
    query_id: str, debug_mode: bool, request_delay: int, 
    failed_extraction_count: Dict[str,int] = {'failed': 0}, 
    few_shot_examples=None
) -> int:
    """
    Evaluates the relevance of a query given a document using few-shot examples.
    This function constructs a user prompt with few-shot examples (if provided) and the current query,
    document, and answer. It then queries an OpenAI model to determine if the query is context relevant to the
    document.
    """
    # ...
    response = openai.chat.completions.create(
                        model=gpt_model,
                        messages=messages
                    )    
    final_response = response.choices[0].message.content
```
ARES uses large language models (GPT-3.5, GPT-4, Claude, Llama-2, etc.) as judges to evaluate RAG system outputs. These are ML models that assess benchmark task outputs for context relevance, answer faithfulness, and answer relevance. The system makes API calls to various LLM providers (OpenAI, Anthropic, TogetherAI) or uses local models via vLLM to generate evaluative judgments.

Evidence 2: Fine-tuned Classifier Models
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Class: `CustomBERTModel`
- Code Reference:
```python
class CustomBERTModel(nn.Module):
    def __init__(self, number_of_labels: int, model_choice: str):
        """
        Initializes the CustomBERTModel with the specified number of labels and model choice.
        """
        self.model_choice = model_choice
        super(CustomBERTModel, self).__init__()
        
        if model_choice in ["roberta-large", "microsoft/deberta-v3-large"]:
            model_encoding = AutoModel.from_pretrained(model_choice)
            embedding_size = 1024
            self.encoderModel = model_encoding
        # ... other model choices
        
        self.classifier = nn.Sequential(
            nn.Linear(embedding_size, 256),
            nn.Linear(256, number_of_labels)
        )
```
ARES trains and uses fine-tuned transformer-based classifiers (BERT, RoBERTa, DeBERTa, T5, MPT variants) to evaluate RAG outputs. These are learned ML models with trained parameters that classify context relevance, answer faithfulness, and answer relevance. The evaluation process loads checkpoints from training and uses these models for inference on benchmark tasks.

Evidence 3: Embedding-based Evaluation with Late Chunking
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Functions: References to late chunking classifier in evaluation functions
- Code Reference:
```python
if use_late_chunking:
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer
    from ares.LLM_as_a_Judge_Adaptation.Late_Chunking_Classifier import SBERTBinaryClassifier, get_late_chunked_embeddings, get_query_embedding
    
    # Load embedding model and tokenizer
    embedding_model_name = "jinaai/jina-embeddings-v2-base-en"
    embedding_model = SentenceTransformer(embedding_model_name, device=device, trust_remote_code=True)
    embedding_model.max_seq_length = 8192
    # ...
    classifier_model = SBERTBinaryClassifier(embedding_dim=embedding_size)
    classifier_model.load_state_dict(torch.load(checkpoint))
    classifier_model.eval()
```
ARES includes an embedding-based evaluation approach using Sentence-BERT models to generate embeddings, which are then fed to a binary classifier. This is another ML-based evaluation method where learned neural network models assess the quality of RAG outputs.

---

### Algorithmic

Evidence 1: Accuracy Calculation
- File: `ares/RAG_Automatic_Evaluation/Evaluation_Functions.py`
- Function: `calculate_accuracy()`
- Code Reference:
```python
def calculate_accuracy(predictions, ground_truth) -> float:
    """
    Calculate the accuracy percentage between predictions and ground truths.

    Args:
    predictions (list): A list of predicted values.
    ground_truth (list): A list of actual values.

    Returns:
    float: The accuracy percentage rounded to two decimal places.

    Raises:
    ValueError: If the input lists have different lengths.
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
This is a deterministic algorithmic metric that computes accuracy by comparing predictions against ground truth labels using simple mathematical operations (counting matches and dividing). This is a standard evaluation metric computed through rule-based logic.

Evidence 2: PPI (Prediction-Powered Inference) Statistical Calculations
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Function: `calculate_ppi()`
- Code Reference:
```python
def calculate_ppi(Y_labeled: np.ndarray, Yhat_labeled: np.ndarray, 
                  Yhat_unlabeled: np.ndarray, alpha: float, num_trials: int) -> tuple:
    """
    Calculate prediction-powered inference (PPI) and classical inference intervals.
    
    Parameters:
    Y_labeled (np.ndarray): Labeled ground truth values.
    Yhat_labeled (np.ndarray): Predictions for the labeled data.
    Yhat_unlabeled (np.ndarray): Predictions for the unlabeled data.
    alpha (float): Significance level for the confidence intervals.
    num_trials (int): Number of trials to run for the inference.
    
    Returns:
    tuple: A tuple containing the average PPI confidence interval, the average classical confidence interval, and the imputed-only confidence interval.
    """
    
    n_max = Y_labeled.shape[0]
    ns = np.linspace(0, n_max, 20).astype(int)

    # Imputed-only estimate
    imputed_estimate = (Yhat_labeled.sum() + Yhat_unlabeled.sum()) / (Yhat_labeled.shape[0] + Yhat_unlabeled.shape[0])
    
    # ... confidence interval calculations
    output = pp_mean_iid_asymptotic(y, f, Yhat_unlabeled, alpha)
```
The PPI calculation is a statistical inference method that uses mathematical formulas to compute confidence intervals. It combines labeled and unlabeled predictions through deterministic statistical computations, making it an algorithmic evaluation approach that doesn't rely on ML models but rather on statistical theory.

Evidence 3: Metric Loading and Computation
- File: `ares/RAG_Automatic_Evaluation/LLMJudge_RAG_Compared_Scoring.py`
- Usage: Throughout evaluation functions
- Code Reference:
```python
def evaluate_model(params: dict) -> tuple:
    # ...
    metric = evaluate.load("accuracy")
    
    # ... during evaluation
    metric.add_batch(predictions=predictions, references=batch['labels'].to(device))
    
    # ... final computation
    results = metric.compute(references=total_references, predictions=total_predictions)
```
The harness uses the HuggingFace `evaluate` library to load and compute standard algorithmic metrics (accuracy). These are predefined mathematical functions that score model outputs based on statistical formulas and exact matching rules.