# 16. Machine Learning Fundamentals

## 1. Introduction
### What it is
Machine Learning is a subfield of AI focused on algorithms that improve performance on a task through experience (data). Classical ML covers supervised, unsupervised, and reinforcement learning paradigms with mathematical foundations in statistics and optimization.

### Why it exists
Traditional software requires explicit rules for every scenario. ML learns patterns from data, generalizing to unseen inputs. This enables spam detection, recommendation, fraud detection, and speech recognition without hand-coding every rule.

### Problems it solves
- **Pattern Discovery**: Finding structure in high-dimensional data.
- **Prediction**: Estimating unknown outputs from inputs.
- **Automation**: Scaling decisions that would be impossible to hand-code.
- **Adaptation**: Updating models as new data arrives (online learning).

### Industry Use Cases
- **Finance**: Credit scoring, fraud detection, algorithmic trading.
- **Healthcare**: Disease prediction, drug discovery, medical imaging.
- **E-commerce**: Recommendation systems, demand forecasting.
- ** autonomous systems**: Self-driving cars, robotics.

### Analogy
ML is like a student learning from practice problems (data) rather than memorizing a textbook (rules). The student improves by identifying patterns and correcting mistakes.

---

## 2. Core Concepts

### Beginner Concepts
- **Features vs Targets**: Input variables (X) and output labels (y).
- **Training vs Inference**: Learning from data vs. using the learned model.
- **Overfitting vs Underfitting**: Memorizing noise vs. being too simple.
- **Bias-Variance Tradeoff**: Model complexity balancing act.
- **Loss Functions**: Measuring prediction error (MSE, cross-entropy).

### Intermediate Concepts
- **Gradient Descent**: Optimization algorithm minimizing loss.
- **Learning Rate**: Step size for gradient updates.
- **Regularization**: L1 (Lasso), L2 (Ridge), Elastic Net.
- **Cross-Validation**: k-fold, stratified, leave-one-out.
- **Hyperparameter Tuning**: Grid search, random search, Bayesian optimization.
- **Feature Engineering**: Transformation, selection, dimensionality reduction.

### Advanced Concepts
- **Ensemble Methods**: Random forests, gradient boosting, stacking.
- **Kernel Methods**: SVM kernels (RBF, polynomial, sigmoid).
- **Dimensionality Reduction**: PCA, t-SNE, UMAP.
- **Bayesian Learning**: Bayesian linear regression, Gaussian processes.
- **Online Learning**: Stochastic gradient descent, bandit algorithms.
- **Causal ML**: Uplift modeling, causal forests, treatment effects.

---

## 3. Internal Working

### Learning Process Diagram
```
Training Data (X, y)
      |
      v
Model Initialization (random weights/parameters)
      |
      v
Forward Pass: predictions = model(X)
      |
      v
Loss Calculation: compare predictions to true labels
      |
      v
Backward Pass: compute gradients via chain rule
      |
      v
Parameter Update: weights -= learning_rate * gradients
      |
      v (repeat until convergence)
Trained Model
```
The "learning" is really optimization: finding parameters that minimize a loss function over training data.

### Gradient Descent Intuition
```text
Loss Landscape (3D surface)
   ^
 H |     * (minimum)
 i |    / \
 g |   /   \
 h |  /  *  \  (* = current parameter position)
   | /       \
   +------------> Parameter space
```
Gradient descent follows the steepest downhill direction. Learning rate controls step size; too large = oscillation, too small = slow convergence.

### Bias-Variance Decomposition
```text
Total Error = Bias² + Variance + Irreducible Error

High Bias (Underfitting):    High Variance (Overfitting):
  Simple model misses          Complex model captures
  true patterns                noise in training data
```
Cross-validation helps detect and diagnose these regimes.

---

## 4. Important Terminology
- **Hypothesis**: Candidate function mapping inputs to outputs.
- **Loss Function**: Penalizes incorrect predictions (cost).
- **Objective Function**: Function to optimize (often loss + regularization).
- **Gradient**: Vector of partial derivatives showing steepest ascent.
- **Learning Rate**: Step size for parameter updates.
- **Epoch**: Full pass through training dataset.
- **Batch**: Subset of examples processed before parameter update.
- **Feature**: measurable property used as input.
- **Label**: Target output for supervised learning.
- **Train/Validation/Test**: Data splits for learning, tuning, evaluation.

