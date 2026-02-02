## DATABASE MANAGEMENT

## 1. Table Connections and Diagram
I designed the database using a Relational Schema (SQLAlchemy) to ensure data integrity and minimize redundancy.

* **Relationship:** The 'Videos' table and 'Comments' table are connected via a One-to-Many relationship. 
* **Foreign Key:** The `video_id` in the Comments table acts as a Foreign Key pointing to the primary record in the Videos table.
* **Threading:** The `parent_id` in the Comments table allows for a "self-referencing hierarchy", which enables me to re-establish reply threads in comments.
* **State Tracking:** The 'CollectionState' table operates independently to track the 'last_search_time' for specific keywords, helping me manage incremental data updates and pulls.

## 2. Unstructured Data Handling
The primary unstructured data in this project consists of the `text` column in the Comments table and the `description` column in the Videos table.

* **Raw Text:** These fields contain emojis, slang, and non-standard punctuation that cannot be analyzed through standard SQL queries.
* **Proposed handling for upcoming weeks:** 
    * **Cleaning:** During the processing phase, I will use Python (NLTK or spaCy) to remove stop words and special characters.
    * **Languages:** I have not decided yet to handle comments in other languages apart from English, whehter to drop them, or keep them for added metrics.
    * **Sentiment Extraction:** I will transform this unstructured text into structured "Sentiment Scores" (Numerical) to be stored in a future table.
* **Ethical Handling:** User identities are treated as sensitive; the `author_hash` variable is used to anonymize users while still allowing for the analysis of unique contributors.