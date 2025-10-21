## Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

**Definition**: Predefined metrics and statistical functions that provide deterministic assessment.

**Goal**: Ensure consistent, reproducible evaluation through established computational measures.

Evidence 1: Expression equivalence pattern matching
- File: `examples/scorer.py`
- Function: `expression_equivalence()`
- Code Reference:
```python
match = re.search(AnswerPattern.LINE, state.output.completion)
```
This scorer uses regex pattern matching to extract answers from model outputs and compare them. The deterministic nature of regex operations—where the same pattern consistently produces identical results on the same input—exemplifies algorithmic evaluation. This approach relies on predefined string matching algorithms rather than learned representations, ensuring reproducible assessment across multiple runs.

Evidence 2: Built-in algorithmic scorers
- File: `tests/test_examples.py` (and references throughout test files)
- Imported Functions: `match()`, `exact()`, `includes()`, `accuracy()`
- Code Reference:
```python
from inspect_ai.scorer import match, exact, includes, accuracy
```
The framework extensively uses these algorithmic scorers which implement predefined mathematical formulas and string comparison operations. Each scorer applies deterministic rules: `match()` uses pattern matching, `exact()` performs string equality checks, `includes()` tests substring containment, and `accuracy()` computes statistical ratios. These functions exemplify algorithmic evaluation by providing consistent, reproducible results without requiring any learning or adaptation.

Evidence 3: Numeric normalization utilities
- File: `tests/util/test_str_to_float.py`
- Functions: `normalize_number()`, `unicode_number_to_float()`
- Code Reference:
```python
def normalize_number(text: str) -> float:
    # Mathematical conversion and normalization
    
def unicode_number_to_float(text: str) -> float:
    # Character encoding conversion
```
These mathematical functions normalize and convert numeric values using deterministic algorithms. They apply fixed rules for parsing different number formats, unicode characters, and string representations into standardized numerical forms. This preprocessing step enables consistent algorithmic comparison of numeric outputs, supporting reproducible evaluation scoring.

Evidence 4: Statistical and computational scorers
- File: `tests/test_sample_limits.py`
- Functions: `token_consuming_scorer()`, `slow_scorer()`, `mean()` metric
- Code Reference:
```python
def token_consuming_scorer():
    # Token counting logic
    
def slow_scorer():
    # Computational delay measurement
    
mean_score = mean([score1, score2, score3])
```
These scorers use mathematical calculations—token counting, timing measurements, and mean computation—to evaluate model outputs. Token counting applies deterministic algorithms to parse and count linguistic units, while `mean()` uses standard statistical formulas. These represent algorithmic approaches that ensure consistent evaluation through predefined computational measures.

---

### ML-based

**Definition**: Machine learning models serving as evaluators, including LLM judges, reward models, and reference models.

**Goal**: Leverage learned representations for nuanced assessment that captures semantic and contextual quality.

Evidence 1: LLM-as-judge for mathematical equivalence
- File: `examples/scorer.py`
- Function: `expression_equivalence()`
- Code Reference:
```python
async def score(state: TaskState, target: Target):
    # extract answer
    match = re.search(AnswerPattern.LINE, state.output.completion)
    if match:
        # ask the model to judge equivalence
        answer = match.group(1)
        prompt = EQUIVALENCE_TEMPLATE % (
            {"expression1": target.text, "expression2": answer}
        )
        result = await get_model().generate(prompt)

        # return the score
        correct = result.completion.lower() == "yes"
        return Score(
            value=CORRECT if correct else INCORRECT,
            answer=answer,
            explanation=state.output.completion,
        )
```
This scorer explicitly uses an ML model as a judge to evaluate mathematical expression equivalence. Rather than relying solely on algorithmic string matching, it leverages a language model's learned representations to assess semantic equivalence between mathematical expressions. The model receives a prompt asking whether two expressions are equivalent and provides a judgment ("Yes" or "No"), which becomes the evaluation result. This exemplifies ML-based evaluation by using learned capabilities to capture nuanced semantic relationships that rigid algorithmic rules might miss.

Evidence 2: Model-based token consumption testing
- File: `tests/test_sample_limits.py`
- Function: `token_consuming_scorer()`
- Code Reference:
```python
async def token_consuming_scorer():
    result = await model.generate("Hello")
    # Use model response in scoring
```
This scorer uses a model to generate responses as part of the scoring process. While designed primarily for testing token consumption limits, it demonstrates how ML models can be integrated into the evaluation pipeline. The scorer invokes model generation, leveraging the model's learned language understanding capabilities within the scoring mechanism, even though the primary purpose here is measuring resource consumption rather than semantic judgment.

Evidence 3: Multi-generation model scorer
- File: `tests/util/test_sample_limits.py`
- Function: `generating_scorer()`
- Code Reference:
```python
async def generating_scorer():
    result = await model.generate(state.messages)
    # Multiple model calls during scoring
```
This scorer calls a model multiple times during the scoring process, demonstrating the framework's support for ML-based evaluation workflows. By generating model responses based on conversation state, the scorer can leverage learned representations to assess contextual quality. This pattern shows how ML models can serve as evaluators that process complex inputs and provide nuanced assessments based on their learned knowledge and reasoning capabilities.