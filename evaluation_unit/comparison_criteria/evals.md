## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, Comparative Baseline, None, Custom]

## Detailed Analysis

### Explicit Labels

Evidence 1: Basic Match Templates
- File: `evals/elsuite/basic/match.py`, `evals/elsuite/basic/includes.py`, `evals/elsuite/basic/fuzzy_match.py`
- Code Reference: Match-based evaluation templates
```
class Match:
    # From docs/eval-templates.md:
    # "For a model completion `a` and a reference list of correct answers `B`"
    # Compares model outputs against reference answers
    
# Sample format from docs/custom-eval.md:
{"problem": "2+2=", "answer": "4"}
{"problem": "48+2=", "answer": "50"}
```
These basic evaluation templates compare model completions against reference answers stored in sample datasets. The `Match` class yields a match if model output is identical to at least one answer from the reference list, providing direct comparison against explicit ground truth labels.

Evidence 2: JSON Match Evaluation
- File: `evals/elsuite/basic/json_match.py`
- Code Reference: JsonMatch class
```
class JsonMatch:
    # From docs/eval-templates.md:
    # "yields a match if `a` is identical to at least one answer from `B`"
    # Compares JSON outputs to reference JSON answers
```
The JsonMatch template compares structured JSON outputs from models against reference JSON answers. This extends explicit label comparison to structured data formats, validating that model-generated JSON matches predetermined correct JSON structures.

Evidence 3: Match Recording Utility
- File: `evals/api.py`
- Code Reference: record_and_check_match() function
```
def record_and_check_match(prompt, sampled, expected):
    # Used in evals/elsuite/skill_acquisition/eval.py:
    picked = evals.record_and_check_match(
        prompt=sample["input"],
        sampled=answer,
        expected=[sample["ideal"]]
    )
```
This utility function checks if model output matches expected answers and is used throughout the codebase. In skill acquisition evaluation, it compares the model's sampled answer against the ideal reference answer stored in the sample, recording whether the output matches the explicit label.

Evidence 4: Dataset Ground Truth Structure
- File: Sample dataset format (from `docs/custom-eval.md`)
- Code Reference: JSONL sample structure
```bash
echo -e '{"problem": "48+2=", "answer": "50"}\n{"problem": "5*20=", "answer": "100"}' > /tmp/test.jsonl
# Samples contain "answer" fields with correct responses
```
Sample datasets contain explicit "answer" fields with correct responses that serve as ground truth for evaluation. Each problem-answer pair provides predetermined reference labels that model outputs are compared against to determine correctness.

---

### Behavioral Specification

Evidence 1: Chess Move Validation
- File: `evals/elsuite/cant_do_that_anymore/chess/board.py`, `evals/elsuite/cant_do_that_anymore/eval.py`
- Code Reference: BoardController validation methods
```
class BoardController:
    def move_within_board(self):
        # Validates chess moves dynamically
    
    def same_color_piece_at_move_start(self):
        # Checks piece ownership
    
    def capturing_same_color(self):
        # Validates capture rules

# From eval.py:
violation = (piece_moved_outside_board or 
             moving_invalid_piece or 
             piece_capturing_same_color or 
             incorrect_notation)
```
The BoardController class validates model-generated chess moves against game rules dynamically. Methods check if moves comply with chess specifications including board boundaries, piece ownership, and capture rules, providing executable behavioral validation of model outputs.

Evidence 2: Chess Implementation Correctness
- File: `evals/elsuite/cant_do_that_anymore/chess/board_test.py`
- Code Reference: simulate_games() function
```
def simulate_games():
    """
    Simulates full chess games and asserts that at every position,
    the set of legal moves is equivalent to the legal moves reported
    by the python-chess library
    """
    # Validates that legal moves match python-chess library
```
This function validates the chess implementation by simulating complete games and verifying that legal move generation matches the python-chess library at every position. This provides behavioral specification validation through executable game simulation.

Evidence 3: Function Deduction Validation
- File: `evals/elsuite/function_deduction/eval.py`
- Code Reference: Function correctness checking
```
def validate_function():
    # Validates if model correctly deduced functions
    if guessed_ints == expected_ints:
        self.success = True
    # Tests function behavior through input-output validation
```
The evaluation validates whether the model correctly deduced functions by checking if guessed outputs match expected outputs for given inputs. The function behavior is tested dynamically through executable input-output validation rather than static comparison.