---

## 5. Beginner Examples

### Example 1: Linear Regression from Scratch
```python
import numpy as np

# Generate synthetic data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Add bias term
X_b = np.c_[np.ones((100, 1)), X]

# Normal equation: theta = (X^T X)^(-1) X^T y
theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
print("Learned parameters:", theta.flatten())  # Should be close to [4, 3]
```

### Example 2: Polynomial Regression with Scikit-Learn
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

# Transform to polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)
print("R² score:", lin_reg.score(X_poly, y))
```

### Example 3: Classification with Decision Boundaries
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=200, n_features=2, n_informative=2,
                           n_redundant=0, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = LogisticRegression().fit(X_train, y_train)
print("Accuracy:", clf.score(X_test, y_test))
```

---

## 6. Intermediate Examples

### Example 1: Cross-Validation for Model Selection
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('ridge', Ridge(alpha=1.0))
])

scores = cross_val_score(pipe, X, y, cv=5, scoring='neg_mean_squared_error')
print("CV MSE:", -scores.mean().round(2))
```
Negative MSE is sklearn convention; higher is better for scoring.

### Example 2: Hyperparameter Tuning with Random Search
```python
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint

param_dist = {
    'n_estimators': randint(50, 300),
    'max_depth': [3, 5, 10, None],
    'min_samples_split': randint(2, 11)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions=param_dist,
    n_iter=20, cv=3, random_state=42
)
random_search.fit(X_train, y_train)
print("Best params:", random_search.best_params_)
```

### Example 3: Feature Selection with Mutual Information
```python
from sklearn.feature_selection import SelectKBest, mutual_info_classif

selector = SelectKBest(mutual_info_classif, k=5)
X_selected = selector.fit_transform(X, y)
mask = selector.get_support()
print("Selected features:", np.where(mask)[0])
```
Mutual information measures statistical dependence between feature and target.

### Example 4: Learning Curves for Diagnosing Bias/Variance
```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

train_sizes, train_scores, val_scores = learning_curve(
    RandomForestClassifier(n_estimators=100),
    X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
)

plt.plot(train_sizes, train_scores.mean(axis=1), label='train')
plt.plot(train_sizes, val_scores.mean(axis=1), label='validation')
plt.xlabel('Training set size')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
```
Wide gap between train and val curves indicates high variance.

---

## 7. Advanced Concepts

### Regularization Paths and Model Complexity
```python
from sklearn.linear_model import LogisticRegression
import numpy as np

C_values = np.logspace(-3, 3, 20)
coefs = []
for C in C_values:
    model = LogisticRegression(penalty='l2', C=C, solver='lbfgs')
    model.fit(X_train, y_train)
    coefs.append(model.coef_[0])

coefs = np.array(coefs)
plt.figure(figsize=(8, 5))
plt.plot(C_values, coefs)
plt.xscale('log')
plt.xlabel('C (inverse regularization)')
plt.ylabel('Coefficient magnitude')
plt.title('Regularization Path')
plt.show()
```
Smaller C = stronger regularization = smaller coefficients.

### Ensemble Methods Comparison
```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

models = {
    'RF': RandomForestClassifier(n_estimators=200),
    'GB': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1),
    'LR': LogisticRegression(max_iter=1000),
    'SVM': SVC(kernel='rbf')  # probability=True for predict_proba
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"{name}: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

### Imbalanced Data Strategies
```python
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

classes = np.unique(y_train)
weights = compute_class_weight('balanced', classes=classes, y=y_train)
class_weights = dict(zip(classes, weights))
# Use with: model = RandomForestClassifier(class_weight=class_weights)
```
Alternatives: SMOTE, ADASYN, focal loss proxies.

---

## 8. How Interviewers Think

### Interviewer's Perspective
They test your ability to take raw data to production model with proper validation, avoiding data leakage and overfitting. They want to know you understand *why* each step matters, not just API calls.

### Red Flags
- Scaling before train/test split.
- Tuning on test set.
- Using accuracy for imbalanced data.
- Not knowing when to use cross-validation.
- Ignoring feature engineering.

