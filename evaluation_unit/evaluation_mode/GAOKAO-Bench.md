## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Direct answer comparison through string equality
- File: `Bench/OBJ_score_evaluation.py`
- Function: `count_score()` and `obj_score_eval()`
- Code Reference:
```python
def count_score(total_score, correct_score, item):
    total_score += len(item["standard_answer"])*item['score']
    for j in range(len(item["standard_answer"])):
        if item["model_answer"][j] == item["standard_answer"][j]:
            correct_score += item['score']
    return total_score, correct_score
```
The harness evaluates objective questions by comparing model-generated answers with standard answers through direct text/pattern matching without executing any generated code. This function directly compares `model_answer` with `standard_answer` using string equality checks.

Evidence 2: Pattern matching and regex-based answer extraction
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
    elif question_type == 'multi_question_choice':
        model_answer = []
        temp = re.findall(r"【答案】\s*[:：]*\s*[A-Z]", model_output)
        # ... pattern matching logic
```
The harness extracts and validates model outputs using pattern matching and regex, which is syntactic analysis of text. This performs format validation and pattern matching on model outputs to extract structured answers.

Evidence 3: String parsing for correction answers
- File: `Bench/bench_function.py`
- Function: `extract_correction_answer()`
- Code Reference:
```python
def extract_correction_answer(model_output):
    model_answer = []
    start_idx = model_output.find('【答案】')
    end_idx = model_output.find('<eoa>')
    if start_idx >= 0:
        if end_idx >= 0:
            answer = model_output[start_idx:end_idx]
        else:
            answer = model_output[start_idx:]
    # ... string parsing logic
```
The harness performs string parsing to extract correction answers from model outputs. This is pure text parsing and structure validation without any execution.

Evidence 4: Score-based evaluation without execution
- File: `Bench/SUB_score_evaluation.py`
- Function: `sub_score_eval()`
- Code Reference:
```python
def sub_score_eval(sub_output_dir: str, mode: str) -> None:
    correction_score_type = 'correction_score' if mode == 'human' else 'model_correction_score'
    # ...
    for question in data['example']:
        score_list = [score for score in question[correction_score_type] if score is not None]
        if len(score_list) == 0:
            continue
        t_score += question['score']
        c_score += round(mean([score for score in question[correction_score_type] if score is not None]), 2)
```
The harness evaluates subjective questions by comparing scores, not by executing model outputs. This calculates statistics from pre-existing scores without executing anything.

Evidence 5: LLM-as-a-Judge with text-based score extraction
- File: `Bench/subjective_grade.py`
- Function: GPT-4 as grader
- Code Reference:
```python
pattern = r"【总分】\s*(?:.*=)?\s*(\d+(\.\d*)?)\s*分"  # 匹配整数或浮点数
matches = re.findall(pattern, model_correction)
model_correction_score = [float(match[0]) for match in matches]
```
The harness uses GPT-4 to grade subjective answers by inspecting text outputs. This extracts scores from GPT-4's text output using regex pattern matching, which is static text analysis.