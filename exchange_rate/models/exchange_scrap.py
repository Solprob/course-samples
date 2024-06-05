import re

import requests
from bs4 import BeautifulSoup
from odoo import fields, models, api
from fake_useragent import UserAgent


def scrap_exchange_rates(url):
    ua = UserAgent()
    header = {"User-Agent": str(ua.chrome)}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", attrs={})
        elements_name = table.find_all("td", attrs={"class": "name-cell"})
        price_sale = table.find_all("span", attrs={"class": "price-text change-minus"})
        currencies = [currency.get_text(strip=True) for currency in elements_name]
        rates = [price.get_text(strip=True) for price in price_sale]
        return currencies, rates


def combine_currency_rates( currencies, rates):
    if len(currencies) * 2 != len(rates):
        raise ValueError("The number of rates must be twice the number of currencies")

    combined = []
    for i, currency in enumerate(currencies):
        rate_max = rates[i * 2]
        rate_min = rates[i * 2 + 1]
        combined.append(
            {"currency": currency, "rate-max": rate_max, "rate-min": rate_min}
        )
    return combined


def usd_value(data):
    for item in data:
        if item["currency"] == "1USD":
            return item["rate-max"]
    return None


def convert2float(text):
    try:
        number_str = re.findall(r"[0-9\.,]+", text)[0]
        numeric_value = float(number_str.replace(",", ""))
        return numeric_value
    except ValueError:
        print("Error: Could not convert value to float.")
        return 0.00


class ExchangeRate(models.AbstractModel):
    _name = "scraping.exchange.rate"
    _description = "Exchange Rate"

    def save_current_exchange_rate(self):
        cup = self.env["res.currency"].search([("name", "=", "CUP")], limit=1)

        url = "https://eltoque.com/tasas-de-cambio-de-moneda-en-cuba-hoy"
        exchanges = scrap_exchange_rates(url)
        combined_rates = combine_currency_rates(exchanges[0], exchanges[1])
        Exchange = self.env["res.currency.rate"]
        rate_usd = usd_value(combined_rates)  # return EX: '350.00CUP'
        usd_rate = Exchange.create(
            {
                "name": fields.Date.today(),
                "company_rate": convert2float(rate_usd),  # EX: 350.00
                "currency_id": cup.id,
            }
        )
        cup.rate_ids += usd_rate
