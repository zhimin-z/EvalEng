## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification]

## Detailed Analysis

### Explicit Labels

Evidence 1: Target-Based Scoring
- File: `examples/scorer.py`
- Code Reference: `EQUIVALENCE_TEMPLATE` variable and `expression_equivalence()` scorer
```
prompt = EQUIVALENCE_TEMPLATE % ({"expression1": target.text, "expression2": answer})
```
The scorer compares model outputs against `target.text` which contains predetermined correct answers. The `Target` object contains reference answers loaded from the dataset, providing explicit ground truth for evaluation.

Evidence 2: Dataset Field Mapping
- File: `examples/scorer.py`
- Code Reference: Dataset loading with `FieldSpec`
```
dataset=hf_dataset(
    "HuggingFaceH4/MATH-500",
    split="test",
    sample_fields=FieldSpec(input="problem", target="solution"),
    shuffle=shuffle,
)
```
The `target="solution"` maps to gold standard solutions from the dataset. This field specification explicitly designates reference answers for comparison against model outputs.

---

### Behavioral Specification

Evidence 1: Semantic Equivalence Validation
- File: `examples/scorer.py`
- Code Reference: `expression_equivalence()` scorer
```
@scorer(metrics=[accuracy(), stderr()])
def expression_equivalence():
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
```
Dynamic validation mechanism using executable logic (model-as-judge) to verify functional correctness. Rather than simple string comparison, this validates semantic equivalence of mathematical expressions through behavioral assessment.