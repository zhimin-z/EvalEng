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

# Read the issues JSONL
df = pd.read_json("data/github_issues.jsonl", orient="records", lines=True)
df = df.sample(n=377, random_state=42)  # Randomly select a sample of issues for analysis
print(f"Total issues to analyze: {len(df)}")

# Condensed version of the evaluation workflow stages
STAGES_SUMMARY = """Unified Evaluation Workflow:

**Stage 0: Provisioning** - Setting up the runtime environment to make evaluation executable.
- Step A: Harness Installation
  * Definition: Installing the evaluation framework and its dependencies.
  * Strategy 1: Git Clone - Cloning repositories and building from source code [Keywords: git clone, build, compile]
  * Strategy 2: Python Package - Installing via pip, uv, conda, or poetry [Keywords: pip install, conda, requirements.txt]
  * Strategy 3: Node Package - Installing via npm, npx, or Homebrew [Keywords: npm, npx, package.json]
  * Strategy 4: Binary Package - Downloading standalone executable files [Keywords: binary, executable, download]
  * Strategy 5: Container Image - Pulling Docker/OCI container images [Keywords: docker, container, image pull]
- Step B: Credential Configuration
  * Definition: Setting up authentication credentials to access external services and resources.
  * Strategy 1: Model API Authentication - Configuring API keys to CALL/INVOKE remote model endpoints (OpenAI, Anthropic, HuggingFace Inference API) [Keywords: API key, rate limit, endpoint, inference call]
  * Strategy 2: Artifact Repository Authentication - Authenticating to DOWNLOAD models/datasets from repositories (HuggingFace Hub, Zenodo, ModelScope) [Keywords: login, download, gated model, access token]
  * Strategy 3: Evaluation Platform Authentication - Logging into evaluation platform to ACCESS features (leaderboards, dashboards, submissions) [Keywords: platform login, account, leaderboard access]

**Stage I: Specification** - Configuring what to evaluate and how to evaluate it.
- Step A: SUT Preparation
  * Definition: Configuring the System Under Test (SUT) - the primary model, algorithm, or system being evaluated.
  * Strategy 1: Model-as-a-Service - Setting up REMOTE API-based models running on external infrastructure [Keywords: API endpoint, remote, cloud, OpenAI API, Anthropic API]
  * Strategy 2: Model-in-Process - LOADING models locally into memory for inference [Keywords: load weights, local inference, VRAM, GPU memory, model.load()]
  * Strategy 3: Non-Parametric Algorithm - Configuring algorithms WITHOUT learned weights [Keywords: BM25, FAISS, ANN index, rule-based, no training]
  * Strategy 4: Interactive Agent - Setting up entities that make SEQUENTIAL decisions over MULTIPLE timesteps [Keywords: agent loop, environment, multi-step, RL policy, tool use]
- Step B: Benchmark Preparation (Inputs)
  * Definition: Preparing test inputs (questions, prompts, images, scenarios) that will be FED TO the SUT during execution.
  * Strategy 1: Benchmark Data Preparation - Loading existing test datasets or custom test cases [Keywords: dataset download, test split, input prompts, questions]
  * Strategy 2: Synthetic Data Generation - Automatically generating new test inputs [Keywords: augmentation, perturbation, synthetic generation]
  * Strategy 3: Simulation Environment Setup - Creating interactive virtual environments [Keywords: 3D scene, environment reset, task config, simulator]
  * Strategy 4: Production Traffic Sampling - Collecting real-world user queries [Keywords: live traffic, production logs, user requests]
- Step C: Benchmark Preparation (References)
  * Definition: Preparing reference materials used to SCORE/JUDGE SUT outputs (NOT fed to SUT).
  * Strategy 1: Ground Truth Preparation - Loading reference answers/labels used FOR COMPARISON [Keywords: gold labels, reference answers, ground truth, annotations]
  * Strategy 2: Judge Preparation - Setting up LLM/classifier models to ACT AS evaluators [Keywords: judge model, evaluator, preference model, critic]

**Stage II: Execution** - Running the SUT to generate outputs.
- Step A: SUT Invocation
  * Definition: Actually RUNNING/EXECUTING the SUT on test inputs to produce outputs or actions.
  * Strategy 1: Batch Inference - Running MULTIPLE inputs through ONE SUT instance [Keywords: inference loop, batch processing, generate output, model.predict()]
  * Strategy 2: Arena Battle - Running SAME input through MULTIPLE SUTs simultaneously [Keywords: head-to-head, A/B comparison, simultaneous execution, pairwise]
  * Strategy 3: Interactive Loop - ITERATIVELY executing SUT actions in environment [Keywords: step(), observation-action loop, rollout, trajectory, episode]
  * Strategy 4: Production Streaming - Continuously processing LIVE real-time requests [Keywords: streaming, real-time, online inference, production traffic]

**Stage III: Assessment** - Measuring how well the SUT performed.
- Step A: Individual Scoring
  * Definition: COMPUTING metrics/scores for INDIVIDUAL test instances (per-sample scoring).
  * Strategy 1: Deterministic Measurement - Rule-based/algorithmic scoring WITHOUT ML models [Keywords: exact match, BLEU, ROUGE, edit distance, accuracy, F1]
  * Strategy 2: Embedding Measurement - Semantic similarity using EMBEDDINGS/latent representations [Keywords: BERTScore, cosine similarity, embedding distance, SBERT]
  * Strategy 3: Subjective Measurement - Using LLM/classifier AS JUDGE to rate quality [Keywords: GPT-4 judge, preference model, pairwise comparison, LLM-as-judge]
  * Strategy 4: Performance Measurement - Measuring RESOURCE consumption/efficiency [Keywords: latency, throughput, memory usage, FLOPs, speed, cost]
- Step B: Aggregate Scoring
  * Definition: AGGREGATING per-instance scores into benchmark-level summary metrics.
  * Strategy 1: Distributional Statistics - Computing summary stats across all instances [Keywords: mean, average, median, percentile, weighted average]
  * Strategy 2: Uncertainty Quantification - Calculating confidence intervals/significance [Keywords: bootstrap, confidence interval, standard error, p-value]

**Stage IV: Reporting** - Presenting and communicating evaluation results.
- Step A: Insight Presentation
  * Definition: VISUALIZING and PUBLISHING results to make them understandable and actionable.
  * Strategy 1: Execution Tracing - Recording DETAILED logs/trajectories of execution steps [Keywords: trace, logging, step-by-step, execution path, debug output]
  * Strategy 2: Subgroup Analysis - STRATIFYING performance by categories/groups [Keywords: breakdown by category, demographic splits, per-task analysis, grouped metrics]
  * Strategy 3: Regression Alerting - DETECTING performance degradation vs baselines [Keywords: regression detection, alert, threshold, performance drop, baseline comparison]
  * Strategy 4: Chart Generation - Creating VISUAL plots/graphs [Keywords: plot, chart, visualization, graph, radar chart, histogram]
  * Strategy 5: Dashboard Creation - Building INTERACTIVE web UI for results [Keywords: dashboard, web interface, UI, interactive display, result viewer]
  * Strategy 6: Leaderboard Publication - SUBMITTING results to public rankings [Keywords: leaderboard, submission, public benchmark, ranking, competition]"""

