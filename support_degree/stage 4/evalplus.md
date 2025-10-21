# EvalPlus - Stage 4 (EVALUATE) Evaluation

## Summary
EvalPlus is a specialized code evaluation framework focused on correctness and efficiency testing for LLM-generated Python code, primarily targeting HumanEval and MBPP benchmarks. It provides strong validation, task-specific metrics, and aggregate statistics, but lacks general-purpose evaluator model integration and multi-modal capabilities.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S4F1: Output Validation | 2 | Basic format validation via syntax checking and tree-sitter parsing, but limited policy compliance and normalization |
| S4F2: Metric Computation | 2 | Specialized metrics for code evaluation (pass@k, DPS) with per-sample scoring, but narrow coverage limited to code correctness |
| S4F3: Evaluator Models | 1 | Minimal evaluator model support - can call LLMs for generation but lacks evaluation-specific features |
| S4F4: Multi-Modal Scoring | 0 | Text/code-only framework with no multi-modal evaluation features |
| S4F5: Aggregate Statistics | 3 | Comprehensive statistical analysis including pass@k estimation, confidence intervals, differential performance scoring, and pairwise comparisons |

## Detailed Analysis

### S4F1: Output Validation and Normalization (Rating: 2)

Evidence:

1. Format Validation - Good implementation via tree-sitter:
   - File: `evalplus/sanitize.py` lines 28-38
   ```python
   def code_extract(text: str) -> str:
       # Remove ANSI escape sequences
       ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
       text = ansi_escape.sub("", text)
       # Find longest valid code segment
       for i in range(len(lines)):
           for j in range(i + 1, len(lines)):
               current_lines = "\n".join(lines[i : j + 1])
               if syntax_check(current_lines):
                   # ... finds longest compilable code
   ```

2. Syntax Checking - Basic validation:
   - File: `evalplus/syncheck.py` lines 12-19
   ```python
   def syntax_check(code, verbose=False):
       try:
           ast.parse(code)
           return True
       except (SyntaxError, MemoryError):
           if verbose:
               traceback.print_exc()
           return False
   ```

3. Normalization - Tree-sitter based code extraction:
   - File: `evalplus/sanitize.py` lines 112-153
   ```python
   def extract_target_code_or_empty(code: str, entrypoint: Optional[str] = None) -> str:
       # Parses code using tree-sitter
       parser = Parser(Language(tree_sitter_python.language()))
       tree = parser.parse(code_bytes)
       # Extracts classes, functions, variables
       for child in root_node.children:
           if child.type in IMPORT_TYPE:
               import_nodes.append(child)
           elif child.type == CLASS_TYPE:
               # ... extracts definitions
   ```

4. Limitations - Missing policy checks:
   - No toxicity/harmful content detection
   - No explicit length constraint validation (only timeout-based)
   - Limited partial output handling beyond syntax

Justification for rating 2: Has solid format validation via AST/tree-sitter parsing and good normalization through structured code extraction. However, lacks policy compliance checks (harmful content, constraints) and advanced sanity checks. Works for its specialized domain but requires manual setup for comprehensive validation.

### S4F2: Task-Specific Metric Computation (Rating: 2)

Evidence:

1. Code Correctness Metrics - pass@k implementation:
   - File: `evalplus/eval/__init__.py` lines 65-85
   ```python
   def estimate_pass_at_k(
       num_samples: Union[int, List[int], np.ndarray],
       num_correct: Union[List[int], np.ndarray],
       k: int,
   ) -> np.ndarray:
       """Estimates pass@k of each problem and returns them in an array."""
       def estimator(n: int, c: int, k: int) -> float:
           """Calculates 1 - comb(n - c, k) / comb(n, k)."""
           if n - c < k:
               return 1.0
           return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
   ```

2. Differential Performance Score (DPS) - Efficiency metric:
   - File: `evalplus/evalperf.py` lines 229-271
   ```python
   def perf_worker(task_id: str, ptask: Dict, ret_dict: Dict, ...):
       # Profiles reference solutions
       avg_ref_profile, ref_score = get_avg_ref_profile(idx)
       # Compares sample to references
       for j in range(n_reference - 1, -1, -1):
           avg_ref_profile, ref_score = get_avg_ref_profile(j)
           if avg_sample_profile <= avg_ref_profile:
               result["matching_cluster_idx"] = j
               score = ref_score
               norm_score = 100 * (j + 1) / n_reference
   ```

