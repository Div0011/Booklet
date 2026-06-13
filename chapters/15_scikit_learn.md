# 15. Scikit-Learn (Classical Machine Learning)

## 1. Introduction
### What it is
Scikit-Learn is a Python library providing unified interfaces for classical machine learning: classification, regression, clustering, dimensionality reduction, preprocessing, and model evaluation.

### Why it exists
Before scikit-learn, ML code was fragmented across Matlab, R, and custom scripts with inconsistent APIs. Scikit-learn standardized estimator `fit`/`predict`/`transform` patterns, built on NumPy/SciPy, enabling rapid prototyping and productionization.

### Problems it solves
- **API fragmentation**: Unified estimator interface.
- **Preprocessing boilerplate**: Imputation, scaling, encoding, pipeline composition.
- **Model selection**: Cross-validation, hyperparameter search, metrics.
- **Reproducibility**: Fixed random seeds and consistent evaluation.

### Industry Use Cases
- Tabular churn prediction, credit scoring.
- Customer segmentation and anomaly detection.
- Baseline models before deep learning.
- Feature selection and dimensionality reduction.

### Analogy
If deep learning is a custom race car, scikit-learn is a well-stocked garage: reliable tools for most everyday ML jobs without tuning a bespoke engine.

---

## 2. Core Concepts

### Beginner Concepts
- **Estimator API**: `fit(X, y)` trains; `predict(X)` infers; `transform(X)` modifies.
- **Supervised vs Unsupervised**: labeled targets vs. no labels.
- **Train/Test Split**: Holdout set prevents optimistic performance estimates.
- **Features vs Target**: `X` matrix, `y` vector.

### Intermediate Concepts
- **Preprocessing**:
  - Imputation (`SimpleImputer`, `KNNImputer`).
  - Scaling (`StandardScaler`, `MinMaxScaler`, `RobustScaler`).
  - Encoding (`OneHotEncoder`, `OrdinalEncoder`).
- **Pipeline**: Chain transformers + estimator into one object.
- **Cross-Validation**: `KFold`, `StratifiedKFold`, `GroupKFold`.
- **Metrics**:
  - Classification: accuracy, precision, recall, F1, ROC AUC.
  - Regression: MAE, MSE, RMSE, R².

### Advanced Concepts
- **Ensemble Methods**:
  - Bagging (`BaggingClassifier`, `RandomForest`).
  - Boosting (`GradientBoosting`, `AdaBoost`, `HistGradientBoosting`).
  - Stacking (`StackingClassifier`).
- **Custom Estimators**: subclass `BaseEstimator`, `ClassifierMixin`, implement `fit`/`predict`.
- **Calibration**: `CalibratedClassifierCV` for reliable probabilities.
- **Out-of-core learning**: `partial_fit` for datasets larger than memory.

---

## 3. Internal Working

### Estimator Lifecycle
```text
Raw data -> Transformer(s) -> Estimator -> Predictions
       |            |             |
   fit/transform  fit/predict   predict/proba
```
`Pipeline.fit` calls `fit_transform` on each transformer, then `fit` on estimator. `Pipeline.predict` calls `transform` then `predict`.

### Cross-Validation Mechanics
```text
KFold splits indices into k folds.
Each iteration:
  train on k-1 folds
  validate on held-out fold
Metric aggregated across folds.
```
Stratified folds preserve class ratios; GroupKFold respects group IDs to prevent leakage.

### Random Forest Decision Flow
```text
Bootstrap sample -> grow tree with random feature subset -> aggregate votes
```
Each tree is independent; prediction is majority vote (classification) or mean (regression).

---

## 4. Important Terminology
- **Estimator**: Object with `fit` method.
- **Transformer**: Object with `fit` and `transform`.
- **Pipeline**: Sequenced transformers + estimator.
- **Cross-Validation**: Repeated train/validation splitting.
- **Hyperparameter**: Estimator setting set before training (e.g., `max_depth`).
- **Feature Importance**: Contribution of each feature to split decisions.
- **ROC AUC**: Area under Receiver Operating Characteristic curve.
- **Calibration**: Mapping predicted probabilities to empirical frequencies.

