import pandas as pd
import dotenv
import json
import time

from tqdm import tqdm
from litellm import completion

# Load environment variables
dotenv.load_dotenv(override=True)

# Set the model to use - can be changed to any LiteLLM supported model
MODEL = "anthropic/claude-sonnet-4-5-20250929"

# Load Jimmy's annotations
df_jimmy = pd.read_json(r"../data/rq3_issues_sample_annotated_jimmy.jsonl", lines=True)
df_jimmy = df_jimmy[df_jimmy['root_cause_label'].notnull()]
df_jimmy = df_jimmy.sort_values(by='issue_url').reset_index(drop=True)

# Load Zehao's annotations
df_zehao = pd.read_json("../data/rq3_issues_sample_annotated_zehao.jsonl", lines=True)
df_zehao = df_zehao[df_zehao['root_cause_label'].notnull()]
df_zehao = df_zehao.sort_values(by='issue_url').reset_index(drop=True)

# Find disagreements
disagreements = df_jimmy[df_jimmy['root_cause_label'] != df_zehao['root_cause_label']].copy()
disagreements['zehao_label'] = df_zehao.loc[disagreements.index, 'root_cause_label'].values

print(f"Total issues: {len(df_jimmy)}")
print(f"Disagreements to adjudicate: {len(disagreements)}")

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

SYSTEM_PROMPT = f"""You are an expert adjudicator for software engineering root cause classifications.

TASK: Given two different labels assigned by two annotators, determine which label is more likely correct based on the taxonomy definitions, or if both seem equally valid/invalid, explain why.

ROOT CAUSE TAXONOMY:
{ROOT_CAUSE_TAXONOMY_TEXT}

DISAMBIGUATION:
- Configuration Error: config EXISTS but doesn't propagate. Architectural Constraint: design prevents config.
- External Dependency Breakage: third-party code changed. Environment Incompatibility: OS/platform/runtime issue.
- Algorithmic Error: wrong logic/calculation. Interface Contract Mismatch: type/format/signature disagreement.
- Validation Gap: missing checks. Don't use for what validation would have prevented.

OUTPUT FORMAT:
Return ONLY a valid JSON object with no additional text, explanation, or markdown. Just the raw JSON.

Required fields:
- "correct_label": One of: "Algorithmic Error", "Architectural Constraint", "Configuration Error", "Documentation Deficiency", "Environment Incompatibility", "External Dependency Breakage", "Interface Contract Mismatch", "Resource Mishandling", "Unimplemented Feature Gap", "Validation Gap", "Others"
- "error_reason": A concise one-liner explaining what the wrong annotator(s) missed or misunderstood that led to their incorrect label. Focus on what evidence or taxonomy distinction they overlooked, not who is right.

Example (output exactly like this, no other text):
{{"correct_label": "Algorithmic Error", "error_reason": "Missed that the issue is about wrong calculation logic, not missing input validation"}}
"""

VALID_LABELS = [
    "Algorithmic Error", "Architectural Constraint", "Configuration Error",
    "Documentation Deficiency", "Environment Incompatibility", "External Dependency Breakage",
    "Interface Contract Mismatch", "Resource Mishandling", "Unimplemented Feature Gap",
    "Validation Gap", "Others"
]

def adjudicate_labels(label_a, label_b, issue_content, max_retries=3):
    """Adjudicate between two different labels"""

    user_prompt = f"""ISSUE DESCRIPTION:
{issue_content}

Annotator A's label: {label_a}
Annotator B's label: {label_b}

Which label is correct? If both are wrong, provide the correct label."""

    for attempt in range(max_retries):
        try:
            response = completion(
                model=MODEL,
                max_tokens=1024,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
                    {"role": "user", "content": user_prompt}
                ]
            )

            raw_response = response.choices[0].message.content

            if raw_response is None or not raw_response.strip():
                raise ValueError("Empty response from API")

            raw_response = raw_response.strip()

            # Clean up markdown wrapping if present
            if raw_response.startswith("```"):
                lines = raw_response.split('\n')
                # Remove first line (```json) and last line (```)
                raw_response = '\n'.join(lines[1:-1] if lines[-1].strip() == '```' else lines[1:]).strip()

            # Parse JSON
            result = json.loads(raw_response)
            correct_label = result.get("correct_label")
            error_reason = result.get("error_reason", "No reason provided")

            # Validate label
            if not correct_label or correct_label not in VALID_LABELS:
                raise ValueError(f"Invalid label '{correct_label}' in JSON response")

            return correct_label, error_reason

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

# Adjudicate disagreements
results = []

print("\nStarting adjudication of disagreements...")
print("=" * 80)

for idx, row in tqdm(disagreements.iterrows(), total=len(disagreements), desc="Adjudicating disagreements"):
    jimmy_label = row['root_cause_label']
    zehao_label = row['zehao_label']
    issue_content = f"Title: {row['issue_title']}\n\nBody:\n{row['issue_body']}\n\nComments:\n{row['issue_comments']}"

    correct_label, error_reason = adjudicate_labels(jimmy_label, zehao_label, issue_content)

    # Determine status
    if correct_label != jimmy_label and correct_label != zehao_label:
        status = 'both_wrong'
    elif correct_label == jimmy_label:
        status = 'zehao_wrong'
    else:
        status = 'jimmy_wrong'

    results.append({
        'issue_url': row['issue_url'],
        'jimmy_label': jimmy_label,
        'zehao_label': zehao_label,
        'adjudicated_label': correct_label,
        'status': status,
        'error_reason': error_reason
    })

    # Print the error reason immediately for ad-hoc analysis
    print(f"\n[{status.upper()}] {row['issue_url'].split('/')[-1]}")
    print(f"  Jimmy: {jimmy_label} | Zehao: {zehao_label} -> {correct_label}")
    print(f"  Why wrong: {error_reason}")

    # Small delay for rate limiting
    time.sleep(0.3)

# Create results dataframe
results_df = pd.DataFrame(results)

# Save to file
output_file = "../data/rq3_adjudicated_disagreements.csv"
results_df.to_csv(output_file, index=False)

print("\n" + "=" * 80)
print(f"Adjudication complete! Results saved to {output_file}")

# Print summary statistics
print(f"\nSummary:")
print(f"  Total disagreements: {len(results_df)}")
print(f"  Agreed with Jimmy: {(results_df['adjudicated_label'] == results_df['jimmy_label']).sum()}")
print(f"  Agreed with Zehao: {(results_df['adjudicated_label'] == results_df['zehao_label']).sum()}")
both_wrong = ((results_df['adjudicated_label'] != results_df['jimmy_label']) &
              (results_df['adjudicated_label'] != results_df['zehao_label'])).sum()
print(f"  Both wrong (new label): {both_wrong}")

# Print detailed results
print("\n" + "=" * 80)
print("Detailed adjudication results:")
print("=" * 80)
for _, row in results_df.iterrows():
    print(f"\nIssue: {row['issue_url']}")
    print(f"  Jimmy: {row['jimmy_label']}")
    print(f"  Zehao: {row['zehao_label']}")
    print(f"  Adjudicated: {row['adjudicated_label']}")
    print(f"  Why wrong: {row['error_reason']}")