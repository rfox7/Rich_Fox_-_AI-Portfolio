# Midterm: Creating Images with Diffusion Models

**Course:** ITAI 2376, Deep Learning | **Report date:** Nov 7, 2026

---

## Overview

I trained a class-conditioned diffusion model on Fashion-MNIST and generated clothing images from pure noise. The best checkpoint (epoch 25) reached a validation loss of **0.0709**, and the generated images clearly look like clothing. However, only about **3 of the 10** images matched the class I asked for.

## Files

| File | What it is |
|---|---|
| `MD_Notebook_Rich_Fox_ITAI.ipynb` | Executed Colab notebook with code, outputs, figures, and my analysis notes |
| `MD_Report_Rich_Fox_ITAI.pdf` | 8-page midterm report |

**Code source:** the notebook code came from a copy of the course diffusion notebook shared in the class GroupMe chat, which the instructor said we could use for this assignment. I ran it, trained the model, and wrote the analysis from my own results. The course starting version is in [Module 9](../MOD%2009/README.md).

## Setup

| Setting | Value |
|---|---|
| Dataset | Fashion-MNIST, 28 x 28 grayscale, 10 classes |
| Train / validation split | 48,000 / 12,000 images |
| Hardware | Google Colab, T4 GPU |
| Noise steps | 300 (linear schedule, beta 0.0001 to 0.02) |
| Model | U-Net, channels 32 / 64 / 128, with time and class conditioning |
| Training | 30 epochs, batch size 64, Adam, learning rate 0.001 |
| Best checkpoint | Epoch 25, validation loss 0.0709 |

## Results

| Measure | Result |
|---|---|
| Final epoch | 0.0712 training loss, 0.0723 validation loss |
| Best validation loss | 0.0709 at epoch 25 |
| Overfitting | None: training and validation lines stay close the whole run |
| Plateau | Loss only wobbles after epoch 14, so longer training alone would not help much |
| Classes that matched the request | About 3 of 10: sneaker, coat, and T-shirt/top |
| Classes that failed | Trouser, dress, sandal, shirt, and bag came out as other items |
| CLIP scores for "sandal" (5 images) | 0.278 to 0.304, mean 0.294. The top score went to a sneaker |

**What the loss measures:** mean squared error between the noise the model predicted and the noise actually added. A low loss does not guarantee the right class, because a model can predict noise well and still ignore the label.

## What I found

- **Noise:** with 300 steps the final alpha-bar was 0.048, so about 22% of the original image signal is left at the end. With the original 100 steps it would be about 60%, which is why the notebook uses 300.
- **When an image becomes recognizable:** the sandal stayed pure static from t=299 to about t=170, a blob appeared around t=85, and a clear outline formed by t=42. The shape only appears in the last 15 to 30% of the reverse steps.
- **Easier vs. harder classes:** big, solid, distinct outlines came out best. Thin straps, handles, and the gap between trouser legs are the first things noise destroys. Shirt, T-shirt/top, pullover, and coat look alike, so a weak label signal drifts to a neighbor.
- **Main weakness:** class conditioning is weak. The label passes through only 8 numbers and enters the network at only one place (the 7 x 7 bottleneck), so the model can mostly ignore it.
- **CLIP is a weak judge here.** It was trained on color internet photos, not tiny grayscale images, and the scores sit in a narrow band. A classifier trained on Fashion-MNIST would be more reliable.

## Three improvements I would test

1. **Stronger class conditioning:** raise the embedding size from 8 to about 128 and add time and class information at every U-Net level.
2. **Classifier-free guidance:** hide the label 10 to 20% of the time in training, then push harder toward the requested class when sampling. The class mask is already built in.
3. **Cosine noise schedule plus a learning-rate schedule:** loss stopped improving after epoch 14, which points to the training setup rather than the number of epochs.

## Where this is used

Design ideas, synthetic training data, image restoration, and text-to-image tools. DALL-E, Stable Diffusion, and Midjourney use the same basic method, scaled up with text conditioning.

## Limitations

- Only 28 x 28 grayscale images, far from real-world resolution or color.
- Matched the requested class only about 3 out of 10 times.
- Slow sampling: 300 model passes for every image.
- Training needs a GPU, and I ran into free Colab GPU limits.

---

*[Back to Deep Learning](../README.md)*
