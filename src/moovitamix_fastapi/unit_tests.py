import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from fetch_data import api_request, save_to_file, run_pipeline, OUTPUT_DIR


class TestDataPipeline(unittest.TestCase):

    @patch("requests.get")
    def test_api_request_success(self, mock_get):
        """This method tests if API request return data correctly"""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result = api_request("tracks")

        # Assert
        self.assertEqual(result, {"key": "value"})
        mock_get.assert_called_once_with("http://127.0.0.1:8000/tracks")

    @patch("requests.get")
    def test_api_request_failure(self, mock_get):
        """This method tests if API request handle the error"""
        # Arrange
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # Act
        result = api_request("tracks")

        # Assert
        self.assertIsNone(result)
        mock_get.assert_called_once_with("http://127.0.0.1:8000/tracks")

    @patch("builtins.open", new_callable=MagicMock)
    @patch("os.makedirs")
    def test_save_to_file(self, mock_makedirs, mock_open):
        """This method tests if the data saving works as intended"""
        # Arrange
        mock_makedirs.return_value = None
        data = {"key": "value"}
        endpoint = "tracks"

        # Act
        save_to_file(endpoint, data)

        # Assert
        file_path = os.path.join(OUTPUT_DIR, f"{endpoint}.json")
        mock_open.assert_called_once_with(file_path, "w")

    @patch("fetch_data.process_endpoint")
    @patch("fetch_data.run_pipeline")
    def test_run_pipeline(self, _, mock_process_endpoint):
        # Arrange
        mock_process_endpoint.return_value = None

        # Act
        run_pipeline()

        # Assert
        mock_process_endpoint.assert_called()
        self.assertEqual(mock_process_endpoint.call_count, 3)


if __name__ == "__main__":
    unittest.main()