---

## 5. Beginner Examples

### Example 1: Classification Pipeline with Cross-Validation
```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])

scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
print("CV accuracy:", scores.mean().round(4))
```

### Example 2: Feature Importance from Random Forest
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier(n_estimators=200, random_state=0).fit(X, y)
importances = model.feature_importances_
print("Feature importances:", importances.round(3))
```
Gini importance measures how much each feature decreases impurity across trees.

### Example 3: Grid Search for Hyperparameters
```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {"C": [0.1, 1, 10], "gamma": [0.001, 0.01, 0.1]}
grid = GridSearchCV(SVC(), param_grid, cv=5)
grid.fit(X_train, y_train)
print("Best params:", grid.best_params_)
```

---

## 6. Intermediate Examples

### Example 1: ColumnTransformer for Heterogeneous Data
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

df = pd.DataFrame({
    "age": [25, 32, 47],
    "income": [50000, 80000, 120000],
    "city": ["NY", "LA", "NY"],
})
num_cols = ["age", "income"]
cat_cols = ["city"]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])
X = preprocess.fit_transform(df)
print(X.shape)
```

### Example 2: Classification Report and Confusion Matrix
```python
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```
`classification_report` gives precision, recall, F1 per class.

### Example 3: Imbalanced Learn with Class Weights
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(class_weight="balanced", n_estimators=200, random_state=0)
model.fit(X_train, y_train)
```
`class_weight="balanced"` weights classes inversely by frequency.

### Example 4: Calibrating Probabilities
```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC

model = CalibratedClassifierCV(SVC(probability=False), cv=5)
model.fit(X_train, y_train)
probs = model.predict_proba(X_test)
```
Use calibrated probabilities for threshold-based decisions or cost-sensitive applications.

### Example 5: Unsupervised Learning Pipeline (PCA + KMeans & DBSCAN Clustering)
```python
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.pipeline import Pipeline

# Generate synthetic high-dimensional cluster data
X_raw, _ = make_blobs(n_samples=500, n_features=10, centers=4, random_state=42)

# Preprocessing and Dimensionality Reduction Pipeline
preprocessor = Pipeline([
    ("scaler", StandardScaler()),
    ("pca", PCA(n_components=2, random_state=42))
])

# Fit and transform
X_proj = preprocessor.fit_transform(X_raw)

# 1. KMeans Clustering (parametric, expects spherical clusters)
kmeans = KMeans(n_clusters=4, random_state=42, n_init="auto")
kmeans_labels = kmeans.fit_predict(X_proj)

# 2. DBSCAN Clustering (non-parametric density-based, handles arbitrary shapes & noise)
dbscan = DBSCAN(eps=0.3, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_proj)

print("KMeans cluster centers:\n", kmeans.cluster_centers_)
print("DBSCAN noise points detected:", sum(dbscan_labels == -1))
```

### Example 6: Ensemble Models (AdaBoost & XGBoost Integration)
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. AdaBoost with Decision Tree stump base estimator
ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)
ada.fit(X_train, y_train)
print("AdaBoost Test Accuracy:", ada.score(X_test, y_test))

# 2. XGBoost Classifier using scikit-learn API wrapper
xgb = XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    random_state=42,
    eval_metric="logloss"
)
xgb.fit(X_train, y_train)
print("XGBoost Test Accuracy:", xgb.score(X_test, y_test))
```

