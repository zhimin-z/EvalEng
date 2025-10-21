# Evaluator Categories

[Algorithmic, ML-based, Human]

## Detailed Analysis

### Algorithmic

Evidence 1: Exact string matching for objective questions
- File: `Bench/OBJ_score_evaluation.py`
- Function: `count_score()`
- Code Reference:
```python
def count_score(total_score, correct_score, item):
    total_score += len(item["standard_answer"])*item['score']
    for j in range(len(item["standard_answer"])):
        if item["model_answer"][j] == item["standard_answer"][j]:
            correct_score += item['score']
    return total_score, correct_score
```
This function performs exact string matching between model answers and standard answers for objective questions. It uses rule-based comparison to calculate scores, which is a deterministic algorithmic approach that requires no ML models or human judgment—answers are either exactly correct or incorrect based on string equality.

Evidence 2: Rule-based partial credit system for Physics
- File: `Bench/OBJ_score_evaluation.py`
- Function: `obj_score_eval()`
- Code Reference:
```python
if key == 'Physics':
    t_score += len(item['standard_answer'])*item['score']
    # Fully correct: 6 points; Partially correct: 3 points; Incorrect: 0 points. 
    for j in range(len(item['model_answer'])):
        if item['model_answer'][j] == item['standard_answer'][j]:
            c_score += 6
        else:
            is_error = 0
            for z in item['model_answer'][j]:
                if z not in item['standard_answer'][j]:
                    is_error = 1
                    break
            c_score += 0 if is_error else 3
```
This implements a custom rule-based partial credit system for Physics questions using string matching and logical rules to assign scores (fully correct: 6 points, partially correct: 3 points, incorrect: 0 points). The algorithmic nature is evident in the predetermined scoring logic that evaluates answer components through deterministic string containment checks without requiring external judgment.

Evidence 3: Regex-based answer extraction
- File: `Bench/bench_function.py`
- Function: `extract_choice_answer()`
- Code Reference:
```python
def extract_choice_answer(model_output, question_type, answer_lenth=None):
    if question_type == 'single_choice':
        model_answer = []
        temp = re.findall(r'[A-D]', model_output[::-1])
        if len(temp) != 0:
            model_answer.append(temp[0])
```
Uses regex pattern matching to extract answers from model outputs. This is a rule-based algorithmic approach for answer extraction before scoring, operating purely on pattern recognition without semantic understanding or learned models.

Evidence 4: Statistical aggregation for subjective scores
- File: `Bench/SUB_score_evaluation.py`
- Function: `sub_score_eval()`
- Code Reference:
```python
for question in data['example']:
    q_num += 1
    score_list = [score for score in question[correction_score_type] if score is not None]
    if len(score_list) == 0:
        continue
    t_score += question['score']
    c_score += round(mean([score for score in question[correction_score_type] if score is not None]), 2)
```
Uses statistical mean calculation to aggregate scores for subjective questions. This is an algorithmic metric (statistical function) applied to evaluation results, demonstrating deterministic mathematical operations rather than learned or human-based judgment.

---

### ML-based

Evidence 1: GPT-4 as teacher model for grading
- File: `Bench/subjective_grade.py`
- Code Reference:
```python
teacher_model_name = 'gpt-4-1106-preview'
teacher_model_api = OpenaiAPI([openai_api_key], model_name=teacher_model_name, temperature=0.0, max_tokens=4096)
```
Uses GPT-4 as an LLM-as-judge to evaluate subjective question answers. This is a clear example of an ML model serving as an evaluator, leveraging the learned capabilities of a large language model to assess answer quality rather than relying on fixed rules or human annotators.

Evidence 2: LLM-based subjective grading function
- File: `Bench/bench_function.py`
- Function: `subjective_grade()`
- Code Reference:
```python
def subjective_grade(
        teacher_model_api, 
        teacher_model_name, 
        keyword, 
        zero_shot_prompt_text,
        w_marking_criterion,
        teacher_prompt_template, 
        result_directory, 
        marking_criterion_directory: None
        ):
    # ... 
    model_correction = teacher_model_api(zero_shot_prompt_text, content)
    pattern = r"【总分】\s*(?:.*=)?\s*(\d+(\.\d*)?)\s*分"  # 匹配整数或浮点数
    matches = re.findall(pattern, model_correction)
    model_correction_score = [float(match[0]) for match in matches]
```
This function invokes a teacher LLM (GPT-4) to grade subjective responses by passing questions, standard answers, and model outputs to the LLM, which returns scored evaluations. The scores are extracted from the LLM's response. This demonstrates ML-based evaluation where the model applies learned reasoning to assess answer quality, with the only algorithmic component being the score extraction via regex.

Evidence 3: Documentation of LLM-as-a-Judge approach
- File: `README.md`
- Code Reference:
```markdown
由于人工批改的高昂成本，我们提供了LLM-as-a-Judge脚本，利用GPT-4-turbo为模型的主观题打分。
```
(Translation: "Due to the high cost of manual grading, we provide LLM-as-a-Judge scripts that use GPT-4-turbo to score the model's subjective questions.")

Explicit documentation confirms the use of an LLM model (GPT-4-turbo) as an evaluator for subjective questions. This establishes the intentional design choice to use ML-based evaluation as a scalable alternative to human grading, positioning the LLM as a learned evaluator rather than a rule-based system.

---

### Human

Evidence 1: Human scoring mode in evaluation script
- File: `Bench/SUB_score_evaluation.py`
- Code Reference:
```python
parser.add_argument('--mode', type=str, choices=['human', 'model'])
# ...
correction_score_type = 'correction_score' if mode == 'human' else 'model_correction_score'
```
The evaluation script explicitly supports a "human" mode where human-provided correction scores are used instead of model-generated scores. This programmatic distinction demonstrates that the harness was designed to accommodate human evaluators, with their judgments stored separately from ML-based scores and selectable at runtime.

Evidence 2: Acknowledgment of human evaluators
- File: `README.md`
- Code Reference:
```markdown
## 致谢
我们非常感谢上海市曹杨第二中学的老师们，他们负责了GAOKAO-Bench主观题部分的评分。
```
(Translation: "We are very grateful to the teachers of Shanghai Caoyang No. 2 High School, who were responsible for scoring the subjective questions in GAOKAO-Bench.")

This explicitly acknowledges human teachers who manually evaluated subjective question responses, confirming human evaluation as part of the harness. The involvement of subject-matter expert teachers adds domain expertise to the evaluation, distinguishing this from purely automated assessment methods.

Evidence 3: Documentation of manual grading methodology
- File: `README.md`
- Code Reference:
```markdown
对客观题采用基于规则的答案抽取方式，对主观题采取人工评阅的方式
```
(Translation: "For objective questions, rule-based answer extraction is used; for subjective questions, manual grading is adopted.")

States that human manual grading was used for subjective questions in the benchmark evaluation. This establishes human evaluation as the primary methodology for subjective assessment, with LLM-as-a-judge serving as a cost-effective alternative rather than the original gold standard approach.