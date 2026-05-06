# Lab 3B — Image Classification with SVM (CIFAR-10)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 03B
> **Type:** Lab / Hands-on Exercise
> **Student:** Rich Fox
> **File:** `L03b_FoxRich_ITAI_1378.ipynb`

---

## Overview

In this lab, we built an image classifier using a **Support Vector Machine (SVM)** trained on a subset of the **CIFAR-10 dataset** — a benchmark collection of 60,000 color images across 10 object categories. To keep computational demands manageable, we selected three classes: **cat, dog, and ship**. The pipeline covered data loading, grayscale conversion, normalization, flattening, SVM training with a linear kernel, and model evaluation using accuracy and a full classification report.

This lab provided a practical introduction to how classical ML handles real-world image data, and laid groundwork for understanding where classical methods hit their limits before transitioning to deep learning (CNNs) in later modules.

---

## What I Learned

- **SVM finds the optimal decision boundary** — called a hyperplane — that maximizes the margin between classes. The support vectors are the data points closest to that boundary, and they are the only ones that actually define it, making SVM memory-efficient even with large feature spaces.
- **Kernel choice matters.** A linear kernel works when data is approximately linearly separable in the feature space. For more complex, non-linear patterns, polynomial or RBF kernels map data into higher dimensions where a linear boundary can be found.
- **Preprocessing is not optional.** Converting images to grayscale reduced each 32×32×3 RGB image to a 32×32 single-channel array, and normalization (dividing by 255) scaled pixel values to [0, 1]. Flattening converted each 2D image into a 1,024-element feature vector suitable for Scikit-learn.
- **Installing all libraries in a single `pip install` command** is more efficient than separate installs — it lets pip resolve dependencies together and reduces overhead.
- **Classical ML struggles with raw pixel features.** While SVM is powerful in high-dimensional spaces, raw flattened pixels carry a lot of noise and lose spatial structure — motivating the move to CNNs in future modules.

---

## Challenges Faced

The most notable challenge was working with CIFAR-10's multi-label format — `y_train` and `y_test` are stored as 2D arrays of shape `(N, 1)`, requiring `.ravel()` or `.flatten()` calls when passing labels to Scikit-learn functions that expect 1D arrays. The class filtering step using `np.isin()` also required careful mask handling to keep the image and label arrays aligned after subsetting.

---

## Pipeline Summary

### Step 1 — Data Loading & Class Selection

Loaded CIFAR-10 via `tensorflow.keras.datasets` and filtered to three chosen classes:

| Class | CIFAR-10 Index |
|---|---|
| Cat | 3 |
| Dog | 5 |
| Ship | 8 |

Training and test arrays were subsetted using `np.isin()` masks applied to the label arrays.

---

### Step 2 — Preprocessing

Each image went through three transformations before being fed to the SVM:

| Step | Operation | Result |
|---|---|---|
| Grayscale conversion | Weighted dot product: `[0.2989, 0.5870, 0.1140]` | 32×32 single-channel image |
| Normalization | Divide by 255.0 | Pixel values scaled to [0, 1] |
| Flattening | `.reshape(N, -1)` | 1,024-element feature vector per image |

Visualizations were generated at each stage — original color, grayscale, and normalized — to confirm transformations were applied correctly.

---

### Step 3 — Model Training

Trained a **linear kernel SVM** (`SVC(kernel='linear')`) on the flattened, normalized training features:

```python
model = SVC(kernel='linear')
model.fit(X_train_flat, y_train_subset.ravel())
```

The linear kernel was chosen because it is the simplest and most interpretable starting point for a high-dimensional pixel feature space.

---

### Step 4 — Evaluation

Predictions were generated on the held-out test set and evaluated with:

- **Overall accuracy** via `accuracy_score()`
- **Per-class breakdown** via `classification_report()` — including precision, recall, and F1-score for cat, dog, and ship

The classification report reveals which classes the SVM distinguishes most and least reliably, offering insight into where the linear boundary struggles (e.g., cat vs. dog, which share more visual texture overlap than either does with ship).

---

## SVM Concepts — Quick Reference

| Concept | Description |
|---|---|
| Hyperplane | The decision boundary separating classes |
| Support Vectors | The data points closest to the hyperplane that define it |
| Margin | The distance from the hyperplane to the nearest support vectors — SVM maximizes this |
| Linear Kernel | Separates data with a straight hyperplane — best when data is approximately linearly separable |
| RBF Kernel | Maps data to a higher-dimensional space using a Gaussian function — handles non-linear boundaries |
| Polynomial Kernel | Uses a polynomial function of features to separate non-linear data |

---

## Reflection

This lab highlighted both the strengths and limitations of classical ML for image classification. SVM performs well when features are meaningful and the classes are reasonably separable — but raw pixel values from natural images like CIFAR-10 carry a lot of overlapping signal, especially between visually similar classes like cats and dogs. The grayscale conversion also discards color information that might help distinguish classes.

The most important insight from this lab is that **feature representation drives model performance** — not just the algorithm. An SVM trained on HOG or LBP features (as in Lab 3A) would likely outperform one trained on raw pixels, because those features capture structure rather than raw intensity. This motivates the shift to CNNs, which learn their own feature representations directly from the data.

---

## Technologies Used

| Library | Purpose |
|---|---|
| Python 3 | Primary language |
| NumPy | Array operations, grayscale conversion, masking |
| Matplotlib | Image visualization at each preprocessing stage |
| TensorFlow / Keras | CIFAR-10 dataset loading |
| Scikit-learn | SVM training, accuracy scoring, classification report |

---

## Dataset

- **Name:** CIFAR-10 (subset: cat, dog, ship)
- **Source:** `tensorflow.keras.datasets.cifar10.load_data()`
- **Full dataset:** 60,000 images, 10 classes, 32×32 color
- **Subset used:** 3 classes — ~15,000 training images, ~3,000 test images

> This dataset is not uploaded to this repository. It loads automatically via TensorFlow/Keras.

---

## Files

| File | Description |
|---|---|
| `L03b_FoxRich_ITAI_1378.ipynb` | Complete notebook with all code and rendered outputs |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab3B"
jupyter notebook L03b_FoxRich_ITAI_1378.ipynb
```

Run all cells from top to bottom. All outputs are pre-rendered in the notebook.

### Dependencies

```bash
pip install numpy matplotlib tensorflow scikit-learn
```

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
