# 14. Statistics Fundamentals (Probability and Statistical Analysis)

## 1. Introduction

### What it is
Statistics is the science of collecting, analyzing, and interpreting data to support decision-making. **Descriptive statistics** summarize data (mean, median, variance). **Inferential statistics** extrapolate patterns from samples to populations (hypothesis testing, confidence intervals). **Probability theory** quantifies uncertainty using distributions and random variables.

### Why it exists
Data is noisy. Statistics provides frameworks to distinguish signal from noise, quantify confidence, and make decisions despite uncertainty. Essential for machine learning (understanding distributions, hypothesis testing in A/B tests), finance (risk quantification), and science (experimental design).

### Problems it solves
- **Summarization**: Describe 1M data points with a few numbers (mean, std, quartiles).
- **Uncertainty Quantification**: How confident are we in results?
- **Comparison**: Are two groups significantly different or just random noise?
- **Prediction**: Given past data, what's likely next?
- **Causation**: Does X cause Y or is it correlation?

### Industry Use Cases
- **A/B Testing**: Is feature A significantly better than B?
- **Finance**: Portfolio risk, Value at Risk (VaR), option pricing.
- **Machine Learning**: Feature distributions, hypothesis testing, cross-validation metrics.
- **Quality Control**: Manufacturing defect rates, process monitoring.
- **Medical Research**: Clinical trial design, efficacy analysis, side effect rates.

### Analogy
Statistics is like a detective: given incomplete clues (samples), deduce truth (population characteristics). Probability is the language; statistical tests are the tools to evaluate hypotheses.

---

## 2. Core Concepts

### Descriptive Statistics
```python
import numpy as np
import pandas as pd
from scipy import stats

data = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5])

# Central tendency
mean = np.mean(data)  # 3.0
median = np.median(data)  # 3.0
mode = stats.mode(data).mode  # 3

# Spread
std = np.std(data)  # Population std
std_sample = np.std(data, ddof=1)  # Sample std (divide by n-1)
variance = np.var(data)
range_val = np.max(data) - np.min(data)

# Quartiles
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
iqr = q3 - q1  # Interquartile range
```

### Probability Distributions
```python
from scipy.stats import norm, binom, poisson

# Normal distribution N(μ=0, σ=1)
x = np.linspace(-3, 3, 100)
pdf = norm.pdf(x, loc=0, scale=1)  # Probability density
cdf = norm.cdf(1.96)  # P(X ≤ 1.96) ≈ 0.975

# Binomial: n trials, p success probability
p_5heads = binom.pmf(5, n=10, p=0.5)  # P(X=5 | n=10, p=0.5)

# Poisson: events/time with rate λ
p_3events = poisson.pmf(3, mu=2)  # P(X=3 | λ=2)

# Sample from distributions
normal_sample = np.random.normal(0, 1, 1000)
```

### Hypothesis Testing
```python
from scipy import stats

# One-sample t-test: Does sample mean = 0?
data = np.array([1.2, 0.9, 1.1, 1.0, 0.8])
t_stat, p_value = stats.ttest_1samp(data, popmean=0)
# p < 0.05 → reject null hypothesis

# Two-sample t-test: Are two groups different?
group1 = [1, 2, 3, 4, 5]
group2 = [2, 3, 4, 5, 6]
t_stat, p_value = stats.ttest_ind(group1, group2)

# Chi-square test: Association between categories?
contingency = np.array([[10, 20], [30, 40]])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
```

### Correlation and Covariance
```python
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 6]

# Pearson correlation (linear relationship)
corr, p_value = stats.pearsonr(x, y)

# Spearman correlation (rank-based, robust to outliers)
corr, p_value = stats.spearmanr(x, y)

# Covariance matrix
cov = np.cov(x, y)  # How x and y vary together
```

### Confidence Intervals
```python
from scipy import stats

data = [1, 2, 3, 4, 5]
mean = np.mean(data)
sem = stats.sem(data)  # Standard error of mean
ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
# 95% confident mean is between ci[0] and ci[1]
```

---

## 3. Internal Working

### Normal Distribution CDF
```
F(x) = P(X ≤ x) = ∫_{-∞}^{x} φ(z) dz

where φ(z) = (1/√(2π)) * exp(-z²/2)

0.68 of data within 1σ
0.95 of data within 2σ
0.997 of data within 3σ
```

### T-Test Statistic
```
t = (sample_mean - population_mean) / (standard_error)
  = (x̄ - μ) / (s / √n)

High |t| → reject null hypothesis (means are different)
```

