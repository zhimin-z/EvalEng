# Evaluator Categories

[Algorithmic, ML-based, Environmental]

## Detailed Analysis

### Algorithmic

Evidence 1: Multiple algorithmic metrics for VQA evaluation
- File: `vlmeval/dataset/utils/vqa_eval.py`
- Functions: `anls_compute()`, `levenshtein_distance()`, `relaxed_correctness()`, `process_answer()`, `hit_calculate()`
- Code Reference:
```python
anls_compute()  # Computes ANLS (Average Normalized Levenshtein Similarity) using edit distance
levenshtein_distance()  # Implements Levenshtein distance algorithm
relaxed_correctness()  # Numeric comparison with tolerance checking
process_answer()  # Text normalization and string matching
hit_calculate()  # Accuracy computation using various matching strategies
```
This file implements deterministic VQA evaluation metrics using string matching algorithms (exact match, edit distance) and numeric comparison with tolerance. The ANLS metric computes normalized Levenshtein similarity, while other functions handle text normalization and multiple matching strategies. These are computational functions that score outputs based on logical rules and mathematical formulas, fitting the Algorithmic category definition.

Evidence 2: Mathematical equivalence checking
- File: `vlmeval/dataset/utils/bmmr_grade.py`
- Functions: `math_equal()`, `symbolic_equal()`, `is_digit()`, `extract_answer()`
- Code Reference:
```python
math_equal()  # Checks numerical and symbolic equality
symbolic_equal()  # Symbolic math expression comparison using SymPy
is_digit()  # Numeric value extraction
extract_answer()  # Pattern matching for boxed expressions
```
This module checks mathematical equivalence using both numerical comparison and symbolic math operations via SymPy. It extracts numeric values and matches boxed mathematical expressions using pattern matching. These symbolic math operations and rule-based extraction methods are deterministic computational functions that fit the Algorithmic category.

Evidence 3: Multiple metric types for OCR evaluation
- File: `vlmeval/dataset/utils/ocrbrnch_v2_eval.py`
- Functions: `vqa_evaluation()`, `vqa_evaluation_case_sensitive()`, `counting_evaluation()`, `calculate_iou()`, `compute_f1_score()`, `cal_per_metrics()`
- Code Reference:
```python
vqa_evaluation()  # VQA scoring
vqa_evaluation_case_sensitive()  # Case-sensitive string matching
counting_evaluation()  # Counting accuracy
calculate_iou()  # Intersection over Union calculation
compute_f1_score()  # F1 score computation
cal_per_metrics()  # BLEU, METEOR, edit distance metrics
```
This file implements a comprehensive suite of evaluation metrics including string matching (case-sensitive and insensitive), statistical functions (F1 score, BLEU, METEOR), and mathematical computations (IoU). These deterministic metrics use established formulas and algorithms to score outputs, fitting the Algorithmic category definition.

Evidence 4: Extensive metric catalog
- File: `vlmeval/dataset/utils/megabench/metric_type.py`
- Metrics: `EXACT_STR_MATCH`, `JACCARD_INDEX`, `SET_PRECISION`, `BLEU`, `NORMALIZED_RMSE`, and multiple others
- Code Reference:
```python
EXACT_STR_MATCH  # Exact string matching
JACCARD_INDEX  # Jaccard similarity
SET_PRECISION  # Set-based precision
BLEU  # BLEU score
NORMALIZED_RMSE  # Root mean squared error
# Multiple other algorithmic metrics defined
```
This module defines a catalog of algorithmic metric types spanning string matching, set-based comparisons, NLP metrics (BLEU), and statistical measures (RMSE). These predefined metric identifiers represent deterministic computational measures that ensure consistent, reproducible evaluation through established mathematical formulas.

Evidence 5: Common scoring metrics implementation
- File: `vlmeval/dataset/utils/megabench/scoring/common/metrics.py`
- Functions: `calculate_iou()`, `jaccard_index()`, `set_precision()`, `set_recall()`, `mse()`, `point_distance()`
- Code Reference:
```python
calculate_iou()  # IoU calculation for bounding boxes
jaccard_index()  # Jaccard index implementation
set_precision() / set_recall()  # Set-based metrics
mse()  # Mean squared error
point_distance()  # Euclidean distance
```
This file implements common mathematical and statistical metrics including IoU for spatial overlap, Jaccard similarity for set comparison, MSE for error measurement, and Euclidean distance for geometric calculations. These are deterministic mathematical functions that provide reproducible assessment through established computational measures.

Evidence 6: Rule-based constraint evaluators
- File: `vlmeval/dataset/utils/mmif/function_and_compare.py`
- Functions: Multiple constraint checking functions (paragraph count, sentence count, word count), pattern matching functions using regex, numeric precision checking functions
- Code Reference:
```python
# Multiple constraint checking functions (paragraph count, sentence count, word count)
# Pattern matching functions using regex
# Numeric precision checking functions
```
This module implements rule-based evaluators that check structural constraints (text length, formatting) using regex patterns and count-based validation. These deterministic functions assess outputs against predefined rules without learned models, fitting the Algorithmic category's goal of ensuring consistent, reproducible evaluation through computational measures.

---

### ML-based

