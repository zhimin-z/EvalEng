## Comparison Criteria Categories

[Explicit Labels, Behavioral Specification, None]

## Detailed Analysis

### Explicit Labels

Evidence 1: Exact Match Scoring
- File: `deepeval/scorer/scorer.py`
- Code Reference: exact_match_score() method
```
def exact_match_score(target: str, prediction: str):
    # compares prediction against target
```
The scorer implements exact match comparison that directly checks whether model predictions match the target reference answer. This is a binary comparison against explicit labels where the model output must exactly reproduce the predetermined correct answer.

Evidence 2: SQuAD-Style Scoring
- File: `deepeval/scorer/scorer.py`
- Code Reference: squad_score() method
```
def squad_score():
    # compares prediction against expected_output
```
The harness implements SQuAD-style evaluation that compares model predictions against `expected_output` labels using F1 and exact match metrics. This represents standard benchmark evaluation where model answers are scored against explicit reference answers from the test dataset.

Evidence 3: Quasi-Exact Match Comparison
- File: `deepeval/scorer/scorer.py`
- Code Reference: quasi_exact_match_score() method
```
def quasi_exact_match_score():
    # normalized comparison against target
```
This scoring method performs normalized string comparison between predictions and target references. While allowing for minor variations (case, whitespace), it fundamentally compares model outputs against explicit labels that define the correct answers for benchmark evaluation.

---

### Behavioral Specification

Evidence 1: GEval Dynamic Evaluation Steps
- File: `deepeval/metrics/g_eval/g_eval.py`
- Code Reference: GEval class definition
```
class GEval:
    evaluation_steps: Optional[List[str]]
    
    def _generate_evaluation_steps(self):
        # generates dynamic validation steps
    
    def _evaluate(self):
        # executes evaluation logic against test cases
```
The GEval framework defines evaluation through a sequence of validation steps that specify how to assess model outputs. These steps represent executable behavioral specifications that dynamically validate whether outputs satisfy the evaluation criteria, rather than comparing against static reference text.

Evidence 2: Conversational GEval Specifications
- File: `deepeval/metrics/conversational_g_eval/conversational_g_eval.py`
- Code Reference: ConversationalGEval class definition
```
class ConversationalGEval:
    evaluation_steps: Optional[List[str]]
    # Dynamic step generation and execution for conversational evaluation
```
For conversational tasks, the harness uses evaluation steps that specify behavioral requirements for multi-turn interactions. These steps define acceptable conversation patterns and outcomes through executable validation logic rather than predetermined reference conversations.

Evidence 3: MCP Primitive Usage Validation
- File: `deepeval/metrics/mcp_use_metric/mcp_use_metric.py`
- Code Reference: MCPUseMetric class methods
```
class MCPUseMetric:
    def _get_primitives_used_score(self):
        # validates MCP primitive usage
    
    def _get_argument_correctness_score(self):
        # validates argument correctness
```
The MCP metrics validate functional correctness by checking whether model outputs correctly use MCP primitives and pass valid arguments. This represents behavioral specification—the validation checks whether tool usage satisfies functional requirements through executable verification rather than text comparison.

Evidence 4: Arena-Style Dynamic Evaluation
- File: `deepeval/metrics/arena_g_eval/arena_g_eval.py`
- Code Reference: ArenaGEval class definition
```
class ArenaGEval:
    # Dynamic evaluation steps for arena-style comparisons
```
Arena evaluation uses dynamically generated assessment criteria to compare model outputs. Rather than using static reference answers, the harness specifies behavioral requirements that outputs must satisfy, with evaluation steps that define acceptable characteristics for winning responses.

Evidence 5: Tool Correctness Validation
- File: `deepeval/metrics/mcp_use_metric/mcp_use_metric.py`
- Code Reference: Argument validation logic
```
def _get_argument_correctness_score(self):
    # validates argument correctness
```
The harness validates whether model-generated tool calls have correct arguments by checking against functional specifications. This is behavioral validation—verifying that tool usage conforms to API specifications and type constraints rather than matching predetermined correct tool calls.

---

### None

Evidence 1: Faithfulness Scoring
- File: `deepeval/scorer/scorer.py`
- Code Reference: faithfulness_score() method
```
def faithfulness_score():
    # measures internal consistency without external reference
```
The faithfulness scorer evaluates whether model outputs are internally consistent with provided context without requiring external reference answers. This intrinsic quality measure assesses the coherence and grounding of generated text based solely on its relationship to the source material.

Evidence 2: Toxicity Detection
- File: `deepeval/scorer/scorer.py`
- Code Reference: neural_toxic_score() method
```
def neural_toxic_score():
    # evaluates toxicity intrinsically using Detoxify model
```
Toxicity evaluation uses the Detoxify model to assess harmful content in model outputs without comparing against reference answers. This is a reference-free quality measure that evaluates intrinsic properties of the generated text to detect toxic language patterns.

Evidence 3: Bias Assessment
- File: `deepeval/scorer/scorer.py`
- Code Reference: neural_bias_score() method
```
def neural_bias_score():
    # assesses bias without comparison targets
```
Bias scoring evaluates model outputs for biased language or stereotypes without requiring reference answers. This intrinsic quality measure analyzes the text itself to identify bias patterns rather than comparing against explicit labels or specifications.

Evidence 4: Hallucination Detection
- File: `deepeval/scorer/scorer.py`
- Code Reference: hallucination_score() method
```
def hallucination_score():
    # evaluates hallucination based on source-prediction coherence
```
The hallucination scorer assesses whether model outputs contain unfounded claims by analyzing coherence between the generated text and source documents. This reference-free evaluation measures output quality based on internal consistency rather than comparison to ground truth.