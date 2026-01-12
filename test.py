import pandas as pd

df = pd.read_json("data/rq2_issues_annotated.jsonl", lines=True)
df_sample_new = df[df['root_cause_label'].notna()]
print(len(df_sample_new))
df_sample_new.to_json("data/rq3_issue_sample_annotated.jsonl", orient="records", lines=True, force_ascii=False)