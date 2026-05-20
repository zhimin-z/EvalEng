import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
from collections import defaultdict

# Parse Stages.md and extract stages, steps, strategies, and harnesses
stages_file = Path(__file__).parent / '../data/rq1_workflow.md'
content = stages_file.read_text()

table_data = {}
all_harnesses = set()

# Find all stages (handles numeric 0 and roman numerals I, II, III, IV)
for stage_match in re.finditer(r'### \*\*Stage ([0-9IViv]+):', content):
    stage_num = stage_match.group(1)
    stage_start = stage_match.start()
    next_stage = re.search(r'### \*\*Stage', content[stage_match.end():])
    stage_end = stage_match.end() + next_stage.start() if next_stage else len(content)
    stage_content = content[stage_start:stage_end]
    
    # Find all steps in this stage
    for step_idx, step_match in enumerate(re.finditer(r'^\s{2}\* \*\*Step ([A-Z]):', stage_content, re.MULTILINE)):
        step_letter = step_match.group(1)
        step_start = step_match.start()
        next_step = list(re.finditer(r'^\s{2}\* \*\*Step', stage_content[step_match.end():], re.MULTILINE))
        step_end = step_match.end() + next_step[0].start() if next_step else len(stage_content)
        step_content = stage_content[step_start:step_end]
        step_key = f"Stage {stage_num}\nStep {step_letter}"

        # Find all strategies in this step
        for strat_idx, strategy_match in enumerate(re.finditer(r'^\s{6}\* \*\*Strategy (\d+):', step_content, re.MULTILINE)):
            strategy_num = int(strategy_match.group(1))
            strat_start = strategy_match.start()
            next_strat = list(re.finditer(r'^\s{6}\* \*\*Strategy', step_content[strategy_match.end():], re.MULTILINE))
            strat_end = strategy_match.end() + next_strat[0].start() if next_strat else len(step_content)
            strategy_text = step_content[strat_start:strat_end]
            
            # Extract harnesses from last parenthesis
            harness_matches = list(re.finditer(r'\(\*([^)]+)\*\)', strategy_text))
            if harness_matches:
                harnesses_str = harness_matches[-1].group(1)
                harnesses_list = ['all'] if harnesses_str.lower() == 'all' else [h.strip() for h in harnesses_str.split(',')]
                for h in harnesses_list:
                    if h.lower() != 'all':
                        all_harnesses.add(h)
                if step_key not in table_data:
                    table_data[step_key] = {}
                table_data[step_key][strategy_num] = harnesses_list

# Build the table
steps = sorted(table_data.keys())
harnesses = sorted(all_harnesses)
table = pd.DataFrame('', index=harnesses, columns=steps)

for step in steps:
    for strategy_num, harness_list in table_data[step].items():
        for harness in (harnesses if 'all' in harness_list else harness_list):
            if harness in harnesses:
                table.loc[harness, step] = str(strategy_num) if not table.loc[harness, step] else f"{table.loc[harness, step]}, {strategy_num}"

total_cells = len(harnesses) * len(steps)
filled_cells = (table != '').sum().sum()
empty_cells = total_cells - filled_cells
print(f"Heatmap Filled Rate: {100*filled_cells/total_cells:.1f}% ({filled_cells}/{total_cells} cells filled)")
print(f"Heatmap Empty Rate:  {100*empty_cells/total_cells:.1f}% ({empty_cells}/{total_cells} cells empty)\n")

# ========== HIERARCHICAL STATISTICS ==========
# Build hierarchical data structures: stage -> step -> strategy -> harnesses
stage_harnesses = defaultdict(set)
step_harnesses = defaultdict(set)
strategy_harnesses = defaultdict(set)

