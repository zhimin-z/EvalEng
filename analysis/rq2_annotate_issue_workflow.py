import pandas as pd
import dotenv
import json
import time
import re
import backoff

from tqdm import tqdm
from litellm import completion, RateLimitError

# Load environment variables
dotenv.load_dotenv(override=True)

# Set the model to use - can be changed to any LiteLLM supported model
MODEL = "anthropic/claude-haiku45-20251001"

# Read the issues JSONL
df = pd.read_json("../data/rq2_issues.jsonl", orient="records", lines=True)
# df = df.sample(n=377, random_state=42)  # https://www.calculator.net/sample-size-calculator.html?type=1&cl=95&ci=5&pp=50&ps=20000&x=Calculate
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

**Stage 1: Specification** - Configuring what to evaluate and how to evaluate it.
- Step A: SUT Preparation
  * Definition: Configuring the System Under Test (SUT) - the primary model, algorithm, or system being evaluated.
  * Strategy 1: Model-as-a-Service - Setting up REMOTE API-based models running on external infrastructure [Keywords: API endpoint, remote, cloud, OpenAI API, Anthropic API]
  * Strategy 2: Model-in-Process - LOADING models locally into memory for inference [Keywords: load weights, local inference, VRAM, GPU memory, model.load()]
  * Strategy 3: Non-Parametric Algorithm - Configuring algorithms WITHOUT learned weights [Keywords: BM25, FAISS, ANN index, rule-based, no training]
  * Strategy 4: Interactive Agent - Setting up entities that make SEQUENTIAL decisions over MULTIPLE timesteps [Keywords: agent loop, environment, multi-step, RL policy, tool use]
- Step B: Benchmark Inputs Preparation
  * Definition: Preparing test inputs (questions, prompts, images, scenarios) that will be FED TO the SUT during execution.
  * Strategy 1: Benchmark Data Preparation - Loading existing test datasets or custom test cases [Keywords: dataset download, test split, input prompts, questions]
  * Strategy 2: Synthetic Data Generation - Automatically generating new test inputs [Keywords: augmentation, perturbation, synthetic generation]
  * Strategy 3: Simulation Environment Setup - Creating interactive virtual environments [Keywords: 3D scene, environment reset, task config, simulator]
  * Strategy 4: Production Traffic Sampling - Collecting real-world user queries [Keywords: live traffic, production logs, user requests]
- Step C: Benchmark References Preparation
  * Definition: Preparing reference materials used to SCORE/JUDGE SUT outputs (NOT fed to SUT).
  * Strategy 1: Ground Truth Preparation - Loading reference answers/labels used FOR COMPARISON [Keywords: gold labels, reference answers, ground truth, annotations]
  * Strategy 2: Judge Preparation - Setting up LLM/classifier models to ACT AS evaluators [Keywords: judge model, evaluator, preference model, critic]

**Stage 2: Execution** - Running the SUT to generate outputs.
- Step A: SUT Invocation
  * Definition: Actually RUNNING/EXECUTING the SUT on test inputs to produce outputs or actions.
  * Strategy 1: Batch Inference - Running MULTIPLE inputs through ONE SUT instance [Keywords: inference loop, batch processing, generate output, model.predict()]
  * Strategy 2: Arena Battle - Running SAME input through MULTIPLE SUTs simultaneously [Keywords: head-to-head, A/B comparison, simultaneous execution, pairwise]
  * Strategy 3: Interactive Loop - ITERATIVELY executing SUT actions in environment [Keywords: step(), observation-action loop, rollout, trajectory, episode]
  * Strategy 4: Production Streaming - Continuously processing LIVE real-time requests [Keywords: streaming, real-time, online inference, production traffic]

**Stage 3: Assessment** - Measuring how well the SUT performed.
- Step A: Individual Scoring
  * Definition: COMPUTING metrics/scores for INDIVIDUAL test instances (per-sample scoring).
  * Strategy 1: Deterministic Measurement - Rule-based/algorithmic scoring WITHOUT ML models [Keywords: exact match, BLEU, ROUGE, edit distance, accuracy, F1]
  * Strategy 2: Embedding Measurement - Semantic similarity using EMBEDDINGS/latent representations [Keywords: BERTScore, cosine similarity, embedding distance, SBERT]
  * Strategy 3: Subjective Measurement - Using LLM/classifier AS JUDGE to rate quality [Keywords: GPT4 judge, preference model, pairwise comparison, LLM-as-judge]
  * Strategy 4: Performance Measurement - Measuring RESOURCE consumption/efficiency [Keywords: latency, throughput, memory usage, FLOPs, speed, cost]
- Step B: Aggregate Scoring
  * Definition: AGGREGATING per-instance scores into benchmark-level summary metrics.
  * Strategy 1: Distributional Statistics - Computing summary stats across all instances [Keywords: mean, average, median, percentile, weighted average]
  * Strategy 2: Uncertainty Quantification - Calculating confidence intervals/significance [Keywords: bootstrap, confidence interval, standard error, p-value]

**Stage 4: Reporting** - Presenting and communicating evaluation results.
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

**S0-B Credentials (by PURPOSE):**
  Strategy 1 = DOWNLOADING artifacts | Strategy 2 = CALLING APIs | Strategy 3 = PLATFORM access
  ✓ "HF login to download Llama fails" → S0-B1  |  ✓ "OpenAI API key invalid" → S0-B2  |  ✓ "EvalAI login breaks" → S0-B3

**S1-A SUT Type (by EXECUTION):**
  Strategy 1 = Local weights | Strategy 2 = Remote API | Strategy 3 = Multi-step | Strategy 4 = No weights
  ✓ "OOM loading model" → S1-A1  |  ✓ "API timeout" → S1-A2  |  ✓ "Agent loop stuck" → S1-A3  |  ✓ "BM25 index fails" → S1-A4

