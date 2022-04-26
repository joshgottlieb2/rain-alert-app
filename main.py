import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

twilio_trial_number = "+19106598330"
account_sid = "AC11058f42e13e80e7c981a7cfbe6e80b2"
auth_token = os.environ.get("AUTH_TOKEN")
api_key = os.environ.get("TWILIO_API_KEY")

parameters = {
    "appid": api_key,
    "lat": 42.291706,
    "lon": -85.587227,
    "exclude": "current,minutely,daily"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()    # prints the error if one exists
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Bring an umbrella!☂️",
        from_=twilio_trial_number,
        to="+17349726841"
    )
    print(message.status)



