## DATA DICTIONARY:

## 1. Table: Videos
I have set up this table to contain metadata for YouTube videos retrieved via keyword search through `discovery.py`.

| Variable Name      | Data Type | Description                                         | Attributes        |
|:-------------------|:----------|:----------------------------------------------------|:------------------|
| video_id           | String    | Unique YouTube identifier for the video.            | Primary Key       |
| title              | String    | The title of the video.                             |                   |
| description        | Text      | Full text of the video description.                 |                   |
| channel_id         | String    | Unique ID for the YouTube channel.                  |                   |
| published_at       | DateTime  | Original upload date/time.                          | Default: UTC      |
| keyword_matched    | String    | Search term that triggered the discovery.           |                   |
| first_seen_at      | DateTime  | Timestamp when record was added to local DB.        | Default: UTC      |
| comments_disabled  | Boolean   | Flag for videos with locked comment sections.       | Default: False    |

## 2. Table: Comments
This table contains individual comments from accounts linked to each specific video.

| Variable Name      | Data Type | Description                                         | Attributes        |
|:-------------------|:----------|:----------------------------------------------------|:------------------|
| comment_id         | String    | Unique YouTube identifier for the comment.          | Primary Key       |
| video_id           | String    | Reference to the parent video.                      | Foreign Key       |
| parent_id          | String    | ID of parent comment (if this is a reply).          | Nullable          |
| author_hash        | String    | Anonymized author ID for ethical data handling.     |                   |
| text               | Text      | The raw text content of the comment.                |                   |
| published_at       | DateTime  | Original comment post date.                         | Default: UTC      |
| last_updated_at    | DateTime  | Date of last modification (if edited).              | Default: UTC      |

## 3. Table: CollectionState
This is an internal tracking table, just for my reference to keep track of when the collection happened, and is used by the script to make sure it doesn't pull the same comment twice.

| Variable Name      | Data Type | Description                                         | Attributes        |
|:-------------------|:----------|:----------------------------------------------------|:------------------|
| keyword            | String    | The specific keyword being tracked.                 | Primary Key       |
| last_search_time   | DateTime  | Timestamp of the last successful API crawl.         |                   |

---