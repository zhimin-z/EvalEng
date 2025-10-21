## Comparison Criteria Categories

[Custom]

## Detailed Analysis

### Custom

The EvalAI platform enables challenge hosts to implement custom evaluation logic tailored to their specific benchmarking requirements. The evaluation harness provides a flexible architecture where comparison criteria are defined by user-uploaded scripts rather than predetermined by the platform.

Evidence 1: Custom Evaluation Script Upload
- File: `apps/challenges/models.py`
- Code Reference: Challenge model evaluation_script field
```
class Challenge(TimeStampedModel):
    evaluation_script = models.FileField(
        upload_to=RandomFileName("evaluation_scripts"),
        null=True,
        blank=True
    )
    # Allows challenge hosts to upload Python scripts implementing
    # custom comparison logic for their benchmark tasks
```
Challenge hosts upload custom evaluation scripts that define how participant submissions are scored against reference data. The platform does not impose specific comparison methods—hosts implement their own logic for comparing model outputs to ground truth labels, reference outputs, baseline models, or any other standard they define.

Evidence 2: Dynamic Evaluation Script Execution
- File: `scripts/workers/submission_worker.py`
- Code Reference: Submission evaluation pipeline
```
def evaluate_submission(challenge_pk, submission_pk, user_annotation_file_path):
    # Loads challenge-specific evaluation script
    challenge_evaluation_module = load_challenge_evaluation_script(challenge_pk)
    
    # Executes custom evaluation logic
    result = challenge_evaluation_module.evaluate(
        test_annotation_file=annotation_file_path,
        user_annotation_file=user_annotation_file_path,
        phase_codename=phase_codename
    )
    # Returns metrics computed by user-defined comparison criteria
```
The submission worker dynamically loads and executes challenge-specific evaluation modules. Each module implements custom comparison logic—whether comparing against explicit labels, computing similarity metrics, running behavioral tests, or applying domain-specific validation rules determined entirely by the challenge host.

Evidence 3: Flexible Reference Data Configuration
- File: `apps/challenges/models.py`
- Code Reference: ChallengePhase test annotation configuration
```
class ChallengePhase(TimeStampedModel):
    test_annotation = models.FileField(
        upload_to=RandomFileName("test_annotations"),
        null=True,
        blank=True
    )
    # Reference data used by custom evaluation scripts
    # Can contain ground truth labels, reference outputs, or any comparison standard
```
Challenge phases store reference data in the `test_annotation` field, which is passed to custom evaluation scripts. The platform treats this as opaque data—the interpretation and usage is entirely determined by the user-defined evaluation logic, supporting diverse comparison approaches from classification accuracy to generative quality metrics.

Evidence 4: Custom Metric Result Storage
- File: `apps/jobs/models.py`
- Code Reference: Submission result field
```
class Submission(TimeStampedModel):
    result = JSONField(null=True, blank=True)
    # Stores evaluation metrics computed by custom scripts
    # Structure and semantics defined by challenge-specific evaluation logic
```
Submission results are stored as JSON with structure determined by custom evaluation scripts. The platform does not validate or interpret these metrics—challenge hosts define what metrics are computed, how they are calculated, and what comparison criteria are applied, enabling arbitrary evaluation approaches tailored to specific benchmarking needs.

Evidence 5: Evaluation Module Interface Contract
- File: Documentation architectural reference
- Code Reference: Required evaluation function signature
```
def evaluate(test_annotation_file, user_annotation_file, phase_codename):
    """
    Custom evaluation logic implementation.
    Hosts define comparison criteria by implementing this interface.
    
    Args:
        test_annotation_file: Reference data path (ground truth, baselines, etc.)
        user_annotation_file: Participant submission path
        phase_codename: Challenge phase identifier
    
    Returns:
        Dict with custom metrics computed via user-defined comparison
    """
    # Implementation entirely determined by challenge host
    pass
```
The evaluation interface requires hosts to implement an `evaluate()` function that receives reference data and participant submissions. The platform enforces no constraints on comparison methodology—hosts implement arbitrary comparison logic, from simple accuracy calculations against explicit labels to complex multi-stage evaluation pipelines with domain-specific criteria.