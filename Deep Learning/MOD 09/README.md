# Module 9: Diffusion Models

**Course:** ITAI 2376, Deep Learning | **Lab:** Lab 9

---

## What this module covers

How diffusion models create images: start with pure noise and remove it a little at a time until a picture appears. The lab is a Google Colab notebook that trains a small, class-conditioned diffusion model on Fashion-MNIST (28 x 28 grayscale clothing images).

## Files

| File | What it is |
|---|---|
| `L09_Diffusion_student_notebook_ITAI_2376.ipynb` | Course notebook, 21 cells, no results filled in |

The notebook here is the starting version from the course. The run I trained, with outputs, figures, and analysis, is in the [Midterm project](../Midterm%20Creating%20Images%20with%20Diffusion%20Models/README.md).

## What the notebook does

| Section | What happens |
|---|---|
| 1. Setup | Imports, random seed, GPU check |
| 2. Configuration | 28 x 28 images, 10 classes, batch size 64, 30 epochs, learning rate 0.001, **300 noise steps** (beta 0.0001 to 0.02) |
| 3. Forward and reverse diffusion | `add_noise` jumps to any noise level in one step. `remove_noise` is one reverse step. `sample_image` runs all 300 reverse steps |
| 4. U-Net | A network that shrinks the image (28 -> 14 -> 7), rebuilds it, and uses skip connections. Time step and class label are added at the 7 x 7 bottleneck |
| 5. Data | Fashion-MNIST scaled to [-1, 1], split 80/20 into train and validation |
| 6. Training | The model predicts the noise that was added. Loss is mean squared error. The best validation checkpoint is saved |
| 7. Generation | One image for each of the 10 classes |
| 8. Reverse process | Snapshots of a sandal forming out of static |
| 9. CLIP (optional bonus) | Scores how well generated images match a text description |
| 10. Analysis | Eight questions to answer from the actual outputs |

## Key ideas

- **Forward process:** noise is added in many small steps. Fine detail disappears first, then edges, then overall shape.
- **Reverse process:** a model learns to predict the noise at each step, so it can be subtracted. Small steps are far easier to learn than one jump from static to a finished image.
- **Why 300 steps:** the original example used 100, but its last step still keeps a lot of the picture. With 300 steps, much less of the original signal is left at the end.
- **Why a U-Net:** the model has to predict noise at every pixel, so it needs both the big picture and exact detail. Skip connections carry the fine detail across.

## To run it

Open in Google Colab, choose Runtime, Change runtime type, T4 GPU, then Runtime, Run all.

---

*[Back to Deep Learning](../README.md)*
