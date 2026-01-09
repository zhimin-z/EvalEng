import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set up the figure
fig, ax = plt.subplots(figsize=(24, 14))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title removed per user request

# Color scheme for stages
stage_colors = {
    'Provisioning': {'bg': '#E8F4F8', 'border': '#1E88E5', 'step': '#B3E5FC', 'strategy': '#E1F5FE'},
    'Specification': {'bg': '#E8F5E9', 'border': '#43A047', 'step': '#C8E6C9', 'strategy': '#E8F5E9'},
    'Execution': {'bg': '#FFF3E0', 'border': '#FB8C00', 'step': '#FFE0B2', 'strategy': '#FFF3E0'},
    'Assessment': {'bg': '#F3E5F5', 'border': '#8E24AA', 'step': '#E1BEE7', 'strategy': '#F3E5F5'},
    'Reporting': {'bg': '#FCE4EC', 'border': '#C2185B', 'step': '#F8BBD0', 'strategy': '#FCE4EC'}
}

# Stage definitions with data
stages = [
    {
        'name': 'Stage 0: Provisioning',
        'subtitle': '(The Runtime)',
        'summary': 'Establishing & authenticating\nevaluation infrastructure',
        'x': 2,
        'width': 16,
        'color_key': 'Provisioning',
        'steps': [
            {
                'name': 'Step A: Harness Installation',
                'strategies': [
                    'Strategy 1: Git Clone\n(Source installation)',
                    'Strategy 2: Python Package\n(Pip/Conda/Poetry)',
                    'Strategy 3: Node Package\n(NPM/NPX)',
                    'Strategy 4: Binary Package\n(Standalone executables)',
                    'Strategy 5: Container Image\n(Docker/OCI)'
                ]
            },
            {
                'name': 'Step B: Credential Configuration',
                'strategies': [
                    'Strategy 1: Model API Authentication\n(Remote keys)',
                    'Strategy 2: Repository Authentication\n(Hub/Registry access)',
                    'Strategy 3: Evaluation Platform Authentication\n(Service login)'
                ]
            }
        ]
    },
    {
        'name': 'Stage I: Specification',
        'subtitle': '(The Contract)',
        'summary': 'Defining SUT & benchmark configuration',
        'x': 20,
        'width': 16,
        'color_key': 'Specification',
        'steps': [
            {
                'name': 'Step A: SUT Preparation',
                'strategies': [
                    'Strategy 1: Model-as-a-Service\n(Remote Inference)',
                    'Strategy 2: Model-in-Process\n(Local Inference)',
                    'Strategy 3: Non-Parametric Algorithm\n(Deterministic)',
                    'Strategy 4: Interactive Agent\n(Sequential Decision-Making)'
                ]
            },
            {
                'name': 'Step B: Benchmark Preparation\n(Inputs)',
                'strategies': [
                    'Strategy 1: Benchmark Data Preparation\n(Offline/Static)',
                    'Strategy 2: Synthetic Data Generation\n(Generative)',
                    'Strategy 3: Simulation Environment Setup\n(Interactive/3D)',
                    'Strategy 4: Production Traffic Sampling\n(Online/Live)'
                ]
            },
            {
                'name': 'Step C: Benchmark Preparation\n(References)',
                'strategies': [
                    'Strategy 1: Ground Truth Preparation\n(Annotations/Indexes)',
                    'Strategy 2: Judge Preparation\n(Model-based evaluators)'
                ]
            }
        ]
    },
    {
        'name': 'Stage II: Execution',
        'subtitle': '(The Run)',
        'summary': 'Running SUT with benchmark inputs',
        'x': 38,
        'width': 16,
        'color_key': 'Execution',
        'steps': [
            {
                'name': 'Step A: SUT Invocation',
                'strategies': [
                    'Strategy 1: Batch Inference\n(Standard completion)',
                    'Strategy 2: Arena Battle\n(Side-by-side comparison)',
                    'Strategy 3: Interactive Loop\n(Stateful/Agentic)',
                    'Strategy 4: Production Streaming\n(Real-time monitoring)'
                ]
            }
        ]
    },
    {
        'name': 'Stage III: Assessment',
        'subtitle': '(The Score)',
        'summary': 'Computing metrics from\nSUT outputs & references',
        'x': 56,
        'width': 16,
        'color_key': 'Assessment',
        'steps': [
            {
                'name': 'Step A: Individual Scoring',
                'strategies': [
                    'Strategy 1: Deterministic Measurement\n(Exact match/Distance)',
                    'Strategy 2: Latent Measurement\n(Embedding similarity)',
                    'Strategy 3: Subjective Measurement\n(LLM-as-a-Judge)',
                    'Strategy 4: Performance Measurement\n(Latency/Cost/Efficiency)'
                ]
            },
            {
                'name': 'Step B: Aggregate Scoring',
                'strategies': [
                    'Strategy 1: Distributional Statistics\n(Averages/Ranks)',
                    'Strategy 2: Uncertainty Quantification\n(Confidence intervals/PPI)'
                ]
            }
        ]
    },
    {
        'name': 'Stage IV: Reporting',
        'subtitle': '(The Output)',
        'summary': 'Visualizing & communicating\nevaluation results',
        'x': 74,
        'width': 16,
        'color_key': 'Reporting',
        'steps': [
            {
                'name': 'Step A: Insight Presentation',
                'strategies': [
                    'Strategy 1: Execution Tracing\n(Trace logs/Trajectories)',
                    'Strategy 2: Subgroup Analysis\n(Slicing/Demographics)',
                    'Strategy 3: Regression Alerting\n(Historical comparison)',
                    'Strategy 4: Chart Generation\n(Radar/Trend plots)',
                    'Strategy 5: Dashboard Creation\n(Interactive UIs)',
                    'Strategy 6: Leaderboard Publication\n(Public/Private ranking)'
                ]
            }
        ]
    }
]

