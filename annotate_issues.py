import pandas as pd
import dotenv
import os
from litellm import completion
import json
from tqdm import tqdm
import time

# Load environment variables
dotenv.load_dotenv(override=True)

# Set the model to use - can be changed to any LiteLLM supported model
MODEL = "anthropic/claude-haiku-4-5-20251001"

# Read the issues JSONL
df = pd.read_json("data/github_issues.jsonl", orient="records", lines=True)
df = df.sample(n=377, random_state=42)  # Randomly select a sample of issues for analysis
print(f"Total issues to analyze: {len(df)}")

# Condensed version of the evaluation workflow stages
STAGES_SUMMARY = """Unified Evaluation Workflow:

**Stage 0: Provisioning** - Setting up the runtime environment to make evaluation executable.
- Step A: Harness Installation
  * Definition: Installing the evaluation framework and its dependencies.
  * Strategy 1: Git Clone - Cloning repositories and building from source code
  * Strategy 2: Python Package - Installing via pip, uv, conda, or poetry
  * Strategy 3: Node Package - Installing via npm, npx, or Homebrew
  * Strategy 4: Binary Package - Downloading standalone executable files
  * Strategy 5: Container Image - Pulling Docker/OCI container images
- Step B: Credential Configuration
  * Definition: Setting up authentication credentials to access external services and resources.
  * Strategy 1: Model API Authentication - Configuring API keys to call remote model inference endpoints (OpenAI, Anthropic, HuggingFace APIs)
  * Strategy 2: Artifact Repository Authentication - Authenticating to download models and datasets from repositories (HuggingFace Hub, Zenodo)
  * Strategy 3: Evaluation Platform Authentication - Logging into evaluation platform accounts for accessing services and leaderboards

**Stage I: Specification** - Configuring what to evaluate and how to evaluate it.
- Step A: SUT Preparation
  * Definition: Configuring the System Under Test (SUT) - the primary model, algorithm, or system being evaluated.
  * Strategy 1: Model-as-a-Service - Setting up remote API-based models (OpenAI, Anthropic, cloud providers)
  * Strategy 2: Model-in-Process - Loading models locally into memory for inference (LLMs, VLMs, traditional ML models)
  * Strategy 3: Non-Parametric Algorithm - Configuring rule-based algorithms without learned weights (Approximate Nearest Neighbor (ANN) algorithms, BM25, signal processing)
  * Strategy 4: Interactive Agent - Setting up agents that make sequential decisions over time (RL policies, multi-agent systems, robot controllers)
- Step B: Benchmark Preparation (Inputs)
  * Definition: Preparing the test inputs (questions, prompts, images, scenarios) that will be fed to the SUT.
  * Strategy 1: Benchmark Data Preparation - Loading existing test datasets or specifying custom test cases
  * Strategy 2: Synthetic Data Generation - Automatically generating new test inputs through data augmentation or synthesis
  * Strategy 3: Simulation Environment Setup - Creating interactive virtual environments for agent testing (3D scenes, task configurations)
  * Strategy 4: Production Traffic Sampling - Collecting real-world user queries for evaluation
- Step C: Benchmark Preparation (References)
  * Definition: Preparing reference materials (correct answers, expected outputs, evaluation criteria) for scoring SUT outputs.
  * Strategy 1: Ground Truth Preparation - Loading reference answers, correct labels, expected outputs, or human annotations to compare against
  * Strategy 2: Judge Preparation - Setting up LLM judges or trained evaluator models to assess quality

**Stage II: Execution** - Running the SUT to generate outputs.
- Step A: SUT Invocation
  * Definition: Actually running the SUT on test inputs to produce outputs or actions.
  * Strategy 1: Batch Inference - Running many test inputs through the SUT, one evaluation run at a time
  * Strategy 2: Arena Battle - Running the same input through multiple SUTs simultaneously for head-to-head comparison
  * Strategy 3: Interactive Loop - Repeatedly executing the SUT's actions in an environment over multiple timesteps
  * Strategy 4: Production Streaming - Continuously processing live incoming requests in real-time

**Stage III: Assessment** - Measuring how well the SUT performed.
- Step A: Individual Scoring
  * Definition: Computing quality scores for each individual test case.
  * Strategy 1: Deterministic Measurement - Rule-based scoring using exact matching, string distance, or token overlap metrics (BLEU, ROUGE)
  * Strategy 2: Embedding Measurement - Measuring semantic similarity by comparing neural embeddings
  * Strategy 3: Subjective Measurement - Using LLM judges or classifier models to rate quality or compare outputs
  * Strategy 4: Performance Measurement - Measuring speed, memory usage, or computational cost
- Step B: Aggregate Scoring
  * Definition: Combining individual scores into overall performance metrics.
  * Strategy 1: Distributional Statistics - Computing averages, percentiles, or other summary statistics across test cases
  * Strategy 2: Uncertainty Quantification - Calculating confidence intervals or statistical significance using resampling methods

**Stage IV: Reporting** - Presenting and communicating evaluation results.
- Step A: Insight Presentation
  * Definition: Making results understandable and actionable for users.
  * Strategy 1: Execution Tracing - Recording detailed execution logs or trajectories showing what happened during each test run
  * Strategy 2: Subgroup Analysis - Breaking down performance by categories (task types, demographic groups, difficulty levels)
  * Strategy 3: Regression Alerting - Automatically detecting when performance drops below previous baselines
  * Strategy 4: Chart Generation - Creating visualizations like plots, charts, and graphs
  * Strategy 5: Dashboard Creation - Building interactive web interfaces to explore results
  * Strategy 6: Leaderboard Publication - Submitting scores to public comparison leaderboards"""

