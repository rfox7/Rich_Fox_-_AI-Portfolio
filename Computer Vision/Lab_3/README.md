# Lab 3 — Computer Vision with Classical Machine Learning

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 03
> **Student:** Rich Fox

---

## Overview

This lab is split into two parts, both focused on applying classical machine learning techniques to computer vision tasks. Together they cover the full classical CV pipeline — from feature engineering and overfitting analysis to real-world image classification with SVM.

---

## Parts

### [Part A — Face Recognition with HOG, LBP & Overfitting](./Lab3A/README.md)

Built face recognition models on the **Olivetti Faces dataset** using HOG and LBP feature extraction, SVM, and Random Forest. The core lesson: why a model with 99% training accuracy often fails in production, and how to build models that actually generalize.

**Key topics:** HOG, LBP, SVM, Random Forest, overfitting, cross-validation

---

### [Part B — Image Classification with SVM & CIFAR-10](./Lab3B/README.md)

Built an image classifier on a 3-class subset of the **CIFAR-10 dataset** (cat, dog, ship) using a linear kernel SVM trained on flattened grayscale pixels. Introduced preprocessing pipelines and classical ML's limitations on natural images.

**Key topics:** SVM, linear kernel, grayscale conversion, normalization, classification report

---

## Technologies Used

- Python 3, NumPy, Matplotlib
- Scikit-learn, Scikit-image
- OpenCV, TensorFlow/Keras

---

*[← Back to Computer Vision](../README.md) | [← Back to Portfolio Home](../../README.md)*
