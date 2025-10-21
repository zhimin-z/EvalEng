## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: String matching comparison in Match eval
- File: `evals/elsuite/basic/match.py` (referenced in `docs/eval-templates.md`)
- Code Reference:
```python
# From documentation: "basic/match.py:Match": "any([a.startswith(b) for b in B])"
```
The `Match` eval template compares model completions against expected answers using string matching operations without executing generated code. This performs direct text comparison on model outputs, examining the textual structure and content through pattern matching rather than executing any computational logic.

Evidence 2: Substring containment checking in Includes eval
- File: `evals/elsuite/basic/includes.py` (referenced in `docs/eval-templates.md`)
- Code Reference:
```python
# From documentation: "basic/includes.py:Includes": "any([(b in a) for b in B])"
```
The `Includes` eval template checks if expected strings are contained in model outputs through substring matching. This is a simple containment check without execution, analyzing the surface form of text to determine if required elements are present.

Evidence 3: Bidirectional fuzzy string matching
- File: `evals/elsuite/basic/fuzzy_match.py` (referenced in `docs/eval-templates.md`)
- Code Reference:
```python
# From documentation: "basic/fuzzy_match.py:FuzzyMatch": "any([(a in b or b in a) for b in B])"
```
This performs fuzzy string matching between model outputs and expected answers, allowing for partial matches in either direction. The evaluation compares textual representations without executing any generated code or artifacts.

Evidence 4: JSON structure validation and comparison
- File: `evals/elsuite/basic/json_match.py` (referenced in `docs/eval-templates.md`)
- Code Reference:
```python
# From documentation: "yields a match if `a` is identical to at least one answer from `B`... Invalid JSON never matches."
```
This validates and compares JSON-formatted model outputs against expected JSON structures through parsing and comparison, not execution. The evaluation checks structural equivalence and data matching within JSON documents without running any code contained within them.

Evidence 5: Text normalization and fuzzy matching utilities
- File: `evals/elsuite/utils_test.py`
- Code Reference:
```python
def test_normalize(s: str, expected: str):
    assert normalize(s) == expected

def test_fuzzy_match(s1: str, s2: str, expected: bool):
    assert fuzzy_match(s1, s2) == expected
```
These tests validate normalization and fuzzy matching utilities that perform syntactic analysis on text without execution. The functions process string transformations and similarity comparisons, operating purely on textual representations.

Evidence 6: Model-graded classification with choice parsing
- File: `evals/elsuite/modelgraded/classify.py` (referenced in `docs/eval-templates.md`)
- Code Reference:
```python
# From documentation: "choice_strings: The choices that we expect the model completion to contain... Any other choices returned by the model are parsed into `__invalid__`"
```
Model-graded evaluations parse model responses into predefined choices for classification. This involves parsing and pattern matching without executing model outputs, analyzing the textual content to extract categorical decisions.

Evidence 7: Answer format detection and parsing utilities
- File: `evals/elsuite/skill_acquisition/utils.py` (referenced in `evals/elsuite/skill_acquisition/eval.py`)
- Code Reference:
```python
def answer_detected(output):
    # Pattern matching to detect answer format

def process_answer(output):
    # Extract answer from text

def view_instruction_detected(output):
    # Pattern matching for instructions
```
These functions parse and validate model output formats through string operations and pattern matching. They analyze textual structure to detect specific patterns and extract information without executing any generated logic.

Evidence 8: Violation detection through response parsing
- File: `evals/elsuite/already_said_that/utils.py` (referenced in `evals/elsuite/already_said_that/eval.py`)
- Code Reference:
```python
# Contains parse_solver_output function
```
This contains `parse_solver_output` which analyzes model responses to detect violations and extract information through parsing, not execution. The utility examines text to identify constraint violations through pattern recognition.

Evidence 9: Statistical metric computation from events
- File: `evals/metrics.py`
- Code Reference:
```python
def get_accuracy(events: Sequence[Event]) -> float:
    num_correct = sum(int(event.data["correct"]) for event in events)
    num_total = len(events)
    return num_correct / num_total

def get_confusion_matrix(matches: Sequence[Event], class_labels: Optional[Set] = None):
    # Analyzes match events to build confusion matrix
```
These functions compute metrics by analyzing recorded evaluation events, performing statistical analysis on outputs without execution. They aggregate and analyze evaluation results through mathematical operations on collected data.

Evidence 10: Chess notation syntax validation
- File: `evals/elsuite/cant_do_that_anymore/chess/notation.py` (referenced in `evals/elsuite/cant_do_that_anymore/eval.py`)
- Code Reference:
```python
# AlgebraicNotationParser implementation
```
The `AlgebraicNotationParser` parses chess move notation to validate syntax without executing moves on a real chess engine. This verifies that generated moves conform to proper algebraic notation format through syntactic analysis.

---

### Dynamic Execution

