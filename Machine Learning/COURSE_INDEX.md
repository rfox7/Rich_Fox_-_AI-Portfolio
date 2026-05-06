# Machine Learning (ITAI 1371) — Complete Portfolio

> **Student:** Rich Fox  
> **Institution:** HCC (Houston Community College)  
> **Program:** Applied AI & Robotics  
> **Course:** ITAI 1371 — Machine Learning  
> **Duration:** 12 Modules (Labs 1–12) + 2 Projects  
> **Academic Year:** 2025–2026

---

## Portfolio Overview

This portfolio documents a comprehensive journey through machine learning — from foundational concepts through building real-world predictive models, understanding the bias-variance tradeoff, ensemble methods, unsupervised learning, automated machine learning, and critical ethical considerations in AI deployment.

**The narrative arc:**
1. **Labs 1–3:** Foundations — Understanding ML types and workflow
2. **Labs 4–5:** Data Foundation — Exploration and preparation
3. **Labs 6–7:** First Models — Building and evaluating predictions
4. **Lab 8:** Generalization — Understanding overfitting and regularization
5. **Lab 9:** Ensemble Methods — Combining models for better performance
6. **Lab 10:** Unsupervised Learning — Finding patterns without labels
7. **Lab 11:** Optimization — Hyperparameter tuning and AutoML
8. **Lab 12:** Ethics — Fairness, bias, and responsible AI
9. **Projects:** Real-world application and capstone

---

## Lab Breakdown

### **Lab 1 — Hello ML / Introduction**
- **Focus:** Introduction to machine learning concepts and environment setup
- **Key Learning:** What is ML? Why does it matter? Setting up Python with scikit-learn, pandas, numpy
- **Real-world link:** Foundation for everything that follows

---

### **Lab 3 — Machine Learning Workflow & Types of Learning**
- **Focus:** Understanding the complete ML workflow and different learning paradigms
- **Concepts:**
  - **Supervised Learning:** Classification and regression with labeled data
  - **Unsupervised Learning:** Finding patterns without labels
  - **Reinforcement Learning:** Learning through rewards and penalties
- **Key Learning:** The 6-step ML workflow (data → features → model → evaluation → insights → iterate)
- **Technologies:** scikit-learn, pandas for data manipulation
- **Real-world link:** Customer churn prediction, disease diagnosis, recommendation systems

---

### **Lab 4 — Exploratory Data Analysis (EDA)**
- **Focus:** Understanding your data before modeling
- **Techniques:**
  - Descriptive statistics (mean, std, min, max, quartiles)
  - Visualizations (histograms, box plots, scatter plots, heatmaps)
  - Missing value analysis
  - Outlier detection
- **Dataset:** Titanic (classic binary classification)
- **Key Learning:** EDA reveals patterns, anomalies, and relationships that inform model choices
- **Real-world link:** Understanding data quality before deployment

---

### **Lab 5 — Data Preparation**
- **Focus:** Transforming raw data into model-ready format
- **Techniques:**
  - **Handling Missing Values:** Mean/median/mode imputation
  - **Encoding Categorical Variables:** One-hot encoding, label encoding
  - **Feature Scaling:** Standardization and normalization
  - **Feature Engineering:** Creating new meaningful features
- **Key Learning:** Data preparation is 80% of the ML workflow; garbage in = garbage out
- **Real-world link:** Most time in production ML is spent on data pipelines

---

### **Lab 6 — Regression & Classification Models**
- **Focus:** Building your first predictive models
- **Techniques:**
  - **Linear Regression:** Predicting continuous values
  - **Logistic Regression:** Binary classification
  - **Decision Trees:** Interpretable models for both tasks
- **Key Learning:** 
  - Regression predicts numbers; classification predicts categories
  - Simple linear models are often competitive with complex ones
  - Model interpretation is valuable
- **Real-world link:** House price prediction, customer churn, disease diagnosis

---

### **Lab 7 — Better Model Evaluation**
- **Focus:** Evaluating models beyond simple accuracy
- **Metrics:**
  - **Confusion Matrix:** TP, TN, FP, FN breakdown
  - **Precision:** Of predicted positives, how many are correct?
  - **Recall:** Of actual positives, how many did we find?
  - **F1-Score:** Balanced metric combining precision and recall
  - **Cross-Validation:** Robust estimate of real-world performance
- **Key Learning:** Accuracy alone is misleading; different domains need different metrics
- **Real-world link:** Medical diagnosis needs high recall; spam detection needs high precision

---

