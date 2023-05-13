# crawling 위한 request, bs4 import
import requests
from bs4 import BeautifulSoup as bs

# 민감한 정보를 가리기 위해 .env 활용
import os
from dotenv import load_dotenv

from firebase import Firebase
from datetime import datetime
import schedule
import time

class Crawling():
    def __init__(self):
        load_dotenv(verbose=True)
        self._elec_url = os.getenv("ELEC_RATE_PAGE")
        self._gas_url = os.getenv("GAS_RATE_PAGE")

        self._gas_key = os.getenv("GAS_KEY")
        self._gas_value = os.getenv("GAS_VALUE")

        self._elec_range_other = ['200', '400', 'avobe']
        self._elec_range_summer = ['300', '450', 'avobe']

    def getElecRate(self):
        res = requests.get(self._elec_url)
        if res.status_code == 200:
            ret_data = {}
            m = int(datetime.today().strftime('%m'))

            soup = bs(res.text, 'html.parser')
            td = soup.select("div.clause_box > div.conSection > div.scbox > div:nth-child(5) > table > tbody > tr")[:3]

            for idx, data in enumerate(td):
                data = [ float(txt.text.replace(",", "")) for txt in data.select("td")[2:] ]
                data = {
                    'base': data[0],
                    'rate': data[1]
                }

                if m == 7 or m == 8:
                    ret_data[self._elec_range_summer[idx]] = data
                else:
                    ret_data[self._elec_range_other[idx]] = data
            
            return ret_data
        return -1

    def getGasRate(self):
        res = requests.post(self._gas_url, data={self._gas_key:self._gas_value})
        if res.status_code == 200:
            gas_rate = res.json()[0]['H_COOK'].split('|')[1].replace(" ", "")
            gas_rate = round(float(gas_rate))
            
            return gas_rate

        return -1


def __appendRating():
    global crawling
    global database

    d = datetime.today().strftime('%y-%m-%d-%H')

    data = {
        'gas': crawling.getGasRate(),
        'elec': crawling.getElecRate()
    }
    print(data)

    database.setRating(data, d)

if __name__ == "__main__":
    crawling = Crawling()
    database = Firebase()

    schedule.every(1).hours.do(__appendRating)

    # schedule.every().day.at("00:00").do(__appendRating)

    while True:
        schedule.run_pending()
        time.sleep(1)