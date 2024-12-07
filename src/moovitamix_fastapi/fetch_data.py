import requests
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import logging

# === Configuration ===
API_BASE_URL = "http://127.0.0.1:8000"
OUTPUT_DIR = "data"
ENDPOINTS = ["tracks", "users", "listen_history"]
LOG_FILE = "data_pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)


# === Utility Functions ===
def api_request(endpoint):
    """This method sends a GET request to the desired API endpoint."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        logging.info(f"Making request to {url}")
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Data successfully fetched from {endpoint}")
        return response.json()
    except requests.exceptions.RequestException as error:
        logging.error(f"Error while fetching data from {endpoint}: {error}")
        return None


def save_to_file(endpoint, content):
    """This method writes JSON data to a file named after the endpoint."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"{endpoint}.json")

    try:
        with open(file_path, "w") as file:
            json.dump(content, file, indent=4)
            logging.info(f"Data saved to {file_path}")
    except IOError as error:
        logging.error(f"Error while saving data to {file_path}: {error}")


# === Core Pipeline ===
def process_endpoint(endpoint):
    """This method fetches and saves data for a single API endpoint."""
    data = api_request(endpoint)
    if data is not None:
        save_to_file(endpoint, data)


def run_pipeline():
    """This method runs the data fetch pipeline for all endpoints."""
    logging.info("Starting data fetch pipeline...")
    for endpoint in ENDPOINTS:
        logging.info(f"Processing endpoint: {endpoint}")
        process_endpoint(endpoint)
    logging.info("Data retrieval completed successfully!")


# === Scheduling ===
if __name__ == "__main__":
    logging.info("Initializing the scheduler...")
    scheduler = BackgroundScheduler()
    # Scheduled daily
    scheduler.add_job(run_pipeline, "interval", seconds=10)
    scheduler.start()

    logging.info("Scheduler running...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.shutdown()
        logging.info("Scheduler stopped")
