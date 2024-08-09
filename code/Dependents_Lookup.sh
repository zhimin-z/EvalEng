#! /bin/sh

curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o src
chmod +x src

src search -json "context:global /import alpaca_eval|from alpaca_eval.* import / select:repo count:all patterntype:standard" > "AlpacaEval.json" 
src search -json "context:global /import bigcode_eval|from bigcode_eval.* import / select:repo count:all patterntype:standard" > "Code Generation LM Evaluation Harness.json" 
src search -json "context:global /import evalai|from evalai.* import / select:repo count:all patterntype:standard" > "EvalAI.json" 
src search -json "context:global /import evalplus|from evalplus.* import / select:repo count:all patterntype:standard" > "EvalPlus.json" 
src search -json "context:global /import evals|from evals.* import / select:repo count:all patterntype:standard" > "Evals.json" 

src search -json "context:global /import lm_eval|from lm_eval.* import / select:repo count:all patterntype:standard" > "Language Model Evaluation Harness.json" 
src search -json "context:global /import flageval.serving|from flageval.serving.* import / select:repo count:all patterntype:standard" > "FlagEval.json" 
src search -json "context:global /import trustllm|from trustllm.* import / select:repo count:all patterntype:standard" > "TrustLLM.json" 
src search -json "context:global /import overcooked_ai_py|from overcooked_ai_py.* import / select:repo count:all patterntype:standard" > "Overcooked-AI.json" 
src search -json "context:global /import inspect_ai|from inspect_ai.* import / select:repo count:all patterntype:standard" > "Inspect.json" 
src search -json "context:global /import evalverse|from evalverse.* import / select:repo count:all patterntype:standard" > "Evalverse.json" 
src search -json "context:global /import vbench|from vbench.* import / select:repo count:all patterntype:standard" > "VBench.json" 
src search -json "context:global /import rewardbench|from rewardbench.* import / select:repo count:all patterntype:standard" > "RewardBench.json" 
src search -json "context:global /import lighteval|from lighteval.* import / select:repo count:all patterntype:standard" > "LightEval.json" 
src search -json "context:global /import optimum_benchmark|from optimum_benchmark.* import / select:repo count:all patterntype:standard" > "Optimum-Benchmark.json" 
src search -json "context:global /import promptbench|from promptbench.* import / select:repo count:all patterntype:standard" > "PromptBench.json" 
src search -json "context:global /import vlmeval|from vlmeval.* import / select:repo count:all patterntype:standard" > "VLMEvalKit.json" 
src search -json "context:global /import intercode|from intercode.* import / select:repo count:all patterntype:standard" > "InterCode.json" 
src search -json "context:global /import prometheus_eval|from prometheus_eval.* import / select:repo count:all patterntype:standard" > "Prometheus-Eval.json" 
src search -json "context:global /import llmperf|from llmperf.* import / select:repo count:all patterntype:standard" > "LLMPerf.json" 



github-dependents-info --repo confident-ai/deepeval -p -j > "DeepEval.json"
github-dependents-info --repo embeddings-benchmark/mteb -p -j > "Massive Text Embedding Benchmark.json"
github-dependents-info --repo evidentlyai/evidently -p -j > "Evidently.json"
github-dependents-info --repo explodinggradients/ragas -p -j > "Ragas.json"
github-dependents-info --repo huggingface/evaluate -p -j > "Evaluate.json"