# 🤖 NewsBot Intelligence System

**ITAI 2373 – Natural Language Processing | Mid-Term Group Project**
**Team:** Sergio Sanchez & Richard Fox
**Houston City College – October 2026**

---

## What It Does

NewsBot reads a news article and, in one step:

1. **Cleans the text:** removes punctuation, links and filler words, and reduces words to their base form
2. **Predicts the category:** Business, Entertainment, Politics, Sport or Tech
3. **Measures the tone:** positive, negative or neutral
4. **Pulls out key facts:** people, organizations, places, dates and money amounts
5. **Gives a short summary of insights**, and flags articles it isn't sure about for a person to review

It also comes with a simple **web app (Gradio)**: paste in any article, click Analyze, and see the category, tone and highlighted entities. No code needed.

The notebook walks through every step (Modules 1–8 of the course) and then combines them into one reusable `NewsBotIntelligenceSystem` class that can process brand-new articles.

---

## Dataset

**BBC News Classification** (Kaggle): https://www.kaggle.com/competitions/learn-ai-bbc/data

- File used: `BBC News Train.csv`
- 1,490 articles → **1,440 after removing 50 duplicates**
- 5 categories: Sport (342), Business (335), Politics (266), Entertainment (263), Tech (234)
- UK news from 2004–2005; the text is all lowercase and has no separate headlines

---

## How to Run

**Option 1: Google Colab**
1. Open `Midterm_NewsBot_Intelligence_System_Sergio_Sanchez_Richard_Fox_ITAI_2373.ipynb` in Colab.
2. Download `BBC News Train.csv` from the Kaggle link above (you need to click **Join Competition** once), then upload it to the Colab files panel.
3. Click **Runtime → Run all**.

**Option 2: Locally (VS Code or Jupyter)**
1. Put `BBC News Train.csv` in the same folder as the notebook.
2. Open the notebook and click **Run All**. The first cell installs any missing packages.

The last code cell starts the **web app**. It appears inside the notebook and also prints a local web address you can open in your browser.

The entity extraction step takes a few minutes because it processes all 1,440 full-length articles.

**Main libraries:** pandas, scikit-learn, NLTK, spaCy (`en_core_web_sm`), matplotlib, seaborn, wordcloud, plotly, gradio

---

## Key Results

| Area | Result |
|---|---|
| **Classification** | Support Vector Machine: **95.1% test accuracy** (Logistic Regression 93.8%, Naive Bayes 93.4%; all three 95.7–96.5% in 5-fold cross-validation) |
| **Easiest / hardest category** | Sport (100% found) / Tech (89% found; some overlap with Business) |
| **Preprocessing** | Articles 45% shorter, vocabulary 42% smaller after cleaning |
| **Sentiment** | Entertainment most positive; Politics most negative (47% of articles negative) |
| **Entities** | 41,532 found; Sport mentions the most people, Business the most money and companies |
| **New articles** | 5 of 5 classified correctly; the 2 on topics missing from the training data (AI chips, US Senate) were correctly flagged as low confidence |

### What we learned
- **A model only knows what it was trained on.** Our model learned British politics ("labour", "tory", "blair"), so it was only 45% sure about a US Senate article, even though it got the answer right.
- **Lowercase text hurts name-finding.** Proper nouns scored near 0%, and "us" was counted as a country 568 times.
- **Cleaning the data matters.** Removing duplicate articles keeps the same story from appearing in both training and testing, which would make accuracy look better than it really is.

---

## Repository Contents

| File | Description |
|---|---|
| `Midterm_NewsBot_Intelligence_System_Sergio_Sanchez_Richard_Fox_ITAI_2373.ipynb` | Complete notebook with all code, charts, outputs and written analysis |
| `README.md` | This file |

The dataset is not included in this repository (Kaggle competition rules). Download it from the link above.

---

## Team Contributions

We both worked on the same notebook, passing versions back and forth and reviewing each other's changes.

### Richard Fox
- **Initial working pipeline:** built the first version of the notebook that ran end to end on the BBC dataset, including the Kaggle data loading code and the core functions for preprocessing, TF-IDF, POS tagging, syntax parsing, sentiment, classification and entity extraction
- **Dataset decision and loading:** moved the project back to the recommended BBC dataset after a trial with 20 Newsgroups (forum posts rather than news), and rewrote the loading cell to work both in Colab and locally
- **Data quality:** found and removed 50 duplicate articles that could have leaked between the training and test sets
- **Bug fixes and testing:**
  - fixed the "top predictive features" output, which was showing the wrong words for each category because of how the SVM stores its weights
  - fixed package install issues so the notebook runs on current NLTK versions
  - replaced pre-written findings text with results calculated from the data
  - updated the test articles to match the BBC categories and added an intentionally ambiguous article (Apple earnings: Tech or Business?)
- **Analysis and documentation:** wrote the Module 1 discussion answer, the analysis section after each module, the project summary, and this README

### Sergio Sanchez
- **Expanded analysis for every module:** completed the extended "student task" sections, including data quality checks, preprocessing metrics, category term charts, POS heatmaps, sentence complexity analysis, and title vs. body sentiment
- **Visualizations:** built the multi-panel charts for text length, TF-IDF terms, POS patterns, sentiment distribution and entity analysis
- **Classification system:** combined TF-IDF with scaled sentiment and length features, benchmarked three models with 5-fold cross-validation, and built the confusion matrix and evaluation report
- **Performance:** sped up entity extraction by switching to spaCy's batch processing
- **Final pipeline:** rebuilt the `NewsBotIntelligenceSystem` class so it calculates real sentiment and length features for new articles (the earlier version used placeholder zeros), and added confidence-based routing to human review
- **Test articles:** wrote the Nvidia, Houston Astros and US Senate test cases
- **Web app:** built the Gradio interface (bonus) with category scores, tone, and entities highlighted in the article text

---

## Limitations and Future Work

**Limitations**
- All-lowercase text weakens part-of-speech tagging and entity recognition
- No real headlines, so the first 8 words of each article are used as a stand-in title
- Older UK-only news makes the model less confident on newer topics and US news
- VADER sentiment tends toward extremes on long articles and can't tell negative *events* from negative *reporting*

**Future improvements**
- Retrain on recent news from several countries, with original capitalization and headlines
- Try a transformer model (such as BERT) for better handling of context and new topics
- Track entities and sentiment over time to spot trends

---

## Tools and Acknowledgments

- Starter notebook template provided by the ITAI 2373 course
- Dataset: BBC News Classification, Kaggle
- AI assistants were used, as the course allows, to help debug code and refine wording. All results come from running the notebook.
