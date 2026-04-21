# Arc Raiders YouTube Sentiment Analysis

### Event-Driven Sentiment Analysis using Hybrid AI Labeling

Project for CAP5771 – Introduction to Data Science

---

## Project Overview

This project implements an end-to-end **data engineering, NLP, and hybrid AI labeling pipeline** to analyze community sentiment toward *Arc Raiders* using YouTube comments. The goal is not just sentiment classification, but understanding **how sentiment changes around major game announcements and AI-related controversies**.

The pipeline combines:

* Automated YouTube data collection
* Structured data wrangling and feature engineering
* Hybrid LLM + transformer labeling workflow
* Confidence-aware sentiment filtering
* Event-driven temporal sentiment analysis

The study spans major events from the game's reveal through launch and post-release updates, enabling longitudinal sentiment tracking. 

---

## Repository Structure

```text
CAP5771_SI.SEENIVASAN/
│
├── data/                            # Processed datasets
│   ├── comments_data.csv            # Raw dataset used for EDA
│   ├── comments_for_analysis.csv    # Cleaned dataset after wrangling
│   ├── comments_labeled.csv         # Final labeled dataset
│   ├── comments_llama_labeled.csv        
│   ├── comments_llama_labeled.jsonl # LLM labeling outputs
│   └── roberta_classifications.csv  # Baseline transformer predictions
│
├── preprocessing/                   # Data preparation notebooks
│   ├── Data_Wrangling.ipynb
│   ├── EDA.ipynb
│   ├── Llama_Labeler.ipynb
│   ├── Manual_Labeling_Analysis.ipynb
│   ├── roberta_classification.py
│   └── absa_labeler.log
│
├── figures/                         # EDA visualizations
│
├── src/                             # Data collection pipeline
│   ├── database.py
│   ├── discovery.py
│   └── collector.py
│
├── diary/                           # Coursework reflections
│
├── ECJ_Analysis.ipynb               # Analysis notebook for paper
├── arc_raiders_sentiment.db         # SQLite database
├── main.py                          # Pipeline entrypoint
├── collection_log.txt               # Collection logs
├── comments.txt                     # Raw export
├── requirements.txt
├── LICENSE
└── README.md
```

---

---

## Methodology

### 1. Data Collection Pipeline

Data was collected using the YouTube Data API v3 through a custom pipeline:

* Video discovery via keyword search
* Full comment thread extraction (including replies)
* Metadata collection (timestamps, likes, etc.)
* Storage in a SQLite database with deduplication

All user identifiers are anonymized via SHA-256 hashing.

---

### 2. Data Wrangling & Feature Engineering

Implemented in `Data_Wrangling.ipynb`.

#### Data Cleaning

* Removed duplicates and missing entries
* Filtered non-English comments
* Standardized timestamps for time-series analysis

#### Feature Engineering

**Event Features**

* Binary indicators for:

  * Game announcements
  * AI-related discussions
  * Monetization changes
  * Release events

**Temporal Features**

* Days relative to event
* Pre/post-event window indicators

**Engagement Features**

* `like_count_log = log(1 + likes)`
* Engagement tiers
* Comment timing after video upload

**Text Processing**

* URL normalization
* Noise removal
* Token-safe formatting

---

### 3. LLM-Based Aspect-Based Sentiment Analysis (ABSA)

#### Model

* Llama 3.3 70B (UF HiPerGator NaviGator)

#### Task

Each comment is labeled for:

* Sentiment: Positive / Neutral / Negative
* Aspect:

  * Game-related
  * AI-related

#### Why ABSA?

Traditional sentiment classification fails to separate:

> "The game looks great but the AI voices are terrible"

ABSA allows isolating **controversy-specific sentiment**, which is critical for analysis.

---

### 4. Validation of LLM Labels

A manually annotated **Gold Dataset (n ≈ 1000)** was created.

#### Metric

* **Gwet’s AC1** (robust to class imbalance)

#### Result

* AC1 ≈ 0.98 → near-perfect agreement

#### Conclusion

LLM labels are treated as **reliable ground truth** for downstream analysis.

---

### 5. Event Detection Framework

* Daily comment volume aggregation
* Spike detection using statistical thresholds
* Manual verification using:

  * Video uploads
  * Keywords
* Event categorization:

  * Announcements
  * AI controversies
  * Monetization changes
  * Releases/updates

---

### 6. Sentiment Half-Life Modeling (Core Contribution)

We model how sentiment evolves after an event using exponential decay:

```
S(t) = S₀ e^(−λt)
```

Half-life:

```
t½ = ln(2) / λ
```

#### Interpretation

* **Short half-life** → temporary backlash (low risk)
* **Long half-life** → sustained dissatisfaction (high risk)

---

### 7. Engagement-Weighted Sentiment (Silent Majority)

Raw sentiment is adjusted using:

```
like_count_log = log(1 + likes)
```

#### Purpose

* Captures **community agreement**, not just comment volume
* Identifies whether negative sentiment is:

  * Vocal minority OR
  * Widely endorsed opinion