# Draw stages containing all their steps
stage_boxes = []  # Store stage box positions for later arrow drawing
y_start = 96
stage_header_height = 9
strategy_height = 4.0  # Increased for better text visibility
step_header_height = 3.5
box_margin = 0.75  # Horizontal margin for step boxes from stage edge
step_spacing = 1.2  # Vertical gap between steps (larger than horizontal)

for stage in stages:
    colors = stage_colors[stage['color_key']]

    # Calculate total height needed for this stage (header + all steps)
    total_strategies = sum(len(step['strategies']) for step in stage['steps'])
    total_steps = len(stage['steps'])
    step_vertical_padding = 0.3  # Must match the padding in step drawing
    bottom_gap = box_margin  # Gap between last step and stage bottom
    stage_content_height = (total_strategies * strategy_height +
                           total_steps * (step_header_height + step_vertical_padding) +
                           (total_steps - 1) * step_spacing +  # Gaps between steps
                           stage_header_height + bottom_gap)

    # Draw stage container that will contain all steps
    stage_box = FancyBboxPatch(
        (stage['x'], y_start - stage_content_height),
        stage['width'], stage_content_height,
        boxstyle="round,pad=0.2",
        facecolor=colors['bg'],
        edgecolor=colors['border'],
        linewidth=3,
        zorder=1
    )
    ax.add_patch(stage_box)

    # Stage name
    ax.text(stage['x'] + stage['width']/2, y_start - 2,
            stage['name'],
            ha='center', va='center', fontsize=18, weight='bold',
            zorder=5)

    # Stage subtitle
    ax.text(stage['x'] + stage['width']/2, y_start - 4,
            stage['subtitle'],
            ha='center', va='center', fontsize=14, style='italic',
            zorder=5)

    # Stage summary (one-liner)
    ax.text(stage['x'] + stage['width']/2, y_start - 6.5,
            stage['summary'],
            ha='center', va='center', fontsize=11,
            zorder=5, wrap=True)

    # Store stage box position for arrows
    stage_boxes.append({
        'x_left': stage['x'],  # Leftmost edge
        'x_right': stage['x'] + stage['width'],  # Rightmost edge
        'y': y_start - stage_content_height/2,  # Vertical center
        'stage': stage,
        'y_top': y_start,
        'y_bottom': y_start - stage_content_height
    })

# Draw steps inside each stage box
for stage_info in stage_boxes:
    stage = stage_info['stage']
    colors = stage_colors[stage['color_key']]

    # Start drawing steps below the stage header (with minimal gap)
    y_pos = stage_info['y_top'] - stage_header_height

    for step in stage['steps']:
        step_vertical_padding = 0.3  # Padding at bottom of step box
        step_height = len(step['strategies']) * strategy_height + step_header_height + step_vertical_padding

        # Step container - inside stage box
        step_x_margin = box_margin  # Margin from stage edge matches vertical spacing
        step_width = stage['width'] - 2 * step_x_margin
        step_box = FancyBboxPatch(
            (stage['x'] + step_x_margin, y_pos - step_height),
            step_width, step_height,
            boxstyle="round,pad=0.1",
            facecolor=colors['step'],
            edgecolor=colors['border'],
            linewidth=2,
            zorder=2
        )
        ax.add_patch(step_box)

        # Step header
        ax.text(stage['x'] + stage['width']/2, y_pos - 1.8,
                step['name'],
                ha='center', va='center', fontsize=13, weight='bold',
                zorder=5)

        y_strat = y_pos - step_header_height

        # Draw strategies
        for strategy in step['strategies']:
            # Strategy boxes inside step box
            strategy_x_margin = step_x_margin + 0.3  # Additional margin inside step box
            strategy_width = stage['width'] - 2 * strategy_x_margin
            strategy_box = FancyBboxPatch(
                (stage['x'] + strategy_x_margin, y_strat - strategy_height + 0.2),
                strategy_width, strategy_height - 0.4,
                boxstyle="round,pad=0.2",
                facecolor=colors['strategy'],
                edgecolor='gray',
                linewidth=1,
                zorder=3
            )
            ax.add_patch(strategy_box)

            ax.text(stage['x'] + stage['width']/2, y_strat - strategy_height/2,
                    strategy,
                    ha='center', va='center', fontsize=10,
                    zorder=5)

            y_strat -= strategy_height

        # Move y_pos to ensure consistent gap between step boxes
        # Gap should be from bottom of current step box to top of next step box
        y_pos = (y_pos - step_height) - step_spacing

# Draw horizontal arrows between stages at consistent height
# Position arrows at the top section of stage boxes
arrow_y = y_start - 4.5  # Fixed height for all arrows

for i in range(len(stage_boxes) - 1):
    start_x = stage_boxes[i]['x_right']
    end_x = stage_boxes[i + 1]['x_left']

    # Draw simple, straight arrow between stages
    arrow = FancyArrowPatch(
        (start_x, arrow_y),
        (end_x + 0.5, arrow_y),
        arrowstyle='-|>',  # Simple arrow style
        color='#1976D2',  # Vibrant blue
        linewidth=8,
        mutation_scale=30,  # Controls arrow head size
        alpha=0.7,
        zorder=10
    )
    ax.add_patch(arrow)

# Find the minimum y value (bottom of all stages) to adjust plot limits
min_y = min(box['y_bottom'] for box in stage_boxes)
ax.set_ylim(min_y - 2, y_start + 4)  # Add small padding top and bottom
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

output_path = "../figures/rq1_workflow.pdf"
plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='white')
print("Diagram generated successfully!")
print(f"File saved: {output_path}")