### Example 7: Anomaly Detection with Isolation Forest
```python
from sklearn.ensemble import IsolationForest
import numpy as np

# Generate clean training data and some anomalous test data
rng = np.random.default_rng(42)
X_train = rng.normal(loc=0.0, scale=1.0, size=(200, 2))
X_test = np.vstack([
    rng.normal(loc=0.0, scale=1.0, size=(20, 2)),      # Normal points
    rng.uniform(low=-4.0, high=4.0, size=(10, 2))      # Potential outliers
])

# Fit Isolation Forest (contamination is the expected ratio of outliers)
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(X_train)

# Predict anomaly labels (-1: anomaly, 1: normal)
predictions = iso_forest.predict(X_test)
anomaly_scores = iso_forest.decision_function(X_test)  # Lower values indicate anomaly

print("Outliers predicted in test set:", sum(predictions == -1))
```

### Example 8: Time-Series Split and Modeling
```python
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge
import numpy as np

# Generate mock daily time-series target and features
timesteps = 100
X_ts = np.random.randn(timesteps, 5)
y_ts = np.arange(timesteps) * 0.5 + np.random.randn(timesteps)

# TimeSeriesSplit prevents lookahead bias (future leakage into past)
tscv = TimeSeriesSplit(n_splits=5)

for fold, (train_index, test_index) in enumerate(tscv.split(X_ts)):
    X_train, X_test = X_ts[train_index], X_ts[test_index]
    y_train, y_test = y_ts[train_index], y_ts[test_index]
    
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Fold {fold} - Train Range: [{train_index[0]}-{train_index[-1]}], "
          f"Test Range: [{test_index[0]}-{test_index[-1]}], R^2 Score: {score:.3f}")
```

---

## 7. Advanced Concepts

### Custom Scoring and Metric Development
```python
from sklearn.metrics import make_scorer, fbeta_score

f2_scorer = make_scorer(fbeta_score, beta=2)
# GridSearchCV(..., scoring=f2_scorer)
```
`make_scorer` wraps any callable as a scorer compatible with cross-validation.

### Out-of-Core Learning
```python
from sklearn.linear_model import SGDClassifier

model = SGDClassifier(loss="log_loss")
for X_chunk, y_chunk in stream_minibatches(path):
    model.partial_fit(X_chunk, y_chunk, classes=[0,1,2])
```
`partial_fit` enables training on data that does not fit in RAM.

### Stacking Ensembles
```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

stack = StackingClassifier(
    estimators=[
        ("dt", DecisionTreeClassifier(max_depth=3)),
        ("knn", KNeighborsClassifier(n_neighbors=5)),
    ],
    final_estimator=LogisticRegression(),
    cv=5,
)
```
Combines multiple model types; final estimator learns how to weight base predictions.

### Permutation Importance
```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_val, y_val, n_repeats=30, random_state=0)
```
Measures drop in score when a feature is shuffled; model-agnostic and reliable.

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers test whether you can build end-to-end ML workflows with scikit-learn: preprocessing, validation, training, tuning, and evaluation. They want to see that you won't leak test data or overfit validation sets.

### Red Flags
- Scaling after train/test split using the full dataset (data leakage).
- Tuning hyperparameters on the test set.
- Ignoring class imbalance.
- Using accuracy on imbalanced data.

### Green Flags
- Using `Pipeline` to prevent leakage.
- Stratified splits for classification.
- Choosing metrics aligned with business cost (Fβ, recall, precision).
- Explaining bias-variance tradeoff and regularization.

### Answers Matrix
| Level | Question: "How does scikit-learn prevent data leakage?" |
|---|---|
| **Rejected** | "It just works." |
| **Shortlisted** | "Using fit on train and transform on test." |
| **Selected** | "Scikit-learn estimators learn statistics from training data only. Pipelines enforce that preprocessing steps are fit inside cross-validation, preventing information from held-out folds or the test set from leaking into training statistics." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions
1. What is the scikit-learn estimator API?
- Estimators implement `fit(X, y)` and either `predict(X)` (supervised) or `transform(X)` (unsupervised).

2. What is a Pipeline and why is it important?
- Chains preprocessing and modeling steps; prevents data leakage and ensures reproducible inference.