# Re-parse the content to build hierarchical structures
for stage_match in re.finditer(r'### \*\*Stage ([0-9IViv]+):', content):
    stage_num = stage_match.group(1)
    stage_start = stage_match.start()
    next_stage = re.search(r'### \*\*Stage', content[stage_match.end():])
    stage_end = stage_match.end() + next_stage.start() if next_stage else len(content)
    stage_content = content[stage_start:stage_end]

    for step_match in re.finditer(r'^\s{2}\* \*\*Step ([A-Z]):', stage_content, re.MULTILINE):
        step_letter = step_match.group(1)
        step_start = step_match.start()
        next_step = list(re.finditer(r'^\s{2}\* \*\*Step', stage_content[step_match.end():], re.MULTILINE))
        step_end = step_match.end() + next_step[0].start() if next_step else len(stage_content)
        step_content = stage_content[step_start:step_end]

        for strategy_match in re.finditer(r'^\s{6}\* \*\*Strategy (\d+):', step_content, re.MULTILINE):
            strategy_num = int(strategy_match.group(1))
            strat_start = strategy_match.start()
            next_strat = list(re.finditer(r'^\s{6}\* \*\*Strategy', step_content[strategy_match.end():], re.MULTILINE))
            strat_end = strategy_match.end() + next_strat[0].start() if next_strat else len(step_content)
            strategy_text = step_content[strat_start:strat_end]

            harness_matches = list(re.finditer(r'\(\*([^)]+)\*\)', strategy_text))
            if harness_matches:
                harnesses_str = harness_matches[-1].group(1)
                if harnesses_str.strip().lower() == 'all':
                    harnesses_list = list(all_harnesses)
                else:
                    harnesses_list = [h.strip() for h in harnesses_str.split(',')]

                for harness in harnesses_list:
                    strategy_harnesses[(stage_num, step_letter, strategy_num)].add(harness)
                    step_harnesses[(stage_num, step_letter)].add(harness)
                    stage_harnesses[stage_num].add(harness)

# Sort stages in proper order (0, I, II, III, IV)
stage_order = {'0': 0, 'I': 1, 'i': 1, 'II': 2, 'ii': 2, 'III': 3, 'iii': 3, 'IV': 4, 'iv': 4}
sorted_stages = sorted(stage_harnesses.keys(), key=lambda x: stage_order.get(x, 999))

# Build name lookup dictionaries from the parsed content
stage_names = {}
step_names = {}
strategy_names = {}

for stage_match in re.finditer(r'### \*\*Stage ([0-9IViv]+):\s*([^*\n]+)', content):
    stage_num = stage_match.group(1)
    stage_name = stage_match.group(2).strip().rstrip('*').strip()
    stage_names[stage_num] = stage_name

    stage_start = stage_match.start()
    next_stage = re.search(r'### \*\*Stage', content[stage_match.end():])
    stage_end = stage_match.end() + next_stage.start() if next_stage else len(content)
    stage_content = content[stage_start:stage_end]

    for step_match in re.finditer(r'^\s{2}\* \*\*Step ([A-Z]):\s*([^*\n]+)', stage_content, re.MULTILINE):
        step_letter = step_match.group(1)
        step_name = step_match.group(2).strip().rstrip('*').strip()
        step_names[(stage_num, step_letter)] = step_name

        step_start = step_match.start()
        next_step = list(re.finditer(r'^\s{2}\* \*\*Step', stage_content[step_match.end():], re.MULTILINE))
        step_end = step_match.end() + next_step[0].start() if next_step else len(stage_content)
        step_content = stage_content[step_start:step_end]

        for strategy_match in re.finditer(r'^\s{6}\* \*\*Strategy (\d+):\s*([^:*\n]+)', step_content, re.MULTILINE):
            strategy_num = int(strategy_match.group(1))
            strategy_name = strategy_match.group(2).strip().rstrip('*').strip()
            strategy_names[(stage_num, step_letter, strategy_num)] = strategy_name

total_harnesses = len(all_harnesses)

# Map stage numbers to display indices (0-based)
stage_index_map = {s: i for i, s in enumerate(sorted_stages)}

# Print hierarchical tree
print("=" * 80)
print("HIERARCHICAL STATISTICS: Stage → Step → Strategy Support")
print("=" * 80)
print()

