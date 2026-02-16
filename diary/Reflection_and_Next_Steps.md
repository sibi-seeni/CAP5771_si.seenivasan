## Reflection

Working on this project helped me understand what it actually means to build a full pipeline, not just run analysis on a dataset someone else gives you. I had to collect the data, store it properly, avoid duplicates, and think about API limits. That part made me realize how important structure and planning are before doing any modeling.

The data exploration phase was also very useful. I saw that engagement is not evenly spread out. A small number of videos get a lot of comments, and certain days have big spikes. Around 14% of all comments happened during spike days, which surprised me. I also had to think about practical issues like the 512-token limit for RoBERTa, which made me more careful about text length and preprocessing. Overall, the exploration helped me understand the data better before jumping into sentiment analysis.

## Next Steps

The next step is to actually run the sentiment model and turn the comments into sentiment scores. I plan to:

* Use the RoBERTa sentiment model mentioned in the README.
* Filter out low-confidence predictions (only keep scores above 0.70).
* Create a popularity-weighted sentiment score using like counts.
* Track how sentiment changes over time.
* Compare sentiment during spike days vs normal days.

In the future, I also want to check whether high-engagement videos behave differently from low-engagement ones, and whether engagement concentration affects overall sentiment trends.
