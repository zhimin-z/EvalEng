#!/usr/bin/env python3
"""
Script to aggregate clusters from the original 6-cluster Ward hierarchical clustering
into 4 new clusters based on manual analysis of feature-matrix Hamming distances.

New cluster mapping (harness-level, not old-cluster-level):
- Cluster 1: Narrow-Domain Metric Libraries
    DomainBed, HumanEval, JiWER, Melting Pot, Meta-World, OGB, Overcooked-AI,
    Quantus, RLBench, SimplerEnv, mir_eval, ranx
- Cluster 2: Task-Specific Capability Probes
    Ann-benchmarks, BEIR, BigCode Eval, CipherChat, EvalAI, EvalPlus, GuideLLM,
    LLMPerf, Ollama Grid Search, PyKEEN, STT Benchmark, TorchBench
- Cluster 3: Full-Stack LLM Evaluation Platforms
    DeepEval, EvalScope, Evals, Harbor, Inspect AI, IntellAgent, Promptfoo,
    Ragas, Rogue, TruLens
- Cluster 4: Standardized LLM Benchmark Suites
    ARES, AlpacaEval, AutoRAG, C-Eval, COMET, Evalchemy, Evaluate, Evidently,
    GAOKAO-Bench, Giskard, HELM, LM Eval, LightEval, MLPerf, OpenCompass,
    Prometheus-Eval, PromptBench, RewardBench, TFMA, TrustLLM, VBench,
    VLMEvalKit, lmms-eval
"""

import json
import pandas as pd
from pathlib import Path
from collections import defaultdict


def get_stage_from_strategy(strategy: str) -> str:
    """Map strategy code to stage name."""
    if strategy.startswith("S0-"):
        return "Stage 0"
    elif strategy.startswith("S1-"):
        return "Stage 1"
    elif strategy.startswith("S2-"):
        return "Stage 2"
    elif strategy.startswith("S3-"):
        return "Stage 3"
    elif strategy.startswith("S4-"):
        return "Stage 4"
    return "Unknown"


def calculate_cluster_metrics(members: list, feature_matrix: pd.DataFrame) -> dict:
    """
    Calculate cluster metrics from the feature matrix.

    Args:
        members: List of harness names in the cluster
        feature_matrix: DataFrame with harnesses as rows and strategies as columns

    Returns:
        Dictionary with common_strategies, missing_strategies, and step_coverage
    """
    # Filter to only cluster members
    cluster_data = feature_matrix[feature_matrix.index.isin(members)]

    if cluster_data.empty:
        return {
            "common_strategies": [],
            "missing_strategies": [],
            "step_coverage": {}
        }

    strategies = [col for col in feature_matrix.columns if col != ""]

    # Common strategies: ALL members have this strategy (all values = 1)
    common_strategies = []
    for strategy in strategies:
        if cluster_data[strategy].all():  # All values are 1 (truthy)
            common_strategies.append(strategy)

    # Missing strategies: NO members have this strategy (all values = 0)
    missing_strategies = []
    for strategy in strategies:
        if (cluster_data[strategy] == 0).all():  # All values are 0
            missing_strategies.append(strategy)

    # Calculate stage coverage
    # Group strategies by stage
    stage_strategies = defaultdict(list)
    for strategy in strategies:
        stage = get_stage_from_strategy(strategy)
        if stage != "Unknown":
            stage_strategies[stage].append(strategy)

    # Calculate average coverage per stage across all members
    step_coverage = {}
    for stage, stage_strats in stage_strategies.items():
        if stage_strats:
            # For each member, calculate what fraction of stage strategies they have
            # Then average across all members
            member_coverages = []
            for member in members:
                if member in cluster_data.index:
                    member_data = cluster_data.loc[member, stage_strats]
                    coverage = member_data.sum() / len(stage_strats)
                    member_coverages.append(coverage)

            if member_coverages:
                step_coverage[stage] = round(sum(member_coverages) / len(member_coverages), 3)

    return {
        "common_strategies": sorted(common_strategies),
        "missing_strategies": sorted(missing_strategies),
        "step_coverage": step_coverage
    }


