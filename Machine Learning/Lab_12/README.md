# ML Lab 12 — Ethics, Fairness & Bias in ML

## Overview

This is perhaps the most critical lab. Machine learning models inherit and amplify biases from training data and can discriminate against groups. Building fair, ethical systems is non-negotiable in production.

---

## 📚 What I Learned

### Sources of Bias
1. **Representation Bias:** Data doesn't represent all populations
2. **Measurement Bias:** How outcomes are measured affects fairness
3. **Aggregation Bias:** Treating diverse groups as monolithic
4. **Evaluation Bias:** Metrics not equally appropriate for all groups
5. **Feedback Loops:** Model predictions influence future data

### Real-World Examples
- **Hiring:** Resume screening biased against minorities
- **Lending:** Loan approvals discriminate against protected groups
- **Criminal Justice:** Risk assessment biased by historical data
- **Healthcare:** Medical algorithms worse for Black patients
- **Content:** Recommendation systems show filter bubbles

### Fairness Metrics
- **Demographic Parity:** Equal positive rates across groups
- **Equalized Odds:** Equal TPR and FPR across groups
- **Calibration:** Predicted probability = actual probability
- **Individual Fairness:** Similar people treated similarly

### Mitigation Strategies
1. **Data:** Diverse, representative training data
2. **Features:** Careful feature selection, avoid proxies
3. **Evaluation:** Test fairness across subgroups
4. **Monitoring:** Continuous audit in production
5. **Transparency:** Explain decisions to stakeholders

### Ethical Framework
- **Transparency:** Explain how decisions are made
- **Accountability:** Audit trail, human review
- **Fairness:** Measure and mitigate bias
- **Privacy:** Protect sensitive data
- **Responsibility:** Consider real-world impact

---

## 🎯 Learning Objectives

- ✅ Recognize sources of bias
- ✅ Calculate fairness metrics
- ✅ Detect bias in model predictions
- ✅ Understand real-world implications
- ✅ Design ethical ML systems

---

## 🛠️ What I Built

**Analysis:**
1. Train classification model
2. Evaluate performance overall
3. Analyze performance by demographic groups
4. Identify disparities
5. Test statistical significance
6. Propose mitigation strategies

**Findings:**
- Model accuracy varied significantly by group
- Some groups systematically disadvantaged
- Fairness metrics revealed patterns hidden by overall accuracy
- Mitigation requires intentional design

---

## 💡 Real-World Implications

| Domain | Risk | Consequence |
|---|---|---|
| **Hiring** | Discriminatory screening | Exclude qualified candidates |
| **Lending** | Unfair loan decisions | Perpetuate wealth inequality |
| **Criminal Justice** | Biased risk scores | Harsher sentences for minorities |
| **Healthcare** | Unequal treatment | Health disparities worsen |
| **Ads** | Discriminatory targeting | Reduce opportunities |

### Legal & Regulatory
- GDPR: Right to explanation
- Equal Employment Opportunity Laws: Hiring discrimination illegal
- Fair Housing Act: Housing discrimination illegal
- Algorithmic Accountability Act: Audit requirements

---

## 🔧 Technologies Used

- Statistical tests for bias detection
- Fairness libraries (AI Fairness 360, Fairness Indicators)
- pandas for group analysis
- matplotlib for fairness metrics visualization

---

## 📊 Key Code Examples

**Group Performance Analysis:**
```python
df['group'] = df['demographic_column']
for group in df['group'].unique():
    group_data = df[df['group'] == group]
    accuracy = (predictions == group_data['target']).mean()
    print(f"Accuracy for {group}: {accuracy:.3f}")
```

**Demographic Parity:**
```python
# Check if positive rate equal across groups
for group in df['group'].unique():
    pos_rate = df[df['group'] == group]['prediction'].mean()
    print(f"Positive rate for {group}: {pos_rate:.3f}")
```

**Statistical Test:**
```python
from scipy.stats import chi2_contingency
# Test if prediction and group are independent
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(f"p-value: {p_value:.4f}")  # Low p-value = bias exists
```

---

## 🚀 Next Steps

- Always audit models for fairness
- Include ethics review in deployment
- Monitor production for bias drift
- Engage affected communities
- Build diverse teams

---

## ✨ Bottom Line

Ethical AI is not optional. Models reflect training data biases. You must intentionally design fair systems, measure fairness, and continuously monitor. The real-world consequences of algorithmic bias are serious.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