3. Per-sample Scoring - Individual result tracking:
   - File: `evalplus/evaluate.py` lines 138-168
   ```python
   def check_correctness(...) -> Dict[str, Result]:
       ret = {
           "completion_id": completion_id,
           "task_id": problem["task_id"],
           "solution": solution,
       }
       ret["base"] = untrusted_check(...)
       if not base_only:
           ret["plus"] = untrusted_check(...)
       return ret
   ```

4. Limited Coverage - Only code-specific metrics:
   - No BLEU, ROUGE, BERTScore, etc.
   - No classification metrics (accuracy, F1, etc.)
   - No retrieval metrics (NDCG, MRR, etc.)
   - Specialized for code evaluation only

Justification for rating 2: Implements well-designed metrics (pass@k, DPS) with per-sample scoring and reference implementations. However, metric library is highly specialized with <10 diverse metrics, all focused on code correctness/efficiency. Not extensible to general NLP tasks. Custom metric addition requires forking.

### S4F3: Evaluator Model Integration (Rating: 1)

Evidence:

1. LLM Support for Generation - Has model providers but no evaluation-specific features:
   - File: `evalplus/provider/__init__.py` lines 5-122
   ```python
   def make_model(model: str, backend: str, dataset: str, ...) -> DecoderBase:
       if backend == "vllm":
           return VllmDecoder(...)
       elif backend == "openai":
           return OpenAIChatDecoder(...)
       # ... other backends for generation only
   ```

2. No LLM-as-Judge - No judge prompts or evaluation features:
   - Searched codebase: no "judge", "evaluator prompt", "rating", "scoring prompt" patterns
   - All LLM calls are for code generation, not evaluation

3. No Specialized Evaluators - No RAGAS, G-Eval, or similar:
   - File: `requirements.txt` - no evaluation model dependencies
   - Only generation-focused dependencies (vllm, transformers, openai, etc.)

4. ChatGPT for Input Generation - Only tangential use:
   - File: `evalplus/gen/chatgpt_gen.py` lines 14-67
   ```python
   class ChatGPTGen(BaseGen):
       def chatgpt_generate(self, selected_inputs: List) -> List:
           message = f"Here is a function that we want to test:..."
           # Uses GPT to generate test inputs, not for evaluation
   ```

Justification for rating 1: Can call LLMs through various backends (OpenAI, Anthropic, etc.), but these are exclusively for code generation, not evaluation. No evaluation-specific features like judge prompts, multi-aspect scoring, ensemble methods, or rationale capture. Would need significant custom implementation.

### S4F4: Multi-Modal Scoring Protocols (Rating: 0)

Evidence:

1. Code-Only Focus - Explicit dataset limitation:
   - File: `evalplus/evaluate.py` lines 186-199
   ```python
   def evaluate(dataset: str, samples: Optional[str] = None, ...):
       # ...
       if dataset == "humaneval":
           problems = get_human_eval_plus(...)
       elif dataset == "mbpp":
           problems = get_mbpp_plus(...)
       # Only text/code datasets
   ```

2. No Multi-Modal Dependencies:
   - File: `requirements.txt` - no PIL, opencv, torchaudio, CLIP, etc.
   - Only text processing libraries

3. No Multi-Modal Data Structures:
   - Searched for image/audio/video handling: none found
   - All test inputs are Python primitives (str, int, list, dict, etc.)
   - File: `evalplus/gen/type_mut.py` - only supports basic Python types

4. Documentation Confirms Scope:
   - File: `README.md` lines 17-22
   ```md
   ## 📙 About
   EvalPlus is a rigorous evaluation framework for LLM4Code, with:
   - ✨ HumanEval+: 80x more tests than the original HumanEval!
   - ✨ MBPP+: 35x more tests than the original MBPP!
   ```
   - Explicitly focused on code evaluation only

