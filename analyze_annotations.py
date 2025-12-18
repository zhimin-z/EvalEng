#!/usr/bin/env python3
"""
Analyze GitHub issues labels from CSV file.
"""

import csv
import ast
from collections import Counter
from typing import List, Dict

def parse_label_string(label_str: str) -> List[str]:
    """Parse string representation of Python list into actual list."""
    try:
        # Handle empty string or whitespace
        if not label_str or label_str.strip() == '':
            return []
        # Use ast.literal_eval to safely parse the string representation
        parsed = ast.literal_eval(label_str)
        return parsed if isinstance(parsed, list) else []
    except (ValueError, SyntaxError):
        return []

def analyze_issue_labels(csv_file: str):
    """Analyze issue labels from GitHub issues CSV."""

    total_issues = 0
    issues_with_labels = 0
    issues_without_labels = 0
    all_labels = []
    label_count_distribution = Counter()

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_issues += 1
            labels = parse_label_string(row['issue_labels'])
            num_labels = len(labels)

            if num_labels > 0:
                issues_with_labels += 1
                all_labels.extend(labels)
            else:
                issues_without_labels += 1

            label_count_distribution[num_labels] += 1

    # Count individual labels
    label_counter = Counter(all_labels)
    top_30_labels = label_counter.most_common(30)

    # Print results
    print("=" * 80)
    print("GITHUB ISSUES LABEL ANALYSIS")
    print("=" * 80)

    print(f"\n1. TOTAL ISSUES: {total_issues:,}")

    print(f"\n2. LABEL STATUS:")
    print(f"   - Issues with labels: {issues_with_labels:,} ({issues_with_labels/total_issues*100:.2f}%)")
    print(f"   - Issues without labels: {issues_without_labels:,} ({issues_without_labels/total_issues*100:.2f}%)")

    print(f"\n3. TOP 30 MOST COMMON LABELS:")
    print(f"   {'Rank':<6} {'Label':<40} {'Count':<10}")
    print("   " + "-" * 56)
    for rank, (label, count) in enumerate(top_30_labels, 1):
        print(f"   {rank:<6} {label:<40} {count:<10,}")

    print(f"\n4. DISTRIBUTION OF NUMBER OF LABELS PER ISSUE:")
    print(f"   {'# Labels':<12} {'# Issues':<12} {'Percentage'}")
    print("   " + "-" * 40)

    # Sort by number of labels
    sorted_distribution = sorted(label_count_distribution.items())
    for num_labels, count in sorted_distribution:
        percentage = count / total_issues * 100
        print(f"   {num_labels:<12} {count:<12,} {percentage:>6.2f}%")

    print("\n" + "=" * 80)
    print(f"Total unique labels: {len(label_counter):,}")
    print(f"Total label occurrences: {sum(label_counter.values()):,}")
    print(f"Average labels per issue: {sum(label_counter.values())/total_issues:.2f}")
    print("=" * 80)

if __name__ == "__main__":
    csv_file = "/home/local/SAIL/zhimin/Evalware-Survey/data/github_issues.csv"
    analyze_issue_labels(csv_file)
