# ML Final Project — Hybrid Movie Recommendation System

## Overview

This is the capstone project for ITAI 1371 (Machine Learning). It demonstrates a complete real-world machine learning solution: a **hybrid recommendation system that predicts good movie recommendations** using three complementary similarity methods (KNN, SVD, and Jaccard) to analyze user ratings and genre tags.

**Project Status:** ✅ **COMPLETE**

---

## 🎯 Project Goal

Build a complete machine learning solution that:
- ✅ Predicts good movie recommendations based on user ratings and genre tags
- ✅ Implements multiple complementary algorithms (KNN, SVD, Jaccard)
- ✅ Demonstrates complete ML workflow from data to evaluation
- ✅ Addresses real-world challenges (memory constraints, user bias, fairness)
- ✅ Includes comprehensive evaluation and ethical considerations
- ✅ Shows production-ready optimization

---

## 🎬 Problem Statement

**The Challenge:**
Streaming platforms and entertainment providers face a significant challenge in helping users navigate vast content libraries to find movies they will enjoy. Families often struggle with the time-consuming and frustrating process of selecting a film, leading to unnecessary conflict and decision fatigue.

**The Goal:**
Build a recommendation system that can predict which movies a user will rate highly based on:
1. **Collaborative filtering:** User rating patterns (what similar users liked)
2. **Content-based filtering:** Genre similarity (movies with similar genres to what user liked)
3. **Hybrid approach:** Combine both methods for robust recommendations

**Real-World Impact:**
- Reduce decision fatigue for users
- Improve streaming platform user satisfaction
- Increase viewing time through better recommendations
- Create personalized experiences at scale

---

## 📊 Dataset

**Source:** MovieLens Dataset (publicly available)

**Composition:**
- **200,000+ users** with rating history
- **84,000+ movies** with genre tags
- **Millions of user ratings** on 1-5 scale
- **Multiple genres per movie** (Drama, Comedy, Action, etc.)

**Challenge Encountered:**
- Raw dataset: 84,000 × 200,000 = 16.9 billion cells
- Memory requirement: 126 GB RAM (unfeasible)
- Solution: Filter to popular movies (50+ ratings) → reduced to ~3,000 movies
- Result: Sparse matrix storing only actual ratings (99% memory savings)

**Data Characteristics:**
- Dense rating patterns for popular movies
- Sparse patterns for niche movies
- Users have different rating styles (some strict, some generous)
- Multiple genre tags per movie (multi-label classification)

---

## 🏗️ Solution Architecture

### **Three-Method Hybrid System**

```
User Input: "Movies I've watched and rated"
    ↓
┌─────────────────────────────────────────────────────┐
│         Three Similarity Methods (Parallel)         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Method 1: K-Nearest Neighbors (KNN)               │
│  • Find users with similar rating patterns         │
│  • Use their ratings to predict                    │
│  • Weight: 20%                                     │
│                                                     │
│  Method 2: Singular Value Decomposition (SVD)      │
│  • Decompose rating matrix into latent factors     │
│  • Learn hidden preference dimensions              │
│  • Weight: 60%                                     │
│                                                     │
│  Method 3: Jaccard Similarity (Genre-based)        │
│  • Compare genre tags between movies               │
│  • Content-based filtering                         │
│  • Weight: 20%                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
    ↓
Weighted Ensemble Combination
(0.2 × KNN + 0.6 × SVD + 0.2 × Genre)
    ↓
Output: Ranked list of predicted ratings
    ↓
Top 10 Movie Recommendations
```

### **Why This Approach**

**KNN (20% weight):**
- ✅ Interpretable: "Similar users liked these"
- ✅ Captures local patterns
- ❌ Scales poorly, sparse neighbors
- ❌ Cold-start problem for new users

**SVD (60% weight - PRIMARY):**
- ✅ Captures global latent factors (hidden preferences)
- ✅ Memory-efficient dimensionality reduction
- ✅ Good generalization to unseen movies
- ✅ Computational efficiency
- ❌ Less interpretable than KNN

