# EvalAI - Stage 1 (CONFIGURE) Evaluation

## Summary
EvalAI is a web-based platform for hosting AI challenges rather than a traditional evaluation framework. It focuses on challenge configuration through YAML files and web interfaces, with dataset/model configuration happening at the challenge-host level rather than being a general-purpose evaluation tool. Configuration is primarily declarative but tied to the platform's challenge-hosting architecture.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Limited dataset abstraction. EvalAI treats datasets as annotation files uploaded by challenge hosts (`test_annotation_file` in `challenge_config.yaml`), not as discoverable entities. No support for multiple sources (HuggingFace, CSV, APIs, etc.) - only file uploads. Dataset splits exist (`dataset_splits` section) but are declarative mappings to challenge phases, not functional data loaders. No schema definition API or versioning system. Example from `docs/source/configuration.md`: `test_annotation_file: annotations/test_annotations_devsplit.json` - just a file path reference. |
| S1F2: Model Configuration | 0 | No model configuration system. EvalAI is a challenge evaluation platform, not a model evaluation framework. It doesn't configure or manage models - participants submit predictions or code, and the platform evaluates them. The system has no concept of "providers" (OpenAI, Anthropic, etc.) or model parameters. The architecture (`docs/source/architecture.md`) shows it uses Django REST APIs and workers to process submissions, but no model configuration. |
| S1F3: Prompt Configuration | 0 | No prompt system. This is not an LLM evaluation framework. There's no templating engine, no prompt versioning, no few-shot support. Metrics are configured in `leaderboard.schema` (see `docs/source/configuration.md`), but these are output metrics for displaying results, not evaluation parameters. Configuration is limited to challenge metadata and evaluation phases. |
| S1F4: Environment Setup | 2 | Docker-based setup with some gaps. Provides `docker-compose.yml` with multiple services (Django, PostgreSQL, SQS, workers). From `README.md`: "docker-compose up --build" for setup, with optional `--profile worker` and `--profile statsd` flags. Dependencies in `requirements/` folder with separate files (`common.txt`, `dev.txt`, `prod.txt`). Multiple Python worker Dockerfiles (`docker/dev/worker_py3_7/`, `worker_py3_8/`, etc.). However, no hardware specification support, no CUDA version management, and setup is platform-specific rather than evaluation-specific. From `docs/README.md`: requires Python 3.10+, virtualenv recommended. |
| S1F5: Security & Access | 2 | Basic auth with some RBAC. From `docs/source/configuration.md`: supports `allowed_email_domains` and `blocked_email_domains` for challenge access control. Auth token system mentioned in remote evaluation docs: "AUTH_TOKEN: Go to profile page -> Get your Auth Token". User roles exist (superuser, host, participant per `README.md`). However, no vault integration, no enterprise SSO, limited audit logging. From `apps/accounts/` structure: basic Django auth with custom permissions (`apps/accounts/permissions.py`), but no advanced security features. |
| S1F6: Cost Estimation | 0 | No cost features. Being a challenge platform rather than an evaluation framework, there's no cost modeling, token counting, or budget tools. The pricing mentioned in `docs/source/01-getting-started/pricing.md` is for hosting challenges on the EvalAI platform ($125-$850/month plans), not for estimating evaluation costs. No API pricing models, no resource projection tools. |

## Key Observations

### Strengths
1. Challenge Configuration System: Well-documented YAML schema in `docs/source/configuration.md` with comprehensive examples in `docs/source/02-for-challenge-hosts/templates/example-challenges.md` showing 1-4 phase configurations
2. Declarative Phase Management: Clean separation of challenge phases, dataset splits, and leaderboards through `challenge_phase_splits` mapping
3. Docker Infrastructure: Complete containerization with `docker-compose.yml` supporting multiple worker types and optional services

### Limitations for S1 Evaluation
1. Not an Evaluation Framework: EvalAI is a platform for hosting challenges, not a general-purpose evaluation harness. It doesn't configure datasets/models for evaluation - it processes pre-computed submissions
2. No Data Pipeline: Datasets are static annotation files, not configurable data sources. From examples: `test_annotation_file: annotations/test_annotations_devsplit.json`
3. Submission-Based Architecture: The evaluation happens in workers (`scripts/workers/submission_worker.py`) processing user-submitted predictions against ground truth, not running models
4. Limited Configurability: Configuration focuses on challenge metadata (dates, teams, leaderboards) rather than evaluation logic, which is in custom Python scripts

### Evidence of Architecture Mismatch
From `docs/source/architecture.md`:
```
User Submission --> API --> Publish --> SQS Queue --> Submission worker(s)
```

This is a challenge submission processing pipeline, not a model evaluation configuration system. The "evaluation script" (`evaluation_script.zip`) is challenge-specific custom code, not a configurable evaluation framework.

### Configuration Example
From `examples/example1/test_zip_file/zip_challenge.yaml`:
```yaml
title: Challenge Title
evaluation_script: evaluation_script.zip
start_date: 2017-06-09 20:00:00
end_date: 2017-06-19 20:00:00
leaderboard:
  - id: 1
    schema: {"labels": ["yes/no", "number", "others", "overall"]}
challenge_phases:
  - id: 1
    test_annotation_file: test_annotation.txt
    max_submissions_per_day: 100
```

This configures a *challenge* with submission limits and leaderboard columns, not datasets/models for evaluation.

## Overall S1 Score: 5/18 (27.8%)

Conclusion: EvalAI is architecturally mismatched for this evaluation rubric. It's a platform for hosting AI competitions where participants submit predictions, not a framework for configuring and running evaluations. The configuration it provides is for challenge logistics (phases, teams, leaderboards) rather than evaluation components (datasets, models, prompts). For its intended use case (challenge hosting), the YAML configuration system works well, but it lacks the dataset discovery, model configuration, and evaluation parameter features expected of a modern evaluation framework.