import pandas as pd
from sklearn.metrics import cohen_kappa_score

df_zhimin = pd.read_json(r"../data/rq3_issues_sample_annotated_zhimin.jsonl", lines=True)
df_zhimin.fillna({'stage': 'N/A', 'step': 'N/A', 'strategy': 'N/A'}, inplace=True)
df_zhimin['workflow_label'] = df_zhimin['stage'].astype(str) + " - " + df_zhimin['step'].astype(str) + " - " + df_zhimin['strategy'].astype(str)

# Load and filter data
df_zehao = pd.read_json("../data/rq3_issues_sample_annotated_zehao.jsonl", lines=True)
df_zehao.fillna({'stage': 'N/A', 'step': 'N/A', 'strategy': 'N/A'}, inplace=True)
df_zehao['workflow_label'] = df_zehao['stage'].astype(str) + " - " + df_zehao['step'].astype(str) + " - " + df_zehao['strategy'].astype(str)

# Find disagreements
disagreements = df_zhimin[df_zhimin['workflow_label'] != df_zehao['workflow_label']]
print(f"Disagreements to adjudicate: {len(disagreements)}/{len(df_zhimin)}")

# Calculate Cohen's kappa score to measure agreement between original and verified labels
kappa = cohen_kappa_score(df_zehao['workflow_label'], df_zhimin['workflow_label'])
print(f"Cohen's Kappa between original and verified labels: {kappa}")