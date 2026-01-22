import logging
from datetime import datetime
from discovery import search_new_videos
from collector import collect_comments

# Setting up Logging
# Stores logs in a file for documentation
logging.basicConfig(
    filename='collection_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("--- Starting Daily Automated Collection ---")
    
    try:
        # Phase 2: Discovery
        logging.info("Phase 2: Starting Video Discovery...")
        # Note to self: Each 'search.list' call costs 100 quota units
        search_new_videos()
        logging.info("Phase 2 Complete.")

        # Phase 3: Collection
        logging.info("Phase 3: Starting Comment Collection...")
        # Note to self: Each 'commentThreads.list' call costs 1 unit
        collect_comments()
        logging.info("Phase 3 Complete.")

        logging.info("--- Collection Run Successful ---")
        print("Pipeline executed successfully. Check collection_log.txt for details.")

    except Exception as e:
        logging.error(f"Critical error during pipeline execution: {e}")
        print(f"Pipeline failed. Error logged: {e}")

if __name__ == "__main__":
    run_pipeline()