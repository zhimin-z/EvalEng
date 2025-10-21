## Evaluator Categories

[Algorithmic]

## Detailed Analysis

### Algorithmic

Evidence 1: Statistical metrics and drift calculations
- File: `evidently/legacy/calculations/stattests/` (directory)
- File: `tests/calculations/stattests/test_get_stattest.py`
- Code Reference:
```python
@pytest.mark.parametrize(
    "feature_type,stattest_name",
    [
        ("num", "anderson"),
        ("cat", "chisquare"),
        ("num", "cramer_von_mises"),
        ("num", "ed"),
        ("num", "es"),
        ("cat", "fisher_exact"),
        ("cat", "g_test"),
        ("cat", "hellinger"),
        ("num", "hellinger"),
        ("cat", "jensenshannon"),
        ("num", "jensenshannon"),
        ("cat", "kl_div"),
        ("num", "kl_div"),
        ("num", "ks"),
        ("num", "mannw"),
        ("num", "empirical_mmd"),
        ("cat", "psi"),
        ("num", "psi"),
        ("num", "t_test"),
        ("text", "abs_text_content_drift"),
        ("text", "perc_text_content_drift"),
        ("cat", "TVD"),
        ("num", "wasserstein"),
        ("cat", "z"),
    ],
)
def test_use_stattest_by_name(feature_type: str, stattest_name: str):
    assert get_stattest(pd.Series(), pd.Series(), feature_type, stattest_name)
```
The harness implements multiple well-established statistical tests for drift detection across numerical, categorical, and text features. These tests use predefined mathematical formulas (Anderson-Darling, Kolmogorov-Smirnov, Wasserstein distance, Jensen-Shannon divergence, etc.) that produce deterministic, reproducible results based on distributional comparisons. This demonstrates algorithmic evaluation through standardized statistical methods rather than learned models or human judgment.

Evidence 2: Classification performance metrics
- File: `tests/calculations/test_classification_performance.py`
- Code Reference:
```python
def test_calculate_metrics():
    # ... calculates accuracy, precision, recall, f1, tpr, tnr, fpr, fnr, roc_auc, log_loss
    assert actual_result.accuracy == pytest.approx(4 / 10)
    assert actual_result.precision == pytest.approx(1 / 3)
    assert actual_result.recall == pytest.approx(1 / 5)
    assert actual_result.f1 == pytest.approx(1 / 4)
    assert actual_result.tpr == pytest.approx(1 / 5)
    assert actual_result.tnr == pytest.approx(3 / 5)
    assert actual_result.fpr == pytest.approx(2 / 5)
    assert actual_result.fnr == pytest.approx(4 / 5)
    assert actual_result.roc_auc == pytest.approx(0.64)
    assert actual_result.log_loss == pytest.approx(0.6884817487155065)
```
The framework calculates standard classification metrics using fixed mathematical formulas based on confusion matrix values and predicted probabilities. These metrics (accuracy, precision, recall, F1-score, ROC-AUC, etc.) follow well-defined algorithmic procedures that require no machine learning models or subjective judgment, confirming the algorithmic nature of the evaluation approach.

Evidence 3: Data quality metrics
- File: `tests/calculations/test_data_quality.py`
- Code Reference:
```python
def test_calculate_column_distribution(dataset: pd.DataFrame, column_type: str, expected_distribution: list):
    assert calculate_column_distribution(dataset["test"], column_type=column_type) == expected_distribution

def test_calculate_cramer_v_correlations():
    # Calculates Cramér's V correlation coefficient
    assert calculate_cramer_v_correlation("test1", data, ["test2", "test3", "test4"]) == ColumnCorrelations(...)
```
The system computes statistical properties of data distributions and correlations using algorithmic methods like Cramér's V coefficient. These calculations apply predetermined formulas to measure relationships between variables and characterize data distributions, demonstrating purely computational evaluation without requiring external models or human input.

Evidence 4: Recommender system metrics
- File: `tests/metrics/recsys/test_precision_top_k.py`
- File: `tests/metrics/recsys/test_recall_top_k.py`
- File: `tests/metrics/recsys/test_hit_rate_k.py`
- File: `tests/metrics/recsys/test_mrr.py`
- File: `tests/metrics/recsys/test_f_beta_top_k.py`
- File: `tests/metrics/recsys/test_popularity_bias.py`
- File: `tests/metrics/recsys/test_serendipity.py`
- File: `tests/metrics/recsys/test_personalisation.py`
- File: `tests/metrics/recsys/test_mar_k.py`
- Code Reference:
```python
def test_precision_value():
    metric = PrecisionTopKMetric(k=2)
    # Calculates precision@k

def test_recall_values():
    metric = RecallTopKMetric(k=2)
    # Calculates recall@k

def test_hit_rate_value():
    metric = HitRateKMetric(k=2)
    # Calculates hit rate

def test_mrr_value():
    metric = MRRKMetric(k=2)
    # Calculates Mean Reciprocal Rank

def test_fbeta_values():
    metric = FBetaTopKMetric(k=2)
    # Calculates F-beta score

def test_coverage(k, expected_coverage):
    metric = PopularityBias(k=k)
    # Calculates coverage and Gini coefficient

def test_curr_rank():
    metric = SerendipityMetric(k=3, item_features=["item_f1", "item_f2"])
    # Calculates serendipity metric

def test_curr_rank():
    metric = PersonalizationMetric(k=4)
    # Calculates personalization metric

def test_mar_values():
    metric = MARKMetric(k=2)
    # Calculates Mean Average Recall
```
The harness includes comprehensive algorithmic metrics for recommender system evaluation, including precision@k, recall@k, hit rate, MRR, F-beta, coverage, Gini coefficient, serendipity, and personalization metrics. Each metric applies a specific mathematical formula to ranking data to produce objective scores, exemplifying algorithmic evaluation through deterministic calculations rather than learned or subjective assessment methods.

