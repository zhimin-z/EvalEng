import pandas as pd
import ast

from collections import Counter

# Read the GitHub issues CSV
df = pd.read_json("data/rq2_issues.jsonl", lines=True)

print(f"Total issues: {len(df)}")
print(f"Total repos: {len(df['github_repo'].unique())}")
print(f"Total harnesses: {len(df['harness_name'].unique())}")

# Count issues with labels
issues_with_labels = df[df['issue_labels'].apply(len) > 0]
issues_without_labels = df[df['issue_labels'].apply(len) == 0]

print(f"\n📊 LABEL COVERAGE:")
print(f"  Issues with labels:    {len(issues_with_labels):,} ({len(issues_with_labels)/len(df)*100:.1f}%)")
print(f"  Issues without labels: {len(issues_without_labels):,} ({len(issues_without_labels)/len(df)*100:.1f}%)")

# Collect all labels and count them
all_labels = []
for labels_list in df['issue_labels']:
    all_labels.extend(labels_list)

label_counts = Counter(all_labels)

print(f"\n📈 LABEL STATISTICS:")
print(f"  Total unique labels: {len(label_counts)}")
print(f"  Total label instances: {len(all_labels):,}")
print(f"  Average labels per issue (all): {len(all_labels)/len(df):.2f}")
if len(issues_with_labels) > 0:
    print(f"  Average labels per labeled issue: {len(all_labels)/len(issues_with_labels):.2f}")

# Show top 10 most common labels
print(f"\n🏷️  TOP 10 MOST COMMON LABELS:")
print("-" * 80)
for i, (label, count) in enumerate(label_counts.most_common(10), 1):
    percentage = count / len(df) * 100
    print(f"{i:2d}. {label:40s} {count:6,} issues ({percentage:5.2f}%)")

# Show distribution by label count
labels_per_issue = df['issue_labels'].apply(len)
label_count_dist = labels_per_issue.value_counts().sort_index()

print(f"\n📊 DISTRIBUTION BY NUMBER OF LABELS PER ISSUE:")
print("-" * 80)
for num_labels, count in label_count_dist.items():
    percentage = count / len(df) * 100
    bar = '█' * int(percentage / 2)
    print(f"{num_labels:2d} labels: {count:6,} issues ({percentage:5.2f}%) {bar}")

# Show some repository-level statistics
print(f"\n🗂️  LABEL USAGE BY REPOSITORY (Top 10):")
print("-" * 80)
repo_label_stats = df.groupby('github_repo').agg({
    'issue_labels': lambda x: sum(len(labels) for labels in x),
    'issue_title': 'count'
}).rename(columns={'issue_labels': 'total_labels', 'issue_title': 'total_issues'})
repo_label_stats['avg_labels'] = repo_label_stats['total_labels'] / repo_label_stats['total_issues']
repo_label_stats['pct_labeled'] = df.groupby('github_repo')['issue_labels'].apply(lambda x: (x.apply(len) > 0).sum() / len(x) * 100)
repo_label_stats = repo_label_stats.sort_values('total_labels', ascending=False).head(10)

for repo, row in repo_label_stats.iterrows():
    print(f"{repo:50s} {row['total_issues']:4.0f} issues, {row['total_labels']:4.0f} labels, {row['pct_labeled']:.1f}% labeled")