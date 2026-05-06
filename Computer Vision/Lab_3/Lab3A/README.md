# Lab 3 — Computer Vision with Classical Machine Learning

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 03
> **Type:** Lab / Hands-on Exercise
> **Student:** Rich Fox
> **File:** `L03_FoxRich_ITAI_1378.ipynb`

---

## Overview

In this lab, we built face recognition models using classical machine learning techniques on the **Olivetti Faces dataset** — 400 grayscale images of 40 people (10 images per person). The core focus was not just building models, but understanding *why* a model with 99% training accuracy can completely fail on new data. We explored the full classical ML pipeline: data preparation, feature extraction (HOG and LBP), algorithm training (SVM and Random Forest), overfitting analysis, and principled model selection.

---

## What I Learned

- **Images are data structures, not just pictures.** Each 64×64 face image is a matrix of pixel values, and feature extraction transforms that raw data into something meaningful for a machine learning algorithm.
- **HOG (Histogram of Oriented Gradients)** captures edge directions and shape — it compresses 4,096 raw pixels into a much smaller, more informative feature vector by focusing on where brightness changes sharply.
- **LBP (Local Binary Pattern)** captures local texture patterns and is highly compact — representing each image as a short histogram of texture codes, making it the most dimensionally efficient feature type tested.
- **High training accuracy does not mean a good model.** An overfitted Random Forest hit ~100% training accuracy but collapsed on validation data — the most important lesson of the lab.
- **The gap between training and validation accuracy is the real signal.** A smaller gap means the model is learning generalizable patterns rather than memorizing the training set.
- **Cross-validation gives a realistic performance estimate** by testing the model on multiple held-out subsets before touching the test set.

---

## Challenges Faced

The trickiest section was getting the **SVM training pipeline** to work correctly with both HOG and LBP features. Because LBP features were constructed differently (flattened raw LBP maps rather than histograms in some cells), the feature arrays needed careful handling to ensure they were proper 2D NumPy arrays before being passed to `StandardScaler` and `SVC`. Adding explicit shape and NaN checks to the `train_and_evaluate_svm` function helped catch and fix silent bugs early.

The Random Forest section also required careful attention — the placeholder `None` values for `rf_hog` and `rf_lbp` needed to be replaced with actual function calls, and the variable name collisions between HOG/LBP accuracy variables from earlier cells and the RF training step required renaming to avoid overwriting results.

---

## Lab Structure & Key Results

### Section 1 — Data Preparation

Split the Olivetti dataset into three sets using stratified sampling to ensure each person appears in all splits:

| Split | Images | Share |
|---|---|---|
| Training | 240 | 60% |
| Validation | 80 | 20% |
| Test | 80 | 20% |

**Reflection:** With only 10 images per person, the model risks focusing on incidental details rather than true facial structure. Variations in lighting and head angle add to this challenge — the model may key on accessories like glasses rather than face shape, leading to misidentification on new images.

---

### Section 2 — Feature Extraction

Three feature types were extracted and compared:

| Feature Type | Dimensions | What It Captures |
|---|---|---|
| Raw Pixels | 4,096 | All pixel values — noisy, high-dimensional |
| HOG | ~1,764 | Edge directions and shape structure |
| LBP | 10 | Local texture pattern histogram |

**Reflection:** LBP produces the most compact representation. HOG reduces dimensionality while preserving the structural information most useful for face recognition. Raw pixels carry too much noise. Smaller feature vectors can actually outperform larger ones because they focus on what matters and avoid overfitting to irrelevant pixel-level variation.

---

### Section 3 — Algorithm Training

Both SVM and Random Forest were trained on HOG and LBP features and evaluated on the validation set.

**SVM** was trained with an RBF kernel and `StandardScaler` normalization (required for SVM). **Random Forest** used 100 estimators with no feature scaling (trees are scale-invariant).

**Reflection (Q4):** SVM with HOG features showed the strongest validation performance with a smaller overfitting gap, suggesting it generalizes better. Random Forest tended to fit the training data more tightly. For face recognition with limited data, SVM's ability to find a maximum-margin decision boundary in high-dimensional space gives it an advantage.

---

### Section 4 — The Overfitting Trap

An intentionally overfitted Random Forest (500 estimators, no depth limit, `min_samples_leaf=1`) was trained to demonstrate the "training trap":

| Model | Training Accuracy | Validation Accuracy | Gap |
|---|---|---|---|
| Overfitted RF | ~100% | Much lower | Large |
| Reasonable RF | Lower | Closer to training | Small |

**Reflection (Q5):** The overfitted model memorized specific pixel patterns from each person's 10 training images rather than learning generalizable facial features. This is analogous to a student who memorizes practice exam answers verbatim — they score 100% on those questions but fail when the wording changes. In a real-world deployment (e.g., identifying individuals in a security system), this failure could mean misidentifying innocent people or missing actual targets.

**Reflection (Q6):** The reasonable model is the right choice for production despite lower training accuracy, because its smaller train/validation gap indicates it will perform more reliably on unseen faces. Cross-validation is important because it gives a statistically grounded estimate of real-world performance before the test set is ever touched.

---

### Section 5 — Final Model Selection

Based on validation accuracy and overfitting gap across all models, model selection prioritized the combination with the highest validation accuracy and smallest gap — indicating the best balance between learning and generalization.

**Reflection (Q7):** The best-performing model was selected based on validation accuracy rather than training accuracy. For a non-technical stakeholder, this can be explained as: "We chose the model that performed best on faces it had *never seen before* during training — not the one that merely memorized the faces it trained on." To improve further with more time and resources, the next steps would be PCA dimensionality reduction before SVM, hyperparameter tuning via `GridSearchCV`, and experimenting with combined HOG + LBP feature vectors.

---

## Technologies Used

| Library | Purpose |
|---|---|
| Python 3 | Primary language |
| NumPy | Array operations and data handling |
| Scikit-learn | ML algorithms, data splitting, evaluation |
| Scikit-image | HOG and LBP feature extraction |
| OpenCV (`cv2`) | Image processing operations |
| Matplotlib / Seaborn | Visualizations and confusion matrices |

---

## Dataset

- **Name:** Olivetti Faces Dataset
- **Source:** `sklearn.datasets.fetch_olivetti_faces()`
- **Size:** 400 images, 40 subjects, 10 images per person
- **Resolution:** 64×64 pixels (4,096 features per image)

> This dataset is not uploaded to this repository. It loads automatically via scikit-learn.

---

## Files

| File | Description |
|---|---|
| `L03_FoxRich_ITAI_1378.ipynb` | Complete notebook with all code, outputs, and reflection answers |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab3"
jupyter notebook L03_FoxRich_ITAI_1378.ipynb
```

Run all cells from top to bottom. Outputs and visualizations are pre-rendered in the notebook.

### Dependencies

```bash
pip install numpy matplotlib seaborn scikit-learn scikit-image opencv-python-headless
```

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
