## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Predefined metric functions for deterministic assessment
- File: `trustllm_pkg/trustllm/utils/metrics.py`
- Code Reference:
```python
calculate_toxicity(data, key='toxicity')
RtA(data, key='eval_res', refusal_label="LABEL_0", ...)
pearson_correlation(data)
count_agreement(data)
count_stereotype_recognition(data)
count_advglue(data)
p_value(data, attribute, res_column='res')
calculate_cosine_similarity(embeddings)
average_cosine_similarity(embeddings)
count_yes_no(eval_res)
```
This file contains numerous algorithmic metric functions that implement predefined mathematical and statistical operations. The `calculate_toxicity()` function calculates average and maximum toxicity values using basic arithmetic operations. The `RtA()` function calculates "Refusal to Answer" ratio using counting and division. The `pearson_correlation()` function computes Pearson correlation coefficient using covariance and standard deviation formulas. Additional functions include `count_agreement()` for counting agreement instances using keyword matching, `count_stereotype_recognition()` for pattern matching, `count_advglue()` for adversarial GLUE benchmark performance with accuracy calculations, `p_value()` for chi-square test of independence, `calculate_cosine_similarity()` and `average_cosine_similarity()` for embedding comparison, and `count_yes_no()` for response counting using string matching. These are predefined mathematical and statistical functions that score model outputs based on computational rules, formulas, and pattern matching algorithms. They are deterministic and reproducible, providing consistent assessment through established computational measures.

Evidence 2: Task evaluation methods using algorithmic metrics
- File: `trustllm_pkg/trustllm/task/truthfulness.py`
- Function: `eval_single_source()`, `internal_eval()`
- File: `trustllm_pkg/trustllm/task/robustness.py`
- Function: `advglue_eval()`, `advinstruction_eval()`, `ood_generalization()`
- File: `trustllm_pkg/trustllm/task/privacy.py`
- Function: `extract_and_map_ConfAIDe()`, `ConfAIDe_eval()`, `leakage_eval()`
- Code Reference:
```python
# truthfulness.py
eval_single_source()  # Uses sklearn's classification_report() for macro F1 score
internal_eval()  # Aggregates accuracy scores across datasets
# Pattern matching for answer extraction (regex operations)

# robustness.py
advglue_eval()  # Uses keyword matching and regex patterns with statistical aggregation
advinstruction_eval()  # Computes average cosine similarity
ood_generalization()  # Uses sklearn's f1_score() function

# privacy.py
extract_and_map_ConfAIDe()  # Uses regex to extract numerical scores and mappings
ConfAIDe_eval()  # Calculates Pearson correlation
leakage_eval()  # Uses string matching and ratio calculations
```
Multiple task files implement algorithmic evaluation methods across different benchmark dimensions. In `truthfulness.py`, the `eval_single_source()` function uses sklearn's `classification_report()` for macro F1 score calculation, while `internal_eval()` aggregates accuracy scores across datasets and uses pattern matching for answer extraction through regex operations. In `robustness.py`, `advglue_eval()` uses keyword matching and regex patterns with statistical aggregation, `advinstruction_eval()` computes average cosine similarity, and `ood_generalization()` uses sklearn's `f1_score()` function. In `privacy.py`, `extract_and_map_ConfAIDe()` uses regex to extract numerical scores and mappings, `ConfAIDe_eval()` calculates Pearson correlation, and `leakage_eval()` uses string matching and ratio calculations. These methods implement algorithmic scoring based on statistical formulas, string matching algorithms, exact match criteria, and mathematical operations on model outputs, ensuring consistent and reproducible evaluation through established computational measures.

---

### ML-based

Evidence 1: Pre-trained transformer model for text classification
- File: `trustllm_pkg/trustllm/utils/longformer.py`
- Class: `HuggingFaceEvaluator`
- Code Reference:
```python
class HuggingFaceEvaluator:
    def __init__(self, model_name='LibrAI/longformer-harmful-ro', device=None, save_dir='saved_evaluations'):
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.classifier = pipeline('text-classification', model=model, tokenizer=tokenizer, device=self.device)
```
The `HuggingFaceEvaluator` class loads a pre-trained Longformer transformer model from HuggingFace that performs text classification on model outputs. It initializes the model using `AutoModelForSequenceClassification` and creates a text classification pipeline. This evaluator is used extensively across multiple evaluation tasks: in `trustllm_pkg/trustllm/task/safety.py` through the `SafetyEval` class methods, in `trustllm_pkg/trustllm/task/fairness.py` through `FairnessEval.stereotype_query_eval()`, in `trustllm_pkg/trustllm/task/privacy.py` through `PrivacyEval.awareness_query_eval()`, and in `trustllm_pkg/trustllm/task/ethics.py` through `EthicsEval.explicit_ethics_eval()`. This is a machine learning model that uses learned neural network parameters to evaluate whether responses are harmful or refuse to answer, leveraging learned representations for nuanced assessment that captures semantic and contextual quality dimensions that algorithmic methods cannot reliably measure.

