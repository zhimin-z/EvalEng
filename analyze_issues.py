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
df = pd.read_csv("github_issues.old.csv", encoding="utf-8")
df = df.tail(300)  # Test with last 300 samples only
print(f"Total issues to analyze: {len(df)}")

# Condensed version of the evaluation workflow phases
STAGES_SUMMARY = """Evaluation Workflow Phases:

**Phase 0: Provisioning** - Establishing the technical foundation—you cannot evaluate what you cannot run.
- Step A: Harness Installation
  * Definition: Installing dependencies, compiling binaries, building containers, and configuring execution backends.
  * Strategy 1: Git Clone - Cloning repositories and building from source code
  * Strategy 2: PyPI Packages - Installing via pip, requirements files, git-based installations
  * Strategy 3: Node Package - Installing via npm, npx, or Homebrew
  * Strategy 4: Binary Packages - Downloading standalone executables
  * Strategy 5: Container Images - Pulling Docker/OCI images
- Step B: Credential Configuration
  * Definition: Authenticating with model repositories, dataset platforms, evaluation services, and leaderboard APIs.
  * Strategy 1: Model API Authentication - API keys for remote inference (OpenAI, Anthropic, HuggingFace APIs)
  * Strategy 2: Artifact Repository Authentication - Accessing gated/private models and datasets (HuggingFace Hub, Zenodo)
  * Strategy 3: Evaluation Platform Authentication - Account login for platform services and leaderboards

**Phase I: Specification** - Defining the evaluation experiment—what to test, what to test it with, and how to judge the results.
- Step A: SUT Preparation
  * Definition: Specifying how to interact with the System Under Test (SUT).
  * Strategy 1: Model-as-a-Service - Remote inference via APIs (OpenAI, Anthropic, cloud providers)
  * Strategy 2: Model-in-Process - Local inference with loaded weights (LLMs, VLMs, traditional ML)
  * Strategy 3: Non-Parametric Algorithms - Deterministic computation (ANN, BM25, signal processing)
  * Strategy 4: Interactive Agents - Sequential decision-making (RL policies, multi-agent systems, robot controllers)
- Step B: Benchmark Preparation (Inputs)
  * Definition: Acquiring and configuring the test inputs that will be used to evaluate the SUT.
  * Strategy 1: Benchmark Data Preparation - Loading pre-existing datasets or custom inputs
  * Strategy 2: Synthetic Data Generation - Creating test data via perturbation, augmentation, synthesis
  * Strategy 3: Simulation Environment Setup - Initializing interactive 3D environments, scenes, tasks
  * Strategy 4: Production Traffic Sampling - Sampling real-world inference traffic
- Step C: Benchmark Preparation (References)
  * Definition: Pre-computing judges, references, and ground truth materials that will be used to score SUT outputs.
  * Strategy 1: Ground Truth Preparation - Human annotations, embeddings, knowledge claims, baselines
  * Strategy 2: Judge Preparation - Training or loading judge models for evaluation

**Phase II: Execution** - Observing SUT behavior—applying test inputs to elicit outputs and actions.
- Step A: SUT Invocation
  * Definition: Running the System Under Test to generate outputs or take actions.
  * Strategy 1: Batch Inference - Multiple inputs through single SUT instance
  * Strategy 2: Arena Battle - Same input across multiple SUTs for pairwise comparison
  * Strategy 3: Interactive Loop - Iterative state transitions via tool use, simulation, multi-agent coordination
  * Strategy 4: Production Streaming - Real-time processing of live traffic

**Phase III: Assessment** - Converting observations into measurements—judging outputs against quality criteria to produce scores.
- Step A: Individual Scoring
  * Definition: Computing metrics for individual test instances based on SUT outputs.
  * Strategy 1: Deterministic Measurement - Equality checks, edit distance, BLEU, ROUGE
  * Strategy 2: Embedding Measurement - Semantic similarity via embeddings, cross-modal comparisons
  * Strategy 3: Subjective Measurement - LLM/classifier judges for pairwise or quality assessment
  * Strategy 4: Performance Measurement - Latency, throughput, memory, FLOPs, energy
- Step B: Aggregate Scoring
  * Definition: Aggregating instance-level scores into benchmark-level metrics.
  * Strategy 1: Distributional Statistics - Averaging, quantiles, weighted aggregation, rank fusion
  * Strategy 2: Uncertainty Quantification - Bootstrap resampling, Prediction-Powered Inference (PPI)

**Phase IV: Reporting** - Making results actionable—translating metrics into stakeholder-facing insights.
- Step A: Insight Presentation
  * Definition: Visualizing metrics and publishing results to internal/external audiences.
  * Strategy 1: Execution Tracing - Step-by-step logs, function calls, execution flow, with configurable recording backends (JSON Lines, databases, HTTP endpoints, console-only, cloud storage)
  * Strategy 2: Subgroup Analysis - Performance by demographics, domains, task categories
  * Strategy 3: Regression Alerting - Comparing against baselines, detecting degradation
  * Strategy 4: Chart Generation - Radar charts, drift histograms, performance trends
  * Strategy 5: Dashboard Creation - Interactive web interfaces, metric comparisons
  * Strategy 6: Leaderboard Publication - Submitting to public/private leaderboards"""

SYSTEM_PROMPT = f"""You are an expert in machine learning evaluation harnesses.

Analyze GitHub issues from evaluation harness repositories to determine:
1. Whether the issue relates to any part of the evaluation workflow below
2. If so, identify the most specific level: Phase, Step, and Strategy
3. Explain what causes this issue

{STAGES_SUMMARY}

Return a JSON object:
{{
    "is_related": true/false,
    "phase": "Phase X" or null,
    "step": "Step X" or null,
    "strategy": "Strategy X" or null,
    "root_cause": "Brief explanation of what causes this issue (max 50 words)" or null,
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
output_file = "data/github_issues_analyzed.csv"
results_df.to_csv(output_file, index=False, encoding="utf-8")

print("\n" + "=" * 80)
print(f"✓ Analysis complete! Results saved to {output_file}")

# Summary statistics
print("\n=== Summary Statistics ===")
print(f"Total issues analyzed: {len(results_df)}")
related_count = results_df['is_related'].sum() if results_df['is_related'].dtype == 'bool' else len(results_df[results_df['is_related'] == True])
print(f"Related issues: {related_count}")
print(f"Unrelated issues: {len(results_df) - related_count}")

if related_count > 0:
    print("\nRelated issues by phase, step, and strategy:")
    # Combine phase, step, and strategy for better breakdown
    related_df = results_df[results_df['is_related'] == True].copy()
    related_df['phase_step_strategy'] = related_df.apply(
        lambda row: (
            f"{row['phase']} → {row['step']} → {row['strategy']}" if pd.notna(row['strategy'])
            else f"{row['phase']} → {row['step']}" if pd.notna(row['step'])
            else row['phase']
        ),
        axis=1
    )
    phase_step_strategy_counts = related_df['phase_step_strategy'].value_counts()
    for phase_step_strategy, count in phase_step_strategy_counts.items():
        print(f"  {phase_step_strategy}: {count}")
