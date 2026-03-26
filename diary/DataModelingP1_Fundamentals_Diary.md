# Diary Entry 9: Data Modeling I - Fundamentals

**Which model(s) did you choose to try first, and why?**

I started with RoBERTa as my first model since this is a text classification problem and transformers generally perform well on sentiment tasks. I used it as a baseline before experimenting with Llama 3.3 70B to generate better labels. The idea was to use the LLM for supervision, and buidling the ground truth (with manual oversight too) and smaller models for actual classification, and fine-tuning later.

**Explain your reasoning in term sof the problem type (problem type, interpretability, complexity, and data size).**

Since this is NLP classification, transformers are the current technical benchmarks. Pretrained models also reduced complexity since I didn’t need feature engineering. Even though my dataset is big, in the field of NLP, it actually isn’t that big, so transfer learning through fine-tuning was more practical than training anything from scratch.

**What assumptions does your model make about the data?**

The main assumption of NLP models are that the text patterns in training and testing are similar and that the sentiment labels are accurate. They also assume context (the word before and after) carries sentiment meaning, which is why transformer embeddings work well. The LLM labeling assumes the GenAI reasoning is mostly correct, which I did partially verify with manual go through.

**What split will you decide for train/validation/test? why?**

Later, for the fine-tuning of the RoBERTa model, I decided to go with a 70/20/10 split to balance learning and evaluation. The validation set helps tune the models while the test set stays untouched for fair comparison. I also manually checked 1000 samples to make sure the LLM labels were reliable.

---
