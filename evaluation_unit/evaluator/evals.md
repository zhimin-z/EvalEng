## Evaluator Categories

[Algorithmic, ML-based, Environmental, Human, Custom]

## Detailed Analysis

### Algorithmic

Evidence 1: Core mathematical evaluation metrics
- File: `evals/metrics.py`
- Function: `get_accuracy()`, `get_confusion_matrix()`, `compute_precision()`, `compute_recall()`, `compute_f_score()`, `get_bootstrap_accuracy_std()`
- Code Reference:
```python
get_accuracy()
get_confusion_matrix()
compute_precision()
compute_recall()
compute_f_score()
get_bootstrap_accuracy_std()
```
This file defines multiple algorithmic metrics that are applied to model outputs. Functions like `get_accuracy()` compute the proportion of correct answers from recorded events, `get_confusion_matrix()` builds confusion matrices from match events, and various precision/recall/F-score functions perform mathematical calculations on evaluation results. These are deterministic, rule-based metrics used throughout the evaluation framework.

Evidence 2: BLEU score text comparison
- File: `evals/elsuite/skill_acquisition/utils.py` (referenced in `evals/elsuite/skill_acquisition/eval.py`)
- Function: `get_bleu_score()`, `get_average_bleu_score()`
- Code Reference:
```python
"bleu": get_bleu_score(sample["ideal"], answer)
```
The BLEU score mentioned in the evaluation pipeline is a standard algorithmic metric for text comparison, commonly used in translation tasks. It's a deterministic string-matching algorithm that compares n-grams between model outputs and reference texts without requiring external models or human judgment.

Evidence 3: Basic string matching evaluators
- File: `evals/elsuite/basic/` directory (referenced in `docs/eval-templates.md`)
- Code Reference:
```python
# basic/match.py:Match
any([a.startswith(b) for b in B])

# basic/includes.py:Includes
any([(b in a) for b in B])

# basic/fuzzy_match.py:FuzzyMatch
any([(a in b or b in a) for b in B])

# basic/json_match.py:JsonMatch
# compares JSON objects for equality
```
According to the documentation, the framework provides several basic algorithmic evaluators that implement deterministic string and JSON comparison operations. These perform simple pattern matching without requiring machine learning models or external systems.

Evidence 4: Text normalization and fuzzy matching utilities
- File: `evals/elsuite/utils_test.py`
- Function: `test_fuzzy_match()`, `test_normalize()`
- Code Reference:
```python
test_fuzzy_match()
test_normalize()
```
These test functions verify algorithmic string matching functions like `fuzzy_match()` and `normalize()`, which are deterministic text processing algorithms used for evaluation. They standardize text formatting and perform approximate string matching using rule-based approaches.

Evidence 5: Exact match verification
- File: `evals/api.py` (referenced throughout codebase)
- Function: `record_and_check_match()`
- Code Reference:
```python
record_and_check_match()
```
Referenced throughout the codebase in documentation and various eval implementations, this function performs exact matching between model outputs and expected answers, which is an algorithmic comparison based on string equality without external dependencies.

---

### ML-based

Evidence 1: Model-based classification evaluator
- File: `evals/elsuite/modelgraded/classify.py` (referenced in `docs/eval-templates.md`)
- Class: `ModelBasedClassify`
- Code Reference:
```python
ModelBasedClassify
```
The documentation explicitly describes model-graded evaluations where "the evaluation model and the model being evaluated don't have to be the same." The system uses an ML model to grade outputs by wrapping them in an evaluation prompt and parsing the model's response. This is clearly an LLM-as-judge approach where one model evaluates another's outputs.

Evidence 2: Model-graded evaluation framework
- File: `docs/eval-templates.md`
- Code Reference:
```python
eval_type: "cot_classify"
# "In cases where the desired model response can contain significant variation,
# such as answering an open-ended question, we have found that using the model
# to grade itself is a viable strategy for automated evaluation."
```
The documentation describes extensive use of ML-based evaluation, including chain-of-thought classification where models reason about outputs before grading them. The template includes parameters like `eval_type` with options for chain-of-thought classification, demonstrating that models are used as sophisticated evaluators rather than simple pattern matchers.

Evidence 3: Pre-configured model-graded evaluators
- File: `evals/registry/modelgraded/` directory (referenced in docs)
- Code Reference:
```yaml
# fact.yaml - factual consistency eval
# closedqa.yaml - question answering eval
# battle.yaml - head-to-head comparison
# humor.yaml - humor evaluation
```
The documentation describes multiple model-graded evaluators stored in YAML files that use ML models to assess different aspects of outputs: factual consistency, answer quality (relevance, conciseness, correctness), comparative performance, and subjective qualities like humor. These represent diverse ML-based evaluation approaches.