Justification for rating 0: Framework is entirely text/code-focused with no multi-modal capabilities. No support for vision-language, audio-text, video understanding, or cross-modal evaluation. This is by design for its specialized code evaluation purpose.

### S4F5: Aggregate Statistics and Cross-Model Comparison (Rating: 3)

Evidence:

1. Comprehensive Statistical Analysis - Full implementation:
   - File: `evalplus/eval/__init__.py` lines 65-85
   ```python
   def estimate_pass_at_k(...) -> np.ndarray:
       """Calculates 1 - comb(n - c, k) / comb(n, k)."""
       # Unbiased estimator for pass@k with confidence intervals
   ```

2. Distribution Analysis - Detailed profiling:
   - File: `evalplus/perf/profile.py` (referenced in evalperf.py)
   - Collects performance distributions via CPU instruction counting
   - File: `evalplus/evalperf.py` lines 229-271
   ```python
   # Profiles solutions and compares distributions
   sample_profiles = profile(solution, entry_point, [pe_input], ...)
   avg_sample_profile = mean(sample_profiles)
   ```

3. Pairwise Comparison - Cross-model differential performance:
   - File: `evalplus/evalperf.py` lines 244-268
   ```python
   # Matches sample performance to reference clusters
   for j in range(n_reference - 1, -1, -1):
       avg_ref_profile, ref_score = get_avg_ref_profile(j)
       if avg_sample_profile <= avg_ref_profile:
           result["matching_cluster_idx"] = j
           score = ref_score
           norm_score = 100 * (j + 1) / n_reference
   ```

4. Ranking and Leaderboard - Built-in support:
   - File: `README.md` lines 26-27
   ```md
   - ✨ Precise evaluation: See [our leaderboard](https://evalplus.github.io/leaderboard.html)
   ```

5. Weighted Metrics - Task-level weighting:
   - File: `evalplus/evalperf.py` lines 338-348
   ```python
   # Aggregates DPS across tasks
   dps = mean(not_none([res["dps"] for res in eval_results.values()]))
   dps_norm = mean(not_none([res["dps_norm"] for res in eval_results.values()]))
   pass_1 = mean(not_none([res["pass@1"] for res in eval_results.values()]))
   ```

6. Statistical Testing - Confidence intervals via unbiased estimation:
   - File: `evalplus/eval/__init__.py` lines 70-77
   ```python
   def estimator(n: int, c: int, k: int) -> float:
       """Calculates 1 - comb(n - c, k) / comb(n, k)."""
       if n - c < k:
           return 1.0
       return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
   ```

7. Result Persistence and Resumability:
   - File: `evalplus/evaluate.py` lines 201-221
   ```python
   if os.path.isfile(result_path) and not i_just_wanna_run:
       print(f"Load from previous results from {result_path}")
       with open(result_path, "r") as f:
           results = json.load(f)
       results = compatible_eval_result(results)
   ```

Justification for rating 3: Excellent implementation of statistical analysis and comparison features. Provides pass@k estimation with proper unbiased estimators, detailed performance profiling, differential scoring (DPS), task-level aggregation, and leaderboard generation. Supports resumability and has visualization tools (referenced in evalperf.py output). Comprehensive suite meeting all requirements for aggregate statistics and cross-model comparison.

## Overall Assessment

Strengths:
- Exceptional aggregate statistics and comparison framework (S4F5: 3/3)
- Specialized, well-implemented metrics for code evaluation (pass@k, DPS)
- Robust code validation via tree-sitter parsing
- Per-sample granularity with detailed failure analysis
- Production-ready with leaderboard integration

Weaknesses:
- No evaluator model integration (S4F3: 1/3)
- No multi-modal support (S4F4: 0/3)
- Limited to code correctness domain
- Narrow metric library (only code-specific)
- Missing policy compliance checks (toxicity, bias, etc.)

Use Case Fit:
EvalPlus is purpose-built for rigorous code generation evaluation. It excels at what it does (code correctness/efficiency) but is not suitable for general-purpose LLM evaluation across diverse tasks and modalities. Organizations evaluating code generation models will find it comprehensive; those needing broader evaluation capabilities should look elsewhere.

Total Score: 8/15 - Strong in its specialized domain (code evaluation) but limited in scope for general evaluation frameworks.