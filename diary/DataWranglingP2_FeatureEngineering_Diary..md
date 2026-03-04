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
    'text', 'text_preprocessed',
    'video_context', 'video_id',
    'comment_date', 'author_hash',
    'days_from_genai_announcement',
    'days_from_business_model_change',
    'days_from_game_launch',
    'mentions_genai', 'mentions_business_model',
    'likes', 'like_count_log'
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

## Before vs After Example: Engagement Transformation

### Before:

* `likes` highly skewed
* Many zeros
* Few extreme high values

### After:

* `like_count_log` compresses scale
* Engagement tiers categorize intensity:

Example tier bins:

* `no_likes`
* `low_engagement`
* `medium_engagement`
* `high_engagement`
* `viral`

This makes modeling more stable and interpretable.

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