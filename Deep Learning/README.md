# Rich Fox: Deep Learning Portfolio

**Course:** ITAI 2376, Deep Learning
**Institution:** Houston City College
**Program:** Applied AI & Robotics
**Term:** Fall 2026
**Status:** Complete

---

This course took me from how a single neuron works to building an AI agent that learns on its own. Along the way I compared open and hosted language models, presented on convolutional neural networks, explained backpropagation, used the film *Arrival* to study NLP, and trained a diffusion model that generates images. The final project is **PipelinePilot**, a self-correcting data pipeline agent backed by an Azure SQL database.

## Contents

| Work | Topic | What I did |
|---|---|---|
| [Module 2](./MOD%2002/README.md) | Hugging Face vs. OpenAI GPT API | A02 slides and written summary, a demo notebook running the same three tasks both ways, and a Lab 2 notebook on a pre-trained VGG16 model |
| [Module 3](./MOD%2003/README.md) | Neural Network Zoo: the CNN Cheetah | A03 slides, PDF, and a recorded presentation |
| [Module 4](./MOD%2004/README.md) | Backpropagation | A04 kid-friendly slide deck ("How Robo Learns From Mistakes") |
| [Module 5](./MOD%2005/README.md) | NLP through the film *Arrival* | A05 report and slides |
| [Module 9](./MOD%2009/README.md) | Diffusion models | Lab 9 course notebook |
| [Midterm](./Midterm%20Creating%20Images%20with%20Diffusion%20Models/README.md) | Creating images with diffusion models | Trained Fashion-MNIST diffusion model, executed notebook, and 8-page report |
| [AI Agent Creation (Final Project)](./AI%20Agent%20Creation/README.md) | PipelinePilot, a self-correcting data pipeline agent | Working agent with memory, reasoning, tools, reinforcement learning, and safety, plus a full report |

This folder holds the work saved for Modules 2, 3, 4, 5, and 9, the midterm, and the final project. Each folder has a README with a summary, and the original files (`.pptx`, `.docx`, `.pdf`, `.ipynb`) sit next to it.

## Highlights

| Project | Result |
|---|---|
| **PipelinePilot** (final) | After 100 practice runs the agent loaded **89.6%** of incoming rows, up from **26%** at the start, without being told which fixes were good. It recovered from **94%** of simulated database outages once it had some experience. All **40** automated tests pass |
| **Diffusion model** (midterm) | Best validation loss **0.0709** at epoch 25 with no overfitting, but only about **3 of 10** generated images matched the requested class. I traced the cause to weak class conditioning and listed three fixes to test |
| **Hugging Face vs. OpenAI** (A02) | Same three tasks on both: 16.57 s and $0.00 locally vs. 15.60 s and about $0.0002 through the API. The API handled "MIXED" sentiment and the local model could not |

## Final project: PipelinePilot

You give the agent a plain-English request like *"Load this week's sales files, check them, and tell me what happened."* It then:

1. **Screens** the request and refuses anything harmful or out of scope.
2. **Plans** the job: find the files, read them, check them, fix problems, load, report.
3. **Finds problems** in the data: bad dates, text in number columns, missing keys, duplicates, renamed columns.
4. **Picks a fix** for each problem and learns which fixes work from rewards (an epsilon-greedy bandit).
5. **Recovers** when the database is unavailable and learns the best way to retry.
6. **Loads** clean rows into an Azure SQL warehouse and keeps bad rows in a reject table with the reason.
7. **Reports** what happened, what it chose and why, and a short lesson-learned note.

**Safety has two layers.** Python checks screen requests, allow-list SQL statements, and limit file access. Separately, the agent logs in as a database user that cannot drop, alter, or delete outside its staging area, so Azure SQL would refuse a bad statement even if one got past the Python checks.

See the [AI Agent Creation README](./AI%20Agent%20Creation/README.md) for setup and usage, and the `docs/` folder there for architecture, learning, safety, data, and results.

## What I learned

- **Neural network basics:** neurons, layers, activation functions, and how training adjusts the weights.
- **CNNs:** filters, ReLU, pooling, and how layers build from edges to whole objects.
- **Backpropagation:** passing the blame backward through the network, and how it differs from gradient descent.
- **Language models:** the trade-offs between running an open model yourself and renting a hosted one, and how NLP ideas like ambiguity, tokenization, and attention show up in real problems.
- **Diffusion models:** forward noise, reverse denoising, U-Nets, and why conditioning on the class label matters.
- **AI agents:** memory, reasoning, tool use with error handling, reinforcement learning, and safety by design.

## Tools and technologies

| Area | Tools |
|---|---|
| Deep learning | PyTorch, TensorFlow/Keras (VGG16), CLIP |
| Language models | Hugging Face Transformers, OpenAI API, Claude API |
| Agent project | Python, pandas, Azure SQL, SQLite, pytest |
| Environment | Google Colab (T4 GPU), Jupyter, Git/GitHub |

## Folder structure

```
Deep Learning/
├── README.md                                   (this file)
├── MOD 02/                                     Hugging Face vs. OpenAI + Lab 2
├── MOD 03/                                     CNN Cheetah (slides, PDF, video)
├── MOD 04/                                     Backpropagation deck
├── MOD 05/                                     Arrival and NLP (report + slides)
├── MOD 09/                                     Diffusion lab notebook
├── Midterm Creating Images with Diffusion Models/
│                                               notebook + report
└── AI Agent Creation/                          PipelinePilot, the final project (code, tests, docs, report)
```

## AI assistance

The PipelinePilot report notes that Claude (Anthropic) helped write and test code and draft documentation, and that the design choices, testing, Azure setup, and results were reviewed and run by me. The midterm report notes that its notebook code came from a copy of the course diffusion notebook the instructor said we could use.

---

*[Back to Portfolio Home](../README.md)*
