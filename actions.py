from typing import Any, Text, Dict, List

import rasa
import wikipedia
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
from urllib.request import urlopen
import json
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Task #1: запит поточного курсу валют

# intent: currency_rate (was added into nlu.yml file)
# action: utter_currency_rate (was added into domain.yml)
# Additionally: the action itself was used in stories.yml (so we could train our model).

class CurrentCurrencyRate(Action):

    def name(self) -> Text:
        # Note: To connect our Python code and connect to the stories.yml file, where this data would be implemented,
        # we need to define each function (mentioned below) in our actions.py file.
        # Here are all the actions used in domain.yml file:

        # - action_current_currency_rate
        # - action_currency_rate_change
        # - action_highest_currencies
        # - action_currencies_comparison
        return "action_current_currency_rate"

    def run(self, currency):
        API = pd.read_json(f'https://api.currencyfreaks.com/v2.0/rates/latest?apikey=aee02ebb05de41ba9aa96b0af3c55def&symbols={currency}')
        return 'Current currency rate is the following ==>', API[['base', 'rates']].to_string(index=True, header=False)


# Task #2: запит змін курсу валют за певний період

# intent: currency_rate_change (was added into nlu.yml file)
# action: utter_currency_rate_change (was added into domain.yml)


class CurrencyChange(Action):

    def name(self) -> Text:
        return "action_currency_rate_change"

    def run(self, start, end, currency):
        df = pd.read_json(
            f"https://fxmarketapi.com/apipandas?api_key=WwPlOaZJ_P4xukRGUYnk&currency={currency}&start_date={start}&end_date={end}")
        return f"Current currency rate for {currency} is the following", df


# Task 3: запит про найбільш популярну валюту

# intent: highest_currencies (was added into nlu.yml file)
# action: utter_highest_currencies (was added into domain.yml)

class MostTradedCurrencies(Action):
    def name(self) -> Text:
        return "action_highest_currencies"

    def run(self):

        # the file with data taken from Wiki is in additional data folder
        wikiurl = 'https://en.wikipedia.org/wiki/Currency'
        table_class = "wikitable sortable jquery-tablesorter"
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')
        indiatable = soup.find('table', {'class': "wikitable"})
        #
        df = pd.read_html(str(indiatable))
        # convert list to dataframe
        df = pd.DataFrame(df[0])
        return "Top highest currencies are\n", df['Currency'][:10]


# Task 4: запит на порівняння курсу деяких валют

# intent: currencies_comparison (was added into nlu.yml file)
# action: utter_currencies_comparison (was added into domain.yml)

class CurrenciesComparison(Action):
    def name(self) -> Text:
        return "action_currencies_comparison"

    def run(self, start, end, currencies):
        df = pd.read_json(
            f"https://fxmarketapi.com/apipandas?api_key=WwPlOaZJ_P4xukRGUYnk&currency={currencies}&start_date={start}&end_date={end}")
        return 'The result is as follows', df


if __name__ == "__main__":

    # Task 1
    currency_rate = CurrentCurrencyRate()
    print(currency_rate.run(input('Enter currencies (in format: USD,EUR,UAH): ')))

    # Task 2
    currency_change = CurrencyChange()
    print(currency_change.run(input('Enter start date (in format yyyy-mm-dd): '),
                              input('Enter end date (in format yyyy-mm-dd): '),
                              input('Enter currency: ')))

    # Task 3
    most_least = MostTradedCurrencies()
    print(most_least.run())

    # Task 4
    cur_comp = CurrenciesComparison()
    print(cur_comp.run(input('Enter start date (in format yyyy-mm-dd): '),
                       input('Enter end date (in format yyyy-mm-dd): '),
                       input('Enter currencies to compare: ')))








