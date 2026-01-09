import re
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# Parse Stages.md and extract stages, steps, strategies, and harnesses
stages_file = Path('../data/rq1_workflow.md')
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
        step_key = f"Stage {stage_num}: Step {step_letter}"
        
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

print(f"✓ Extracted {len(table_data)} steps from {len([p for p in set(re.findall(r'Stage ([0-9IViv]+)', ''.join(table_data.keys())))])} stages")
print(f"✓ Found {len(harnesses)} unique harnesses")
print(f"✓ Table dimensions: {len(harnesses)}×{len(steps)} = {len(harnesses)*len(steps)} cells")
print(f"✓ Filled cells: {(table != '').sum().sum()} ({100*(table != '').sum().sum()/(len(harnesses)*len(steps)):.1f}%)\n")

# Create a numeric matrix for heatmap: count of strategies per cell
heatmap_data = np.zeros_like(table.values, dtype=float)
text_labels = []
has_value = np.zeros_like(table.values, dtype=bool)

for i, harness in enumerate(table.index):
    row_labels = []
    for j, step in enumerate(table.columns):
        cell_value = table.iloc[i, j]
        if pd.notna(cell_value) and str(cell_value).strip():
            strategy_count = len(str(cell_value).split(','))
            heatmap_data[i, j] = strategy_count
            has_value[i, j] = True
            row_labels.append(str(cell_value))
        else:
            heatmap_data[i, j] = 0
            row_labels.append('')
    text_labels.append(row_labels)

# Create custom colorscale: white for 0, gradient for 1-6
colorscale = [
    [0.0, 'white'],
    [1/6, '#e0f3f8'],
    [2/6, '#abd9e9'],
    [3/6, '#74add1'],
    [4/6, '#4575b4'],
    [5/6, '#313695'],
    [1.0, '#08306b']
]

# Create interactive heatmap with annotations
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=table.columns,
    y=table.index,
    colorscale=colorscale,
    text=text_labels,
    texttemplate='%{text}',
    textfont={"size": 10},
    hovertemplate='<b>%{y}</b><br>%{x}<br>Strategies: %{text}<extra></extra>',
    colorbar=dict(title="Strategy<br>Count", tickvals=[0, 1, 2, 3, 4, 5, 6], ticktext=['0', '1', '2', '3', '4', '5', '6']),
    zmid=3,
    zmin=0,
    zmax=6
))

fig.update_layout(
    xaxis_title='Evaluation Steps',
    yaxis_title='Evaluation Harnesses',
    width=1400,
    height=1000,
    font=dict(size=9),
    xaxis=dict(side='bottom'),
    yaxis=dict(autorange='reversed'),
    margin=dict(l=0, r=0, t=0, b=50)
)

html_path = Path('../figures/rq1_heatmap.pdf')
fig.write_image(html_path)

print(f"✓ Interactive heatmap saved to: {html_path}")
print(f"  - White cells: no strategies (empty)")
print(f"  - Light cyan cells: 1 strategy")
print(f"  - Blue cells: 2-4 strategies")
print(f"  - Dark blue cells: 5-6 strategies")