3. Difference between `fit`, `fit_transform`, and `transform`?
- `fit`: learn parameters.
- `transform`: apply learned parameters.
- `fit_transform`: fit and transform training data only.

4. Why must you split data before scaling?
- Scaling uses mean/std from training data only; using full dataset leaks test statistics into training.

5. What is cross-validation and why use it?
- Repeated holdout across folds reduces variance of performance estimates and uses data efficiently.

6. What is StratifiedKFold?
- Preserves class proportions in each fold for classification.

7. When would you use `RobustScaler` over `StandardScaler`?
- When outliers distort mean/std; robust scaler uses median and IQR.

8. What is the bias-variance tradeoff?
- Simple models -> high bias, low variance; complex models -> low bias, high variance.

9. What is regularization in linear models?
- Penalizes large coefficient magnitudes to reduce overfitting. L1 (lasso) produces sparsity; L2 (ridge) shrinks uniformly.

10. What is one-hot encoding and when should it be avoided?
- Converts categorical values into binary columns. Avoid with high-cardinality categories; use target encoding or embeddings instead.

11. What is the difference between bagging and boosting?
- Bagging trains independent models on bootstrap samples. Boosting trains sequentially, correcting prior errors.

12. What is a confusion matrix?
- Table of predicted vs actual classes; rows/columns encode TP, FP, FN, TN.

13. What is precision vs recall?
- Precision = TP / (TP + FP). Recall = TP / (TP + FN). Tradeoff via threshold.

14. What is ROC AUC?
- Area under true positive rate vs false positive rate curve across thresholds. 0.5 = random; 1.0 = perfect.

15. What is the difference between `RandomForestClassifier` and `GradientBoostingClassifier`?
- Random Forest: bagging, independent trees, aggressive regularization via depth. Gradient Boosting: sequential residuals, more sensitive to learning rate.

16. What is `class_weight` and when should you use it?
- Weights samples inversely to class frequency; improves recall on minority classes.

17. What is calibration of probabilities?
- Adjusting predicted probabilities to match empirical frequencies (Platt scaling, isotonic regression).

18. What is the difference between `predict` and `predict_proba`?
- `predict` returns class labels. `predict_proba` returns class probabilities.

19. What is `partial_fit` and when is it useful?
- Trains in batches without requiring full dataset in memory; useful for streaming or large datasets.

20. What is a weak learner?
- A model slightly better than random guessing; boosting combines many weak learners into a strong predictor.

### Scenario-Based Questions
21. Build a production-ready churn prediction pipeline.
- Clean data -> impute missing -> encode categories -> scale numeric -> stratified train/test split -> pipeline with classifier -> calibrate probabilities -> monitor drift.

22. You have 10M rows and 500 columns but only 8GB RAM.
- Use `partial_fit` with online learners (`SGDClassifier`, `MiniBatchKMeans`). Preprocess chunks with `ColumnTransformer`. Use sparse encodings for categorical columns.

23. Model performs great on validation but poorly on production data.
- Check for covariate shift, data leakage during validation, preprocessing mismatch, and temporal split violations.

24. Improve performance on imbalanced fraud detection.
- Use class weights, focal loss proxy (`class_weight='balanced_subsample'`), ensemble methods like BalancedRandomForest, and precision-recall AUC instead of ROC AUC.

25. Compare models quickly and fairly.
- Use cross-validation with same splits, same random seeds, common scorer. Prefer repeated KFold if variance is high.

26. How do you choose between logistic regression and random forest?
- Logistic regression is interpretable, fast, linear. Random forest captures nonlinear interactions with less tuning. Start simple.

27. A categorical column has 10k unique values in a 50k-row dataset.
- Avoid one-hot. Use target encoding with cross-validation, frequency encoding, or embeddings if using deep learning.

28. You need to explain model decisions to a business stakeholder.
- Use logistic regression coefficients, decision tree rules, SHAP values, or permutation importance.

29. Your preprocessing step depends on target labels (e.g., SMOTE).
- Place inside cross-validation loop or use Pipelines with custom transformers; never apply before split.

