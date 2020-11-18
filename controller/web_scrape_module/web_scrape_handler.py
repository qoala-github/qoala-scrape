from bs4 import BeautifulSoup
import requests
import re
import json


class WebScrapeHandler:
    URL = "https://www.nike.com/promo-code"

    def check_price(self) -> int:
        # get HTML page
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        headers = {"user-agent": user_agent}
        req = requests.get(self.URL, headers=headers)

        # get price
        soup = BeautifulSoup(req.text, "html.parser")
        span_list = soup.find_all("a", href=re.compile("discount"))  # soup.find_all("a", href=lambda href: href and "location" in href) # <span id="priceblock_ourprice">...</span>
        txt_list = [i.text for i in span_list]
        return txt_list
        # price = span.text   # XY,ZW €