---

### 8. Temporal Sentiment Analysis

Event windows:

* Pre-event (−7 days)
* Event window (±2 days)
* Post-event (+7 days)

Analyzed metrics:

* Sentiment ratios
* Polarization trends
* Recovery trajectories

---

## Key Insights

This framework enables:

* Detection of **event-driven sentiment spikes**
* Measurement of **outrage persistence**
* Identification of **true community consensus**

Example insight:

* AI-related controversies show:

  * Stronger negative sentiment
  * Longer recovery times
  * Higher engagement-weighted agreement

---

## How to Run the Project

### 1. Setup

```bash
git clone https://github.com/sibi-seeni/CAP5771_si.seenivasan.git
cd CAP5771_si.seenivasan

uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Set environment variables:

```
YOUTUBE_API_KEY=your_key
NAVIGATOR_API_KEYS=your_key
```

---

### 2. Pipeline Execution

#### Data Collection

```bash
python main.py full
```

(Optional: download DB from HuggingFace and skip collection)

#### EDA

```
preprocessing/EDA.ipynb
```

#### Data Wrangling

```
preprocessing/Data_Wrangling.ipynb
```

#### LLM Labeling

```
preprocessing/Llama_Labeler.ipynb
```

#### Gold Dataset Validation

```
preprocessing/Manual_Labeling_Analysis.ipynb
```

#### Final Analysis (Paper)

```
ECJ_Analysis.ipynb
```

---

## Outputs

### Datasets

* `comments_for_analysis.csv`
* `comments_llama_labeled.csv`
* `comments_labeled.csv`

### Database

* `arc_raiders_sentiment.db`

### Figures

* Temporal sentiment plots
* Event spike visualizations
* Decay curves
* Engagement-weighted sentiment charts

### Logs

* `collection_log.txt`
* `absa_labeler.log`

---

## Research Contributions

* Event-driven sentiment analysis for gaming communities
* LLM-based ABSA pipeline validated with AC1
* Sentiment half-life modeling (novel contribution)
* Engagement-weighted consensus detection
* Empirical analysis of AI-related gaming controversies

---

## Future Work

* Cross-platform validation (Reddit, Twitter)
* Multilingual sentiment analysis
* Emotion classification beyond polarity
* Real-time monitoring dashboard for studios

---

## References

* **Singh, R. K., & Thomas, A. (2025).** *A Systematic Literature Review of YouTube Comments Sentiment Analysis: Challenges and Emerging Trends.* ICTACT Journal on Data Science and Machine Learning, 7(1). [https://doi.org/10.21917/ijdsml.2025.0184](https://doi.org/10.21917/ijdsml.2025.0184)

* **Tohidi, K., Dashtipour, K., Rebora, S., & Pourfaramarz, S. (2025).** *A Comparative Evaluation of Large Language Models for Persian Sentiment Analysis and Emotion Detection in Social Media Texts.* arXiv preprint arXiv:2509.14922. [https://arxiv.org/abs/2509.14922](https://arxiv.org/abs/2509.14922)

* **He, Y., He, Z., Gu, T., Gu, B., Wan, Y., & Li, M. (2025).** *Multi-Chain of Thought Prompt Learning for Aspect-Based Sentiment Analysis.* Applied Sciences, 15, 12225. [https://doi.org/10.3390/app152212225](https://doi.org/10.3390/app152212225)

* **Schmitt, M., Schwerk, A., & Lempert, S. (2026).** *Enhancing Sentiment Classification and Irony Detection in Large Language Models through Advanced Prompt Engineering Techniques.* arXiv preprint arXiv:2601.08302. [https://arxiv.org/abs/2601.08302](https://arxiv.org/abs/2601.08302)

* **Silveira, P. S. P., & Siqueira, J. O. (2023).** *Better to Be in Agreement Than in Bad Company: A Critical Analysis of Many Kappa-Like Tests.* Behavior Research Methods, 55, 3326–3347. [https://doi.org/10.3758/s13428-022-01950-0](https://doi.org/10.3758/s13428-022-01950-0)

* **Loureiro, D., Barbieri, F., Neves, L., Espinosa Anke, L., & Camacho-Collados, J. (2022).** *TimeLMs: Diachronic Language Models from Twitter.* arXiv preprint arXiv:2202.03829. [https://arxiv.org/abs/2202.03829](https://arxiv.org/abs/2202.03829)

* **Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017).** *On Calibration of Modern Neural Networks.* arXiv preprint arXiv:1706.04599. [https://arxiv.org/abs/1706.04599](https://arxiv.org/abs/1706.04599)

* **Giachanou, A., & Crestani, F. (2016).** *Like It or Not: A Survey of Twitter Sentiment Analysis Methods.* ACM Computing Surveys, 49(2), Article 28, 41 pages. [https://doi.org/10.1145/2938640](https://doi.org/10.1145/2938640)

---

*This project is submitted as part of the MS in Applied Data Science coursework at the University of Florida. It adheres to YouTube API Terms of Service and ethical guidelines regarding public data collection.*
