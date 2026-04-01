#!/usr/bin/env python3
"""
Script to aggregate clusters from the original 6-cluster Ward hierarchical clustering
into 4 new clusters based on manual analysis.

New cluster mapping:
- Cluster 1: Standardized Model Benchmark Suites (old cluster 6)
- Cluster 2: Domain-specific Offline Evaluators (merged from old clusters 1, 3, 4)
- Cluster 3: LLM Application Evaluation Platforms (old cluster 5)
- Cluster 4: Interactive Agent Simulators (old cluster 2)
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
    old_cluster_file = data_dir / "rq1_cluster_ward.json"
    feature_matrix_file = data_dir / "rq1_harness_feature_matrix.csv"
    output_file = data_dir / "rq1_cluster_curated.json"

    # Load original cluster data to get member lists
    with open(old_cluster_file, "r") as f:
        old_data = json.load(f)

    # Build mapping from old cluster_id to members
    old_clusters = {c["cluster_id"]: c["members"] for c in old_data["clusters"]}

    # Load feature matrix
    feature_matrix = pd.read_csv(feature_matrix_file, index_col=0)

    new_cluster_definitions = [
        {
            "new_cluster_id": 1,
            "old_cluster_ids": [6],
            "cluster_name": "Standardized Model Benchmark Suites",
            "cluster_interpretation": "Comprehensive frameworks for assessing foundation model capabilities, safety, and multimodal understanding through curated benchmark datasets and leaderboard-oriented evaluation. They excel at scoring and metric aggregation across standardized test sets but lack interactive agent support, simulation environments, and production monitoring—serving as the primary toolkit for systematic model comparison and research benchmarking."
        },
        {
            "new_cluster_id": 2,
            "old_cluster_ids": [1, 3, 4],
            "cluster_name": "Domain-specific Offline Evaluators",
            "cluster_interpretation": "Specialized tools for measuring narrow capabilities—code generation, information retrieval, speech recognition, knowledge graphs, XAI, and system performance—on local hardware against predefined datasets using deterministic metrics. They require minimal infrastructure and lack LLM-as-judge, remote API, and interactive agent support, prioritizing reproducible, lightweight benchmarking of specific ML tasks."
        },
        {
            "new_cluster_id": 3,
            "old_cluster_ids": [5],
            "cluster_name": "LLM Application Evaluation Platforms",
            "cluster_interpretation": "Full-stack platforms for testing LLM-powered applications—RAG pipelines, chatbots, tool-using agents—through flexible evaluation workflows combining LLM-as-judge scoring, remote API integration, CI/CD hooks, and interactive dashboards. With the highest workflow coverage and no universally missing strategies, they support the broadest range of evaluation patterns from development through production monitoring."
        },
        {
            "new_cluster_id": 4,
            "old_cluster_ids": [2],
            "cluster_name": "Interactive Agent Simulators",
            "cluster_interpretation": "Harnesses for evaluating sequential decision-making systems—RL policies, robotic manipulators, multi-agent teams—through stateful simulation environments with deterministic reward metrics. They prioritize agent-environment interaction loops over language model evaluation, lacking remote API support, LLM judges, and rich reporting infrastructure."
        }
    ]

    # Build new clusters
    new_clusters = []

    for definition in new_cluster_definitions:
        # Aggregate members from old clusters
        members = []
        for old_id in definition["old_cluster_ids"]:
            members.extend(old_clusters[old_id])
        members = sorted(members)

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

    # Calculate overall silhouette score note
    output_data = {
        "description": "Curated clusters from 6-cluster Ward hierarchical clustering into 4 semantic groups",
        "original_linkage_method": "ward",
        "original_num_clusters": 6,
        "curated_num_clusters": 4,
        "cluster_mapping": {
            "1": "Merged from original clusters 1, 3, 4",
            "2": "Original cluster 6",
            "3": "Original cluster 5",
            "4": "Original cluster 2"
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
        print(f"\nCluster {cluster['cluster_id']}:")
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