SYSTEM_PROMPT = f"""You are an expert classifier for machine learning evaluation workflow issues.

TASK: Classify ONE GitHub issue into the evaluation workflow taxonomy below.

WORKFLOW TAXONOMY:
{STAGES_SUMMARY}

## STEP 1: DETERMINE RELEVANCE (is_related: true/false)

Mark is_related=true if the issue directly affects ANY stage of the evaluation workflow above (Provisioning, Specification, Execution, Assessment, Reporting). This includes bugs, failures, missing features, or documentation gaps that prevent/change workflow actions.

## STEP 2: ASSIGN LABELS (stage, step, strategy)

CLASSIFICATION APPROACH:
- Understand the CORE PROBLEM semantically first
- Match to appropriate Stage/Step/Strategy from taxonomy
- Keywords are INDICATORS, not strict requirements
- Always assign Stage if is_related=true
- Assign Step/Strategy only if clearly identifiable
- If uncertain at any level, use null (e.g., Stage only without Step)
- If multiple stages relevant → choose PRIMARY blocker (earliest failure point)
- Semantic understanding > keyword matching

EXAMPLES:
✓ "pip install fails with dependency conflict" → Stage 0, Step A, Strategy 2
✓ "Installation broken after upgrade" → Stage 0, Step A, strategy=null
✓ "Can't get evaluations running" → Stage III, step=null, strategy=null

## STEP 3: WRITE ROOT CAUSE (max 15 words)

FORMAT: "Technical-cause + causing-verb + symptom"
EXAMPLE: "Missing dependency causes import failure"
- State underlying technical cause, not just symptom
- Do NOT restate user complaint or propose solutions
- If is_related=false → root_cause=null

## VALIDATION RULES

1. is_related=false → all fields null
2. is_related=true → stage NOT null
3. strategy set → step MUST be set
4. step set → stage MUST be set
5. Stage: "0", "I", "II", "III", "IV"
6. Step: "A", "B", "C"
7. Strategy: 1, 2, 3, 4, 5, or 6

## OUTPUT FORMAT (return ONLY valid JSON, no markdown)

{{"is_related": true, "stage": "0", "step": "A", "strategy": "2", "root_cause": "Missing numpy dependency breaks pip installation process"}}

or

{{"is_related": false, "stage": null, "step": null, "strategy": null, "root_cause": null}}"""