Evidence 5: Text feature metrics
- File: `tests/features/test_text_length_feature.py`
- File: `tests/features/test_non_letter_character_percentage_feature.py`
- File: `tests/features/test_OOV_words_percentage_feature.py`
- Code Reference:
```python
def test_text_length_feature():
    feature_generator = TextLength("column_1")
    # Counts character length

def test_non_letter_character_percentage():
    feature_generator = NonLetterCharacterPercentage(column_name="column_1", display_name="cl")
    # Calculates percentage of non-letter characters

def test_oov_words_percentage():
    feature_generator = OOVWordsPercentage("column_1", ignore_words=("foobar",))
    # Calculates out-of-vocabulary words percentage
```
The framework measures text characteristics using simple algorithmic computations: counting characters, calculating character-type percentages, and identifying out-of-vocabulary words through dictionary lookups. These are rule-based, deterministic operations that require no machine learning models or human judgment, reinforcing the algorithmic evaluation methodology.

Evidence 6: String matching and validation metrics
- File: `tests/features/test_is_valid_json_feature.py`
- File: `tests/features/test_is_valid_sql_feature.py`
- File: `tests/features/test_is_valid_python_feature.py`
- File: `tests/features/test_exact_feature.py`
- File: `tests/features/test_json_schema_match_feature.py`
- File: `tests/features/test_contains_link_feature.py`
- Code Reference:
```python
def test_is_valid_json_feature(item: str, expected: bool):
    feature_generator = IsValidJSON("column_1")
    # Validates JSON syntax

def test_is_valid_sql_feature():
    feature_generator = IsValidSQL("column_1")
    # Validates SQL syntax

def test_is_valid_python(expected: bool):
    is_python = IsValidPython("TestColumnName")
    # Validates Python syntax

def test_exact_match_feature(value1: str, value2: str, expected: bool):
    feature_generator = ExactMatchFeature(columns=["column_1", "column_2"])
    # Performs exact string matching

def test_match_json_schema(...):
    schema_match = JSONSchemaMatch(...)
    # Validates JSON against schema

def test_contains_link_feature():
    feature_generator = ContainsLink("column_1")
    # Checks for URL presence using regex
```
The harness validates structured data formats (JSON, SQL, Python) through syntax parsing and performs pattern matching operations (exact matching, schema validation, regex-based URL detection). These are deterministic algorithmic operations that apply formal grammar rules and pattern recognition without requiring learned models or human evaluation.

Evidence 7: Text pattern matching
- File: `tests/features/test_text_contains_feature.py`
- File: `tests/features/test_text_part_feature.py`
- File: `tests/features/test_words_feature.py`
- Code Reference:
```python
def test_text_contains_feature(items: List[str], case: bool, mode: str, expected: List[bool]):
    feature_generator = Contains("column_1", items, case_sensitive=case, mode=mode)
    # Pattern matching in text

def test_text_begins_feature(substr: str, case: bool, expected: List[bool]):
    feature_generator = BeginsWith("column_1", substr, case_sensitive=case)
    # String prefix/suffix matching

def test_includes_words(words: List[str], mode: str, lemmatize: bool, expected: List[bool]):
    feature_generator = IncludesWords("column_1", words_list=words, mode=mode, lemmatize=lemmatize)
    # Word-level matching with optional lemmatization
```
The system implements text pattern matching through substring searches, prefix/suffix detection, and word-level matching with optional lemmatization. These operations use rule-based string algorithms and linguistic preprocessing (lemmatization) that follow deterministic procedures, demonstrating algorithmic rather than model-based or human-based evaluation.

Evidence 8: Similarity metrics
- File: `tests/features/test_bertscore_feature.py`
- File: `tests/features/test_json_match.py`
- Code Reference:
```python
def test_bert_score_feature(column_1: str, column_2: str, expected: float):
    feature_generator = BERTScoreFeature(columns=["column_1", "column_2"], tfidf_weighted=False)
    # Calculates BERTScore (note: uses pre-computed embeddings from BERTScore library)

def test_is_valid_sql_feature():
    feature_generator = JSONMatch(...)
    # JSON comparison
```
The harness computes similarity scores through algorithmic methods: BERTScore uses pre-computed embeddings from an external library to calculate semantic similarity via fixed mathematical operations, while JSON matching compares structured data algorithmically. Although BERTScore involves embeddings from a neural model, the evaluation itself applies deterministic cosine similarity calculations, maintaining the algorithmic nature of the evaluation process.

Evidence 9: Data drift metrics
- File: `tests/calculations/test_data_drift.py`
- Code Reference:
```python
def test_get_one_column_drift_success(...):
    result = get_one_column_drift(...)
    # Statistical drift detection
```
The framework detects data drift through statistical hypothesis testing, comparing distributions between reference and current datasets using algorithmic statistical tests. This approach applies predetermined mathematical procedures to identify distribution shifts, exemplifying algorithmic evaluation through quantitative, reproducible statistical methods rather than subjective or learned assessment.