Evidence 1: Chess move execution in game simulation
- File: `evals/elsuite/cant_do_that_anymore/chess/board.py` and `evals/elsuite/cant_do_that_anymore/eval.py`
- Class: `BoardController`
- Code Reference:
```python
class BoardController:
    def update_board(self, move):
        # Executes chess moves

# From eval.py:
def construct_controller(piece_id_to_instance: Dict[int, Piece]) -> BoardController:
    controller = BoardController(...)
    for move in previous_moves:
        controller.update_board(move)  # Executing model-generated moves
    return controller
```
This executes model-generated chess moves in a chess game simulation. The moves are generated by the model and then executed on the board state to validate legality and determine game outcomes, testing the functional correctness of generated moves through actual game state manipulation.

Evidence 2: Game simulation for move validation
- File: `evals/elsuite/cant_do_that_anymore/chess/board_test.py`
- Function: `simulate_games()`
- Code Reference:
```python
def simulate_games():
    """Simulates full chess games..."""
    for _ in range(N_GAMES):
        my_controller = BoardController(...)
        # Pick random move
        move = random.choice(our_legal_moves)
        my_controller.update_board(move)  # Execute move
```
This test harness executes chess moves to validate the board controller's move execution logic. It runs complete game simulations to ensure that the move execution mechanism correctly handles legal moves and game state transitions.

Evidence 3: Function deduction through query execution
- File: `evals/elsuite/function_deduction/eval.py`
- Function: `eval_sample()`
- Code Reference:
```python
def eval_sample(self, solver: Solver, sample: Sample, rng: random.Random):
    test_inputs = rng.sample(range(101), 3)
    values = sample.values  # Function values to test against
    expected = tuple(sample.values[test_input] for test_input in test_inputs)
    
    # Model queries function and gets results
    result = values[ask] if ask not in test_inputs else None

# From sample structure:
@dataclass(frozen=True)
class Sample:
    code: str  # Python code defining the function
    values: List[int]  # Pre-computed function values
```
While the code shows pre-computed values, the sample contains `code: str` which represents executable Python code (`"lambda x: " + sample.code`). The evaluation tests if the model can deduce the function by querying it, which involves executing the function logic (though pre-computed in this implementation for efficiency). The evaluation framework tests functional understanding through execution-based queries.

Evidence 4: Reinforcement learning action execution
- File: `evals/elsuite/incontext_rl/eval.py`
- Function: `eval_sample()`
- Code Reference:
```python
def eval_sample(self, solver: Solver, sample: Any, rng: random.Random):
    env = sample["env"]  # Gymnasium environment
    observation, _ = env.reset(seed=42)
    
    for _ in range(self.max_steps):
        action = self._try_get_valid_action(solver, ts, env.action_space.n)
        # Execute model-generated action
        next_observation, reward, terminated, truncated, _ = env.step(action)
```
This executes model-generated actions in a Gymnasium environment (reinforcement learning simulator). The model outputs actions which are then executed in the environment to produce state transitions and rewards, directly testing behavioral correctness through environmental interaction.

Evidence 5: Card game move execution
- File: `evals/elsuite/bluff/eval.py`
- Function: `eval_sample()`
- Code Reference:
```python
def eval_sample(self, solver: Solver, sample_ix: int, rng: random.Random):
    game = Game(self.num_rounds, starting_player=sample_ix % 2, rng=rng)
    player_0 = SolverPlayer(game, solver)  # Solver controls player actions
    
    try:
        game.play()  # Execute game with model-generated moves
```
This executes a card game where the model generates game actions (bids, bluff calls) that are executed in the game environment to determine outcomes. The evaluation tests strategic decision-making through actual game play execution.

Evidence 6: Coordination protocol execution
- File: `evals/elsuite/schelling_point/eval.py`
- Function: `eval_sample()`
- Code Reference:
```python
def eval_sample(self, sample: Any, *_):
    for i, completion_fn in enumerate(self.completion_fns):
        prompt = sample[f"{i}"]
        # Get model response and execute coordination logic
        completion, scratchpad = get_response(completion_fn, sys_prompt_no_ci, prompt, self.temperature)
        completions_no_ci.append(completion)
    
    # Check if coordination succeeded
    converged_no_ci = len(set(completions_no_ci)) == 1
```
While not traditional code execution, this executes a coordination protocol where model outputs (coordination choices) are processed to determine if convergence occurred - a form of executing game-theoretic logic with model-generated moves. The evaluation tests coordination capabilities through protocol execution.

Evidence 7: Retrieval computation execution
- File: `evals/completion_fns/retrieval.py`
- Code Reference:
```python
def __call__(self, prompt: Union[str, list[dict]], **kwargs: Any):
    # Embed the prompt
    embedded_prompt = client.embeddings.create(...)
    
    # Execute similarity search
    topk = " ".join(self.embeddings_df.iloc[
        find_top_k_closest_embeddings(embedded_prompt, embs, k=self.k)
    ].text.values)
```
This executes embedding computations and similarity searches as part of the retrieval pipeline, processing model queries through executable search algorithms. The evaluation tests information retrieval capabilities through actual computational execution of embedding and search operations.