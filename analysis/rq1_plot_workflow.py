import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set up the figure
fig, ax = plt.subplots(figsize=(20, 10))
ax.set_xlim(0, 100)  # Stages span x=1 to x=99 with 1-unit margins on each side
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
        'name': 'Stage 0:\nProvisioning (57)',
        'summary': 'Establishing & authenticating\nevaluation infrastructure',
        'x': 1,
        'width': 18,
        'color_key': 'Provisioning',
        'steps': [
            {
                'name': 'Step A:\nHarness Installation (57)',
                'strategies': [
                    'Strategy 1:\nGit Clone (57)\n(Source installation)',
                    'Strategy 2:\nPython Package (54)\n(Pip/Conda/Poetry)',
                    'Strategy 3:\nContainer Image (12)\n(Docker/OCI)',
                    'Strategy 4:\nBinary Package (2)\n(Standalone executables)',
                    'Strategy 5:\nNode Package (1)\n(NPM/NPX)',
                ]
            },
            {
                'name': 'Step B:\nCredential Configuration (48)',
                'strategies': [
                    'Strategy 1:\nRepository Authentication (43)\n(Hub/Registry access)',
                    'Strategy 2:\nModel API Authentication (39)\n(Remote keys)',
                    'Strategy 3:\nEvaluation Platform Authentication (11)\n(Service login)'
                ]
            }
        ]
    },
    {
        'name': 'Stage 1:\nSpecification (57)',
        'summary': 'Defining SUT & benchmark configuration',
        'x': 21,
        'width': 18,
        'color_key': 'Specification',
        'steps': [
            {
                'name': 'Step A:\nSUT Preparation (54)',
                'strategies': [
                    'Strategy 1:\nModel-in-Process (44)\n(Local Inference)',
                    'Strategy 2:\nModel-as-a-Service (40)\n(Remote Inference)',
                    'Strategy 3:\nInteractive Agent (16)\n(Sequential Decision-Making)',
                    'Strategy 4:\nNon-Parametric Algorithm (8)\n(Deterministic)',
                ]
            },
            {
                'name': 'Step B:\nBenchmark Inputs\n Preparation (54)',
                'strategies': [
                    'Strategy 1:\nBenchmark Data Preparation (52)\n(Offline/Static)',
                    'Strategy 2:\nSynthetic Data Generation (23)\n(Generative)',
                    'Strategy 3:\nSimulation Environment Setup (8)\n(Interactive/3D)',
                    'Strategy 4:\nProduction Traffic Sampling (4)\n(Online/Live)'
                ]
            },
            {
                'name': 'Step C:\nBenchmark References\n Preparation (54)',
                'strategies': [
                    'Strategy 1:\nGround Truth Preparation (52)\n(Annotations/Indexes)',
                    'Strategy 2:\nJudge Preparation (35)\n(Model-based evaluators)'
                ]
            }
        ]
    },
    {
        'name': 'Stage 2:\nExecution (54)',
        'summary': 'Running SUT with benchmark inputs',
        'x': 41,
        'width': 18,
        'color_key': 'Execution',
        'steps': [
            {
                'name': 'Step A:\nSUT Invocation (54)',
                'strategies': [
                    'Strategy 1:\nBatch Inference (54)\n(Standard completion)',
                    'Strategy 2:\nInteractive Loop (18)\n(Stateful/Agentic)',
                    'Strategy 3:\nArena Battle (7)\n(Side-by-side comparison)',
                    'Strategy 4:\nProduction Streaming (4)\n(Real-time monitoring)'
                ]
            }
        ]
    },
    {
        'name': 'Stage 3:\nAssessment (57)',
        'summary': 'Computing metrics from\nSUT outputs & references',
        'x': 61,
        'width': 18,
        'color_key': 'Assessment',
        'steps': [
            {
                'name': 'Step A:\nIndividual Scoring (57)',
                'strategies': [
                    'Strategy 1:\nDeterministic Measurement (51)\n(Exact match/Distance)',
                    'Strategy 2:\nSubjective Measurement (34)\n(LLM-as-a-Judge)',
                    'Strategy 3:\nLatent Measurement (28)\n(Embedding similarity)',
                    'Strategy 4:\nPerformance Measurement (22)\n(Latency/Cost/Efficiency)'
                ]
            },
            {
                'name': 'Step B:\nAggregate Scoring (55)',
                'strategies': [
                    'Strategy 1:\nDistributional Statistics (55)\n(Averages/Ranks)',
                    'Strategy 2:\nUncertainty Quantification (13)\n(Confidence intervals/PPI)'
                ]
            }
        ]
    },
    {
        'name': 'Stage 4:\nReporting (47)',
        'summary': 'Visualizing & communicating\nevaluation results',
        'x': 81,
        'width': 18,
        'color_key': 'Reporting',
        'steps': [
            {
                'name': 'Step A:\nInsight Presentation (47)',
                'strategies': [
                    'Strategy 1:\nChart Generation (25)\n(Radar/Trend plots)',
                    'Strategy 2:\nDashboard Creation (26)\n(Interactive UIs)',
                    'Strategy 3:\nLeaderboard Publication (23)\n(Public/Private ranking)',
                    'Strategy 4:\nSubgroup Analysis (23)\n(Slicing/Demographics)',
                    'Strategy 5:\nExecution Tracing (19)\n(Trace logs/Trajectories)',
                    'Strategy 6:\nRegression Alerting (5)\n(Historical comparison)',
                ]
            }
        ]
    }
]

