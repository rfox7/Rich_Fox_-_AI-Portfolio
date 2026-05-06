# ML Lab 7 — Better Model Evaluation

## Overview

Accuracy alone is misleading. This lab teaches you sophisticated evaluation techniques: confusion matrix, precision, recall, F1-score, and cross-validation. These metrics tell you how your model really performs.

---

## 📚 What I Learned

### The Confusion Matrix
Breakdown of predictions into four categories:
- **TP (True Positive):** Correctly predicted positive
- **TN (True Negative):** Correctly predicted negative  
- **FP (False Positive):** Incorrectly predicted positive (Type I error)
- **FN (False Negative):** Incorrectly predicted negative (Type II error)

### Key Metrics
- **Precision:** TP/(TP+FP) - Of predicted positives, how many correct?
- **Recall:** TP/(TP+FN) - Of actual positives, how many found?
- **F1-Score:** 2(P×R)/(P+R) - Balanced metric
- **AUC-ROC:** Model's ability to rank positives above negatives

### When to Use What
- **High Recall:** Medical diagnosis (don't miss cases)
- **High Precision:** Spam detection (minimize false alarms)
- **Balanced:** Fraud detection (both matter)

### Cross-Validation
- K-fold cross-validation for robust estimates
- Reduces variance from train/test split
- Catches overfitting early

---

## 🎯 Learning Objectives

- ✅ Create and interpret confusion matrices
- ✅ Calculate precision, recall, F1-score
- ✅ Understand metric trade-offs
- ✅ Perform cross-validation
- ✅ Select metrics appropriate for problem

---

## 🛠️ What I Built

**Analysis:**
1. Train multiple models
2. Generate confusion matrices
3. Calculate all metrics
4. Perform k-fold cross-validation
5. Compare models using appropriate metrics

**Insights:**
- Different models have different precision/recall trade-offs
- Cross-validation more reliable than single train/test split
- Metric choice depends on business problem

---

## 💡 Real-World Applications

| Domain | Priority | Why |
|---|---|---|
| Medical | High Recall | Missing disease = dangerous |
| Spam | High Precision | False alarm = user annoyance |
| Fraud | Balanced | Both false positives and false negatives costly |
| Security | High Recall | Can't miss threats |

---

## 🔧 Technologies Used

- sklearn.metrics (confusion_matrix, precision_recall_fscore_support)
- sklearn.model_selection (cross_val_score, StratifiedKFold)
- pandas, matplotlib

---

## 📊 Key Code Examples

**Confusion Matrix:**
```python
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
```

**Metrics:**
```python
from sklearn.metrics import precision_recall_fscore_support
p, r, f, _ = precision_recall_fscore_support(y_test, y_pred)
```

**Cross-Validation:**
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
print(f"Mean: {scores.mean()}, Std: {scores.std()}")
```

---

## 🚀 Next Steps

- Lab 8: Address overfitting with regularization
- Lab 9: Use ensemble methods for better performance
- Lab 7 insights guide model selection

---

## ✨ Bottom Line

Accuracy hides important information. Precision, recall, and F1-score reveal the true story. Choose metrics aligned with your problem's real-world consequences.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
