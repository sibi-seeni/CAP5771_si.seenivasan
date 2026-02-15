# Arc Raiders Sentiment Analysis Pipeline

### Project for CAP5771: Introduction to Data Science

## Project Overview

My project implements an end-to-end data engineering and NLP pipeline to track community sentiment for the video game **Arc Raiders** (developed by Embark Studios). By utilizing the YouTube Data API v3 and a State-of-the-Art (SOTA) Transformer model, I analyze how sentiment shifts in response to game updates, roadmaps (e.g., the 2026 Roadmap), and seasonal events.

The study period covers the game's launch (October 30, 2025) through the present, providing a longitudinal view of community reception.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Repository Structure](#repository-structure)
* [Methodology & Progress](#methodology--progress)

  * [Data Source: The YouTube Data API v3 (Phase 1)](#data-source-the-youtube-data-api-v3-phase-1)
  * [Data Engineering (Phases 2-3)](#data-engineering-phases-2-3)

    * [ER Diagram](#er-diagram)
  * [Data Exploration (Phase 4)](#data-exploration-phase-4)
  * [Future Steps: Natural Language Processing](#future-steps-natural-language-processing)
* [How to Run the Program](#how-to-run-the-program)

  * [1. Prerequisites](#1-prerequisites)
  * [2. Setup](#2-setup)
  * [3. Execution](#3-execution)
  * [4. Alternative](#4-alternative)
* [Expected Outputs](#expected-outputs)
* [References](#references)

---

## Repository Structure

```text
CAP5771_si.seenivasan/
├── diary/                   # Diary entries for CAP5771
├── src/                     # Source Code for Data Acquisition
│   ├── __init__.py          # Package initialization
│   ├── database.py          # Phase 3: SQLAlchemy models & SQLite schema
│   ├── discovery.py         # Phase 2: Automated video discovery
│   └── collector.py         # Phase 2: Comment scraping
├── .env                     # (Git-ignored) YOUTUBE_API_KEY
├── .gitignore               # Ensures sensitive/large data is not pushed to GitHub
├── collection_log.txt       # (Git-ignored) Pipeline execution logs
├── arc-raiders-sentiment.db # (Git-ignored) SQLite3 Database to store all collected data
├── main.py                  # Pipeline orchestrator (Entry Point)
├── EDA.ipynb                # Jupyter Notebook that contains the data exploration
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation

```

---

## Methodology & Progress

### Data Source: The YouTube Data API v3 (Phase 1)

The primary data for this study was retrieved using the YouTube Data API v3, a RESTful interface provided by Google that allows for the systematic collection of video metadata and user-generated comments. For this project, the API was leveraged to perform **keyword-based discovery** of Arc Raiders content and to conduct deep-crawl extractions of **associated comment threads** for sentiment analysis.

In the current landscape of computational social science, the YouTube Data API represents a critical resource, as it remains one of the last prominent, high-fidelity social media APIs accessible to researchers without the prohibitive costs or restrictive access tiers recently implemented by platforms such as X (formerly Twitter) and Reddit.

### Data Engineering (Phases 2-3)

* **Incremental Discovery:** Implemented a state-aware search logic that tracks `last_search_time` to avoid redundant API calls and manage daily quotas.
* **Data Privacy (Ethics):** As I am planning to work towards an article, all user identifiers are anonymized using **SHA-256 hashing** (`author_hash`) before storage to ensure data minimization.
* **Database Infrastructure:** Built a relational SQLite schema using SQLAlchemy to handle video-comment relationships and maintain search state. Implemented 2-layer deduplication (Memory Set + DB Unique Constraints).

#### ER Diagram

```mermaid
%%{init: {
  "themeVariables": {
    "fontSize": "9px"
  }
}}%%
erDiagram
    VIDEOS {
        string video_id PK
        string title
        text description
        string channel_id
        datetime published_at
        string keyword_matched
        datetime first_seen_at
        boolean comments_disabled
    }

    COMMENTS {
        string comment_id PK
        string video_id FK
        string parent_id
        string author_hash
        text text
        datetime published_at
        datetime last_updated_at
    }

    COLLECTION_STATE {
        string keyword PK
        datetime last_search_time
    }

    VIDEOS ||--o{ COMMENTS : has
```

### Data Exploration (Phase 4)

* **Loading the database:** SQL Joins were performed on the stored data to load into pandas DataFrames. 
* **Text-based analysis:** Examines comment length distributions, word frequency trends, multilingual presence, and sentiment-indicating vocabulary. Special consideration is given to transformer-based NLP constraints, such as the 512-token input limit for RoBERTa, ensuring that the dataset is suitable for downstream modeling. Domain-specific keyword detection provides insight into community discourse and feature-driven discussions.
* **Time-based analysis:** It revealed some useful insights, like that engagement is highly concentrated, and approximately 14% of total comment volume occurs during statistically significant spike days, largely driven by a small number of high-performing videos. This indicates a heavy-tailed engagement distribution, where a minority of videos account for a disproportionate share of interaction.

Overall, the dataset demonstrates strong potential for sentiment modeling, engagement prediction, and event-driven trend analysis.

### Future Steps: Natural Language Processing

* **Model Selection:** Utilized `cardiffnlp/twitter-roberta-base-sentiment-latest`, a RoBERTa-base model fine-tuned on 124M tweets, providing superior nuance over lexicon-based methods like VADER.
* **Confidence Filtering:** Implementing a "Reject Option" based on **Softmax Probability** (Hendrycks & Gimpel, 2016). Only predictions with confidence > 0.70 are utilized for trend analysis to reduce noise.
* **Interaction Weighting:** To account for community consensus, a **Popularity-Weighted Sentiment** feature will be engineered:
$$\text{Weighted Score} = \text{Sentiment Label} \times \log(1 + \text{Like Count})$$. This prevents viral outliers from skewing trends while ensuring highly-voted community feedback is prioritized (Giachanou & Crestani, 2016).

---

## How to Run the Program

### 1. Prerequisites

* Python 3.10+
* A Google Cloud Project with the **[YouTube Data API v3](https://developers.google.com/youtube/v3/getting-started)** enabled.
* An API Key.

### 2. Setup

1. **Clone the repository:**
```bash
git clone https://github.com/sibi-seeni/CAP5771_si.seenivasan.git
cd CAP5771_si.seenivasan
````

2. **Create a virtual environment with uv:**

```bash
uv venv .venv
```

3. **Activate the virtual environment:**

* macOS / Linux: `source .venv/bin/activate`

* Windows (PowerShell): `.venv\Scripts\Activate.ps1`

4. **Install dependencies using uv:**

```bash
uv pip install -r requirements.txt
```

5. **Configure Environment:**
   Create a `.env` file in the root directory and add your key:

```text
YOUTUBE_API_KEY=your_actual_key_here
```


### 3. Execution

To run the full pipeline (Discovery -> Collection -> Storing), execute the main orchestrator:

```bash
python3 main.py

```

Next, for performing exploratory data analysis, run the Jupyter Notebook `EDA.ipynb` in the main directory.


### 4. Alternative:

If you want to skip the data collection pipeline, and directly start from data exploration, the database can be downloaded directly from [HuggingFace](https://huggingface.co/datasets/persona-156/arc-raiders-sentiment/tree/main): `persona-156/arc-raiders-sentiment/arc_raiders_sentiment.db`, and storing it in the root directory after cloning (In Step 2).

---

## Expected Outputs

* **`arc_raiders_sentiment.db`**: A local database containing thousands of categorized comments.
* **`collection_log.txt`**: A detailed log of API quota usage and video discovery counts.
* **`comments_data.csv`**: The dataframe on which EDA was performed, exported into a CSV for reference.

---

## References

* **Loureiro, D., et al. (2022).** *TimeLMs: Diachronic Language Models from Twitter.* (Base for the RoBERTa model used).
* **Guo, C., et al. (2017).** *On Calibration of Modern Neural Networks.* ICML. (Validation for Confidence Scoring).
* **Giachanou, A., & Crestani, F. (2016).** *Like It or Not: A Survey of Twitter Sentiment Analysis Methods.* ACM Computing Surveys. (Validation for Engagement Weighting).

---

*This project is submitted as part of the MS in Applied Data Science coursework at the University of Florida. It adheres to YouTube API Terms of Service and ethical guidelines regarding public data collection.*
