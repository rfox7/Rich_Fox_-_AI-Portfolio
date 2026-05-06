# ML Lab 4 — Exploratory Data Analysis (EDA)

## Overview

EDA is like being a detective investigating your data. Before you build any model, you need to understand what your data contains: patterns, anomalies, relationships, missing values. This lab teaches you the essential EDA techniques.

---

## 📚 What I Learned

### Why EDA Matters
- Reveal patterns that inform model choices
- Detect data quality issues
- Identify outliers and anomalies
- Understand feature relationships
- Uncover data collection problems

### EDA Techniques
1. **Descriptive Statistics:** mean, std, min, max, quartiles
2. **Visualizations:** histograms, box plots, scatter plots, heatmaps
3. **Missing Value Analysis:** identify patterns in missing data
4. **Outlier Detection:** find unusual values
5. **Correlation Analysis:** understand feature relationships

### Key Insights
- Data quality > Model complexity
- Visualizations reveal patterns faster than numbers
- Missing data patterns indicate problems
- Outliers can be errors or important signals

---

## 🎯 Learning Objectives

- ✅ Load and explore datasets
- ✅ Generate descriptive statistics
- ✅ Create informative visualizations
- ✅ Identify missing values and outliers
- ✅ Understand feature relationships

---

## 🛠️ What I Built

**Dataset:** Titanic (892 passengers, 11 features)

**Analysis:**
1. Basic info (shape, dtypes, missing values)
2. Descriptive statistics by class
3. Visualizations (distributions, relationships, missing patterns)
4. Correlation analysis
5. Key insights from visual inspection

---

## 💡 Real-World Applications

- Data quality assurance before deployment
- Feature selection based on variance
- Understanding data collection bias
- Detecting fraudulent patterns
- Identifying market segments

---

## 🔧 Technologies Used

- pandas (data loading, describe, groupby)
- Matplotlib, Seaborn (visualization)
- NumPy (numerical analysis)

---

## 📊 Key Code Examples

**Descriptive Statistics:**
```python
import pandas as pd
df.describe()  # Quick summary
df.groupby('column').describe()  # By group
```

**Visualizations:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.hist(df['column'])  # Distribution
sns.heatmap(df.corr())  # Correlations
plt.scatter(df['x'], df['y'])  # Relationships
```

---

## 🚀 Next Steps

- Lab 5: Data preparation (handle missing values)
- Lab 6: Build models with understanding of data
- Lab 7: Evaluate models

---

## ✨ Bottom Line

EDA is not optional. Understanding your data prevents model failures and informs better feature engineering. Time spent on EDA saves time later.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