### Green Flags
- Explaining train/val/test split necessity.
- Understanding bias-variance tradeoff.
- Choosing appropriate metrics (precision/recall for imbalanced).
- Using pipelines to prevent leakage.
- Knowing when to use which algorithm.

### Answers Matrix
| Level | Question: "What is the bias-variance tradeoff?" |
|---|---|
| **Rejected** | "Balancing model complexity." |
| **Shortlisted** | "Simple models underfit, complex models overfit." |
| **Selected** | "Bias is error from wrong assumptions (underfitting); variance is error from sensitivity to training noise (overfitting). Increasing complexity reduces bias but increases variance. The goal is minimizing total expected error by finding the sweet spot, diagnosed via learning curves and cross-validation." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions
1. What is the difference between supervised and unsupervised learning?
- Supervised uses labeled data to predict targets. Unsupervised finds patterns without labels.

2. Explain the bias-variance tradeoff.
- High bias: model too simple, underfits. High variance: model too complex, overfits. We seek balance.

3. What is cross-validation and why is it important?
- Repeated train/validation splitting reduces performance estimate variance and uses data efficiently.

4. What is regularization? L1 vs L2?
- Penalizes large coefficients to reduce overfitting. L1 produces sparsity; L2 shrinks uniformly.

5. What is the difference between batch and mini-batch gradient descent?
- Batch uses all data per update (noisy-free but slow). Mini-batch uses subset (faster, noisier steps).

6. What is a learning rate and how do you choose it?
- Step size for gradient updates. Too large = oscillation; too small = slow convergence. Use schedule or learning rate finder.

7. What is the difference between classification and regression?
- Classification predicts discrete labels. Regression predicts continuous values.

8. What is the difference between bagging and boosting?
- Bagging trains independent models on bootstrap samples. Boosting trains sequentially, correcting prior errors.

9. What is the difference between parametric and nonparametric models?
- Parametric have fixed number of parameters (linear regression). Nonparametric grow complexity with data (KNN, trees).

10. What is the curse of dimensionality?
- As features increase, data becomes sparse; distance metrics lose meaning and models overfit.

11. What is the difference between precision and recall?
- Precision = TP / (TP + FP). Recall = TP / (TP + FN). Tradeoff via threshold.

12. What is ROC AUC and when should you not use it?
- Area under TPR vs FPR curve. Not ideal for highly imbalanced data; use PR AUC instead.

13. What is the difference between L1 and L2 regularization?
- L1 (Lasso) sets some coefficients to zero (sparsity). L2 (Ridge) shrinks all coefficients.

14. What is the difference between online learning and batch learning?
- Online updates after each example; batch trains on full dataset.

15. What is feature engineering?
- Creating informative features from raw data. Often the biggest performance lever.

16. What is the difference between correlation and causation?
- Correlation measures association. Causation requires controlled experiments or causal assumptions.

17. What is the difference between a parameter and a hyperparameter?
- Parameters are learned from data. Hyperparameters are set before training.

18. What is the difference between a model and an algorithm?
- Algorithm is the learning procedure. Model is the learned function/policy.

19. What is the difference between generative and discriminative models?
- Generative models joint distribution p(x,y). Discriminative models conditional p(y|x).

20. What is the difference between ensemble and single models?
- Ensemble combines multiple models for better performance than any single model.

### Scenario-Based Questions
21. Your model performs great on training but poorly on test data.
- Overfitting. Solutions: more data, regularization, simpler model, cross-validation.

22. You have 1M samples but only 50 features.
- Tree-based models or linear models work well. Add polynomial features if needed. Consider feature importance for interpretation.

23. How do you handle categorical features with many levels?
- Target encoding, frequency encoding, or embeddings for high-cardinality. Avoid one-hot for 1000+ levels.

24. Your dataset has 30% missing values. What do you do?
- Understand missingness mechanism (MCAR, MAR, MNAR). Use imputation (mean, median, KNN, model-based) or add missing indicator.

25. How do you select features for a high-dimensional dataset?
- Filter methods (mutual info, chi-squared), wrapper methods (RFE), embedded methods (L1, tree importance).

26. Design a recommendation system for an e-commerce site.
- Collaborative filtering (user-item matrix), content-based (item features), hybrid approach with ALS or matrix factorization.

