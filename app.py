from flask import Flask, render_template, request

from application.stader import STADER, finns_stad
from application.tolka import tolka
from application.vader_api import VaderError, hamta_vader

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", STADER=STADER)


@app.route("/prognos")
def prognos():
    stad = request.args.get("stad", "")
    if not finns_stad(stad):
        return render_template("fel.html", fel="Ogiltig stad"), 400
    stad = stad.capitalize()
    lat, lon = STADER[stad]
    try:
        vader = hamta_vader(lat, lon)
    except VaderError:
        return render_template(
            "fel.html", fel="vädret kunde inte hämtas från Open-Meteo."
        ), 502
    vind = vader["current"]["wind_speed_10m"]
    temp = vader["current"]["temperature_2m"]
    dagar = tolka(vader)
    return render_template("prognos.html", stad=stad, temp=temp, vind=vind, dagar=dagar)


@app.template_filter("omvandling")
def omvandling(tal):
    omv_tal = str(tal).replace(".", ",")
    return f"{omv_tal} °C"


if __name__ == "__main__":
    app.run(debug=True)
