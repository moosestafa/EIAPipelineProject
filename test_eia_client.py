from unittest.mock import patch, MagicMock
import pytest
from pipeline.eia_client import fetch_data
from requests.exceptions import HTTPError
def test_fetch_data_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": {"data": []}}
    
    with patch("pipeline.eia_client.requests.get", return_value=mock_response):
        result = fetch_data("TX", "2024-01", "2024-01")
    
    assert result == {"response": {"data": []}}

def test_fetch_data_fail():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError()
    with patch("pipeline.eia_client.requests.get", return_value=mock_response):
        with pytest.raises(HTTPError):
            fetch_data("TX", "2024-01", "2024-01")