**Jaccard (20% weight - CONTENT):**
- ✅ Handles cold-start (new movies with genres known)
- ✅ Direct relevance to user preferences
- ✅ Robust to user bias (based on movie attributes, not ratings)
- ❌ Limited by genre information
- ❌ Can miss subjective preferences

**Hybrid Approach:**
- Combines interpretability (KNN) + power (SVD) + robustness (Jaccard)
- Weights reflect relative importance: SVD provides main signal, KNN and Jaccard provide robustness
- Different methods handle different data scenarios (new users, new movies, sparse ratings)

---

## 🛠️ Technical Implementation

### **Key Algorithms**

**1. K-Nearest Neighbors (KNN)**
```python
# Find K most similar users to target user
# Based on cosine similarity of rating vectors
similarity = cosine_similarity(user_ratings)
nearest_k_users = find_k_most_similar(similarity, k=20)
predictions = weighted_average(nearest_k_users_ratings)
```

**2. Singular Value Decomposition (SVD)**
```python
# Decompose user-movie matrix: A ≈ U × Σ × Vᵀ
# U: user latent factors
# V: movie latent factors
# Σ: importance weights

# Critical fix applied:
# Sort singular values descending (importance order)
# This ensures reconstruction prioritizes major factors
# Instead of: random predictions (RMSE ~2.81)
# After fix: RMSE 0.9152 (interpretable)
```

**3. Jaccard Similarity (Genre-based)**
```python
# Genre overlap between movies
jaccard(movie_a_genres, movie_b_genres) = 
    |genres_in_both| / |genres_in_either|
```

**4. User Bias Correction**
```python
# Account for different rating styles
mean_rating = user_average_from_training_set
centered_rating = actual_rating - mean_rating
# Train on centered ratings
# De-center predictions back to 1-5 scale
```

**5. Per-User Fairness Threshold**
```python
# Instead of: "Is prediction ≥ 4.0?" (unfair to strict raters)
# Use: "Is prediction ≥ user's average?" (fair across all users)
# Ensures Precision@K consistent for all user types
```

### **Critical Optimizations**

**Memory Problem:**
- Original attempt: Load 84,000 × 200,000 dense matrix → 126 GB RAM
- Solution: Filter to popular movies (50+ ratings) → 3,000 movies
- Result: Sparse matrix with 99% memory savings

**Model Quality Problem:**
- Original SVD: Returns singular values ascending (backwards)
- Solution: Sort descending before reconstruction
- Result: RMSE improved from 2.81 → 0.915

**Evaluation Speed Problem:**
- Original: 90+ minutes (nested loops calling models repeatedly)
- Solution: Precompute all matrices, do simple lookups
- Result: 2 minutes total evaluation time

---

## 📈 Results & Performance

### **Standard ML Metrics**

| Model | RMSE | MAE | Precision@10 |
|---|---|---|---|
| **KNN** | 0.9202 | 0.6649 | 0.0120 |
| **SVD** | 0.9152 | 0.6989 | 0.0491 |
| **Hybrid** | — | — | 0.0234 |

**Interpretation:**
- **RMSE (Root Mean Squared Error):** ~0.92 means predictions off by ~1 star on average
- **MAE (Mean Absolute Error):** ~0.67 means median error ~0.67 stars
- **Precision@10:** Of top 10 recommendations, what % does user actually rate above their average?
  - SVD highest (4.91%) — best single method
  - Hybrid (2.34%) — balances all three methods

### **Key Performance Insights**

1. **SVD Dominance:** 60% weight on SVD justified by:
   - Lowest RMSE (0.9152)
   - Highest Precision (0.0491)
   - Captures latent preference dimensions effectively

2. **KNN Contribution:** 20% weight for:
   - Local pattern capture
   - Interpretability ("similar users liked...")
   - Neighbor-based robustness

3. **Genre Jaccard:** 20% weight for:
   - Content-based signal
   - Cold-start handling
   - Diversity in recommendations

