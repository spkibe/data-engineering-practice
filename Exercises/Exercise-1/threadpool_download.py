import os
import requests
import zipfile
from concurrent.futures import ThreadPoolExecutor

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",  # Likely incorrect URL
]

download_path = "downloads"
extract_path = "extracted"

def download_file(url):
    """Downloads a file and extracts it."""
    filename = os.path.basename(url)
    zip_file_path = os.path.join(download_path, filename)

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"Failed to download {url}. HTTP Status: {response.status_code}")
            return

        # Save the file
        with open(zip_file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Downloaded: {zip_file_path}")

        # Extract the ZIP file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"Extracted: {filename} to {extract_path}")

        # Delete the ZIP file after extraction
        os.remove(zip_file_path)

    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(extract_path, exist_ok=True)

    # Use ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_file, download_uris)

if __name__ == "__main__":
    main()
