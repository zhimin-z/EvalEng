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
root_cause_file = "../data/rq3_issues_annotated_full.jsonl"
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
    sorted_root_cause_labels = sorted(root_cause_totals.keys(), key=lambda x: root_cause_totals[x], reverse=True)

    # Calculate root cause percentages
    total_root_cause_issues = len(root_cause_df)
    root_cause_percentages = {
        rc: (root_cause_totals[rc] / total_root_cause_issues * 100) if total_root_cause_issues > 0 else 0
        for rc in root_cause_totals.keys()
    }

    # Get all unique stages and steps across root causes (excluding None for visualization)
    all_stages_in_root_causes = set()
    all_steps_in_root_causes = set()
    for stages_dict in root_cause_hierarchy.values():
        for stage in stages_dict.keys():
            if stage is not None:
                all_stages_in_root_causes.add(stage)
        for steps_dict in stages_dict.values():
            all_steps_in_root_causes.update(steps_dict.keys())

    # Define explicit stage order: 0, I, II, III, IV (only actual workflow stages)
    # This ensures consistent ordering
    explicit_stage_order = [0, 'I', 'II', 'III', 'IV']

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

    # Create the plot
    fig, ax = plt.subplots(figsize=(16, 8))

    # Prepare data for grouped and stacked bars
    num_root_causes = len(sorted_root_cause_labels)
    num_stages = len(stage_order_for_root_causes)
    num_steps = len(step_order)
    bar_width = 0.6

    # Use different color map for steps (legend will show steps)
    step_colors = plt.cm.Set3(np.linspace(0, 1, num_steps))

    # Track positions for each root cause (for top labels)
    root_cause_positions = defaultdict(list)
    x_positions = []
    x_labels = []
    current_x = 0
    root_cause_boundaries = []

    # Plot grouped bars with stacking by steps
    for rc_idx, root_cause in enumerate(sorted_root_cause_labels):
        for stage_idx, stage in enumerate(stage_order_for_root_causes):
            x_positions.append(current_x)
            x_labels.append(str(stage))
            root_cause_positions[root_cause].append(current_x)

            # Stack bars by steps
            bottom = 0

            for step_idx, step in enumerate(step_order):
                count = root_cause_hierarchy[root_cause].get(stage, {}).get(step, 0)

                # Only add to legend once (for the first root cause and first stage)
                # Convert None to "NA" for legend display (steps stay as-is, not converted to int)
                legend_label = "NA" if step is None else step
                label = legend_label if rc_idx == 0 and stage_idx == 0 else ""

                bars = ax.bar(current_x, count, bar_width, bottom=bottom,
                             label=label if rc_idx == 0 and stage_idx == 0 else "",
                             color=step_colors[step_idx], edgecolor='white', linewidth=0.5)

                bottom += count

            # Add total count labels on top of each stacked bar
            if bottom > 0:
                ax.text(current_x, bottom, str(int(bottom)), ha='center', va='bottom',
                       fontsize=9, fontweight='bold')

            current_x += 1

        # Add boundary after each root cause (except the last one)
        if rc_idx < num_root_causes - 1:
            root_cause_boundaries.append(current_x - 0.5)

    # Add vertical lines to separate root causes
    for boundary in root_cause_boundaries:
        ax.axvline(x=boundary, color='black', linewidth=2, linestyle='--', alpha=0.5)

    # Set labels and title
    ax.set_xlabel('Stages (grouped by Root Cause)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Issues', fontsize=12, fontweight='bold')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, ha='center', fontsize=9)

    # Set tight x-axis limits to eliminate margin space
    ax.set_xlim(-0.5, current_x - 0.5)

    # Add root cause labels as text annotations near the top
    for idx, root_cause in enumerate(sorted_root_cause_labels):
        positions = root_cause_positions[root_cause]
        if positions:
            # Center based on boundaries for margin groups, use actual bar positions
            if idx == 0:
                # First group: use min position as left boundary
                left_boundary = min(positions) - 0.5
                right_boundary = root_cause_boundaries[0] if root_cause_boundaries else max(positions) + 0.5
            elif idx == len(sorted_root_cause_labels) - 1:
                # Last group: use max position as right boundary
                left_boundary = root_cause_boundaries[-1]
                right_boundary = max(positions) + 0.5
            else:
                # Middle groups: use adjacent boundaries
                left_boundary = root_cause_boundaries[idx - 1]
                right_boundary = root_cause_boundaries[idx]
            center_x = (left_boundary + right_boundary) / 2
            # Split label smartly, keeping short consecutive words together, with percentage
            root_cause_percentage = root_cause_percentages[root_cause]
            root_cause_with_percentage = f"{root_cause} ({root_cause_percentage:.2f}%)"
            display_label = smart_split_label(root_cause_with_percentage)
            ax.text(center_x, 0.97, display_label, transform=ax.get_xaxis_transform(),
                   ha='center', va='top', fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.7))

    # Add legend (showing steps now instead of stages)
    ax.legend(title='Step', bbox_to_anchor=(0.93, 0.85), loc='upper left',
             fontsize=12, title_fontsize=13, markerscale=1.5)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Add padding to y-axis limit to make room for labels above bars
    y_max = ax.get_ylim()[1]
    ax.set_ylim(0, y_max * 1.1)

    # Adjust layout
    plt.tight_layout()

    # Save figure
    root_cause_output_path = "../figures/rq3_root_cause.pdf"
    plt.savefig(root_cause_output_path, format='pdf', bbox_inches='tight')
    
    # Print LaTeX table for root cause breakdown
    print("=" * 70)
    print(f"ROOT CAUSE DISTRIBUTION BY STAGE ({root_cause_output_path})")
    print("=" * 70)
    print(f"Total issues with root cause labels: {len(root_cause_df)}")

    # Collect table rows: (RootCause, WorkflowStep, Count, Proportion)
    table_rows = []

    for root_cause in sorted_root_cause_labels:
        total = root_cause_totals[root_cause]

        # Count issues with no stage specified (general root cause level)
        no_stage_count = sum(root_cause_hierarchy[root_cause].get(None, {}).values())

        # Add row if there are issues at root cause level but no stage
        if no_stage_count > 0:
            no_stage_pct = (no_stage_count / total * 100) if total > 0 else 0
            table_rows.append((root_cause, "General", no_stage_count, no_stage_pct))

        # Iterate through stages for this root cause
        for stage in stage_order_for_root_causes:
            if stage not in root_cause_hierarchy[root_cause]:
                continue
            stage_total = sum(root_cause_hierarchy[root_cause][stage].values())
            if stage_total == 0:
                continue

            # Get steps for this stage
            steps_dict = root_cause_hierarchy[root_cause][stage]

            # Count issues with no step specified (general stage level)
            no_step_count = steps_dict.get(None, 0)

            # Add row if there are issues at stage level but no step
            if no_step_count > 0:
                no_step_pct = (no_step_count / stage_total * 100) if stage_total > 0 else 0
                table_rows.append((root_cause, f"S{stage} (general)", no_step_count, no_step_pct))

            # Get specified steps for this stage (excluding None)
            steps_with_counts = [(step, steps_dict[step]) for step in steps_dict.keys() if step is not None]
            # Sort steps
            steps_with_counts = sorted(steps_with_counts, key=lambda x: (
                x[0] is None if not isinstance(x[0], str) else False,
                x[0] if isinstance(x[0], str) else str(x[0])
            ))

            for step, step_count in steps_with_counts:
                step_pct = (step_count / stage_total * 100) if stage_total > 0 else 0
                table_rows.append((root_cause, f"S{stage}-{step}", step_count, step_pct))

    # Print LaTeX table
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{Root Cause Distribution Across Workflow Stages and Steps. Unlisted root cause/stage/step combinations indicate no issues exist.}")
    print("\\label{tab:root_cause_breakdown}")
    print("\\begin{tabular}{llrr}")
    print("\\toprule")
    print("Root Cause & Workflow Step & Count & Local \\% \\\\")
    print("\\midrule")
    for root_cause, workflow_step, count, proportion in table_rows:
        print(f"{root_cause} & {workflow_step} & {count} & {proportion:.1f}\\% \\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{table}")

    plt.close()