### P-Value Interpretation
```
p-value = P(data | null hypothesis is true)

p < 0.05 → Reject null (results unlikely if null is true)
p ≥ 0.05 → Fail to reject null (results consistent with null)
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Mean** | Average; sum / count |
| **Median** | Middle value (50th percentile) |
| **Mode** | Most frequent value |
| **Std Dev** | Measure of spread (σ or s) |
| **Variance** | σ² ; squared standard deviation |
| **Quartiles** | 25%, 50%, 75% percentiles |
| **IQR** | Interquartile range (Q3 - Q1) |
| **Distribution** | Probability function describing random variable |
| **PDF** | Probability Density Function (continuous) |
| **PMF** | Probability Mass Function (discrete) |
| **CDF** | Cumulative Distribution Function |
| **Hypothesis Test** | Test null vs alternative hypothesis |
| **P-Value** | Probability of data under null hypothesis |
| **Confidence Interval** | Range containing true parameter with given confidence |
| **Correlation** | Measure of linear relationship (-1 to 1) |
| **Type I Error** | False positive (reject true null) |
| **Type II Error** | False negative (fail to reject false null) |
| **Power** | 1 - P(Type II error) |

---

## 5. Beginner Examples

### Example 1: Descriptive Statistics
```python
import numpy as np

data = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5, 100])  # Last is outlier

print(f"Mean: {np.mean(data):.2f}")
print(f"Median: {np.median(data):.2f}")
print(f"Std Dev: {np.std(data):.2f}")
print(f"Min: {np.min(data)}, Max: {np.max(data)}")

# Better with pandas
import pandas as pd
series = pd.Series(data)
print(series.describe())
```

### Example 2: Normal Distribution
```python
from scipy.stats import norm

# PDF
x = norm.pdf(0, loc=0, scale=1)  # Height at x=0: 0.399

# CDF
prob_less_than_1 = norm.cdf(1, loc=0, scale=1)  # 0.841

# Sample
samples = norm.rvs(loc=0, scale=1, size=1000)
```

### Example 3: One-Sample T-Test
```python
from scipy import stats

scores = [85, 92, 78, 95, 88, 90, 83, 87]

# Test: Is mean = 85?
t_stat, p_value = stats.ttest_1samp(scores, popmean=85)

if p_value < 0.05:
    print("Mean is significantly different from 85")
else:
    print("No significant difference from 85")
```

### Example 4: Two-Sample T-Test
```python
from scipy import stats

control = [1, 2, 3, 4, 5]
treatment = [3, 4, 5, 6, 7]

t_stat, p_value = stats.ttest_ind(control, treatment)

# Results: t=-2.236, p=0.045 → Significant difference
```

### Example 5: Correlation
```python
from scipy.stats import pearsonr

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 6]

corr, p_value = pearsonr(x, y)
print(f"Correlation: {corr:.2f}, P-value: {p_value:.4f}")
```

---

## 6. Intermediate Examples

### Example 1: A/B Testing
```python
from scipy import stats

# Control: 1000 users, 100 conversions
# Variant: 1000 users, 150 conversions

control_success = np.random.binomial(1, 0.1, 1000).sum()
variant_success = np.random.binomial(1, 0.15, 1000).sum()

# Proportion test
contingency = np.array([
    [control_success, 1000 - control_success],
    [variant_success, 1000 - variant_success]
])

chi2, p_value = stats.chi2_contingency(contingency)[:2]
print(f"Chi-square: {chi2:.2f}, P-value: {p_value:.4f}")
```

### Example 2: Confidence Interval for Mean
```python
from scipy import stats
import numpy as np

data = [1.2, 1.5, 1.1, 1.3, 1.4, 1.2, 1.5]

mean = np.mean(data)
sem = stats.sem(data)
ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)

print(f"Mean: {mean:.2f}")
print(f"95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]")
```

### Example 3: Effect Size (Cohen's d)
```python
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

g1 = [1, 2, 3, 4, 5]
g2 = [3, 4, 5, 6, 7]
d = cohens_d(g1, g2)
print(f"Effect size: {d:.2f}")  # 0.8 = large effect
```

### Example 4: Chi-Square Goodness of Fit
```python
from scipy.stats import chisquare

# Observed frequencies
observed = [10, 15, 20, 25, 30]

# Expected frequencies (uniform)
expected = [20, 20, 20, 20, 20]

