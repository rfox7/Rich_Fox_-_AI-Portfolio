# Assignment 2 — *(Assignment Title Here)*

> **Course:** Machine Learning  
> **Type:** Assignment  
> **Student:** Rich Fox

---

## Problem Statement

*(Clearly describe the problem you were asked to solve. Example: "This assignment focused on binary classification — predicting whether a patient is at risk for diabetes based on medical measurements from the Pima Indians Diabetes dataset.")*

---

## Approach & Methods

*(Walk through your process step by step. Example:)*

1. **Data Exploration** — Analyzed feature distributions and identified class imbalance using value counts and histograms.
2. **Preprocessing** — Handled zero-values in features like glucose and BMI (which represent missing data), then scaled features.
3. **Modeling** — Trained a Logistic Regression model and a Support Vector Machine (SVM); compared using cross-validation.
4. **Evaluation** — Measured performance using accuracy, precision, recall, F1-score, and AUC-ROC.

---

## Results

*(Report your metrics clearly. Example:)*

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | *(value)* | *(value)* | *(value)* | *(value)* |
| SVM | *(value)* | *(value)* | *(value)* | *(value)* |

*(Interpret what these results mean in 2–3 sentences.)*

---

## Key Findings

- *(Finding #1)*
- *(Finding #2)*
- *(Finding #3 — e.g., "Recall was prioritized over precision since false negatives carry higher risk in medical contexts.")*

---

## Dataset

- **Name:** *(Dataset name)*
- **Source:** *(Link or description)*
- **Size:** *(e.g., rows × columns)*

> **Note:** This dataset is not uploaded to this repository. See the source link above to access it.

---

## Files

| File | Description |
|---|---|
| `assignment2_notebook.ipynb` | Jupyter Notebook with full code, outputs, and markdown explanations |

---

## Technologies Used

- Python 3
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn

---

## How to Run

```bash
cd "Machine Learning/Assignments/Assignment2"
jupyter notebook assignment2_notebook.ipynb
```

Run all cells from top to bottom. Outputs and visualizations are pre-rendered in the notebook.

---

*[← Back to Machine Learning](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
