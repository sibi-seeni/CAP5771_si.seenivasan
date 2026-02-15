## Issues Identified

### 1. Long Comments (Model Constraint Issue)

Where: `text` column
How big: The exact % was not yet computed

Meaning: Comments longer than 512 tokens cannot be directly processed by RoBERTa without truncation. This could result in loss of information.

---

### 2. Engagement Concentration

Where: Popular videos (Aggregated `video_id` comment counts)
How big: ~14% of total comment volume occurs during spike days (as observed in time-based analysis).

Meaning: Engagement is highly concentrated and not evenly distributed. This may bias modeling if not normalized.

---

### 3. Potential Language Noise

In the collected data, majority of the **comments are in English** (75.5%), and all the other languages are split up with the second being Russian with a far off 4.5%. However, the non-English comments may affect sentiment modeling as I am using English-only models.

---

### 4. Missingness

As I have collected the data on my own, I encountered no missing data, and no duplicates too.

---

## Some potential stakeholder questions

1. Should non-English comments be translated, filtered, or modeled separately?
2. Should extremely long comments be truncated or excluded?
3. Are edited comments meaningful for analysis, or should only original timestamps be used?
4. Should engagement spikes be treated as outliers or analyzed separately?

These questions majorly affect modeling decisions and interpretation.