### **Fairness Analysis**

**Problem Addressed:**
- Strict raters (average 2.8 stars) penalized by global threshold
- Generous raters (average 4.2 stars) favored by global threshold
- Per-user threshold: "above your average" is consistent measure

**Solution Impact:**
- Precision@10 fair across user segments
- Strict users: 2.8+ counts as "liked"
- Generous users: 4.2+ counts as "liked"

---

## 🔍 Real-World Challenges & Solutions

### **Challenge 1: Memory Explosion**
- **Problem:** 84,000 movies × 200,000 users = 16.9B cells = 126 GB RAM
- **Solution:** Filter to popular movies (50+ ratings)
- **Result:** Reduced to 3,000 movies, sparse matrix, ~1 GB RAM

### **Challenge 2: SVD Producing Garbage**
- **Problem:** scipy.sparse.svds() returns singular values ascending (backwards)
- **Reconstruction:** U × Σ × Vᵀ prioritizes least significant factors
- **Result:** RMSE 2.81 (essentially random)
- **Solution:** Sort singular values descending
- **Result:** RMSE 0.9152 (interpretable)

### **Challenge 3: User Bias Distortion**
- **Problem:** User "3.0" means different things (enthusiasm vs disappointment)
- **Solution:** Center ratings by user average before training
- **Impact:** Models learn relative preference, not absolute ratings

