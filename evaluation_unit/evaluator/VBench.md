## Evaluator Categories

[Algorithmic, ML-based, Custom]

## Detailed Analysis

### Algorithmic

Evidence 1: CLIP-based similarity score calculation
- File: `competitions/clip_score.py`
- Function: `clip_alignment()`
- Code Reference:
```python
def clip_alignment(clip_model, video_dict, preprocess, device):
    sim = []
    video_results = []
    
    image_transform = clip_transform(224)
    for info in tqdm(video_dict):
        
        query = info["prompt"]
        text = clip.tokenize([query], truncate=True).to(device)
        text_feature = clip_model.encode_text(text)
        text_feature = F.normalize(text_feature, dim=-1)
        
        video_list = info["video_list"]
        for video_path in video_list:
            with torch.no_grad():
                images = read_frames_decord_by_fps(video_path, num_frames=8, sample="middle")
                images = image_transform(images)
                images = images.to(device)
                
                image_features = clip_model.encode_image(images)
                image_features = F.normalize(image_features, dim=-1, p=2)

                video_sim = image_features @ text_feature.T
                video_sim = np.mean(video_sim.cpu().tolist())
                sim.append(video_sim)
```
This implements a CLIP-based similarity score calculation using cosine similarity between video frames and text prompts. The similarity is computed via dot product and normalization (lines with `F.normalize` and `@` operator), which are deterministic mathematical operations. The final score is the mean of frame-level similarities, representing a predefined algorithmic metric that provides reproducible assessment through established computational measures.

Evidence 2: Score normalization and aggregation
- File: `scripts/cal_final_score.py`
- Functions: `get_nomalized_score()` and `get_quality_score()`
- Code Reference:
```python
def get_nomalized_score(upload_data):
    # get the normalize score
    normalized_score = {}
    for key in TASK_INFO:
        min_val = NORMALIZE_DIC[key]['Min']
        max_val = NORMALIZE_DIC[key]['Max']
        normalized_score[key] = (upload_data[key] - min_val) / (max_val - min_val)
        normalized_score[key] = normalized_score[key] * DIM_WEIGHT[key]
    return normalized_score

def get_quality_score(normalized_score):
    quality_score = []
    for key in QUALITY_LIST:
        quality_score.append(normalized_score[key])
    quality_score = sum(quality_score)/sum([DIM_WEIGHT[i] for i in QUALITY_LIST])
    return quality_score
```
These functions implement min-max normalization and weighted averaging formulas, which are deterministic statistical and mathematical operations used to aggregate evaluation scores across dimensions. This represents the algorithmic evaluator category's goal of ensuring consistent, reproducible evaluation through established computational measures.

---

### ML-based

Evidence 1: Pre-trained CLIP model for embedding-based evaluation
- File: `competitions/clip_score.py`
- Function: `compute_clip_score()`
- Code Reference:
```python
def compute_clip_score(json_dir, device, submodules_list, **kwargs):
    
    clip_model, preprocess = clip.load("ViT-B/32", device=device)
    logger.info("Initialize CLIP success")
    
    _, video_dict = load_dimension_info(json_dir, dimension='clip_score', lang='en')
    all_results, video_results = clip_alignment(clip_model, video_dict, preprocess, device)
    return all_results, video_results
```
The code loads a pre-trained CLIP model (ViT-B/32) which is a neural network-based model. This model is used to encode both images and text into embedding space for similarity comparison. The model inference happens through `clip_model.encode_text()` and `clip_model.encode_image()` calls, making it a learned ML-based evaluator that leverages learned representations for nuanced assessment capturing semantic and contextual quality.

Evidence 2: Multimodal LLM for anomaly detection
- File: `VBench-2.0/vbench2/third_party/Instance_detector/test.py`
- Function: `compute_anomaly()`
- Code Reference:
```python
def compute_anomaly(prompt_dict_ls, device, submodules_dict):
    processed_json=[]
    request_config = RequestConfig(max_tokens=512, temperature=0)
    adapter_path = submodules_dict['model']
    args = BaseArguments.from_pretrained(adapter_path)
    model, tokenizer = get_model_tokenizer(args.model)
    model = Swift.from_pretrained(model, adapter_path)
    template = get_template(args.template, tokenizer, args.system)
    engine = PtEngine.from_model_template(model, template)
    final_score=0
    final_num=0
    processed_json=[]
    for prompt_dict in tqdm(prompt_dict_ls):
        video_paths = prompt_dict['video_list']
        model_name = video_paths[0].split('/')[-3]
        split(os.path.dirname(video_paths[0]), model_name)
        for video_path in video_paths:
            frame_count, fps, video_length = get_video_info(video_path)
            os.environ['FPS'] = f'{fps}'
            valid=True
            new_item={
                'video_path':video_path,
            }
            video_clip_paths = f"./model_clip/{model_name}"
            for idx in range(int(video_length)-1):
                clip_path = os.path.join(video_clip_paths, f"{video_path.split('/')[-1][:-4]}_clip_{idx:04d}.mp4")
                message = [
                {
                    "role": "system",
                    "content": "You are a helpful and harmless assistant."
                },
                {
                    'role': 'user',
                    'content': 
                        [
                            {
                                'type': 'video',
                                'video': clip_path
                            }, 
                            {
                                'type': 'text',
                                'text': 'Does the video contain one or more of the following anomalies: sudden appearance, disappearance, fusion, fission?\nOptions:\nA. Yes\nB. No'
                            }
                        ]
                }]
                infer_request = InferRequest(messages=message)
                output_text = infer_lora(engine, request_config, infer_request)
                if '(A)' in output_text or 'yes' in output_text.lower() or 'A'==output_text:
                    valid=False
                    break
```
This code loads a multimodal LLM model (via `get_model_tokenizer` and `Swift.from_pretrained`) and uses it to evaluate video clips for anomalies. The model performs inference through `infer_lora()`, which returns text judgments parsed for evaluation. This is a clear ML-based evaluator using a trained model to assess video quality, demonstrating the use of LLM judges as evaluators that leverage learned representations for nuanced semantic assessment.