30. Detect data leakage in a feature engineering step.
- Inspect whether a feature contains information from the future or target. Examples: including revenue after churn date, using test summary stats in train features.

### Debugging Questions
31. Pipeline gives different train vs test performance.
- Likely leakage: preprocessing fit on full dataset, or target encoded features. Use Pipeline/CV correctly.

32. `GridSearchCV` overfits validation folds.
- Too many hyperparameter combinations relative to data. Reduce search space and use cross-validation.

33. `OneHotEncoder` fails on unseen category in test set.
- Set `handle_unknown='ignore'` to avoid errors on new categories.

34. `ValueError: Input contains NaN` during training.
- Add imputer step before classifier. Inspect missingness patterns first.

35. Model predicts same class for all samples on imbalanced data.
- Use class weights, resampling, or choose metric-sensitive algorithms.

### System Design Questions
36. Design a model retraining pipeline.
- Data freshness check -> feature recomputation -> train/validation split -> model training -> evaluation vs champion -> promotion if metrics improve -> shadow deploy -> monitoring.

37. Design a feature store interface.
- Entity + timestamp keyed feature tables. Point-in-time correctness. Offline store for training; online store for low-latency serving with cache invalidation.

38. Design a model evaluation dashboard.
- Metrics table with CIs, confusion matrix, calibration curve, per-segment performance, fairness slices, and champion/challenger comparison.

---

#### 61. Explain how ColumnTransformer prevents data leakage. How does it handle heterogeneous datasets?
- **Detailed Answer**: `ColumnTransformer` allows you to apply different preprocessing pipelines to specific subsets of columns (numeric, categorical, text) in a heterogeneous dataset, and concatenate the output features into a single matrix.
  It prevents **data leakage** because:
  1. It respects the standard estimator contract: fitting statistics (e.g., mean/standard deviation for `StandardScaler`, category mapping for `OneHotEncoder`) occurs strictly on the training folds/sets when calling `ColumnTransformer.fit()`.
  2. These parameters are then statically applied during `ColumnTransformer.transform()` on validation or test folds.
  3. When combined within an overall `Pipeline`, the entire preprocessing graph is executed within cross-validation folds, guaranteeing that no test/validation data statistics leak into the training transformations.
- **Follow-up Questions**: How do you pass through specific columns unmodified or drop columns inside a ColumnTransformer? (Answer: Use the `"passthrough"` or `"drop"` string literals as the transformer parameter in the tuple specification).
- **Interviewer's Expectations**: Define `ColumnTransformer`'s column-specific mapping capability, explain why fit-on-train and transform-on-test prevents leakages of means/categories, and describe integrating it inside a scikit-learn `Pipeline`.

---

#### 62. What is the contract for custom estimators and transformers in scikit-learn? How do you implement a custom transformer?
- **Detailed Answer**: To create custom, pipeline-compatible components in scikit-learn, you must adhere to the estimator/transformer contract:
  1. Subclass `BaseEstimator` to automatically inherit parameter inspection helpers, get/set parameter mechanisms for hyperparameter tuning (`get_params`, `set_params`), and avoid using `*args` or `**kwargs` in your `__init__`.
  2. Subclass `TransformerMixin` to automatically get the `fit_transform()` implementation from your `fit` and `transform` methods.
  3. Implement `fit(self, X, y=None)`: Learn data-driven parameters from `X` and store them as public attributes ending with a trailing underscore (e.g., `self.mean_`). It must return `self`.
  4. Implement `transform(self, X)`: Apply the learned parameters to `X` and return a new array or DataFrame without modifying the original input.
- **Follow-up Questions**: Why should learned attributes in a custom transformer end with a trailing underscore? (Answer: It is a scikit-learn convention that separates hyperparameters set in `__init__` from parameters computed during the `fit` phase).
- **Interviewer's Expectations**: Describe the inheritance of `BaseEstimator` and `TransformerMixin`, explain the signature contracts of `fit` and `transform`, and identify the trailing underscore convention for learned parameters.

