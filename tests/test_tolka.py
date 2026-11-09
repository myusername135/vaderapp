import pytest

from application.tolka import tolka


@pytest.mark.parametrize(
    "indata, forvantat",
    [
        (
            {
                "daily": {
                    "time": ["2026-11-08"],
                    "temperature_2m_max": [3.7],
                    "temperature_2m_min": [1.5],
                    "precipitation_sum": [0.0],
                }
            },
            [
                {
                    "datum": "2026-11-08",
                    "max": 3.7,
                    "min": 1.5,
                    "nederbord": 0.0,
                }
            ],
        ),
    ],
)
def test_tolka(indata, forvantat):
    assert tolka(indata) == forvantat