SYSTEM_PROMPT = f"""You are an expert classifier for machine learning evaluation workflow issues.

TASK: Classify ONE GitHub issue into the evaluation workflow taxonomy below.

WORKFLOW TAXONOMY:
{STAGES_SUMMARY}

## STEP 1: DETERMINE RELEVANCE (is_related: true/false)

Mark is_related=true if the issue directly affects ANY stage of the evaluation workflow above (Provisioning, Specification, Execution, Assessment, Reporting). This includes bugs, failures, missing features, or documentation gaps that prevent/change workflow actions.

## STEP 2: ASSIGN LABELS (stage, step, strategy)

HIERARCHICAL CLASSIFICATION FRAMEWORK:
1. **Stage** = WHEN in the workflow does the issue occur? (Provisioning → Specification → Execution → Assessment → Reporting)
2. **Step** = WHAT component within that stage is affected? (e.g., within Provisioning: installation vs credentials)
3. **Strategy** = HOW specifically is that component implemented? (e.g., within installation: pip vs Docker vs npm)

CLASSIFICATION APPROACH:
- Understand the CORE PROBLEM semantically first
- Match to appropriate Stage/Step/Strategy from taxonomy
- Keywords are INDICATORS, not strict requirements
- Always assign Stage if is_related=true
- Assign Step/Strategy only if clearly identifiable
- If uncertain at any level, use null (e.g., Stage only without Step)
- If multiple stages relevant → choose PRIMARY blocker (earliest failure point)
- Semantic understanding > keyword matching

CRITICAL DISAMBIGUATION RULES:

**0-B Credentials (by PURPOSE):**
  Strategy 1 = CALLING APIs | Strategy 2 = DOWNLOADING artifacts | Strategy 3 = PLATFORM access
  ✓ "OpenAI API key invalid" → 0-B-1  |  ✓ "HF login to download Llama" → 0-B-2  |  ✓ "EvalAI login fails" → 0-B-3

**I-A SUT Type (by EXECUTION):**
  Strategy 1 = Remote API | Strategy 2 = Local weights | Strategy 3 = No weights | Strategy 4 = Multi-step
  ✓ "API timeout" → I-A-1  |  ✓ "OOM loading model" → I-A-2  |  ✓ "BM25 index fails" → I-A-3  |  ✓ "Agent loop stuck" → I-A-4

**I-B vs I-C (by DATA FLOW):**
  I-B = Fed TO SUT  |  I-C = Used FOR scoring
  ✓ "Test prompts missing" → I-B  |  ✓ "Ground truth labels missing" → I-C

**I-A vs II-A (by PHASE):**
  I-A = LOADING/config  |  II-A = RUNNING/inference
  ✓ "Model load OOM" → I-A-2  |  ✓ "Generation timeout" → II-A-1

**III-A Scoring (by METHOD):**
  Strategy 1 = Algorithmic | Strategy 2 = Embeddings | Strategy 3 = LLM judge | Strategy 4 = Resources
  ✓ "BLEU bug" → III-A-1  |  ✓ "BERTScore crash" → III-A-2  |  ✓ "GPT-4 judge fails" → III-A-3  |  ✓ "Latency broken" → III-A-4

STAGE DECISION TREE:
Setup tools? → 0 | Configure test? → I | Run SUT? → II | Compute scores? → III | Display results? → IV

KEY PRINCIPLE: Choose PRIMARY/EARLIEST blocker (e.g., "Can't run tests due to pip install" → Stage 0)

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