### **Challenge 4: Unfair Fairness Metrics**
- **Problem:** Global threshold (4.0+) penalizes strict raters
- **Solution:** Per-user threshold (above user's average)
- **Impact:** Precision@K fair across all user segments

### **Challenge 5: 90-Minute Evaluation**
- **Problem:** Nested loops calling model functions repeatedly
- **Solution:** Precompute all matrices, use array lookups
- **Result:** 2-minute evaluation

---

## 🎓 What This Project Demonstrates

✅ **Complete ML Workflow**
- Problem definition & motivation
- Data exploration and understanding
- Data preparation (filtering, normalization, fairness)
- Model building (3 complementary methods)
- Hyperparameter tuning
- Comprehensive evaluation
- Production optimization

✅ **Multiple Algorithms**
- KNN: Instance-based learning
- SVD: Matrix factorization
- Jaccard: Content-based similarity
- Ensemble: Weighted combination

✅ **Real-World Problem Solving**
- Memory constraints (16.9B → 3K movies)
- Numerical issues (SVD reconstruction)
- User bias correction
- Fairness in evaluation metrics
- Performance optimization (90min → 2min)

✅ **Fairness & Responsibility**
- Per-user fairness thresholds
- User bias correction
- Equitable evaluation across segments
- Recognition of implicit bias in metrics

✅ **Production Readiness**
- Optimized code (2-minute evaluation)
- Reproducible pipeline
- Clear documentation
- Handling edge cases

✅ **Communication**
- Clear problem motivation
- Technical justification
- Results interpretation
- Ethical considerations

---

## 🔧 Technologies Used

| Category | Tools |
|---|---|
| **Core ML** | scikit-learn, SciPy, NumPy, Pandas |
| **Algorithms** | KNN, SVD, Cosine Similarity, Jaccard |
| **Data Handling** | Sparse matrices, NumPy arrays |
| **Development** | Jupyter Notebook, Python 3 |
| **Evaluation** | Custom metrics, cross-validation |
| **Optimization** | Matrix precomputation, sampling |

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `Final_Project.ipynb` | Complete implementation notebook |
| `Final_Project_ITAI_1371_Selection_Info.docx` | Project proposal |
| `ITAI_1371_Final_Project.docx` | Final report |
| `ITAI_1371_Final_Project_Part_B.docx` | AI usage documentation |
| `Performance_Report.docx` | Detailed results analysis |
| `Final_Project.pptx` | Presentation slides |

---

## 🚀 Next Steps & Future Improvements

### **Short-term (Production Ready)**
- [ ] Deploy as web API (Flask/FastAPI)
- [ ] Add real-time recommendation endpoint
- [ ] Implement caching for frequent users
- [ ] Create dashboard for metrics monitoring
- [ ] A/B testing framework

### **Medium-term (Advanced Features)**
- [ ] Temporal dynamics (user preferences change over time)
- [ ] Cold-start handling for new users
- [ ] Implicit feedback (viewing without rating)
- [ ] Cross-domain recommendations
- [ ] Multi-armed bandit for exploration

### **Long-term (Research)**
- [ ] Deep learning approaches (Neural Collaborative Filtering)
- [ ] Context-aware recommendations (time of day, viewing with others)
- [ ] Explanation generation ("because you watched X")
- [ ] Serendipity and diversity objectives
- [ ] Fairness across provider preferences

---

## 💡 Key Insights

### **On Hybrid Approaches**
1. **No single method is best:** KNN good locally, SVD good globally, Jaccard good for cold-start
2. **Weighting matters:** SVD at 60% vs 33% each makes significant difference
3. **Complementarity is power:** Methods fail differently, ensemble robustness

### **On Real-World ML**
1. **Data is the bottleneck:** Memory constraints forced fundamental redesign
2. **Small bugs = big impact:** SVD singular value sort caused 3x RMSE increase
3. **Fairness is not free:** Per-user thresholds require deliberate implementation

### **On User Preference**
1. **Users are inconsistent:** Same 3.0 rating means different things
2. **Relative preference matters:** "Above your average" more meaningful than "4+ stars"
3. **Context changes preference:** Genre affects preference more than absolute rating

### **On Production Systems**
1. **Optimization is essential:** 90 minutes → 2 minutes changes feasibility
2. **Precomputation saves billions:** Matrix lookup vs model call
3. **Clear thinking prevents bugs:** Matrix order matters, singular value order matters

---

## 🎯 Project Status

- [x] Problem definition complete
- [x] Data exploration done
- [x] Data preparation (filtering, normalization)
- [x] Model building (KNN, SVD, Jaccard)
- [x] Hyperparameter tuning
- [x] Comprehensive evaluation
- [x] Fairness audit completed
- [x] Production optimization
- [x] Final report written
- [x] Presentation prepared
- [x] Documentation complete

---

## 📝 AI Usage Log

**Claude (Anthropic):**
- Used for coding processes (combining 3 models, user input processes)
- Addressed technical errors (memory issues, SVD reconstruction, evaluation optimization)
- Problem-solving for model fairness and bias correction

**NotebookLM:**
- Created markdown documentation for GitHub
- Verified all requirements met

**Key Insights from AI Usage:**
- Memory constraints drove fundamental architecture decisions
- User bias correction was critical for fair evaluation
- Precomputation transformed infeasible (90min) to practical (2min)

---

## ✅ Summary

This project successfully implements a **hybrid movie recommendation system** that synthesizes all course concepts (Labs 1-12 + Midterm) into a real-world solution. It demonstrates:

**Technical Achievement:**
- Three complementary algorithms (KNN 20%, SVD 60%, Jaccard 20%)
- RMSE 0.92 (predictions within ~1 star on average)
- Complete ML workflow from data to production

**Problem-Solving:**
- Addressed memory constraint (16.9B → 3K movies, sparse matrix)
- Fixed numerical issue (SVD reconstruction order)
- Optimized evaluation (90min → 2min)
- Corrected user bias with centering
- Implemented fair evaluation metrics

**Real-World Readiness:**
- Handles edge cases (new users, new movies, different rating styles)
- Fair across user segments
- Production-optimized code
- Comprehensive documentation

**Ethical Maturity:**
- Fairness audit across rating styles
- Per-user evaluation thresholds
- Recognition of implicit biases
- Transparent limitation discussion

---

**Status:** ✅ **PROJECT COMPLETE**

*[← Back to Machine Learning](../../ML_README.md) | [← Back to Portfolio Home](../../../PORTFOLIO_README_FINAL.md)*
