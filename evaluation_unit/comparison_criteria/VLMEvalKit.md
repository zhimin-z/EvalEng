## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, Comparative Baseline, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: VQA Answer Processing
- File: `vlmeval/dataset/utils/vqa_eval.py`
- Code Reference: `process_line()` function
```python
def process_line(line, method='vqa_score'):
    ret = {}
    if istype(line['answer'], list):
        answers = eval(line['answer'])
    else:
        answers = [line['answer']]
```
Loads explicit answer labels from the `line['answer']` field in datasets. These predetermined correct answers are extracted for comparison against model predictions in VQA evaluation.

Evidence 2: P-Level Task Ground Truth
- File: `vlmeval/dataset/mmifeval.py`
- Code Reference: Ground truth answer loading (Lines 280-283)
```python
pt = generate_eval_pt_p_level(item["question"], item["prediction"], json.loads(item["answer"]))
```
Loads ground truth answers from `item["answer"]` for P-Level tasks. These explicit reference answers provide comparison targets for evaluating model predictions.

Evidence 3: Mathematical Answer Comparison
- File: `vlmeval/dataset/utils/bmmr_grade.py`
- Code Reference: `math_equal()` function (Line 82)
```python
def math_equal(
    prediction: Union[bool, float, str],
    reference: Union[float, str],
    ...
) -> bool:
```
Compares predictions against explicit reference answers. The `reference` parameter contains ground truth values for mathematical problems, providing static comparison targets.

Evidence 4: LaTeX Expression Evaluation
- File: `vlmeval/dataset/utils/physics_eval_utils.py`
- Code Reference: `is_equiv()` function
```python
def is_equiv(model, expr1: str, expr2: str, verbose: bool = False) -> dict:
    result_data = {
        "input_expressions": {"expr1": expr1, "expr2": expr2},
```
Compares model outputs against explicit correct LaTeX expressions. Ground truth answers are stored in dataset fields and used for direct comparison with model-generated mathematical expressions.

---

### Behavioral Specification

Evidence 1: Code Test Case Execution
- File: `vlmeval/dataset/utils/megabench/scoring/program_judge.py`
- Code Reference: `CodeTester` class (Lines 53-119)
```python
class CodeTester:
    def __init__(self, user_code, test_cases, timeout=2, verbose=True):
        self.user_code = user_code
        self.test_cases = test_cases
```
- Code Reference: `run_user_code()` method
```python
def run_user_code(self, input_data):
    input_str = "\n".join(input_data) + "\n"
    output_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=self.target, args=(output_queue, input_str)
    )
```
Executes model-generated code against test cases dynamically. The `evaluate_test_case()` method validates outputs against expected results through runtime execution, providing behavioral specification for code correctness.

Evidence 2: Constraint Validation Functions
- File: `vlmeval/dataset/utils/mmif/function_and_compare.py`
- Code Reference: Verification functions
```python
def check_whether_response_paragraph_number_in_range(
    response: str, lower_bound: int, upper_bound: int
) -> bool:
```
Implements executable specifications checking structural properties of outputs. These verification functions validate model outputs against behavioral constraints rather than static labels.

Evidence 3: Rule-Based Constraint Verification
- File: `vlmeval/dataset/mmifeval.py`
- Code Reference: Dynamic constraint validation (Lines 301-317)
```python
for constraint in constraint_other:
    if constraint["judge"]["method"] == "rule_based":
        for func_dict in constraint["judge"]["verify_funcs"]:
            func = globals()[func_dict["func"]]
            judge_result = func(item["prediction"], *func_dict["params"])
```
Dynamically calls verification functions to validate model outputs against functional requirements. This applies executable specifications for behavioral validation of text generation tasks.

Evidence 4: OCR Metric Validation
- File: `vlmeval/dataset/utils/ocrbrnch_v2_eval.py`
- Code Reference: `spotting_evaluation()` function (Line 204)
Validates text spotting outputs through functional correctness checking. Test cases validate behavioral properties of OCR model outputs beyond static comparison.

---

### Comparative Baseline

Evidence 1: Alternative Prediction Comparison
- File: `vlmeval/dataset/mmifeval.py`
- Code Reference: Comparative baseline usage (Lines 318-328)
```python
for constraint in constraint_other:
    if constraint["judge"]["method"] == "cmp_gpt":
        del_cons_prediction = aux_data_dict[item["id"]][constraint["key"]]
        pt = generate_cmp_pt(constraint["value"], item["prediction"], del_cons_prediction)
```
Uses predictions without constraints as comparison baseline. The `aux_data_dict` stores alternative model predictions for comparative evaluation, enabling relative quality assessment.

Evidence 2: Comparative GPT Evaluation
- File: `vlmeval/dataset/mmifeval.py`
- Code Reference: `generate_cmp_pt()` function (Lines 64-97)
```python
def generate_cmp_pt(constraint, pred_with_constraint, pred_without_constraint):
    pt = f"""
    <start of response under the constraint>
    {pred_with_constraint}
    <end of response under the constraint>
    
    <start of response without the constraint>
    {pred_without_constraint}
    <end of response without the constraint>
```
Compares constrained versus unconstrained model responses. Uses one model output as baseline to evaluate another, implementing comparative assessment where alternative predictions serve as reference points.

---

### None

Evidence 1: Word Count Validation
- File: `vlmeval/dataset/utils/mmif/function_and_compare.py`
- Code Reference: Intrinsic property checks
```python
def check_whether_response_word_count_in_range(
    response: str, lower_bound: int, upper_bound: int
) -> bool:
    response_clean = re.sub(r"[^\w\s.-]", "", response)
    word_list = response_clean.split()
    word_count = len(word_list)
    return lower_bound <= word_count <= upper_bound
```
Measures intrinsic text properties including word count, paragraph count, and sentence count without comparing to external references. These self-contained metrics assess output characteristics independently.

Evidence 2: Numeric Precision Validation
- File: `vlmeval/dataset/utils/mmif/function_and_compare.py`
- Code Reference: `check_percentage_number_precision_in_response()` (Line 228)
```python
def check_percentage_number_precision_in_response(
        response: str, precision: int) -> bool:
    pattern = r'(\d+\.\d+|\d+)\s*%'
    matches = re.findall(pattern, response)
```
Validates numeric formatting precision without external standards. This intrinsic check assesses whether percentage values meet specified precision requirements independent of ground truth comparison.

Evidence 3: Structural Pattern Checks
- File: `vlmeval/dataset/utils/mmif/function_and_compare.py`
- Code Reference: Self-contained structural validation
```python
# check_whether_each_paragraph_begin_with_certain_substring() at line 169
# check_whether_whole_response_not_contain_certain_substrings() at line 145
```
Checks internal consistency and structural patterns without external references. These functions validate formatting and organizational properties as intrinsic quality measures.

Evidence 4: Format Extraction Validation
- File: `vlmeval/dataset/utils/ocrbrnch_v2_eval.py`
- Code Reference: Multiple choice answer extraction (Lines 69-76)
```python
predict = ''.join(c for c in data_item["predict"] if c.isalpha())
```
Validates response structure independently through format extraction. This reference-free check assesses whether outputs conform to expected structural patterns without comparing to ground truth content.