### **Lab 8 — The Bias-Variance Tradeoff**
- **Focus:** Understanding overfitting, underfitting, and generalization
- **Concepts:**
  - **Underfitting:** Model too simple, high bias, ignores patterns
  - **Overfitting:** Model too complex, high variance, memorizes noise
  - **Regularization:** L1 (Lasso) and L2 (Ridge) techniques to prevent overfitting
  - **Train/Test Split:** Assessing generalization on unseen data
- **Key Learning:** Every model faces this fundamental tradeoff; regularization helps balance it
- **Real-world link:** Production models must generalize; overfitting leads to poor real-world performance

---

### **Lab 9 — Ensemble Methods**
- **Focus:** Combining multiple models for better predictions
- **Techniques:**
  - **Random Forests:** Ensemble of decision trees
  - **Gradient Boosting:** Sequential model improvement
  - **Voting Classifiers:** Simple majority voting
  - **Bagging & Boosting:** Fundamental ensemble approaches
- **Key Learning:** Ensemble > individual model; diversity and accuracy matter
- **Real-world link:** Most Kaggle winners use ensembles; production systems stack models

---

### **Lab 10 — Unsupervised Learning**
- **Focus:** Finding patterns without labeled data
- **Techniques:**
  - **K-Means Clustering:** Grouping similar data points
  - **Principal Component Analysis (PCA):** Dimensionality reduction
  - **Silhouette Analysis:** Evaluating cluster quality
- **Key Learning:** 
  - Unsupervised learning uncovers hidden structure
  - Choosing K in K-means is a challenge
  - PCA useful for visualization and reducing features
- **Real-world link:** Customer segmentation, feature reduction, anomaly detection

---

### **Lab 11 — Hyperparameter Tuning & AutoML**
- **Focus:** Optimizing model performance and automating the process
- **Techniques:**
  - **GridSearchCV:** Exhaustive search over parameter grid
  - **RandomSearchCV:** Random sampling of parameter space
  - **AutoML (AutoGluon):** Automated model selection and hyperparameter tuning
- **Key Learning:**
  - Most models have hyperparameters that dramatically affect performance
  - Automated tools can find good settings faster than manual tuning
  - AutoML democratizes ML; non-experts can build competitive models
- **Real-world link:** AutoML tools enable smaller teams to compete with large ML teams

---

### **Lab 12 — Ethics, Fairness & Bias in ML**
- **Focus:** Building responsible, fair ML systems
- **Topics:**
  - **Fairness Metrics:** Demographic parity, equalized odds, calibration
  - **Bias Detection:** Identifying unfair patterns in model predictions
  - **Transparency:** Explaining model decisions to stakeholders
  - **Ethics Frameworks:** Responsible deployment guidelines
- **Key Learning:**
  - ML models inherit biases from training data
  - Fairness requires measurement and active mitigation
  - Ethical AI isn't optional; it's essential
- **Real-world link:** Hiring systems, loan approvals, criminal justice must be fair

---

## Cross-Lab Themes

### **1. The Complete ML Workflow**
Labs 3-7 walk through: problem → data → features → model → evaluation → iteration

### **2. Accuracy ≠ Good Model**
Labs 7-8 emphasize: precision, recall, F1, cross-validation, and generalization matter more

### **3. Overfitting is Universal**
Every model faces bias-variance tradeoff; regularization and validation are non-negotiable

### **4. Ensemble > Individual**
Lab 9 proves: combining models often outperforms any single model

### **5. Unsupervised Learning Unlocks Value**
Lab 10 shows: many datasets have no labels; clustering and dimensionality reduction are powerful

### **6. AutoML Democratizes ML**
Lab 11 demonstrates: tools can automate tedious hyperparameter tuning

### **7. Ethical AI is Mandatory**
Lab 12 emphasizes: fairness, bias detection, and transparency are non-negotiable in deployment

---

## Key Evaluation Metrics

| Metric | Use Case | Formula | Interpretation |
|---|---|---|---|
| **Accuracy** | Overall correctness | (TP+TN)/Total | What % of predictions are correct? |
| **Precision** | Minimize false positives | TP/(TP+FP) | Of predicted positives, how many are right? |
| **Recall** | Minimize false negatives | TP/(TP+FN) | Of actual positives, how many did we find? |
| **F1-Score** | Balanced metric | 2(P×R)/(P+R) | Harmonic mean of precision & recall |
| **AUC-ROC** | Model ranking | Area under curve | How well does model rank positives above negatives? |

---

## Real-World Applications by Lab

