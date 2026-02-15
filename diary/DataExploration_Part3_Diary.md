## Feature / Relationships Explored

I focused on:

* Comment length vs engagement patterns
* Time (comment_date) vs volume spikes
* Video-level comment distribution
* Language distribution
* Keyword presence and gaming-specific terminology

---

## Why I Chose These Variables

These variables directly relate to:

* NLP feasibility (text length, token limit)
* Engagement modeling
* Event-driven activity detection
* Community behavior patterns

---

## What I Expected to Find

I expected:

* A long-tailed engagement distribution
* Majority English comments
* Most comments to be short (under 512 tokens)

---

## What the Visualizations Revealed

* Engagement is highly concentrated — a small number of videos generate disproportionate comments.
* Approximately 14% of total volume happens during spike days.
* Most comments fall within reasonable length ranges, but a minority exceed model token limits.
* No clear linear relationship between time and engagement; instead, spikes are event-driven (nonlinear).

---

## Strength of Relationships

* Engagement distribution: Strongly skewed (heavy-tailed).
* Time vs volume: Nonlinear, spike-driven.
* Text length vs frequency: Slightly right-skewed distribution.

No strong linear relationships were observed.

---

## Clusters or Group Differences

Yes:

* High-engagement videos form a distinct cluster separate from the majority of low-engagement videos.
* Spike days represent temporal clusters.

---

## What Surprised Me

* How concentrated engagement was.
* The proportion of comment volume occurring in short time windows.
* The existence of extremely long comments beyond typical conversational length.

---

## Did Anything Contradict My Initial Hypothesis?

Not strongly. The heavy-tailed distribution and spike behavior matched expectations. However, I expected engagement to be slightly more evenly distributed across videos.

---