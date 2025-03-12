import unittest
import os
import requests
from script import download_file  # Import from the script file

class TestFileDownload(unittest.TestCase):
    """Unit tests for file download and extraction."""

    def setUp(self):
        """Set up test environment."""
        self.test_url = "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip"
        self.test_path = "downloads"
        os.makedirs(self.test_path, exist_ok=True)

    def test_download_successful(self):
        """Test if a file is successfully downloaded."""
        filename = os.path.basename(self.test_url)
        file_path = os.path.join(self.test_path, filename)

        # Run download function
        download_file(self.test_url)

        # Check if file exists
        self.assertTrue(os.path.exists(file_path))

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_invalid_url(self):
        """Test downloading from an invalid URL."""
        invalid_url = "https://invalid-url.com/file.zip"
        with self.assertRaises(requests.exceptions.RequestException):
            download_file(invalid_url)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.test_path):
            os.rmdir(self.test_path)

if __name__ == "__main__":
    unittest.main()
