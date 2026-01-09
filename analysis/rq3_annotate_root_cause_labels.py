import pandas as pd
import dotenv
import os
import json
import time

from tqdm import tqdm
from litellm import completion

# Load environment variables
dotenv.load_dotenv(override=True)

# Set the model to use - can be changed to any LiteLLM supported model
MODEL = "anthropic/claude-haiku-4-5-20251001"

# Read the root cause annotated JSONL
df = pd.read_json("../data/github_issues_annotated.jsonl", lines=True)
# Filter only related issues with valid root causes
df = df[df['is_related'] == True].copy()
df = df[df['root_cause'].notna()].copy()
print(f"Total root causes to classify: {len(df)}")

ROOT_CAUSE_TAXONOMY = """Root Cause Taxonomy for Software Issues

1. Algorithmic Error
   The core logic contains errors that produce wrong results, unintended behaviors, or performance degradation.
   Examples: Wrong calculations, incorrect formulas, faulty conditional logic, algorithmic bugs, off-by-one errors, wrong business logic, performance regressions due to algorithmic changes, non-deterministic behavior when determinism is required.

2. Architectural Constraint
   Code structure or design decisions prevent necessary adaptations, extensions, or maintenance operations.
   Examples: Hardcoded values that should be configurable, tight coupling preventing changes, inflexible abstractions, design that doesn't allow required modifications, cache designs lacking update mechanisms, stale whitelists requiring manual updates.

3. Configuration Error
   Settings, parameters, or configuration values fail to flow correctly through the system, or are missing when needed for consistent behavior.
   Examples: Ignored config values, parameters not forwarded to downstream components, wrong default values, configuration not applied where needed, missing randomization seeds causing non-deterministic behavior, temperature settings causing instability.

4. Documentation Deficiency
   Documentation is missing, incomplete, outdated, or unclear, preventing proper system use.
   Examples: Undocumented features or APIs, unclear setup instructions, missing usage examples, outdated guides, unclear configuration documentation.

5. Environment Incompatibility
   System makes assumptions about the environment that fail in practice, especially during setup or deployment.
   Examples: Platform-specific bugs, broken installation process, missing system dependencies, OS-specific failures, environment-specific configuration mismatches, runtime version incompatibilities.

6. External Dependency Breakage
   Third-party libraries, APIs, external systems, or network services changed or became unavailable in ways that break existing code.
   Examples: Library version updates introducing incompatibilities, deprecated APIs, upstream breaking changes, external service modifications, network connectivity failures, API timeouts, third-party service outages.

7. Interface Contract Mismatch
   Components disagree on expected data types, formats, or API signatures at integration points.
   Examples: Type errors between functions, wrong return value formats, API signature changes, protocol violations between modules, mismatched data structure expectations.

8. Resource Mishandling
   Improper handling of system resources like memory, GPU, file handles, or concurrency.
   Examples: Memory leaks, GPU out-of-memory errors, deadlocks, race conditions, resource exhaustion, improper cleanup, unbalanced resource allocation, concurrent access violations.

9. Unimplemented Feature Gap
   The system lacks functionality that users reasonably expect to exist.
   Examples: Unsupported model types, missing platform compatibility, absent dataset formats, requested features not yet implemented, missing API integrations, unsupported configurations.

10. Validation Gap
    Missing or insufficient validation checks for inputs, outputs, or state; or inadequate error handling and messages.
    Examples: No input validation allowing invalid states, missing output validation (e.g., cached downloads, data quality checks), unclear error messages, silent failures, crashes on edge cases, missing validation preventing early error detection, insufficient state verification."""

