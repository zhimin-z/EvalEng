"""
Cluster harnesses based on their similarity in supporting different stages/steps/strategies.

This script:
1. Parses the workflow markdown to extract strategy support for each harness
2. Builds a binary feature matrix (harnesses x strategies)
3. Applies hierarchical clustering with appropriate distance metrics
4. Identifies natural cluster groupings
5. Uses LLM to automatically interpret and name each cluster
"""

import re
import json
import pandas as pd
import numpy as np
import dotenv
import backoff
from pathlib import Path
from collections import defaultdict
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import silhouette_score
from litellm import completion, RateLimitError

# Load environment variables
dotenv.load_dotenv(override=True)

# LLM model for cluster interpretation
MODEL = "anthropic/claude-haiku-4-5-20251001"


# =============================================================================
# LLM HELPER FUNCTIONS
# =============================================================================

@backoff.on_exception(backoff.expo, RateLimitError, max_tries=5)
def call_llm(prompt: str, system: str = None) -> str:
    """Call the LLM with retry on rate limit."""
    messages = [{"role": "user", "content": prompt}]
    response = completion(
        model=MODEL,
        messages=messages,
        system=system,
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


# Complete workflow reference for LLM interpretation
WORKFLOW_REFERENCE = """
## Unified Evaluation Workflow Stages

### Stage 0: Provisioning (The Runtime)
*Establishing the technical foundation—you cannot evaluate what you cannot run.*

- **Step A: Harness Installation** - Installing dependencies, compiling binaries, building containers
  - S0-A1: Git Clone - Cloning repository and installing from source
  - S0-A2: Python Package - Installing via pip, conda, poetry
  - S0-A3: Container Image - Pulling Docker/OCI images
  - S0-A4: Binary Package - Downloading standalone executables
  - S0-A5: Node Package - Installing via npm/npx

- **Step B: Credential Configuration** - Authenticating with services
  - S0-B1: Repository Authentication - HuggingFace Hub, Zenodo, ModelScope access
  - S0-B2: Model API Authentication - OpenAI/Anthropic/Gemini API keys
  - S0-B3: Evaluation Platform Authentication - Platform-specific login flows

### Stage 1: Specification (The Contract)
*Defining the evaluation experiment—what to test, what to test it with, how to judge.*

- **Step A: SUT Preparation** - Specifying the System Under Test
  - S1-A1: Model-in-Process (Local Inference) - Local models with weights loaded in memory
  - S1-A2: Model-as-a-Service (Remote Inference) - API-based model evaluation
  - S1-A3: Interactive Agent - Sequential decision-making agents (RL, multi-agent, robots)
  - S1-A4: Non-Parametric Algorithm - Deterministic algorithms (ANN, BM25, signal processing)

- **Step B: Benchmark Inputs Preparation** - Acquiring test inputs
  - S1-B1: Benchmark Data Preparation (Offline) - Loading predefined datasets
  - S1-B2: Simulation Environment Setup - 3D environments, physics simulation
  - S1-B3: Synthetic Data Generation - On-the-fly test generation
  - S1-B4: Production Traffic Sampling - Real-world inference traffic

- **Step C: Benchmark References Preparation** - Pre-computing scoring materials
  - S1-C1: Ground Truth Preparation - Human annotations, embedding indexes
  - S1-C2: Judge Preparation - Training/loading LLM judges and reward models

### Stage 2: Execution (The Run)
*Observing SUT behavior—applying test inputs to elicit outputs and actions.*

- **Step A: SUT Invocation** - Running the system under test
  - S2-A1: Batch Inference - Multiple samples through single SUT
  - S2-A2: Arena Battle - Same input across multiple SUTs simultaneously
  - S2-A3: Interactive Loop - Stateful stepping through state transitions
  - S2-A4: Production Streaming - Live traffic with real-time metrics

### Stage 3: Assessment (The Score)
*Converting observations into measurements—judging outputs against quality criteria.*

- **Step A: Individual Scoring** - Computing per-instance metrics
  - S3-A1: Deterministic Measurement - Exact match, BLEU, ROUGE, edit distance
  - S3-A2: Subjective Measurement - LLM-as-judge, classifier-based evaluation
  - S3-A3: Latent Measurement - Embedding similarity, BERTScore
  - S3-A4: Performance Measurement - Latency, throughput, memory, energy

- **Step B: Aggregate Scoring** - Combining instance scores
  - S3-B1: Distributional Statistics - Mean, quantiles, weighted aggregation
  - S3-B2: Uncertainty Quantification - Bootstrap, confidence intervals

### Stage 4: Reporting (The Output)
*Making results actionable—translating metrics into stakeholder-facing insights.*

- **Step A: Insight Presentation** - Visualizing and publishing results
  - S4-A1: Chart Generation - Radar charts, histograms, trend plots
  - S4-A2: Dashboard Creation - Interactive web interfaces
  - S4-A3: Leaderboard Publication - Public/private ranking submissions
  - S4-A4: Subgroup Analysis - Performance breakdown by categories
  - S4-A5: Execution Tracing - Step-by-step execution logs
  - S4-A6: Regression Alerting - Automated performance degradation detection
"""


def interpret_cluster(
    cluster_id: int,
    members: list[str],
    supported_strategies: list[str],
    missing_strategies: list[str],
    step_coverage: dict[str, float],
) -> dict:
    """Use LLM to interpret and name a cluster based on its characteristics."""

    prompt = f"""You are analyzing evaluation harnesses (tools for evaluating AI/ML models) grouped by unsupervised clustering based on their workflow support patterns.

{WORKFLOW_REFERENCE}

---

## Cluster {cluster_id} Analysis

**Members ({len(members)} harnesses):**
{', '.join(sorted(members))}

**Strategies supported by ALL members in this cluster:**
{', '.join(supported_strategies) if supported_strategies else 'None universally shared'}

**Strategies supported by NO members in this cluster:**
{', '.join(missing_strategies) if missing_strategies else 'None'}

**Stage-level coverage (proportion of strategies supported):**
{json.dumps(step_coverage, indent=2)}

---

Based on the workflow reference and cluster characteristics above, provide:
1. A short descriptive name for this cluster (2-5 words, capturing the distinguishing characteristic)
2. A one-sentence interpretation explaining what makes this group of harnesses similar and what distinguishes them from other clusters

Focus on:
- Which evaluation domains these harnesses serve (LLM evaluation, RL/robotics, retrieval, etc.)
- Key workflow capabilities they share or lack
- Their position in the evaluation ecosystem

Respond in JSON format:
{{"name": "...", "interpretation": "..."}}"""

    response = call_llm(prompt)

    # Parse JSON from response
    try:
        # Handle markdown code blocks if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        return json.loads(response.strip())
    except json.JSONDecodeError:
        return {"name": f"Cluster {cluster_id}", "interpretation": response}


# =============================================================================
# 1. PARSE WORKFLOW FILE
# =============================================================================

stages_file = Path('../data/rq1_workflow.md')
content = stages_file.read_text()

all_harnesses = set()
strategy_harnesses = defaultdict(set)  # (stage, step, strategy) -> set of harnesses

# Stage ordering for proper display
stage_order = {'0': 0, 'I': 1, 'i': 1, 'II': 2, 'ii': 2, 'III': 3, 'iii': 3, 'IV': 4, 'iv': 4}

# Parse all stages
for stage_match in re.finditer(r'### \*\*Stage ([0-9IViv]+):', content):
    stage_num = stage_match.group(1)
    stage_start = stage_match.start()
    next_stage = re.search(r'### \*\*Stage', content[stage_match.end():])
    stage_end = stage_match.end() + next_stage.start() if next_stage else len(content)
    stage_content = content[stage_start:stage_end]

    # Parse all steps in this stage
    for step_match in re.finditer(r'^\s{2}\* \*\*Step ([A-Z]):', stage_content, re.MULTILINE):
        step_letter = step_match.group(1)
        step_start = step_match.start()
        next_step = list(re.finditer(r'^\s{2}\* \*\*Step', stage_content[step_match.end():], re.MULTILINE))
        step_end = step_match.end() + next_step[0].start() if next_step else len(stage_content)
        step_content = stage_content[step_start:step_end]

        # Parse all strategies in this step
        for strategy_match in re.finditer(r'^\s{6}\* \*\*Strategy (\d+):', step_content, re.MULTILINE):
            strategy_num = int(strategy_match.group(1))
            strat_start = strategy_match.start()
            next_strat = list(re.finditer(r'^\s{6}\* \*\*Strategy', step_content[strategy_match.end():], re.MULTILINE))
            strat_end = strategy_match.end() + next_strat[0].start() if next_strat else len(step_content)
            strategy_text = step_content[strat_start:strat_end]

            # Extract harnesses from the last parenthesis
            harness_matches = list(re.finditer(r'\(\*([^)]+)\*\)', strategy_text))
            if harness_matches:
                harnesses_str = harness_matches[-1].group(1)
                if harnesses_str.strip().lower() == 'all':
                    # Will be expanded later once all_harnesses is complete
                    strategy_harnesses[(stage_num, step_letter, strategy_num)] = 'all'
                else:
                    harnesses_list = [h.strip() for h in harnesses_str.split(',')]
                    for h in harnesses_list:
                        all_harnesses.add(h)
                    strategy_harnesses[(stage_num, step_letter, strategy_num)] = set(harnesses_list)

# Expand 'all' entries now that we know all harnesses
for key, value in strategy_harnesses.items():
    if value == 'all':
        strategy_harnesses[key] = all_harnesses.copy()

harnesses = sorted(all_harnesses)
print(f"Found {len(harnesses)} unique harnesses")
print(f"Found {len(strategy_harnesses)} unique strategies across all stages/steps")

# =============================================================================
# 2. BUILD FEATURE MATRIX
# =============================================================================

# Sort strategy keys for consistent ordering
strategy_keys = sorted(
    strategy_harnesses.keys(),
    key=lambda x: (stage_order.get(x[0], 999), x[1], x[2])
)

# Create readable feature names
feature_names = [f"S{k[0]}-{k[1]}{k[2]}" for k in strategy_keys]

# Build binary feature matrix: rows = harnesses, columns = strategies
feature_matrix = np.zeros((len(harnesses), len(strategy_keys)), dtype=int)

for j, key in enumerate(strategy_keys):
    for harness in strategy_harnesses[key]:
        if harness in harnesses:
            i = harnesses.index(harness)
            feature_matrix[i, j] = 1

df_features = pd.DataFrame(feature_matrix, index=harnesses, columns=feature_names)
print(f"\nFeature matrix shape: {df_features.shape}")
print(f"Feature density: {feature_matrix.sum() / feature_matrix.size:.1%}")

# =============================================================================
# 3. COMPUTE DISTANCE MATRIX
# =============================================================================

# Jaccard distance is appropriate for binary data
# Jaccard distance = 1 - (intersection / union)
jaccard_distances = pdist(feature_matrix, metric='jaccard')
jaccard_dist_matrix = squareform(jaccard_distances)

# Also compute cosine distance for comparison
cosine_distances = pdist(feature_matrix, metric='cosine')

print(f"\nMean Jaccard distance: {jaccard_distances.mean():.3f}")
print(f"Mean Cosine distance: {cosine_distances.mean():.3f}")

# =============================================================================
# 4. HIERARCHICAL CLUSTERING (WARD LINKAGE)
# =============================================================================

# Perform hierarchical clustering with Ward linkage
Z_ward = linkage(feature_matrix, method='ward')

# Use k=6 clusters as determined by silhouette analysis
K_CLUSTERS = 6
cluster_labels = fcluster(Z_ward, K_CLUSTERS, criterion='maxclust')

# Calculate silhouette score for reporting
silhouette = silhouette_score(jaccard_dist_matrix, cluster_labels, metric='precomputed')
print(f"\nWard linkage with k={K_CLUSTERS}: silhouette={silhouette:.3f}")

# =============================================================================
# 5. CLUSTER ANALYSIS WITH LLM INTERPRETATION (before visualization)
# =============================================================================

# Aggregate features by stage for stage-level coverage calculation
stage_features = defaultdict(list)
for j, key in enumerate(strategy_keys):
    stage_features[key[0]].append(j)
stage_names = sorted(stage_features.keys(), key=lambda x: stage_order.get(x, 999))

# Group harnesses by cluster
clusters = defaultdict(list)
for harness, label in zip(harnesses, cluster_labels):
    clusters[label].append(harness)

# Check if interpretations file already exists to skip LLM calls
interpretations_file = Path('../data/rq1_cluster_ward.json')
if interpretations_file.exists():
    print("\nLoading existing cluster interpretations (skipping LLM calls)...")
    with open(interpretations_file) as f:
        existing_data = json.load(f)
    cluster_interpretations = existing_data["clusters"]
    cluster_id_to_name = {c["cluster_id"]: c["cluster_name"] for c in cluster_interpretations}

    # Print summary of loaded interpretations
    for c in cluster_interpretations:
        print(f"\n--- Cluster {c['cluster_id']} ({c['size']} harnesses) ---")
        print(f"Members: {', '.join(c['members'])}")
        print(f"Name: {c['cluster_name']}")
        print(f"Interpretation: {c['cluster_interpretation']}")
else:
    cluster_interpretations = []

    # Analyze each cluster
    for cluster_id in sorted(clusters.keys()):
        members = clusters[cluster_id]
        print(f"\n--- Cluster {cluster_id} ({len(members)} harnesses) ---")
        print(f"Members: {', '.join(sorted(members))}")

        # Find common strategies (supported by all members in this cluster)
        cluster_indices = [harnesses.index(h) for h in members]
        cluster_features = feature_matrix[cluster_indices, :]
        common_strategies = np.all(cluster_features == 1, axis=0)
        missing_strategies = np.all(cluster_features == 0, axis=0)

        common_names = [feature_names[i] for i in np.where(common_strategies)[0]]
        missing_names = [feature_names[i] for i in np.where(missing_strategies)[0]]

        if common_names:
            print(f"Common strategies: {', '.join(common_names)}")

        # Strategy coverage statistics
        coverage = cluster_features.sum(axis=1).mean()
        print(f"Avg strategy coverage: {coverage:.1f}/{len(feature_names)} ({coverage/len(feature_names):.1%})")

        # Calculate stage-level coverage for this cluster
        step_coverage = {}
        for stage in stage_names:
            stage_cols = stage_features[stage]
            stage_cov = cluster_features[:, stage_cols].mean()
            step_coverage[f"Stage {stage}"] = round(stage_cov, 3)

        # Call LLM to interpret this cluster
        interpretation = interpret_cluster(
            cluster_id=cluster_id,
            members=members,
            supported_strategies=common_names,
            missing_strategies=missing_names,
            step_coverage=step_coverage,
        )

        print(f"Name: {interpretation['name']}")
        print(f"Interpretation: {interpretation['interpretation']}")

        cluster_interpretations.append({
            "cluster_id": int(cluster_id),
            "members": sorted(members),
            "size": len(members),
            "common_strategies": common_names,
            "missing_strategies": missing_names,
            "step_coverage": step_coverage,
            "avg_step_coverage": round(coverage / len(feature_names), 3),
            "cluster_name": interpretation["name"],
            "cluster_interpretation": interpretation["interpretation"],
        })

    # Build mapping from cluster_id to LLM name for visualization
    cluster_id_to_name = {c["cluster_id"]: c["cluster_name"] for c in cluster_interpretations}


# =============================================================================
# 7. SAVE OUTPUTS
# =============================================================================

# Save cluster interpretations to JSON
interpretations_output = {
    "linkage_method": "ward",
    "num_clusters": K_CLUSTERS,
    "silhouette_score": round(float(silhouette), 3),
    "clusters": cluster_interpretations,
}
with open(interpretations_file, 'w') as f:
    json.dump(interpretations_output, f, indent=2)
print(f"Saved {interpretations_file}")

# Save feature matrix to CSV
feature_csv_path = Path('../data/rq1_harness_feature_matrix.csv')
df_features.to_csv(feature_csv_path)
print(f"Saved {feature_csv_path}")