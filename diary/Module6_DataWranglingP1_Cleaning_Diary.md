# Data Cleaning Diary for Module 6

### Overview

In this phase, I focused on making the dataset analytically reliable before moving into modeling and sentiment analysis. The goal was to eliminate structural noise, standardize formats, and ensure that the remaining comments represent meaningful, high-quality input data.

---

## Top Data Problems I Fixed First (and Why)

### 1. Missing and Empty Text Fields

**Why this first?**
Sentiment analysis depends entirely on textual input. Rows with missing or empty `text` or `video_description` fields are unusable for NLP tasks and would distort later statistics.

### Rule Applied:

* **Drop** rows where:

  * `video_description` is null
  * `text` is null
  * `video_description` or `text` is an empty string (after stripping whitespace)

This ensures that all retained rows contain meaningful content.

#### Before vs After (Structure Summary)

**Before cleaning:**

* Dataset loaded with full row count from `comments_data.csv`
* Included nulls and empty strings in key text columns

```python
data.isna().sum()
```

**After filtering:**

```python
filtered_data = data[
    data['video_description'].notna() &
    data['text'].notna()
]
```

Result:

* All remaining rows contain usable comment text
* Removed structurally invalid observations

This step reduced dataset size but still kept up the relevant entries.

---

### 2. Datetime Inconsistency

**Why?**
Time-based features are central to my project (event reactions, sentiment decay, comment latency). Incorrect datetime types would break temporal calculations.

### Rule Applied:

* **Convert** string columns to datetime:

  * `comment_date`
  * `video_date`
  * `last_updated_at`
* **Sort** dataset chronologically by `comment_date`

```python
data['comment_date'] = pd.to_datetime(data['comment_date'])
data = data.sort_values('comment_date').reset_index(drop=True)
```

This enabled:

* Event-relative day calculations
* Latency metrics
* Time-series analysis

---

### 3. Low-Quality and Non-English Comments

**Why this early?**
My sentiment model (RoBERTa) is English-based. Non-English text and very short comments (e.g., “lol”, “ok”) introduce noise and reduce signal clarity.

### Rule Applied:

* **Filter**:

  * `language == 'en'`
  * `word_count >= 3`
  * `text` not null

```python
data_clean = data[
    (data['language'] == 'en') &
    (data['word_count'] >= 3)
].copy()
```

This step prioritizes consistency and keeps only meaningful content.

---

### 4. Bot-like or Duplicate Comments

**Why important?**
Duplicate comments inflate frequency-based analysis and bias engagement statistics.

### Rule Applied:

* **Deduplicate** identical comment texts

```python
data_clean = data_clean.drop_duplicates(subset=['text'], keep='first')
```

This reduces artificial amplification and improves fairness in engagement-weighted sentiment scoring.

---

### 5. Text Normalization for NLP

**Why necessary?**
Transformer models are sensitive to noise like URLs and user mentions.

### Rule Applied:

* **Normalize**:

  * Replace URLs → `[URL]`
  * Replace @mentions → `[USER]`
  * Normalize whitespace

```python
text = re.sub(r'http\S+|www\S+', '[URL]', text)
text = re.sub(r'@\w+', '[USER]', text)
```

This preserves semantic meaning while reducing token noise.

---

## Remaining Risks

Even after cleaning, several risks remain:

### 1. Language Filtering Bias

Filtering to English-only:

* Removes potentially valid opinions
* Biases sentiment toward English-speaking users
* May underrepresent global player perspectives

### 2. Short Comment Removal

By enforcing `word_count >= 3`, I removed:

* Emotional but short reactions (“trash”, “amazing”)
* Highly polarized but concise feedback

This may dampen extreme sentiment representation.

### 3. Duplicate Removal Assumptions

Dropping identical text assumes:

* Repeated comments are bots or spam
  However:
* Some real users may independently write identical short reactions

This could slightly distort engagement frequency.

### 4. Engagement Skew

Like counts are highly skewed:

* A small fraction of comments drive most engagement
* Future weighting decisions could amplify popularity bias

---