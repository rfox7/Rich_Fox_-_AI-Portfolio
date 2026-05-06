# Lab 8 — Visual Language Models (CLIP & BLIP)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 08
> **Type:** Lab / Hands-on Exercise + Deep Analysis
> **Student:** Rich Fox
> **File:** `L08_Fox_Rich_ITAI1378.ipynb`

---

## Overview

In this lab, we explored **Visual Language Models (VLMs)** — AI systems that jointly understand images and text. We implemented two architectural approaches: **CLIP** (contrastive, zero-shot classification) and **BLIP** (generative, with unified image-text understanding). The lab emphasized practical applications (zero-shot classification, image search, captioning, VQA), deployment trade-offs (API vs. self-hosted), and critical ethical considerations (hallucinations, bias, computational cost, human accountability).

---

## What I Learned

- **Shared embedding spaces enable cross-modal reasoning.** CLIP maps both images and text into the same high-dimensional space using contrastive learning — images similar to a text description have embeddings close together, enabling zero-shot classification without task-specific training.

- **VLMs achieve zero-shot learning through semantic understanding.** CLIP was never explicitly trained to distinguish chihuahuas from muffins, yet it can because it learned general image-text relationships from 400M examples. This transfers to novel domains and classes.

- **Generative VLMs (BLIP) vs. classifiers (CLIP) have different strengths.** CLIP is fast, deterministic, and ideal for search/filtering. BLIP generates richer outputs (captions, answers) but requires more compute. Architecture choice depends on downstream task.

- **Confidence and accuracy don't correlate.** VLMs often provide plausible but incorrect "hallucinated" answers with high confidence. A caption with low BLEU score might be semantically correct; high confidence on a hallucination is the opposite of helpful.

- **Precision-recall trade-offs have real consequences.** For self-driving cars, high recall on pedestrian detection is critical (missing someone = catastrophe). For photo tagging, high precision matters (falsely identifying someone in a murder scene = reputational harm). No single metric is universal.

- **Pre-trained models transfer knowledge but encode dataset bias.** Models trained on COCO or ImageNet inherit biases present in internet data — gender stereotypes, racial disparities, cultural misrepresentation. Bias doesn't disappear through scale; it amplifies.

- **Deployment cost scales dramatically with usage.** Switching from API ($0.01/image) to self-hosted ($500/month infrastructure) makes sense only above ~20,000 images/month. For 100M images/month, the math is brutal — necessity drives architecture choice, not preference.

---

## Challenges Faced

The most instructive challenge was **achieving non-zero evaluation metrics**. Initial experiments evaluating COCO-trained CLIP against VOC-dataset ground truth labels returned 0% precision and recall. The issue wasn't the model — it was **class label mismatch**. COCO uses different class names than VOC (e.g., "person" vs. "person"). By pivoting evaluation to measure **IoU-based localization independent of class labels**, we discovered the model actually achieves 55.69% precision and 69.92% recall — revealing that the localization works well even if label predictions don't align with the dataset's schema.

This taught a hard lesson: **sometimes your code is fine, but your evaluation assumptions are wrong**. Debugging isn't just about fixing bugs — it's about questioning what you're measuring.

---

## Architecture Comparison

| Architecture | Approach | Strengths | Best For |
|---|---|---|---|
| **CLIP** | Contrastive | Zero-shot, fast, deterministic | Classification, search, filtering |
| **BLIP** | Unified vision-language | Flexible, high-quality generation | Captioning, VQA, reasoning |
| **LLaVA** | Instruction-tuned | Multimodal conversation | Chat, dialogue, complex questions |
| **Flamingo** | In-context learning | Few-shot adaptation | Limited-data domains |
| **GPT-4V** | State-of-the-art integrated | Complex reasoning, charts, tables | High-stakes analysis, medical |

---

## Key Reflection Insights

### The Alignment Problem (Reflection 1)

