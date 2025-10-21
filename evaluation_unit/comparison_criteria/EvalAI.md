## Comparison Criteria Categories

[Custom]

## Detailed Analysis

### Custom

Evidence 1: Challenge-Specific Evaluation Scripts
- File: `apps/challenges/models.py`
- Code Reference: Challenge evaluation_script field
```python
class Challenge:
    evaluation_script = models.FileField(upload_to=...)
    # Allows hosts to upload custom Python scripts that implement
    # evaluation logic tailored to their specific challenge requirements
```
Challenge hosts can upload custom evaluation scripts defining how participant submissions should be scored. These scripts implement comparison criteria specific to each challenge, supporting diverse evaluation approaches from explicit label comparison to behavioral validation or hybrid methodologies determined by challenge organizers.

Evidence 2: Dynamic Evaluation Script Execution
- File: `scripts/workers/submission_worker.py`
- Code Reference: Dynamic evaluation script loading
```python
def evaluate_submission(challenge_id, submission_id):
    # Loads challenge-specific evaluation script
    # Executes custom comparison logic defined by host
    # Returns metrics computed according to custom criteria
```
The submission worker dynamically loads and executes challenge-specific evaluation scripts, enabling custom comparison criteria implementation. Each challenge defines unique evaluation logic allowing flexible benchmarking approaches including multi-metric assessments, domain-specific validation, and specialized scoring systems.

Evidence 3: Flexible Metric Configuration
- File: `apps/challenges/models.py`
- Code Reference: ChallengePhase metrics configuration
```python
class ChallengePhase:
    test_annotation = models.FileField(...)  # Reference data
    # Metrics computed by custom evaluation script
    # Can compare against annotations, baselines, or custom criteria
```
Challenge phases support flexible metric definitions through the evaluation script system. The `test_annotation` field provides reference data that custom scripts can use for comparison, but actual comparison logic is user-defined, supporting various evaluation paradigms including explicit labels, behavioral specifications, or novel hybrid approaches.

Evidence 4: Submission Result Storage
- File: `apps/jobs/models.py`
- Code Reference: Submission result storage
```python
class Submission:
    output = JSONField()  # Stores evaluation results
    # Results computed by custom evaluation script
    # reflecting user-defined comparison criteria
```
Submissions store evaluation results computed by custom scripts with scoring logic entirely determined by challenge hosts. This architecture enables diverse comparison criteria implementations from standard metrics like accuracy and F1-score to domain-specific evaluation measures, specialized validation pipelines, and tailored benchmarking requirements specific to each challenge domain.