# Midterm Project — *(Project Title Here)*

> **Course:** Machine Learning  
> **Type:** Midterm Project  
> **Student:** Rich Fox

---

## Problem Statement

*(Describe the real-world problem your project addresses. Be specific and compelling. Example: "This project builds a classification model to predict customer churn for a telecom company. Identifying customers likely to leave allows the business to take proactive retention steps before losing revenue.")*

---

## Approach & Methods

*(Describe your full workflow in detail. Example:)*

### 1. Data Exploration & Analysis
- Loaded and explored the dataset (shape, dtypes, null values, class distribution)
- Visualized feature correlations with a heatmap
- Identified and handled class imbalance using SMOTE

### 2. Data Preprocessing
- Dropped irrelevant columns
- Encoded categorical features with `LabelEncoder` and `OneHotEncoder`
- Scaled numerical features using `StandardScaler`

### 3. Model Selection & Training
- Trained three models: Logistic Regression, Random Forest, and Gradient Boosting
- Used 5-fold cross-validation to compare baseline performance

### 4. Hyperparameter Tuning
- Applied `GridSearchCV` to optimize the best-performing model

### 5. Evaluation
- Assessed final model using: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Generated a confusion matrix and ROC curve

---

## Results

| Model | Accuracy | F1 Score | AUC-ROC |
|---|---|---|---|
| Logistic Regression | *(value)* | *(value)* | *(value)* |
| Random Forest | *(value)* | *(value)* | *(value)* |
| Gradient Boosting | *(value)* | *(value)* | *(value)* |

*(Summarize findings in 3–4 sentences. Which model performed best and why? What do the metrics tell you about real-world performance?)*

---

## Key Findings

- *(Finding #1 — e.g., "Gradient Boosting achieved the highest AUC-ROC, indicating strong ability to distinguish churn from non-churn customers.")*
- *(Finding #2 — e.g., "Contract type and tenure were the most important features in predicting churn.")*
- *(Finding #3 — e.g., "Addressing class imbalance with SMOTE improved recall by 12% on the minority class.")*

---

## Visualizations

> Results plots are saved in the `results/` folder of this directory.

- `confusion_matrix.png` — Model prediction breakdown
- `roc_curve.png` — AUC-ROC comparison across models
- `feature_importance.png` — Top predictive features

---

## Dataset

- **Name:** *(Dataset name)*
- **Source:** *(URL or description)*
- **Size:** *(e.g., 7,043 rows × 21 features)*

> **Note:** This dataset is not uploaded to this repository. See source above to download it.

---

## Files

| File | Description |
|---|---|
| `midterm_notebook.ipynb` | Full project notebook with code, markdown, and rendered outputs |
| `results/` | Saved plots and performance metrics |

---

## Technologies Used

- Python 3
- Pandas, NumPy
- Scikit-learn (modeling, preprocessing, evaluation)
- Imbalanced-learn (SMOTE)
- Matplotlib, Seaborn

---

## How to Run

```bash
cd "Machine Learning/Projects/Midterm Project"
jupyter notebook midterm_notebook.ipynb
```

Run all cells top to bottom. All outputs are pre-rendered.

---

*[← Back to Machine Learning](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
