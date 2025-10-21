# GAOKAO-Bench - Stage 4 (EVALUATE) Evaluation

## Summary
GAOKAO-Bench is a specialized evaluation framework for testing large language models on Chinese National College Entrance Examination (GAOKAO) questions. It has minimal evaluation infrastructure, focusing primarily on rule-based answer extraction for objective questions and LLM-as-judge for subjective questions. The framework lacks comprehensive metric computation, validation, and statistical analysis features expected of a modern evaluation harness.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Basic answer extraction with regex patterns exists but no validation framework. Only format checking via regex in `bench_function.py::extract_choice_answer()` and `extract_correction_answer()`. No schema validation, policy compliance checks, or normalization beyond simple regex matching. |
| S4F2: Metric Computation | 1 | Extremely limited metric library. Only exact match accuracy for objective questions (`OBJ_score_evaluation.py`) and GPT-4 scoring for subjective questions (`subjective_grade.py`). No standard NLP metrics (ROUGE, BLEU, etc.), no per-sample scoring APIs, no extensibility framework. |
| S4F3: Evaluator Models | 2 | Basic LLM-as-judge implementation exists for subjective questions using GPT-4-turbo (`subjective_grade.py`). Has configurable prompts (`Sub_Grade_Prompt_wo_marking_criterion.json`) and captures scores via regex. However, no ensemble support, no rationale capture beyond raw output, no calibration mechanisms, limited to single evaluator. |
| S4F4: Multi-Modal Scoring | 0 | Text-only framework. No support for vision-language, audio-text, or video understanding metrics. All questions are text-based Chinese exam questions. |
| S4F5: Aggregate Statistics | 1 | Basic aggregation only. Computes totals and scoring rates by subject (`OBJ_score_evaluation.py::score_dict`, `SUB_score_evaluation.py`). No percentiles, confidence intervals, distribution analysis, significance testing, or ranking systems. Simple mean calculation in `SUB_score_evaluation.py` using `statistics.mean()`. |

## Detailed Analysis

### S4F1: Output Validation and Normalization (Rating: 1)

Evidence:

The framework has minimal validation, only basic regex-based answer extraction:

```python
# Bench/bench_function.py
def extract_choice_answer(model_output, question_type, answer_lenth=None):
    if question_type == 'single_choice':
        model_answer = []
        temp = re.findall(r'[A-D]', model_output[::-1])
        if len(temp) != 0:
            model_answer.append(temp[0])
```

Limitations:
- No format validation beyond regex patterns
- No schema validation against expected output format
- No policy compliance checks (harmful content, length constraints)
- No sanity checks (logical consistency, anomaly detection)
- No robust normalization (only extracts answers via regex)
- No handling of malformed JSON/XML
- Failed extractions silently return empty lists

Why not 0: At least has basic regex-based extraction for multiple question types (single choice, multi-choice, five-out-of-seven, etc.)

### S4F2: Task-Specific Metric Computation (Rating: 1)

Evidence:

Only two metrics are computed:

1. Exact match for objective questions:
```python
# Bench/OBJ_score_evaluation.py
def count_score(total_score, correct_score, item):
    total_score += len(item["standard_answer"])*item['score']
    for j in range(len(item["standard_answer"])):
        if item["model_answer"][j] == item["standard_answer"][j]:
            correct_score += item['score']
    return total_score, correct_score
```

2. LLM-as-judge scoring for subjective questions:
```python
# Bench/subjective_grade.py
pattern = r"【总分】\s*(?:.*=)?\s*(\d+(\.\d*)?)\s*分"
matches = re.findall(pattern, model_correction)
model_correction_score = [float(match[0]) for match in matches]
```

Limitations:
- No standard NLP metrics (BLEU, ROUGE, METEOR, BERTScore)
- No classification metrics (precision, recall, F1, AUC-ROC)
- No retrieval metrics (P@k, NDCG, MRR)
- No per-sample metric API (scores are aggregated, individual scores not easily accessible)
- No custom metric framework
- No vectorized/efficient computation
- Scoring logic hardcoded in evaluation scripts

Why not 0: At least computes accuracy for objective questions and has LLM-based scoring for subjective questions.

### S4F3: Evaluator Model Integration (Rating: 2)

Evidence:

The framework has a basic LLM-as-judge implementation:

```python
# Bench/subjective_grade.py
teacher_model_api = OpenaiAPI([openai_api_key], model_name=teacher_model_name, temperature=0.0, max_tokens=4096)

# Configurable prompts
with open("./Sub_Grade_Prompt_wo_marking_criterion.json", "r") as f:
    data = json.load(f)['examples']
```

