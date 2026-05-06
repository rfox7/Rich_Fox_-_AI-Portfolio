# Lab 4 — Deep Learning Image Classification (Chihuahua vs. Muffin)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 04
> **Type:** Lab / Hands-on Exercise
> **Student:** Rich Fox
> **File:** `L04_FoxRich_ITAI_1378.ipynb`

---

## Overview

In this lab, we built and trained a **Convolutional Neural Network (CNN)** from scratch using **PyTorch** to solve a binary classification problem: distinguishing chihuahuas from muffins — two things that look surprisingly alike. The lab introduced the full deep learning pipeline: network architecture design, data augmentation, dataloader construction, forward/backward pass training loops, and validation performance visualization. This marks the transition from classical ML (Labs 3A/3B) to deep learning.

---

## What I Learned

- **CNNs learn their own features.** Unlike Lab 3 where we manually engineered HOG or LBP features, a CNN automatically learns what to look for through its convolutional layers — edges, textures, and shapes emerge from training rather than being hand-coded.
- **Network architecture is a design decision.** The `MySkynet` model stacks four convolutional blocks (Conv2d → BatchNorm → ReLU → MaxPool), progressively deepening feature maps from 32 → 64 → 128 → 256 channels, then flattens into fully connected layers for classification.
- **Data augmentation reduces overfitting.** Training transforms included random cropping, horizontal flipping, rotation (±20°), and color jitter — artificially expanding the diversity of the 120-image training set so the model generalizes better.
- **The training loop has two phases.** Each epoch runs a `train` phase (forward pass + backward pass + weight update) and a `validation` phase (forward pass only, no gradient updates) to track generalization performance.
- **CrossEntropyLoss + Adam** is a standard and effective combination for classification — Cross-Entropy measures prediction error across classes, and Adam adapts the learning rate per parameter during optimization.
- **GPU acceleration matters.** The model is placed on CUDA if available (`cuda:0`), falling back to CPU — illustrating the practical importance of hardware for deep learning workflows.

---

## Challenges Faced

With only 120 training images and 30 validation images, the dataset is very small for deep learning — making overfitting a real risk. Data augmentation was the primary defense: transforms like `RandomResizedCrop`, `RandomHorizontalFlip`, `RandomRotation`, and `ColorJitter` were applied during training (but not validation) to create effective variation. Getting the `_get_conv_output()` helper function to dynamically compute the flattened size after the conv layers — rather than hardcoding it — was a key architectural detail that makes the model adaptable to different input sizes.

---

## Model Architecture — `MySkynet`

```
Input (3 × 128 × 128)
│
├── Conv Block 1: Conv2d(3→32) → BatchNorm → ReLU → MaxPool2d
├── Conv Block 2: Conv2d(32→64) → BatchNorm → ReLU → MaxPool2d
├── Conv Block 3: Conv2d(64→128) → BatchNorm → ReLU → MaxPool2d
├── Conv Block 4: Conv2d(128→256) → BatchNorm → ReLU → MaxPool2d
│
├── Flatten
├── Linear(conv_output → 256) → ReLU → Dropout(0.5)
└── Linear(256 → 2)   ← 2 output classes: chihuahua / muffin
```

| Layer Type | Purpose |
|---|---|
| `Conv2d` | Learns spatial features (edges, textures, shapes) |
| `BatchNorm2d` | Stabilizes training by normalizing layer outputs |
| `ReLU` | Introduces non-linearity |
| `MaxPool2d` | Downsamples feature maps, reduces spatial dimensions |
| `Dropout(0.5)` | Randomly zeroes 50% of neurons during training to reduce overfitting |
| `Linear` | Fully connected classification head |

---

## Training Configuration

| Parameter | Value |
|---|---|
| Input size | 128 × 128 px |
| Training images | 120 (60 chihuahua, 60 muffin) |
| Validation images | 30 |
| Batch size (train) | 120 (full dataset per batch) |
| Batch size (val) | 30 |
| Epochs | 30 |
| Loss function | `CrossEntropyLoss` |
| Optimizer | `Adam` (lr = 0.0005) |
| Device | CUDA if available, else CPU |

---

## Data Pipeline

Images were loaded using PyTorch's `ImageFolder`, which expects the folder structure:

```
data/
├── train/
│   ├── chihuahua/
│   └── muffin/
└── validation/
    ├── chihuahua/
    └── muffin/
```

**Training transforms** (augmentation applied):
`RandomResizedCrop(128)` → `RandomHorizontalFlip` → `RandomRotation(20°)` → `ColorJitter` → `ToTensor` → `Normalize`

**Validation transforms** (no augmentation):
`Resize(128×128)` → `ToTensor` → `Normalize`

---

## Results

After 30 epochs of training, model predictions were visualized across all 30 validation images, displaying confidence percentages for each class (e.g., "82% Chi, 18% Muff"). This grid visualization made it easy to see where the model was confident vs. uncertain, and to spot any misclassifications at a glance.

---

## Key Takeaways

- Deep learning models **learn features automatically** — no manual feature engineering required
- **Small datasets need augmentation** to prevent memorization
- **Validation accuracy, not training accuracy**, is the true measure of model quality
- The gap between classical ML (SVM on flat pixels) and CNNs becomes clear: CNNs preserve spatial structure, which is critical for recognizing objects in images

---

## Technologies Used

| Library | Purpose |
|---|---|
| Python 3 | Primary language |
| PyTorch (`torch`) | Neural network framework |
| TorchVision | Image transforms, `ImageFolder`, pretrained models |
| Matplotlib | Visualization of images and predictions |
| PIL (Pillow) | Image loading |
| tqdm | Training progress bars |

---

## Dataset

- **Name:** Chihuahua vs. Muffin (workshop dataset)
- **Source:** Cloned from `github.com/patitimoner/workshop-chihuahua-vs-muffin`
- **Size:** 120 training images, 30 validation images
- **Classes:** `chihuahua`, `muffin`

> This dataset is not uploaded to this repository. Clone it using the command in the notebook.

---

## Files

| File | Description |
|---|---|
| `L04_FoxRich_ITAI_1378.ipynb` | Complete notebook with architecture, training loop, and prediction visualizations |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab4"
jupyter notebook L04_FoxRich_ITAI_1378.ipynb
```

Run all cells from top to bottom. The notebook clones the dataset automatically via `git clone`.

### Dependencies

```bash
pip install torch torchvision matplotlib pillow tqdm
```

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
