# stanford-crfm/helm - Stage 2 (PREPARE) Evaluation

## Summary
HELM (Holistic Evaluation of Language Models) is a comprehensive evaluation framework with moderate preparation capabilities. It excels at dataset loading and scenario generation but lacks explicit data quality assessment, PII detection, red-teaming tools, and contamination detection features. Infrastructure building is limited to basic caching mechanisms.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 2 | Has basic preprocessing with scenario-specific loaders and caching, but lacks systematic validation and versioning. Examples show download utilities (`ensure_file_downloaded()`) and caching (`cache_backend_config`), but no comprehensive preprocessing pipelines or format validation. |
| S2F2: Quality Assessment | 1 | Minimal quality assessment tools. No built-in duplicate detection, demographic analysis, or systematic bias detection in datasets. Framework focuses on post-generation metrics rather than pre-evaluation data quality checks. |
| S2F3: PII Detection | 0 | No PII detection or anonymization features found in codebase. The `medhelm.md` mentions "redact_annotations.py" in scripts but provides no implementation details or documentation for PII handling. |
| S2F4: Infrastructure Building | 1 | Basic caching infrastructure only. Uses SQLite cache (`SqliteCacheBackendConfig`) for request caching. No support for building retrieval indices (FAISS, BM25), databases, or specialized environments beyond basic model serving. |
| S2F5: Model Validation | 2 | Basic model validation exists through credential checks and API connectivity tests. No cryptographic checksums, version compatibility checks, or corruption detection found. Examples show configuration validation but not artifact integrity verification. |
| S2F6: Scenario Generation | 2 | Good support for scenario instantiation with templates and parameter sweeps through run entries (e.g., `mmlu:subject=anatomy,model=openai/gpt2`). Limited multi-turn dialogue support. No built-in edge case generators or adversarial input generation beyond specific scenarios like `decodingtrust_adv_demonstration`. |
| S2F7: Red-Teaming | 1 | Minimal red-teaming support. Has `decodingtrust_adv_demonstration_scenario.py` for adversarial demonstrations, but no comprehensive framework for jailbreak generation, prompt injection testing, or systematic safety boundary exploration. |
| S2F8: Contamination Detection | 0 | No contamination detection features. Documentation at `docs/adding_new_scenarios.md` mentions updating `contamination.yaml` manually but provides no automated detection or comparison tools for identifying train/test overlap. |

---

## Detailed Evidence

### S2F1: Data Preprocessing and Physical Partitioning (Rating: 2)

Evidence of basic preprocessing:

From `docs/adding_new_scenarios.md`:
```python
# Downloading data to local disk
# The output_path argument contains a scenario-specific download folder
# Use ensure_directory_exists() and ensure_file_downloaded() helper functions
```

From `src/helm/benchmark/scenarios/mtsamples_replicate_scenario.py`:
```python
def download_file(self, file_name: str, output_dir: str) -> str:
    """Downloads a text file from GitHub and saves it locally."""
    file_url = self.RAW_BASE_URL + file_name
    file_path = os.path.join(output_dir, file_name)
    
    if not os.path.exists(file_path):  # Caching mechanism
        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download {file_url}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
    return file_path
```

From `scripts/examples/auto_client_usage.py`:
```python
# Set up SQLite cache
cache_backend_config = SqliteCacheBackendConfig(sqlite_cache_path)
```

Limitations:
- No systematic validation (checksums, format checking)
- No versioned splits mentioned in documentation
- No stratified splitting utilities
- Basic text preprocessing only (shown in scenario examples)
- No multi-modal preprocessing pipelines beyond image scenarios

### S2F2: Dataset Quality and Bias Assessment (Rating: 1)

Evidence of minimal tools:

From searching the codebase, no quality assessment utilities were found for:
- Label noise detection
- Duplicate detection (exact or semantic)
- Demographic distribution analysis
- Systematic bias detection in datasets

The framework focuses on post-generation metrics rather than pre-evaluation data quality:

From `docs/metrics.md`:
```md
# Metrics
::: helm.benchmark.metrics
```

The metrics system evaluates model outputs, not input data quality. No dataset quality assessment tools are documented.

### S2F3: PII Detection and Anonymization (Rating: 0)

Evidence:

From `scripts/medhelm/redact_annotations.py` (filename only, no code provided in context):
- Mentioned in directory structure but no implementation details

No PII detection mentioned in:
- `docs/credentials.md` (only API keys)
- `docs/adding_new_scenarios.md` (no privacy guidance)
- Scenario implementations (e.g., MTSamples scenarios process raw medical text without PII handling)