---

### Custom

Evidence 1: Multi-stage weighted evaluation pipeline
- File: `scripts/cal_final_score.py`
- Function: `get_final_score()`
- Code Reference:
```python
def get_final_score(quality_score,semantic_score):
    return (quality_score * QUALITY_WEIGHT + semantic_score * SEMANTIC_WEIGHT) / (QUALITY_WEIGHT + SEMANTIC_WEIGHT)
```
This implements a custom multi-stage evaluation pipeline that combines normalized scores from multiple dimensions (quality and semantic), applies dimension-specific weights, and aggregates them into category-level scores (quality_score, semantic_score) before computing a final weighted score. This hierarchical aggregation with custom weighting schemes represents a specialized evaluation workflow specific to VBench, addressing unique evaluation requirements through a domain-specific mechanism that extends standard evaluator categories.

Evidence 2: VBench 2.0 multi-dimensional capability scoring
- File: `VBench-2.0/scripts/cal_final_score.py`
- Functions: `get_creativity_score()` and `get_final_score()`
- Code Reference:
```python
def get_creativity_score(score):
    creativity_score = []
    for key in CREATIVITY_LIST:
        creativity_score.append(score[key])
    creativity_score = sum(creativity_score)/len(CREATIVITY_LIST)
    return creativity_score

def get_final_score(creativity_score, commonsense_score, controllability_score, human_fidelity_score, physics_score):
    return (creativity_score + commonsense_score + controllability_score + human_fidelity_score + physics_score) / 5
```
VBench 2.0 implements a custom evaluation framework with five distinct capability categories (creativity, commonsense, controllability, human fidelity, physics). Each category aggregates multiple metrics using equal weighting, and the final score is computed as an unweighted average across categories. This domain-specific multi-dimensional evaluation design represents a custom pipeline tailored to video generation benchmarking that combines standard evaluator types to meet unique requirements for comprehensive video quality assessment.

Evidence 3: Configuration-based adaptive evaluation pipeline
- File: `competitions/run_eval.py`
- Code Reference:
```python
if "short_prompt_list" in args.prompt_file:
    myvbench.evaluate(
        videos_path = args.video_path,
        name = f'results_short_{current_time}',
        prompt_list=prompts,
        dimension_list = args.dimension,
        **kwargs
    )
    
elif "long_prompt_list" in args.prompt_file:   
    
    kwargs['sb_clip2clip_feat_extractor'] = 'dino'
    kwargs['bg_clip2clip_feat_extractor'] = 'clip'
    kwargs['clip_length_config'] = "clip_length_mix.yaml"
    kwargs['w_inclip'] = 1.0
    kwargs['w_clip2clip'] = 0.0
    kwargs['use_semantic_splitting'] = True
    kwargs['slow_fast_eval_config'] = "configs/slow_fast_params.yaml"
    kwargs['dev_flag'] = False
    kwargs['sb_mapping_file_path'] = "configs/subject_mapping_table.yaml"
    kwargs['bg_mapping_file_path'] = "configs/background_mapping_table.yaml"
    
    myvbench.evaluate_long(
        videos_path = args.video_path,
        name = f'results_long_{current_time}',
        prompt_list=prompts,
        dimension_list = args.dimension,
        **kwargs
    )
```
This demonstrates a custom evaluation pipeline that switches between different evaluation modes based on prompt type (short vs. long videos). The long video evaluation mode involves specialized configurations for semantic splitting, multiple feature extractors (DINO and CLIP), and temporal analysis parameters. This represents a complex, domain-specific evaluation workflow that combines multiple evaluation strategies based on content characteristics, exemplifying the custom evaluator category's goal of addressing unique evaluation requirements through specialized mechanisms that adapt to specific content properties.