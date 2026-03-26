# Diary Entry 10: Data Modeling II - Evaluation

**What evaluation metrics did you choose and why?**

I used accuracy, F1 score, precision, and recall since sentiment data can be slightly imbalanced. I also used *Cohen’s Kappa* on the 'Gold Dataset' created by manual labeling to measure how well the LLM labels matched my validation. This is so that I can confidently say that my training data was trustworthy.

**How does your model compare to the baseline?**

The initial RoBERTa baseline worked reasonably well, but fine-tuning will improve consistency and F1 scores. I am also planning to implement a DeBERTa-v3, which is expected to perform slightly better in some edge cases. *Llama* performed strongly without training, but the fine-tuned smaller models will get close while being **much cheaper** to run.

**What does feature importance suggest about the patterns your model is using?**

Since transformers don’t have traditional feature importance, I looked at errors and confidence scores instead. The models seem to rely heavily on emotional wording and reaction phrases rather than simple keywords. Most mistakes happen with sarcasm or with slang words - as they depend upon context that are outside of the particular input sentence too. I was able to engineer this context by adding additional inputs to *Llama* like the video_title, video_description, and parent_comment, which is not possible in RoBERTa and DeBERTa based models.

---
