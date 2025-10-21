## Evaluation Mode Categories

[Custom]

## Detailed Analysis

### Custom

Evidence 1: Custom evaluation script architecture
- File: `apps/challenges/models.py`
- Class: `Challenge`
- Code Reference:
```python
class Challenge:
    evaluation_script = models.FileField(upload_to=...)
    # Allows hosts to upload custom Python scripts that implement
    # evaluation logic tailored to their specific challenge requirements
```
EvalAI provides a plugin architecture where challenge hosts upload custom Python evaluation scripts that define how participant submissions should be evaluated. Unlike standardized evaluation harnesses that provide fixed evaluation mode implementations (e.g., static output analysis, code execution environments, or interactive simulation loops), EvalAI serves as infrastructure that executes user-defined evaluation logic. Each challenge implements its own evaluation mode through these uploaded scripts, making every evaluation setup custom by design. This approach enables diverse interactive methodologies ranging from simple static analysis of prediction files to complex multi-step validation procedures with dynamic execution and feedback loops, all determined by the challenge host's uploaded script.

Evidence 2: Dynamic evaluation script execution
- File: `scripts/workers/submission_worker.py`
- Function: `evaluate_submission()`
- Code Reference:
```python
def evaluate_submission(challenge_id, submission_id):
    # Loads challenge-specific evaluation script
    # Executes custom comparison logic defined by host
    # Returns metrics computed according to custom criteria
```
The submission worker dynamically loads and executes challenge-specific evaluation scripts at runtime, implementing a custom evaluation mode pattern where the evaluation methodology is defined per-challenge rather than built into the platform. This architecture means EvalAI does not enforce a specific evaluation mode (static vs. dynamic vs. simulation) but instead provides the infrastructure for challenge organizers to implement any interactive approach they choose. The actual interaction pattern—whether the script simply reads and scores static outputs, executes generated code in sandboxed environments, orchestrates multi-turn interactions with simulated systems, or implements novel hybrid approaches—is entirely determined by the custom script uploaded by each challenge host. This makes the evaluation mode fundamentally custom and challenge-specific.

Evidence 3: Flexible reference data and interaction configuration
- File: `apps/challenges/models.py`
- Class: `ChallengePhase`
- Code Reference:
```python
class ChallengePhase:
    test_annotation = models.FileField(...)  # Reference data
    # Metrics computed by custom evaluation script
    # Can compare against annotations, baselines, or custom criteria
```
Challenge phases support arbitrary reference data through the `test_annotation` field, which custom evaluation scripts can use according to their specific evaluation mode requirements. The platform does not prescribe how this reference data should be used in the interaction process—it could serve as static ground truth for one-shot comparison (Static Analysis mode), as test cases for code execution validation (Dynamic Execution mode), as initial states for multi-turn simulations (Interactive Simulation mode), or any other purpose defined by the custom evaluator. This flexibility in reference data usage reinforces that EvalAI is infrastructure for hosting custom evaluation modes rather than a standardized evaluation harness with predefined interaction patterns. Challenge hosts have complete control over defining whether their evaluation involves single-pass output assessment, iterative execution with feedback, or complex multi-step interaction sequences.

Evidence 4: User-defined evaluation result structure
- File: `apps/jobs/models.py`
- Class: `Submission`
- Code Reference:
```python
class Submission:
    output = JSONField()  # Stores evaluation results
    # Results computed by custom evaluation script
    # reflecting user-defined comparison criteria
```
Submission results are stored in a flexible JSON field that accommodates any evaluation output structure defined by custom scripts, including outputs that reflect different evaluation mode characteristics. Unlike standardized harnesses that enforce specific result schemas tied to their evaluation mode (e.g., pass/fail for static code checks, execution traces for dynamic testing, or trajectory metrics for interactive simulations), EvalAI allows each challenge to define its own evaluation output format. This design enables custom evaluation modes to return appropriate metrics for their interaction pattern—simple accuracy scores for static analysis, execution logs and test case results for dynamic execution, multi-step performance metrics for interactive simulations, or any specialized data structure appropriate for novel hybrid interactive approaches. This confirms that the platform serves as infrastructure for custom evaluation mode implementations rather than providing built-in standardized interaction patterns.