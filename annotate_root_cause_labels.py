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
df = pd.read_json("data/github_issues_annotated.jsonl", lines=True)
# Filter only related issues with valid root causes
df = df[df['is_related'] == True].copy()
df = df[df['root_cause'].notna()].copy()
print(f"Total root causes to classify: {len(df)}")

ROOT_CAUSE_SUMMARY = """Root Cause Taxonomy for Software Issues

1. Unimplemented Feature Gap
   The system lacks functionality that users reasonably expect to exist.
   Examples: Unsupported model types, missing platform compatibility, absent dataset formats,
   requested features not yet implemented.

2. External Dependency Breakage
   Third-party libraries, APIs, or external systems changed in ways that break existing code.
   Examples: Library version updates introducing incompatibilities, deprecated APIs, upstream
   breaking changes, external service modifications.

3. Interface Contract Mismatch
   Components disagree on expected data types, formats, or API signatures at integration points.
   Examples: Type errors between functions, wrong return value formats, API signature changes,
   protocol violations between modules.

4. Incorrect Algorithm Implementation
   The core logic contains errors that produce wrong results or unintended behaviors.
   Examples: Wrong calculations, incorrect formulas, faulty conditional logic, algorithmic bugs,
   off-by-one errors, wrong business logic.

5. Configuration Propagation Failure
   Settings, parameters, or configuration values fail to flow correctly through the system.
   Examples: Ignored config values, parameters not forwarded to downstream components, wrong
   default values, configuration not applied where needed.

6. Resource Management Failure
   Improper handling of system resources like memory, GPU, file handles, or concurrency.
   Examples: Memory leaks, GPU out-of-memory errors, deadlocks, race conditions, resource
   exhaustion, improper cleanup.

7. Inadequate Input Validation
   Missing or insufficient checks for invalid inputs, or poor error handling and messages.
   Examples: No input validation allowing invalid states, unclear error messages, silent failures,
   crashes on edge cases.

8. Documentation Knowledge Gap
   Documentation is missing, incomplete, outdated, or unclear, preventing proper system use.
   Examples: Undocumented features or APIs, unclear setup instructions, missing usage examples,
   outdated guides.

9. Fragile Environment Assumption
   System makes assumptions about the environment that fail in practice, especially during setup.
   Examples: Platform-specific bugs, broken installation process, missing system dependencies,
   environment-specific configuration issues.

10. Rigid Architectural Design
    Code structure or design decisions prevent necessary adaptations or extensions.
    Examples: Hardcoded values that should be configurable, tight coupling preventing changes,
    inflexible abstractions, design that doesn't allow required modifications."""

SYSTEM_PROMPT = f"""You are an expert classifier for software engineering root causes.

TASK: Classify a root cause description into ONE category from the taxonomy below.

ROOT CAUSE TAXONOMY:
{ROOT_CAUSE_SUMMARY}

CLASSIFICATION APPROACH:
1. Read and understand the root cause description semantically
2. Identify the UNDERLYING TECHNICAL PROBLEM, not just surface symptoms
3. Consider which category best captures the fundamental nature of the issue
4. DO NOT rely on keyword matching - understand the meaning and context
5. Choose the single most appropriate category (1-10) based on the core problem
6. Only use "Others" if genuinely none of the categories fit

IMPORTANT:
- Understand the problem semantically, not through keyword matching
- Different wording can describe the same underlying issue
- Focus on WHY the problem exists, not just WHAT the symptom is
- Consider the examples in each category as illustrations of the concept, not keyword lists

CLASSIFICATION EXAMPLES:
- "Missing numpy dependency breaks pip installation" → "2"
  (Root cause: external library dependency issue, not installation per se)

- "Function returns wrong data type causing type error" → "3"
  (Root cause: components expect different contracts, not the type error itself)

- "Incorrect calculation in loss function" → "4"
  (Root cause: algorithmic logic error)

- "Model parameter not passed to trainer" → "5"
  (Root cause: configuration value not propagating through system)

- "Documentation doesn't explain how to set API key" → "8"
  (Root cause: knowledge gap in documentation)

CRITICAL OUTPUT REQUIREMENTS:
- Your response must be ONLY valid JSON with no other text before or after
- Use this EXACT format: {{"label": "X"}} where X is the category number
- Valid values for X: "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", or "Others"
- Do NOT include any explanation, reasoning, or additional text
- Do NOT wrap the JSON in markdown code blocks
- Example valid responses: {{"label": "2"}}, {{"label": "Others"}}, {{"label": "5"}}
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
os.makedirs("data", exist_ok=True)
output_file = "data/github_issues_with_labels.jsonl"
df.to_json(output_file, orient="records", lines=True, force_ascii=False)

print("\n" + "=" * 80)
print(f"✓ Classification complete! Results saved to {output_file}")

# Summary statistics
print("\n=== Summary Statistics ===")
print(f"Total root causes classified: {len(df)}")
print("\nLabel distribution:")
label_counts = df['root_cause_label'].value_counts().sort_index()
for label, count in label_counts.items():
    print(f"  {label}: {count}")

# Cost tracking
print("\n=== Token Usage & Cost ===")
print(f"Input tokens: {total_input_tokens:,}")
print(f"Output tokens: {total_output_tokens:,}")
print(f"Cache read tokens: {total_cache_read_tokens:,}")
print(f"Cache creation tokens: {total_cache_creation_tokens:,}")

# Claude Haiku 4.5 pricing (as of Dec 2024)
# Input: $1/M, Output: $5/M, Cache writes: $1.25/M, Cache reads: $0.10/M
input_cost = (total_input_tokens / 1_000_000) * 1.0
output_cost = (total_output_tokens / 1_000_000) * 5.0
cache_write_cost = (total_cache_creation_tokens / 1_000_000) * 1.25
cache_read_cost = (total_cache_read_tokens / 1_000_000) * 0.10
total_cost = input_cost + output_cost + cache_write_cost + cache_read_cost

print(f"\nEstimated cost breakdown:")
print(f"  Input tokens: ${input_cost:.4f}")
print(f"  Output tokens: ${output_cost:.4f}")
print(f"  Cache creation: ${cache_write_cost:.4f}")
print(f"  Cache reads: ${cache_read_cost:.4f}")
print(f"  TOTAL: ${total_cost:.2f}")
print(f"  Cost per root cause: ${total_cost/len(df):.4f}")