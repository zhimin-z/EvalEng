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

# Helper function for sorting stages (numeric 0-4)
def stage_sort_key(x):
    if x is None:
        return (1, 0)  # Put unspecified at the end
    if isinstance(x, (int, float)):
        return (0, x)  # Numeric stages, sorted by value
    return (1, 0)  # Other values at the end

# Helper function for sorting steps
def step_sort_key(x):
    if x is None:
        return (2, '')  # Put unspecified at the end
    if isinstance(x, (int, float)):
        return (0, x)  # Numeric steps first, sorted by value
    if isinstance(x, str) and len(x) == 1 and x.isalpha():
        return (1, x.upper())  # Single letter steps second, sorted alphabetically
    if isinstance(x, str):
        return (1, x.upper())  # Other string steps, sorted alphabetically
    return (2, '')  # Default to end


# Load data for workflow visualization (full dataset)
workflow_file = "../data/rq3_issues_annotated_full.jsonl"
workflow_df = pd.read_json(workflow_file, lines=True)

if len(workflow_df) > 0:
    # Filter related issues
    related_df = workflow_df[workflow_df['is_related'] == True].copy()

    # Convert numeric values to integers (keep NaN as is)
    related_df['stage'] = related_df['stage'].apply(convert_to_int_if_numeric)
    related_df['step'] = related_df['step'].apply(convert_to_int_if_numeric)
    related_df['strategy'] = related_df['strategy'].apply(convert_to_int_if_numeric)

    # Create hierarchical structure: Stage -> Step -> Strategy -> Count
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for _, row in related_df.iterrows():
        # Normalize NaN to None for dictionary keys (NaN != NaN causes issues)
        stage = None if pd.isna(row['stage']) else row['stage']
        step = None if pd.isna(row['step']) else row['step']
        strategy = None if pd.isna(row['strategy']) else row['strategy']
        hierarchy[stage][step][strategy] += 1

    # Sort stages (numeric 0-4, with None at end)
    stage_order = sorted(hierarchy.keys(), key=stage_sort_key)

    # Calculate total issues and stage percentages
    total_issues = len(related_df)
    stage_percentages = {}
    for stage in stage_order:
        stage_val = stage if stage is not None else None
        if stage is None:
            stage_count = len(related_df[related_df['stage'].isna()])
        else:
            stage_count = len(related_df[related_df['stage'] == stage])
        stage_percentage = (stage_count / total_issues * 100) if total_issues > 0 else 0
        stage_percentages[stage] = stage_percentage

    # Prepare data for plotting
    stages = []
    steps_per_stage = []
    strategies_per_step = []

    for stage in stage_order:
        # Sort steps (handles numeric, alphabetic, and "NA")
        steps = sorted(hierarchy[stage].keys(), key=step_sort_key)

        for step in steps:
            strategies = hierarchy[stage][step]
            stages.append(stage)
            steps_per_stage.append(step)
            strategies_per_step.append(strategies)

    # Get all unique strategies across all data
    all_strategies = set()
    for strategies_dict in strategies_per_step:
        all_strategies.update(strategies_dict.keys())

    # Sort strategies (handles integers/strings, with None at the end)
    strategy_order = sorted(all_strategies, key=lambda x: (
        x is None, x if isinstance(x, (int, float)) and x is not None else 0
    ))

    # Create the plot
    fig, ax = plt.subplots(figsize=(16, 8))

    # Prepare data for stacked bars
    x_positions = []
    x_labels = []
    bar_width = 0.6

    # Group positions by stage
    stage_positions = defaultdict(list)
    current_x = 0
    stage_boundaries = []

    for i, (stage, step) in enumerate(zip(stages, steps_per_stage)):
        x_positions.append(current_x)
        # Add "Step " prefix for clarity unless it's None (convert to "NA" for display)
        step_label = step if step is not None else "NA"
        x_labels.append(step_label)
        stage_positions[stage].append(current_x)
        current_x += 1

    # Calculate stage boundaries for grouping
    prev_stage = None
    for i, stage in enumerate(stages):
        if stage != prev_stage:
            if prev_stage is not None:
                stage_boundaries.append(i - 0.5)
            prev_stage = stage

    # Plot stacked bars
    bottom = np.zeros(len(x_positions))
    colors = plt.cm.Set3(np.linspace(0, 1, len(strategy_order)))
    all_segments = []  # Collect segment data for value annotations

    for strategy_idx, strategy in enumerate(strategy_order):
        heights = []
        for strategies_dict in strategies_per_step:
            heights.append(strategies_dict.get(strategy, 0))

        # Convert None to "NA" for legend display, ensure integers are shown as int
        if strategy is None:
            legend_label = "NA"
        elif isinstance(strategy, float) and strategy.is_integer():
            legend_label = int(strategy)
        else:
            legend_label = strategy
        bars = ax.bar(x_positions, heights, bar_width, bottom=bottom,
                     label=legend_label, color=colors[strategy_idx], edgecolor='white', linewidth=0.5)
        # Collect segment data for annotations
        for i in range(len(x_positions)):
            if heights[i] > 0:
                all_segments.append({
                    'x': x_positions[i],
                    'bottom': bottom[i],
                    'height': heights[i],
                    'value': int(heights[i]),
                    'bar_idx': i,
                })
        bottom += heights

    # Add value annotations to each stack segment
    max_bar_height = max(bottom) if len(bottom) > 0 else 1
    thin_threshold = max(max_bar_height * 0.06, 2)

    # Separate thick and thin segments; group thin ones by bar
    thin_segments_by_bar = defaultdict(list)
    for seg in all_segments:
        if seg['height'] >= thin_threshold:
            # Place value text centered inside the segment
            mid_y = seg['bottom'] + seg['height'] / 2
            ax.text(seg['x'], mid_y, str(seg['value']),
                    ha='center', va='center', fontsize=9, fontweight='bold',
                    color='black')
        else:
            thin_segments_by_bar[seg['bar_idx']].append(seg)

    # Annotate thin segments with arrows at varying angles to avoid collision
    import math
    arrow_len = 18  # arrow length in points
    base_angle = 20  # starting angle in degrees
    angle_step = 40  # rotation between successive arrows in the same bar
    for bar_idx, thin_segs in thin_segments_by_bar.items():
        thin_segs.sort(key=lambda s: s['bottom'])
        for i, seg in enumerate(thin_segs):
            mid_y = seg['bottom'] + seg['height'] / 2
            angle = math.radians(base_angle + i * angle_step)
            length = arrow_len + i * 12  # progressively longer to avoid box collision
            x_offset_pts = length * math.cos(angle)
            y_offset_pts = length * math.sin(angle)
            ax.annotate(
                str(seg['value']),
                xy=(seg['x'], mid_y),
                xytext=(x_offset_pts, y_offset_pts),
                textcoords='offset points',
                fontsize=9, fontweight='bold',
                arrowprops=dict(
                    arrowstyle='->,head_length=0.3,head_width=0.15',
                    color='gray',
                    lw=0.8,
                    shrinkA=0,
                    shrinkB=0,
                ),
                ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor='gray', alpha=0.8),
            )

    # Add vertical lines to separate stages
    for boundary in stage_boundaries:
        ax.axvline(x=boundary, color='black', linewidth=2, linestyle='--', alpha=0.5)

    # Set labels and title
    ax.set_xlabel('Steps (grouped by Stage)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Issues', fontsize=12, fontweight='bold')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, ha='center', fontsize=12)

    # Set tight x-axis limits to eliminate margin space
    ax.set_xlim(-0.5, current_x - 0.5)

    # Add stage labels as text annotations near the top
    for idx, stage in enumerate(stage_order):
        positions = stage_positions[stage]
        if positions:
            # Center based on boundaries for margin groups, use actual bar positions
            if idx == 0:
                # First group: use min position as left boundary
                left_boundary = min(positions) - 0.5
                right_boundary = stage_boundaries[0] if stage_boundaries else max(positions) + 0.5
            elif idx == len(stage_order) - 1:
                # Last group: use max position as right boundary
                left_boundary = stage_boundaries[-1]
                right_boundary = max(positions) + 0.5
            else:
                # Middle groups: use adjacent boundaries
                left_boundary = stage_boundaries[idx - 1]
                right_boundary = stage_boundaries[idx]
            center_x = (left_boundary + right_boundary) / 2
            # Add "Stage " prefix for clarity with percentage
            stage_percentage = stage_percentages[stage]
            stage_label = f"Stage {stage}\n({stage_percentage:.2f}%)"
            ax.text(center_x, 0.97, stage_label, transform=ax.get_xaxis_transform(),
                   ha='center', va='top', fontsize=13, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.7))

    # Add legend
    ax.legend(title='Strategy', bbox_to_anchor=(0.91, 0.9), loc='upper left',
             fontsize=12, title_fontsize=13, markerscale=1.5)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Add padding to y-axis limit to make room for labels above bars
    y_max = ax.get_ylim()[1]
    ax.set_ylim(0, y_max * 1.2)  # Add 20% padding for labels and arrows

    # Adjust layout
    plt.tight_layout()

    # Save figure
    output_path = "../figures/rq2_workflow.pdf"
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
   
    # Print LaTeX table for workflow breakdown
    print("=" * 70)
    print(f"WORKFLOW STAGE/STEP/STRATEGY BREAKDOWN ({output_path})")
    print("=" * 70)

    if len(related_df) > 0:
        # Collect table rows: (ID, Count, Proportion)
        table_rows = []

        # Get all unique stages, sorted (excluding NaN)
        stages_list = sorted([s for s in related_df['stage'].unique() if not pd.isna(s)], key=stage_sort_key)

        # Count issues with no stage specified (general workflow level)
        no_stage_count = len(related_df[related_df['stage'].isna()])

        # Add "General" row (workflow level - no stage)
        if no_stage_count > 0:
            general_pct = (no_stage_count / total_issues * 100) if total_issues > 0 else 0
            table_rows.append(("General", no_stage_count, general_pct))

        # Iterate through stages
        for stage in stages_list:
            stage_df = related_df[related_df['stage'] == stage]
            stage_count = len(stage_df)
            stage_label = str(int(stage) if isinstance(stage, float) else stage)

            # Add stage summary row with percentage relative to total issues
            stage_pct = (stage_count / total_issues * 100) if total_issues > 0 else 0
            table_rows.append((f"S{stage_label}", stage_count, stage_pct))

            # Count issues with no step specified (general stage level)
            no_step_count = len(stage_df[stage_df['step'].isna()])

            # Add "S{stage} (general)" row if there are issues at stage level but no step
            if no_step_count > 0:
                no_step_pct = (no_step_count / stage_count * 100) if stage_count > 0 else 0
                table_rows.append((f"S{stage_label} (general)", no_step_count, no_step_pct))

            # Get all unique steps for this stage (excluding NaN)
            steps = sorted([s for s in stage_df['step'].unique() if not pd.isna(s)], key=step_sort_key)

            for step in steps:
                step_df = stage_df[stage_df['step'] == step]
                step_count = len(step_df)
                step_label = str(int(step) if isinstance(step, float) else step)

                # Count issues with no strategy specified (general step level)
                no_strategy_count = len(step_df[step_df['strategy'].isna()])

                # Add "S{stage}-{step} (general)" row if there are issues at step level but no strategy
                if no_strategy_count > 0:
                    no_strat_pct = (no_strategy_count / step_count * 100) if step_count > 0 else 0
                    table_rows.append((f"S{stage_label}-{step_label} (general)", no_strategy_count, no_strat_pct))

                # Get all unique strategies for this step (excluding NaN)
                strategies = sorted([s for s in step_df['strategy'].unique() if not pd.isna(s)], key=str)

                for strategy in strategies:
                    strategy_count = len(step_df[step_df['strategy'] == strategy])
                    strat_label = str(int(strategy) if isinstance(strategy, float) else strategy)
                    strat_pct = (strategy_count / step_count * 100) if step_count > 0 else 0
                    table_rows.append((f"S{stage_label}-{step_label}{strat_label}", strategy_count, strat_pct))

        # Print LaTeX table
        print("\\begin{table}[!t]")
        print("\\centering")
        print("\\caption{Issue distribution across workflow stages, steps, and strategies. ``Local \\%'' denotes the percentage relative to the parent workflow component. Stage rows show percentage relative to total issues. Unlisted workflow components indicate no issues exist.}")
        print("\\label{tab:workflow_breakdown}")
        print("\\begin{tabular}{lrr}")
        print("\\toprule")
        print("Workflow Component & Count & Local \\% \\\\")
        print("\\midrule")
        table_rows_sorted = sorted(table_rows, key=lambda row: row[0])
        for row_id, count, proportion in table_rows_sorted:
            print(f"{row_id} & {count} & {proportion:.1f}\\% \\\\")
        print("\\bottomrule")
        print("\\end{tabular}")
        print("\\end{table}")

    plt.close()