def analyze_issue(title, body, harness_name):
    """Analyze a single issue using the configured LLM model"""
    issue_text = f"Harness: {harness_name}\nTitle: {title}\nBody: {body if pd.notna(body) and body.strip() else 'No description'}"

    try:
        response = completion(
            model=MODEL,
            max_tokens=200,  # Reduced: JSON output is ~100 tokens
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
                {"role": "user", "content": issue_text}
            ]
        )

        response_text = response.choices[0].message.content

        # Extract JSON
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        result = json.loads(response_text)

        # Track token usage
        usage = response.usage
        return result, usage

    except Exception as e:
        print(f"  Error: {str(e)[:100]}")
        return {
            "is_related": None,
            "stage": None,
            "step": None,
            "strategy": None,
            "root_cause": f"Error: {str(e)[:100]}"
        }, None

# Analyze all issues
results = []
total_input_tokens = 0
total_output_tokens = 0
total_cache_read_tokens = 0
total_cache_creation_tokens = 0

print("\nStarting analysis...")
print("=" * 80)

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Analyzing issues"):
    analysis, usage = analyze_issue(
        title=row['issue_title'],
        body=row['issue_body'],
        harness_name=row['harness_name']
    )

    # Track token usage
    if usage:
        total_input_tokens += getattr(usage, 'prompt_tokens', 0)
        total_output_tokens += getattr(usage, 'completion_tokens', 0)
        total_cache_read_tokens += getattr(usage.prompt_tokens_details, 'cached_tokens', 0) if hasattr(usage, 'prompt_tokens_details') else 0
        total_cache_creation_tokens += getattr(usage.prompt_tokens_details, 'cache_creation_tokens', 0) if hasattr(usage, 'prompt_tokens_details') else 0

    result_row = {
        'harness_name': row['harness_name'],
        'github_repo': row['github_repo'],
        'issue_title': row['issue_title'],
        'issue_body': row['issue_body'],
        'issue_url': row['issue_url'],
        'issue_created_at': row['issue_created_at'],
        'issue_closed_at': row['issue_closed_at'],
        'is_related': analysis.get('is_related'),
        'stage': analysis.get('stage'),
        'step': analysis.get('step'),
        'strategy': analysis.get('strategy'),
        'root_cause': analysis.get('root_cause')
    }
    results.append(result_row)

    # Small delay for rate limiting
    time.sleep(0.3)

# Create results DataFrame
results_df = pd.DataFrame(results)

# Save to CSV
os.makedirs("data", exist_ok=True)
output_file = "data/github_issues_annotated.jsonl"
results_df.to_json(output_file, orient="records", lines=True, force_ascii=False)

print("\n" + "=" * 80)
print(f"✓ Analysis complete! Results saved to {output_file}")

# Summary statistics
print("\n=== Summary Statistics ===")
print(f"Total issues annotated: {len(results_df)}")
related_count = results_df['is_related'].sum() if results_df['is_related'].dtype == 'bool' else len(results_df[results_df['is_related'] == True])
print(f"Related issues: {related_count}")
print(f"Unrelated issues: {len(results_df) - related_count}")

# Cost tracking
print("\n=== Token Usage & Cost ===")
print(f"Input tokens: {total_input_tokens:,}")
print(f"Output tokens: {total_output_tokens:,}")
print(f"Cache read tokens: {total_cache_read_tokens:,}")
print(f"Cache creation tokens: {total_cache_creation_tokens:,}")

# Claude Sonnet 4.5 pricing (as of Dec 2024)
# Input: $3/M, Output: $15/M, Cache writes: $3.75/M, Cache reads: $0.30/M
input_cost = (total_input_tokens / 1_000_000) * 3.0
output_cost = (total_output_tokens / 1_000_000) * 15.0
cache_write_cost = (total_cache_creation_tokens / 1_000_000) * 3.75
cache_read_cost = (total_cache_read_tokens / 1_000_000) * 0.30
total_cost = input_cost + output_cost + cache_write_cost + cache_read_cost

print(f"\nEstimated cost breakdown:")
print(f"  Input tokens: ${input_cost:.4f}")
print(f"  Output tokens: ${output_cost:.4f}")
print(f"  Cache creation: ${cache_write_cost:.4f}")
print(f"  Cache reads: ${cache_read_cost:.4f}")
print(f"  TOTAL: ${total_cost:.2f}")
print(f"  Cost per issue: ${total_cost/len(results_df):.4f}")