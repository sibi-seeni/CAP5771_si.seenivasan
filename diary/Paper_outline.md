# Event-Driven Sentiment Dynamics in Gaming Communities Using Hybrid AI Labeling

Paper Outline

---

## Abstract

- Problem: Limited event-driven sentiment studies on YouTube gaming communities
- Dataset: 189,726 comments, 941 channels, 2021–2026
- Method: Hybrid RoBERTa + LLM labeling pipeline with confidence-aware workflow
- Contributions: Event detection framework, LLM reliability evaluation, temporal sentiment analysis
- Key findings: Measurable sentiment shifts during events; AI announcements as illustrative case study
- Implication: LLMs viable for scalable sentiment labeling in imbalanced, noisy domains

---

## 1. Introduction

### Background

Growth of YouTube gaming communities as organic discussion platforms distinct from Twitter/Reddit.

### Problem Statement

Sentiment research concentrated on:

- Twitter, Reddit, product reviews
- Static sentiment snapshots

Underexplored:

- YouTube comment dynamics
- Event-linked sentiment shifts
- Gaming as a domain, and datasets generated in this domain capture the lexicon of a younger audience.

### Research Gap

- No temporal, event-driven sentiment framework for YouTube gaming communities
- LLM labeling reliability in noisy, imbalanced, domain-specific text is understudied
- No evaluation of how gaming communities specifically react to AI-related announcements vs. traditional ones

### Research Questions

- **RQ1:** Do major gaming announcements produce measurable sentiment shifts in YouTube comment activity?
- **RQ2:** How reliable is LLM sentiment labeling compared to a RoBERTa benchmark on noisy, imbalanced gaming data?
- **RQ3:** Can a confidence-aware hybrid labeling workflow improve classification quality over single-model approaches?
- **RQ4:** *(Case study framing)* Do AI-related gaming announcements elicit qualitatively different sentiment patterns compared to traditional announcements?

### Contributions

1. A reproducible pipeline for event detection and sentiment analysis in YouTube gaming communities
2. A large-scale dataset: 189,726 comments, 941 channels, 4+ year span
3. Evaluation of LLM labeling reliability using Krippendorff's Alpha and per-class agreement analysis
4. Confidence-aware hybrid labeling workflow
5. Temporal sentiment analysis across event windows
6. Illustrative case comparison: AI vs. non-AI announcement sentiment

---

## 2. Literature Review

### 2.1 Sentiment Analysis in Social Media

- Evolution: lexicon (VADER, TextBlob) → transformer models
- Limitations of lexicon approaches on domain-specific noisy text
- Trend toward contextual, transfer-learning approaches

### 2.2 YouTube Comments as a Sentiment Dataset

**Challenges:**

- Noise: emojis, slang, short text, gaming jargon
- Context loss: reply threads, meme references
- Class imbalance: neutral comments dominate organic data

**Opportunities:**

- Large-scale organic reactions
- Natural event-driven discussion spikes
- Real consumer sentiment without survey bias

### 2.3 Transformer Models for Sentiment Classification

- Why RoBERTa: contextual embeddings, pretraining scale, transfer learning
- `cardiffnlp/twitter-roberta-base-sentiment-latest` as domain-adjacent benchmark
- Limitations: domain shift from Twitter to YouTube gaming text

### 2.4 LLMs for Weak Supervision and Data Labeling

- Emerging use of LLMs as scalable annotators
- Advantages: reasoning outputs, context awareness, scalability
- Risks: hallucination, prompt sensitivity, class bias
- Validation approaches: gold datasets, inter-annotator agreement
- **Position:** Verified LLM as verification and enrichment layer, not replacement

### 2.5 Prompt Engineering for Text Classification

- Instruction clarity and output formatting effects on classification
- Zero-shot vs. structured prompting
- Role prompting and domain-specific instruction design
- Temperature and determinism considerations

### 2.6 Annotation Agreement in Imbalanced Settings

- Limitations of Cohen's Kappa under class imbalance
- Scott's Pi and weighted Kappa as alternatives
- **Krippendorff's Alpha as primary metric** — rationale and advantages
- Per-class agreement as complementary analysis

### 2.7 Event-Driven Sentiment Analysis

*(Central positioning section)*

- Prior work: finance, politics, product launches
- Volume spike detection as event proxy
- Gap: gaming communities as natural experiment platforms
- **Position your work here explicitly**

---

## 3. Methods

