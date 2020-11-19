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

    def fetch_site_data(self):
        try:
            user_agent = app_settings.WEB_SCRAPE_USER_AGENT
            headers = {"user-agent": user_agent}
            max_redirects = int(app_settings.SITE_URL_MAX_REDIRECTS)

            # get the company details json
            company_json = None
            with open(app_settings.COMPANY_SITE_DETAILS_JSON_FILE) as f:
                company_json = json.load(f)

            # get the keywords json
            keyword_json = None
            with open(app_settings.PROMOTION_KEY_WORDS_JSON_FILE) as pkf:
                keyword_json = json.load(pkf)

            main_list = []
            prop_match_list = []
            keyword_list = []
            description_list = []
            coupon_code_list = []
            terms_data_list = []
            exp_data_list = []
            sample_list = []

            empty_obj = {"comp_id": "", "site_name": "", "host": "", "url": "",
                         "text_type": "", "html_element": "",
                         "html_text": ""}

            company_json = [company_json[0]]

            loop_ref = ""

            for c in range(len(company_json)):
                try:
                    com_obj = company_json[c]
                    print(com_obj)
                    site_urls = com_obj.get('site_url')
                    comp_id = com_obj.get('site_no')
                    site_name = com_obj.get('site_name')
                    site_host = com_obj.get('site_host')
                    target_elem = com_obj.get('web_scrape_key_elements')
                    df = None

                    for i in range(len(target_elem)):
                        target_elem_obj = target_elem[i]
                        site_url = target_elem_obj.get('site_url')
                        print(f"{c}:{site_url}")
                        scrape_filters = target_elem_obj.get('scrape_filters')

                        # extract the html content from URL
                        session_ini = requests.Session()
                        session_ini.max_redirects = max_redirects
                        session_ini.headers['User-Agent'] = user_agent
                        req = session_ini.get(site_url)
                        # req = requests.get(site_url, headers=headers)
                        print(f"{c}:{req.text}")
                        soup = BeautifulSoup(req.text, "html.parser")

                        for sf in range(len(scrape_filters)):
                            prop_attr_text_type = scrape_filters[sf].get('text_type')
                            prop_filter_list = scrape_filters[sf].get('property_filter')
                            keyword_list = keyword_json[prop_attr_text_type].get('keyword_list')

                            for j in range(len(prop_filter_list)):
                                try:
                                    loop_ref = f"company_counter:{c},main_loop_counter:{i},sub_loop_counter:{j}"
                                    print(loop_ref)
                                    prop_obj = prop_filter_list[j]
                                    parent_node = prop_obj.get('parent_node')
                                    parent_tag = parent_node.get('tag_name')
                                    parent_attr = {parent_node.get('prop'): parent_node.get('search_key')}
                                    prop_attr_sub_list = prop_obj.get('prop_list')
                                    attr_search_key_list = [{obj.get('prop'): obj.get('search_key')} for obj in
                                                            prop_attr_sub_list]
                                    tag_name_list = [obj.get('tag_name') for obj in
                                                     prop_attr_sub_list]
                                    print(f"prop_obj:{prop_obj}")

                                    # get all elements from parent node
                                    ele_list = soup.find(parent_tag, attrs=parent_attr)

                                    if ele_list is not None:
                                        children = ele_list.findChild("div", attrs=parent_attr, recursive=False)
                                        for child in children:
                                            sample_list.append(child)
                                        # for el in range(len(ele_list)):
                                        # print(ele_list[el])
                                        """
                                        for attr_key in range(len(attr_search_key_list)):
                                            attr_prop = attr_search_key_list[attr_key]
                                            html_prop = tag_name_list[attr_key]

                                            if prop_attr_text_type == "description":
                                                description = ele_list[el].find(html_prop, attr_prop)
                                                if description is not None:
                                                    [description_list.append(
                                                    description and self.is_keyword_found(keyword_list,
                                                                                          description.text) if description.text else "")]
                                            elif prop_attr_text_type == "code":
                                                code = ele_list[el].find(html_prop, attr_prop)
                                                if code is not None:
                                                    [coupon_code_list.append(code and self.is_keyword_found(keyword_list,
                                                                                                        code.text) if code.text else "")]
                                            elif prop_attr_text_type == "terms":
                                                terms = ele_list[el].find(html_prop, attr_prop)
                                                if terms is not None:
                                                    [terms_data_list.append(terms and self.is_keyword_found(keyword_list,
                                                                                                        terms.text) if terms.text else "")]
                                            elif prop_attr_text_type == "expiry":
                                                exp_data = ele_list[el].find(html_prop, attr_prop)
                                                if exp_data is not None:
                                                    [exp_data_list.append(self.is_keyword_found(keyword_list,
                                                                                                exp_data.text) if exp_data.text else "")]

                                            # price = ele_list[el].find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
                                    """
                                    """"
                                    for m in range(len(attr_search_key_list)):
                                        attr_search_key = attr_search_key_list[m]
                                        ele_list = soup.find_all(tag_name, attrs=attr_search_key)
                                        # soup.find_all("a", href=lambda href: href and "location" in href)
                                        # soup.find_all('a', href=True, attrs={'class': '_31qSD5', '': ''}):
                                        [main_list.append(
                                            {"comp_id": comp_id, "site_name": site_name, "host": site_host,
                                             "url": site_url,
                                             "text_type": prop_attr_text_type, "html_element": str(el),
                                             "html_text": el.text} if self.is_keyword_found(keyword_list,
                                                                                            el.text) else empty_obj
                                        ) for el
                                            in ele_list]
                                    """

                                except Exception:
                                    msg = f'WebScrapeHandler=>fetch_site_data()=>prop_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                                    print(msg)
                                    logger.error(msg)
                except Exception:
                    msg = f'WebScrapeHandler=>fetch_site_data()=>company_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    print(msg)
                    logger.error(msg)
            print(f"sample_list:{sample_list},no_of_items:{len(sample_list)}")
            # filtered_list = [obj for obj in main_list if (obj.get('comp_id') != "" and obj.get('html_text') != "")]
            return description_list, coupon_code_list, terms_data_list, exp_data_list  # filtered_list
        except Exception:
            msg = f'WebScrapeHandler=>fetch_site_data()=>before_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def is_keyword_found(self, keyword_list, element_text):
        try:
            match_counter: int = 0
            element_text = element_text.lower()
            for i in range(len(keyword_list)):
                key_val = keyword_list[i]
                if key_val in element_text:
                    match_counter = match_counter + 1
            return match_counter > 0
        except Exception:
            msg = f'WebScrapeHandler=>is_keyword_found()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def send_promotion_data(self):
        description_list, coupon_code_list, terms_data_list, exp_data_list = self.fetch_site_data()
        print(f"description_list:{description_list}")
        print("\n")
        print(f"coupon_code_list:{coupon_code_list}")
        print("\n")
        print(f"terms_data_list:{terms_data_list}")
        print("\n")
        print(f"exp_data_list:{exp_data_list}")
        print("\n")
        return "success"