Evidence 4: Model-graded evaluation generator
- File: `scripts/modelgraded_generator.py`
- Code Reference:
```python
unlabeled_prompts
modelgraded_spec: "humor_jp"
eval_type: "cot_classify_jp"
```
This script generates model-graded evaluations, specifically referencing humor evaluation with chain-of-thought classification. This demonstrates automated generation of ML-based evaluation configurations, where models are used to judge subjective qualities that would be difficult to assess algorithmically.

Evidence 5: Embedding-based retrieval evaluation
- File: `evals/completion_fns/retrieval.py`
- Class: `RetrievalCompletionFn`
- Code Reference:
```python
client.embeddings.create(model=self.embedding_model, ...)
find_top_k_closest_embeddings()
# using cosine similarity
```
This uses embeddings to retrieve relevant documents and finds the top k closest embeddings using cosine similarity. While embeddings are used for retrieval rather than direct evaluation, this represents an ML-based component in the evaluation pipeline that leverages neural network embeddings to assess semantic similarity.

---

### Environmental

Evidence 1: Reinforcement learning gym environment evaluation
- File: `evals/elsuite/incontext_rl/eval.py`
- Class: `InContextRl`
- Code Reference:
```python
env = sample["env"]
observation, _ = env.reset(seed=42)
next_observation, reward, terminated, truncated, _ = env.step(action)
```
This evaluator explicitly uses OpenAI Gym environments to evaluate model performance. The environment provides feedback (observations, rewards, termination signals) based on the model's actions. This is clearly environmental evaluation where a simulator provides task-specific feedback. The evaluation records metrics like `total_return`, `episode_rewards`, and `average_episode_reward` based on environment responses.

Evidence 2: Gym environment setup configuration
- File: `evals/elsuite/incontext_rl/env_setup.py` (referenced)
- Code Reference:
```python
ENV_SETUP_FUNCS
```
The code references `ENV_SETUP_FUNCS` which contains setup scripts for specific gym environments, confirming the use of external simulation environments for evaluation. This demonstrates that the system supports multiple different simulated environments with custom initialization logic.

Evidence 3: Chess board simulator
- File: `evals/elsuite/cant_do_that_anymore/chess/board.py`
- Class: `BoardController`
- Code Reference:
```python
default_controller = BoardController(...)
variant_controller = BoardController(...)
```
The chess evaluator uses a chess board simulator to validate moves. The simulator determines legal moves, validates model-generated chess moves, and provides feedback on violations. This is environment-based evaluation where a chess engine provides task feedback based on game rules and state.

Evidence 4: Chess move validation through environment
- File: `evals/elsuite/cant_do_that_anymore/eval.py`
- Function: `get_violations()`
- Code Reference:
```python
move = controller.notation_parser._str_to_move(...)
piece_moved_outside_board = not move_within_board(move)
```
This method validates model chess moves against the game environment by checking if moves are legal according to chess rules. The chess board controller acts as an environment that validates moves and detects violations like moving outside the board or capturing same-color pieces, providing structured feedback on rule compliance.

Evidence 5: Chess game simulation and validation
- File: `evals/elsuite/cant_do_that_anymore/chess/board_test.py`
- Function: `simulate_games()`
- Code Reference:
```python
simulate_games()
```
The test simulates full chess games and compares legal moves against the python-chess library, demonstrating that the board controller is used as an environment to evaluate model chess playing ability. This validates that the environment correctly implements chess rules and can serve as a ground truth for evaluation.

Evidence 6: Card game environment simulation
- File: `evals/elsuite/bluff/eval.py`
- Class: `BluffEval` with `Game` class
- Code Reference:
```python
game = Game(self.num_rounds, starting_player=sample_ix % 2, rng=rng)
game.play()
```
This evaluator uses a game environment to simulate the Bluff card game. The game provides feedback on valid moves and game outcomes, acting as an environment for evaluation. The environment maintains game state, enforces rules, and determines winners based on gameplay.

---

### Human

Evidence 1: Human-in-the-loop CLI solver
- File: `evals/solvers/human_cli_solver.py` (referenced in `evals/elsuite/bluff/eval.py`)
- Class: `HumanCliSolver`
- Code Reference:
```python
if self.opponent_name == "human_cli":
    return self._create_human_player(game)
# human_cli player is available only with EVALS_SEQUENTIAL=1
```
Multiple eval files reference `HumanCliSolver`, and the system explicitly supports human-in-the-loop evaluation where a human provides responses that are then evaluated. This allows direct human participation in the evaluation process, with human actions serving as either baselines or test subjects.

