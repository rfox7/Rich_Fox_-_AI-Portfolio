# Lab 2 — Digital Image Processing Fundamentals

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 2 (Lab)
> **Type:** Hands-on Laboratory
> **Student:** Rich Fox
> **Files:** `L02_Fox_Rich_ITAI1378.ipynb` + `J02_Fox_Rich_ITAI1378.pdf` (Reflection)

---

## Overview

Lab 2 was the foundational gateway to computer vision — where Rich learned that **images are just matrices of numbers**. Rather than abstract theory, this lab was hands-on implementation: loading images, separating RGB channels, applying point operations (brightness/contrast), performing convolutions (blur, edge detection, sharpening), analyzing histograms, applying geometric transformations, and combining techniques into artistic effects. The capstone connected everything back to how modern AI tools like Nano Banana work.

---

## What I Learned

- **Images are data.** A photograph is just a 2D or 3D matrix where each number represents pixel intensity (0-255). This fundamental insight changes how you think about digital media.

- **Every visual effect is math.** Brightness adjustments are addition. Contrast changes are multiplication. Blurring is averaging neighboring pixels. Sharpening is subtracting the difference. Complex effects are combinations of these simple operations.

- **Point vs. neighborhood operations.** Point operations process each pixel independently (brightness, contrast). Neighborhood operations consider surrounding context (convolution: blur, edge detection, sharpening). Both are essential.

- **Convolution is the foundation.** Using a kernel (filter matrix) to compute weighted sums across neighborhoods enables nearly all image processing. Understanding convolution unlocks understanding of how CNNs, GANs, and other deep learning models work.

- **Representation matters.** RGB channels carry different information. Grayscale simplifies. Histograms reveal distribution. Color spaces (RGB, HSV, etc.) encode information differently. Choosing the right representation enables different insights.

- **Geometric transformations preserve content.** Scaling, rotation, translation, perspective, and shearing all modify spatial relationships while maintaining the underlying image content — critical for data augmentation and image registration.

- **Complex effects from simple building blocks.** Vintage filters, dramatic effects, soft glow, Instagram-style filters — all combine multiple simple operations in sequence. Understanding the pipeline demystifies how professional tools work.

- **Traditional and AI approaches are connected.** The hand-designed convolution kernels we implemented are exactly what neural networks *learn* during training. Nano Banana doesn't invent new operations; it learns optimal filter combinations automatically.

---

## Challenges Faced

The initial surprise was **conceptual** — realizing images are just matrices. Rich's reflection journal captured this perfectly: "I've always thought of pictures as just… pictures. But each pixel has separate red, green, and blue values, and tweaking those numbers can completely change what we see."

**Technical challenges:**
- Understanding how convolution works spatially (the kernel slides across the image, computing weighted sums at each position)
- Grasping why different kernels produce different effects (blur averages, edge detection finds differences, sharpening subtracts neighbors)
- Appreciating the role of normalization (kernel values must sum correctly to prevent unwanted brightness changes)
- Implementing histogram equalization conceptually (spreading pixel values across the full 0-255 range)

**The biggest insight:** Many lab students find histogram equalization tricky because it's a global operation (not per-pixel or neighborhood-based). Understanding why and when to use it requires stepping back from local thinking.

---

## Lab Architecture: The 5-Part Structure

### **Part 1: Digital Image Fundamentals (10 min)**

**Concept:** Images as matrices

```python
# Load image as BGR (OpenCV default)
img_bgr = cv2.imread('image.jpg')

# Convert to RGB for correct display
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# Examine properties
shape = img_rgb.shape  # (height, width, 3) for color
dtype = img_rgb.dtype  # uint8
values = (0-255)       # Pixel intensity range
```

**RGB Channel Separation:**
```python
red_channel = img_rgb[:, :, 0]      # Index 0 = Red
green_channel = img_rgb[:, :, 1]    # Index 1 = Green
blue_channel = img_rgb[:, :, 2]     # Index 2 = Blue
```

**Grayscale Conversion:**
```python
# OpenCV method (weighted for human vision)
gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# Manual method (0.299*R + 0.587*G + 0.114*B)
gray_manual = (0.299*R + 0.587*G + 0.114*B)
```

**Key insight:** Different channels carry different information. Red/green/blue aren't equally important to human perception (green contributes most).

---

### **Part 2: Basic Image Operations (10 min)**

**Point Operations** — Each pixel processed independently

