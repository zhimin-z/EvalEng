#!/usr/bin/env python3
"""
Script to aggregate clusters from the original 6-cluster Ward hierarchical clustering
into 4 new clusters based on manual analysis.

New cluster mapping:
- Cluster 1: Task-Specific Offline Benchmarks (merged from old clusters 1, 3, 4)
- Cluster 2: Foundation Model Evaluation Suites (old cluster 6)
- Cluster 3: LLM-Centric API Evaluators (old cluster 5)
- Cluster 4: Interactive Agent Environments (old cluster 2)
"""

import json
import pandas as pd
from pathlib import Path
from collections import defaultdict


def get_stage_from_strategy(strategy: str) -> str:
    """Map strategy code to stage name."""
    if strategy.startswith("S0-"):
        return "Stage 0"
    elif strategy.startswith("SI-"):
        return "Stage I"
    elif strategy.startswith("SII-"):
        return "Stage II"
    elif strategy.startswith("SIII-"):
        return "Stage III"
    elif strategy.startswith("SIV-"):
        return "Stage IV"
    return "Unknown"


def calculate_cluster_metrics(members: list, feature_matrix: pd.DataFrame) -> dict:
    """
    Calculate cluster metrics from the feature matrix.

    Args:
        members: List of harness names in the cluster
        feature_matrix: DataFrame with harnesses as rows and strategies as columns

    Returns:
        Dictionary with common_strategies, missing_strategies, and stage_coverage
    """
    # Filter to only cluster members
    cluster_data = feature_matrix[feature_matrix.index.isin(members)]

    if cluster_data.empty:
        return {
            "common_strategies": [],
            "missing_strategies": [],
            "stage_coverage": {}
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
    stage_coverage = {}
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
                stage_coverage[stage] = round(sum(member_coverages) / len(member_coverages), 3)

    return {
        "common_strategies": sorted(common_strategies),
        "missing_strategies": sorted(missing_strategies),
        "stage_coverage": stage_coverage
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

    # Define new cluster mapping
    # New Cluster 1: Merge old clusters 1, 3, 4 -> Task-Specific Offline Benchmarks
    # New Cluster 2: Old cluster 6 -> Foundation Model Evaluation Suites
    # New Cluster 3: Old cluster 5 -> LLM-Centric API Evaluators
    # New Cluster 4: Old cluster 2 -> Interactive Agent Environments

    new_cluster_definitions = [
        {
            "new_cluster_id": 1,
            "old_cluster_ids": [1, 3, 4],
            "cluster_name": "",  # To be filled manually
            "cluster_interpretation": ""  # To be filled manually
        },
        {
            "new_cluster_id": 2,
            "old_cluster_ids": [6],
            "cluster_name": "",
            "cluster_interpretation": ""
        },
        {
            "new_cluster_id": 3,
            "old_cluster_ids": [5],
            "cluster_name": "",
            "cluster_interpretation": ""
        },
        {
            "new_cluster_id": 4,
            "old_cluster_ids": [2],
            "cluster_name": "",
            "cluster_interpretation": ""
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
        stage_coverages = list(metrics["stage_coverage"].values())
        avg_stage_coverage = round(sum(stage_coverages) / len(stage_coverages), 3) if stage_coverages else 0

        new_cluster = {
            "cluster_id": definition["new_cluster_id"],
            "members": members,
            "size": len(members),
            "common_strategies": metrics["common_strategies"],
            "missing_strategies": metrics["missing_strategies"],
            "stage_coverage": metrics["stage_coverage"],
            "avg_stage_coverage": avg_stage_coverage,
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
        print(f"  Avg coverage: {cluster['avg_stage_coverage']:.1%}")
        print(f"  Stage coverage:")
        for stage, cov in sorted(cluster['stage_coverage'].items()):
            print(f"    {stage}: {cov:.1%}")


if __name__ == "__main__":
    main()
