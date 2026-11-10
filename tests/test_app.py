import pytest
from app import app
from unittest.mock import Mock, patch
import requests

TESTDATA = {
    "current": {"temperature_2m": 5.5, "wind_speed_10m": 3.2},
    "daily": {
        "time": ["2026-11-10", "2026-11-11", "2026-11-12"],
        "temperature_2m_max": [5.9, 5.9, 5.5],
        "temperature_2m_min": [4.4, 4.3, 1.9],
        "precipitation_sum": [0.50, 3.20, 3.40],
    },
}


@pytest.fixture
def klient():
    app.config["TESTING"] = True
    return app.test_client()


def test_ogiltig_adress(klient):
    svar = klient.get("/finns-inte")
    assert svar.status_code == 404


def test_ogiltig_stad(klient):
    svar = klient.get("/prognos?stad=ankeborg")
    assert svar.status_code == 400


@patch("application.vader_api.requests.get")
def test_prognos(mock_get, klient):
    mock_get.return_value = Mock(status_code=200, json=lambda: TESTDATA)
    svar = klient.get("/prognos?stad=Stockholm")
    assert svar.status_code == 200
    assert "Stockholm" in svar.get_data(as_text=True)


@patch("application.vader_api.requests.get", side_effect=requests.Timeout)
def test_timeout(mock_get, klient):
    assert klient.get("/prognos?stad=Stockholm").status_code == 502