SYSTEM_PROMPT = f"""You are an expert classifier for software engineering root causes.

TASK: Classify a root cause description into ONE category from the taxonomy below.

ROOT CAUSE TAXONOMY:
{ROOT_CAUSE_TAXONOMY}

INSTRUCTIONS:
1. Read the root cause description
2. Match it to the single most appropriate category (1-10) from the taxonomy above
3. Use "Others" only if none of the 10 categories fit

DISAMBIGUATION GUIDELINES:

Configuration Error (3) vs Architectural Constraint (2):
- Use "3" when a config option EXISTS but doesn't flow/propagate correctly
- Use "2" when the DESIGN doesn't allow proper configuration at all

External Dependency Breakage (6) vs Environment Incompatibility (5):
- Use "6" when THIRD-PARTY code (libraries, APIs, services) changed externally
- Use "5" when the issue is with OS, platform, installation, or runtime environment

Algorithmic Error (1) vs Interface Contract Mismatch (7):
- Use "1" when the LOGIC/CALCULATION/ALGORITHM itself is wrong
- Use "7" when components disagree on types, formats, or signatures

Validation Gap (10) vs other categories:
- Use "10" when the root cause is MISSING validation/checks/error handling
- Don't use "10" for what the validation would have prevented

CRITICAL OUTPUT REQUIREMENTS:
- Your response MUST be ONLY valid JSON with NO other text before or after
- Use this EXACT format: {{"label": "X"}} where X is the category number
- Valid values for X are STRICTLY: "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", or "Others"
- Do NOT include any explanation, reasoning, or additional text whatsoever
- Do NOT wrap the JSON in markdown code blocks or any other formatting
- Example valid responses: {{"label": "1"}}, {{"label": "6"}}, {{"label": "Others"}}
- INVALID responses: ```json{{"label": "1"}}```, {{"label": "1", "reason": "..."}}, Any text before/after JSON
"""

def classify_root_cause(root_cause, max_retries=3):
    """Classify a root cause description into a taxonomy category"""
    valid_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Others"]

    for attempt in range(max_retries):
        try:
            response = completion(
                model=MODEL,
                max_tokens=10,
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
                    {"role": "user", "content": f"Root cause: {root_cause}"}
                ]
            )

            raw_response = response.choices[0].message.content

            if raw_response is None or not raw_response.strip():
                raise ValueError("Empty response from API")

            raw_response = raw_response.strip()

            # Try to clean up the response if it has markdown
            if raw_response.startswith("```"):
                lines = raw_response.split('\n')
                raw_response = '\n'.join(lines[1:-1]) if len(lines) > 2 else raw_response
                raw_response = raw_response.strip()

            # Parse JSON
            result = json.loads(raw_response)
            label = result.get("label")

            # Validate label
            if not label or label not in valid_labels:
                raise ValueError(f"Invalid label '{label}' in JSON response")

            return label, response.usage

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt+1}/{max_retries}: {str(e)[:100]}")
                if 'raw_response' in locals():
                    print(f"    Response was: {raw_response[:150]}")
                time.sleep(1)
            else:
                print(f"  Failed response: {raw_response[:200] if 'raw_response' in locals() else 'No response'}")
                raise RuntimeError(f"Failed to get valid label after {max_retries} attempts for: {root_cause[:100]}") from e
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt+1}/{max_retries}: Unexpected error: {str(e)[:100]}")
                time.sleep(1)
            else:
                raise RuntimeError(f"Failed after {max_retries} attempts for: {root_cause[:100]}") from e

# Classify all root causes
labels = []
total_input_tokens = 0
total_output_tokens = 0
total_cache_read_tokens = 0
total_cache_creation_tokens = 0

print("\nStarting classification...")
print("=" * 80)

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Classifying root causes"):
    label, usage = classify_root_cause(row['root_cause'])

    # Track token usage
    if usage:
        total_input_tokens += getattr(usage, 'prompt_tokens', 0)
        total_output_tokens += getattr(usage, 'completion_tokens', 0)
        total_cache_read_tokens += getattr(usage.prompt_tokens_details, 'cached_tokens', 0) if hasattr(usage, 'prompt_tokens_details') else 0
        total_cache_creation_tokens += getattr(usage.prompt_tokens_details, 'cache_creation_tokens', 0) if hasattr(usage, 'prompt_tokens_details') else 0

    labels.append(label)

    # Small delay for rate limiting
    time.sleep(0.3)

# Add labels to dataframe
df['root_cause_label'] = labels

# Save to file
output_file = "../data/github_issues_annotated.jsonl"
df.to_json(output_file, orient="records", lines=True, force_ascii=False)

print("\n" + "=" * 80)
print(f"✓ Classification complete! Results saved to {output_file}")