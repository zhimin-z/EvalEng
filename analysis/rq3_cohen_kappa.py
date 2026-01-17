import pandas as pd
from sklearn.metrics import cohen_kappa_score

df_zhimin = pd.read_json(r"../data/rq3_issues_annotated_sample_zhimin.jsonl", lines=True)
df_zhimin = df_zhimin[df_zhimin['root_cause_label'].notna()]

# Load and filter data
df_zehao = pd.read_json("../data/rq3_issues_annotated_sample_zehao.jsonl", lines=True)
df_zehao = df_zehao[df_zehao['root_cause_label'].notna()]

# Find disagreements
disagreements = df_zhimin[df_zhimin['root_cause_label'] != df_zehao['root_cause_label']]
print(f"Disagreements to adjudicate: {len(disagreements)}/{len(df_zhimin)}")

# Calculate Cohen's kappa score to measure agreement between original and verified labels
kappa = cohen_kappa_score(df_zehao['root_cause_label'], df_zhimin['root_cause_label'])
print(f"Cohen's Kappa between original and verified labels: {kappa}")