**S1-B vs S1-C (by DATA FLOW):**
  S1-B = Fed TO SUT  |  S1-C = Used FOR scoring
  ✓ "Test prompts missing" → S1-B  |  ✓ "Ground truth labels missing" → S1-C

**S1-A vs S2-A (by PHASE):**
  S1-A = LOADING/config  |  S2-A = RUNNING/inference
  ✓ "Model load OOM" → S1-A2  |  ✓ "Generation timeout" → S2-A1

**S3-A Scoring (by METHOD):**
  Strategy 1 = Algorithmic | Strategy 2 = LLM judge | Strategy 3 = Embeddings | Strategy 4 = Resources
  ✓ "BLEU bug" → S3-A1  |  ✓ "GPT5 judge fails" → S3-A2  |  ✓ "BERTScore crash" → S3-A3  |  ✓ "Latency broken" → S3-A4

STAGE DECISION TREE:
Setup tools? → 0 | Configure test? → 1 | Run SUT? → 2 | Compute scores? → 3 | Display results? → 4

KEY PRINCIPLE: Choose PRIMARY/EARLIEST blocker (e.g., "Can't run tests due to pip install" → Stage 0)

## VALIDATION RULES

1. is_related=false → all fields null
2. is_related=true → stage NOT null
3. strategy set → step MUST be set
4. step set → stage MUST be set
5. Stage: 0, 1, 2, 3, or 4
6. Step: "A", "B", "C"
7. Strategy: 1, 2, 3, 4, 5, or 6

## OUTPUT FORMAT

CRITICAL: Your ENTIRE response must be ONLY the JSON object below. Do NOT include:
- Explanatory text before or after the JSON
- Markdown code blocks or backticks
- Any conversational responses
- Questions or clarifications

Return EXACTLY this format (raw JSON only):

{{"is_related": true, "stage": "0", "step": "A", "strategy": "2"}}

or

{{"is_related": false, "stage": null, "step": null, "strategy": null}}

If information is insufficient, make your best judgment based on available details."""

def strip_code_blocks(text):
    """Replace all code blocks with [CODE] placeholder to reduce token usage"""
    if not text:
        return text
    # Replace triple backtick code blocks with [CODE]
    return re.sub(r'```[\s\S]*?```', '[CODE]', text)

@backoff.on_exception(
    backoff.expo,
    (RateLimitError, Exception),
    max_tries=5,
    max_time=300,
    giveup=lambda e: not isinstance(e, RateLimitError) and "rate" not in str(e).lower()
)
def analyze_issue(title, body, harness_name, comments=None):
    """Analyze a single issue using the configured LLM model"""
    # Strip code blocks from body
    body_stripped = strip_code_blocks(body) if pd.notna(body) else None
    issue_text = f"Harness: {harness_name}\nTitle: {title}\nBody: {body_stripped if body_stripped and body_stripped.strip() else 'No description'}"

    # Add comments if available
    if comments and len(comments) > 0:
        issue_text += f"\n\nComments ({len(comments)}):\n"
        for i, comment in enumerate(comments, 1):
            comment_stripped = strip_code_blocks(comment) if comment else ""
            issue_text += f"[Comment {i}] {comment_stripped}\n"

    try:
        response = completion(
            model=MODEL,
            max_tokens=200,  # Increased buffer for potential wrapping
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": SYSTEM_PROMPT,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                },
                {"role": "user", "content": issue_text}
            ]
        )

        response_text = response.choices[0].message.content.strip()

        # Validate response is not empty
        if not response_text:
            raise ValueError("Empty response from model")

        # Extract JSON from markdown code blocks if present
        if response_text.startswith("```json"):
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif response_text.startswith("```"):
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        # Check if response starts with { (valid JSON)
        if not response_text.startswith("{"):
            raise ValueError(f"Response is not JSON: {response_text[:100]}")

        result = json.loads(response_text)

        return result

    except Exception as e:
        print(f"  Error: {str(e)}")
        return {
            "is_related": None,
            "stage": None,
            "step": None,
            "strategy": None
        }

# Analyze all issues
results = []

# Set up output file path
output_file = "../data/rq2_issues_annotated_full.jsonl"

print("\nStarting analysis...")
print("=" * 80)

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Analyzing issues"):
    analysis = analyze_issue(
        title=row['issue_title'],
        body=row['issue_body'],
        harness_name=row['harness_name'],
        comments=row["issue_comments"]
    )

    result_row = {
        'harness_name': row['harness_name'],
        'github_repo': row['github_repo'],
        'issue_title': row['issue_title'],
        'issue_body': row['issue_body'],
        'issue_url': row['issue_url'],
        'issue_comments': row['issue_comments'],
        'issue_created_at': row['issue_created_at'],
        'issue_closed_at': row['issue_closed_at'],
        'is_related': analysis.get('is_related'),
        'stage': analysis.get('stage'),
        'step': analysis.get('step'),
        'strategy': analysis.get('strategy')
    }
    results.append(result_row)

    # Save every 50 issues
    if len(results) % 50 == 0:
        pd.DataFrame(results).to_json(output_file, orient="records", lines=True, mode='a')
        print(f"\n✓ Saved progress: {len(results)} new issues appended")
        results = []

    # Small delay for rate limiting
    time.sleep(0.1)

# Save any remaining results
if results:
    pd.DataFrame(results).to_json(output_file, orient="records", lines=True, mode='a')

print("\n" + "=" * 80)
print(f"✓ Analysis complete! Results saved to {output_file}")