```python
def adjust_brightness(image, value):
    """new_pixel = old_pixel + brightness_value"""
    result = image.astype(np.int16) + value
    return np.clip(result, 0, 255).astype(np.uint8)

def adjust_contrast(image, factor):
    """new_pixel = old_pixel * contrast_factor"""
    result = image.astype(np.float32) * factor
    return np.clip(result, 0, 255).astype(np.uint8)
```

**Neighborhood Operations** — Convolution with kernels

```python
# Blur kernel (Gaussian-like)
blur_kernel = np.array([[1, 2, 1],
                        [2, 4, 2],
                        [1, 2, 1]]) / 16

# Edge detection (Sobel)
edge_kernel = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

# Sharpening
sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

# Apply kernel via convolution
result = cv2.filter2D(image, -1, kernel)
```

**How it works:** The kernel slides across the image. At each position, it computes a weighted sum of the 3×3 neighborhood, producing a single output pixel.

**Why different kernels do different things:**
- **Blur:** Small positive values average neighbors → smoothing
- **Edge detection:** Mix of positive/negative values highlight transitions → edges
- **Sharpening:** Center amplified, neighbors subtracted → emphasized differences

---

### **Part 3: Advanced Processing (10 min)**

**Histogram Analysis and Enhancement**

```python
# Plot histogram of pixel intensities
hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256])
plt.plot(bins[:-1], hist)

# Histogram equalization (spreads values across full range)
equalized = cv2.equalizeHist(image)

# CLAHE (Contrast Limited Adaptive Histogram Equalization)
# More sophisticated: adjusts locally, prevents over-enhancement
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(image)
```

**Key insight:** Low-contrast images have narrow histograms (pixel values clustered). Equalization spreads them across 0-255, improving visibility.

---

### **Part 4: Geometric Transformations (5 min)**

**Spatial modifications** — Change pixel positions, not values

```python
# Scaling (resize)
scaled = cv2.resize(image, (new_width, new_height))

# Rotation
rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, rotation_matrix, (width, height))

# Translation (shifting)
translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
translated = cv2.warpAffine(image, translation_matrix, (width, height))

# Perspective transformation (3D-like effect)
src = np.float32([[0,0], [w,0], [w,h], [0,h]])
dst = np.float32([[20,30], [w-10,20], [w-30,h-20], [10,h-10]])
perspective_matrix = cv2.getPerspectiveTransform(src, dst)
perspective = cv2.warpPerspective(image, perspective_matrix, (w, h))
```

---

### **Part 5: Creative Combinations (5 min)**

**Complex effects from simple operations**

**Vintage effect:**
1. Boost red channel (warm tone)
2. Reduce blue channel
3. Lower contrast slightly (soften)
4. Apply subtle blur

**Dramatic effect:**
1. Edge detection
2. Increase contrast
3. Overlay edges on original

**Soft glow:**
1. Create heavily blurred version
2. Blend with original using screen blend mode (1 - (1-a)*(1-b))

**Instagram-style:**
1. Boost saturation (HSV color space)
2. Apply vignette (darken edges gradually)

---

## Student Reflection (from Journal)

### Technical Understanding

"One thing that really surprised me during this lab was seeing how images are actually represented as matrices of numbers. I've always thought of pictures as just… pictures. But each pixel has separate red, green, and blue values, and tweaking those numbers can completely change what we see."

This quote captures the fundamental insight — images aren't magical; they're data structures you can manipulate mathematically.

"Sharpening filters highlight edges by looking at differences between neighboring pixels, while blurring smooths things out by averaging values. Honestly, the trickiest part for me was histogram equalization. I understood the idea—it's about spreading out pixel intensity values—but actually doing it manually made me appreciate how much is going on behind the scenes."

### Connections and Applications

"The AI in [Nano Banana] basically does a lot of what we did manually—but faster and smarter. Things like edge detection or contrast adjustments are happening automatically, but it's cool to see the same principles at work."

Perfect insight: Modern AI tools use the same fundamental operations, just learned automatically rather than hand-designed.

"Filters like blurring or edge detection are used in everything from facial recognition to medical imaging. Geometric transformations could be applied in AR or robotics, and CLAHE enhancement is super handy for low-light images. I can imagine combining traditional methods with AI in a project to automatically enhance photos or even create artistic effects based on learned patterns."

Rich recognized that traditional techniques and AI can complement each other.

### Personal Reflection

"What excites me most about image processing is the creative side. Being able to combine filters and transformations to make something visually unique was a highlight for me. This lab changed how I think about digital photos—I now see them as data I can manipulate, not just something to look at."

"I still have questions. How does AI know what adjustments will look natural versus fake? How can I mix traditional and AI methods to get both accuracy and creativity? Those are the kinds of things I want to explore more in future projects."

