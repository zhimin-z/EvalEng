# EvalAI - Stage 2 (PREPARE) Evaluation

## Summary
EvalAI is a web platform for hosting AI challenges, not an evaluation framework/harness for dataset preprocessing or model evaluation. It focuses on challenge management, submission handling, and leaderboard generation. It lacks most Stage 2 preparation features as it's designed for challenge orchestration rather than data preparation workflows.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 0 | No data preprocessing utilities exist. The platform expects challenge hosts to provide pre-prepared test annotation files (e.g., `test_annotation_file: annotations/test_annotations_devsplit.json` in `examples/example1/test_zip_file/zip_challenge.yaml`). No tokenization, normalization, caching, or splitting functionality is provided. Users must prepare data externally. |
| S2F2: Quality Assessment | 0 | No dataset quality assessment tools. No label quality checking, demographic analysis, duplicate detection, or bias detection features. The system only validates submission format (e.g., `allowed_submission_file_types: ".json, .zip, .txt, .tsv, .gz, .csv, .h5, .npy"` in `docs/source/configuration.md`), not data quality. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features. The platform handles challenge data as-is without privacy scanning. Documentation mentions `allowed_email_domains` and `blocked_emails_domains` for participant access control but no content-level PII handling exists. |
| S2F4: Infrastructure Building | 0 | No infrastructure building utilities for retrieval systems, databases, or specialized environments. The platform uses PostgreSQL for its own data (`docs/source/architecture.md` mentions "PostgreSQL is used as our primary datastore") but provides no tools for challenge-specific infrastructure. No FAISS, Elasticsearch, or vector DB support. |
| S2F5: Model Artifact Validation | 0 | No model validation features. The system validates submission file formats but not model checksums, versions, or integrity. File type validation is basic: `allowed_submission_file_types` accepts specific extensions but performs no cryptographic verification or corruption detection. |
| S2F6: Evaluation Scenario Generation | 0 | No scenario generation capabilities. The platform expects static test sets provided by hosts. Challenge phases (`challenge_phases` in config) define evaluation stages, but no dynamic prompt variation, multi-turn dialogue generation, or edge case creation exists. Evaluation runs on fixed annotation files. |
| S2F7: Red-Teaming | 0 | No red-teaming or adversarial testing framework. The platform evaluates user submissions against ground truth but provides no jailbreak libraries, prompt injection tests, or bias probing. Security is limited to participant authentication and submission limits (`max_submissions_per_day` in config). |
| S2F8: Contamination Detection | 0 | No contamination detection. No ability to compare evaluation data against training corpora, perform n-gram overlap analysis, or semantic similarity checks. The system assumes hosts provide clean, non-contaminated test sets without providing verification tools. |

## Detailed Analysis

### Evidence of Missing Preparation Features

1. No Data Processing Pipeline
From `docs/source/configuration.md`:
```yaml
test_annotation_file: This file is used for ranking the submission made by a participant.
```
The platform expects pre-prepared annotation files with no preprocessing support.

2. Evaluation Script Structure
From `docs/source/02-for-challenge-hosts/evaluation/evaluation-scripts.md`:
```python
def evaluate(test_annotation_file, user_annotation_file, phase_codename, kwargs):
    # Custom evaluation logic here
    pass
```
The evaluation function receives file paths but no preprocessing utilities. All data preparation must be done externally.

3. Example Configuration
From `examples/example1/test_zip_file/zip_challenge.yaml`:
```yaml
evaluation_script: evaluation_script.zip
test_annotation_file: test_annotation.txt
```
Challenge hosts must provide both evaluation scripts AND prepared test data - no platform-level data preparation.

4. Submission Processing
From `docs/source/03-for-participants/submissions/submission-status.md`:
```python
# Worker downloads submission and runs evaluation
submission_output = EVALUATION_SCRIPTS[challenge_id].evaluate(*params)
```
The worker invokes custom evaluation scripts but provides no data quality checks, preprocessing, or contamination detection.

5. No Infrastructure Utilities
From `scripts/workers/submission_worker.py` structure (inferred from docs):
- Workers load challenge evaluation scripts dynamically
- No mention of index building, database setup, or retrieval system integration
- Focus is on message queue processing (Amazon SQS) for submission handling

6. Architecture Focus
From `docs/source/04-development/architecture/system-architecture.md`:
```
Django Rest Framework → Amazon SQS → Submission Workers → PostgreSQL
```
Architecture designed for web service orchestration, not data preparation pipelines.

### What EvalAI Actually Does

EvalAI is a challenge hosting platform that:
- Manages challenge metadata (title, dates, phases)
- Handles user submissions via web interface
- Queues submissions through Amazon SQS
- Runs custom evaluation scripts provided by hosts
- Maintains leaderboards
- Provides participant/host authentication

It is not an evaluation harness that prepares datasets, builds infrastructure, or validates data quality.

## Conclusion

EvalAI scores 0/24 on Stage 2 (PREPARE) as it is fundamentally a challenge management platform, not a data preparation framework. Challenge hosts must:
- Prepare datasets externally
- Write custom evaluation scripts
- Provide pre-validated test annotations
- Handle all data quality, preprocessing, and infrastructure needs independently

The platform excels at submission orchestration and leaderboard management but provides no data preparation utilities. For Stage 2 capabilities, users would need to combine EvalAI with external tools (HuggingFace Datasets for preprocessing, custom scripts for quality checks, etc.).