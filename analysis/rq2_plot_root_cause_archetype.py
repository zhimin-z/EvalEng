import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

# ── Load cluster mapping (harness_name -> cluster_name) ──────────────────────
cluster_file = Path(__file__).parent.parent / "data" / "rq1_cluster_curated.json"
with open(cluster_file, "r") as f:
    cluster_data = json.load(f)

harness_to_cluster = {}
cluster_id_to_name = {}
for cluster in cluster_data["clusters"]:
    cid = cluster["cluster_id"]
    cname = cluster["cluster_name"]
    cluster_id_to_name[cid] = cname
    for member in cluster["members"]:
        harness_to_cluster[member.lower()] = (cid, cname)

# ── Load annotated issues ────────────────────────────────────────────────────
issues_file = Path(__file__).parent.parent / "data" / "rq2_issues_annotated_full.jsonl"
df = pd.read_json(issues_file, lines=True)

# Filter to issues with root_cause_label
df = df[df['root_cause_label'].notna()].copy()
df['root_cause_label'] = df['root_cause_label'].astype(str)

# Map harness to cluster
df['harness_lower'] = df['harness_name'].str.lower()
df['cluster_id'] = df['harness_lower'].map(lambda h: harness_to_cluster.get(h, (None, None))[0])
df['cluster_name'] = df['harness_lower'].map(lambda h: harness_to_cluster.get(h, (None, None))[1])

# Report unmapped harnesses
unmapped = df[df['cluster_id'].isna()]['harness_name'].unique()
if len(unmapped) > 0:
    print(f"WARNING: {len(unmapped)} harness(es) not mapped to any cluster: {list(unmapped)}")

# Drop rows without a cluster mapping
df = df[df['cluster_id'].notna()].copy()

# ── Sort root causes alphabetically, "Others" last ──────────────────────────
root_cause_totals = df['root_cause_label'].value_counts().to_dict()
sorted_root_causes = sorted(
    [rc for rc in root_cause_totals.keys() if rc.lower() != 'others'],
    key=lambda x: x.lower()
)

# Sort clusters by cluster_id
sorted_cluster_ids = sorted(cluster_id_to_name.keys())
sorted_cluster_names = [cluster_id_to_name[cid] for cid in sorted_cluster_ids]

total_issues = len(df)

# ── Build heatmap matrix: rows = clusters, columns = root causes ─────────────
num_rc = len(sorted_root_causes)
num_cl = len(sorted_cluster_names)
heatmap_data = np.zeros((num_cl, num_rc), dtype=int)

for cl_idx, cid in enumerate(sorted_cluster_ids):
    for rc_idx, rc in enumerate(sorted_root_causes):
        count = len(df[(df['root_cause_label'] == rc) & (df['cluster_id'] == cid)])
        heatmap_data[cl_idx, rc_idx] = count

# ── Create the heatmap ───────────────────────────────────────────────────────
fig_width = max(12, num_rc * 2.2)
fig_height = max(4, num_cl * 1.4)
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

im = ax.imshow(heatmap_data, cmap='Blues', aspect='auto')

# Add colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Number of Issues', fontsize=14, fontweight='bold')
cbar.ax.tick_params(labelsize=13)

# Annotate each cell with count and percentage (count / column total = per root cause)
col_totals = heatmap_data.sum(axis=0)  # sum over clusters for each root cause column
for i in range(num_cl):
    for j in range(num_rc):
        val = heatmap_data[i, j]
        ratio = val / col_totals[j] * 100 if col_totals[j] > 0 else 0
        label = f"{val}\n({ratio:.1f}%)"
        text_color = 'white' if val > heatmap_data.max() * 0.6 else 'black'
        ax.text(j, i, label, ha='center', va='center',
                fontsize=13, fontweight='bold', color=text_color)

# Split label into lines based on full accumulated line width
def smart_split_label(label, max_line_width=20):
    words = label.split(' ')
    if len(words) <= 1:
        return label
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if len(current_line) + 1 + len(word) <= max_line_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return '\n'.join(lines)

