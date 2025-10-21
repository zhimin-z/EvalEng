# Evaluation Mode Categories

[Interactive Simulation]

## Detailed Analysis

### Interactive Simulation

Evidence 1: Multi-turn Dialog System with State Management
- File: `simulator/visualization/pages/1_📈_Experiments_Report.py`
- Functions: `read_experiment_data()`, `load_data()`
- Code Reference:
```python
df['violated_policies']  # Tracks policy violations across dialog turns
events_info = df[['id', 'scenario', 'score', 'reason', 'violated_policies']]  # Captures simulation outcomes
# Graph data showing 'scores' and 'challenge_level' over multiple events
```
This system tracks policy violations and scores across multiple dialog turns, demonstrating state evolution throughout the simulation. The tracking of violated policies and challenge levels indicates multi-step interaction where outcomes depend on the accumulated history of agent actions.

Evidence 2: Dialog Manager with Feedback Loops
- File: `docs/architecture.md`
- Code Reference:
```
Dialog Graph implements a state machine that manages the conversation flow between the simulated user and chatbot

State Management: Uses DialogState to track:
- User and chatbot message history
- User thoughts and reasoning
- Critique feedback
- Stop signals for conversation termination

Critique Node: Evaluates conversation adherence to policies
Feedback loops for model behavior, state transitions based on model actions, multi-step processes with model interaction
```
The Dialog Graph implements a complete state machine managing conversation flow with explicit feedback loops. The Critique Node evaluates ongoing conversations and provides feedback that influences subsequent dialog turns, creating the iterative interaction characteristic of simulation environments.

Evidence 3: Simulation Execution Pipeline
- File: `run.py`
- Function: `main()`
- Code Reference:
```python
executor = SimulatorExecutor(config, args.output_path)
executor.load_dataset(args.dataset)
executor.run_simulation(args.experiment)
```
The execution pipeline orchestrates complete simulation runs, managing the entire lifecycle from dataset loading through simulation execution. This structure supports extended multi-step interactions rather than single-pass evaluation.

Evidence 4: Event-Driven Simulation with User Agent Interaction
- File: `docs/architecture.md`
- Section: "Dialog Simulation Architecture"
- Code Reference:
```
Multi-step environment interaction with feedback loops and state evolution
- User agent receives event details and expected behaviors
- Conversation alternates between user and chatbot
- Critique agent evaluates responses against policies
- Conversation continues until success or policy violation
```
The architecture implements event-driven simulation where user agents interact with chatbots through alternating turns. The critique agent continuously evaluates responses, and conversations proceed until terminal conditions are met, demonstrating adaptive multi-step interaction.

Evidence 5: State Evolution and Memory Management
- File: `docs/architecture.md`
- Code Reference:
```
SQLite-based conversation storage (memory.db)
- Tracks tool calls and their outputs
- Maintains conversation history
- Flow Control: Manages message passing between participants
- Handles conversation termination conditions
```
Persistent state management through SQLite ensures conversation history and tool interactions are maintained across simulation steps. This memory system enables agents to make decisions based on accumulated context, supporting complex behavioral assessment over extended interactions.

Evidence 6: Policy-Based Simulation Environment
- File: `examples/airline/input/wiki.md`
- Code Reference:
```
Before taking any actions that update the booking database... must list the action details and obtain explicit user confirmation

Multi-step workflows:
- book flight
- modify flight
- cancel flight
- refund

State-dependent actions (pending vs. delivered orders)
```
The comprehensive policy framework defines multi-step workflows with state-dependent behavior requirements. These policies govern how the simulation environment responds to agent actions, creating realistic scenarios that test behavioral competence across complex interaction sequences.

Evidence 7: Results Tracking Across Simulation Episodes
- File: `simulator/visualization/pages/1_📈_Experiments_Report.py`
- Code Reference:
```python
for i, row in df.iterrows():
    policies = ast.literal_eval(row['policies'])
    policies_sublist = ast.literal_eval(row['policies_in_dialog'])
    violated_policies = ast.literal_eval(row['violated_policies'])
    for j in policies_sublist:
        score = 0 if j in violated_policies else 1
```
The system tracks outcomes across multiple simulation episodes, evaluating which policies were followed or violated during each dialog. This scoring mechanism assesses behavioral competence by analyzing the cumulative results of multi-turn interactions.

Evidence 8: Multi-Agent Simulation Architecture
- File: `docs/architecture.md`
- Section: "Dialog Simulation"
- Code Reference:
```
Three interacting agents in simulation:
- User Node: Simulates user responses and tracks reasoning
- Chatbot Node: Handles chatbot responses and tool interactions
- Critique Node: Evaluates conversation adherence to policies

Feedback loop:
User agent receives event details and expected behaviors
→ Conversation alternates between user and chatbot
→ Critique agent evaluates responses against policies
```
The multi-agent architecture creates a complete simulation ecosystem where three distinct agents interact over multiple steps. Each agent's output influences subsequent interactions, with the critique agent providing continuous evaluation that shapes conversation flow, demonstrating the feedback loops and state evolution characteristic of interactive simulation.