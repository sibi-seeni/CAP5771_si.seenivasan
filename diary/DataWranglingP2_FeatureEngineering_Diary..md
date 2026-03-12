# Data Wrangling – Part 2: Feature Engineering Diary

### Overview

After cleaning the dataset, I engineered features designed to capture temporal context, event relevance, engagement intensity, and conversational structure. These features transform raw comments into analytically meaningful variables.

---

## Features Engineered (and Why)

### 1. Event Mention Detection

**Why?**
I wanted to identify comments directly responding to major announcements:

* GenAI voice announcement
* Business model change
* Game launch

### Implementation:

Binary keyword detection:

```python
data['mentions_genai'] = data['text'].apply(...)
data['mentions_business_model'] = data['text'].apply(...)
```

This allows:

* Isolating event-driven discourse
* Comparing sentiment between event-focused and general comments

---

### 2. Temporal Distance from Major Events

**Why?**
Sentiment often decays or intensifies over time after announcements.

### Implementation:

For each event:

```python
data['days_from_genai_announcement'] = (
    data['comment_date'] - event_date
).dt.days
```

This enables:

* Pre vs post-event comparison
* Sentiment decay modeling
* Time-relative regression analysis

---

### 3. Engagement Features

Engagement is central to weighted sentiment modeling.

#### Engineered:

* `has_likes` → Boolean engagement flag
* `like_count_log` → Log transform to reduce skew
* `engagement_tier` → Categorical binning
* `comment_latency_days` → Time between upload and comment
* `latency_category` → Binned latency class

Example transformation:

```python
data['like_count_log'] = np.log1p(data['likes'])
```

**Why log-transform?**
Like distributions are heavily right-skewed. Log scaling:

* Reduces dominance of viral comments
* Stabilizes variance for modeling

---

### 4. Conversational Context Features

To enrich context for future LLM analysis:

* `video_context` → First 500 characters of description
* `parent_text` → Mapped parent comment for replies

This allows:

* Thread-level sentiment analysis
* Conversation-aware modeling

---

## Feature Selection: What I Removed and Why

In the final dataset, I retained only analytically relevant columns:

```python
columns_to_keep = [
    'comment_id', 'parent_id', 'parent_text',
    'text_preprocessed',    
    'video_context', 'video_id',               
    'comment_date', 'author_hash',             
    'days_from_genai_announcement', 
    'days_from_business_model_change', 
    'days_from_game_announcement',
    'days_from_early_access',
    'days_from_game_launch',              
    'mentions_genai', 'mentions_business_model',
    'mentions_launch', 'has_likes', 
    'engagement_tier', 'comment_latency_days', 
    'comment_latency_hours', 'latency_category',
    'likes', 'like_count_log'] 
]
```

### Removed Columns

* Redundant timestamp variants
* Unused auxiliary fields

### Justification:

* **Relevance**: Only features tied to sentiment, time, or engagement were retained.
* **Redundancy**: Derived fields replaced raw equivalents.
* **Ethics**: No personally identifiable information retained (only `author_hash`).

---

### Tokenization

A surprising finding for me is that accessing the model using `tweetnlp` also loads the specific tokenizer for the same, so I need not perform a separate step during feature engineering to perform the appropriate tokenization. I will be using it for performing the sentiment classification task next.

---

## Before vs After Summary (Dataset Structure)

### Before Cleaning (`data.info()`)

```text
<class 'pandas.DataFrame'>
RangeIndex: 210486 entries, 0 to 210485
Data columns (total 27 columns):

 0   comment_id        210486 non-null  str
 1   text              210400 non-null  str
 2   comment_date      210486 non-null  str
 3   author_hash       210486 non-null  str
 4   parent_id          46219 non-null  str
 ...
12   video_description 192158 non-null  str
...
24   language          210486 non-null  str
```

**Key observations before cleaning:**

* 210,486 total rows
* Missing values in `text` (86 missing)
* Significant missing values in `video_description`
* Datetime columns stored as strings
* 27 total columns (including raw metadata and unused fields)

---

### After Cleaning + Feature Engineering

```text
<class 'pandas.DataFrame'>
Index: 143065 entries, 1 to 192075
Data columns (total 15 columns):

 0   comment_id                       143065 non-null  str
 1   parent_id                        29931 non-null   str
 2   parent_text                      29931 non-null   str
 3   text_preprocessed                143065 non-null  str
 4   video_context                    143065 non-null  str
 5   video_id                         143065 non-null  str
 6   comment_date                     143065 non-null  datetime64[us]
 7   author_hash                      143065 non-null  str
 8   days_from_genai_announcement     143065 non-null  int64
 9   days_from_business_model_change  143065 non-null  int64
10   days_from_game_launch            143065 non-null  int64
11   mentions_genai                   143065 non-null  bool
12   mentions_business_model          143065 non-null  bool
13   likes                            143065 non-null  int64
14   like_count_log                   143065 non-null  float64
```

**What changed:**

* Rows reduced from **210,486 → 143,065** after filtering
* Columns reduced from **27 → 15** (removed unused metadata and redundant fields)
* All retained text fields now fully non-null
* `comment_date` successfully converted to `datetime64`
* Added engineered features:

  * Event-relative day counts
  * Event mention flags
  * Log-transformed engagement (`like_count_log`)

> After cleaning and feature selection, the dataset became smaller but structurally stronger. The row count dropped from 210,486 to 143,065 due to removing missing, low-quality, and irrelevant entries. Columns were reduced from 27 to 15, focusing only on variables relevant to sentiment, engagement, and event timing. Datetime fields were properly typed, and engineered features replaced several raw metadata fields, making the dataset more modeling-ready and easier to interpret.

---

## Risks and Interpretation Considerations

### 1. Keyword-Based Event Detection

* May miss implicit references
* May falsely classify sarcasm or unrelated usage

### 2. Log Transformation Bias

Log scaling reduces dominance of viral comments, but:

* It also reduces the relative influence of genuinely important high-impact discourse.

### 3. Engagement Tiers

Bin thresholds are manually defined:

* Different bin cutoffs could change results
* This introduces researcher subjectivity

### 4. Temporal Framing

Using fixed event dates assumes:

* All audience members react immediately
  In reality:
* Exposure timing varies significantly

---