---

#### 63. What is target leakage/pipeline leakage? How do you detect and fix it in scikit-learn pipelines?
- **Detailed Answer**: **Target leakage** occurs when features used to train a model contain information about the target variable that would not be available at inference time (e.g., customer transaction IDs representing fraud outcomes, or raw target values incorporated in calculation steps). **Pipeline leakage** occurs when preprocessing calculations (like scaling, mean imputation, or target encoding) are fit on the entire dataset *before* splitting into train/test or cross-validation folds, leaking test distribution data into the training process.
  - **Detection**: Check if cross-validation scores are unrealistically high compared to out-of-sample/production test scores. Inspect feature importances to see if a feature explains nearly 100% of target variance.
  - **Fix**: Package all preprocessing transformers and final estimators in a scikit-learn `Pipeline` object. Enforce validation splits *before* calling `.fit()`. Never compute global statistics on the entire dataset.
- **Follow-up Questions**: What is the difference between target encoding leakage and data leakage? (Answer: Data leakage is a general term for test data informing training, whereas target encoding leakage specifically refers to a feature calculation using target labels of the same row or fold, causing overfitting).
- **Interviewer's Expectations**: Define target leakage and pipeline leakage, identify symptoms (e.g., optimistic CV scores, dominant features), and detail how wrapping steps in a `Pipeline` resolves preprocessing leakage.

---

## 10. Common Mistakes
- Scaling using full dataset before split (data leakage).
- Hyperparameter tuning on the test set.
- Using accuracy on imbalanced data.
- Forgetting to set `random_state` for reproducibility.
- Applying encoders independently on train and test.

---

## 11. Comparison Section: Scikit-Learn vs Alternatives
| Feature | Scikit-Learn | XGBoost | TensorFlow | PyTorch |
|---|---|---|---|---|
| **Focus** | classical ML | gradient boosted trees | DL production | DL research |
| **API style** | uniform estimators | sklearn-like | Keras/programmatic | programmatic |
| **Data size** | medium | medium-large | large | large |
| **GPU** | no | optional | first-class | first-class |
| **Diagnostics** | strong | good | Keras callbacks | PyTorch Lightning |

---

## 12. Practical Project Ideas
- **Beginner**: Iris or Titanic classifier with Pipeline, CV, and evaluation report.
- **Intermediate**: Customer churn pipeline with preprocessing, model tuning, and calibration.
- **Advanced**: Stacking ensemble benchmark comparing logistic regression, random forest, and gradient boosting.

---

## 13. Internship Preparation Notes
- Data roles: preprocessing, pipelines, metrics, CV.
- ML roles: bias-variance, regularization, ensemble comparisons, leakage prevention.
- MLE roles: serialization, serving, and monitoring.

---

## 14. Cheat Sheet
- **API**: `fit`, `predict`, `transform`, `fit_transform`.
- **Preprocessing**: `StandardScaler`, `MinMaxScaler`, `OneHotEncoder`, `SimpleImputer`.
- **Models**: `LogisticRegression`, `RandomForestClassifier`, `GradientBoostingClassifier`, `SVC`.
- **CV**: `train_test_split`, `KFold`, `StratifiedKFold`, `cross_val_score`.
- **Metrics**: `accuracy_score`, `precision_recall_fscore_support`, `roc_auc_score`, `mean_squared_error`, `r2_score`.

---

## 15. One-Day Revision Guide
- [ ] List estimator API methods and contracts.
- [ ] Build Pipeline with scaler + classifier from scratch.
- [ ] Explain why scaling must be fit on train only.
- [ ] Compare bagging, boosting, and stacking.
- [ ] Compute and interpret precision, recall, F1 for a confusion matrix.
- [ ] Run GridSearchCV and interpret best params.
- [ ] Choose a metric for imbalanced classification and justify it.
