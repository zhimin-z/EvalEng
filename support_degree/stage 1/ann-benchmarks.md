# ann-benchmarks - Stage 1 (CONFIGURE) Evaluation

## Summary
Ann-benchmarks is a benchmarking framework for approximate nearest neighbor (ANN) algorithms. It focuses on configuring algorithm implementations via YAML files and running them in Docker containers. The framework has strong dataset handling and algorithm configuration capabilities, but lacks advanced features like cost estimation, security controls, and sophisticated environment management. Configuration is declarative but limited to algorithm parameters rather than full evaluation pipelines.

## Feature Ratings

| Feature | Rating | Justification |
|---------|--------|---------------|
| S1F1: Dataset Discovery | 2 | Supports multiple dataset sources (HDF5, download from URLs) with basic versioning via filenames, but no schema definition API or flexible split strategies |
| S1F2: Model Configuration | 2 | Algorithm configuration via YAML with Docker container support for 40+ algorithms, but limited provider abstraction and no runtime override capabilities |
| S1F3: Prompt Configuration | 0 | Not applicable - this is an ANN benchmark framework, not an LLM evaluation framework. No prompt or parameter templating system |
| S1F4: Environment Setup | 2 | Docker-based isolation with requirements.txt and automated build scripts, but no sophisticated dependency management or multi-environment support |
| S1F5: Security & Access | 0 | No security features, access control, credential management, or audit logging present in the codebase |
| S1F6: Cost Estimation | 0 | No cost modeling, resource projection, or budget tracking capabilities |

---

## Detailed Analysis

### S1F1: Dataset Discovery and Logical Configuration

Rating: 2/3

Evidence:

1. Dataset Source Support (Limited):
   - Supports HDF5 files and HTTP downloads
   - From `ann_benchmarks/datasets.py`:
   ```python
   DATASETS = {
       "fashion-mnist-784-euclidean": _fashion_mnist,
       "gist-960-euclidean": _gist,
       "glove-25-angular": lambda out_fn: _glove(out_fn, 25),
       # ... many more datasets
   }
   
   def get_dataset(dataset_name):
       # Downloads and loads HDF5 files
       hdf5_filename = get_dataset_fn(dataset_name)
       return h5py.File(hdf5_filename, "r"), dimension
   ```
   - From `README.md`:
   ```
   | Dataset | Dimensions | Train size | Test size | Download |
   | MNIST   | 784        | 60,000     | 10,000    | [HDF5](http://ann-benchmarks.com/mnist-784-euclidean.hdf5) |
   ```

2. Schema Definition (Absent):
   - No schema API - datasets are pre-processed HDF5 files
   - Fixed schema: `train`, `test`, `neighbors`, `distances` keys
   - From `ann_benchmarks/datasets.py`:
   ```python
   def get_dataset(dataset_name):
       hdf5_filename = get_dataset_fn(dataset_name)
       hdf5_file = h5py.File(hdf5_filename, "r")
       # Fixed structure expected: train, test, neighbors, distances
   ```

3. Split Strategies (Fixed):
   - Splits are pre-defined in HDF5 files, not configurable
   - From `create_dataset.py`:
   ```python
   # Datasets are created with fixed train/test splits
   f.create_dataset("train", data=train)
   f.create_dataset("test", data=test)
   ```

4. Versioning (Basic):
   - Version tracking via dataset names/URLs, not systematic
   - No version history or querying capabilities
   - From `README.md`: Different dataset versions referenced by name (e.g., "glove-25-angular", "glove-50-angular")

Why not 3 points: Limited to 2 sources (HDF5, HTTP), no schema definition API, fixed splits, no proper versioning system.

Why not 1 point: Does support multiple dataset sources and has a clear dataset registration mechanism.

---

### S1F2: Model and Backend Configuration

Rating: 2/3

Evidence:

1. Provider Support (Good):
   - Supports 40+ algorithm implementations as "providers"
   - From `ann_benchmarks/algorithms/` directory structure:
   ```
   algorithms/
   ├── annoy/
   ├── faiss/
   ├── hnswlib/
   ├── nmslib/
   ├── scann/
   └── [37+ more algorithms]
   ```
   - Each algorithm has its own Docker container

2. Configuration Method (YAML-based):
   - From `ann_benchmarks/algorithms/hnswlib/config.yml`:
   ```yaml
   float:
     any:
     - base_args: ['@metric']
       constructor: HnswLib
       docker_tag: ann-benchmarks-hnswlib
       module: ann_benchmarks.algorithms.hnswlib
       name: hnswlib
       run_groups:
         M-12:
           arg_groups: [{M: 12, efConstruction: 500}]
           query_args: [[10, 20, 40, 80, 120, 200, 400, 600, 800]]
   ```

3. Authentication (Absent):
   - No authentication or credential management
   - Docker containers run locally without security controls

