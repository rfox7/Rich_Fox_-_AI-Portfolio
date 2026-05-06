# Assignment 1 — *(Assignment Title Here)*

> **Course:** Machine Learning  
> **Type:** Assignment  
> **Student:** Rich Fox

---

## Problem Statement

*(Clearly describe the problem you were asked to solve. Be specific. Example: "The goal of this assignment was to predict housing prices using a regression model trained on the Boston Housing dataset. Given a set of features like square footage, number of rooms, and neighborhood crime rate, the model should predict the sale price of a home.")*

---

## Approach & Methods

*(Explain how you approached solving the problem. What steps did you take? What algorithms or techniques did you use and why? Example:)*

1. **Data Exploration** — Loaded the dataset and examined distributions, missing values, and correlations using Pandas and Seaborn.
2. **Preprocessing** — Normalized numerical features using `StandardScaler` and encoded categorical variables.
3. **Modeling** — Trained a Linear Regression model as a baseline, then compared against a Random Forest Regressor.
4. **Evaluation** — Used Mean Absolute Error (MAE) and R² Score to compare model performance.

---

## Results

*(Share your results clearly. Include metrics. Example:)*

| Model | MAE | R² Score |
|---|---|---|
| Linear Regression | *(value)* | *(value)* |
| Random Forest | *(value)* | *(value)* |

*(Add 2–3 sentences interpreting the results. Example: "The Random Forest model outperformed Linear Regression, achieving a lower MAE and higher R² score. This suggests the relationship between features and price is non-linear.")*

---

## Key Findings

- *(Finding #1 — e.g., "Square footage was the most important predictor of housing price.")*
- *(Finding #2 — e.g., "Regularization significantly reduced overfitting on the training set.")*
- *(Finding #3 — e.g., "Outliers in the crime rate feature had a large impact on model performance.")*

---

## Dataset

- **Name:** *(Dataset name, e.g., Boston Housing Dataset)*
- **Source:** *(Link or description, e.g., available via `sklearn.datasets.load_boston()`)*
- **Size:** *(e.g., 506 samples, 13 features)*

> **Note:** This dataset is not uploaded to this repository. See the source link above to access it.

---

## Files

| File | Description |
|---|---|
| `assignment1_notebook.ipynb` | Jupyter Notebook with full code, outputs, and markdown explanations |

---

## Technologies Used

- Python 3
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn

---

## How to Run

```bash
cd "Machine Learning/Assignments/Assignment1"
jupyter notebook assignment1_notebook.ipynb
```

Run all cells from top to bottom. Outputs and visualizations are pre-rendered in the notebook.

---

*[← Back to Machine Learning](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