Evidence 1: OpenAI VLM judge for evaluation
- File: `vlmeval/dataset/utils/megabench/scoring/vlm_as_judge.py`
- Classes: `OpenAIVLMJudger`, `VLMJudgeScore`
- Code Reference:
```python
class OpenAIVLMJudger:
    # Uses GPT-4o as a judge model
    def query(self):
        # Calls OpenAI API to evaluate model outputs
        pass

class VLMJudgeScore:
    # ML model-based evaluation
    pass
```
This module uses GPT-4o vision-language model as a judge to evaluate open-ended generation tasks. The `query()` method makes inference calls to the OpenAI API, leveraging the trained neural network to assess task outputs. This fits the ML-based category as it uses a learned model to capture semantic and contextual quality that deterministic metrics cannot assess.

Evidence 2: GPT-4o judge for ASCII art evaluation
- File: `vlmeval/dataset/utils/megabench/scoring/ascii_art_gpt4o_judge.py`
- Classes: `AsciiArtGPT4OJudge`, `AsciiArtVLMJudgeScore`
- Code Reference:
```python
class AsciiArtGPT4OJudge:
    # GPT-4o judge for ASCII art evaluation
    pass

class AsciiArtVLMJudgeScore:
    # Uses ML model to compare ASCII art
    # Queries GPT-4o to determine equivalence
    pass
```
This specialized judge uses GPT-4o to evaluate ASCII art by comparing model outputs to reference examples. It leverages the vision-language model's learned representations to assess visual similarity in text-based art, a task requiring nuanced semantic understanding that fits the ML-based category's goal of capturing contextual quality.

Evidence 3: Judge model integration for MMIF evaluation
- File: `vlmeval/dataset/mmifeval.py`
- Functions: `build_judge()`, `judge_one_item()`
- Code Reference:
```python
# build_judge() function imported from judge_util.py
# Uses judge models (GPT-4o, GPT-4-turbo variants) for evaluation

def judge_one_item():
    # Calls ML models via run_once_with_image() and run_once_without_image()
    # Line 160-165: Uses LLM to judge text equivalence when direct methods fail
    pass
```
This evaluation module integrates ML model judges (GPT-4o, GPT-4-turbo) to assess constraint satisfaction and text equivalence. When direct algorithmic methods fail, it falls back to LLM judgment via `run_once_with_image()` and `run_once_without_image()`, leveraging learned representations for nuanced assessment as defined in the ML-based category.

Evidence 4: Judge model builder utility
- File: `vlmeval/dataset/utils/judge_util.py`
- Function: `build_judge()`
- Code Reference:
```python
def build_judge():
    # Creates ML model instances for judging
    # Supports OpenAI models (GPT-4, GPT-3.5 variants), SiliconFlow API models, and HuggingFace chat models
    # Models used: gpt-4o, gpt-4-turbo, Qwen variants, DeepSeek, Llama
    pass
```
This utility function instantiates various ML models (GPT-4o, GPT-4-turbo, Qwen, DeepSeek, Llama) to serve as evaluators. It provides a unified interface for creating judge model instances across different API providers (OpenAI, SiliconFlow, HuggingFace), enabling the use of learned neural networks for evaluation tasks as specified in the ML-based category.

Evidence 5: ML fallback for physics evaluation
- File: `vlmeval/dataset/utils/physics_eval_utils.py`
- Function: `is_equiv()`
- Code Reference:
```python
def is_equiv():
    # Uses ML model judge when SymPy fails
    # Lines 73-79: Calls model.generate() to check LaTeX expression equivalence
    # Falls back to LLM judgment when symbolic methods are insufficient
    pass
```
This function attempts symbolic comparison using SymPy, but falls back to ML model judgment (via `model.generate()`) when symbolic methods cannot determine LaTeX expression equivalence. This hybrid approach leverages learned representations to handle cases requiring semantic understanding beyond rule-based methods, fitting the ML-based category's goal of nuanced contextual assessment.

---

### Environmental

Evidence 1: Program execution judge with test cases
- File: `vlmeval/dataset/utils/megabench/scoring/program_judge.py`
- Classes: `ProgramJudge`, `CodeTester`
- Code Reference:
```python
class ProgramJudge:
    # Executes user-generated code against test cases
    pass

class CodeTester:
    # Runs model-generated code in isolated processes
    def run_user_code(self):
        # Executes code with input data and captures output
        pass
    
    def target(self):
        # Uses exec() to run code and catch execution results
        pass
    
    def evaluate_test_case(self):
        # Compares execution output against expected results
        # Lines 35-38: "Create a CodeTester instance with the response and the found test cases"
        # Lines 60-63: Runs code in subprocess with timeout, capturing execution results
        pass
```
This module executes model-generated code in an external Python environment (subprocess with isolation) and validates outputs against test cases. The `run_user_code()` method runs code with inputs and captures results, while `evaluate_test_case()` compares execution output to expected values. This fits the Environmental category as it assesses performance through direct interaction with the Python interpreter, using system-provided feedback (execution results, test outcomes) rather than computational metrics.

Evidence 2: Chart code execution evaluator
- File: `vlmeval/dataset/utils/chartmimic/evaluator/legend_evaluator.py`
- Class: `LegendEvaluator`
- Code Reference:
```python
class LegendEvaluator:
    # Executes generated chart code
    def _log_legends(self):
        # Runs code files and captures matplotlib outputs
        # Line 44-47: Uses run_script_safe() to execute code and capture results
        # Evaluates model-generated visualization code by executing it and checking outputs
        pass
```
This evaluator runs model-generated visualization code in an external environment and captures matplotlib rendering outputs via `run_script_safe()`. It validates chart generation by executing the code and examining the resulting plot properties. This fits the Environmental category as it uses simulator-provided feedback (matplotlib execution results, visualization properties) to assess code generation performance on benchmark tasks.