### 3.1 Dataset Collection

- **Source:** YouTube Data API v3
- **Pipeline:** Custom collection pipeline *(describe architecture briefly)*
- **Raw dataset:** 258,443 comments, 941 channels, 147,062 unique commenters
- **Date range:** December 2021 – March 2026
- **Cleaning:** Removed duplicates, non-English comments, spam, short comments
- **Final dataset:** 189,726 comments

### 3.2 Engagement Feature Analysis

- Engagement tier distribution *(report your statistics here)*
- Key insight: 71.96% zero-like comments → validates volume spikes over engagement scores as event signal
- Justification for spike-based event detection approach

### 3.3 Event Detection Framework

*(Present as a methodological contribution)*

**Step 1 — Daily Volume Aggregation:**

- Aggregate comment counts per day
- Establish baseline activity distribution

**Step 2 — Spike Detection:**

- Rolling average baseline
- Z-score threshold for anomaly flagging
- Percent deviation as secondary filter

**Step 3 — Event Verification:**

- Manual verification of spike dates
- Video upload correlation
- Keyword matching for event type

**Step 4 — Event Taxonomy:**

| Category | Description |
|---|---|
| Game Announcement | New title or sequel reveals |
| AI Controversy | AI voice/asset usage debates |
| Technical Reveal | Engine, gameplay, feature demos |
| Release News | Launch dates, updates, patches |
| Trailer Drop | Cinematic or gameplay trailers |

*Explain how each event was assigned a category and note inter-rater process if applicable.*

### 3.4 Sentiment Classification Pipeline

#### RoBERTa Baseline

- Model: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Rationale: domain-adjacent, well-validated, outputs probability scores
- Applied to full 189,726 comment dataset
- Output: Positive / Neutral / Negative + confidence score

#### LLM Labeling Pipeline

- Model: Llama via UF NaviGator API
- Rationale: availability, reasoning output, cost efficiency
- Applied to: gold subset + conflict resolution subset

#### Prompt Design

- Instruction structure and domain adaptation
- Output formatting requirements
- Temperature: set to deterministic/low
- Include final prompt template in **Appendix A**

#### Hybrid Labeling Workflow

*(Define the decision logic explicitly — this is a contribution)*

Proposed logic:
1. RoBERTa labels all comments → primary label
2. LLM labels gold subset → agreement evaluation
3. For low-confidence RoBERTa cases (define threshold): LLM label used or flagged
4. Conflict cases → manual inspection sample

*The decision rule for when LLM overrides RoBERTa is a methodological contribution — state it clearly.*

### 3.5 Confidence-Aware Analysis

- RoBERTa probability score distribution
- LLM confidence estimation approach
- Low-confidence case handling: threshold definition, flagging, inspection
- Report: what proportion of dataset falls below confidence threshold

### 3.6 Gold Dataset Construction

- Sampling strategy: stratified by event type and sentiment class
- Size and composition
- Validation approach
- Used for: Krippendorff's Alpha evaluation and per-class agreement

### 3.7 Agreement Evaluation

**Primary metric:** Gwet's AC1

- Rationale: handles class imbalance, ordinal-aware, robust to unequal distributions

**Supporting analysis:**

- Per-class precision/recall between RoBERTa and LLM labels
- Confusion matrix between model outputs
- Disagreement pattern analysis

### 3.8 Temporal Sentiment Analysis

- Daily sentiment aggregation across full dataset
- Event window structure:

| Window | Definition |
|---|---|
| Pre-event | 7 days before spike |
| Event | Spike day ± 1–2 days |
| Post-event | 7 days after spike |

- Sentiment ratio trends across windows
- Polarization index *(optional but strengthens analysis)*

---

## 4. Results

### 4.1 Dataset Statistics

- Full breakdown: raw → cleaned → analyzed
- Sentiment distribution across full dataset *(note imbalance explicitly)*
- Engagement tier distribution with interpretation

### 4.2 Event Detection Results

- Number of detected spikes and verified events
- Breakdown by event taxonomy category
- Spike magnitude comparison across event types
- *Include event list in **Appendix B***

### 4.3 Temporal Sentiment Trends

- Pre/event/post sentiment ratios across all detected events
- Visualization: sentiment time series with event markers
- Key pattern: polarization during events, normalization after

### 4.4 Sentiment Distribution Across Event Types

- Compare event vs. baseline periods
- Per-category sentiment breakdown
- Notable patterns: which event types drive most negative/positive response