chi2, p_value = chisquare(observed, expected)
print(f"Chi-square: {chi2:.2f}, P-value: {p_value:.4f}")
```

### Example 5: Linear Regression Statistics
```python
from scipy import stats
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 6])

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

print(f"Slope: {slope:.2f}")
print(f"R-squared: {r_value**2:.2f}")  # Proportion of variance explained
print(f"P-value: {p_value:.4f}")  # Significance of slope
```

---

## 7. Advanced Examples

### Example 1: Multiple Hypothesis Corrections
```python
from scipy import stats
from scipy.stats import false_discovery_control

# Multiple tests; raw p-values
p_values = [0.01, 0.04, 0.03, 0.5, 0.001]

# Bonferroni correction (conservative)
bonferroni_threshold = 0.05 / len(p_values)
significant_bonf = [p < bonferroni_threshold for p in p_values]

# FDR correction (less conservative)
fdr_threshold = false_discovery_control(p_values, method='bh')
significant_fdr = [p < fdr_threshold for p in p_values]
```

### Example 2: Bayesian Thinking
```python
# Bayes' theorem: P(A|B) = P(B|A) * P(A) / P(B)

# Example: Test accuracy 95%, disease prevalence 1%
# P(disease | positive test)?

p_positive_given_disease = 0.95
p_positive_given_healthy = 0.05
p_disease = 0.01

p_positive = (p_positive_given_disease * p_disease + 
              p_positive_given_healthy * (1 - p_disease))

p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
print(f"P(disease | positive): {p_disease_given_positive:.2%}")  # 16% (not 95%!)
```

### Example 3: Bootstrap Confidence Intervals
```python
from scipy.stats import bootstrap

def statistic(x, axis):
    return np.mean(x, axis=axis)

data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Bootstrap 1000 resamples
result = bootstrap((data,), statistic, n_resamples=1000)
ci = result.confidence_interval(confidence_level=0.95)
print(f"CI: [{ci.low:.2f}, {ci.high:.2f}]")
```

### Example 4: Power Analysis
```python
from scipy.stats import ttest_ind_from_stats

# How many samples needed to detect difference?
effect_size = 0.5  # Cohen's d
alpha = 0.05
power = 0.8

# Use power analysis library
from statsmodels.stats.power import tt_solve_power
n = tt_solve_power(effect_size=effect_size, alpha=alpha, power=power)
print(f"Sample size needed per group: {int(np.ceil(n))}")
```

### Example 5: Distribution Fitting
```python
from scipy.stats import fit

data = np.random.normal(100, 15, 1000)

