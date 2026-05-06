# ML Lab 6 — Regression & Classification Models

## Overview

This lab introduces your first predictive models. You'll learn the difference between regression (predicting continuous values) and classification (predicting categories), and build models for both tasks.

---

## 📚 What I Learned

### Regression vs Classification

**Regression:**
- Predict continuous numerical values
- Output: Any number in range
- Examples: House prices, temperature, age
- Metrics: Mean squared error, R² score

**Classification:**
- Predict discrete categories/classes
- Output: Specific class labels
- Examples: Spam/not spam, disease/healthy
- Metrics: Accuracy, precision, recall, F1

### Linear Regression
- Find best-fitting line through data
- Model: y = mx + b (with multiple features)
- Coefficients show feature importance
- Simple, interpretable, often effective

### Logistic Regression
- Despite name, used for classification
- Outputs probability of class membership
- Decision boundary at probability = 0.5
- Works well with linear relationships

### Decision Trees
- Interpretable models (show decision rules)
- Work for both regression and classification
- Split features to minimize impurity
- Can overfit easily (addressed in Lab 8)

---

## 🎯 Learning Objectives

- ✅ Understand regression vs classification
- ✅ Build linear regression model
- ✅ Build logistic regression model
- ✅ Understand decision trees
- ✅ Compare model performance

---

## 🛠️ What I Built

**Tasks:**
1. Linear Regression: Predict fare from age and pclass
2. Logistic Regression: Predict Titanic survival
3. Decision Tree: Both regression and classification

**Results:**
- Linear model achieved reasonable R² score
- Logistic model achieved good classification accuracy
- Trees showed interpretable decision paths

---

## 💡 Real-World Applications

- **Regression:** Real estate pricing, stock prediction, demand forecasting
- **Classification:** Medical diagnosis, credit approval, email filtering
- **Interpretability:** Decision trees preferred when explanation crucial

---

## 🔧 Technologies Used

- sklearn.linear_model (LinearRegression, LogisticRegression)
- sklearn.tree (DecisionTreeClassifier/Regressor)
- pandas, NumPy, Matplotlib

---

## 📊 Key Code Examples

**Linear Regression:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

**Logistic Regression:**
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
probability = model.predict_proba(X_test)
```

**Decision Tree:**
```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)
```

---

## 🚀 Next Steps

- Lab 7: Evaluate models beyond accuracy
- Lab 8: Address overfitting
- Lab 9: Ensemble methods (improve)

---

## ✨ Bottom Line

Simple models often work well. Linear regression and logistic regression are foundational and often outperform complex alternatives. Start simple, add complexity only if needed.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
