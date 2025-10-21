# CipherChat - Stage 1 (CONFIGURE) Evaluation

## Summary
CipherChat is a research framework for testing LLM safety alignment through cipher-based attacks, not a general-purpose evaluation framework. It has minimal configuration capabilities, as it's designed for a specific adversarial testing methodology. Configuration is primarily hardcoded in Python scripts with limited abstraction or declarative setup.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 1 | Evidence: Single hardcoded dataset loaded via `torch.load("data/data_en_zh.dict")` (main.py:16). No dataset abstraction layer, no support for multiple sources, no schema definition, no versioning. Splits are handled programmatically through array slicing `samples[:args.debug_num]` (main.py:75) with no declarative configuration. The data structure appears to be a simple dictionary with no formal schema validation. |
| S1F2: Model Configuration | 1 | Evidence: Only OpenAI models supported via hardcoded API key `OPENAI_API_KEY = ""` (main.py:14). Model selection through command-line argument with hardcoded list (main.py:65-67). No unified provider abstraction - direct API calls in `query_function()` with conditional logic for different model types (main.py:29-47). No support for local models, HuggingFace, or other providers. Authentication is environment variable only with no rotation or vault integration. |
| S1F3: Prompt Configuration | 2 | Evidence: Has basic prompt templating via string formatting in `prompts_and_demonstrations.py` with system role prompts (lines 3-48) and demonstration dictionaries (lines 115-400+). Supports variable substitution through Python string formatting: `"Example {}\n".format(i) + expert.encode(demon)` (main.py:93). Few-shot examples are configurable via demonstrations (main.py:88-93), but limited to 3 hardcoded examples `[:3]`. No Jinja2 or formal templating engine, no prompt versioning system. Parameters like temperature are configurable via args (main.py:62, 31) but no validation against model capabilities. |
| S1F4: Environment Setup | 1 | Evidence: No requirements.txt, setup.py, or pyproject.toml visible in repository structure. No Dockerfile or container configuration. Dependencies must be inferred from imports (openai, torch, logging, argparse, tqdm). Manual setup required. README provides no installation instructions - only usage example (README.md:24-31). No virtual environment management or hardware configuration specification. |
| S1F5: Security & Access | 0 | Evidence: API key stored as plaintext variable in code: `OPENAI_API_KEY = ""` (main.py:14) with comment "you should write your api key here". No environment variable handling, no vault integration, no encryption at rest. No RBAC, no user/group system, no audit logging of credential access. Complete absence of security features beyond basic error handling for quota exceptions (main.py:60). |
| S1F6: Cost Estimation | 0 | Evidence: No cost estimation functionality present. Only a hardcoded `wait_time = 20` for rate limiting (main.py:15). No token counting, no API call projection, no budget limits or cost modeling. The framework logs conversations but provides no cost analysis or optimization suggestions. No awareness of pricing models for different providers. |

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration (Rating: 1)
The framework loads a single dataset file directly:
```python
da = torch.load("data/data_en_zh.dict")  # main.py:16
```

Dataset selection is via command-line argument with limited options:
```python
parser.add_argument("--data_path", type=str, default=["data/data_en_zh.dict", ][0])
parser.add_argument("--instruction_type", type=str, 
    default=["Crimes_And_Illegal_Activities", "Ethics_And_Morality", ...][0])
parser.add_argument("--language", type=str, default=["zh", "en"][-1])
```

No schema validation, no multi-source support, no versioning. This is minimal dataset handling suitable only for this specific research purpose.

### S1F2: Model and Backend Configuration (Rating: 1)
Model configuration is primitive with hardcoded provider support:
```python
model_name = args.model_name  # main.py:59
# Only OpenAI models in default list
default=["gpt-3.5-turbo-0613", "gpt-4-0613", "text-davinci-003", ...]
```

The `query_function` has conditional logic but no abstraction:
```python
if "text-" in model_name:  # Old completion API
    chat_completion = openai.Completion.create(...)
else:  # Chat API
    chat_completion = openai.ChatCompletion.create(...)
```

No provider abstraction layer, no support for non-OpenAI providers.

### S1F3: Prompt Configuration (Rating: 2)
Has structured prompt configuration via dictionaries and basic templating:
```python
system_role_propmts = {
    "baseline": "You are ChatGPT...",
    "caesar": 'You are an expert on The Caesar Cipher...',
    # Multiple cipher types defined
}
```

Supports few-shot demonstrations:
```python
demonstrations = demonstration_dict[args.instruction_type][demonstration_type][:3]
for i, demon in enumerate(demonstrations):
    encode_demonstrations += "Example {}\n".format(i) + expert.encode(demon) + "\n"
```

However, no formal templating engine, no versioning, limited to string formatting.

### S1F4: Environment Setup (Rating: 1)
README shows only usage, no setup:
```markdown
## 🛠️ Usage
✨An example run:
python3 main.py \
 --model_name gpt-4-0613 \
 --data_path data/data_en_zh.dict \
```

No dependency management files, no containerization, manual configuration required.

### S1F5: Security and Access Control (Rating: 0)
Plaintext credential storage with no security features:
```python
OPENAI_API_KEY = ""    # you should write your api key here
```

This is a critical security anti-pattern with no mitigation strategies present.

### S1F6: Cost Estimation and Budget Planning (Rating: 0)
Only basic rate limiting present:
```python
wait_time = 20    # to avoid the rate limitation of OpenAI api
time.sleep(wait_time)
```

No cost modeling, token estimation, or budget controls. The framework tracks toxic detection calls but not their costs.

## Summary Assessment

Overall Stage 1 Score: 5/18 (27.8%)

CipherChat is a specialized research tool, not a general-purpose evaluation framework. Its configuration capabilities are minimal and purpose-built for cipher-based adversarial testing. The framework:

- ✅ Works for its intended research purpose
- ❌ Lacks general dataset/model abstractions
- ❌ Has no security considerations
- ❌ Provides no cost management
- ❌ Requires significant manual configuration

Recommendation: This is not suitable as a general evaluation framework. It serves as a proof-of-concept for a specific research paper on LLM safety vulnerabilities through cipher attacks. Organizations needing robust evaluation capabilities should look elsewhere.