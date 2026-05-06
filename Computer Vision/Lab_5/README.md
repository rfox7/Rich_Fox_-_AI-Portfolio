# Lab 5 — CNN Optimization & Comparative Analysis (Chihuahua vs. Muffin)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 05
> **Type:** Lab / Hands-on Exercise + Reflective Journal
> **Student:** Rich Fox
> **Files:** `Lab05_CNN_Chihuahua_Muffin.ipynb` + `Lab05_RichFox_ITAI_1378.docx`

---

## Overview

In this lab, we built an optimized **Convolutional Neural Network (CNN)** using PyTorch to classify chihuahuas vs. muffins, building directly on Lab 4's foundational model. The lab emphasized comparative analysis — benchmarking CNN performance against the traditional neural network from Lab 4, understanding convolutional feature extraction, and critically reflecting on real-world deployment challenges including data bias and ethical implications.

---

## What I Learned

- **CNNs are dramatically faster than fully-connected networks.** The CNN trained in ~15 seconds, while the traditional neural network from Lab 4 took ~20 minutes — a 80× speedup. This demonstrates why convolutional architectures are standard for image tasks.

- **Convolutional layers preserve spatial structure.** By applying filters across local neighborhoods, convolutions extract edges, textures, and shapes at multiple scales while maintaining spatial relationships — information that's lost when raw pixels are flattened for classical ML or dense networks.

- **Data augmentation fundamentally reduces overfitting.** Random flips, rotations, and color jitter artificially expand training diversity, teaching the model that objects are still recognizable under transformations — essential with only 120 training images.

- **Feature extraction is learned, not engineered.** The CNN's convolutional layers automatically discover meaningful visual features during training, unlike Lab 3 where we manually designed HOG/LBP features.

- **Real-world deployment has non-technical challenges.** Model bias (all muffins were blueberry; all chihuahuas similar color), domain shift (different lighting, angles, image quality), and false positive consequences create ethical and safety concerns that test accuracy alone cannot address.

- **Normalization matters.** Using ImageNet's mean/std `[0.485, 0.456, 0.406]` and `[0.229, 0.224, 0.225]` for normalization leverages implicit domain knowledge and improves convergence.

---

## Challenges Faced

The most insightful challenge was **recognizing dataset bias**. The training data contained only blueberry muffins and similarly-colored chihuahuas. This limitation became apparent when considering real-world robustness — the model's strong validation accuracy (on the same biased test set) offered no guarantee it would handle black chihuahuas or bran muffins. This tension between reported metrics and actual deployability is the core lesson of the reflective journal.

Getting the fully connected layer dimensions correct also required careful calculation: with input 224×224 and three MaxPool2d operations (each /2), the feature map size is `128 × (224//8) × (224//8) = 128 × 28 × 28 = 100,352` — a calculation that must match the `nn.Linear` input size.

---

## Model Architecture — `ChihuahuaMuffinCNN`

```
Input (3 × 224 × 224)
│
├── Conv Block 1: Conv2d(3→32, k=3, p=1) → ReLU → MaxPool2d(2)
├── Conv Block 2: Conv2d(32→64, k=3, p=1) → ReLU → MaxPool2d(2)
├── Conv Block 3: Conv2d(64→128, k=3, p=1) → ReLU → MaxPool2d(2)
│   [Feature maps now 128 × 28 × 28]
│
├── Flatten → 100,352 features
├── Linear(100,352 → 512) → ReLU → Dropout(0.5)
└── Linear(512 → 2)   ← chihuahua / muffin
```

**Key differences from Lab 4:**
- Larger input: 224×224 (vs. 128×128) — better captures fine details
- No BatchNorm (simplified architecture) — direct ReLU activations
- Explicit feature dimension calculation — `128 * (input_height//8) * (input_width//8)`
- Batch size 32 (vs. 120) — better gradient estimates from smaller batches

---

## Training Configuration

| Parameter | Value |
|---|---|
| Input size | 224 × 224 px |
| Training images | 120 (60 chihuahua, 60 muffin) |
| Validation images | 30 |
| Batch size | 32 |
| Epochs | Configurable (see reflection) |
| Loss function | `CrossEntropyLoss` |
| Optimizer | Adam (lr = 0.001) |
| Device | CUDA if available, else CPU |

---

## Data Pipeline & Augmentation

**Training transforms** (augmentation applied):
```
Resize(224×224) → RandomHorizontalFlip → RandomRotation(10°) → 
ToTensor → Normalize(ImageNet mean/std)
```

**Validation transforms** (no augmentation):
```
Resize(224×224) → ToTensor → Normalize(ImageNet mean/std)
```