Evidence 4: Gym Environment Validation
- File: `evals/elsuite/incontext_rl/eval.py`
- Code Reference: Environment-based action validation
```
def validate_actions(solver, env):
    action = self._try_get_valid_action(solver, ts, env.action_space.n)
    next_observation, reward, terminated, truncated, _ = env.step(action)
    # Environment acts as executable specification for valid behavior
```
Uses gymnasium environments to validate agent actions through execution. The environment serves as an executable specification that determines valid actions and provides feedback through state transitions and rewards, validating model behavior dynamically.

---

### Comparative Baseline

Evidence 1: Voter-Influencer Comparison
- File: `evals/elsuite/ballots/eval.py`
- Code Reference: Dual model debate scenario
```
class Ballots:
    def __init__(self):
        self.voter_fn, self.influencer_fn = completion_fns
    # Compares two models in debate scenario
    # Measures how one model influences another's voting behavior
```
Compares two models in a debate scenario where one model (influencer) attempts to change another model's (voter) decision. The evaluation measures relative performance by assessing how effectively one model influences another, creating comparative baseline assessment.

Evidence 2: Head-to-Head Battle Evaluation
- File: `evals/registry/modelgraded/battle.yaml`
- Code Reference: Model comparison template (from `docs/eval-templates.md`)
```yaml
# battle.yaml: a head-to-head eval which compares two model completions
# for two potentially different prompts. choice_scores is used to log
# how often the first completion is judged to be better than the second
```
Implements head-to-head evaluation comparing two model completions directly. The battle template uses choice scores to track which model's output is judged superior, providing relative performance assessment through pairwise comparison.

Evidence 3: Player vs Opponent Comparison
- File: `evals/elsuite/bluff/eval.py`
- Code Reference: Player comparison setup
```
def setup_players(game, solver):
    player_0 = SolverPlayer(game, solver)
    player_1 = self._create_opponent(game)
    # Records win rates and comparative metrics between players
```
Compares solver performance against opponent players in game scenarios. The evaluation records win rates and comparative metrics between the solver and opponents, measuring relative performance through competitive gameplay.

Evidence 4: Model-Graded Comparison Generation
- File: `scripts/modelgraded_generator.py`
- Code Reference: Comparative evaluation sample generation
```
# Generates evaluation samples where models compare outputs
# Creates prompts for model-graded evaluation with comparative assessment
```
Generates evaluation samples for model-graded comparisons where models assess outputs. The script creates prompts that inherently involve comparative assessment, enabling baseline comparison through model judgment.

---

### Implicit Standard

**NOT PRESENT**

The repository does not show evaluation against unlabeled corpora or distributional similarity measures. All evaluations use either explicit labels, behavioral validation, comparative baselines, reference-free metrics, or custom hybrid approaches.

---

### None

Evidence 1: Bootstrap Statistical Measures
- File: `evals/metrics.py`
- Code Reference: get_bootstrap_accuracy_std() function
```
def get_bootstrap_accuracy_std(vals, num_samples):
    return np.std([
        np.mean(random.sample(vals, len(vals) // 2)) 
        for _ in range(num_samples)
    ])
    # Computes bootstrap standard deviation as intrinsic statistical measure
```
Computes bootstrap standard deviation to measure internal consistency of results without external reference. This intrinsic statistical measure assesses result stability through resampling, providing quality metrics independent of ground truth comparison.

Evidence 2: Chess Rule Violation Detection
- File: `evals/elsuite/cant_do_that_anymore/eval.py`
- Code Reference: Violation tracking
```
violation = (piece_moved_outside_board or 
             moving_invalid_piece or 
             piece_capturing_same_color or 
             incorrect_notation)
# Tracks violations like piece_moved_outside_board, moving_invalid_piece
# These are intrinsic rule violations without external references
```
Tracks intrinsic rule violations in chess moves including pieces moving outside the board, invalid piece movements, and same-color captures. These violation metrics measure internal consistency with game rules without requiring external reference standards.

Evidence 3: Repetition Self-Consistency
- File: `evals/elsuite/already_said_that/eval.py`
- Code Reference: Repetition measurement
```
def measure_repetition():
    repeated_rounds = len(cs.parsed_responses) - len(set(cs.parsed_responses))
    # Measures if model repeats itself - self-consistency checking
```
Measures whether the model repeats itself by comparing the number of total responses to unique responses. This self-consistency check evaluates output quality through internal repetition detection without external standards.

