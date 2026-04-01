#!/usr/bin/env python3
"""
Data Streamer - Simulates sensor data ingestion for live dashboard
Continuously reads RW classification data and sends it to the backend API
"""
import time
import requests
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataStreamer:
    def __init__(self, api_url="http://localhost:9090", data_file="data/rw_classification_data.csv"):
        self.api_url = api_url
        self.data_file = Path(__file__).parent / data_file
        self.current_index = 0
        self.load_data()

    def load_data(self):
        """Load the RW classification data"""
        try:
            self.data = pd.read_csv(self.data_file)
            logger.info(f"Loaded {len(self.data)} sensor readings from {self.data_file}")
        except Exception as e:
            logger.error(f"Failed to load data file: {e}")
            raise

    def get_next_reading(self):
        """Get the next sensor reading in loop"""
        if self.current_index >= len(self.data):
            self.current_index = 0
            logger.info("Restarting data loop")

        row = self.data.iloc[self.current_index]
        self.current_index += 1

        # Extract RW metrics (excluding Water_Status column)
        rw_metrics = {
            "RW pH": float(row["RW pH"]),
            "RW Tur": float(row["RW Tur"]),
            "RW Colour": float(row["RW Colour"]),
            "RW TDS": float(row["RW TDS"]),
            "RW Iron": float(row["RW Iron"]),
            "RW Hardness": float(row["RW Hardness"]),
            "RW S Solids": float(row["RW S Solids"]),
            "RW Aluminium": float(row["RW Aluminium"]),
            "RW Chloride": float(row["RW Chloride"]),
            "RW Manganese": float(row["RW Manganese"]),
            "RW Conductivity": float(row["RW Conductivity"]),
            "RW Calcium": float(row["RW Calcium"]),
            "RW Magnesium": float(row["RW Magnesium"]),
            "RW Alkalinity": float(row["RW Alkalinity"]),
            "RW Ammonia as N": float(row["RW Ammonia as N"])
        }

        return rw_metrics

    def send_to_backend(self, sensor_data):
        """Send sensor data to backend API"""
        try:
            # Use the analyze endpoint to process the sensor data
            response = requests.post(
                f"{self.api_url}/api/v1/analyze",
                json=sensor_data,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                classification = result["classification"]
                status = "SAFE" if classification["status_code"] == 1 else "TOXIC"
                logger.info(f"Sent reading {self.current_index}: {status} "
                          f"(Safe: {classification['confidence_safe_percent']:.1f}%, "
                          f"Toxic: {classification['confidence_toxic_percent']:.1f}%)")
                return True
            else:
                logger.error(f"Backend returned status {response.status_code}: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send data to backend: {e}")
            return False

    def run(self, interval_seconds=60):
        """Run the data streamer continuously"""
        logger.info(f"Starting data streamer - sending data every {interval_seconds} seconds")
        logger.info(f"API URL: {self.api_url}")

        while True:
            try:
                # Get next sensor reading
                sensor_data = self.get_next_reading()

                # Send to backend
                success = self.send_to_backend(sensor_data)

                if success:
                    logger.info(f"Data sent successfully at {datetime.now().strftime('%H:%M:%S')}")
                else:
                    logger.warning("Failed to send data, will retry next cycle")

                # Wait for next reading
                time.sleep(interval_seconds)

            except KeyboardInterrupt:
                logger.info("Data streamer stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(5)  # Brief pause before retrying

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Water Quality Data Streamer")
    parser.add_argument("--api-url", default="http://localhost:9090",
                       help="Backend API URL (default: http://localhost:9090)")
    parser.add_argument("--data-file", default="data/rw_classification_data.csv",
                       help="Path to sensor data file")
    parser.add_argument("--interval", type=int, default=60,
                       help="Interval between readings in seconds (default: 60)")

    args = parser.parse_args()

    streamer = DataStreamer(api_url=args.api_url, data_file=args.data_file)
    streamer.run(interval_seconds=args.interval)

if __name__ == "__main__":
    main()