Example prompt structure:
```json
{
    "type": "subjective",
    "keyword": "2010-2022_Geography_Open-ended_Questions",
    "prefix_prompt": "你是一名高中地理老师，正在批改高考地理试卷。请根据下面的【题目】、【分析过程】、【标准答案】、【分值】、【学生分析与答案】，对【学生分析与答案】进行判分并给出理由。"
}
```

Score extraction:
```python
pattern = r"【总分】\s*(?:.*=)?\s*(\d+(\.\d*)?)\s*分"
matches = re.findall(pattern, model_correction)
model_correction_score = [float(match[0]) for match in matches]
```

Strengths:
- Configurable judge prompts for different subjects
- Multiple attempts (up to 3) if scoring fails
- Captures full model output for reasoning
- Subject-specific prompts

Limitations:
- Only single evaluator (GPT-4-turbo)
- No ensemble support
- No multi-aspect scoring (single score only)
- No calibration mechanisms
- Rationale not structured (just raw text)
- No disagreement handling
- No specialized evaluator models (RAGAS, G-Eval, Prometheus)

Why 2 not 3: Has configurable LLM judge with prompt templates, but lacks ensemble, multi-aspect scoring, and advanced features.

### S4F4: Multi-Modal Scoring Protocols (Rating: 0)

Evidence:

The framework is exclusively text-based:

```python
# All data files in Data/ directory are JSON with text fields only
# Example from Data/Objective_Questions/2010-2022_Math_I_MCQs.json structure:
{
    "question": "若 $z=-1+\\sqrt{3} \\mathrm{i}$, 则...",
    "answer": ["C"],
    "analysis": "【详解】..."
}
```

No code references to:
- Image processing
- Vision-language models (CLIP, VQA)
- Audio processing (WER, MOS)
- Video understanding
- Multi-modal artifact handling

Why 0: Completely text-only framework with no multi-modal support.

### S4F5: Aggregate Statistics and Cross-Model Comparison (Rating: 1)

Evidence:

Basic aggregation only:

```python
# Bench/OBJ_score_evaluation.py
score_dict = {
    "total_score": 0.0,
    "correct_score": 0.0,
    "scoring_rate": 0.0,
    "subject": {
        "English": {
            'total_score': 0.0,
            'correct_score': 0.0,
            'scoring_rate': 0.0,
        }
    }
}

# Simple rate calculation
s_rate = round(c_score / t_score, 3)
```

For subjective questions:
```python
# Bench/SUB_score_evaluation.py
from statistics import mean

c_score += round(mean([score for score in question[correction_score_type] if score is not None]), 2)
```

Final score merging:
```python
# Bench/merge_OBJ_SUB_score.py
result_dict['Liberal-Arts_Total_score'] = 0
for s in ['Chinese', 'English', 'Liberal-Arts-Math', ...]:
    result_dict[s]['total_score'] = round(result_dict[s]['Subjective_score'] + result_dict[s]['Objective_score'], 3)
```

Limitations:
- Only mean and totals computed
- No standard deviation, variance, percentiles
- No confidence intervals
- No distribution analysis (histograms, density plots)
- No outlier detection
- No significance testing (t-test, Wilcoxon)
- No bootstrap methods
- No ranking systems (Elo, TrueSkill)
- No weighted metrics or stratified statistics
- No cross-model comparison infrastructure

Why not 0: At least computes basic aggregates (mean, total, rate) by subject and overall.

## Key Strengths

1. Domain-specific focus: Well-designed for Chinese exam evaluation
2. LLM-as-judge implementation: Basic but functional subjective question scoring
3. Subject organization: Clear structure by subject and question type
4. Configurable prompts: JSON-based prompt templates for different subjects

## Critical Gaps

1. No metric library: Missing all standard NLP metrics
2. No validation framework: Only basic regex extraction
3. No statistical analysis: No distribution analysis, significance testing, or CI
4. No per-sample API: Scores are aggregated, individual metrics hard to access
5. No extensibility: No plugin system for custom metrics
6. Single evaluator only: No ensemble or multi-evaluator support
7. Text-only: No multi-modal capabilities

## Recommendations

To improve from total 5/15 to a more comprehensive framework:

1. Add metric library: Integrate standard metrics (ROUGE, BLEU, BERTScore)
2. Implement validation: Add schema validation, format checking, normalization
3. Add statistical analysis: Compute percentiles, CI, distributions, significance tests
4. Create per-sample API: Allow accessing individual scores before aggregation
5. Build extensibility: Create plugin system for custom metrics and evaluators
6. Add ensemble support: Allow multiple evaluators with aggregation strategies