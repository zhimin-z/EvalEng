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

# Read the issues CSV
df = pd.read_csv("data/github_issues.csv", encoding="utf-8")
sample_size = min(400, len(df))
df = df.sample(n=sample_size, random_state=42)  # Randomly select a sample of issues for analysis
print(f"Total issues to analyze: {len(df)}")

# Condensed version of the evaluation workflow phases
STAGES_SUMMARY = """Unified Evaluation Workflow:

**Phase 0: Provisioning** - Setting up the runtime environment to make evaluation executable.
- Step A: Harness Installation
  * Definition: Installing the evaluation framework and its dependencies.
  * Strategy 1: Git Clone - Cloning repositories and building from source code
  * Strategy 2: PyPI Packages - Installing via pip from PyPI or git URLs
  * Strategy 3: Node Package - Installing via npm, npx, or Homebrew
  * Strategy 4: Binary Packages - Downloading standalone executable files
  * Strategy 5: Container Images - Pulling Docker/OCI container images
- Step B: Credential Configuration
  * Definition: Setting up authentication credentials to access external services and resources.
  * Strategy 1: Model API Authentication - Configuring API keys to call remote model inference endpoints (OpenAI, Anthropic, HuggingFace APIs)
  * Strategy 2: Artifact Repository Authentication - Authenticating to download models and datasets from repositories (HuggingFace Hub, Zenodo)
  * Strategy 3: Evaluation Platform Authentication - Logging into evaluation platform accounts for accessing services and leaderboards

**Phase I: Specification** - Configuring what to evaluate and how to evaluate it.
- Step A: SUT Preparation
  * Definition: Configuring the System Under Test (SUT) - the primary model, algorithm, or system being evaluated.
  * Strategy 1: Model-as-a-Service - Setting up remote API-based models (OpenAI, Anthropic, cloud providers)
  * Strategy 2: Model-in-Process - Loading models locally into memory for inference (LLMs, VLMs, traditional ML models)
  * Strategy 3: Non-Parametric Algorithms - Configuring rule-based algorithms without learned weights (Approximate Nearest Neighbor (ANN) algorithms, BM25, signal processing)
  * Strategy 4: Interactive Agents - Setting up agents that make sequential decisions over time (RL policies, multi-agent systems, robot controllers)
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

**Phase II: Execution** - Running the SUT to generate outputs.
- Step A: SUT Invocation
  * Definition: Actually running the SUT on test inputs to produce outputs or actions.
  * Strategy 1: Batch Inference - Running many test inputs through the SUT, one evaluation run at a time
  * Strategy 2: Arena Battle - Running the same input through multiple SUTs simultaneously for head-to-head comparison
  * Strategy 3: Interactive Loop - Repeatedly executing the SUT's actions in an environment over multiple timesteps
  * Strategy 4: Production Streaming - Continuously processing live incoming requests in real-time

**Phase III: Assessment** - Measuring how well the SUT performed.
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

**Phase IV: Reporting** - Presenting and communicating evaluation results.
- Step A: Insight Presentation
  * Definition: Making results understandable and actionable for users.
  * Strategy 1: Execution Tracing - Recording detailed execution logs or trajectories showing what happened during each test run
  * Strategy 2: Subgroup Analysis - Breaking down performance by categories (task types, demographic groups, difficulty levels)
  * Strategy 3: Regression Alerting - Automatically detecting when performance drops below previous baselines
  * Strategy 4: Chart Generation - Creating visualizations like plots, charts, and graphs
  * Strategy 5: Dashboard Creation - Building interactive web interfaces to explore results
  * Strategy 6: Leaderboard Publication - Submitting scores to public comparison leaderboards"""

SYSTEM_PROMPT = f"""You are an expert in machine learning evaluation harnesses.

Analyze GitHub issues from evaluation harness repositories to determine:
1. Whether the issue relates to any part of the evaluation workflow below
2. If so, identify the most specific level: Phase, Step, and Strategy
3. Explain what causes this issue

{STAGES_SUMMARY}

Return a JSON object:
{{
    "is_related": true/false,
    "phase": "X" or null,
    "step": "Y" or null,
    "strategy": "Z" or null,
    "root_cause": "One-liner explaining the root cause" or null,
    "confidence": "high/medium/low"
}}

Notes:
- Even if is_related is true, step and strategy are optional (may be null if issue is general to a phase)
- Be as specific as possible - if you can identify the strategy, include it
- root_cause should explain what technical issue or gap causes the problem
- Only mark as related if there's a clear connection to the evaluation workflow."""

def analyze_issue(title, body, harness_name):
    """Analyze a single issue using the configured LLM model"""
    issue_text = f"Harness: {harness_name}\nTitle: {title}\nBody: {body if pd.notna(body) and body.strip() else 'No description'}"

    try:
        response = completion(
            model=MODEL,
            max_tokens=512,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
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
        return result

    except Exception as e:
        print(f"  Error: {str(e)[:100]}")
        return {
            "is_related": None,
            "phase": None,
            "step": None,
            "strategy": None,
            "root_cause": f"Error: {str(e)[:100]}",
            "confidence": None
        }

# Analyze all issues
results = []
print("\nStarting analysis...")
print("=" * 80)

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Analyzing issues"):
    analysis = analyze_issue(
        title=row['issue_title'],
        body=row['issue_body'],
        harness_name=row['harness_name']
    )

    result_row = {
        'harness_name': row['harness_name'],
        'github_repo': row['github_repo'],
        'issue_title': row['issue_title'],
        'issue_body': row['issue_body'],
        'issue_url': row['issue_url'],
        'issue_created_at': row['issue_created_at'],
        'issue_closed_at': row['issue_closed_at'],
        'is_related': analysis.get('is_related'),
        'phase': analysis.get('phase'),
        'step': analysis.get('step'),
        'strategy': analysis.get('strategy'),
        'root_cause': analysis.get('root_cause'),
        'confidence': analysis.get('confidence')
    }
    results.append(result_row)

    # Small delay for rate limiting
    time.sleep(0.3)

# Create results DataFrame
results_df = pd.DataFrame(results)

# Save to CSV
os.makedirs("data", exist_ok=True)
output_file = "data/github_issues_analyzed.json"
results_df.to_json(output_file, orient="records", lines=True, force_ascii=False)

print("\n" + "=" * 80)
print(f"✓ Analysis complete! Results saved to {output_file}")

# Summary statistics
print("\n=== Summary Statistics ===")
print(f"Total issues analyzed: {len(results_df)}")
related_count = results_df['is_related'].sum() if results_df['is_related'].dtype == 'bool' else len(results_df[results_df['is_related'] == True])
print(f"Related issues: {related_count}")
print(f"Unrelated issues: {len(results_df) - related_count}")