The use of ImageNet normalization statistics (rather than dataset-specific stats) reflects a common practice when working with pretrained models or datasets thought to be similar to ImageNet.

---

## Reflective Journal — Key Insights

### CNN vs. Traditional Neural Network Performance

**Speed:** CNN ≈ 15 seconds | Traditional NN ≈ 20 minutes (80× faster)

**Accuracy:** CNN achieves higher accuracy through learned spatial feature hierarchies.

**Why?** Convolutional layers exploit the 2D structure of images, dramatically reducing parameters and computation compared to fully connected layers.

---

### Role of Convolutional Layers

Convolutional layers extract important visual features — edges, textures, shapes — by applying learned filters across the image. These operations preserve spatial relationships, allowing the network to understand that a chihuahua's ear position or a muffin's texture matters. This is fundamentally different from flattening pixels, where spatial information is lost.

---

### Model Improvement Strategies

Potential improvements include:
- **Network depth:** Add more convolutional layers to capture complex hierarchical features
- **Data augmentation:** Expand the diversity of the training set (cropping, brightness, contrast)
- **Learning rate tuning:** Experiment with learning rate schedules (decay, warmup)
- **Regularization:** Increase dropout, add L1/L2 weight decay
- **Transfer learning:** Leverage pretrained models (ResNet, VGG) fine-tuned on this dataset
- **Hyperparameter search:** Systematically sweep epochs, batch size, layer dimensions

---

### Real-World Challenges

**Data bias & distribution shift:**
- All training muffins were blueberry; all chihuahuas had similar coloring
- A black chihuahua or bran muffin would likely confuse the model
- Real deployments face variations in lighting, camera angle, image quality, background clutter

**Overfitting & generalization:**
- With only 120 training images, overfitting is a constant threat
- Validation accuracy on the same distribution doesn't guarantee real-world performance

**Class imbalance & under-representation:**
- If training data is skewed (e.g., 80% muffins, 20% chihuahuas), the model learns a biased decision boundary

---

### Data Augmentation's Contribution

Data augmentation artificially increases training diversity. By randomly flipping, rotating, and scaling images, the model learns that an object's identity is invariant to these transformations. This is especially critical with small datasets — it's the difference between memorizing 120 specific images and learning generalizable visual concepts.

---

### Ethical Considerations

**Chihuahua vs. Muffin:** While harmless, it illustrates principles of higher-stakes systems.

**Real-world examples of AI failures:**
- **Chips misidentified as gun:** AI at a picnic table flagged a bag of chips as a firearm, resulting in SWAT team response with weapons drawn — endangering innocent students.
- **Fugitive misidentification:** AI incorrectly identified an innocent person as a fugitive, leading to police action.

**Ethical lessons:**
When developing image classification systems for safety-critical or law-enforcement applications, false positive consequences are severe. A model that's 95% accurate sounds good — until a 5% error rate means innocent people are arrested or endangered. We must:
- Understand the cost of misclassification in each class
- Audit for bias (demographic, geographic, etc.)
- Consider adversarial robustness
- Implement human-in-the-loop review for high-stakes decisions
- Be transparent about model limitations to stakeholders

---

## Technologies Used

| Library | Purpose |
|---|---|
| Python 3 | Primary language |
| PyTorch (`torch`) | Neural network framework |
| TorchVision | Transforms, ImageFolder, model utilities |
| NumPy | Numerical operations |
| Matplotlib | Visualization |
| tqdm | Training progress bars |

---

## Dataset

- **Name:** Chihuahua vs. Muffin (workshop dataset)
- **Source:** `github.com/patitimoner/workshop-chihuahua-vs-muffin`
- **Size:** 120 training, 30 validation
- **Bias note:** All muffins are blueberry; chihuahuas have limited color variation

> This dataset is not uploaded to this repository. Clone it using the command in the notebook.

---

## Files

| File | Description |
|---|---|
| `Lab05_CNN_Chihuahua_Muffin.ipynb` | Complete notebook with model definition, training, and evaluation |
| `Lab05_RichFox_ITAI_1378.docx` | Reflective journal with detailed answers to 6 reflection questions |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab5"
jupyter notebook Lab05_CNN_Chihuahua_Muffin.ipynb
```

Run all cells from top to bottom. The notebook clones the dataset automatically.

### Dependencies

```bash
pip install torch torchvision numpy matplotlib tqdm
```

---

## Key Takeaway

Lab 5 bridges technical proficiency with critical thinking. Yes, we built a faster, more accurate CNN — but the real learning is recognizing that **test accuracy is not deployment readiness**. Understanding data bias, failure modes, and ethical consequences transforms this lab from "build a classifier" to "build a responsible AI system."

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