4. Resource Allocation (Basic):
   - From `ann_benchmarks/main.py`:
   ```python
   def run_worker(cpu: int, mem_limit: int, args, queue):
       cpu_limit = str(cpu) if not args.batch else f"0-{multiprocessing.cpu_count() - 1}"
       run_docker(definition, args.dataset, args.count, args.runs, 
                  args.timeout, args.batch, cpu_limit, mem_limit)
   ```
   - Memory limits calculated: `mem_limit = int((psutil.virtual_memory().available - memory_margin) / args.parallelism)`

Why not 3 points: No multi-provider abstraction (each algorithm is separate), no runtime config override, no sophisticated authentication.

Why not 1 point: Comprehensive algorithm support with YAML configuration and Docker isolation.

---

### S1F3: Evaluation Parameters and Prompt Configuration

Rating: 0/3

Evidence:

This framework is for benchmarking ANN algorithms, not LLM evaluation. There are no prompts, templates, or LLM-related parameters.

From `ann_benchmarks/main.py`, the configuration is about algorithm parameters:
```python
parser.add_argument("--dataset", help="the dataset to load training points from")
parser.add_argument("-k", "--count", help="the number of near neighbours to search for")
```

The "query_args" in configs are algorithm-specific hyperparameters (e.g., `ef` for HNSW), not prompt parameters.

Why 0 points: Not applicable to this type of framework.

---

### S1F4: Environment Setup and Dependency Management

Rating: 2/3

Evidence:

1. Dependency Specification:
   - From `requirements.txt`:
   ```txt
   ansicolors==1.1.8
   docker==7.1.0
   h5py==3.13.0
   matplotlib==3.10.1
   numpy==2.2.4
   pyyaml==6.0.2
   psutil==7.0.0
   scikit-learn==1.6.1
   ```
   - From `pyproject.toml`:
   ```toml
   [tool.black]
   line-length = 120
   ```
   - Dependencies are pinned but not extensively documented

2. Containerization (Strong):
   - Each algorithm has a Dockerfile
   - From `install.py`:
   ```python
   subprocess.check_call(
       "docker build %s --rm -t ann-benchmarks-%s -f "
       "ann_benchmarks/algorithms/%s/Dockerfile ." % (q, library, library),
       shell=True,
   )
   ```
   - Base image provided at `ann_benchmarks/algorithms/base/Dockerfile`

3. Environment Automation:
   - From `install.py`:
   ```python
   def build(library, args):
       print("Building %s..." % library)
       subprocess.check_call("docker build ...")
   ```
   - Parallel builds supported:
   ```python
   pool = Pool(processes=args.proc)
   install_status = pool.map(build_multiprocess, [(tag, args.build_arg) for tag in tags])
   ```

4. Hardware Configuration (Basic):
   - CPU allocation: `cpu_limit = str(cpu)`
   - Memory limits calculated automatically
   - No GPU management or explicit hardware specs

Why not 3 points: Basic dependency management without virtual environments, no hardware specification beyond CPU/memory, limited setup automation.

Why not 1 point: Docker containerization is comprehensive, dependencies are specified, automated build scripts exist.

---

### S1F5: Security and Access Control

Rating: 0/3

Evidence:

No security features found in the codebase:

1. Credential Management: None
2. Access Control: None
3. Audit Logging: Only basic logging for execution
   - From `logging.conf`:
   ```ini
   [logger_annb]
   level=INFO
   handlers=consoleHandler
   ```
   - No security-focused logging

4. Enterprise Integration: None

The framework runs locally with Docker containers that have full system access.

Why 0 points: Complete absence of security features, access control, or credential management.

---

### S1F6: Cost Estimation and Budget Planning

Rating: 0/3

Evidence:

No cost-related features:

1. Cost Modeling: Not present
2. Resource Projection: Only basic memory calculation:
   ```python
   memory_margin = 500e6  # reserve some extra memory
   mem_limit = int((psutil.virtual_memory().available - memory_margin) / args.parallelism)
   ```
3. Budget Tools: None
4. Optimization Suggestions: None

The framework tracks execution time and memory usage for benchmarking but not for cost estimation:
- From `ann_benchmarks/results.py`:
```python
store_results(dataset_name, count, definition, query_argument_group, attrs, results, batch)
```

Why 0 points: No cost estimation, budgeting, or optimization features. Only performance tracking for benchmarking purposes.

---

## Summary Assessment

Ann-benchmarks excels at what it's designed for: benchmarking ANN algorithms with standardized datasets. However, as an evaluation framework assessed against LLM evaluation criteria:

Strengths:
- Comprehensive algorithm configuration via YAML
- Strong Docker-based isolation for reproducibility  
- Good dataset handling with 20+ pre-defined datasets
- Parallel execution support

Critical Gaps:
- No security or access control features
- No cost estimation or budget management
- Limited to pre-defined datasets with fixed schemas
- No sophisticated environment/dependency management
- Not designed for LLM evaluation (prompt configuration N/A)

Overall Stage 1 Score: 6/18 (33%)

This framework is purpose-built for ANN benchmarking and would require significant architectural changes to support general evaluation framework features like security, cost management, or LLM-specific capabilities.