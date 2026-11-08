STADER = {
    "Stockholm": ("59.33", "18.07"),
    "Göteborg": ("57.71", "11.97"),
    "Malmö": ("55.61", "13.00"),
    "Umeå": ("63.83", "20.26"),
    "Kiruna": ("67.86", "20.23"),
}


def finns_stad(stad):
    """Kontrollerar om staden finns i STADER."""
    stad = stad.capitalize()
    return stad in STADER
