import requests
import configparser
from flask import Flask, render_template, request


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api"]


def get_weather_results(city, api_key):
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    r = requests.get(api_url)
    return r.json()


API_KEY = get_api_key()


app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def render_results():
    # getting the 'city' because we `named` it 'city'
    city = request.form["city"]

    data = get_weather_results(city, API_KEY)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather_desc = data["weather"][0]["main"]
    location = data["name"]

    return render_template(
        "results.html",
        location=location,
        temp=temp,
        feels_like=feels_like,
        weather_desc=weather_desc,
    )


# this runs our app only once
if __name__ == "__main__":
    app.run()


# get_weather_results("Sydney", API_KEY)
# print(get_weather_results("Sydney", API_KEY))
