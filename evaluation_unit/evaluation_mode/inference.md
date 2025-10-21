## Evaluation Mode Categories

[Static Analysis, Dynamic Execution]

## Detailed Analysis

### Static Analysis

Evidence 1: Text-to-Image FID Score Calculation
- File: `text_to_image/tools/fid/fid_score.py`
- Functions: `compute_fid()`, `calculate_activation_statistics()`, `calculate_frechet_distance()`
- Code Reference:
```python
def compute_fid(results, statistics_path, device, dims=2048, ...):
    imgs = [Image.fromarray(e).convert("RGB") for e in results]
    # ... statistical comparison of features
    fid_value = calculate_frechet_distance(m1, s1, m2, s2)
    return fid_value
```
This code evaluates text-to-image model outputs by computing the Fréchet Inception Distance (FID) metric. The evaluation loads generated images from model outputs, computes activation statistics using an InceptionV3 model as a feature extractor, and calculates statistical distance between distributions. No execution of model-generated artifacts occurs; only statistical comparison of image features.

Evidence 2: Speech Recognition Word Error Rate (WER) Calculation
- File: `speech2text/accuracy_eval.py`
- Functions: `word_error_rate()`, `main()`
- Code Reference:
```python
def word_error_rate(hypotheses: List[str], references: List[str]) -> float:
    normalizer = EnglishTextNormalizer()
    for h, r in zip(hypotheses, references):
        h = normalizer(h)
        r = normalizer(r)
        h_list = h.split()
        r_list = r.split()
        scores_clip, words_clip = compute_wer_with_concatenation(h_list, r_list)
```
Evaluates speech-to-text model outputs by decoding model output arrays to text, computing Levenshtein distance between hypothesis and reference transcripts, and performing text normalization and comparison using `EnglishTextNormalizer`. No execution of generated code occurs, only text comparison metrics.

Evidence 3: COCO Object Detection Evaluation
- File: `vision/classification_and_detection/tools/coco-analyze.py`
- Functions: `calculate_map()`, `annotate_image()`
- Code Reference:
```python
def calculate_map(results, cocoGt, output):
    cocoDt = cocoGt.loadRes(results)
    cocoEval = COCOeval(cocoGt, cocoDt, iouType="bbox")
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()
```
Evaluates object detection model outputs by loading detection results from JSON (bounding boxes, scores, categories), computing mAP (mean Average Precision) using pycocotools, comparing predicted boxes against ground truth annotations, and annotating images with detection results for visualization. No execution of model-generated code occurs, only evaluation of detection outputs.

Evidence 4: Neural Machine Translation BLEU/ROUGE Evaluation
- File: `retired_benchmarks/translation/gnmt/tensorflow/nmt/utils/evaluation_utils.py`
- Functions: `evaluate()`, `_bleu()`, `_rouge()`, `_accuracy()`, `_word_accuracy()`
- Code Reference:
```python
def evaluate(ref_file, trans_file, metric, subword_option=None):
    if metric.lower() == "bleu":
        evaluation_score = _bleu(ref_file, trans_file, subword_option=subword_option)
    elif metric.lower() == "rouge":
        evaluation_score = _rouge(ref_file, trans_file, subword_option=subword_option)
```
Evaluates translation model outputs using BLEU score computation for translation quality, ROUGE score for summarization tasks, text cleaning and BPE/SPM subword handling, and accuracy metrics based on text comparison. No execution of generated artifacts occurs, only text metric calculation.

Evidence 5: GPT-3 ROUGE Evaluation
- File: `retired_benchmarks/never_adopted/language/gpt3/megatron/evaluation.py`
- Functions: `main()`, `postprocess_text()`
- Code Reference:
```python
def main():
    # Load predictions and compute ROUGE
    result = metric.compute(
        predictions=preds, references=targets, use_stemmer=True, use_aggregator=False
    )
    result = {k: round(np.mean(v) * 100, 4) for k, v in result.items()}
```
Evaluates language model outputs by loading predictions from accuracy log, detokenizing model outputs, computing ROUGE metrics against reference targets, and post-processing text with NLTK sentence tokenization. Static text comparison is performed without code execution.

---

### Dynamic Execution

Evidence 1: Graph Neural Network Model Training/Evaluation
- File: `retired_benchmarks/recommendation/dlrm/tf/train_and_eval_runner.py`
- Class: `TrainAndEvalRunner`
- Functions: `train_and_eval()`, `train_loop()`, `eval_loop()`
- Code Reference:
```python
def train_and_eval(self, eval_init_fn=None, eval_finish_fn=None, run_finish_fn=None):
    def infeed_thread_fn(thread_index):
        for _ in range(self.max_train_iterations):
            self.input_sess[True][thread_index].run([self.enqueue_ops[True][thread_index]])
            if self.eval_steps > 0:
                self.input_sess[False][thread_index].run([self.enqueue_ops[False][thread_index]])
```
This code executes model-generated predictions by running TensorFlow computational graphs on TPU devices, executing training loops with `sess.run()` calls, running evaluation steps that process model outputs through the computational graph, and creating and executing TPU programs with `tpu.shard()` and `training_loop.repeat()`. This represents execution of the model itself for evaluation purposes, qualifying as dynamic execution in the context of evaluating model behavior.

Evidence 2: Loadgen Performance Testing
- File: `loadgen/tests/perftests_null_sut.py`
- Functions: `issue_query()`, `main()`
- Code Reference:
```python
def main(argv):
    settings = mlperf_loadgen.TestSettings()
    settings.scenario = mlperf_loadgen.TestScenario.SingleStream
    settings.mode = mlperf_loadgen.TestMode.PerformanceOnly
    sut = mlperf_loadgen.ConstructSUT(issue_query, flush_queries)
    qsl = mlperf_loadgen.ConstructQSL(1024 * 1024, 1024, load_samples_to_ram, unload_samples_from_ram)
    mlperf_loadgen.StartTest(sut, qsl, settings)
```
Executes performance evaluation scenarios by running loadgen test scenarios (SingleStream, MultiStream, Server, Offline), executing query processing loops through `mlperf_loadgen.StartTest()`, simulating system-under-test (SUT) behavior with query handling, and performing dynamic runtime evaluation of model serving performance. While this is a "null SUT" test, it demonstrates the execution framework used for benchmark evaluation.