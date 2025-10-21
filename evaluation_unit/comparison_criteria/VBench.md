## Comparison Criteria Categories

[Explicit Labels, None, Custom]

## Detailed Analysis

### Explicit Labels

Evidence 1: Normalization Reference Values
- File: `scripts/constant.py` (referenced by `scripts/cal_final_score.py`)
- Code Reference: Constants defining reference ranges
```python
# NORMALIZE_DIC, TASK_INFO, DIM_WEIGHT define normalization ranges
# These contain predetermined reference values for scoring
```
The harness uses explicit normalization dictionaries (`NORMALIZE_DIC`, `NORMALIZE_DIC_I2V`) containing min/max reference values for each evaluation dimension. These predetermined ranges serve as ground truth references for evaluating video generation quality.

Evidence 2: Score Normalization Against References
- File: `scripts/cal_final_score.py`, `scripts/cal_i2v_final_score.py`
- Code Reference: `get_nomalized_score()` function
```python
def get_nomalized_score(upload_data):
    normalized_score = {}
    for key in TASK_INFO:
        min_val = NORMALIZE_DIC[key]['Min']
        max_val = NORMALIZE_DIC[key]['Max']
        normalized_score[key] = (upload_data[key] - min_val) / (max_val - min_val)
```
Normalizes model outputs against predetermined min/max ranges. These reference values serve as explicit labels defining acceptable performance bounds across dimensions like subject consistency, background consistency, and temporal flickering.

Evidence 3: Submission Score Loading
- File: `scripts/cal_final_score.py`
- Code Reference: `submission()` function
```python
def submission(model_name, zip_file):
    upload_data = {}
    # load your score
    for file in os.listdir(model_name):
        cur_file = os.path.join(model_name, file)
        if os.path.isdir(cur_file):
            for subfile in os.listdir(cur_file):
                if subfile.endswith(".json"):
                    with open(os.path.join(cur_file, subfile)) as ff:
                        cur_json = json.load(ff)
                        if isinstance(cur_json, dict):
                            for key in cur_json:
                                upload_data[key.replace('_',' ')] = cur_json[key][0]
```
Loads evaluation scores and compares them against explicit reference ranges defined in normalization dictionaries. This demonstrates systematic comparison of model outputs to predetermined reference standards.

---

### None

Evidence 1: Text-Video Alignment Without References
- File: `competitions/clip_score.py`
- Code Reference: `clip_alignment()` function
```python
def clip_alignment(clip_model, video_dict, preprocess, device):
    sim = []
    video_results = []
    for info in tqdm(video_dict):
        query = info["prompt"]
        text = clip.tokenize([query], truncate=True).to(device)
        text_feature = clip_model.encode_text(text)
        # Compute similarity without reference videos
        video_sim = image_features @ text_feature.T
        video_sim = np.mean(video_sim.cpu().tolist())
```
Measures text-video alignment using cosine similarity between CLIP embeddings without requiring reference videos. This intrinsic metric evaluates semantic correspondence through learned representations.

Evidence 2: Intrinsic Video Evaluation
- File: `evaluate.py`, `evaluate_i2v.py`, `evaluate_trustworthy.py`
- Code Reference: Evaluation instantiation
```python
# evaluate.py
my_VBench = VBench(device, args.full_json_dir, args.output_path)
my_VBench.evaluate(
    videos_path = args.videos_path,
    name = f'results_{current_time}',
    dimension_list = args.dimension,
    # No reference videos or labels required
)
```
Evaluates intrinsic properties of generated videos including imaging quality, motion smoothness, and temporal consistency without external references. These reference-free metrics assess inherent video characteristics.

Evidence 3: Anomaly Detection Without Ground Truth
- File: `VBench-2.0/vbench2/third_party/Instance_detector/test.py`
- Code Reference: `compute_anomaly()` function
```python
def compute_anomaly(prompt_dict_ls, device, submodules_dict):
    for video_path in video_paths:
        # Binary classification without reference
        if '(A)' in output_text or 'yes' in output_text.lower():
            valid=False
        if valid:
            final_score+=1
            new_item['video_results']=1.0
```
Performs binary detection of visual anomalies (appearance/disappearance/fusion/fission) without ground truth references. This intrinsic validation assesses video quality through internal consistency checks.

---

### Custom

Evidence 1: Hierarchical Score Aggregation
- File: `scripts/cal_final_score.py`
- Code Reference: Multi-stage scoring functions
```python
def get_quality_score(normalized_score):
    quality_score = []
    for key in QUALITY_LIST:
        quality_score.append(normalized_score[key])
    quality_score = sum(quality_score)/sum([DIM_WEIGHT[i] for i in QUALITY_LIST])
    return quality_score

def get_final_score(quality_score,semantic_score):
    return (quality_score * QUALITY_WEIGHT + semantic_score * SEMANTIC_WEIGHT) / 
           (QUALITY_WEIGHT + SEMANTIC_WEIGHT)
```
Implements custom hierarchical evaluation combining normalized reference-based scores with weighted aggregation. This multi-stage pipeline creates composite scores through domain-specific weighting schemes.

Evidence 2: Image-to-Video Specialized Scoring
- File: `scripts/cal_i2v_final_score.py`
- Code Reference: I2V-specific aggregation functions
```python
def get_i2v_quality_score(normalized_score):
    quality_score = []
    for key in I2V_QUALITY_LIST:
        quality_score.append(normalized_score[key])
    quality_score = sum(quality_score)/sum([DIM_WEIGHT_I2V[i] for i in I2V_QUALITY_LIST])
    return quality_score
```
Custom scoring pipeline specialized for image-to-video generation tasks. Implements dimension-specific weights (`DIM_WEIGHT_I2V`) creating domain-tailored composite evaluation metrics.

Evidence 3: Domain-Specific Category Scoring
- File: `VBench-2.0/scripts/cal_final_score.py`
- Code Reference: Category-based score computation
```python
def get_creativity_score(score):
    creativity_score = []
    for key in CREATIVITY_LIST:
        creativity_score.append(score[key])
    creativity_score = sum(creativity_score)/len(CREATIVITY_LIST)
    return creativity_score
```
VBench 2.0 implements specialized evaluation taxonomy organizing metrics into categories (creativity, commonsense, controllability, human fidelity, physics). This custom framework combines multiple evaluation dimensions into domain-specific composite scores through hierarchical aggregation, integrating both reference-based normalization and reference-free intrinsic metrics in a specialized video generation assessment pipeline.