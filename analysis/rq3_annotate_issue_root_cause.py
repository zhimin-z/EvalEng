import pandas as pd
import dotenv
import json
import time

from tqdm import tqdm
from litellm import completion

# Load environment variables
dotenv.load_dotenv(override=True)

# Set the model to use - can be changed to any LiteLLM supported model
MODEL = "anthropic/claude-haiku-4-5-20251001"

# Input and output files
INPUT_FILE = "../data/rq3_issues_sample_annotated.jsonl"
OUTPUT_FILE = "../data/rq3_issues_sample_annotated_reference.jsonl"

ROOT_CAUSE_TAXONOMY_TEXT = """Root Cause Taxonomy for Software Issues

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
   The system lacks functionality that users reasonably expect to exist, including adding/removing features or automating manual processes.
   Examples: Unsupported model types, missing platform compatibility, missing API integrations, feature removal requests, manual tasks users expect to be automated (e.g., leaderboard updates).

10. Validation Gap
    Missing or insufficient validation checks for inputs, outputs, or state; or inadequate error handling and messages.
    Examples: No input validation allowing invalid states, missing output validation (e.g., cached downloads, data quality checks), unclear error messages, silent failures, crashes on edge cases, missing validation preventing early error detection, insufficient state verification."""

VALID_LABELS = [
    "Algorithmic Error", "Architectural Constraint", "Configuration Error",
    "Documentation Deficiency", "Environment Incompatibility", "External Dependency Breakage",
    "Interface Contract Mismatch", "Resource Mishandling", "Unimplemented Feature Gap",
    "Validation Gap", "Others"
]

SYSTEM_PROMPT = f"""You are an expert software engineering analyst specializing in root cause classification.

TASK: Given a GitHub issue, classify its root cause into ONE of the categories from the taxonomy below.

ROOT CAUSE TAXONOMY:
{ROOT_CAUSE_TAXONOMY_TEXT}

ANNOTATION GUIDELINES:
- User misunderstanding or confusion about how to use the system → Documentation Deficiency (the docs failed to prevent misunderstanding)
- Config exists but doesn't propagate correctly → Configuration Error
- Design prevents adding/modifying config → Architectural Constraint
- Third-party library/API changed or broke → External Dependency Breakage
- OS/platform/runtime environment issue → Environment Incompatibility
- Wrong logic or calculation → Algorithmic Error
- Type/format/signature mismatch between components → Interface Contract Mismatch
- Missing input/output checks → Validation Gap

OUTPUT FORMAT:
Return ONLY valid JSON: {{"root_cause_label": "<label>"}}

Valid labels: "Algorithmic Error", "Architectural Constraint", "Configuration Error", "Documentation Deficiency", "Environment Incompatibility", "External Dependency Breakage", "Interface Contract Mismatch", "Resource Mishandling", "Unimplemented Feature Gap", "Validation Gap", "Others"
"""


def classify_root_cause(issue_content, max_retries=3):
    """Classify the root cause of an issue"""

    user_prompt = f"""ISSUE DESCRIPTION:
{issue_content}

Classify the root cause of this issue. Return ONLY the JSON object, no explanation."""

    for attempt in range(max_retries):
        try:
            response = completion(
                model=MODEL,
                max_tokens=64,
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": "{"}  # Prefill to force JSON start
                ]
            )

            raw_response = response.choices[0].message.content

            if raw_response is None or not raw_response.strip():
                raise ValueError("Empty response from API")

            # Prepend the '{' from prefill since response continues from there
            raw_response = "{" + raw_response.strip()

            # Try to clean up the response if it has markdown code blocks
            # Handle cases like: ```json\n{...}\n``` or ```\n{...}\n```
            if "```" in raw_response:
                # Remove markdown code block markers
                import re
                # Match content between ``` markers (with optional language identifier)
                match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', raw_response)
                if match:
                    raw_response = match.group(1).strip()
                else:
                    # Fallback: just remove all ``` markers
                    raw_response = raw_response.replace('```json', '').replace('```', '').strip()

            # Parse JSON
            result = json.loads(raw_response)
            root_cause_label = result.get("root_cause_label")

            # Validate label
            if not root_cause_label or root_cause_label not in VALID_LABELS:
                raise ValueError(f"Invalid label '{root_cause_label}' in JSON response")

            return root_cause_label

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt+1}/{max_retries}: {str(e)[:100]}")
                if 'raw_response' in locals():
                    print(f"    Response was: {raw_response[:200]}")
                time.sleep(1)
            else:
                print(f"  Failed response: {raw_response[:300] if 'raw_response' in locals() else 'No response'}")
                raise RuntimeError(f"Failed to get valid response after {max_retries} attempts") from e
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt+1}/{max_retries}: Unexpected error: {str(e)[:100]}")
                time.sleep(1)
            else:
                raise RuntimeError(f"Failed after {max_retries} attempts") from e


def main():
    # Load the data
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_json(INPUT_FILE, lines=True)

    # Filter to only related issues
    df_related = df[df['is_related'] == True].copy()
    print(f"Total issues: {len(df)}")
    print(f"Related issues to annotate: {len(df_related)}")

    # Track results
    results = []

    print("\nStarting root cause classification...")
    print("=" * 80)

    max_retries = 5
    for idx, row in tqdm(df_related.iterrows(), total=len(df_related), desc="Classifying issues"):
        issue_content = f"Title: {row['issue_title']}\n\nBody:\n{row['issue_body']}\n\nComments:\n{row['issue_comments']}"

        success = False
        for attempt in range(max_retries):
            try:
                root_cause_label = classify_root_cause(issue_content)

                # Keep all original attributes and add root_cause_label
                result_row = row.to_dict()
                result_row['root_cause_label'] = root_cause_label
                results.append(result_row)
                success = True
                break

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"\nRetry {attempt+1}/{max_retries} for {row['issue_url']}: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"\nFailed after {max_retries} attempts for {row['issue_url']}: {e}")
                    result_row = row.to_dict()
                    result_row['root_cause_label'] = 'ERROR'
                    results.append(result_row)

        # Small delay for rate limiting
        time.sleep(0.3)

    # Create results dataframe and save
    results_df = pd.DataFrame(results)
    results_df.to_json(OUTPUT_FILE, orient='records', lines=True)

    print("\n" + "=" * 80)
    print(f"Classification complete! Results saved to {OUTPUT_FILE}")

    # Print summary statistics
    print(f"\nSummary:")
    print(f"  Total classified: {len(results_df)}")
    error_count = (results_df['root_cause_label'] == 'ERROR').sum()
    if error_count > 0:
        print(f"  Errors: {error_count}")
    print(f"\nLabel distribution:")
    label_counts = results_df['root_cause_label'].value_counts()
    for label, count in label_counts.items():
        print(f"  {label}: {count}")


if __name__ == "__main__":
    main()
