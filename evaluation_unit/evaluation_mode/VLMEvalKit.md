## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Multiple text processing and comparison functions
- File: `vlmeval/dataset/utils/vqa_eval.py`
- Functions: `process_answer()`, `anls_compute()`, `relaxed_correctness()`, `process_line()`
- Code Reference:
```python
def process_line(line, method='vqa_score'):
    ret = {}
    if istype(line['answer'], list):
        answers = eval(line['answer'])
    else:
        answers = [line['answer']]
    if method == 'vqa_score':
        ret['gt'] = [process_answer(x) for x in answers]
        ret['pred'] = process_answer(line['prediction'])
        # ... matching logic
    elif method == 'anls':
        ret['gt'] = answers
        ret['pred'] = line['prediction']
        ret['match'] = [anls_compute(x, ret['pred']) for x in ret['gt']]
```
These functions perform direct text comparison and similarity scoring on model outputs without executing any generated code or artifacts. They validate format, compute text-based metrics, and check patterns in responses through punctuation handling, digit/article processing, Levenshtein distance computation, and various accuracy methods including VQA score, ANLS, and relaxed accuracy.

Evidence 2: Mathematical expression evaluation
- File: `vlmeval/dataset/utils/bmmr_grade.py`
- Functions: `math_equal()`, `symbolic_equal()`, `extract_answer()`, `format_intervals()`
- Code Reference:
```python
def math_equal(
    prediction: Union[bool, float, str],
    reference: Union[float, str],
    include_percentage: bool = True,
    tolerance: float = 1e-4,
    timeout: float = 10.0,
    pi: float = math.pi
) -> bool:
    # ... numerical and string comparison
    # 2. symbolic equal
    return symbolic_equal(prediction, reference, tolerance, timeout)

def symbolic_equal(a, b, tolerance, timeout=10.0):
    def _parse(s):
        for f in [parse_expr, parse_latex]:
            try:
                with time_limit(timeout):
                    return f(s)
            except Exception:
                pass
        return s
    # ... symbolic comparison using SymPy
```
This performs static analysis of mathematical expressions by parsing and comparing them symbolically using SymPy, without executing model-generated code. It validates mathematical correctness through symbolic manipulation, handling LaTeX expressions, boxed answers, and interval notation with numerical tolerance checking.

Evidence 3: Physics expression evaluation
- File: `vlmeval/dataset/utils/physics_eval_utils.py`
- Functions: `extract_final_answer()`, `is_equiv()`, `_preprocess_latex()`, `_standardize_expr()`
- Code Reference:
```python
def is_equiv(model, expr1: str, expr2: str, verbose: bool = False) -> dict:
    # ... preprocessing
    try:
        expr1_sympy = _standardize_expr(parse_latex(expr1_core))
        expr2_sympy = _standardize_expr(parse_latex(expr2_core))
        sympy_result = simplify(expr1_sympy - expr2_sympy) == 0 or expr1_sympy.equals(expr2_sympy)
    except Exception as e:
        # ... LLM fallback
```
Validates physics expressions through LaTeX parsing and symbolic comparison using SymPy. The primary evaluation is through static symbolic manipulation, with LLM used only as a fallback judge. Expressions are preprocessed, standardized, and compared through symbolic simplification.

Evidence 4: OCR and document parsing evaluation
- File: `vlmeval/dataset/utils/ocrbrnch_v2_eval.py`
- Function: `process_predictions()`
- Code Reference:
```python
def process_predictions(predict_file):
    teds = TEDS(n_jobs=32)
    # ... various evaluation branches
    elif data_item["type"] == "table parsing en":
        pred_table_html = convert_markdown_table_to_html(data_item["predict"])
        gt_table_html = convert_markdown_table_to_html(data_item["answers"][0])
        data_item["score"] = teds.evaluate(pred_table_html, gt_table_html)
```
Performs static structural analysis of OCR outputs, tables, charts, and documents by comparing parsed structures without executing any generated code. Validates format, structure, and content similarity using TEDS metric for table structure comparison, text metrics (BLEU, METEOR, F-measure), and IoU calculations for bounding boxes.

Evidence 5: Constraint checking functions
- File: `vlmeval/dataset/utils/mmif/function_and_compare.py`
- Functions: `check_whether_response_paragraph_number_in_range()`, `check_whether_response_sentence_number_in_range()`, `check_whether_response_word_count_in_range()`, `check_whether_each_keyword_in_list_metioned_in_range()`, `check_percentage_number_precision_in_response()`
- Code Reference:
```python
def check_whether_response_paragraph_number_in_range(
    response: str, lower_bound: int, upper_bound: int
) -> bool:
    def clean_text(text: str) -> str:
        return "\n".join(line.strip() for line in text.splitlines()).strip()
    cleaned_response = clean_text(response)
    paragraphs = [p for p in re.split(r"\n\s*\n", cleaned_response) if p.strip()]
    actual_count = len(paragraphs)
    return lower_bound <= actual_count <= upper_bound
```
These functions perform static analysis of response structure, format, and content using regex patterns, text parsing, and counting operations without executing model outputs. They validate paragraph counts, sentence counts using NLTK, word counts, keyword frequency, and numeric precision in responses.

