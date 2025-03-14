import os
import requests
import zipfile
import io

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

def main():
    # Ensure the folders exist
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(extract_path, exist_ok=True)

    print(f"Downloading and extracting files into: {extract_path}")

    for url in download_uris:
        filename = os.path.basename(url)  # Extract filename from URL
        zip_file_path = os.path.join(download_path, filename)

        # Download the file
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(zip_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {zip_file_path}")

            # Extract the ZIP file
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Extracted: {filename} to {extract_path}")

            # Optionally delete the ZIP file after extraction
            os.remove(zip_file_path)

        else:
            print(f"Failed to download {url}. HTTP Status: {response.status_code}")

if __name__ == "__main__":
    main()