From `src/helm/benchmark/scenarios/mtsamples_replicate_scenario.py`:
```python
# Processes raw medical reports with no PII redaction
with open(file_path, "r", encoding="utf-8") as f:
    text_content = f.read().strip()
```

### S2F4: Task-Specific Infrastructure Building (Rating: 1)

Evidence of basic caching only:

From `scripts/examples/auto_client_usage.py`:
```python
# Set up SQLite cache
base_path = "prod_env"
sqlite_cache_path = os.path.join(base_path, CACHE_DIR)
ensure_directory_exists(sqlite_cache_path)
cache_backend_config = SqliteCacheBackConfig(sqlite_cache_path)
```

From `docs/tutorial.md`:
```bash
# The environment directory is `prod_env/` by default
# The output directory is `benchmark_output/` by default
```

No evidence of:
- Retrieval system builders (FAISS, ColBERT, BM25)
- Database setup utilities (PostgreSQL, vector DBs)
- Index versioning or artifact management
- Multi-agent environments

### S2F5: Model Artifact Validation (Rating: 2)

Evidence of basic validation:

From `docs/credentials.md`:
```
# Credentials file validation
platformOneApiKey: sk-abcdefgh
platformTneApiKey: sk-ijklmnop
```

From `docs/adding_new_models.md`:
```yaml
# Model configuration validation
model_deployments:
  - name: huggingface/pythia-70m
    model_name: eleutherai/pythia-70m
    tokenizer_name: EleutherAI/gpt-neox-20b
    max_sequence_length: 2048
```

Limitations:
- No cryptographic checksum verification
- No model weight integrity checks
- No version compatibility warnings
- No corruption detection beyond API failures

### S2F6: Evaluation Scenario Generation (Rating: 2)

Evidence of template-based generation:

From `docs/run_entries.md`:
```
# Run entry format supports parameterization
mmlu:subject=anatomy,model=openai/gpt2
```

From `docs/run_entries_configuration_files.md`:
```conf
entries: [
  {description: "mmlu:subject=anatomy,model=text", priority: 1},
  {description: "mmlu:subject=philosophy,model=text", priority: 1},
]
```

From `src/helm/benchmark/annotation/mtsamples_procedures_annotator.py`:
```python
PROMPT_TEMPLATE = """You are a medical expert tasked with evaluating...
<user_request>
{QUESTION}
</user_request>
<response>
{RESPONSE}
</response>
"""
```

Limitations:
- Limited multi-turn support (no conversation state management)
- No built-in edge case generators
- No adversarial input generation utilities
- Reproducibility through seeds but not comprehensive scenario versioning

### S2F7: Red-Teaming and Adversarial Test Generation (Rating: 1)

Evidence of minimal support:

From `src/helm/benchmark/scenarios/decodingtrust_adv_demonstration_scenario.py`:
```python
class DecodingTrustAdvDemoScenario(Scenario):
    """
    Robustness analysis of LM generations when facing adversarial demonstrations
    """
    name = "decodingtrust_adv_demonstration"
    description = "Robustness analysis of LM generations when facing adversarial demonstrations"
    tags = ["robustness", "demonstration"]
```

Limitations:
- Only one adversarial scenario (DecodingTrust)
- No jailbreak library or generation tools
- No prompt injection test framework
- No systematic bias probing utilities
- No attack taxonomy or classification

### S2F8: Data Contamination Detection (Rating: 0)

Evidence:

From `docs/adding_new_scenarios.md`:
```md
11. Update `src/helm/benchmark/static/contamination.yaml` with models 
    that were trained on your scenario (i.e. contaminated).
```

This is manual annotation only, not automated detection.

No contamination detection tools found for:
- N-gram overlap checking
- Embedding-based similarity
- Fingerprint comparison
- Training corpus analysis

The framework relies on manual declaration of contamination rather than automated detection.

---

## Key Strengths

1. Flexible scenario system with easy parameterization through run entries
2. Request caching prevents redundant API calls
3. Modular architecture supports custom scenarios
4. Template-based prompting enables systematic variation

## Key Weaknesses

1. No data quality assessment tools (duplicates, balance, demographics)
2. No PII detection despite medical scenario support
3. No contamination detection - relies on manual annotation
4. Limited infrastructure - only basic caching, no retrieval/database support
5. Minimal red-teaming - no comprehensive adversarial framework
6. No artifact validation - no checksums or integrity verification

## Recommendations

To improve Stage 2 capabilities, HELM should add:
1. Data quality assessment module (duplicates, demographics, label quality)
2. PII detection/anonymization for sensitive domains (medical, legal)
3. Automated contamination detection using n-gram/embedding methods
4. Red-teaming toolkit with jailbreak/injection test generators
5. Model artifact validation with checksums and version compatibility
6. Infrastructure builders for retrieval systems and databases