import os
import requests
import investpy
import pandas as pd
import json


def crypto_calendar():
    url = "https://developers.coinmarketcal.com/v1/events"
    querystring = {"max":"100"}
    payload = ""
    headers = {
        'x-api-key': "8kn6nhe3Dw8bkt0NnQx5p52ImfmUwjcm8g9GMlO8",
        'Accept-Encoding': "deflate, gzip",
        'Accept': "application/json"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    df = pd.DataFrame(json.loads(response.text)['body'])

    return



    # Get Token
    # client_secret = os.environ.get('COINMARKETCAL_SECRET')
    # print(client_secret)
    # coinmarketcal = Coinmarketcal(client_id, client_secret)
    # events = coinmarketcal.get_events(page=None, max=None,
    #                          dateRangeStart=None, dateRangeEnd=None, coins=None,
    #                          categories=None, sortBy=None, showOnly=None)
    # return events


def econ_calendar():
    file = 'calendar.files'
    refresh_rate = 86400

    if file in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(file) < refresh_rate:
        calendar = pd.read_csv(file, index_col=0)
    else:
        calendar = investpy.economic_calendar()
        calendar.to_csv(file)

    return calendar



def tech_calendar():
    pass