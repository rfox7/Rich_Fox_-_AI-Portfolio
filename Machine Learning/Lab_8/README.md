# ML Lab 8 — The Bias-Variance Tradeoff

## Overview

This is one of the most important concepts in machine learning. Every model faces a fundamental tension between being too simple (underfitting) and too complex (overfitting). Understanding and navigating this tradeoff is essential for building models that generalize.

---

## 📚 What I Learned

### Underfitting (High Bias)
- Model too simple, ignores patterns
- Performs poorly on training AND test data
- Solution: Use more complex model or add features
- Example: Linear model on non-linear data

### Overfitting (High Variance)
- Model too complex, memorizes noise
- Performs well on training data, poorly on test data
- Solution: Regularization, more data, simpler model
- Example: Deep decision tree on small dataset

### The Tradeoff
- Simple model = high bias, low variance (underfitting)
- Complex model = low bias, high variance (overfitting)
- Sweet spot = balanced generalization

### Regularization Techniques
- **L1 (Lasso):** Shrinks coefficients to zero (feature selection)
- **L2 (Ridge):** Shrinks coefficients smoothly (smooth penalty)
- **Elastic Net:** Combination of L1 and L2
- **Early Stopping:** Stop training before overfitting
- **Dropout:** Random feature removal during training

### Validation Strategies
- Train/test split: Basic separation
- Cross-validation: More robust estimates
- Learning curves: Visualize bias vs variance
- Train/val/test split: True validation

---

## 🎯 Learning Objectives

- ✅ Understand underfitting and overfitting
- ✅ Recognize overfitting in train/test performance
- ✅ Apply regularization techniques
- ✅ Use cross-validation effectively
- ✅ Find the generalization sweet spot

---

## 🛠️ What I Built

**Experiments:**
1. Train models of increasing complexity
2. Plot train vs test error
3. Apply L1 and L2 regularization
4. Compare with and without regularization
5. Use learning curves to diagnose problems

**Results:**
- Unregularized model showed clear overfitting
- Regularization improved test performance
- Learning curves revealed where additional data helps

---

## 💡 Real-World Insights

- Overfitting is the #1 cause of model failure in production
- Validation must happen on unseen data
- Regularization is not optional
- Learning curves inform next actions (more data? more features? simpler model?)

---

## 🔧 Technologies Used

- sklearn.linear_model (Ridge, Lasso, ElasticNet)
- sklearn.model_selection (cross_val_score, learning_curve)
- matplotlib (visualization of tradeoff)

---

## 📊 Key Code Examples

**Ridge Regression:**
```python
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)  # Higher alpha = more regularization
model.fit(X_train, y_train)
```

**Lasso Regression:**
```python
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)  # Sparse solutions
model.fit(X_train, y_train)
```

**Cross-Validation:**
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='neg_mse')
```

---

## 🚀 Next Steps

- Lab 9: Ensemble methods reduce variance
- Lab 11: Hyperparameter tuning finds optimal alpha
- Always check train/test gap

---

## ✨ Bottom Line

The bias-variance tradeoff is unavoidable. Your job is to find the sweet spot where your model generalizes well. Regularization, cross-validation, and learning curves are your tools.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
