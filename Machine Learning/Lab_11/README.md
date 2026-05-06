# ML Lab 11 — Hyperparameter Tuning & AutoML

## Overview

Model performance heavily depends on hyperparameters. This lab teaches you to optimize them systematically. You'll also explore AutoML tools that automate the entire model selection process.

---

## 📚 What I Learned

### Hyperparameters vs Parameters
- **Parameters:** Learned from data (weights, coefficients)
- **Hyperparameters:** Set before training (learning rate, max depth, regularization)

### GridSearchCV
- Exhaustive search over parameter grid
- Try all combinations, select best
- Computationally expensive but thorough
- Works well for small grids
- Best for: Understanding parameter effects

### RandomSearchCV
- Random sampling of parameter space
- More efficient than grid search
- Often finds good solutions faster
- Works well with large grids
- Best for: Exploring large spaces

### AutoML (AutoGluon)
- Automated model selection and hyperparameter tuning
- Handles preprocessing, feature engineering, model selection, ensemble
- Competitive with manual tuning
- Dramatically reduces human effort
- Best for: Rapid prototyping, baseline models

### Key Hyperparameters
- **Learning Rate:** How fast model learns
- **Regularization:** L1/L2 penalty strength
- **Tree Depth:** Complexity of decision trees
- **Number of Estimators:** Ensemble size
- **Batch Size:** Samples per iteration

---

## 🎯 Learning Objectives

- ✅ Use GridSearchCV for exhaustive search
- ✅ Use RandomSearchCV for efficient exploration
- ✅ Interpret hyperparameter effects
- ✅ Apply AutoML tools
- ✅ Compare manual vs automated approaches

---

## 🛠️ What I Built

**Experiments:**
1. Grid search over decision tree parameters
2. Random search over larger parameter space
3. Compare search efficiency
4. Apply AutoGluon to same problem
5. Benchmark manual vs AutoML

**Results:**
- Grid search found optimal parameters (but slow)
- Random search found good parameters faster
- AutoGluon achieved competitive results automatically
- Huge time savings with AutoML

---

## 💡 Real-World Applications

- **Production:** AutoML enables rapid iteration
- **Prototyping:** Get baseline quickly, tune if needed
- **Research:** Grid search for publication-quality results
- **Teams:** AutoML democratizes ML for non-experts
- **Competition:** Careful tuning gives edge

---

## 🔧 Technologies Used

- sklearn.model_selection (GridSearchCV, RandomSearchCV)
- AutoGluon (automated ML)
- pandas, matplotlib

---

## 📊 Key Code Examples

**GridSearchCV:**
```python
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

params = {
    'max_depth': [3, 5, 7, 10],
    'min_samples_split': [2, 5, 10]
}
gs = GridSearchCV(DecisionTreeClassifier(), params, cv=5)
gs.fit(X_train, y_train)
print(f"Best params: {gs.best_params_}")
```

**RandomSearchCV:**
```python
from sklearn.model_selection import RandomSearchCV
rs = RandomSearchCV(DecisionTreeClassifier(), params, n_iter=10, cv=5)
rs.fit(X_train, y_train)
```

**AutoGluon:**
```python
from autogluon.tabular import TabularPredictor
predictor = TabularPredictor(label='target')
predictor.fit(train_data)
predictions = predictor.predict(test_data)
```

---

## 🚀 Next Steps

- Lab 12: Ethics in deployed models
- Master hyperparameter tuning workflow
- Use AutoML for rapid prototyping

---

## ✨ Bottom Line

Hyperparameters matter. GridSearch finds optimal values but costs computation. AutoML automates everything. Choose GridSearch for publication-quality, AutoML for production velocity.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
