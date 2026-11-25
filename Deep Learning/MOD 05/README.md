# Module 5: Analyzing *Arrival* Through the Lens of NLP

**Course:** ITAI 2376, Deep Learning | **Assignment:** A05 | **Team:** Fox

---

## What this module covers

The assignment was to watch *Arrival* (Villeneuve, 2016) and use it as a case study for Natural Language Processing. The film is about a translation problem with the highest possible stakes: twelve alien ships land, and a linguist (Louise Banks) and a physicist (Ian Donnelly) have to work out why. Almost every problem they run into is one that NLP systems face today.

## Files

| File | What it is |
|---|---|
| `A05_Fox_RichFox_ITAI 2376.docx` | Written report (Nov 1, 2026) |
| `A05_Fox_RichFox_ITAI 2376.pptx` | 14-slide presentation with speaker notes |
| `Arrival Viewing Guide for A05.docx` | Note-taking guide for watching the film |
| `Arrival_A05_Guide_Final.docx` | Final version of the viewing guide |

## Six NLP challenges in the film

| Challenge | Scene in *Arrival* | Real NLP parallel |
|---|---|---|
| Ambiguity | "Offer weapon" is read as a threat | Word-sense disambiguation |
| Context and culture | The Sanskrit word for "war" (*gavisti*): "an argument" vs. "a desire for more cows" | Translation that is word-for-word right but misses intent |
| Tokenization | Circular logograms with no start, end, or direction | Splitting text for languages with no spaces (Chinese, Japanese), subword tokenizers |
| Speech vs. text | Heptapod sounds are noisy and unfamiliar, the written symbols hold still | Speech recognition is harder than working with clean text |
| Little training data | No dictionary and no paired examples | Low-resource languages, the "cold start" problem |
| Bias in interpretation | Each country's team reads the message through its own assumptions | Training-data bias in language models |

## The team's methods follow the history of NLP

| In the film | NLP approach | Modern parallel |
|---|---|---|
| Louise builds vocabulary one word at a time on a whiteboard | Rule-based | Hand-built lexicons and grammars |
| Screens match, group, and compare logogram shapes | Statistical | Clustering, frequency analysis |
| Louise reads a whole logogram as one idea | Deep NLP | Transformers and attention |
| Ian finds the message is split across all 12 ships | Shared data | Combining datasets, federated learning |

The logogram point is the most interesting one. A heptapod sentence is not read left to right, which is close to how a transformer's attention lets every token look at every other token at once, unlike an RNN that reads one token at a time.

## Four ideas the film points toward

1. **Show uncertainty.** Give several readings with confidence levels (for example weapon 40%, tool 35%, gift 25%) so people see the doubt before they act.
2. **Ground language in the real world.** Louise ties every word to something both sides can see. Text alone cannot teach meaning (Bender & Koller, 2020).
3. **Use AI to decode languages with no dictionary.** Real examples: Project CETI studying sperm whale codas, and a neural model that helped decipher Ugaritic and Linear B.
4. **Keep humans in the loop and share data.** The model suggests patterns, a linguist checks them, and teams pool what they find.

## Reflection (short version)

- Attention is a step away from strict word-by-word reading, but models still start from a sequence. The film asks whether meaning could be modeled as one connected whole.
- The film leans on the Sapir-Whorf hypothesis. The strong version is not supported by research, but the weaker version still matters: models trained on human language pick up human assumptions, including biased ones.
- Confident-sounding models deserve caution. Speed and accuracy pull against each other, and when people will act on the output, a careful answer beats a quick one.

## Sources

The report and slides use APA references, including Vaswani et al. (2017) on attention, Bender et al. (2021) on large language models, Bender & Koller (2020) on meaning, Sharma et al. (2024) on whale codas, and Luo et al. (2019) on deciphering ancient scripts. The full list is in the `.docx` and the last slide.

---

*[Back to Deep Learning](../README.md)*
