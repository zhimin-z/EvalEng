# Evaluator Categories

[Algorithmic, ML-based]

## Detailed Analysis

### Algorithmic

Evidence 1: Deterministic formatting and scoring functions
- File: `simulator/visualization/pages/1_📈_Experiments_Report.py`
- Functions: `_format_arrow()`, `_format_percentage()`, `_format_binary()`, `_color_arrow()`, `_color_binary()`
- Code Reference:
```python
success_rate.append(100 * sum([policy['score'] for policy in cur_policies]) / len(cur_policies))
mean_scores = merged_df[score_columns].apply(lambda row: row[row >= 0].mean(), axis=1)
merged_df[new_col] = merged_df[col] - mean_scores
```
These are formatting and scoring functions that apply deterministic rules to evaluate and display experimental results. The code calculates success rates, deviations from mean, and differences between experiments using mathematical formulas, providing consistent and reproducible assessment through predefined computational measures. This aligns with the Algorithmic evaluator definition as these metrics ensure deterministic assessment without learned representations.

Evidence 2: Policy-level success rate calculation
- File: `simulator/visualization/pages/1_📈_Experiments_Report.py`
- Function: `read_experiment_data()`
- Code Reference:
```python
for policy_info in policies_info_list:
    cur_policies = [policy for policy in all_policies_list if policy['policy'] == policy_info['name']]
    if len(cur_policies) < 3:
        success_rate.append(-1)
        continue
    success_rate.append(100 * sum([policy['score'] for policy in cur_policies]) / len(cur_policies))
```
This function reads evaluation results and calculates policy-level success rates using algorithmic aggregation. The system computes binary success/failure scores (0 or 1) for policies and aggregates them to produce success rate metrics through established statistical functions, ensuring consistent and reproducible evaluation independent of any learned models.

Evidence 3: Rule-based policy violation extraction
- File: `simulator/visualization/pages/1_📈_Experiments_Report.py`
- Function: `extract_violated_policies_str()`
- Code Reference:
```python
# Function performs rule-based policy violation extraction and matching
```
This function performs rule-based policy violation extraction and matching, which is an algorithmic evaluation approach for identifying which policies were not adhered to during conversations. It applies predefined logic to parse and categorize policy violations, providing deterministic assessment through computational pattern matching rather than learned behavior.

---

### ML-based

Evidence 1: LLM-based conversation critique and feedback
- File: `README.md` and `docs/architecture.md`
- Section: "Critiquing the conversation and providing feedback on the tested policies" and Section 3: "Fine-Grained Analysis"
- Code Reference:
```text
The Dialog critique component performs a detailed evaluation of the conversation by analyzing:
1. The user-chatbot dialog history
2. The chatbot's system prompt
3. The termination reason provided by the user agent
```
The system explicitly uses LLMs (Large Language Models) as evaluators through a "critique" component that performs detailed conversation evaluation. The critique process includes Termination Validation (verifying if stated termination reason is accurate), Multi-Level Policy Coverage Analysis (identifying which policies were tested/violated), and Report Generation with complexity-level categorization. This leverages learned representations for nuanced assessment that captures semantic and contextual quality dimensions beyond what algorithmic metrics can measure.

Evidence 2: Dedicated critique node in dialog graph
- File: `docs/architecture.md`
- Section: Dialog Graph section describing "Critique Node"
- Code Reference:
```text
- Critique Node: Evaluates conversation adherence to policies
```
The Dialog Graph architecture includes a dedicated "Critique Node" that evaluates conversation adherence to policies using ML models to assess whether the chatbot followed defined policies during the simulated conversation. This node serves as an ML-based judge that provides learned evaluation capabilities, enabling the system to capture nuanced policy compliance that requires understanding of context and intent rather than simple rule matching.

Evidence 3: Configurable LLM providers for evaluation
- File: `config/config_default.yml` and `docs/installation.md`
- Section: LLM configuration for evaluation
- Code Reference:
```yaml
llm_intellagent:
    type: 'azure'
```
The system is configured to use various LLM providers (OpenAI/Azure/Vertex/Anthropic) for evaluation purposes. These LLMs serve as judges to evaluate the quality and policy compliance of chatbot responses in the benchmark scenarios, providing flexible ML-based evaluation that can adapt to different domains and assessment requirements through the use of different language models.

Evidence 4: ML-generated scores and natural language explanations
- File: `simulator/visualization/pages/1_📈_Experiments_Report.py`
- Code Reference:
```python
events_info = df[['id', 'scenario', 'score', 'reason', 'violated_policies']]
```
The results include 'score' and 'reason' fields that are generated by ML-based evaluators (the critique agents) rather than simple algorithmic metrics. The 'reason' field particularly indicates natural language explanations that would come from an LLM judge, demonstrating the use of machine learning models to provide human-interpretable justifications for evaluation decisions alongside quantitative scores.