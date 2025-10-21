## Comparison Criteria Categories

[Explicit Labels, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Classification and QA Metrics
- File: `promptbench/metrics/eval.py`
- Code Reference: `compute_cls_accuracy()`, `compute_squad_v2_f1()`, `compute_bleu()`, `compute_math_accuracy()`
```python
@staticmethod
def compute_cls_accuracy(preds, gts):
    """
    Computes classification accuracy based on predictions and ground truths.
    
    Parameters:
    -----------
    preds : list
        A list of predictions.
    gts : list
        A list of ground truths.
    """
    try:
        preds = [str(pred).lower() for pred in preds]
        gts = [str(gt).lower() for gt in gts]
    except AttributeError:
        print("Something in either preds or gts can not be convert to a string.")
    
    if not isinstance(preds, list):
        preds = [preds]
        gts = [gts]

    return sum(a == b for a, b in zip(preds, gts)) / len(preds)
```
These methods compare model predictions against ground truth labels (`gts` parameter). The evaluation functions expect explicit reference answers for benchmark tasks including classification (SST-2, CoLA), question answering (SQuAD v2), translation (BLEU), and math problems, using predetermined correct answers as comparison targets.

Evidence 2: Label Mapping Dictionaries
- File: `promptbench/config.py`
- Code Reference: `LABEL_TO_ID` and `ID_TO_LABEL` dictionaries
```python
LABEL_TO_ID = {
    'mmlu': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
    'sst2': {'negative': 0, 'positive': 1, '0': 0, '1': 1, 0: 0, 1: 1},
    'mnli': {'entailment': 0, 'neutral': 1, 'contradiction': 2, ...},
    ...
}

ID_TO_LABEL = {
    'mmlu': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
    'sst2': {0: 'negative', 1: 'positive'},
    ...
}
```
These mappings define explicit labels for various benchmark datasets. They represent predetermined correct answer categories that model outputs are compared against for evaluation.

Evidence 3: Dataset Label Extraction
- File: `docs/examples/basic.md`
- Code Reference: Dataset loading and label comparison
```python
for data in tqdm(dataset):
    # process input
    input_text = pb.InputProcess.basic_format(prompt, data)
    label = data['label']  # Extracting ground truth label
    raw_pred = model(input_text)
    # process output
    pred = pb.OutputProcess.cls(raw_pred, proj_func)
    preds.append(pred)
    labels.append(label)  # Collecting ground truth labels

# evaluate
score = pb.Eval.compute_cls_accuracy(preds, labels)
```
Demonstrates loading explicit labels from dataset instances (`data['label']`) and comparing predictions against these ground truth labels. The labels are static reference answers for benchmark evaluation.

Evidence 4: SQuAD v2 Ground Truth
- File: `promptbench/metrics/squad_v2/compute_score.py`
- Code Reference: SQuAD v2 evaluation
```python
def get_raw_scores(dataset, preds):
    exact_scores = {}
    f1_scores = {}
    for article in dataset:
        for p in article["paragraphs"]:
            for qa in p["qas"]:
                qid = qa["id"]
                gold_answers = [t for t in qa["answers"]["text"] if normalize_answer(t)]
                if not gold_answers:
                    # For unanswerable questions, only correct answer is empty string
                    gold_answers = [""]
                if qid not in preds:
                    print(f"Missing prediction for {qid}")
                    continue
                a_pred = preds[qid]
                # Take max over all gold answers
                exact_scores[qid] = max(compute_exact(a, a_pred) for a in gold_answers)
                f1_scores[qid] = max(compute_f1(a, a_pred) for a in gold_answers)
    return exact_scores, f1_scores
```
Loads explicit reference answers (`gold_answers`) from the SQuAD v2 dataset and computes exact match and F1 scores against model predictions. These are predetermined correct answers for the QA benchmark.

Evidence 5: VQA Ground Truth Answers
- File: `promptbench/metrics/vqa/eval_vqa.py`
- Code Reference: VQA evaluation with ground truth answers
```python
def evaluate(self, gts, res, quesIds=None):
    # ...
    for quesId in quesIds:
        resAns = res[quesId]["answer"]
        # ... processing ...
        gtAcc = []
        gtAnswers = [ans["answer"] for ans in gts[quesId]["answers"]]
        # ... 
        for gtAnsDatum in gts[quesId]["answers"]:
            otherGTAns = [
                item for item in gts[quesId]["answers"] if item != gtAnsDatum
            ]
            matchingAns = [item for item in otherGTAns if item["answer"] == resAns]
            acc = min(1, float(len(matchingAns)) / 3)
            gtAcc.append(acc)
        avgGTAcc = float(sum(gtAcc)) / len(gtAcc)
        accQA.append(avgGTAcc)
```
Loads ground truth answers (`gts[quesId]["answers"]`) from the VQA dataset and compares them against model responses to compute accuracy. These are explicit reference labels for the visual question answering benchmark.

---

### None

Evidence 1: Extended Rasch Model
- File: `promptbench/prompteval/efficient_eval.py`
- Code Reference: `fit_Y()` function
```python
def fit_Y(X, Y_seen, seen_examples):
    """
    Fits a model to the seen examples using the Extended Rasch Model and calculates the 
    predicted scores for each prompt.

    Parameters:
    X (np.ndarray): The matrix of prompt embeddings.
    Y_seen (np.ndarray): The matrix of observed example results (1 for correct, 0 for incorrect, 
                         -99 for unseen).
    seen_examples (np.ndarray): A boolean matrix indicating which examples were observed.

    Returns:
    np.ndarray: A vector of predicted scores for each prompt, calculated as the mean score 
                across all seen examples.
    """
    
    extended_rasch_cov = ExtendedRaschModel()
    extended_rasch_cov.fit(seen_examples, Y_seen, X)
    S_hat_cov = extended_rasch_cov.get_Y_hat().mean(1)
    
    return S_hat_cov
```
Implements the Extended Rasch Model (from PromptEval), a statistical model that predicts prompt performance from observed samples without requiring explicit reference answers for all examples. Uses intrinsic patterns in observed data to estimate performance across unseen examples, providing reference-free evaluation of prompt quality through self-contained statistical properties.

Evidence 2: Efficient Evaluation Statistics
- File: `promptbench/prompteval/efficient_eval.py`
- Code Reference: `efficient_eval()` function
```python
def efficient_eval(model, prompt_list, example_list, proj_func, budget=1000, visualize=True, pca_dim=25, method='EmbPT'):
    """
    Efficient evaluation of a model on a list of prompts and examples.
    
    Returns:
    dict: A dictionary containing the following keys:
        'full_performances' (np.ndarray): The complete list of model performance scores 
                                          for each prompt after fitting the examples.
        'quantiles' (dict): A dictionary containing the 5th, 25th, 50th, 75th, and 95th 
                            percentiles of the performance scores.
        'average' (float): The average performance score across all prompts.
        'std_dev' (float): The standard deviation of the performance scores.
    """
    # ...
    # Calculate quantiles (5th, 25th, 50th, 75th, 95th)
    percentile_list = [5, 25, 50, 75, 95]
    quantiles = np.percentile(S_hat_cov, percentile_list)
    quantiles_dict = {str(k): v for k, v in zip(percentile_list, quantiles)}

    # Calculate the average
    average = np.mean(S_hat_cov)
    # Calculate the standard deviation
    std_dev = np.std(S_hat_cov)
```
Computes intrinsic statistical properties of model performance (quantiles, average, standard deviation) without comparing against external references for all examples. Uses limited labeled samples to build a statistical model, then estimates performance for unseen prompts based on embeddings and observed patterns, representing reference-free assessment of prompt quality.

Evidence 3: PromptEval Method Description
- File: `README.md`
- Code Reference: Description of PromptEval
```
Efficient multi-prompt evaluation: We integrated the efficient multi-prompt evaluation method [PromptEval](https://arxiv.org/abs/2405.17202) [8]. This method uses the performance of LLMs on a small amount of data to build an IRT-like model. This model is then used to predict the performance of LLMs on unseen data. Tests on MMLU, BBH, and LMentry show that this method requires sampling only 5% of the data to reduce the error between estimated and actual performance to around 2%.
```
Documentation confirms PromptEval is a reference-free method that predicts performance on unseen data without requiring explicit labels for all examples. Measures intrinsic quality based on statistical modeling from limited observations, requiring only 5% of labeled data to estimate full performance.