Evidence 2: Human evaluation framework documentation
- File: `docs/eval-templates.md`
- Code Reference:
```markdown
Human evaluation: Manual annotation and expert judgment for evaluating model outputs
Examples: Human preference ratings, expert evaluations, crowdsourced annotations,
manual quality assessments, human feedback on task completions
```
The documentation describes human evaluation as a distinct category involving manual annotation and expert judgment. This includes various forms of human feedback mechanisms that provide qualitative and subjective assessments that automated systems cannot easily replicate.

Evidence 3: Human player integration in game evaluation
- File: `evals/elsuite/bluff/eval.py`
- Function: `_create_human_player()`
- Code Reference:
```python
@staticmethod
def _create_human_player(game: Game) -> Player:
    if os.environ.get("EVALS_SEQUENTIAL") != "1":
        raise ValueError("human_cli player is available only with EVALS_SEQUENTIAL=1")
    solver = HumanCliSolver()
    return SolverPlayer(game, solver)
```
This method creates a human player using `HumanCliSolver()`, allowing human experts to play against the model. Their performance serves as an evaluation benchmark, providing ground truth for how well models perform compared to human-level play in strategic games.

---

### Custom

Evidence 1: Multi-agent coordination evaluation
- File: `evals/elsuite/schelling_point/eval.py`
- Class: `SchellingPoint`
- Code Reference:
```python
for i, completion_fn in enumerate(self.completion_fns):
    prompt = sample[f"{i}"]
    sys_prompt_no_ci = random.choice(sys_prompts_no_ci)
    completion, scratchpad = get_response(...)
converged_no_ci = len(set(completions_no_ci)) == 1
```
This evaluator implements a custom multi-agent coordination task where multiple models attempt to converge on the same answer without communication (Schelling point). This is a specialized evaluation that checks coordination ability by combining multiple model calls with custom convergence logic. It's not a standard metric, model grading, or simple environmental feedback.

Evidence 2: Memory tracking across conversation turns
- File: `evals/elsuite/already_said_that/eval.py`
- Class: `AlreadySaidThat`
- Code Reference:
```python
def _conversation_loop(self, solver, words, distractor_data, rng):
    words_prev_shown = set()
    words_not_shown = set(words)
    words_from_solver = set()
    words_from_distractors = set()
    ...
    message, message_words, distractor_added = utils.build_message(...)
```
This implements a custom memory-tracking evaluation with complex multi-turn conversation logic. It tracks what words have been shown to the model, manages distractor questions, and evaluates the model's ability to remember previous information across a conversation. This specialized task requires custom state management and evaluation criteria.

Evidence 3: Interactive function deduction game
- File: `evals/elsuite/function_deduction/eval.py`
- Class: `FunctionDeductionEval`
- Code Reference:
```python
for round_ix in range(self.n_rounds):
    ...
    if len(ints) == 1:
        ask = ints[0]
        result = values[ask] if ask not in test_inputs else None
    else:
        cs.guess_update(ints, expected)
```
This implements a custom interactive game where the model tries to deduce a hidden function through queries. The evaluation involves a custom protocol for querying function values and making guesses, with specialized parsing and game-state management. This tests reasoning and hypothesis formation abilities through a unique task design.

Evidence 4: Combined retrieval and non-retrieval skill evaluation
- File: `evals/elsuite/skill_acquisition/eval.py`
- Class: `SkillAcquisition`
- Code Reference:
```python
non_retrieval_out = self._eval_non_retrieval_sample(non_retrieval_solver, sample)
retrieval_out = self._eval_retrieval_sample(retrieval_solver, sample)

def _conversation_loop(self, solver, task_state):
    ...
    if view_instruction_detected(output):
        file, section = process_view_instruction(output)
        content, sections_visible_to_model, sections_viewed = self._view_content(...)
```
This implements a complex custom evaluation pipeline combining retrieval and non-retrieval phases. The retrieval phase includes a custom conversation loop where the model can request to view files and sections. This is a specialized evaluation combining retrieval, conversation management, and custom instruction parsing to assess learning and information gathering abilities.

Evidence 5: Persuasion dynamics with logit bias control
- File: `evals/elsuite/ballots/eval.py`
- Class: `BallotsEval`
- Code Reference:
```python
def query(prompt, fn, reversed_roles=False, max_tokens=2_000, **kwargs):
    ...
    if "logit_bias" not in kwargs:
        if fn.model in {"gpt-4-base"}:
            kwargs["logit_bias"] = {
                id: LOGIT_BIAS_MIN
                for id in toks_to_id(fn.model, BASE_REMOVED_TOKS + ALL_DOUBLE_NEWLINE_TOKS)
            }
```
This custom evaluation tests influence dynamics between an influencer and voter model with specialized token bias controls and multi-turn conversation tracking. It manipulates model behavior through logit biases while evaluating persuasion and influence capabilities, representing a highly specialized evaluation approach that combines prompt engineering with low-level model control.