Images and text are fundamentally different — pixels vs. words. Yet CLIP creates a shared space where "dog" clusters near dog images. This works because the model learns that these modalities represent the same semantic concept, though detail is lost in embedding compression. Small text, precise spatial info, and rare visual patterns become sacrificed for the compact mathematical representation.

### Zero-Shot Learning (Knowledge Check 2)

"Zero-shot" means the model performs tasks it was never explicitly trained on. CLIP achieves this through learned general knowledge. More specific category descriptions (e.g., "golden retriever" vs. "dog") improve accuracy by constraining the semantic space.

### Metrics & Evaluation (Knowledge Check 5)

Different metrics evaluate different capabilities:
- **Retrieval (Recall@K):** Selecting from a ranked list
- **Generation (BLEU):** Creating new text

BLEU has limitations — a caption with BLEU score 0 might capture the image correctly if phrasing differs from the reference. Automatic metrics are high-level; human evaluation remains essential.

### Precision vs. Recall Trade-offs

| Application | Priority | Why |
|---|---|---|
| Self-driving car (pedestrian detection) | **HIGH RECALL** | Missing = collision = death. Tolerate false alarms. |
| Photo app (person tagging) | **HIGH PRECISION** | Mislabeling = reputational harm. Tolerate non-detections. |
| Medical diagnosis | **BOTH** | Sensitivity (recall) to catch disease; specificity (precision) to avoid false alarms. |

### Deployment Decision: API vs. Self-Hosted

**API services (GPT-4V, Claude):**
- Pro: Instant scaling, always updated, no infrastructure
- Con: $0.01/image adds up; data privacy concerns

**Self-hosted (CLIP, BLIP, LLaVA):**
- Pro: Fixed costs, data privacy, customization
- Con: Development overhead, maintenance burden

**Break-even:** ~20,000 images/month. For 100M images/month, self-hosting is mandatory from a cost perspective.

---

## Real-World Application Design: Museum Interactive App

**Scenario:** Mobile app where visitors point cameras at exhibits and get descriptions, ask questions, hear historical context.

**Architecture Decision:** BLIP (unified vision-language learning via bootstrapping)

**Deployment:** Self-hosted

**Why:** 
- Visitors provide live camera feeds (privacy mandate → self-host)
- High volume (1000s daily queries) → fixed costs better than API
- Needs generation (descriptions + dialogue) → BLIP over CLIP

**Data Needs:** Curated exhibit descriptions, synthetic bootstrapping, bounding boxes, archival photos

**Metrics:** Recall@K for identification; CIDEr/SPICE for description quality

**Risk Mitigation:** 
- Hallucinations → ground outputs in curated knowledge base
- Bias → audit across diverse exhibit types
- Privacy → anonymize visitor data

**Accessibility:** Text-to-speech, high contrast, large fonts, keyboard navigation

---

## Hallucinations and Trust (Reflection 7)

VLMs confidently generate plausible but false information. Examples:
- Model counts "3 people" when there are 2
- Reads tiny text that's actually illegible
- Invents facts about artwork provenance

**Why problematic:**
- High-stakes domains (medical, legal, safety) can't tolerate confident falsehoods
- Users assume confidence = accuracy (false)
- Dangerous without human oversight

**Mitigation:**
- Multimodal safety filters (Llama Guard 4)
- "LLM as a judge" verification
- Human-in-the-loop for mission-critical tasks
- Selective prediction (abstain when uncertain)

---

## Bias and Fairness

VLMs inherit biases from training data:
- Gender: "doctor" → male images; "nurse" → female images
- Race: Facial recognition works better on some demographics
- Culture: Western-centric training data
- Socioeconomic: Certain lifestyles over-represented

**Testing:** Create balanced test sets, measure performance gaps across groups, analyze word-image associations.

**Responsibility:** Audit before deployment, especially for high-stakes applications.

---

## Ethical Leadership & The Golden Rule

> **"VLMs are powerful assistants, NOT autonomous decision-makers."**