### **Supervised Learning (Labs 3, 6)**
- **Regression:** House prices, stock prices, temperature forecasting
- **Classification:** Email spam detection, disease diagnosis, customer churn

### **Data Understanding (Labs 4-5)**
- Data quality assurance before model deployment
- Feature engineering for domain-specific insights
- Handling missing data in production systems

### **Model Evaluation (Lab 7)**
- Medical diagnosis: High recall (don't miss cases)
- Spam detection: High precision (avoid false alarms)
- Fraud detection: Balance both (rare positive class)

### **Generalization (Lab 8)**
- Regularization prevents overfitting in production
- Cross-validation ensures reliable performance estimates
- Real-world performance gap reveals data shift

### **Ensembles (Lab 9)**
- Kaggle competitions: top solutions are always ensembles
- Production systems: stack multiple models for robustness
- Risk reduction: ensemble diversity hedges model failure

### **Unsupervised Learning (Lab 10)**
- Customer segmentation for targeted marketing
- Document clustering for organization
- Feature reduction for computational efficiency

### **AutoML (Lab 11)**
- Rapid prototyping for stakeholder demos
- Baseline models to beat
- Democratizing ML in resource-constrained organizations

### **Ethics (Lab 12)**
- Hiring systems: ensure fairness across demographics
- Loan approvals: identify discriminatory patterns
- Criminal justice: audit for racial bias
- Healthcare: ensure equitable care across populations

---

## Technologies & Libraries

| Tool | Purpose | Key Use |
|---|---|---|
| **scikit-learn** | ML algorithms | Models, metrics, preprocessing |
| **pandas** | Data manipulation | Loading, cleaning, exploring |
| **NumPy** | Numerical computing | Array operations, math |
| **Matplotlib/Seaborn** | Visualization | EDA plots, results |
| **Jupyter Notebook** | Interactive development | Experimentation, reporting |
| **AutoGluon** | Automated ML | Hyperparameter tuning |

---

## The Complete Learning Arc

```
Lab 1: Foundation
   ↓
Lab 3: Understanding Types of Learning
   ↓
Labs 4-5: Data Exploration & Preparation
   ↓
Lab 6: Building First Models (Linear Regression & Logistic Regression)
   ↓
Lab 7: Better Evaluation (Beyond Accuracy)
   ↓
Lab 8: Understanding Generalization (Bias-Variance Tradeoff)
   ↓
Lab 9: Ensemble Methods (Combining Models)
   ↓
Lab 10: Unsupervised Learning (Finding Patterns)
   ↓
Lab 11: Optimization (Hyperparameter Tuning & AutoML)
   ↓
Lab 12: Ethical Deployment (Fairness & Bias)
   ↓
Midterm Project: Real-World Application
   ↓
Final Project: Capstone Synthesis
```

---

## Critical Lessons

1. **Data Quality > Model Complexity:** 80% of time spent on data; simple models often win
2. **Generalization > Accuracy:** Real-world performance is what matters; cross-validate
3. **Fairness is Non-Negotiable:** Ethical deployment requires measurement and active mitigation
4. **Ensemble > Individual:** Combine models for robustness
5. **Overfitting is Always Lurking:** Regularization and validation are mandatory
6. **Interpretability Matters:** Explain decisions to stakeholders and regulators
7. **Baseline First:** Simple models inform complex ones

---

## For Future Study

### **Intermediate Topics**
- Support Vector Machines (SVMs) for non-linear classification
- Neural Networks and Deep Learning
- Time series forecasting (ARIMA, LSTM)
- Natural Language Processing
- Computer Vision applications

### **Advanced Topics**
- Feature selection and engineering at scale
- Handling imbalanced datasets
- Transfer learning
- Interpretability techniques (LIME, SHAP)
- Production ML systems (MLOps)

### **Specialized Domains**
- Recommender systems
- Anomaly detection
- Reinforcement learning
- Graph neural networks
- Causal inference

---

## Course Reflection

This 12-lab + 2-project journey reflects the modern ML landscape: technical tools combined with critical thinking about generalization, fairness, and responsible deployment.

The progression from simple models → ensemble methods → unsupervised learning → AutoML → ethics mirrors industry evolution: ML has moved from research laboratories to production systems that must be fair, interpretable, and robust.

The key insight: **Machine learning is not just about building models; it's about understanding data, building systems that generalize, and deploying them responsibly.**

---

*Portfolio compiled: May 2026  
All 12 labs documented | 2 projects (1 complete, 1 in progress)  
Course: ITAI 1371 — Machine Learning  
Institution: Houston Community College*
