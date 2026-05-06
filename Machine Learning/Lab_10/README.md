# ML Lab 10 — Unsupervised Learning

## Overview

Many datasets have no labels. Unsupervised learning finds hidden structure: grouping similar items (clustering) or simplifying high-dimensional data (dimensionality reduction). This lab covers K-means and PCA.

---

## 📚 What I Learned

### K-Means Clustering
- Find K groups in unlabeled data
- Centroid-based approach
- Iterative algorithm: assign points → update centroids
- Convergence when centroids stabilize
- **Key challenge:** Choosing K

### Choosing K
- **Elbow Method:** Plot inertia vs K, look for elbow
- **Silhouette Score:** Measures cluster quality (0 to 1)
- **Domain Knowledge:** Often tells you expected clusters

### Principal Component Analysis (PCA)
- Dimensionality reduction technique
- Find principal components (directions of variance)
- Reduce from high-dimensional to low-dimensional
- Useful for visualization, feature reduction, denoising
- Trade-off: Lost information vs computational efficiency

### Applications
- **Clustering:** Customer segmentation, document grouping, image segmentation
- **Dimensionality Reduction:** Feature reduction, visualization, noise removal
- **Anomaly Detection:** Outliers don't fit clusters
- **Data Exploration:** Understand structure without labels

---

## 🎯 Learning Objectives

- ✅ Implement K-means clustering
- ✅ Choose optimal K
- ✅ Evaluate cluster quality
- ✅ Apply PCA for dimensionality reduction
- ✅ Visualize high-dimensional data

---

## 🛠️ What I Built

**Experiments:**
1. Apply K-means with different K values
2. Evaluate with silhouette score
3. Find optimal K using elbow method
4. Apply PCA to high-dimensional data
5. Visualize in 2D and 3D

**Results:**
- Found natural clusters in data
- Silhouette scores guided K selection
- PCA captured variance with fewer dimensions
- Visualization revealed patterns

---

## 💡 Real-World Applications

- **Marketing:** Customer segmentation for targeted campaigns
- **Biology:** Gene clustering, protein analysis
- **Document:** Organize articles, find topics
- **Retail:** Product grouping, recommendation
- **Image:** Compression, segmentation

---

## 🔧 Technologies Used

- sklearn.cluster (KMeans)
- sklearn.decomposition (PCA)
- pandas, matplotlib, seaborn

---

## 📊 Key Code Examples

**K-Means:**
```python
from sklearn.cluster import KMeans
model = KMeans(n_clusters=3, random_state=42)
clusters = model.fit_predict(X)
```

**Silhouette Score:**
```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, clusters)
print(f"Silhouette Score: {score:.3f}")
```

**PCA:**
```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
print(f"Explained Variance: {pca.explained_variance_ratio_}")
```

---

## 🚀 Next Steps

- Lab 11: Optimize hyperparameters of unsupervised models
- Explore hierarchical clustering, DBSCAN
- Use clustering for feature engineering

---

## ✨ Bottom Line

Unlabeled data is everywhere. Unsupervised learning uncovers structure without ground truth. Clustering finds natural groups; dimensionality reduction simplifies complexity.

**Status:** ✅ Complete

*[← Back to Machine Learning](../../ML_README.md)*
