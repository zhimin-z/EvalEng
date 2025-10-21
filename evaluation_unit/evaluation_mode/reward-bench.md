## Evaluation Mode Categories

[Static Analysis]

## Detailed Analysis

### Static Analysis

Evidence 1: Reward Model Scoring
- File: `scripts/run_rm.py`
- Key Functions/Lines: Lines 197-238 (Pipeline inference setup), Lines 240-271 (Built-in pipeline execution), Lines 273-337 (Custom pipeline execution)
- Code Reference:
```python
# pairwise comparison list comprehension
results = [1 if chosen > rejected else 0 for chosen, rejected in zip(scores_chosen, scores_rejected)]
```
```python
[
    results.append(1) if chosen > rejected else results.append(0)
    for chosen, rejected in zip(score_chosen_batch, score_rejected_batch)
]
```
This script loads reward models and evaluates them by comparing scores between chosen and rejected responses. The evaluation is purely based on comparing scalar outputs (scores/logits) from the model without executing any generated code or artifacts. The script performs static comparison of model outputs to determine correctness.

---

Evidence 2: DPO Model Evaluation
- File: `scripts/run_dpo.py`
- Key Functions/Lines: Lines 142-154 (DPO inference setup), Lines 174-185 (Batch processing and reward computation)
- Code Reference:
```python
[
    results.append(1) if chosen > rejected else results.append(0)
    for chosen, rejected in zip(scores_chosen_batch, scores_rejected_batch)
]
scores_chosen += scores_chosen_batch
scores_rejected += scores_rejected_batch
```
This script evaluates Direct Preference Optimization (DPO) models by computing rewards for chosen vs rejected responses and performing static comparisons. The evaluation examines model outputs (reward scores) without any execution of generated artifacts.

---

Evidence 3: RewardBench 2 Evaluation
- File: `scripts/run_v2.py`
- Key Functions/Lines: Lines 153-198 (Model and pipeline setup), Lines 222-248 (Batch inference processing), Lines 259-274 (Best-of-N scoring)
- Code Reference:
```python
if isinstance(rewards[0], dict):
    scores_batch = [result["score"] for result in rewards]
else:
    scores_batch = rewards.float().cpu().numpy().tolist()
scores.extend(scores_batch)
```
```python
out_dataset = reroll_and_score_dataset(out_dataset, total_completions, cols_to_combine=["text", "scores"])
```
This script evaluates reward models on the RewardBench 2 dataset with best-of-N completions. It computes scores for multiple completions per prompt and selects the highest-scoring one. The evaluation is entirely based on comparing numerical scores without executing any generated content.

---

Evidence 4: LLM-as-a-Judge Evaluation
- File: `scripts/run_generative.py`
- Key Functions/Lines: Lines 96-135 (API-based judgment processing), Lines 176-207 (Local model inference), Lines 209-218 (Winner processing)
- Code Reference:
```python
def get_judgement(batch, debug=args.debug):
    # ... format prompts ...
    winner, request, judgement = run_judge_pair(
        prompt, answer_a, answer_b, args.model, multi_turn=mult_turn, model_modifier=model_modifier
    )
    # ... handle voting ...
    if winner == winner_text:
        return 1
    elif winner == loser_text:
        return 0
    else:
        return 0.5
```
```python
answers = [o.outputs[0].text for o in outputs]
winners = [process_judgement(a, model_modifier) for a in answers]

def process_shuffled(win, shuffle):
    # ... determine winner ...
    if win == winner_text:
        return 1
    elif win == loser_text:
        return 0
    else:
        return 0.5
```
This script uses generative models as judges to compare pairs of responses. While the models generate text judgments, the evaluation harness itself performs static analysis by parsing the generated text to extract a winner (A or B) and comparing it against the ground truth. The harness doesn't execute any generated code—it only parses and compares text outputs.

---

Evidence 5: Best-of-N Ranking
- File: `scripts/run_bon.py`
- Key Functions/Lines: Lines 143-151 (Pipeline inference), Lines 153-157 (Score extraction), Lines 188-199 (Custom pipeline batch processing)
- Code Reference:
```python
# extract scores from results which is list of dicts
scores = [r["score"] for r in results]
```
```python
if isinstance(rewards[0], dict):
    scores_batch = [result["score"] for result in rewards]
else:
    scores_batch = rewards.cpu().numpy().tolist()
scores.extend(scores_batch)
```
This script ranks multiple completions using reward model scores to select the best response. The evaluation is purely based on comparing numerical scores across multiple candidates without executing any generated artifacts.

---

Evidence 6: Data Loading and Processing
- File: `tests/test_data.py` (Lines 17-133), `tests/test_package.py` (Lines 20-37)
- Key Operations: Format validation, text tokenization, template application, structural validation
- Code Reference:
```python
# Format validation of prompt-response pairs
# Text tokenization and template application
# Structural validation of conversation format
```
The test files demonstrate that the harness performs format validation, text processing, and structural checks on model outputs and datasets. These are all static analysis operations that examine the structure and format of data without executing it.