Evidence 2: LLM-as-judge implementation using GPT models
- File: `trustllm_pkg/trustllm/utils/gpt_auto_eval.py`
- Class: `AutoEvaluator`
- Function: `get_res()`
- Code Reference:
```python
@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(6))
def get_res(string, model='gpt-4-1106-preview', temperature=0, message=None):
    if trustllm.config.azure_openai:
        client = AzureOpenAI(...)
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": string}],
            temperature=temperature
        )
    else:
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(model=model, messages=message, temperature=temperature)
    response = stream.choices[0].message.content
    return response

class AutoEvaluator:
    def evaluate(self, data, task, resume=False, progress_filename='auto_eval.json', concat=True):
        # Uses GPT-4 to evaluate model outputs based on task-specific prompts
```
The `AutoEvaluator` class implements an LLM-as-judge evaluation system using GPT-4 or GPT-3.5-turbo to assess model outputs on benchmark tasks. The `get_res()` function creates API calls to OpenAI or Azure OpenAI services with retry logic, sending evaluation prompts and receiving model judgments. This evaluator is used extensively across multiple tasks: in `truthfulness.py` for `eval_internal_squad()`, `eval_internal_adv()`, `eval_internal_hotpot()` to evaluate answer correctness, `advfact_eval()` for factuality correction judgment, and `sycophancy_eval()` for preference evaluation; in `ethics.py` for `implicit_ethics_eval()` to classify ethical judgments and `other_awareness_eval()` for awareness evaluation; in `fairness.py` for `stereotype_agreement_eval()` and `stereotype_recognition_eval()` to assess stereotype-related responses; and in `robustness.py` for `ood_generalization()` to evaluate diagnosis correctness. The system uses task-specific prompts from `trustllm/config.py` (task_prompt dictionary) and generates evaluative judgments through model inference, leveraging the learned capabilities of large language models to capture nuanced semantic quality that deterministic metrics cannot assess.

Evidence 3: Neural network-based embedding model for semantic representation
- File: `trustllm_pkg/trustllm/utils/embedder.py`
- Class: `DataEmbedder`
- Function: `get_embeddings()`
- Code Reference:
```python
class DataEmbedder:
    @retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(6))
    def get_embeddings(self, string, embedding_model='text-embedding-ada-002'):
        if trustllm.config.azure_openai:
            client = AzureOpenAI(...)
            response = client.embeddings.create(model=model, input=string)
        else:
            client = OpenAI(api_key=api_key)
            response = client.embeddings.create(model=embedding_model, input=string)
        return response.data[0].embedding
```
The `DataEmbedder` class uses OpenAI's text-embedding-ada-002 model, a neural network-based embedding model, to generate semantic representations of model outputs. The `get_embeddings()` function creates API calls to OpenAI or Azure OpenAI services with retry logic to obtain dense vector embeddings that capture semantic meaning. This ML-based component is used in evaluation tasks within `truthfulness.py` where `sycophancy_eval()` with eval_type='persona' uses embeddings for similarity calculation, and in `robustness.py` where `advinstruction_eval()` uses embeddings for cosine similarity evaluation. While the embeddings are subsequently processed using algorithmic similarity metrics (cosine similarity), the embedding generation itself is performed by a trained neural network that learns to represent semantic content in vector space, leveraging learned representations to enable nuanced semantic assessment that captures contextual relationships between model outputs.

Evidence 4: ML-based toxicity detection service
- File: `trustllm_pkg/trustllm/utils/perspective.py`
- Class: `PerspectiveEval`
- Function: `get_toxicity_value()`
- Code Reference:
```python
class PerspectiveEval:
    def get_toxicity_value(self, sentence):
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=self.api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )
        analyze_request = {
            'comment': {'text': sentence},
            'requestedAttributes': {'TOXICITY': {}}
        }
        response = client.comments().analyze(body=analyze_request).execute()
        return response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']
```
The `PerspectiveEval` class integrates Google's Perspective API, a machine learning-based toxicity detection service that uses trained neural networks to score text for toxicity and other attributes. The `get_toxicity_value()` function sends text to the Perspective API through Google's Comment Analyzer service and retrieves toxicity scores ranging from 0 to 1. This evaluator is used in `trustllm_pkg/trustllm/task/safety.py` through the `SafetyEval.toxicity_eval()` method to assess the safety of model-generated outputs. Perspective API represents an ML-based evaluator that uses learned models trained on large datasets of human-annotated toxic content to provide nuanced toxicity assessment, capturing contextual and semantic qualities that simple keyword-based algorithmic approaches cannot reliably detect.