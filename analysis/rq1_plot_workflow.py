import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
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
        'name': 'Stage 0:\nProvisioning (56)',
        'summary': 'Establishing & authenticating\nevaluation infrastructure',
        'x': 2,
        'width': 16,
        'color_key': 'Provisioning',
        'steps': [
            {
                'name': 'Step A:\nHarness Installation (56)',
                'strategies': [
                    'Strategy 1:\nGit Clone (56)\n(Source installation)',
                    'Strategy 2:\nPython Package (53)\n(Pip/Conda/Poetry)',
                    'Strategy 3:\nNode Package (1)\n(NPM/NPX)',
                    'Strategy 4:\nBinary Package (2)\n(Standalone executables)',
                    'Strategy 5:\nContainer Image (12)\n(Docker/OCI)'
                ]
            },
            {
                'name': 'Step B:\nCredential Configuration (47)',
                'strategies': [
                    'Strategy 1:\nModel API Authentication (38)\n(Remote keys)',
                    'Strategy 2:\nRepository Authentication (42)\n(Hub/Registry access)',
                    'Strategy 3:\nEvaluation Platform Authentication (10)\n(Service login)'
                ]
            }
        ]
    },
    {
        'name': 'Stage I:\nSpecification (56)',
        'summary': 'Defining SUT & benchmark configuration',
        'x': 20,
        'width': 16,
        'color_key': 'Specification',
        'steps': [
            {
                'name': 'Step A:\nSUT Preparation (53)',
                'strategies': [
                    'Strategy 1:\nModel-as-a-Service (39)\n(Remote Inference)',
                    'Strategy 2:\nModel-in-Process (43)\n(Local Inference)',
                    'Strategy 3:\nNon-Parametric Algorithm (8)\n(Deterministic)',
                    'Strategy 4:\nInteractive Agent (15)\n(Sequential Decision-Making)'
                ]
            },
            {
                'name': 'Step B:\nBenchmark Preparation (53)\n(Inputs)',
                'strategies': [
                    'Strategy 1:\nBenchmark Data Preparation (51)\n(Offline/Static)',
                    'Strategy 2:\nSynthetic Data Generation (23)\n(Generative)',
                    'Strategy 3:\nSimulation Environment Setup (8)\n(Interactive/3D)',
                    'Strategy 4:\nProduction Traffic Sampling (4)\n(Online/Live)'
                ]
            },
            {
                'name': 'Step C:\nBenchmark Preparation (53)\n(References)',
                'strategies': [
                    'Strategy 1:\nGround Truth Preparation (51)\n(Annotations/Indexes)',
                    'Strategy 2:\nJudge Preparation (34)\n(Model-based evaluators)'
                ]
            }
        ]
    },
    {
        'name': 'Stage II:\nExecution (53)',
        'summary': 'Running SUT with benchmark inputs',
        'x': 38,
        'width': 16,
        'color_key': 'Execution',
        'steps': [
            {
                'name': 'Step A:\nSUT Invocation (53)',
                'strategies': [
                    'Strategy 1:\nBatch Inference (53)\n(Standard completion)',
                    'Strategy 2:\nArena Battle (7)\n(Side-by-side comparison)',
                    'Strategy 3:\nInteractive Loop (17)\n(Stateful/Agentic)',
                    'Strategy 4:\nProduction Streaming (4)\n(Real-time monitoring)'
                ]
            }
        ]
    },
    {
        'name': 'Stage III:\nAssessment (56)',
        'summary': 'Computing metrics from\nSUT outputs & references',
        'x': 56,
        'width': 16,
        'color_key': 'Assessment',
        'steps': [
            {
                'name': 'Step A:\nIndividual Scoring (56)',
                'strategies': [
                    'Strategy 1:\nDeterministic Measurement (50)\n(Exact match/Distance)',
                    'Strategy 2:\nLatent Measurement (27)\n(Embedding similarity)',
                    'Strategy 3:\nSubjective Measurement (33)\n(LLM-as-a-Judge)',
                    'Strategy 4:\nPerformance Measurement (21)\n(Latency/Cost/Efficiency)'
                ]
            },
            {
                'name': 'Step B:\nAggregate Scoring (54)',
                'strategies': [
                    'Strategy 1:\nDistributional Statistics (54)\n(Averages/Ranks)',
                    'Strategy 2:\nUncertainty Quantification (13)\n(Confidence intervals/PPI)'
                ]
            }
        ]
    },
    {
        'name': 'Stage IV:\nReporting (46)',
        'summary': 'Visualizing & communicating\nevaluation results',
        'x': 74,
        'width': 16,
        'color_key': 'Reporting',
        'steps': [
            {
                'name': 'Step A:\nInsight Presentation (46)',
                'strategies': [
                    'Strategy 1:\nExecution Tracing (18)\n(Trace logs/Trajectories)',
                    'Strategy 2:\nSubgroup Analysis (22)\n(Slicing/Demographics)',
                    'Strategy 3:\nRegression Alerting (5)\n(Historical comparison)',
                    'Strategy 4:\nChart Generation (25)\n(Radar/Trend plots)',
                    'Strategy 5:\nDashboard Creation (25)\n(Interactive UIs)',
                    'Strategy 6:\nLeaderboard Publication (22)\n(Public/Private ranking)'
                ]
            }
        ]
    }
]

# Draw stages containing all their steps
stage_boxes = []  # Store stage box positions for later arrow drawing
y_start = 96
stage_header_height = 6.5  # Reduced since subtitle was removed
strategy_height = 2.8  # Height of each strategy box
strategy_spacing = 0.5  # Vertical gap between strategy boxes
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
    ax.text(stage['x'] + stage['width']/2, y_start - 2,
            stage['name'],
            ha='center', va='center', fontsize=18, weight='bold',
            zorder=5)

    # Stage summary
    ax.text(stage['x'] + stage['width']/2, y_start - 5,
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
        ax.text(stage['x'] + stage['width']/2, y_pos - 1.8,
                step['name'],
                ha='center', va='center', fontsize=13, weight='bold',
                zorder=5)

        y_strat = y_pos - step_header_height

        # Draw strategies
        for i, strategy in enumerate(step['strategies']):
            # Strategy boxes inside step box
            strategy_x_margin = step_x_margin + 1  # Additional margin inside step box
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