for stage_num in sorted_stages:
    stage_count = len(stage_harnesses[stage_num])
    stage_index = stage_index_map[stage_num]
    stage_name = stage_names.get(stage_num, stage_num)
    stage_pct = round(100 * stage_count / total_harnesses, 1)
    print(f"Stage {stage_index} ({stage_name}): {stage_count} ({stage_pct}%)")

    # Get all steps for this stage
    stage_steps = sorted([
        (step_letter, step_harnesses[(s, step_letter)])
        for s, step_letter in step_harnesses.keys()
        if s == stage_num
    ])

    for step_idx, (step_letter, step_harness_set) in enumerate(stage_steps):
        step_count = len(step_harness_set)
        step_name = step_names.get((stage_num, step_letter), step_letter)
        step_pct = round(100 * step_count / total_harnesses, 1)
        is_last_step = (step_idx == len(stage_steps) - 1)
        step_prefix = "  └─" if is_last_step else "  ├─"
        print(f"{step_prefix} Step {step_idx} ({step_name}): {step_count} ({step_pct}%)")

        # Get all strategies for this step
        step_strategies = sorted([
            (strategy_num, strategy_harnesses[(s, sl, strategy_num)])
            for s, sl, strategy_num in strategy_harnesses.keys()
            if s == stage_num and sl == step_letter
        ])

        for strat_idx, (strategy_num, strategy_harness_set) in enumerate(step_strategies):
            strategy_count = len(strategy_harness_set)
            strategy_name = strategy_names.get((stage_num, step_letter, strategy_num), str(strategy_num))
            strategy_pct = round(100 * strategy_count / total_harnesses, 1)
            is_last_strategy = (strat_idx == len(step_strategies) - 1)
            if is_last_step:
                strat_prefix = "     └─" if is_last_strategy else "     ├─"
            else:
                strat_prefix = "  │  └─" if is_last_strategy else "  │  ├─"
            print(f"{strat_prefix} Strategy {strat_idx} ({strategy_name}): {strategy_count} ({strategy_pct}%)")

    print()

# Print summary statistics
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total unique harnesses: {len(all_harnesses)}")
print(f"Total stages: {len(stage_harnesses)}")
print(f"Total steps: {len(step_harnesses)}")
print(f"Total strategies: {len(strategy_harnesses)}")
print()
print(f"Average harnesses per stage: {sum(len(h) for h in stage_harnesses.values()) / len(stage_harnesses):.1f}")
print(f"Average harnesses per step: {sum(len(h) for h in step_harnesses.values()) / len(step_harnesses):.1f}")
print(f"Average harnesses per strategy: {sum(len(h) for h in strategy_harnesses.values()) / len(strategy_harnesses):.1f}")
print()

# Create a numeric matrix for heatmap: count of strategies per cell
heatmap_data = np.zeros_like(table.values, dtype=float)
text_labels = []

for i, harness in enumerate(table.index):
    row_labels = []
    for j, step in enumerate(table.columns):
        cell_value = table.iloc[i, j]
        if pd.notna(cell_value) and str(cell_value).strip():
            strategy_count = len(str(cell_value).split(','))
            heatmap_data[i, j] = strategy_count
            row_labels.append(str(cell_value))
        else:
            heatmap_data[i, j] = 0
            row_labels.append('')
    text_labels.append(row_labels)

# Create custom colormap: white for 0, gradient for 1-6
colors = ['white', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695', '#08306b']
n_bins = 7
cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

# Create matplotlib heatmap
fig, ax = plt.subplots(figsize=(14, 10))
im = ax.imshow(heatmap_data, cmap=cmap, aspect='auto', vmin=0, vmax=6)

# Set ticks and labels
ax.set_xticks(np.arange(len(table.columns)))
ax.set_yticks(np.arange(len(table.index)))
ax.set_xticklabels(table.columns, ha='center', fontsize=11)
ax.set_yticklabels(table.index, fontsize=11)

# Add text annotations with adaptive color (white text on dark backgrounds)
for i in range(len(table.index)):
    for j in range(len(table.columns)):
        if text_labels[i][j]:
            # Use white text for darker colors (strategy count >= 3), black for lighter colors
            text_color = "white" if heatmap_data[i, j] >= 3 else "black"
            text = ax.text(j, i, text_labels[i][j],
                         ha="center", va="center", color=text_color, fontsize=10)

# Add colorbar with reduced gap
cbar = plt.colorbar(im, ax=ax, ticks=[0, 1, 2, 3, 4, 5, 6], pad=0.01)
cbar.set_label('Strategy Count', rotation=270, labelpad=15, fontsize=11)

# Labels and title
ax.set_xlabel('')
ax.set_ylabel('')

# Grid
ax.set_xticks(np.arange(len(table.columns)) - 0.5, minor=True)
ax.set_yticks(np.arange(len(table.index)) - 0.5, minor=True)
ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)

plt.tight_layout()

# Save as PDF
pdf_path = Path(__file__).parent / '../figures/rq1_heatmap.pdf'
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
print(f"\n✓ Heatmap saved to: {pdf_path}")