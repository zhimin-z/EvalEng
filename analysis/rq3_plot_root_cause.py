import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict

# Helper function to convert numeric values to integers
def convert_to_int_if_numeric(val):
    if pd.isna(val):
        return val
    try:
        # Try to convert to float first, then to int
        num_val = float(val)
        if num_val.is_integer():
            return int(num_val)
        return num_val
    except (ValueError, TypeError):
        return val

# Helper function for smart label splitting
def smart_split_label(label, max_combined_length=10):
    """
    Split label into lines, keeping short consecutive words together.
    Two successive words are kept on the same line if their combined length <= max_combined_length.
    """
    words = label.split(' ')
    if len(words) <= 1:
        return label

    lines = []
    current_line_words = [words[0]]

    for i in range(1, len(words)):
        # Check if the last word in current line and the next word should be on same line
        last_word = current_line_words[-1]
        next_word = words[i]

        if len(last_word) + len(next_word) <= max_combined_length:
            # Keep them together
            current_line_words.append(next_word)
        else:
            # Start a new line
            lines.append(' '.join(current_line_words))
            current_line_words = [next_word]

    # Add the final line
    if current_line_words:
        lines.append(' '.join(current_line_words))

    return '\n'.join(lines)

# Load data for root cause visualization (sample dataset)
root_cause_file = "../data/rq2_issues_annotated_full.jsonl"
root_cause_results_df = pd.read_json(root_cause_file, lines=True)

