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

# Helper function to convert roman numerals to integers for sorting
def roman_to_int(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not isinstance(s, str):
        return None
    total = 0
    prev_value = 0
    for char in reversed(s.upper()):
        if char not in roman_values:
            return None
        value = roman_values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

# Helper function for sorting stages
def stage_sort_key(x):
    if x is None:
        return (2, 0)  # Put unspecified at the end
    if isinstance(x, (int, float)):
        return (0, x)  # Numeric stages first, sorted by value
    roman_val = roman_to_int(x)
    if roman_val is not None:
        return (1, roman_val)  # Roman numerals second, sorted by value
    return (2, 0)  # Other strings at the end

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
workflow_file = "../data/rq2_issues_annotated.jsonl"
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

    # Sort stages (handles numeric, roman numerals, and "NA")
    stage_order = sorted(hierarchy.keys(), key=stage_sort_key)

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
        bottom += heights

    # Add total count labels on top of each bar
    for i, (x_pos, total) in enumerate(zip(x_positions, bottom)):
        if total > 0:  # Only show label if there are issues
            ax.text(x_pos, total, str(int(total)), ha='center', va='bottom',
                   fontsize=9, fontweight='bold')

    # Add vertical lines to separate stages
    for boundary in stage_boundaries:
        ax.axvline(x=boundary, color='black', linewidth=2, linestyle='--', alpha=0.5)

    # Set labels and title
    ax.set_xlabel('Steps (grouped by Stage)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Issues', fontsize=12, fontweight='bold')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, ha='center', fontsize=9)

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
            # Add "Stage " prefix for clarity unless it's None (convert to "NA" for display)
            stage_label = f"Stage {stage}" if stage is not None else "NA"
            ax.text(center_x, 0.97, stage_label, transform=ax.get_xaxis_transform(),
                   ha='center', va='top', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.7))

    # Add legend
    ax.legend(title='Strategy', bbox_to_anchor=(0.92, 0.9), loc='upper left',
             fontsize=12, title_fontsize=13, markerscale=1.5)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Add padding to y-axis limit to make room for labels above bars
    y_max = ax.get_ylim()[1]
    ax.set_ylim(0, y_max * 1.1)  # Add 10% padding above the highest bar

    # Adjust layout
    plt.tight_layout()

    # Save figure
    output_path = "../figures/rq2_workflow.pdf"
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
   
    # Print hierarchical tree-style breakdown
    print("=" * 70)
    print(f"WORKFLOW STAGE/STEP/STRATEGY BREAKDOWN ({output_path})")
    print("=" * 70)

    if len(related_df) > 0:
        # Get all unique stages, sorted (excluding NaN)
        stages_list = sorted([s for s in related_df['stage'].unique() if not pd.isna(s)], key=stage_sort_key)

        # Count issues with no stage specified (general workflow level)
        no_stage_count = len(related_df[related_df['stage'].isna()])

        # Iterate through stages
        for stage in stages_list:
            stage_df = related_df[related_df['stage'] == stage]
            stage_count = len(stage_df)
            print(f"{'Stage ' + str(int(stage) if isinstance(stage, float) else stage) + ':':<24} {stage_count:>3}")

            # Count issues with no step specified (general stage level)
            no_step_count = len(stage_df[stage_df['step'].isna()])

            # Show "General (no step)" if applicable
            if no_step_count > 0:
                print(f"  {'├─ General (no step):':<22} {no_step_count:>3}")

            # Get all unique steps for this stage (excluding NaN)
            steps = sorted([s for s in stage_df['step'].unique() if not pd.isna(s)], key=step_sort_key)

            for step_idx, step in enumerate(steps):
                step_df = stage_df[stage_df['step'] == step]
                step_count = len(step_df)
                is_last_step = (step_idx == len(steps) - 1) and no_step_count == 0
                step_prefix = "└─" if is_last_step else "├─"
                step_label = str(int(step) if isinstance(step, float) else step)
                print(f"  {step_prefix} {'Step ' + str(int(stage) if isinstance(stage, float) else stage) + '-' + step_label + ':':<20} {step_count:>3}")

                # Count issues with no strategy specified (general step level)
                no_strategy_count = len(step_df[step_df['strategy'].isna()])

                # Get all unique strategies for this step (excluding NaN)
                strategies = sorted([s for s in step_df['strategy'].unique() if not pd.isna(s)], key=str)

                step_continuation = "  " if is_last_step else "│ "

                if no_strategy_count > 0:
                    if len(strategies) > 0:
                        print(f"  {step_continuation}  {'├─ General (no strategy):':<18} {no_strategy_count:>3}")
                    else:
                        print(f"  {step_continuation}  {'└─ General (no strategy):':<18} {no_strategy_count:>3}")

                for strat_idx, strategy in enumerate(strategies):
                    strategy_count = len(step_df[step_df['strategy'] == strategy])
                    is_last_strategy = (strat_idx == len(strategies) - 1)
                    strat_prefix = "└─" if is_last_strategy else "├─"
                    strat_label = str(int(strategy) if isinstance(strategy, float) else strategy)
                    print(f"  {step_continuation}  {strat_prefix} {'Strategy ' + str(int(stage) if isinstance(stage, float) else stage) + '-' + step_label + '-' + strat_label + ':':<14} {strategy_count:>3}")

        # Show "General (no stage)" at the same level as other stages
        if no_stage_count > 0:
            print(f"{'General (no stage):':<24} {no_stage_count:>3}")

    plt.close()
