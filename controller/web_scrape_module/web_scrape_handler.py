import sys
import traceback
import requests
import re
import json
import pandas as pd
import logging

from bs4 import BeautifulSoup

from app_configurations.app_settings import AppSetting

app_settings = AppSetting()
logger = logging.getLogger(__name__)


class WebScrapeHandler:

    def fetch_site_data(self):
        loop_ref = ""
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
            site_coupon_list = []

            empty_obj = {"comp_id": "", "site_name": "", "host": "", "url": "",
                         "text_type": "", "html_element": "",
                         "html_text": ""}

            company_list = []
            data_count = 2  # len(company_json)
            for csl in range(data_count):
                company_list.append(company_json[csl])

            for c in range(len(company_list)):
                try:
                    com_obj = company_list[c]
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
                        site_coupon_list = []
                        print(f"{c}:{site_url}")
                        scrape_filters = target_elem_obj.get('scrape_filters')

                        # extract the html content from URL
                        session_ini = requests.Session()
                        session_ini.max_redirects = max_redirects
                        session_ini.headers['User-Agent'] = user_agent
                        req = session_ini.get(site_url)
                        # req = requests.get(site_url, headers=headers)
                        # print(f"{c}:{req.text}")
                        soup = BeautifulSoup(req.content, "html5lib")

                        for sf in range(len(scrape_filters)):
                            prop_filter_list = scrape_filters[sf].get('property_filter')

                            for j in range(len(prop_filter_list)):
                                try:
                                    loop_ref = f"company_counter:{c},main_loop_counter:{i},sub_loop_counter:{j}"
                                    print(loop_ref)
                                    prop_obj = prop_filter_list[j]
                                    parent_node = prop_obj.get('parent_node')
                                    parent_tag = parent_node.get('tag_name')
                                    parent_attr = {parent_node.get('prop'): parent_node.get('search_key')}
                                    prop_attr_sub_list = []
                                    prop_attr_sub_list = prop_obj.get('prop_list')

                                    # for description
                                    descr_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'description']
                                    descr_attr = {descr_obj[0].get('prop'): descr_obj[0].get('search_key')}
                                    descr_tag_name = descr_obj[0].get('tag_name')

                                    # for coupon code
                                    coupon_code_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'code']
                                    coupon_code_attr = {
                                        coupon_code_obj[0].get('prop'): coupon_code_obj[0].get('search_key')}
                                    coupon_code_tag_name = coupon_code_obj[0].get('tag_name')

                                    # for terms details
                                    terms_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'terms']
                                    terms_attr = {terms_obj[0].get('prop'): terms_obj[0].get('search_key')}
                                    terms_tag_name = terms_obj[0].get('tag_name')

                                    # for expiry details
                                    exp_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'expiry']
                                    exp_attr = {exp_obj[0].get('prop'): exp_obj[0].get('search_key')}
                                    exp_tag_name = exp_obj[0].get('tag_name')

                                    print(f"prop_obj:{prop_obj}")

                                    # get all elements from parent node
                                    ele_list = soup.find_all(parent_tag, attrs=parent_attr)
                                    print(f"parent_tag(new):{parent_tag},ele_list:{ele_list}")
                                    if ele_list is not None:
                                        descendant_list = []
                                        for el in range(len(ele_list)):
                                            el_obj = ele_list[el]
                                            descendants_list = el_obj.descendants
                                            descendant_list.append(descendants_list)
                                            for ds in descendants_list:
                                                descendant_list.append(descendants_list[ds].descendants)
                                                #print(f"div_name:{ds.name},class:{ds.get('class', '')}")

                                            description = el_obj.find(descr_tag_name, descr_attr)
                                            coupon_code = el_obj.find(coupon_code_tag_name, coupon_code_attr)
                                            terms = el_obj.find(terms_tag_name, terms_attr)
                                            expiry = el_obj.find(exp_tag_name, exp_attr)

                                            descr_text = description.text if description is not None and description.text is not None else ""
                                            cc_text = coupon_code.text if coupon_code is not None and coupon_code.text is not None else ""
                                            terms_text = terms.text if terms is not None and terms.text is not None else ""
                                            exp_text = expiry.text if expiry is not None and expiry.text is not None else "2020-12-31T00:00:00Z"

                                            if len(cc_text) > 0 or len(descr_text) > 0:
                                                site_coupon_list.append(
                                                    {"description": descr_text, "code": cc_text, "terms": terms_text,
                                                     "expiry": exp_text})

                                except Exception:
                                    msg = f'WebScrapeHandler=>fetch_site_data()=>prop_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                                    print(msg)
                                    logger.error(msg)
                        main_list.append(
                            {"host": site_host, "url": site_url, "name": site_name, "coupons": site_coupon_list})
                except Exception:
                    msg = f'WebScrapeHandler=>fetch_site_data()=>company_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    print(msg)
                    logger.error(msg)
            print(f"main_list:{main_list},no_of_items:{len(main_list)}")
            return main_list
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
        result = self.fetch_site_data()
        res = json.dumps(result)
        return res