Evidence 4: Performance Intrinsic Metrics
- File: `evals/elsuite/skill_acquisition/eval.py`
- Code Reference: Context and timeout tracking
```
ctx_len_exceeded_rate = sum(
    1 for result in retrieval_results 
    if result['ctx_len_exceeded']
) / len(retrieval_results)

timeout_rate = sum(
    1 for result in retrieval_results 
    if result['timeout']
) / len(retrieval_results)
```
Tracks context length exceeded rate and timeout rate as intrinsic performance measures. These metrics assess model operational characteristics like context window usage and response latency without requiring external reference comparisons.

---

### Custom

Evidence 1: Model-Based Self-Evaluation
- File: `evals/elsuite/modelgraded/classify.py`
- Code Reference: ModelBasedClassify class (from `docs/eval-templates.md`)
```
class ModelBasedClassify:
    """
    Gets the model's completion to the original prompt,
    wraps it in an evaluation prompt,
    and gets the model's completion to the evaluation prompt
    """
    # Custom hybrid approach using model itself as evaluator
```
Implements a custom hybrid evaluation where the model evaluates its own outputs. The approach wraps the original completion in an evaluation prompt and uses the model's judgment as the evaluation criterion, creating a specialized self-assessment pipeline.

Evidence 2: Factual Consistency Custom Rubric
- File: `evals/registry/modelgraded/fact.yaml`
- Code Reference: Multi-option consistency check (from `docs/eval-templates.md`)
```yaml
# Uses custom criteria checking if answer is:
# - subset of expert answer (option A)
# - superset of expert answer (option B)  
# - equal to expert answer (option C)
# - contradicts expert answer (option D/E)
# Domain-specific multi-stage comparison beyond standard categories
```
Implements domain-specific factual consistency evaluation with custom multi-option rubric. The evaluation checks whether answers are subsets, supersets, equal to, or contradicting expert answers, providing nuanced comparison beyond binary correctness.

Evidence 3: Criteria-Based Assessment
- File: `evals/registry/modelgraded/closedqa.yaml`
- Code Reference: Custom criteria checking (from `docs/eval-templates.md`)
```yaml
# Implemented as 'criteria-checking' eval
# Specifies evaluation prompt as checking given criterion
# Checks: relevance, conciseness, and correctness through custom rubric
```
Implements generalized criteria-checking evaluation where evaluation prompts specify custom criteria to assess. The approach checks multiple dimensions like relevance, conciseness, and correctness through specialized rubrics tailored to closed-question answering.

Evidence 4: Convergence Measurement
- File: `evals/elsuite/schelling_point/eval.py`
- Code Reference: Multi-instance convergence checking
```
def measure_convergence():
    converged_no_ci = len(set(completions_no_ci)) == 1
    # Measures if multiple model instances converge on same answer
    # Combines reference-free convergence with comparative analysis
```
Custom evaluation measuring whether multiple model instances converge on the same answer without communication. This combines reference-free convergence metrics with comparative analysis across model copies, creating a specialized coordination assessment.

Evidence 5: Hybrid Retrieval Pipeline
- File: `evals/completion_fns/retrieval.py`
- Code Reference: RetrievalCompletionFn class
```
class RetrievalCompletionFn:
    """
    Uses embeddings to retrieve the top k relevant docs from a dataset
    to the prompt, then adds them to the context
    """
    # Custom hybrid pipeline combining embeddings-based retrieval with completion
```
Implements custom multi-stage evaluation workflow combining embeddings-based retrieval with completion generation. The pipeline first retrieves relevant documents using embeddings, then augments prompts with retrieved context, creating a hybrid evaluation approach.

Evidence 6: Dual Evaluation with Delta Metrics
- File: `evals/elsuite/skill_acquisition/eval.py`
- Code Reference: Retrieval vs non-retrieval comparison
```
def dual_evaluation():
    non_retrieval_out = self._eval_non_retrieval_sample()
    retrieval_out = self._eval_retrieval_sample()
    
    # Computes delta metrics between approaches
    delta_accuracy = retrieval_accuracy - baseline_accuracy
```
Runs both retrieval-augmented and non-retrieval experiments per sample, then computes delta metrics comparing the two approaches. This custom evaluation design measures the value added by retrieval through differential performance analysis.