import requests

URL = "https://api.open-meteo.com/v1/forecast"


class VaderError(Exception):
    """Anpassad undantagsklass för väderrelaterade fel."""


def hamta_vader(lat, lon):
    """Hämtar väderdata från OpenMeteo API för en given latitud och longitud."""
    try:
        svar = requests.get(
            URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto",
                "forecast_days": 3,
            },
            timeout=5,
        )
        svar.raise_for_status()
        return svar.json()
    except requests.exceptions.RequestException as e:
        raise VaderError(f"Fel vid hämtning av väderdata: {e}") from e
