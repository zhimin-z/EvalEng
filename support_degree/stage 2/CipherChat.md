# CipherChat - Stage 2 (PREPARE) Evaluation

## Summary
CipherChat is a research framework for testing LLM safety through cipher-based attacks, not a general-purpose evaluation framework. It has minimal data preparation capabilities, focusing instead on encoding harmful prompts using various ciphers. The framework lacks most standard evaluation preparation features like dataset management, quality assessment, and infrastructure building.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S2F1: Data Preprocessing | 1 | Evidence: Data is loaded from a simple dictionary file (`data/data_en_zh.dict`) via `torch.load()` in `main.py`. The `get_data()` function in `utils.py` (referenced but not shown) appears to do basic filtering by domain and language. No caching, validation, or sophisticated preprocessing exists. The only "preprocessing" is cipher encoding via `expert.encode()` in `main.py:198-199`. No support for multiple modalities, stratified splitting, or versioning. |
| S2F2: Quality Assessment | 0 | Evidence: No quality assessment tools exist. The framework uses pre-existing datasets (`data/data_en_zh.dict`) without any validation. No duplicate detection, bias analysis, or label quality checks. The only quality-related feature is post-hoc toxicity detection via GPT-4 (`generate_detection_prompt()` in `prompts_and_demonstrations.py:395-447`), which evaluates outputs not inputs. |
| S2F3: PII Detection | 0 | Evidence: No PII detection or anonymization capabilities. The framework's `prompts_and_demonstrations.py` actually contains potentially harmful demonstrations including detailed criminal instructions, but has no mechanisms to detect or redact PII. The comment "Love and Peace, we love the world" (line 1) acknowledges sensitive content but provides no tooling. |
| S2F4: Infrastructure Building | 0 | Evidence: No infrastructure building capabilities. The framework only implements cipher encoding/decoding via `encode_experts.py` (referenced but not provided in full). No retrieval systems, databases, or specialized environments. The only "infrastructure" is basic OpenAI API calls in `main.py:41-73`. |
| S2F5: Model Validation | 0 | Evidence: No model validation features. The framework simply makes API calls to OpenAI models specified by string (`model_name` parameter in `main.py:154`). No checksum validation, version compatibility checks, or integrity verification. The code assumes models are accessible via API keys. |
| S2F6: Scenario Generation | 1 | Evidence: Limited scenario generation exists. The framework can select demonstrations based on domain and toxicity type (`demonstration_dict` in `prompts_and_demonstrations.py:73-93`), and combines them with system prompts. Example from `main.py:195-201`: generates encoded demonstrations dynamically. However, no parameter sweeps, multi-turn dialogues, or edge case generation. Only deterministic prompt construction. |
| S2F7: Red-Teaming | 2 | Evidence: This is the framework's core capability. Contains extensive adversarial content across 11 domains (Crimes, Ethics, Physical_Harm, etc.) in `prompts_and_demonstrations.py`. Multiple cipher methods (Caesar, Morse, ASCII, etc.) in `encode_experts.py`. However, attack library is static (hardcoded demonstrations), no automated generation of new attacks, and no attack taxonomy beyond domain categories. From `main.py:137`: `instruction_type` selection provides domain-based testing. Limited to jailbreak attempts via encoding, not comprehensive red-teaming. |
| S2F8: Contamination Detection | 0 | Evidence: No contamination detection capabilities. The framework tests safety alignment, not training data leakage. No methods to compare evaluation data against training corpora, n-gram overlap detection, or semantic similarity analysis. |

## Key Observations

### Strengths
1. Domain-specific red-teaming: Well-organized harmful prompt library across 11 safety domains (`prompts_and_demonstrations.py:73-397`)
2. Cipher-based attack methods: Multiple encoding schemes to test safety alignment (`encode_method` parameter supports ASCII, Caesar, Morse, etc.)
3. Bilingual support: Demonstrations in both English and Chinese

### Critical Gaps
1. Not a general evaluation framework: Purpose-built for safety testing via cipher attacks, not general LLM evaluation
2. No data management: Relies on pre-existing static dataset with no validation or preprocessing pipeline
3. Manual curation required: All demonstrations are hardcoded; no automated generation or augmentation
4. Limited reproducibility: No seed management, version control, or experiment tracking beyond basic file saving
5. API-only: No support for local models or custom infrastructure

### Evidence of Limited Scope

From `main.py:137-143`:
```python
parser.add_argument("--instruction_type", type=str,
                    default=["Crimes_And_Illegal_Activities", "Ethics_And_Morality",
                             "Inquiry_With_Unsafe_Opinion", "Insult", "Mental_Health", "Physical_Harm",
                             "Privacy_And_Property", "Reverse_Exposure", "Role_Play_Instruction",
                             "Unfairness_And_Discrimination", "Unsafe_Instruction_Topic"][0])
```
This shows fixed domains with no extensibility for custom evaluation scenarios.

From `main.py:184-190`:
```python
system_prompt = ""
if args.use_system_role:
    system_prompt += system_role_propmts[args.encode_method]
if args.use_demonstrations:
    # ... simple concatenation of pre-defined demonstrations
```
Minimal scenario generation—just template concatenation.

## Conclusion

CipherChat is a specialized research tool for adversarial safety testing, not a comprehensive evaluation framework. It scores 4/24 total points in Stage 2, with most capabilities rated 0. The framework excels only at providing pre-curated adversarial prompts with cipher encoding, which partially satisfies red-teaming requirements. All other preparation features—data preprocessing, quality assessment, PII handling, infrastructure building, model validation, and contamination detection—are absent.