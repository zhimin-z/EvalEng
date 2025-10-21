# RewardBench - Stage 4 (EVALUATE) Evaluation

## Summary
RewardBench is a specialized evaluation framework focused on assessing reward models for RLHF. It provides comprehensive infrastructure for computing metrics on reward model outputs, including support for various model architectures (sequence classifiers, DPO models, generative RMs), but is narrowly scoped to preference-based ranking accuracy rather than general metric computation. The framework excels at aggregating results across subsets but lacks extensive validation, multi-modal support, and statistical testing features.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 1 | Minimal validation. No format validation, schema checks, or normalization features found. The framework assumes model outputs are valid scores/logits and performs basic comparisons (chosen > rejected). No evidence of handling malformed outputs, policy checks, or sanity checks beyond basic result assignment (`results.append(1) if chosen > rejected else results.append(0)` in `scripts/run_rm.py:161`). |
| S4F2: Metric Computation | 2 | Limited to ranking accuracy metrics. Core metric is binary correctness (chosen > rejected) computed per-example (`rewardbench/utils.py` contains `calculate_scores_per_section` for aggregation). Supports per-sample scoring with `scores_chosen` and `scores_rejected` columns added to dataset. Extension requires custom code rather than plugin system. Covers ~3-5 aggregate metrics (accuracy per subset, weighted averages) but lacks standard NLG metrics (BLEU, ROUGE), classification metrics (precision, recall, F1), or retrieval metrics. |
| S4F3: Evaluator Models | 2 | Basic LLM-as-judge support for generative RMs. `scripts/run_generative.py` implements judge prompts via `rewardbench/generative.py` with `run_judge_pair` and `run_judge_ratings` functions. Supports multiple providers (OpenAI, Anthropic, Gemini) via `API_MODEL_LIST`. Limited ensemble via PoLL (plurality of LLM judges, lines 99-103 in `run_generative.py`). No rationale capture, calibration, or specialized evaluator models (RAGAS, G-Eval) beyond basic prompting. Model-specific modifiers exist (`prometheus`, `gemini`, `offsetbias`) but are hardcoded switches. |
| S4F4: Multi-Modal Scoring | 1 | Minimal multi-modal support. One vision-language model supported (`Skywork/Skywork-VL-Reward-7B` in `rewardbench/models/skyvl.py`) but uses text-only evaluation pipeline. Config shows `Qwen2_5_VLForConditionalGeneration` model class but no multi-modal metrics (CLIP score, VQA accuracy, etc.). No audio, video, or cross-modal evaluation capabilities. Framework is text-centric with token-based processing throughout. |
| S4F5: Aggregate Statistics | 2 | Basic statistics with subset-based aggregation. `calculate_scores_per_section` in `rewardbench/utils.py:134-159` computes weighted averages across predefined subsets using `EXAMPLE_COUNTS` and `SUBSET_MAPPING` constants. Per-subset accuracy printed in evaluation scripts (e.g., `scripts/run_rm.py:236-240`). No variance, confidence intervals, percentiles, distribution analysis, or significance testing. No model comparison features (t-tests, bootstrap CIs, effect sizes). Simple mean aggregation with custom weighting for specific categories (Chat, Safety, Reasoning). |

## Detailed Evidence

### S4F1: Output Validation and Normalization

Evidence of minimal validation:

From `scripts/run_rm.py` lines 159-163:
```python
[
    results.append(1) if chosen > rejected else results.append(0)
    for chosen, rejected in zip(scores_chosen_batch, scores_rejected_batch)
]
```

This shows direct score comparison with no validation of:
- Score ranges or distributions
- Malformed outputs (NaN, infinite values)
- Format consistency

From `scripts/run_dpo.py` lines 164-173:
```python
# for each item in batch, record 1 if chosen > rejected
# extra score from dict within batched results (e.g. logits)
# [{'label': 'LABEL_1', 'score': 0.6826171875},... ]
if isinstance(rewards_chosen[0], dict):
    scores_chosen_batch = [result["score"] for result in rewards_chosen]
    scores_rejected_batch = [result["score"] for result in rewards_rejected]
# for classes that directly output scores (custom code)
else:
    scores_chosen_batch = rewards_chosen.float().cpu().numpy().tolist()
    scores_rejected_batch = rewards_rejected.float().cpu().numpy().tolist()
```

Basic type checking but no validation of score validity or normalization.

### S4F2: Task-Specific Metric Computation

Limited metric library:

From `rewardbench/utils.py` lines 134-159 (calculate_scores_per_section):
```python
def calculate_scores_per_section(example_counts, subset_mapping, metrics):
    """
    Calculate overall scores per section from metrics data.
    """
    section_scores = {}
    for section, tests in subset_mapping.items():
        total_weighted_score = 0
        total_examples = 0
        for test in tests:
            if test in metrics:
                test_score = metrics[test]
                test_count = example_counts[test]
                total_weighted_score += test_score * test_count
                total_examples += test_count
        if total_examples > 0:
            section_scores[section] = total_weighted_score / total_examples
        else:
            section_scores[section] = 0
    return section_scores
```

This only computes weighted accuracy, no diversity of metrics.

Per-sample scoring supported:

From `scripts/run_rm.py` lines 245-246:
```python
out_dataset = out_dataset.add_column("scores_chosen", scores_chosen)
out_dataset = out_dataset.add_column("scores_rejected", scores_rejected)
```

Individual scores are preserved but only for accuracy computation.

### S4F3: Evaluator Model Integration

Basic LLM-as-judge implementation:

From `scripts/run_generative.py` lines 88-113:
```python
def get_judgement(batch, debug=args.debug):
    mult_turn = True if len(batch["text_chosen"]) > 2 else False
    prompt = batch["text_chosen"][0]["content"]
    answer_a = batch["text_chosen"]
    answer_b = batch["text_rejected"]

    # shuffle a and b randomly for position bias
    is_shuffled = np.random.rand() > 0.5
    if is_shuffled:
        answer_a, answer_b = answer_b, answer_a
        winner_text = "B"
        loser_text = "A"
    else:
        winner_text = "A"
        loser_text = "B"

    if len(batch["text_chosen"]) <= 4:  # set up only for 1 or 2 turns
        if not args.score_w_ratings:
            winner, request, judgement = run_judge_pair(...)
        else:
            winner, request, judgement = run_judge_ratings(...)
```

Ensemble support (PoLL):

From `scripts/run_generative.py` lines 99-103:
```python
# handle voting
if isinstance(winner, list):
    if debug:
        print(winner)
    winner = max(set(winner), key=winner.count)
```

Simple majority voting, no sophisticated aggregation or rationale capture.

### S4F4: Multi-Modal Scoring Protocols

Single vision model with text-only evaluation:

From `rewardbench/models/__init__.py` lines 276-283:
```python
"Skywork/Skywork-VL-Reward-7B": {
    "model_builder": Qwen2_5_VLForConditionalGeneration.from_pretrained,
    "pipeline_builder": SkyVLPipeline,
    "quantized": False,
    "custom_dialogue": False,
    "model_type": "Seq. Classifier",
    "torch_dtype": torch.bfloat16,
},
```

Despite using a vision-language model class, the evaluation remains text-centric with no image input handling or multi-modal metrics.

### S4F5: Aggregate Statistics and Cross-Model Comparison

Basic subset aggregation:

From `scripts/run_rm.py` lines 236-242:
```python
present_subsets = np.unique(subsets)
for subset in present_subsets:
    subset_dataset = out_dataset.filter(lambda example: example["subset"] == subset)
    num_correct = sum(subset_dataset["results"])
    num_total = len(subset_dataset["results"])
    print(f"{subset}: {num_correct}/{num_total} ({num_correct/num_total})")
    results_grouped[subset] = num_correct / num_total
```

Simple accuracy computation per subset, no statistical testing or advanced analysis.

Weighted aggregation:

From `rewardbench/constants.py` (referenced in utils):
```python
EXAMPLE_COUNTS = {
    "alpacaeval-easy": 100,
    "alpacaeval-hard": 95,
    # ... more subsets
}

SUBSET_MAPPING = {
    "Chat": ["alpacaeval-easy", "alpacaeval-hard", "mt-bench-easy", "mt-bench-medium"],
    "Chat Hard": ["alpacaeval-length", "llmbar-natural", "llmbar-adver-*"],
    # ... more categories
}
```

Custom weighting scheme but no confidence intervals, significance tests, or model comparison features.

## Key Strengths
1. Specialized for reward model evaluation with clear focus on preference ranking
2. Per-sample score tracking enables detailed analysis
3. Multiple model architecture support (classifiers, DPO, generative)
4. Subset-based organization with weighted aggregation

## Key Weaknesses
1. No validation pipeline for outputs or sanity checks
2. Single metric focus (ranking accuracy) with no standard NLG/classification metrics
3. Limited statistical analysis - no variance, CIs, or significance testing
4. Minimal multi-modal support despite having one VL model
5. No model comparison tools for statistical testing between RMs