if len(root_cause_results_df) > 0:
    # Filter issues that have root_cause_label from ALL issues (not just related ones)
    root_cause_df = root_cause_results_df[root_cause_results_df['root_cause_label'].notna()].copy()

    # Convert root_cause_label to string for mapping
    root_cause_df['root_cause_label'] = root_cause_df['root_cause_label'].astype(str)

    # Handle any unmapped values
    root_cause_df['root_cause_label'] = root_cause_df['root_cause_label'].fillna('Unknown')

    # Convert stage and step values to proper types (keep NaN as is)
    root_cause_df['stage'] = root_cause_df['stage'].apply(convert_to_int_if_numeric)
    root_cause_df['step'] = root_cause_df['step'].apply(convert_to_int_if_numeric)

    # Create hierarchical structure: RootCause -> Stage -> Step -> Count
    root_cause_hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for _, row in root_cause_df.iterrows():
        root_cause = row['root_cause_label']
        # Normalize NaN to None for dictionary keys (NaN != NaN causes issues)
        stage = None if pd.isna(row['stage']) else row['stage']
        step = None if pd.isna(row['step']) else row['step']
        root_cause_hierarchy[root_cause][stage][step] += 1

    # Sort root causes by total count (descending)
    root_cause_totals = {
        rc: sum(sum(steps.values()) for steps in stages.values())
        for rc, stages in root_cause_hierarchy.items()
    }
    # Sort alphabetically, excluding "Others"
    sorted_root_cause_labels = sorted(
        [rc for rc in root_cause_totals.keys() if rc.lower() != 'others'],
        key=lambda x: x.lower()
    )

    # Calculate root cause percentages
    total_root_cause_issues = len(root_cause_df)
    root_cause_percentages = {
        rc: (root_cause_totals[rc] / total_root_cause_issues * 100) if total_root_cause_issues > 0 else 0
        for rc in root_cause_totals.keys()
    }

    # Print ratio of total issues for each root cause
    print(f"Total issues with root cause label: {total_root_cause_issues}")
    print()
    for rc in sorted_root_cause_labels:
        count = root_cause_totals[rc]
        pct = root_cause_percentages[rc]
        print(f"  {rc}: {count} ({pct:.1f}%)")
    print()

    # Get all unique stages and steps across root causes (excluding None for visualization)
    all_stages_in_root_causes = set()
    all_steps_in_root_causes = set()
    for stages_dict in root_cause_hierarchy.values():
        for stage in stages_dict.keys():
            if stage is not None:
                all_stages_in_root_causes.add(stage)
        for steps_dict in stages_dict.values():
            all_steps_in_root_causes.update(steps_dict.keys())

    # Define explicit stage order: 0-4 (only actual workflow stages)
    # This ensures consistent ordering
    explicit_stage_order = [0, 1, 2, 3, 4]

    # Filter to only include stages that actually exist in the data
    stage_order_for_root_causes = [s for s in explicit_stage_order if s in all_stages_in_root_causes]

    # Add any unexpected stages at the end (shouldn't happen, but be safe)
    for stage in all_stages_in_root_causes:
        if stage not in stage_order_for_root_causes:
            stage_order_for_root_causes.append(stage)

    # Sort steps (handles alphabetic and None)
    step_order = sorted(all_steps_in_root_causes, key=lambda x: (
        x is None,  # Put None at the end
        x if isinstance(x, str) and x is not None else str(x) if x is not None else ''  # Alphabetically sort the rest
    ))

    # Build per-(stage, step) counts for each root cause (for the heatmap)
    plot_stage_step_counts = defaultdict(lambda: defaultdict(int))
    all_plot_combos = set()

    for _, row in root_cause_df.iterrows():
        root_cause = row['root_cause_label']
        stage = None if pd.isna(row['stage']) else row['stage']
        step = None if pd.isna(row['step']) else row['step']
        combo = (stage, step)
        plot_stage_step_counts[root_cause][combo] += 1
        all_plot_combos.add(combo)

    # Sort combos: by stage then step, General (None, None) last
    def plot_combo_sort_key(combo):
        stage, step = combo
        if stage is None:
            return (999, 1, '')
        stage_rank = stage
        if step is None:
            return (stage_rank, 1, '')
        return (stage_rank, 0, step)

    sorted_plot_combos = sorted(all_plot_combos, key=plot_combo_sort_key)

    # Generate column labels like "Stage 0\nStep A", "General"
    def combo_to_short_label(combo):
        stage, step = combo
        if stage is None:
            return "General"
        slabel = str(int(stage)) if isinstance(stage, (int, float)) else str(stage)
        if step is None:
            return f"Stage {slabel}"
        return f"Stage {slabel}\nStep {step}"

    combo_labels = [combo_to_short_label(c) for c in sorted_plot_combos]

    # Build the heatmap matrix: rows = root causes, columns = stage-step combos
    num_root_causes = len(sorted_root_cause_labels)
    num_combos = len(sorted_plot_combos)
    heatmap_data = np.zeros((num_root_causes, num_combos), dtype=int)

    for rc_idx, root_cause in enumerate(sorted_root_cause_labels):
        for combo_idx, combo in enumerate(sorted_plot_combos):
            heatmap_data[rc_idx, combo_idx] = plot_stage_step_counts[root_cause].get(combo, 0)

    # Create the heatmap
    fig_width = max(14, num_combos * 1.2)
    fig_height = max(6, num_root_causes * 0.7)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    im = ax.imshow(heatmap_data, cmap='Blues', aspect='auto')

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Number of Issues', fontsize=12, fontweight='bold')
    cbar.ax.tick_params(labelsize=11)

    # Annotate each cell with count and ratio (count / column total)
    col_totals = heatmap_data.sum(axis=0)  # sum over rows for each column
    for i in range(num_root_causes):
        for j in range(num_combos):
            val = heatmap_data[i, j]
            ratio = val / col_totals[j] * 100 if col_totals[j] > 0 else 0
            label = f"{val}\n({ratio:.1f}%)"
            # Use white text on dark cells, black on light cells
            text_color = 'white' if val > heatmap_data.max() * 0.6 else 'black'
            ax.text(j, i, label, ha='center', va='center',
                    fontsize=12, color=text_color)

    # Set tick labels
    ax.set_xticks(np.arange(num_combos))
    ax.set_xticklabels(combo_labels, ha='center', fontsize=14, fontweight='bold')
    ax.set_yticks(np.arange(num_root_causes))
    rc_labels = [smart_split_label(rc) for rc in sorted_root_cause_labels]
    ax.set_yticklabels(rc_labels, fontsize=14, fontweight='bold')

    # Move x-axis labels to top
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')

    # Add grid lines to separate cells
    for i in range(num_root_causes + 1):
        ax.axhline(y=i - 0.5, color='white', linewidth=1.5)
    for j in range(num_combos + 1):
        ax.axvline(x=j - 0.5, color='white', linewidth=1.5)

    # Adjust layout
    plt.tight_layout()

    # Save figure
    root_cause_output_path = "../figures/rq3_root_cause.pdf"
    plt.savefig(root_cause_output_path, format='pdf', bbox_inches='tight')
    
    # Map numeric stages to display labels
    stage_to_label = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'}

    # ================================================================
    # Table 1: Root Cause x Stage (stage-level cross-tab)
    # ================================================================
    numeric_stage_keys = [0, 1, 2, 3, 4]

    # Include General column for issues with no stage
    has_general_stage = any(
        None in root_cause_hierarchy[rc] for rc in sorted_root_cause_labels
    )

    stage_table_lines = []
    stage_table_lines.append("\\begin{table}[!t]")
    stage_table_lines.append("\\centering")
    stage_table_lines.append("\\caption{Root cause distribution across different workflow steps. "
                             "Each cell reports the absolute number of issues, while the percentage indicates the relative proportion of each root cause within the corresponding workflow step.}")
    stage_table_lines.append("\\label{tab:root_cause_stages}")

    stage_headers = [f"Stage {stage_to_label[k]}" for k in numeric_stage_keys]
    if has_general_stage:
        stage_headers.append("General")
    col_spec = "l" + "r" * len(stage_headers)
    stage_table_lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    stage_table_lines.append("\\toprule")
    stage_table_lines.append(" & ".join(["Root Cause"] + stage_headers) + " \\\\")
    stage_table_lines.append("\\midrule")

    for root_cause in sorted_root_cause_labels:
        total = root_cause_totals[root_cause]
        cells = [root_cause]

        for stage_key in numeric_stage_keys:
            if stage_key in root_cause_hierarchy[root_cause]:
                stage_count = sum(root_cause_hierarchy[root_cause][stage_key].values())
            else:
                stage_count = 0
            if stage_count > 0 and total > 0:
                pct = stage_count / total * 100
                cells.append(f"{pct:.1f}\\%")
            else:
                cells.append("")

        if has_general_stage:
            general_count = sum(root_cause_hierarchy[root_cause].get(None, {}).values())
            if general_count > 0 and total > 0:
                pct = general_count / total * 100
                cells.append(f"{pct:.1f}\\%")
            else:
                cells.append("")

        stage_table_lines.append(" & ".join(cells) + " \\\\")

    stage_table_lines.append("\\bottomrule")
    stage_table_lines.append("\\end{tabular}")
    stage_table_lines.append("\\end{table}")

    print()
    print('\n'.join(stage_table_lines))
    print()

    # ================================================================
    # Table 2 (Cross-tabulation): Root Cause x Stage-Step
    # Rows = root cause categories, Columns = "Stage {num}\nStep {letter}"
    # Matching the column format from rq1_plot_heatmap.py
    # ================================================================

    # Build per-(stage, step) counts for each root cause
    stage_step_counts = defaultdict(lambda: defaultdict(int))
    all_stage_step_combos = set()

    for _, row in root_cause_df.iterrows():
        root_cause = row['root_cause_label']
        stage = None if pd.isna(row['stage']) else row['stage']
        step = None if pd.isna(row['step']) else row['step']
        combo = (stage, step)
        stage_step_counts[root_cause][combo] += 1
        all_stage_step_combos.add(combo)

    # Sort combos: known stage-step pairs first (by stage order, then step letter),
    # stage-only (no step) after steps of same stage, General (None, None) last
    stage_order_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

    def combo_sort_key(combo):
        stage, step = combo
        if stage is None:
            return (999, 1, '')
        stage_rank = stage_order_map.get(stage, 998)
        if step is None:
            return (stage_rank, 1, '')
        return (stage_rank, 0, step)

    sorted_combos = sorted(all_stage_step_combos, key=combo_sort_key)

    # Generate column names matching rq1 format: "Stage {num}\nStep {letter}"
    def combo_to_col_name(combo):
        stage, step = combo
        if stage is None:
            return "General"
        slabel = stage_to_label.get(stage, str(stage))
        if step is None:
            return f"Stage {slabel}"
        return f"Stage {slabel}\nStep {step}"

    col_names = [combo_to_col_name(c) for c in sorted_combos]

    # Build cross-tab DataFrame (counts)
    crosstab = pd.DataFrame(0, index=sorted_root_cause_labels, columns=col_names)
    for root_cause in sorted_root_cause_labels:
        for combo, count in stage_step_counts[root_cause].items():
            col = combo_to_col_name(combo)
            crosstab.loc[root_cause, col] = count

    # Generate LaTeX table with percentages (each cell = step count / root cause total)
    def combo_to_latex_header(combo):
        stage, step = combo
        if stage is None:
            return "General"
        slabel = stage_to_label.get(stage, str(stage))
        if step is None:
            return f"Stage {slabel}"
        return f"Stage {slabel} Step {step}"

    latex_col_headers = [combo_to_latex_header(c) for c in sorted_combos]

    latex_lines = []
    latex_lines.append("\\begin{table}[!t]")
    latex_lines.append("\\centering")
    latex_lines.append("\\caption{Root cause distribution across workflow stage-step combinations. "
                       "Each cell reports the absolute number of issues, while the percentage indicates the relative proportion of each stage-step within the corresponding root cause.}")
    latex_lines.append("\\label{tab:root_cause_steps}")

    col_spec = "l" + "r" * len(sorted_combos)
    latex_lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    latex_lines.append("\\toprule")

    header_cells = ["Root Cause"] + latex_col_headers
    latex_lines.append(" & ".join(header_cells) + " \\\\")
    latex_lines.append("\\midrule")

    for root_cause in sorted_root_cause_labels:
        total = root_cause_totals[root_cause]
        cells = [root_cause]
        for col in col_names:
            count = int(crosstab.loc[root_cause, col])
            if count > 0 and total > 0:
                pct = count / total * 100
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

    plt.close()