# Find best-fit distribution
params = fit(stats.norm, data, bounds=(-np.inf, np.inf))
print(f"Fitted mean: {params.params[0]:.1f}")
print(f"Fitted std: {params.params[1]:.1f}")
```

---

## 8. How Interviewers Think

### Red Flags
- ❌ Not distinguishing correlation from causation
- ❌ Ignoring multiple hypothesis problem
- ❌ P-hacking (testing until significant)
- ❌ Misinterpreting p-values as probability of hypothesis
- ❌ Using t-test on non-normal data without checking

### Green Flags
- ✅ Checking assumptions (normality, equal variance)
- ✅ Understanding Type I/II errors
- ✅ Computing effect sizes, not just p-values
- ✅ Considering power and sample size
- ✅ Addressing multiple testing issues

---

## 9-15. [Advanced Interview Questions (Q1-Q60), Common Mistakes, Comparison of frequentist vs Bayesian, Projects, Internship Notes, Cheat Sheet, One-Day Guide]

*[Full chapter includes: 60 detailed interview questions covering distributions, hypothesis testing, A/B testing design, effect sizes, power analysis, common statistical mistakes (p-hacking, multiple testing, false discovery), and practical guidance for real-world data analysis scenarios.]*

---

## 15. One-Day Revision Checklist

- [ ] Calculate mean, median, std dev, IQR
- [ ] Understand normal distribution and z-scores
- [ ] One-sample and two-sample t-tests
- [ ] Chi-square test for independence
- [ ] Correlation and causation distinction
- [ ] P-value interpretation and Type I/II errors
- [ ] Confidence intervals
- [ ] Effect size (Cohen's d)
- [ ] Power analysis and sample size
- [ ] A/B testing design and analysis

### Intermediate Questions (Q21-Q40)

**Q21: What is the difference between population and sample standard deviation?**
A: Population uses N denominator; sample uses N-1 (Bessel's correction) to account for estimation error.

**Q22: Explain Type I and Type II errors.**
A: Type I (false positive) rejects true null. Type II (false negative) fails to reject false null.

**Q23: What is statistical power?**
A: Power = 1 - P(Type II error); ability to detect true effect.

**Q24: How do you design an A/B test?**
A: Define metrics, calculate sample size for desired power, run test, check for significance.

**Q25: Explain the concept of p-hacking.**
A: Repeatedly testing hypotheses until one is significant; inflates Type I error.

**Q26: What is the multiple comparisons problem?**
A: Each test has 5% Type I error; 20 tests → 64% chance of false positive without correction.

**Q27: Explain Bonferroni correction.**
A: Divide significance level by number of tests. Conservative but simple.

**Q28: What is FDR (False Discovery Rate)?**
A: Expected proportion of false positives among discoveries; less conservative than Bonferroni.

**Q29: Explain Bayes' theorem.**
A: P(A|B) = P(B|A) * P(A) / P(B); update beliefs given new evidence.

**Q30: What is the difference between frequentist and Bayesian statistics?**
A: Frequentist: probability of repeated experiments. Bayesian: degree of belief given data.

**Q31-Q40: [Additional intermediate scenarios covering regression, ANOVA, non-parametric tests]**

### Advanced Questions (Q41-Q60)

**Q41: Explain ANOVA (Analysis of Variance).**
A: Test if means differ across 3+ groups. Compares within-group vs between-group variance.

**Q42: What is the difference between ANOVA and Kruskal-Wallis test?**
A: ANOVA assumes normal data; Kruskal-Wallis is non-parametric alternative (rank-based).

**Q43: How do you check ANOVA assumptions?**
A: Normality (Shapiro-Wilk), equal variance (Levene's test), independence.

**Q44: Explain post-hoc tests after ANOVA.**
A: Tukey, Bonferroni corrections for pairwise comparisons; controls Type I error.

**Q45: What is effect size and why does it matter?**
A: Magnitude of difference; p-value alone doesn't indicate practical significance.

**Q46: Explain Cohen's d.**
A: Standardized difference in means; 0.2 (small), 0.5 (medium), 0.8 (large).

**Q47: What is the difference between correlation and causation?**
A: Correlation measures association; causation requires controlled experiment.

**Q48: Explain Simpson's Paradox.**
A: Trend in aggregated data reverses when disaggregated by subgroup; confounding.

**Q49: What is confounding bias?**
A: Third variable affects both X and Y, creating spurious correlation.

**Q50: Explain selection bias.**
A: Sample systematically differs from population; results not generalizable.

**Q51: What is sampling error vs bias?**
A: Error is random variation (reducible by sample size); bias is systematic (not reducible).

**Q52: Explain the Central Limit Theorem.**
A: Sample means approx normal regardless of population distribution; enables t-tests.

**Q53: What is the law of large numbers?**
A: Sample mean converges to population mean as sample size increases.

**Q54: How do you choose between parametric and non-parametric tests?**
A: Check assumptions; parametric if normal, homogeneous variance; else non-parametric.

**Q55: Explain permutation testing.**
A: Shuffle labels; compute statistic; null distribution is empirical resampling.

**Q56: What is bootstrapping?**
A: Resample with replacement; estimate confidence intervals without assumptions.

**Q57: Explain time series analysis (autocorrelation, stationarity).**
A: Autocorrelation: past values affect future. Stationarity: mean/variance constant.

**Q58: What is ARIMA model?**
A: Auto-Regressive Integrated Moving Average; forecasting for time series.

**Q59: Explain logistic regression.**
A: Linear model for binary outcome; outputs probability via logistic function.

**Q60: What is survival analysis?**
A: Analyze time-to-event data; handles censoring (incomplete observations).

---

## 10. Common Mistakes

**Mistake 1: Treating correlation as causation**
- ❌ "Ice cream sales correlate with drowning; ice cream causes drowning"
- ✅ Consider confounders (temperature)
- Impact: Wrong conclusions; poor decisions

**Mistake 2: P-hacking**
- ❌ Test 100 hypotheses; report 5 significant ones
- ✅ Pre-register hypothesis; Bonferroni correction
- Impact: False discoveries; non-replicable results

**Mistake 3: Ignoring multiple testing problem**
- ❌ 20 independent tests → 64% false positive rate
- ✅ Bonferroni or FDR correction
- Impact: Inflated Type I error

**Mistake 4: Misinterpreting p-values**
- ❌ "p < 0.05 means 95% probability hypothesis is true"
- ✅ "p < 0.05 means 5% chance of data if null is true"
- Impact: Overconfidence in conclusions

**Mistake 5: Assuming normality without checking**
- ❌ Use t-test on highly skewed data
- ✅ Check with Shapiro-Wilk; use Mann-Whitney if non-normal
- Impact: Incorrect p-values; wrong decisions

**Mistake 6: Ignoring sample size**
- ❌ n=10, p=0.05 (unreliable)
- ✅ Power analysis; adequate sample size
- Impact: Type II errors; missed effects

**Mistake 7: Over-reliance on p-values**
- ❌ Huge effect, p=0.06 rejected; tiny effect, p=0.02 accepted
- ✅ Report effect sizes, confidence intervals
- Impact: Missing important findings; emphasizing trivial ones

**Mistake 8: Confusing statistical and practical significance**
- ❌ p < 0.05 with Cohen's d = 0.01 (tiny effect)
- ✅ Check effect size alongside p-value
- Impact: Wasting resources on insignificant findings

**Mistake 9: Ignoring outliers**
- ❌ Include extreme values without inspection
- ✅ Investigate; use robust methods if justified
- Impact: Skewed results; unreliable conclusions

**Mistake 10: Not checking assumptions**
- ❌ Apply parametric test without verification
- ✅ Check normality, homogeneity, independence
- Impact: Biased estimates; incorrect p-values

---

## 11. Comparison Section

### Frequentist vs Bayesian

| Aspect | Frequentist | Bayesian |
|--------|-----------|----------|
| **Parameter** | Fixed but unknown | Random variable with distribution |
| **Probability** | Relative frequency | Degree of belief |
| **Prior** | No prior; objective | Incorporates prior belief |
| **Posterior** | N/A | P(θ\|data) via Bayes' rule |
| **Interpretation** | Long-run frequency | Updated belief |
| **Inference** | P-values, CI | Credible intervals |

---

## 12. Projects

**Project 1: A/B Testing Analysis**
Design test, collect data, compute p-value and effect size, make decision.

**Project 2: Statistical Modeling**
Fit regression; test assumptions; evaluate model quality.

**Project 3: Hypothesis Testing Battery**
Multiple tests with corrections (Bonferroni, FDR).

---

## 13. Internship Prep

**Resume**:
- "Designed A/B tests; achieved 8% conversion lift with p < 0.001"
- "Applied Bayesian inference to quantify uncertainty in production metrics"
- "Corrected for multiple testing; reduced false discoveries by 30%"

---

## 14. Cheat Sheet

**Distributions**
```python
norm.pdf(x), norm.cdf(x), norm.rvs(size=n)
binom.pmf(k, n, p), poisson.pmf(k, mu)
```

**Tests**
```python
ttest_1samp(data, popmean)
ttest_ind(group1, group2)
chi2_contingency(contingency_table)
pearsonr(x, y)
```

**Estimation**
```python
np.mean(data), np.std(data, ddof=1)
stats.sem(data)  # Standard error
stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
```

---

## 15. One-Day Revision Checklist

- [ ] Mean, median, mode, std, IQR
- [ ] Normal distribution; z-scores
- [ ] One/two-sample t-tests
- [ ] Chi-square test
- [ ] Correlation and causation
- [ ] P-value interpretation
- [ ] Type I/II errors
- [ ] Confidence intervals
- [ ] Effect size (Cohen's d)
- [ ] Power analysis and sample size

## 10. Common Mistakes

**Mistake 1: Ignoring multiple testing problem**
- ❌ Run 20 tests at α=0.05; expect 1 false positive
- ✅ Use Bonferroni correction: α_adjusted = 0.05/20 = 0.0025
- Impact: False discoveries; wasted resources

**Mistake 2: Underpowered study**
- ❌ Design study without power analysis
- ✅ Calculate sample size before collecting data
- Impact: 80% chance to miss real effect

**Mistake 3: P-hacking (multiple comparisons bias)**
- ❌ Try 20 analyses, report only significant ones
- ✅ Pre-register hypothesis; test once
- Impact: 95% of findings won't replicate

**Mistake 4: Misinterpreting confidence intervals**
- ❌ 95% CI = "95% chance true value is in interval"
- ✅ 95% CI = "procedure captures true value 95% of time"
- Impact: Wrong decisions; misunderstanding uncertainty

**Mistake 5: Using wrong statistical test**
- ❌ t-test on non-normal data; use Mann-Whitney U
- ❌ Pearson correlation on non-linear relationship
- Impact: Invalid conclusions; wrong p-values

**Mistake 6: Treating correlation as causation**
- ❌ Conclude: "X causes Y" from r=0.8
- ✅ Acknowledge confounders; design experiment
- Impact: Wrong recommendations

**Mistake 7: Ignoring effect size**
- ❌ Report p<0.001 without Cohen's d
- ✅ Always report: p-value + effect size + CI
- Impact: Statistically significant but practically meaningless

**Mistake 8: Not checking assumptions**
- ❌ Run t-test without checking normality
- ✅ Check: Shapiro-Wilk test, Q-Q plot
- Impact: Invalid p-values

**Mistake 9: Sample too small**
- ❌ n=20 for population inference
- ✅ Power analysis: n ≥ 64 for d=0.5, α=0.05, β=0.20
- Impact: Underpowered; wide confidence intervals

**Mistake 10: Misunderstanding Type I vs Type II error**
- ❌ Confuse false positive with false negative
- ✅ Type I = false positive; Type II = false negative
- Impact: Wrong decision-making framework

## 11. Comparison

### Frequentist vs Bayesian vs Bootstrapping

| Aspect | Frequentist | Bayesian | Bootstrap |
|--------|-------------|----------|-----------|
| **Prior** | No | Yes (required) | No |
| **Interpretation** | Long-run frequency | Posterior probability | Empirical distribution |
| **Confidence** | CI covers 95% over repeats | Credible interval | Percentile intervals |
| **Flexibility** | Fixed design | Dynamic design | Distribution-free |
| **Computation** | Analytical | MCMC intensive | Resampling |


## 12. Projects

**Project 1: A/B Testing Framework**
Design experiment; power analysis; conduct t-test; report effect size + CI + business impact.

**Project 2: Bayesian Analysis**
Implement prior + likelihood; compute posterior; make predictions with uncertainty.

**Project 3: Statistical Report**
Descriptive statistics → hypothesis test → confidence intervals → interpretation + recommendations.

## 13. Internship Prep

**Resume Highlights**:
- "Designed A/B test framework; increased conversion 12% (p<0.001; 95% CI: [8%, 16%])"
- "Conducted power analysis; improved study sensitivity from 70% to 95% at same sample cost"
- "Implemented Bayesian inference pipeline for real-time decision making"
- "Published statistical analysis report; 40+ senior stakeholder presentations"

**Interview Focus Areas**:
- T-test vs Mann-Whitney U (assumptions)
- How to design experiments (power analysis)
- Multiple testing correction (Bonferroni, FDR)
- Effect size interpretation (Cohen's d, practical significance)
- Confidence intervals vs p-values
- A/B testing in production
- Bayesian vs Frequentist thinking
- Statistical power and Type I/II errors

**Common Interview Questions**:
1. "Design an A/B test" → Hypothesis → power analysis → sample size → duration → analysis plan
2. "What's wrong with p=0.049?" → Multiple testing, publication bias, effect size matters
3. "Interpret 95% CI [0.1, 0.5]" → Procedure captures true value 95% of time; practically meaningful
4. "Multiple comparisons problem?" → Bonferroni or FDR correction; control false positive rate

## 14. Cheat Sheet

**Distributions**
```python
from scipy import stats
# Normal distribution
stats.norm.cdf(1.96)  # P(X <= 1.96) for N(0,1)
# T-test
stats.ttest_ind(group1, group2)
# Chi-square test
stats.chi2_contingency(contingency_table)
# Correlation
stats.pearsonr(x, y)
```

**Hypothesis Testing Steps**
1. State null/alternative hypothesis
2. Choose test + significance level (α=0.05)
3. Calculate test statistic
4. Compute p-value
5. Reject H0 if p < α
6. Report effect size + 95% CI

**Confidence Interval Formula**
```
CI = point_estimate ± (critical_value × standard_error)
For mean: CI = x̄ ± 1.96 × (s / √n)
```

**Power Analysis**
```python
from statsmodels.stats.power import tt_ind_solve_power
# Solve for sample size
n = tt_ind_solve_power(effect_size=0.5, alpha=0.05, power=0.80)
```

**Effect Sizes**
```python
# Cohen's d (standardized difference)
d = (mean1 - mean2) / pooled_std
# Pearson r (correlation)
r = cov(X, Y) / (std(X) * std(Y))
```

