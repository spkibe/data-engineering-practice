import os
import aiohttp
import asyncio
import zipfile

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

async def download_file(session, url):
    """Downloads a file asynchronously using aiohttp."""
    filename = os.path.basename(url)
    zip_file_path = os.path.join(download_path, filename)

    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to download {url}. HTTP Status: {response.status}")
                return

            # Save the file
            with open(zip_file_path, "wb") as file:
                while chunk := await response.content.read(1024):
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

async def main():
    """Main async function to manage downloads."""
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(extract_path, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in download_uris]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
