import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

output_file = "data/github_issues_analyzed.jsonl"
results_df = pd.read_json(output_file, lines=True)

if len(results_df) > 0:
    print("\nRelated issues by phase, step, and strategy:")
    # Filter related issues
    related_df = results_df[results_df['is_related'] == True].copy()

    # Replace NaN with "unspecific" for better visualization
    related_df['phase'] = related_df['phase'].fillna('unspecific')
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

    related_df['phase'] = related_df['phase'].apply(convert_to_int_if_numeric)
    related_df['step'] = related_df['step'].apply(convert_to_int_if_numeric)
    related_df['strategy'] = related_df['strategy'].apply(convert_to_int_if_numeric)

    # Create hierarchical structure: Phase -> Step -> Strategy -> Count
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for _, row in related_df.iterrows():
        phase = row['phase']
        step = row['step']
        strategy = row['strategy']
        hierarchy[phase][step][strategy] += 1

    # Sort phases (handles integers/strings, with "unspecific" at the end)
    phase_order = sorted(hierarchy.keys(), key=lambda x: (
        x == 'unspecific', x if isinstance(x, (int, float)) else 0
    ))

    # Prepare data for plotting
    phases = []
    steps_per_phase = []
    strategies_per_step = []

    for phase in phase_order:
        # Sort steps (handles integers/strings, with "unspecific" at the end)
        steps = sorted(hierarchy[phase].keys(), key=lambda x: (
            x == 'unspecific', x if isinstance(x, (int, float)) else 0
        ))

        for step in steps:
            strategies = hierarchy[phase][step]
            phases.append(phase)
            steps_per_phase.append(step)
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

    # Group positions by phase
    phase_positions = defaultdict(list)
    current_x = 0
    phase_boundaries = []

    for i, (phase, step) in enumerate(zip(phases, steps_per_phase)):
        x_positions.append(current_x)
        # Add "Step " prefix for clarity unless it's "unspecific"
        step_label = f"Step {step}" if step != 'unspecific' else step
        x_labels.append(step_label)
        phase_positions[phase].append(current_x)
        current_x += 1

    # Calculate phase boundaries for grouping
    prev_phase = None
    for i, phase in enumerate(phases):
        if phase != prev_phase:
            if prev_phase is not None:
                phase_boundaries.append(i - 0.5)
            prev_phase = phase

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

    # Add vertical lines to separate phases
    for boundary in phase_boundaries:
        ax.axvline(x=boundary, color='black', linewidth=2, linestyle='--', alpha=0.5)

    # Set labels and title
    ax.set_xlabel('Steps (grouped by Phase)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Issues', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Issues Across Phases, Steps, and Strategies',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)

    # Add phase labels as text annotations near the top
    for phase in phase_order:
        positions = phase_positions[phase]
        if positions:
            center_x = np.mean(positions)
            # Add "Phase " prefix for clarity unless it's "unspecific"
            phase_label = f"Phase {phase}" if phase != 'unspecific' else phase
            ax.text(center_x, 0.97, phase_label, transform=ax.get_xaxis_transform(),
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
    print(f"\nIssues by Phase, Step, and Strategy:")
    for phase in phase_order:
        phase_total = sum(sum(strategies.values()) for strategies in hierarchy[phase].values())
        print(f"\nPhase {phase if phase != 'unspecific' else 'unspecific'}: {phase_total} issues")

        # Sort steps for this phase
        steps = sorted(hierarchy[phase].keys(), key=lambda x: (
            x == 'unspecific', x if isinstance(x, (int, float)) else 0
        ))

        for step in steps:
            step_total = sum(hierarchy[phase][step].values())
            print(f"  Step {step if step != 'unspecific' else 'unspecific'}: {step_total} issues")

            # Sort strategies for this step
            strategies = sorted(hierarchy[phase][step].keys(), key=lambda x: (
                x == 'unspecific', x if isinstance(x, (int, float)) else 0
            ))

            for strategy in strategies:
                count = hierarchy[phase][step][strategy]
                print(f"    Strategy {strategy if strategy != 'unspecific' else 'unspecific'}: {count} issues")

    plt.close()
