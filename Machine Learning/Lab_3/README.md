# ML Lab 3 — Machine Learning Workflow & Types of Learning

## Overview

This lab is the conceptual heart of the course. You'll understand the three types of machine learning (supervised, unsupervised, reinforcement), the complete 6-step ML workflow, and see how different types of data fit into the process.

---

## 📚 What I Learned

### The Three Types of Learning

**1. Supervised Learning**
- Learn from labeled examples (input + correct answer)
- **Classification:** Predict categories (disease/healthy, spam/not spam)
- **Regression:** Predict continuous values (house prices, temperature)
- Requires labeled training data

**2. Unsupervised Learning**
- Find hidden patterns without labels
- **Clustering:** Group similar data points (customer segmentation)
- **Dimensionality Reduction:** Simplify high-dimensional data

**3. Reinforcement Learning** (Preview)
- Learn through rewards and penalties
- Agent takes actions in environment

### The Complete ML Workflow

1. Define problem & get data
2. Explore & understand (EDA)
3. Prepare data (clean, encode, scale)
4. Train model
5. Evaluate model
6. Iterate & improve

---

## 🎯 Learning Objectives

- ✅ Distinguish between supervised, unsupervised, reinforcement learning
- ✅ Understand complete ML workflow
- ✅ Build and evaluate classification model
- ✅ Work with different data types

---

## 🛠️ What I Built

**Dataset:** Wine classification (3 cultivars, 13 chemical features)

**Complete Workflow:**
1. Load data
2. Explore (describe, visualize)
3. Split train/test
4. Train logistic regression
5. Evaluate with accuracy and confusion matrix

---

## 💡 Real-World Applications

- Medical diagnosis (supervised classification)
- Customer segmentation (unsupervised clustering)
- Stock price prediction (supervised regression)
- Recommendation systems (hybrid)
- Game AI (reinforcement learning)

---

## 🔧 Technologies Used

- scikit-learn, pandas, NumPy
- Matplotlib, Seaborn
- Jupyter Notebook

---

## 📊 Key Code Examples

**Training a Model:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
```

---

## 🚀 Next Steps

- Lab 4: Deeper EDA
- Lab 5: Data preparation
- Lab 6: Different model types
- Lab 7: Better evaluation

---

## ✨ Bottom Line

The 6-step workflow applies to every ML problem. Understanding which learning type to use is as important as knowing how to build models.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
