from unittest.mock import Mock, patch

import pytest
import requests

from application.vader_api import VaderError, hamta_vader

DATA = {
    "temperature_2m": 10,
    "wind_speed_10m": 5,
    "temperature_2m_max": 2,
    "temperature_2m_min": 1,
    "precipitation_sum": 0.5,
}


@patch("application.vader_api.requests.get")
def test_hamta_vader_success(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: DATA)
    resultat = hamta_vader("59.33", "18.07")
    assert resultat == DATA


@patch("application.vader_api.requests.get", side_effect=requests.Timeout())
def test_timeout(mock_get):
    with pytest.raises(VaderError):
        hamta_vader("59.33", "18.07")


@patch("application.vader_api.requests.get")
def test_http_fel(mock_get):
    svar = Mock()
    svar.raise_for_status.side_effect = requests.HTTPError()
    mock_get.return_value = svar
    with pytest.raises(VaderError):
        hamta_vader("59.33", "18.07")
