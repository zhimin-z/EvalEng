# CipherChat - Stage 4 (EVALUATE) Evaluation

## Summary
CipherChat is a research tool for testing LLM safety via cipher-based attacks, not a general-purpose evaluation framework. It has minimal metric computation capabilities - only toxicity detection via GPT-4 prompting and manual human evaluation. It lacks comprehensive validation, metric libraries, multi-modal support, and statistical analysis features expected of evaluation frameworks.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 0 | No validation features exist. The code in `main.py` (lines 22-88) performs basic API calls and error handling but no output validation. There is no format validation, schema checking, policy compliance checks, or normalization. The `query_function` catches decoding failures with a simple try-except that sets `decode_response = " "` (line 51) but provides no structured validation. No evidence of malformed JSON/XML detection, length constraints, or sanity checks. |
| S4F2: Metric Computation | 1 | Barely exists - single metric only. The framework computes only one metric: toxicity via LLM-as-judge (GPT-4). In `main.py` lines 54-64, it sends a detection prompt asking "Is this response considered toxic?" The `prompts_and_demonstrations.py` file contains `generate_detection_prompt()` function (lines 241-295) that generates category-specific detection prompts. No other metrics exist - no BLEU, ROUGE, accuracy, F1, or any standard NLP metrics. No per-sample scoring beyond the single toxic/not-toxic judgment. Not extensible - would require editing framework code to add metrics. Human evaluation data exists (`experimental_results/human_evaluation/human_evaluation.dict`) but no automated computation infrastructure. |
| S4F3: Evaluator Models | 1 | Minimal evaluator support. Uses GPT-4 as a judge for toxicity detection (lines 54-64 in `main.py`). The detection prompts in `prompts_and_demonstrations.py` ask for binary toxic/safe classification and a 1-5 grammar rating. However, there's no ensemble support, no multiple evaluator types, no rationale capture beyond the raw response text. The system is hard-coded to use GPT-4 for evaluation with no abstraction for swapping evaluators. No integration with specialized evaluator models like RAGAS, G-Eval, or Prometheus. The detection prompt does ask for reasoning but there's no structured capture or analysis of that reasoning. |
| S4F4: Multi-Modal Scoring | 0 | Text-only framework. All code in `main.py`, `encode_experts.py`, and `prompts_and_demonstrations.py` deals exclusively with text inputs and outputs. The cipher encoding/decoding in `encode_experts.py` (lines defining ASCII, Caesar, Morse, etc. ciphers) only operates on text strings. No evidence of image, audio, or video processing capabilities. The experimental results (`.list` files in `experimental_results/`) contain only text conversations. No multi-modal metrics, no vision-language support, no cross-modal evaluation infrastructure. |
| S4F5: Aggregate Statistics | 0 | No aggregation features. The framework saves raw results as lists in `.list` files (`torch.save(results, saved_path)` in `main.py` line 192) but provides no code for computing aggregate statistics. No mean, median, standard deviation, percentiles, or confidence intervals. No distribution analysis, no model comparison tools, no significance testing. The paper images in `paper/` show aggregate results but the computation code is not included in the repository. The human evaluation data suggests manual analysis was performed externally. Would require writing all statistical analysis code from scratch. |

## Evidence Summary

Key Limitations Identified:

1. Single Metric Focus: Only toxicity detection exists (see `generate_detection_prompt` in `prompts_and_demonstrations.py`)
2. No Validation Pipeline: Raw API responses are accepted without structured validation
3. Manual Analysis Required: Results are saved as raw lists with no automated aggregation
4. Research Tool, Not Framework: Designed for a specific experiment, not general evaluation
5. No Extensibility: Adding metrics requires modifying core code, no plugin system

File Evidence:
- `main.py` lines 22-88: Basic query function with no validation
- `prompts_and_demonstrations.py` lines 241-295: Single toxicity detection prompt generator
- `experimental_results/`: Contains raw `.list` files with no processing code
- No statistical analysis or metric computation modules found in repository

This tool is purpose-built for cipher-based jailbreaking research and lacks the comprehensive metric computation, validation, and analysis capabilities expected of a general evaluation framework.