cluster_labels = [smart_split_label(name) for name in sorted_cluster_names]

# Set tick labels: x = root causes, y = clusters
ax.set_xticks(np.arange(num_rc))
rc_labels = [smart_split_label(rc) for rc in sorted_root_causes]
ax.set_xticklabels(rc_labels, ha='center', fontsize=13, fontweight='bold')
ax.set_yticks(np.arange(num_cl))
ax.set_yticklabels(cluster_labels, fontsize=13, fontweight='bold')

# Move x-axis labels to top
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')
ax.tick_params(axis='x', pad=4)

# Add grid lines to separate cells
for i in range(num_cl + 1):
    ax.axhline(y=i - 0.5, color='white', linewidth=1.5)
for j in range(num_rc + 1):
    ax.axvline(x=j - 0.5, color='white', linewidth=1.5)

plt.tight_layout()

# Save figure
output_path = Path(__file__).parent.parent / "figures" / "rq2_root_cause_archetype.pdf"
plt.savefig(output_path, format='pdf', bbox_inches='tight')

# ── LaTeX tables: Root Cause x Cluster ──────────────────────────────────────

row_totals = heatmap_data.sum(axis=1)  # total issues per archetype (cluster)
col_spec = "l" + "r" * num_rc
header_cells = ["Archetype"] + sorted_root_causes

# Table 1: row-normalized (proportion of each root cause within its archetype)
latex_lines = []
latex_lines.append("\\begin{table}[!t]")
latex_lines.append("\\centering")
latex_lines.append("\\caption{Root cause distribution across different harness archetypes. "
                    "The percentage indicates the relative proportion of each root cause within the corresponding archetype.}")
latex_lines.append("\\label{tab:root_cause_archetype}")
latex_lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
latex_lines.append("\\toprule")
latex_lines.append(" & ".join(header_cells) + " \\\\")
latex_lines.append("\\midrule")

for cl_idx, cid in enumerate(sorted_cluster_ids):
    cells = [sorted_cluster_names[cl_idx]]
    for rc_idx, rc in enumerate(sorted_root_causes):
        count = heatmap_data[cl_idx, rc_idx]
        row_total = row_totals[cl_idx]
        if count > 0 and row_total > 0:
            pct = count / row_total * 100
            cells.append(f"{pct:.1f}\\%")
        else:
            cells.append("")
    latex_lines.append(" & ".join(cells) + " \\\\")

latex_lines.append("\\bottomrule")
latex_lines.append("\\end{tabular}")
latex_lines.append("\\end{table}")

print()
print('\n'.join(latex_lines))
print()

# Table 2: column-normalized (proportion of each archetype within its root cause)
latex_col_lines = []
latex_col_lines.append("\\begin{table}[!t]")
latex_col_lines.append("\\centering")
latex_col_lines.append("\\caption{Root cause distribution across different harness archetypes. "
                        "The percentage indicates the relative proportion of each archetype within the corresponding root cause.}")
latex_col_lines.append("\\label{tab:root_cause_archetype_col}")
latex_col_lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
latex_col_lines.append("\\toprule")
latex_col_lines.append(" & ".join(header_cells) + " \\\\")
latex_col_lines.append("\\midrule")

for cl_idx, cid in enumerate(sorted_cluster_ids):
    cells = [sorted_cluster_names[cl_idx]]
    for rc_idx, rc in enumerate(sorted_root_causes):
        count = heatmap_data[cl_idx, rc_idx]
        col_total = col_totals[rc_idx]
        if count > 0 and col_total > 0:
            pct = count / col_total * 100
            cells.append(f"{pct:.1f}\\%")
        else:
            cells.append("")
    latex_col_lines.append(" & ".join(cells) + " \\\\")

latex_col_lines.append("\\bottomrule")
latex_col_lines.append("\\end{tabular}")
latex_col_lines.append("\\end{table}")

print()
print('\n'.join(latex_col_lines))
print()

plt.close()
