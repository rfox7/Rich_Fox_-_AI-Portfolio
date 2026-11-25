# Module 2: Hugging Face vs. OpenAI GPT API

**Course:** ITAI 2376, Deep Learning | **Assignment:** A02 | **Lab:** Lab 2

---

## What this module covers

Two ways to put a language model to work:

- **Own it:** download an open model from Hugging Face and run it yourself.
- **Rent it:** send text to the OpenAI GPT API and pay per token.

A02 compares the two on usability, performance, support, and scalability, then runs the same three jobs both ways in a demo notebook. Lab 2 is a hands-on look at a pre-trained image model (VGG16).

## Files

| File | What it is |
|---|---|
| `A02a_Fox_RichFox_ITA2376.pptx` | 12-slide presentation with speaker notes |
| `A02b_Fox_RichFox_ITA2376.docx` | One-page written summary (Oct 11, 2026) |
| `A02c_Fox_RichFox_ITA2376_Demo.ipynb` | Demo notebook: same 3 tasks on Hugging Face and OpenAI |
| `ITAI2376_L02.ipynb` | Lab 2 notebook: working with a pre-trained VGG16 model |

## A02: the comparison

| Criterion | Hugging Face | OpenAI API |
|---|---|---|
| Usability | Easy pipelines, but you manage setup | Easiest: an API key and a prompt |
| Performance | A small tuned model can match a big one on a narrow task | Best general reasoning out of the box |
| Support | Huge community, docs, forums | Official docs, enterprise support |
| Scalability | You buy and run the hardware | Scales automatically, with rate limits |
| Privacy | Data can stay on your own machines | Data goes to OpenAI (zero-retention deals exist) |
| Cost | Free code, pay for hardware | Pay per token |

**Note on models:** the assignment said GPT-4, but GPT-4-era models were no longer on OpenAI's price list by October 2026, so the comparison uses the current GPT-6 family (Astra, Sol, Luna).

### Case studies

- **Hugging Face, Capital Fund Management:** a large open model labeled about 900,000 news headlines for roughly $70. A small model fine-tuned on that data scored 93.4% accuracy (F1), slightly above the big model's 92.7%, at up to 80 times lower running cost.
- **OpenAI, Morgan Stanley:** an assistant built on GPT-4 for about 16,000 financial advisors. More than 98% of advisor teams use it. A zero-data-retention agreement was what got it approved.

### Conclusion

Pick Hugging Face when data is sensitive, the task is narrow and repeats at high volume, or you want to own the model. Pick OpenAI when you need results fast, the task needs real reasoning, or traffic is small and unpredictable. Many teams use both: a big hosted model to prototype and label data, then a small open model to run it cheaply.

## A02c: demo notebook

Runs the same three tasks both ways on five customer reviews, one short article, and three news headlines.

| Task | Hugging Face model | OpenAI model |
|---|---|---|
| Sentiment of reviews | `distilbert-base-uncased-finetuned-sst-2-english` | `gpt-6-luna` |
| Summarize an article | `Qwen/Qwen2.5-0.5B-Instruct` | `gpt-6-luna` |
| Find company names | `dslim/bert-base-NER` | `gpt-6-luna` |

**What the run showed:**

| | Hugging Face (local) | OpenAI API |
|---|---|---|
| Total run time | 16.57 s | 15.60 s |
| Cost | $0.00 (my hardware) | about $0.000181 |
| Labels | POSITIVE / NEGATIVE only | any label you ask for (e.g. MIXED) |
| Where data goes | stays on my machine | sent to OpenAI |

- The Hugging Face sentiment model only knows positive or negative, so the "app is okay, but..." review was forced into NEGATIVE. GPT answered MIXED.
- The Hugging Face model also marked the "transfer went through in minutes" review as NEGATIVE. GPT got it right.
- Both found Apple, Microsoft, and Western Union in the headlines. Neither tagged "Fast Money Picks" as a company.
- The notebook also includes a fine-tuning sketch (not run) showing how Hugging Face lets you retrain a small model on your own data.

**To run it:** open in Google Colab. Part A needs no account. Part B needs an OpenAI API key; set it as the `OPENAI_API_KEY` environment variable or a Colab secret rather than typing it into a cell.

## Lab 2: pre-trained VGG16

The notebook walks through a deep learning workflow with a ready-made model, no training needed:

1. Load VGG16 with ImageNet weights and print the model summary.
2. Load an image, resize it to 224 x 224, and preprocess it.
3. Get the model's top-3 predictions.
4. Use an upload button to try your own images and see how changes to the input affect the predictions.

## Takeaways

- "Own it" gives you control and privacy. "Rent it" gives you speed and general ability.
- A small model trained on your own data can beat a giant general one on a narrow job.
- Cost works differently: per token for the API, per hour of hardware for your own model.

---

*[Back to Deep Learning](../README.md)*