# Draw stages containing all their steps
stage_boxes = []  # Store stage box positions for later arrow drawing
y_start = 96
stage_header_height = 9.5  # Enlarged for larger stage fonts
strategy_height = 4.5  # Height of each strategy box (enlarged for 11pt text)
strategy_spacing = 0.8  # Vertical gap between strategy boxes
step_header_height = 5.5  # Enlarged for larger step fonts
box_margin = 0.8  # Horizontal margin for step boxes from stage edge
step_spacing = 1.8  # Vertical gap between steps (larger than horizontal)

for stage in stages:
    colors = stage_colors[stage['color_key']]

    # Calculate total height needed for this stage (header + all steps)
    total_strategies = sum(len(step['strategies']) for step in stage['steps'])
    total_steps = len(stage['steps'])
    step_vertical_padding = 0.6  # Must match the padding in step drawing
    bottom_gap = box_margin  # Gap between last step and stage bottom
    # Count gaps between strategies within each step
    total_strategy_gaps = sum(max(0, len(step['strategies']) - 1) for step in stage['steps'])
    stage_content_height = (total_strategies * strategy_height +
                           total_strategy_gaps * strategy_spacing +  # Gaps between strategies
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
    ax.text(stage['x'] + stage['width']/2, y_start - 3,
            stage['name'],
            ha='center', va='center', fontsize=20, weight='bold',
            zorder=5)

    # Stage summary
    ax.text(stage['x'] + stage['width']/2, y_start - 7,
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
        step_vertical_padding = 0.6  # Padding at bottom of step box
        num_strategies = len(step['strategies'])
        strategy_gaps = max(0, num_strategies - 1)  # Gaps between strategies
        step_height = (num_strategies * strategy_height +
                      strategy_gaps * strategy_spacing +
                      step_header_height + step_vertical_padding)

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
        ax.text(stage['x'] + stage['width']/2, y_pos - 2.7,
                step['name'],
                ha='center', va='center', fontsize=12, weight='bold',
                zorder=5)

        y_strat = y_pos - step_header_height

        # Draw strategies
        for i, strategy in enumerate(step['strategies']):
            # Strategy boxes inside step box
            strategy_x_margin = step_x_margin + box_margin  # Additional margin inside step box (same as stage-to-step gap)
            strategy_width = stage['width'] - 2 * strategy_x_margin
            strategy_box = FancyBboxPatch(
                (stage['x'] + strategy_x_margin, y_strat - strategy_height),
                strategy_width, strategy_height,
                boxstyle="round,pad=0.05",
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

            # Move down by strategy height plus spacing (except for the last strategy)
            y_strat -= strategy_height
            if i < len(step['strategies']) - 1:  # Add spacing only between strategies
                y_strat -= strategy_spacing

        # Move y_pos to ensure consistent gap between step boxes
        # Gap should be from bottom of current step box to top of next step box
        y_pos = (y_pos - step_height) - step_spacing

# Draw horizontal arrows between stages at consistent height
# Position arrows at the top section of stage boxes
arrow_y = y_start - 6.5  # Fixed height for all arrows

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
max_x = max(box['x_right'] for box in stage_boxes)
min_x = min(box['x_left'] for box in stage_boxes)
ax.set_xlim(min_x - 0.5, max_x + 0.5)  # Tight horizontal margins
ax.set_ylim(min_y - 0.5, y_start + 0.5)  # Tight vertical margins
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

output_path = os.path.join(os.path.dirname(__file__), "../figures/rq1_workflow.pdf")
plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='white')
print(f"File saved: {output_path}")