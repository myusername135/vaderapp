import pytest
from application.stader import finns_stad


@pytest.mark.parametrize(
    "stad, forvantat",
    [
        ("Stockholm", True),
        ("Göteborg", True),
        ("Malmö", True),
        ("Umeå", True),
        ("Kiruna", True),
        ("Norrköping", False),
        ("Linköping", False),
        ("", False),
        ("stockholm", True),
    ],
)
def test_finns_stad(stad, forvantat):
    assert finns_stad(stad) == forvantat
