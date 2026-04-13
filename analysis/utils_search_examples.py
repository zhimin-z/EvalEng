import json

issues = []
with open("data/rq2_issues_annotated_full.jsonl") as f:
    for line in f:
        issues.append(json.loads(line))

related = [i for i in issues if i.get("is_related")]

# Check what stages Environment Incompatibility issues have
env_issues = [i for i in related if i.get("root_cause_label") == "Environment Incompatibility"]
print(f"Environment Incompatibility total: {len(env_issues)}")
from collections import Counter
print("Stage distribution:", Counter(i.get("stage") for i in env_issues))
print()

# Search Environment Incompatibility at any stage with keywords
keywords = ["install","version","cuda","pip","dependency","conflict","incompatible",
     "require","torch","numpy","python","gpu","package"]
matches = []
for i in env_issues:
    text = ((i.get("issue_title") or "") + " " + (i.get("issue_body") or "")).lower()
    score = sum(1 for k in keywords if k in text)
    if score > 0:
        matches.append((score, i))
matches.sort(key=lambda x: -x[0])

print(f"=== Environment Incompatibility (all stages): {len(matches)} matches ===")
for score, i in matches[:8]:
    print(f"  [{i['harness_name']}] {i['issue_title']}")
    print(f"    URL: {i['issue_url']}")
    print(f"    Stage: {i.get('stage')}, Step: {i.get('step')}")
    body = (i.get("issue_body") or "").replace("\r\n"," ").replace("\n"," ")[:300]
    print(f"    Body: {body}")
    print()
