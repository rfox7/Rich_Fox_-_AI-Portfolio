# ML Lab 9 — Ensemble Methods

## Overview

Combining multiple models often produces better predictions than any single model. This lab explores ensemble methods: random forests, boosting, and voting classifiers. Most winning solutions use ensembles.

---

## 📚 What I Learned

### Random Forests
- Ensemble of decision trees
- Each tree trained on random data sample (bagging)
- Predictions averaged across trees
- Reduces variance, handles overfitting better
- Feature importance from ensemble

### Gradient Boosting
- Sequential ensemble approach
- Each tree corrects errors of previous trees
- Focus on hard examples
- More powerful but slower than bagging
- Variants: XGBoost, LightGBM, CatBoost

### Bagging vs Boosting
- **Bagging:** Parallel trees, reduces variance
- **Boosting:** Sequential, reduces bias
- Different philosophies for different problems

### Voting Classifiers
- Combine diverse algorithms
- Hard voting: Majority rule
- Soft voting: Average probabilities
- Diversity > accuracy of individuals

### Ensemble Advantages
- Better generalization
- Reduced overfitting
- Robustness to outliers
- Capture complex patterns

---

## 🎯 Learning Objectives

- ✅ Understand bagging vs boosting
- ✅ Build random forests
- ✅ Apply gradient boosting
- ✅ Create voting classifiers
- ✅ Compare ensemble vs individual models

---

## 🛠️ What I Built

**Experiments:**
1. Train individual models (logistic, tree, SVM)
2. Create random forest
3. Apply gradient boosting
4. Build voting classifier
5. Compare performance

**Results:**
- Random forest outperformed single decision tree
- Gradient boosting achieved highest accuracy
- Voting classifier combined strengths of diverse models
- Ensemble > any individual model

---

## 💡 Real-World Applications

- Kaggle competitions: #1 winning solutions are ensembles
- Production systems: Stack multiple models for robustness
- Risk management: Ensemble diversity reduces failure modes
- Scientific prediction: Combine model classes for stability

---

## 🔧 Technologies Used

- sklearn.ensemble (RandomForest, GradientBoosting, VotingClassifier)
- XGBoost, LightGBM (advanced boosting)
- pandas, matplotlib

---

## 📊 Key Code Examples

**Random Forest:**
```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X_train, y_train)
importance = model.feature_importances_
```

**Gradient Boosting:**
```python
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)
```

**Voting Classifier:**
```python
from sklearn.ensemble import VotingClassifier
ensemble = VotingClassifier(estimators=[
    ('lr', LogisticRegression()),
    ('rf', RandomForestClassifier()),
    ('svm', SVC())
], voting='soft')
ensemble.fit(X_train, y_train)
```

---

## 🚀 Next Steps

- Lab 10: Unsupervised learning for new insights
- Lab 11: Hyperparameter tuning of ensembles
- Explore advanced boosting (XGBoost, LightGBM)

---

## ✨ Bottom Line

Ensembles are powerful. Combine diverse models and you get better predictions than any single approach. This is why ensembles dominate competitions and production systems.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
