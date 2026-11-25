# Module 3: The Neural Network Zoo, CNN Cheetah

**Course:** ITAI 2376, Deep Learning | **Assignment:** A03

---

## What this module covers

Each student picked one "animal" from the Neural Network Zoo (an idea based on the chart by Fjodor van Veen at the Asimov Institute) and presented that type of network. I picked the **CNN Cheetah**: the Convolutional Neural Network, built to understand images and video.

## Files

| File | What it is |
|---|---|
| `A03_ Fox_RichFox_ITAI2376.pptx` | Presentation with speaker notes |
| `A03_ Fox_RichFox_ITAI2376.pdf` | PDF copy of the slides |
| `A03_ Fox_RichFox_ITAI2376.mp4` | Recorded presentation (about 80 seconds) |

## Key ideas

**Neural network basics**

- A neuron takes numbers in, multiplies each by a weight, adds a bias, and passes the total through an activation function (ReLU keeps positives and zeroes out negatives).
- Neurons stack into layers: input, hidden, and output. "Deep learning" means many hidden layers.
- Training means nudging the weights, over and over, until the outputs come out right.

**How a CNN works**

1. **Convolution:** a small filter (for example 3 x 3) slides across the image and writes a number into a feature map wherever it finds the pattern it is looking for.
2. **ReLU:** negative numbers become zero so the network can learn curvy, non-linear patterns.
3. **Pooling:** max pooling keeps only the largest number in each small block, dropping noise.
4. **Flatten and decide:** the final feature maps are unrolled into one list and fully connected layers pick the label.

Early layers find edges and lines, middle layers find textures and corners, and later layers find parts (eyes, ears, paws) and then whole objects.

**Why a cheetah**

| The cheetah... | The CNN... |
|---|---|
| Scans the whole savanna with sharp eyes | Slides filters across the whole image |
| Has a repeating spot pattern | Reuses one filter everywhere (shared weights) |
| Spots prey anywhere in its view | Finds a feature wherever it shows up |
| Ignores the tall grass | Pooling drops weak signals |
| Is a specialist built for speed | Is a specialist built for grid data like images |

**The rest of the zoo**

| Animal | Network | Good at |
|---|---|---|
| Cheetah | CNN | Images and video |
| Raccoon | RNN | Sequences, but forgets quickly |
| Lemur | LSTM | Sequences with better memory (speech, forecasts) |
| Octopus | Transformer | Reading every word at once with attention (powers ChatGPT) |
| Chameleon | GAN | Two networks compete: one makes fakes, one spots them |
| Armadillo | Autoencoder | Squeezing data down and rebuilding it (compression, spotting oddities) |

**Strengths and weaknesses**

- Strengths: learns its own features, needs far fewer weights than a plain fully connected network, finds patterns anywhere in the picture, fast once trained.
- Weaknesses: needs a lot of labeled images and a lot of GPU power.

**History:** LeNet-5 (1998, reading handwritten digits on bank checks), AlexNet (2012, won ImageNet and kicked off the deep learning boom), VGGNet (2014), and later ResNet and YOLO.

## Connection to earlier work

My license plate detector in ITAI 1378 (Computer Vision) used YOLOv8n, which is a CNN-based detector. Walking through filters, ReLU, pooling, and the layer-by-layer feature hierarchy showed me what each piece was doing inside what I had treated as a black box. See the [Computer Vision project](../../Computer%20Vision/README.md).

---

*[Back to Deep Learning](../README.md)*
