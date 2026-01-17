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
INPUT_FILE = "../data/rq3_issues_annotated.jsonl"

ROOT_CAUSE_TAXONOMY_TEXT = """Root Cause Taxonomy for Software Issues

1. Algorithmic Error
   The core logic produces wrong results or unintended behaviors. Use when the code runs but computes incorrectly.
   Examples: Wrong calculations, incorrect formulas, faulty conditional logic, off-by-one errors, non-deterministic behavior due to logic bugs, inefficient algorithms causing performance issues.
   Distinguish from: Missing checks (→ Validation Gap), type mismatches between components (→ Interface Contract Mismatch).

2. Architectural Constraint
   Code structure prevents necessary adaptation; fixing requires refactoring or design changes.
   Examples: Hardcoded values embedded in logic, tight coupling between modules, rigid class hierarchies, no extension points where flexibility is needed.
   Distinguish from: Config mechanism exists but doesn't propagate (→ Configuration Error).

3. Configuration Error
   Configuration mechanism exists but values fail to flow correctly, or defaults are inappropriate.
   Examples: Config parameter ignored in code path, nested component doesn't receive forwarded config, environment variable read but not applied, wrong default values.
   Distinguish from: No configuration mechanism exists (→ Architectural Constraint).

4. Documentation Deficiency
   Feature EXISTS but users can't find or understand how to use it. Docs failed to guide the user.
   Examples: Undocumented features, unclear setup instructions, user confusion resolved by pointing to existing docs/code.
   Distinguish from: Feature doesn't exist (→ Unimplemented Feature Gap).

5. Environment Incompatibility
   User's machine/environment is missing something or incompatible. The problem is WHERE the code runs.
   Examples: Missing system dependencies, OS-specific failures, conda/pip setup issues, Python version incompatibility, user has wrong installed version.
   Distinguish from: Third-party library code changed (→ External Dependency Breakage).

6. External Dependency Breakage
   Third-party library/API CODE changed or became unavailable. The external code itself broke the integration.
   Examples: Library version updates with breaking changes, deprecated APIs, upstream breaking changes, Pydantic v2 migration.
   Distinguish from: User missing a dependency (→ Environment Incompatibility).

7. Interface Contract Mismatch
   Two or more components have incompatible assumptions at their integration boundary.
   Examples: Async vs sync function mismatch, caller expects dict but callee returns float, API signature changed between library versions, incompatible serialization formats between services.
   Distinguish from: Single component lacking internal validation (→ Validation Gap).

8. Resource Mishandling
   Improper handling of memory, GPU, file handles, or concurrency primitives.
   Examples: Memory leaks, GPU OOM due to improper allocation, deadlocks, race conditions, event loop errors.
   Distinguish from: Slow algorithms (→ Algorithmic Error).

9. Unimplemented Feature Gap
   Feature does NOT EXIST and users are requesting it. Maintainer confirms it needs to be built.
   Examples: Unsupported model types, missing platform support, feature requests acknowledged by maintainers.
   Distinguish from: Feature exists but undocumented (→ Documentation Deficiency).

10. Validation Gap
    Missing checks, guards, or compile-time validation within a single component.
    Examples: No bounds checking, missing null checks, syntax errors, type errors caught at compile time, unhandled exceptions, unclear error messages for invalid input.
    Distinguish from: Logic produces wrong output (→ Algorithmic Error), two components disagreeing on interface (→ Interface Contract Mismatch)."""

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

KEY PRINCIPLE: Identify what's BROKEN in the code, not the symptom. Ask: "What code change would fix this?"

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
    results_df.to_json(INPUT_FILE, orient='records', lines=True)

    print("\n" + "=" * 80)
    print(f"Classification complete! Results saved to {INPUT_FILE}")

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
