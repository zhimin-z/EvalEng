## Evaluator Categories

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
EvalAI provides a plugin architecture where challenge hosts upload custom Python evaluation scripts that define how participant submissions should be evaluated. Unlike standardized evaluation harnesses that provide fixed evaluator implementations, EvalAI serves as infrastructure that executes user-defined evaluation logic. Each challenge implements its own evaluator through these uploaded scripts, making every evaluation setup custom by design. This approach enables diverse evaluation methodologies ranging from traditional metric-based assessment to complex domain-specific evaluation procedures.

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
The submission worker dynamically loads and executes challenge-specific evaluation scripts at runtime, implementing a custom evaluator pattern where evaluation logic is defined per-challenge rather than built into the platform. This architecture means EvalAI does not provide standardized evaluators (algorithmic, ML-based, environmental, or human) but instead provides the infrastructure for challenge organizers to implement any evaluator type they choose. The actual evaluation methodology—whether rule-based metrics, model-based scoring, or other approaches—is entirely determined by the custom script uploaded by each challenge host.

Evidence 3: Flexible reference data and metric computation
- File: `apps/challenges/models.py`
- Class: `ChallengePhase`
- Code Reference:
```python
class ChallengePhase:
    test_annotation = models.FileField(...)  # Reference data
    # Metrics computed by custom evaluation script
    # Can compare against annotations, baselines, or custom criteria
```
Challenge phases support arbitrary reference data through the `test_annotation` field, which custom evaluation scripts can use according to their specific evaluation methodology. The platform does not prescribe how this reference data should be used—it could serve as ground truth labels for algorithmic metrics, reference outputs for comparison-based evaluation, test cases for code execution environments, or any other purpose defined by the custom evaluator. This flexibility reinforces that EvalAI is infrastructure for hosting custom evaluators rather than a standardized evaluation harness.

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
Submission results are stored in a flexible JSON field that accommodates any evaluation output structure defined by custom scripts. Unlike standardized harnesses that enforce specific metric schemas (e.g., accuracy, BLEU scores, pass@k rates), EvalAI allows each challenge to define its own evaluation output format. This design enables custom evaluators to return domain-specific metrics, multi-faceted assessment results, or any evaluation data structure appropriate for their benchmarking goals, confirming that the platform serves as infrastructure for custom evaluation implementations rather than providing built-in standardized evaluators.