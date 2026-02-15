## What features are you keeping for data preview (and why)?

For data preview, I am keeping the following features:

From the **comments table**:

* `comment_id` – to verify uniqueness and detect duplicates
* `text` – main variable for NLP and length analysis
* `comment_date` – for time-based trends
* `author_hash` – to analyze user-level activity
* `last_updated_at` – to check for edits or data freshness

From the **videos table**:

* `video_id` – key for joining and aggregation
* `video_title` – to interpret engagement spikes
* `video_date` – for temporal comparison with comment dates
* `channel_id` – for grouping by creator
* `keyword_matched` – to see if filtering affected engagement
* `comments_disabled` – to understand missing comment behavior

I kept these because they directly support:

* Text analysis
* Engagement aggregation
* Temporal spike detection
* Video-level concentration analysis

---

## Descriptive Values for Variables of Interest

### Comments Table

* Total rows: **311,548 comments** from 4,566 videos
* Missing `text`: No missing data
* Missing `comment_date`: No missing data
* Duplicate `comment_id`: No duplicated data

Text length:

* Max length: 9740 characters (1702 words)
* Mean length: ~119 characters (22 words)

Token limit insight:
A small portion of comments exceed 512 tokens (RoBERTa limit), meaning truncation would be required for transformer modeling.

---

### Videos Table

* Total videos: 4566 (including long-form and short-form content)
* Videos with comments disabled: 72

Engagement distribution:
A small subset of videos accounts for a large portion of total comments, indicating a heavy-tailed distribution.

---

## Snippets

```
RangeIndex: 311548 entries, 0 to 311547
Data columns (total 11 columns):
 #   Column             Non-Null Count   Dtype         
---  ------             --------------   -----         
 0   comment_id         311548 non-null  str           
 1   text               311548 non-null  str           
 2   comment_date       311548 non-null  datetime64[us]
 3   author_hash        311548 non-null  str           
 4   last_updated_at    311548 non-null  str           
 5   video_id           311548 non-null  str           
 6   video_title        311548 non-null  str           
 7   video_date         311548 non-null  datetime64[us]
 8   channel_id         311548 non-null  str           
 9   keyword_matched    311548 non-null  str           
 10  video_description  311548 non-null  str 
```

And:

```
Total Videos: 4,566
Total Comments: 311,548
Unique Channels: 1,531
Unique Commenters: 196,857
Date Range: 2025-10-30 to 2026-02-14
```
---