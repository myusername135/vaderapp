import requests

URL = "https://api.open-meteo.com/v1/forecast"

# {"latitude":59.3289,"longitude":18.072357,"generationtime_ms":0.08058547973632812,"utc_offset_seconds":3600,"timezone":"Europe/Stockholm","timezone_abbreviation":"GMT+1","elevation":18.0,"current_units":{"time":"iso8601","interval":"seconds","temperature_2m":"°C","wind_speed_10m":"km/h"},"current":{"time":"2026-11-08T20:45","interval":900,"temperature_2m":3.5,"wind_speed_10m":12.6},"daily_units":{"time":"iso8601","temperature_2m_max":"°C","temperature_2m_min":"°C","precipitation_sum":"mm"},"daily":{"time":["2026-11-08","2026-11-09","2026-11-10"],"temperature_2m_max":[3.7,4.6,5.4],"temperature_2m_min":[1.5,3.5,3.7],"precipitation_sum":[0.00,0.00,0.20]}}


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
