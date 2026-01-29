### 1. WHERE THE DATA WOULD COME FROM:

The plan is to collect the data for the project through the YouTube Data API, which is free (up to a daily limit) for research/academic purposes.

I am collecting the data from all videos posted with the keywords like "Arc Raiders", "Arc Raiders gameplay", "Arc Raiders review", "#ArcRaiders", "ARC RAIDERS", and "arc raiders". This is then stored, and another script pulls comments from all these videos, with the addition of having a cutoff date, either Oct 30, when the game was released, as well as checking the db for the latest pull.

--

### 2. HOW IT WOULD BE COLLECTED:

I am writing a set of scripts for this purpose, and that will pull the comments data from youtube videos posted about the game "ARC Raiders" since its release.
- i. `database.py` script is used to set up the SQL database to store the pulled videos and respective comments.
- ii. `discovery.py` script runs the set of keywords to search for videos that were posted about Arc Raiders, and store it as a table in the database.
- iii. `collector.py` is the script that actually collects the comments from the discovered videos.

--

### 3. KNOWN LIMITATIONS:

Storing the collectd data, as well the API rate limits are known limitations for this project. Another limitation I expect to hit is whether enough comments and videos are posted now (a couple of months after release) for me to analyse.
- UPDATE: An issue I faced while collecting the data was the fact that the script pulls the comments/vidoes again and again (duplication).

--