### 4.5 AI vs. Non-AI Announcement Comparison

*(Framed explicitly as an illustrative case study)*
- Sample size transparency: ~1,000–2,000 AI-related comments
- Sentiment ratio comparison: AI vs. traditional announcements
- Qualitative comment examples supporting quantitative patterns
- Careful language: *"suggests"*, *"indicates"*, not *"proves"*

### 4.6 RoBERTa vs. LLM Agreement Results

- Gwet's AC1: overall score + interpretation
- Per-class agreement matrix *(including as **Appendix C**)*
- Where models agree most: clear positive/negative sentiment
- Where disagreement occurs: sarcasm, mixed opinions, memes, gaming slang

### 4.7 Confidence Analysis

- Distribution of low-confidence cases
- Proportion affected by hybrid override
- Where models struggle: ambiguous comments, jokes, domain slang

### 4.8 (Maybe) Error Analysis

- Sarcasm failures: *"Yeah this totally won't flop"*
- Mixed sentiment: *"Looks amazing but the AI worries me"*
- Domain slang misclassification examples
- Systematic error patterns

---

## 5. Discussion

### 5.1 Event-Driven Sentiment as a Measurable Signal

- Events reliably produce detectable sentiment shifts
- Volume spikes as valid event proxies in platform data
- Community behavior insights: polarization patterns, recovery dynamics

### 5.2 AI Announcement Reactions — Case Study Insights

*(Your most distinctive section for Entertainment Computing)*
- What the sentiment patterns suggest about community attitudes toward AI in gaming
- Contrast with traditional announcement hype cycles
- Implications for studios and community managers
- Careful framing given sample size

### 5.3 Reliability of LLM Labeling in This Domain

- Where LLM labeling is competitive with RoBERTa
- Where it underperforms and why
- Practical viability for scalable annotation pipelines

### 5.4 Hybrid Labeling as a Workflow Contribution

- Value of combining models: scalability + quality control
- Confidence-aware routing as a reusable design pattern
- Recommendations for researchers adopting similar workflows

### 5.5 Limitations

- Single platform (YouTube only)
- English comments only
- Gaming domain — generalizability caveat
- AI case study sample size — explicitly acknowledged
- Prompt sensitivity in LLM labeling
- No human baseline annotation beyond gold subset

### 5.6 Future Work

- Multilingual expansion
- Human annotation comparison at scale
- Emotion classification beyond polarity
- Cross-platform comparison (YouTube vs. Reddit vs. Twitter)
- Larger AI announcement dataset as dedicated study

---

## 6. Conclusion

- Event-driven sentiment is measurable and structured in YouTube gaming communities
- Hybrid AI labeling is viable and scalable with appropriate confidence routing
- Gaming communities show distinct, detectable reactions to AI-related topics
- Gwet's AC1 + per-class analysis as recommended practice for imbalanced NLP annotation

**Close with:**
Implications for researchers, game studios, and platform community analysts.

---

## Appendices

### Appendix A — Prompt Templates

Full prompts used for LLM labeling. Improves reproducibility.

### Appendix B — Detected Event List

Dates, event types, spike magnitudes. Improves transparency.

### Appendix C — Per-Class Label Agreement Matrix

RoBERTa vs. LLM confusion matrix. Strengthens reviewer confidence.

---

Draft (Scratched work)

## Lit Review

I used the `cardiffnlp/twitter-roberta-base-sentiment-latest`, a RoBERTa-base model fine-tuned on 124M tweets, providing superior nuance over lexicon-based methods like VADER as a baseline.

### Using Gold Dataset on LLM Labels

Why using a Gold Dataset to validate LLMs is a good idea, and the idea behind using Cohen's Kappa to measure that.

### Prompt Engineering for Text Classification

Crafting a good prompt matters, and it should be specific to the model I am using, which is Llama3.3 70b.

### Llama for Labeling

Why among the models that UF NaviGator offers, I went with Llama, and how it holds up for this labeling work, with reasoning output too, that I can manually verify easier.

## Methods

To assess inter-rater reliability between the Llama 3.3 70B silver labels and the human gold standard, we calculated Percent Agreement, Cohen’s Kappa, and Gwet’s AC1. Given the high class imbalance in our category distribution, Gwet’s AC1 was utilized as a paradox-resistant metric to provide a more stable estimate of agreement (AC1 = 0.XX).

--