27. Your model needs to update in real-time as new data arrives.
- Use online learning algorithms (SGD, online random forests), or periodic retraining pipeline.

28. How do you measure fairness in ML models?
- Disaggregated metrics across protected groups (demographic parity, equalized odds, calibration).

29. Your model has 95% accuracy but 0 recall on the minority class.
- Accuracy is misleading on imbalanced data. Switch metric to F1, PR AUC, or use class weights/resampling.

30. How do you deploy a model in production?
- Serialize model (pickle, joblib), wrap in API (FastAPI/Flask), containerize with Docker, monitor for drift.

### Debugging Questions
31. Model predictions are all the same class.
- Check class imbalance, loss function, and whether model is actually learning (check gradients).

32. Cross-validation scores vary wildly.
- Data too small, or model unstable (high variance). Use stratified k-fold, increase data, or regularize.

33. Feature importance shows all features have zero importance.
- Model not learning, or features are uninformative, or labels are random.

34. Model trains fine but inference is very slow.
- Model too complex, features too many, or implementation inefficient (Python loops vs vectorized).

35. Predictions are consistently biased.
- Check for data leakage, label noise, or systematic bias in training data.

### System Design Questions
36. Design a fraud detection system.
- Real-time feature engineering, ensemble model (gradient boosting + rules), online learning for concept drift, feedback loop.

37. Design a customer churn prediction pipeline.
- Feature store with customer behavior metrics, monthly retraining, A/B testing, monitoring for distribution shift.

38. Design a credit scoring model.
- Interpretable model (logistic regression with FICO-like scorecard), regulatory compliance, explainability features.

---

## 10. Common Mistakes
- **Data leakage**: Using test information in training.
- **Overfitting to validation set**: Tuning too many times on same validation.
- **Ignoring class imbalance**: Accuracy as sole metric.
- **Not understanding data**: Skipping EDA.
- **Premature optimization**: Complex models before trying simple baselines.
- **No baseline**: Not comparing against simple models.

---

## 11. Comparison Section: ML Algorithms
| Algorithm | Type | Speed | Interpretability | Best For |
|---|---|---|---|---|
| **Linear Regression** | Regression | Fast | High | Continuous targets, sparse |
| **Logistic Regression** | Classification | Fast | High | Binary/multiclass, sparse |
| **Decision Tree** | Both | Medium | High | Interpretable rules |
| **Random Forest** | Both | Medium | Medium | Tabular, non-linear |
| **GBM (XGBoost)** | Classification/Regression | Medium | Low | Tabular competitions |
| **SVM (RBF)** | Classification/Regression | Slow | Low | Small-medium datasets |
| **KNN** | Both | Slow | Low | Small datasets, local patterns |

---

## 12. Practical Project Ideas
- **Beginner**: Iris or Titanic classifier with cross-validation and hyperparameter search.
- **Intermediate**: Customer churn prediction with feature engineering and model comparison.
- **Advanced**: Stacking ensemble benchmarking multiple classical models.

---

## 13. Internship Preparation Notes
- Data roles: preprocessing, pipelines, cross-validation, metrics.
- ML roles: bias-variance, regularization, ensemble methods, leakage prevention.
- MLE roles: serialization, serving, monitoring.

---

## 14. Cheat Sheet
- **Supervised**: labeled data, predict target.
- **Unsupervised**: no labels, find structure.
- **Evaluation**: train/val/test split, cross-validation.
- **Metrics**: accuracy, precision, recall, F1, ROC AUC, MAE, RMSE, R².
- **Algorithms**: linear models, trees, forests, boosting, SVM, KNN.
- **Preprocessing**: scaling, encoding, imputation, feature selection.

---

## 15. One-Day Revision Guide
- [ ] Define supervised vs unsupervised vs reinforcement learning.
- [ ] Draw and explain bias-variance tradeoff.
- [ ] Explain train/val/test split and cross-validation.
- [ ] Compare regularization methods (L1/L2/ElasticNet).
- [ ] List 3 metrics for classification and regression.
- [ ] Describe overfitting symptoms and remedies.
- [ ] Write code for a simple logistic regression with scikit-learn.
- [ ] Compare random forest vs gradient boosting.
- [ ] Explain feature engineering importance with one example.
- [ ] Design a basic ML pipeline from raw data to prediction.
