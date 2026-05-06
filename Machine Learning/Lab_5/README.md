# ML Lab 5 — Data Preparation

## Overview

Raw data is rarely ready for modeling. This lab covers the essential preprocessing steps: handling missing values, encoding categorical variables, and scaling features. This is typically 80% of the ML effort.

---

## 📚 What I Learned

### Missing Value Strategies
- **Mean Imputation:** Use average (normally distributed data)
- **Median Imputation:** Use middle value (skewed data, outliers)
- **Mode Imputation:** Use most frequent (categorical data)
- **Drop Rows:** Last resort when data unusable

### Categorical Encoding
- **One-Hot Encoding:** Create binary columns (no ordinal relationship)
- **Label Encoding:** Integer mapping (ordinal relationship)
- **Target Encoding:** Use target variable for encoding

### Feature Scaling
- **Standardization:** (x - mean) / std (zero mean, unit variance)
- **Normalization:** (x - min) / (max - min) (0-1 range)
- **Robust Scaling:** Handles outliers better

### Feature Engineering
- Create new meaningful features from existing ones
- Domain knowledge crucial
- Can improve model performance significantly

---

## 🎯 Learning Objectives

- ✅ Handle missing values appropriately
- ✅ Encode categorical variables
- ✅ Scale numerical features
- ✅ Engineer new features
- ✅ Understand why each step matters

---

## 🛠️ What I Built

**Dataset:** Titanic with missing values

**Processing Pipeline:**
1. Identify missing values
2. Impute age (median strategy)
3. Encode categorical variables (sex, embarked)
4. Scale numerical features (age, fare)
5. Create new features (family size, etc.)

---

## 💡 Real-World Insights

- Imputation strategy depends on data distribution
- Categorical encoding affects model interpretability
- Scaling essential for distance-based models
- Feature engineering domain-specific
- Data preparation is 80% of effort

---

## 🔧 Technologies Used

- pandas (data manipulation)
- scikit-learn.preprocessing (standardization, encoding)
- NumPy (numerical operations)

---

## 📊 Key Code Examples

**Missing Value Imputation:**
```python
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
df['age'] = imputer.fit_transform(df[['age']])
```

**Categorical Encoding:**
```python
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(sparse=False)
encoded = encoder.fit_transform(df[['category']])
```

**Feature Scaling:**
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled = scaler.fit_transform(df[['age', 'fare']])
```

---

## 🚀 Next Steps

- Lab 6: Build models with prepared data
- Lab 7: Evaluate on prepared features
- Implement preprocessing pipelines

---

## ✨ Bottom Line

Data preparation is unglamorous but essential. A simple model on clean, well-prepared data outperforms complex models on messy data.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