Evidence 6: Multiple static scoring metrics
- File: `vlmeval/dataset/utils/megabench/scoring/` directory
- Files: `exact_str_match.py`, `jaccard.py`, `set_equality.py`, `normalized_similarity_damerau_levenshtein.py`, `nbbox_iou.py`
- Code Reference:
```python
def jaccard_index(predicted: Iterable, target: Iterable) -> float:
    """Calculate the Jaccard Index."""
    return set_relevance_score(_union_denominator, predicted, target)

def calculate_iou(predicted: Iterable[Number], target: Iterable[Number]):
    """Calculate the IoU between predicted and target bounding boxes."""
    # ... IoU calculation logic
```
These metrics perform static mathematical and structural comparisons of model outputs without execution, including set operations (Jaccard index, set equality), distance metrics (Damerau-Levenshtein edit distance, string matching), and geometric calculations (bounding box IoU).

Evidence 7: MM-IFEval constraint evaluation
- File: `vlmeval/dataset/mmifeval.py`
- Functions: `judge_one_item()`, `extract_score_from_direct_gpt_resp()`, `extract_score_from_p_level_gpt_resp()`
- Code Reference:
```python
def judge_one_item(item, retry=3):
    # ... P-Level evaluation
    if item.get("tag", None) == "P-Level":
        pt = generate_eval_pt_p_level(item["question"], item["prediction"], json.loads(item["answer"]))
        gpt_resp = run_once_without_image(pt)
        score = extract_score_from_p_level_gpt_resp(gpt_resp)
    # ... C-Level evaluation with rule-based checks
    for constraint in constraint_other:
        if constraint["judge"]["method"] == "rule_based":
            # call function according to constraint["judge"]["verify_funcs"]
            func = globals()[func_dict["func"]]
            judge_result = func(item["prediction"], *func_dict["params"])
```
While this uses LLM as judge in some cases, the core evaluation includes static pattern extraction and rule-based constraint checking on model outputs. The LLM judge responses themselves are parsed using static regex patterns for P-Level and C-Level constraint evaluation.

---

### Dynamic Execution

Evidence 1: Code execution for testing
- File: `vlmeval/dataset/utils/megabench/scoring/program_judge.py`
- Class: `CodeTester`
- Code Reference:
```python
class CodeTester:
    def __init__(self, user_code, test_cases, timeout=2, verbose=True):
        self.user_code = user_code
        self.test_cases = test_cases
        self.timeout = timeout
        
    def run_user_code(self, input_data):
        input_str = "\n".join(input_data) + "\n"
        output_queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            target=self.target, args=(output_queue, input_str)
        )
        process.start()
        process.join(self.timeout)
        if process.is_alive():
            process.terminate()
            return f"ERROR: Code execution exceeded the time limit."
        # ... retrieve results
        
    def target(self, output_queue, input_str):
        # ... execute code with mocked input
        with patch("builtins.input", side_effect=input_str.splitlines()):
            with patch("sys.stdout", new=stdout):
                exec(self.user_code)
```
This explicitly executes model-generated Python code in a controlled environment with timeout protection and input/output capture. The code is run using Python's `exec()` function in isolated processes with mocked stdin/stdout, running multiple test cases against generated code and capturing outputs for comparison with expected results.

Evidence 2: Chart code execution
- File: `vlmeval/dataset/utils/chartmimic/evaluator/legend_evaluator.py`
- Class: `LegendEvaluator`
- Code Reference:
```python
class LegendEvaluator:
    def _log_legends(self, code_file):
        """Get legend objects of the code"""
        with open(code_file, 'r') as f:
            lines = f.readlines()
        code = ''.join(lines)
        
        prefix = self._get_prefix()
        suffix = self._get_suffix(output_file)
        code = prefix + code + suffix
        
        code_log_texts_file = code_file.replace(".py", "_log_legends.py")
        with open(code_log_texts_file, 'w') as f:
            f.write(code)
        
        success = run_script_safe(code_log_texts_file)
        # ... process execution results
```
This evaluator executes model-generated matplotlib/visualization code to extract and validate chart properties like legends. The generated code is modified with prefix/suffix additions, written to a file, and run as a Python script in a safe environment, with its outputs (text positions, legend content) captured for evaluation.

Evidence 3: Model inference execution
- File: `vlmeval/vlm/transcore_m.py`
- Function: `generate_inner()`
- Code Reference:
```python
def generate_inner(self, message, dataset=None):
    # ... preprocessing
    with torch.inference_mode():
        output_ids = self.model.generate(
            input_ids,
            images=image_patches,
            use_cache=True,
            stopping_criteria=[stopping_criteria],
            **self.kwargs)
    # ... postprocessing
```
While this is model execution rather than executing model-generated code, it demonstrates the dynamic execution pattern where artifacts (model predictions) are generated through runtime execution with image processing, tokenization, model forward pass with generation, and postprocessing rather than static analysis.