These questions show Rich's maturity — not just learning the what/how, but asking about the why and future applications.

---

## Key Concepts Mastered

| Concept | What It Does | Formula | Real-World Use |
|---|---|---|---|
| **Brightness** | Shifts pixel intensity | `new = old + value` | Photography adjustment |
| **Contrast** | Stretches/compresses intensity | `new = old × factor` | Improving visibility |
| **Convolution** | Weighted neighborhood sum | Kernel slides, computes sum | Filtering, edge detection |
| **Blur** | Averages neighboring pixels | Uniform or Gaussian weights | Smoothing noise |
| **Edge Detection** | Finds intensity transitions | Sobel/Canny operators | Object boundaries |
| **Sharpening** | Amplifies differences | Center + negative neighbors | Detail enhancement |
| **Histogram Equalization** | Spreads pixel values | Remap via CDF | Improved contrast |
| **Scaling** | Changes size | Interpolation | Resizing images |
| **Rotation** | Turns image | Rotation matrix | Photo adjustments |
| **Perspective** | Simulates 3D view | Perspective transform | Document scanning |

---

## Technologies Used

| Tool | Purpose | Key Use |
|---|---|---|
| **OpenCV** | Industry computer vision library | Image loading, filtering, transforms |
| **NumPy** | Numerical computing | Matrix operations, array manipulation |
| **Pillow (PIL)** | Python image processing | Simpler interface, enhancements |
| **Matplotlib** | Visualization | Displaying images and histograms |

---

## How to Run

```bash
cd "Computer_Vision/Lab_2"
jupyter notebook L02_Fox_Rich_ITAI1378.ipynb
```

**Environment setup:**
```bash
pip install opencv-python pillow matplotlib numpy
```

**Basic workflow:**
1. Run setup cells (imports and environment)
2. Load or download sample images
3. Execute each part sequentially
4. Examine visualizations
5. Experiment by modifying parameters (kernel values, brightness values, etc.)

---

## Real-World Applications

### Photography & Media
- **Instagram filters:** Combine saturation, blur, vignette, color shifts
- **HDR processing:** Enhance low-light or overexposed images
- **Photo enhancement:** Brightness, contrast, sharpening, noise reduction

### Medical Imaging
- **CT/MRI enhancement:** CLAHE improves visibility in scans
- **Diagnosis:** Edge detection highlights tumors or abnormalities
- **Registration:** Geometric transforms align multiple scans

### Autonomous Systems
- **Vehicle detection:** Edge detection finds car boundaries
- **Lane marking:** Perspective transforms correct camera angle
- **Obstacle avoidance:** Geometric understanding of scene

### Security & Surveillance
- **Object tracking:** Requires understanding spatial changes
- **Low-light enhancement:** Critical for night vision
- **Anomaly detection:** Changes in local regions

### Robotics & AR
- **Perspective correction:** Aligns virtual objects with scene
- **Geometric registration:** Matches real world to digital models
- **Texture mapping:** Applies images to 3D surfaces

---

## Key Takeaway

Lab 2's greatest value isn't the specific techniques (though those are important). It's **removing the mystique from digital images**. 

Once you understand that:
- Images are matrices of numbers
- Every effect is mathematical operations
- Complex visuals come from combining simple operations
- This is exactly how AI systems work (just with learned parameters instead of hand-designed kernels)

Then you're no longer intimidated by image processing or AI. You can ask "how" instead of accepting "magic."

Rich's journey from "pictures are just pictures" to "I can manipulate images as data" is exactly the transformation this lab is designed to create. The skills learned here form the foundation for everything that comes next (CNNs, object detection, VLMs, agents).

---

## Connection to Course Arc

**Previous:** None (Lab 1 is implied in COURSE_INDEX)

**This Lab:** Digital Image Processing Fundamentals — understand images as data

**Next:** Lab 3 (Classical ML) uses feature extraction (HOG, LBP) built on this understanding

**Progression:** Pixels → Features → Models → Understanding → Agents

---

## Future Study Directions

1. **Fourier Transform:** Frequency-domain analysis of images
2. **Morphological Operations:** Erosion, dilation, opening, closing
3. **Image Segmentation:** Dividing images into meaningful regions
4. **Feature Extraction:** HOG, SIFT, ORB (foundation for Lab 3)
5. **Advanced Filtering:** Bilateral filters, guided filters
6. **3D Processing:** Depth maps, point clouds
7. **Video Processing:** Frame-by-frame analysis, optical flow
8. **Deep Learning Integration:** Using traditional ops as preprocessing for neural networks

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
