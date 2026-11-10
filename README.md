# Väderapp

Webbapp i Flask som visar nuvarande väder och en prognos för tre dagar för fem svenska städer:
Stockholm, Göteborg, Malmö, Umeå och Kiruna. Väderdata hämtas från Open-Meteo.

## Funktioner
- Startsida med rullgardinslista över de fem städerna och en knapp.
- Prognossida som visar stadens namn, nuvarande temperatur och vind, samt en tabell med datum,
  högsta och lägsta temperatur och nederbörd för tre dagar.
- Eget Jinja-filter som visar temperaturer som `8,2 °C`.
- Felhantering: ogiltig stad ger HTTP 400, API-fel ger HTTP 502 och okänd adress ger en egen 404-sida.
  Appen kraschar inte, utan visar ett felmeddelande.

## Teknik
- Python och Flask (routes, `request.args`, `url_for`, felhanterare för 404)
- Jinja2 (bas-mall med block, `for`, `if` och eget filter)
- requests (timeout, `raise_for_status()` och eget fel `VaderError`)
- pytest (parametrize, fixture, mockning med `unittest.mock`)
- ruff (kodkvalitet och formatering)
- Git och GitHub

## Projektstruktur
```
vaderapp/
├── app.py                    # routes och felhantering
├── application/
│   ├── stader.py             # de fem städerna och finns_stad()
│   ├── vader_api.py          # API-anropet och VaderError
│   └── tolka.py              # gör om API-svaret till en lista med dagar
├── templates/
│   ├── base.html             # gemensam bas-mall
│   ├── index.html            # startsidan
│   ├── prognos.html          # prognossidan
│   └── fel.html              # felsidan (400, 404, 502)
├── tests/
│   ├── test_stader.py
│   ├── test_vader_api.py
│   ├── test_tolka.py
│   └── test_app.py
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

## Installation
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Köra appen
```powershell
flask --app app run --debug
```
Öppna http://127.0.0.1:5000 och välj en stad. Internetanslutning krävs för att hämta väderdata.

## Köra testerna
```powershell
python -m pytest
```
Testerna körs utan nätverk, eftersom alla anrop mot API:et mockas. De täcker:
- stadskontroll (`finns_stad`, parametrize)
- API-modulen: lyckat svar, timeout och HTTP-fel
- tolkningen av API-svaret (`tolka`, parametrize)
- routes med Flasks testklient: ogiltig stad (400), okänd adress (404), lyckad prognos (200) och API-fel (502)

## Kodkvalitet
```powershell
ruff check .
ruff format .
```

## Testdriven utveckling
Testet skrevs och committades före funktionen för `finns_stad` och `tolka`, vilket syns i Git-historiken.

## Felhantering
| Situation | Svar |
|---|---|
| Stad saknas eller är ogiltig | HTTP 400 och en felsida |
| Open-Meteo svarar inte, timeout eller HTTP-fel | HTTP 502 och en felsida |
| Adressen finns inte | HTTP 404 och en egen felsida |

## Källa
Väderdata från [Open-Meteo](https://open-meteo.com/), licens CC BY 4.0.

## Frågor

### 1. Varför mockar du anropen mot API i dina tester, och vad skulle hända om du inte gjorde det?
I mina tester mockar jag API-anropen för att kunna testa applikationen utan att behöva kontakta det riktiga API eller vara beroende av internetuppkoppling. Utan mockning skulle testerna kunna misslyckas på grund av nätverksproblem eller om API inte fungerar, även om min egen kod är korrekt. Jag kan också simulera olika fel, exempelvis timeout, för att kontrollera hur applikationen hanterar dem.

### 2. Vad gör `timeout` och `raise_for_status()`, och varför behövs de?
I `application/vader_api.py` använder jag `timeout=5` i `requests.get()` för att förhindra att applikationen väntar hur länge som helst på ett svar från API. Jag använder också `svar.raise_for_status()` för att upptäcka HTTP-fel, exempelvis 404 eller 500, genom att skapa ett undantag (exception). På så sätt kan applikationen hantera felaktiga API-svar istället för att försöka arbeta vidare med dem.

### 3. Hur fungerar mallarv i Jinja2?
I mitt projekt använder jag mallarv i Jinja2 för att återanvända samma grundstruktur på flera sidor och slippa upprepa HTML-kod. I `prognos.html` använder jag `{% extends "base.html" %}` för att ärva grundmallen och fyller sedan blocket `content` med sidans eget innehåll. Det gör det enklare att ändra den gemensamma layouten utan att behöva uppdatera varje sida separat.

### 4. Vad är en fixture, och vilken använder du?
En fixture i pytest används för att återanvända kod och förberedelser i flera tester. I mitt projekt har jag en fixture som heter `klient` och som använder `app.test_client()` för att skapa en testklient till min Flask-applikation. Den gör det möjligt att simulera HTTP-anrop i testerna utan att behöva starta en riktig server. Jag kan sedan använda samma fixture i flera tester istället för att upprepa samma kod.
