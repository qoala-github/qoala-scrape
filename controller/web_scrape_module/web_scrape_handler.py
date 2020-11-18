import sys
import traceback

from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import logging

from app_configurations.app_settings import AppSetting

app_settings = AppSetting()
logger = logging.getLogger(__name__)


class WebScrapeHandler:
    URL = "https://www.nike.com/promo-code"

    def fetch_site_data(self):
        user_agent = app_settings.WEB_SCRAPE_USER_AGENT
        headers = {"user-agent": user_agent}
        # get the company details json
        company_json = None
        with open(app_settings.COMPANY_SITE_DETAILS_JSON_FILE) as f:
            company_json = json.load(f)

        products = []  # List to store name of the product
        prices = []  # List to store price of the product
        ratings = []  # List to store rating of the product
        main_list = []

        for c in range(len(company_json)):
            com_obj = company_json[c]
            print(com_obj)
            # get HTML page
            site_url = com_obj.get('site_url')[0]
            print(f"{c}:{site_url}")
            req = requests.get(site_url, headers=headers)
            print(f"{c}:{req.text}")
            soup = BeautifulSoup(req.text, "html.parser")

            target_elem = com_obj.get('web_scrape_key_elements')

            for i in range(len(target_elem)):
                target_elem_obj = target_elem[i]
                prop_filter_list = target_elem_obj.get('property_filter')

                for j in range(len(prop_filter_list)):
                    try:
                        loop_ref = f"company_counter:{c},main_loop_counter:{i},sub_loop_counter:{j}"
                        print(loop_ref)
                        prop_obj = prop_filter_list[j]
                        print(f"prop_obj:{prop_obj}")
                        # print(f"target_name:{target_elem_obj.get('tag_name')}")
                        prop_attr_list = prop_obj.get('prop_attribute')

                        for k in range(len(prop_attr_list)):
                            prop_attr_sub = prop_attr_list[k]
                            prop_attr_sub_list = prop_attr_sub.get('prop_list')
                            prop_attr_text_type = prop_attr_sub.get('text_type')
                            attr_search_key_list = [{obj.get('prop'): obj.get('search_key')} for obj in
                                                    prop_attr_sub_list]

                            for m in range(len(attr_search_key_list)):
                                attr_search_key = attr_search_key_list[m]
                                ele_list = soup.find_all(target_elem_obj.get('tag_name'), attrs=attr_search_key)
                                [main_list.append(
                                    {"text_type": str(prop_attr_text_type), "html_element": str(el), "html_text": str(el.text)}) for el
                                 in ele_list]

                    except Exception:
                        print(loop_ref)
                        logger.error(
                            f'WebScrapeHandler=>fetch_site_data()=>prop_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

            """
            for a in soup.find_all('a', href=True, attrs={'class': '_31qSD5', '': ''}):
                name = a.find('div', attrs={'class': '_3wU53n'})
                price = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
                rating = a.find('div', attrs={'class': 'hGSR34 _2beYZw'})
                products.append(name.text)
                prices.append(price.text)
                ratings.append(rating.text)
            df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})
            df.to_csv('products.csv', index=False, encoding='utf-8')
            """
        # get price
        """
        soup = BeautifulSoup(req.text, "html.parser")
        span_list = soup.find_all("a", href=re.compile(
            "discount"))  # soup.find_all("a", href=lambda href: href and "location" in href) # <span id="priceblock_ourprice">...</span>
        txt_list = [i.text for i in span_list]
        """
        return main_list
        # price = span.text   # XY,ZW €

    def send_promotion_data(self):
        return [""]