def main():
    # Paths
    data_dir = Path(__file__).parent.parent / "data"
    feature_matrix_file = data_dir / "rq1_harness_feature_matrix.csv"
    output_file = data_dir / "rq1_cluster_curated.json"

    # Load feature matrix
    feature_matrix = pd.read_csv(feature_matrix_file, index_col=0)

    new_cluster_definitions = [
        {
            "new_cluster_id": 1,
            "members": [
                "DomainBed", "HumanEval", "JiWER", "Melting Pot", "Meta-World",
                "OGB", "Overcooked-AI", "Quantus", "RLBench", "SimplerEnv",
                "mir_eval", "ranx",
            ],
            "cluster_name": "Narrow-Domain Metric Libraries",
            "cluster_interpretation": "Pure pip-installable libraries that compute one well-defined metric over structured inputs—word error rate, ranking quality, graph link prediction, robotics task success, or attribution fidelity—without invoking any remote model API, LLM judge, or production plumbing. Agent-environment harnesses (RLBench, Meta-World, Overcooked-AI, SimplerEnv, Melting Pot) belong here because they are fundamentally scoring libraries that use simulation environments rather than evaluation platforms: their feature profile is as sparse as JiWER or ranx. The defining characteristic is the combination of a narrow, algorithmic metric and a complete absence of external service dependencies.",
        },
        {
            "new_cluster_id": 2,
            "members": [
                "Ann-benchmarks", "BEIR", "BigCode Eval", "CipherChat", "EvalAI",
                "EvalPlus", "GuideLLM", "LLMPerf", "Ollama Grid Search", "PyKEEN",
                "STT Benchmark", "TorchBench",
            ],
            "cluster_name": "Task-Specific Capability Probes",
            "cluster_interpretation": "Purpose-built harnesses that answer 'how well does system X do task Y?' on one narrow axis—retrieval precision (BEIR), code execution correctness (EvalPlus, BigCode Eval), ANN throughput (Ann-benchmarks), speech WER (STT Benchmark), inference latency (LLMPerf, TorchBench, GuideLLM), adversarial safety (CipherChat), graph embedding (PyKEEN), or cross-system leaderboard comparison (EvalAI). They always invoke a remote model endpoint and produce a scalar leaderboard score, but lack judge-based scoring, persistent dashboards, and production monitoring. Distinct from Cluster 1 in that they run a model; distinct from Cluster 4 in that they target a single capability rather than sweeping across many benchmarks.",
        },
        {
            "new_cluster_id": 3,
            "members": [
                "DeepEval", "EvalScope", "Evals", "Harbor", "Inspect AI",
                "IntellAgent", "Promptfoo", "Ragas", "Rogue", "TruLens",
            ],
            "cluster_name": "Full-Stack LLM Evaluation Platforms",
            "cluster_interpretation": "End-to-end LLM evaluation operating systems that support all execution modes simultaneously: batch regression, live arena head-to-head (ArenaBattle), production traffic monitoring (ProdStreaming), agentic loop tracing (InteractiveLoop), and automated regression alerting. With 13 features universally ON and no universally missing strategies, these are the most feature-complete harnesses in the corpus. They are deployed as persistent infrastructure rather than run episodically per paper, and they evaluate anything about an LLM in any mode rather than targeting a single benchmark or capability axis.",
        },
        {
            "new_cluster_id": 4,
            "members": [
                "ARES", "AlpacaEval", "AutoRAG", "C-Eval", "COMET", "Evalchemy",
                "Evaluate", "Evidently", "GAOKAO-Bench", "Giskard", "HELM",
                "LM Eval", "LightEval", "MLPerf", "OpenCompass", "Prometheus-Eval",
                "PromptBench", "RewardBench", "TFMA", "TrustLLM", "VBench",
                "VLMEvalKit", "lmms-eval",
            ],
            "cluster_name": "Standardized LLM Benchmark Suites",
            "cluster_interpretation": "Academic and industry benchmark runners that sweep a model across fixed, published task collections—safety probes, multimodal tasks, translation quality, reward modeling, RAG corpora—and produce normalized leaderboard scores via batch inference and latent/subjective metrics. They share remote inference, distributional statistics, and uncertainty quantification, but universally lack binary distribution, deterministic pass/fail metrics, and bespoke chart generation pipelines. Run episodically for model release comparisons rather than as persistent production monitoring infrastructure, distinguishing them from Cluster 3.",
        },
    ]

    # Build new clusters
    new_clusters = []

    for definition in new_cluster_definitions:
        members = sorted(definition["members"])

        # Calculate metrics from feature matrix
        metrics = calculate_cluster_metrics(members, feature_matrix)

        # Calculate average coverage across all stages
        step_coverages = list(metrics["step_coverage"].values())
        avg_step_coverage = round(sum(step_coverages) / len(step_coverages), 3) if step_coverages else 0

        new_cluster = {
            "cluster_id": definition["new_cluster_id"],
            "members": members,
            "size": len(members),
            "common_strategies": metrics["common_strategies"],
            "missing_strategies": metrics["missing_strategies"],
            "step_coverage": metrics["step_coverage"],
            "avg_step_coverage": avg_step_coverage,
            "cluster_name": definition["cluster_name"],
            "cluster_interpretation": definition["cluster_interpretation"]
        }

        new_clusters.append(new_cluster)

    output_data = {
        "description": "Curated clusters re-derived from harness-level Hamming distance analysis of the 6-cluster Ward hierarchical clustering into 4 semantically coherent groups",
        "original_linkage_method": "ward",
        "original_num_clusters": 6,
        "curated_num_clusters": 4,
        "cluster_mapping": {
            "1 (Narrow-Domain Metric Libraries)": "Parts of old clusters 2, 3, 4",
            "2 (Task-Specific Capability Probes)": "Parts of old clusters 1, 3, 4",
            "3 (Full-Stack LLM Evaluation Platforms)": "Old cluster 5",
            "4 (Standardized LLM Benchmark Suites)": "Old cluster 6 + parts of old clusters 1, 5"
        },
        "clusters": new_clusters
    }

    # Write output
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"Curated clusters written to: {output_file}")

    # Print summary
    print("\n" + "=" * 60)
    print("CLUSTER AGGREGATION SUMMARY")
    print("=" * 60)

    for cluster in new_clusters:
        print(f"\n{cluster['cluster_name']}:")
        print(f"  Size: {cluster['size']} harnesses")
        print(f"  Members: {', '.join(cluster['members'][:5])}{'...' if len(cluster['members']) > 5 else ''}")
        print(f"  Common strategies: {len(cluster['common_strategies'])}")
        print(f"  Missing strategies: {len(cluster['missing_strategies'])}")
        print(f"  Avg coverage: {cluster['avg_step_coverage']:.1%}")
        print(f"  Stage coverage:")
        for stage, cov in sorted(cluster['step_coverage'].items()):
            print(f"    {stage}: {cov:.1%}")


if __name__ == "__main__":
    main()
