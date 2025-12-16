import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

output_file = "data/github_issues_analyzed.jsonl"
results_df = pd.read_json(output_file, lines=True)

if len(results_df) > 0:
    print("\nRelated issues by stage, step, and strategy:")
    # Filter related issues
    related_df = results_df[results_df['is_related'] == True].copy()

    # Replace NaN with "unspecific" for better visualization
    related_df['stage'] = related_df['stage'].fillna('unspecific')
    related_df['step'] = related_df['step'].fillna('unspecific')
    related_df['strategy'] = related_df['strategy'].fillna('unspecific')

    # Convert numeric values to integers (keep "unspecific" as string)
    def convert_to_int_if_numeric(val):
        if val == 'unspecific':
            return val
        try:
            # Try to convert to float first, then to int
            num_val = float(val)
            if num_val.is_integer():
                return int(num_val)
            return num_val
        except (ValueError, TypeError):
            return val

    related_df['stage'] = related_df['stage'].apply(convert_to_int_if_numeric)
    related_df['step'] = related_df['step'].apply(convert_to_int_if_numeric)
    related_df['strategy'] = related_df['strategy'].apply(convert_to_int_if_numeric)

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

    # Create hierarchical structure: Stage -> Step -> Strategy -> Count
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for _, row in related_df.iterrows():
        stage = row['stage']
        step = row['step']
        strategy = row['strategy']
        hierarchy[stage][step][strategy] += 1

    # Sort stages (handles numeric, roman numerals, and "unspecific")
    def stage_sort_key(x):
        if x == 'unspecific':
            return (2, 0)  # Put unspecific at the end
        if isinstance(x, (int, float)):
            return (0, x)  # Numeric stages first, sorted by value
        roman_val = roman_to_int(x)
        if roman_val is not None:
            return (1, roman_val)  # Roman numerals second, sorted by value
        return (2, 0)  # Other strings at the end

    stage_order = sorted(hierarchy.keys(), key=stage_sort_key)

    # Helper function for sorting steps
    def step_sort_key(x):
        if x == 'unspecific':
            return (2, '')  # Put unspecific at the end
        if isinstance(x, (int, float)):
            return (0, x)  # Numeric steps first, sorted by value
        if isinstance(x, str) and len(x) == 1 and x.isalpha():
            return (1, x.upper())  # Single letter steps second, sorted alphabetically
        if isinstance(x, str):
            return (1, x.upper())  # Other string steps, sorted alphabetically
        return (2, '')  # Default to end

    # Prepare data for plotting
    stages = []
    steps_per_stage = []
    strategies_per_step = []

    for stage in stage_order:
        # Sort steps (handles numeric, alphabetic, and "unspecific")
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

    # Sort strategies (handles integers/strings, with "unspecific" at the end)
    strategy_order = sorted(all_strategies, key=lambda x: (
        x == 'unspecific', x if isinstance(x, (int, float)) else 0
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
        # Add "Step " prefix for clarity unless it's "unspecific"
        step_label = f"Step {step}" if step != 'unspecific' else step
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

        bars = ax.bar(x_positions, heights, bar_width, bottom=bottom,
                     label=strategy, color=colors[strategy_idx], edgecolor='white', linewidth=0.5)
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
    ax.set_title('Distribution of Issues across Stages, Steps, and Strategies',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)

    # Add stage labels as text annotations near the top
    for stage in stage_order:
        positions = stage_positions[stage]
        if positions:
            center_x = np.mean(positions)
            # Add "Stage " prefix for clarity unless it's "unspecific"
            stage_label = f"Stage {stage}" if stage != 'unspecific' else stage
            ax.text(center_x, 0.97, stage_label, transform=ax.get_xaxis_transform(),
                   ha='center', va='top', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.7))

    # Add legend
    ax.legend(title='Strategies', bbox_to_anchor=(1.05, 1), loc='upper left',
             fontsize=9, title_fontsize=10)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Add padding to y-axis limit to make room for labels above bars
    y_max = ax.get_ylim()[1]
    ax.set_ylim(0, y_max * 1.1)  # Add 10% padding above the highest bar

    # Adjust layout
    plt.tight_layout()

    # Save figure
    output_path = "data/github_issue_distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to {output_path}")

    # Also print summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total related issues: {len(related_df)}")
    print(f"\nIssues by Stage, Step, and Strategy:")
    for stage in stage_order:
        stage_total = sum(sum(strategies.values()) for strategies in hierarchy[stage].values())
        print(f"\nStage {stage if stage != 'unspecific' else 'unspecific'}: {stage_total} issues")

        # Sort steps for this stage (using the same step_sort_key function)
        steps = sorted(hierarchy[stage].keys(), key=step_sort_key)

        for step in steps:
            step_total = sum(hierarchy[stage][step].values())
            print(f"  Step {step if step != 'unspecific' else 'unspecific'}: {step_total} issues")

            # Sort strategies for this step
            strategies = sorted(hierarchy[stage][step].keys(), key=lambda x: (
                x == 'unspecific', x if isinstance(x, (int, float)) else 0
            ))

            for strategy in strategies:
                count = hierarchy[stage][step][strategy]
                print(f"    Strategy {strategy if strategy != 'unspecific' else 'unspecific'}: {count} issues")

    plt.close()