### Why This Matters

VLMs hallucinate, exhibit bias, and lack real-time unified reasoning. No single metric captures quality. Autonomous decision-making in high-stakes domains (security, medical, legal) is unethical without human oversight.

### Where NOT to Use VLMs Autonomously

1. **Medical diagnosis** — hallucinations could harm patients
2. **Security/law enforcement** — false IDs can arrest innocents
3. **Legal document analysis** — confident misreading of contracts
4. **Resume screening** — amplifies hiring bias

### Human-in-the-Loop Design

- Model generates candidates; human reviews and decides
- Confidence thresholds trigger escalation
- Audit trails for accountability
- Regular bias audits

### User Training

- Treat outputs as suggestions, not facts
- Verify before acting on information
- Watch for hallucinations and bias
- Follow clear protocols for high-stakes decisions

---

## Computational Cost & Sustainability

**Inference time:** 
- CLIP: ~10-50 ms/image (fast, single forward pass)
- BLIP: ~1-5 seconds/image (slower, token-by-token generation)

**At scale:**
- 100M images/month with GPT-4V = millions in API costs + massive carbon footprint
- Alternative: Tiered architecture (CLIP for routine, BLIP for complex, GPT-4V for rare edge cases)

**Sustainability practices:**
- Model distillation (smaller model learns from larger)
- Carbon-aware computing (batch during low-carbon hours)
- Caching (avoid redundant inference)

---

## Architecture Selection Framework

When choosing a VLM:

| Need | Architecture | Why |
|---|---|---|
| Zero-shot classification | CLIP | Contrastive space; no retraining needed |
| Natural descriptions | BLIP | Bootstrapped generation; high quality |
| Conversation | LLaVA | Instruction-tuned LLM backbone |
| Few-shot learning | Flamingo | In-context adaptation; minimal data |
| Complex reasoning | GPT-4V | SOTA integrated; handles nuance |

---

## Future of VLMs (Reflection 4)

**Biggest remaining challenge:** Reliable, grounded understanding without hallucinations.

**Most exciting applications:** AR guides, accessibility tools for visually impaired, robotics that understand natural language instructions.

**Biggest concerns:** Spreading misinformation at scale through confident hallucinations.

**Research focus:** Reliability and accuracy — trustworthiness is the bottleneck, not capability.

---

## Technologies Used

| Library | Purpose |
|---|---|
| PyTorch | Deep learning framework |
| Transformers | Pre-trained VLM models (CLIP, BLIP) |
| TensorFlow Datasets | COCO dataset loading |
| Matplotlib | Visualization |
| PIL | Image processing |

---

## Datasets

- **COCO (Common Objects in Context):** Image captioning, dense annotations
- **Flickr30k:** Image-caption pairs
- **Visual Genome:** Scene understanding, relationships

> Not uploaded to repository; load via TensorFlow Datasets or Hugging Face Datasets.

---

## Files

| File | Description |
|---|---|
| `L08_Fox_Rich_ITAI1378.ipynb` | Complete notebook with two paths (CLIP or BLIP), experiments, and reflection questions |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab8"
jupyter notebook L08_Fox_Rich_ITAI1378.ipynb
```

Choose **Path A (CLIP)** for limited compute or **Path B (BLIP)** for GPU with 8GB+ VRAM. Run all cells sequentially.

### Dependencies

```bash
pip install torch torchvision transformers pillow matplotlib datasets
```

---

## Key Takeaway

Lab 8 shifts focus from *recognition* (Labs 1–6) to *understanding* — VLMs that jointly reason across vision and language. The technical foundation matters (architectures, embeddings, metrics), but the deeper insight is **maturity**: recognizing that no model is perfect, that metrics can mislead, and that with power comes responsibility. The "Golden Rule" — treating VLMs as assistants, not decision-makers — reflects this maturity. As you progress toward deploying AI in the real world, this ethical stance will define whether your systems help people or harm them.

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
