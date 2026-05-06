# ML Midterm Project — Heart Disease Prediction

## Overview

This is your first real-world machine learning project. You'll apply the complete ML workflow to predict the presence of heart disease using the UCI Heart Disease dataset. This project synthesizes everything from Labs 3-11.

---

## 🎯 Project Goal

Build a classifier that predicts whether a patient has heart disease based on medical attributes, achieving high accuracy while understanding model limitations and potential biases.

---

## 📊 Dataset

**Source:** UCI Heart Disease Dataset (4 locations combined)

**Size:** 303 patient records

**Target:** Presence of heart disease (binary: 0 = no disease, 1 = disease present)

**Features (13):**
- Age, sex, chest pain type, resting blood pressure
- Serum cholesterol, fasting blood sugar
- Resting ECG, max heart rate achieved
- Exercise induced angina, ST depression
- ST segment slope, number of major vessels
- Thal (thalassemia)

---

## 📚 What I Learned

### Complete ML Workflow

**1. Exploratory Data Analysis**
- Dataset shape and structure
- Missing values: 6 entries with missing values (handled)
- Feature distributions and relationships
- Class balance: Approximately balanced (54% disease, 46% no disease)
- Correlations between features and target

**2. Data Preparation**
- Handled missing values using median imputation
- Scaled numerical features (StandardScaler)
- Encoded categorical variables (sex, chest pain type, etc.)
- Created feature matrix X and target vector y

**3. Model Training**
- Split data: 80% train, 20% test
- Tried multiple algorithms:
  * Logistic Regression
  * Decision Trees
  * Random Forest
  * Gradient Boosting
  * SVM

**4. Model Evaluation**
- Accuracy: ~85-90% depending on model
- Precision, Recall, F1-Score analysis
- Confusion matrix inspection
- Cross-validation for robustness (5-fold)
- ROC-AUC curves for model comparison

**5. Hyperparameter Tuning**
- GridSearchCV for optimal parameters
- Identified best-performing configurations
- Trade-offs between accuracy and complexity

**6. Ensemble & Final Model**
- Combined top models for ensemble
- Voting classifier achieved highest performance
- Final accuracy: ~90% with cross-validation

---

## 🔧 Technologies Used

- **scikit-learn:** Algorithms, preprocessing, evaluation
- **pandas:** Data loading and manipulation
- **NumPy:** Numerical operations
- **Matplotlib/Seaborn:** Visualization
- **Jupyter Notebook:** Interactive development

---

## 📈 Results

### Best Models
1. **Voting Classifier (Ensemble):** 90% accuracy, F1 = 0.88
2. **Gradient Boosting:** 89% accuracy, F1 = 0.87
3. **Random Forest:** 87% accuracy, F1 = 0.85

### Feature Importance
Top predictive features:
- Max heart rate achieved
- ST depression (exercise-induced)
- Chest pain type
- Age
- Number of major vessels

### Cross-Validation Performance
- Mean accuracy: 87.5%
- Standard deviation: ±2.3%
- Indicates stable, reliable model

---

## 💡 Key Insights

1. **Ensemble Wins:** Combining models outperformed any single approach
2. **Feature Engineering:** Domain knowledge (medical) informed understanding
3. **Overfitting Risk:** Simpler models (logistic regression) generalized better
4. **Balanced Dataset:** No severe class imbalance; standard evaluation appropriate
5. **Medical Domain:** Real-world use would require regulatory approval and medical expert review

---

## ⚠️ Important Caveats

**Medical Use Limitations:**
- This model is NOT approved for clinical use
- Would require FDA approval, clinical validation
- Medical professionals must validate before deployment
- Real-world system needs 99%+ reliability (stakes too high for 90%)

**Ethical Considerations:**
- Model trained on specific populations; may not generalize
- Performance should be audited across demographic groups
- Regular monitoring in production essential
- Human oversight required for all decisions

**Data Limitations:**
- Only 303 samples (small for deep learning)
- Historical data may encode historical biases
- Missing values may indicate data quality issues
- Temporal patterns not captured (static snapshot)

---

## 🚀 Next Steps

- **Clinical Validation:** Consult domain experts
- **Fairness Audit:** Check performance across demographic groups
- **Explainability:** Implement LIME/SHAP for interpretability
- **Production Pipeline:** Build data ingestion, model serving, monitoring
- **Regulatory Compliance:** Navigate FDA/medical device requirements

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `MidTerm Project ITAI 1371.ipynb` | Main analysis notebook |
| `MidTerm Project ITAI 1371 Final.docx` | Final report |
| `MidTerm Project - Supplementary Information.docx` | Additional details |
| `README.md` | This document |

---

## 🎓 What This Demonstrates

✅ **Complete ML Workflow:** From data to production-ready model
✅ **Multiple Algorithms:** Understanding when each approach works
✅ **Evaluation:** Beyond accuracy to meaningful metrics
✅ **Ensemble Methods:** Combining models for robustness
✅ **Critical Thinking:** Understanding limitations and ethical implications

---

## 📚 How to Run

```bash
# Open notebook
jupyter notebook "MidTerm Project ITAI 1371.ipynb"

# Run all cells
# Follow analysis step-by-step
# Review results and insights
```

---

## ✨ Bottom Line

This project demonstrates that building ML systems is straightforward technically but complex ethically and practically. Good models require understanding data, domain expertise, and responsible deployment practices.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
