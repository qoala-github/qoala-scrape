import sys
import traceback
import requests
import json
import logging


from bs4 import BeautifulSoup
from requests import Response
from app_configurations.app_settings import AppSetting

app_settings = AppSetting()
logger = logging.getLogger(__name__)

# get the promotion keywords json
keyword_json = None
with open(app_settings.PROMOTION_KEY_WORDS_JSON_FILE) as pkf:
    promo_keyword_json = json.load(pkf)

# get the company details json
company_json = None
with open(app_settings.COMPANY_SITE_DETAILS_JSON_FILE) as f:
    company_json = json.load(f)


class WebScrapeHandler:

    def fetch_site_data(self):
        loop_ref = ""
        try:
            user_agent = app_settings.WEB_SCRAPE_USER_AGENT
            headers = {"user-agent": user_agent}
            max_redirects = int(app_settings.SITE_URL_MAX_REDIRECTS)
            main_list = []
            site_coupon_list = []
            company_list = []
            data_count = 7  # len(company_json)
            for csl in range(data_count):
                company_list.append(company_json[csl])

            for c in range(len(company_list)):
                try:
                    com_obj = company_list[c]
                    print(com_obj)
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

                                    print(f"prop_obj:{prop_obj}")

                                    # get all elements from parent node
                                    ele_list = soup.find_all(parent_tag, attrs=parent_attr)
                                    print(f"parent_tag(new):{parent_tag},ele_list:{ele_list}")

                                    # get actual descendant elements
                                    elem_by_field = self.get_elems_by_field(prop_attr_sub_list)
                                    descr_node = elem_by_field["description"]
                                    coupon_code_node = elem_by_field["coupon_code"]
                                    terms_node = elem_by_field["terms"]
                                    expiry_node = elem_by_field["expiry"]

                                    descr_attr = descr_node.get("attr")
                                    descr_tag_name = descr_node.get("tag_name")
                                    coupon_code_attr = coupon_code_node.get("attr")
                                    coupon_code_tag_name = coupon_code_node.get("tag_name")
                                    terms_attr = terms_node.get("attr")
                                    terms_tag_name = terms_node.get("tag_name")
                                    exp_attr = expiry_node.get("attr")
                                    exp_tag_name = expiry_node.get("tag_name")

                                    if ele_list is not None:
                                        for el in range(len(ele_list)):
                                            el_obj = ele_list[el]
                                            description = el_obj.find(descr_tag_name, descr_attr)
                                            coupon_code = el_obj.find(coupon_code_tag_name, coupon_code_attr)
                                            terms = el_obj.find(terms_tag_name, terms_attr)
                                            expiry = el_obj.find(exp_tag_name, exp_attr)

                                            descr_text = self.get_description(
                                                description.text) if description is not None else ""
                                            cc_text = self.get_coupon_code(
                                                coupon_code.text) if coupon_code is not None else ""
                                            terms_text = self.get_terms(terms.text) if terms is not None else ""
                                            exp_text = self.get_expiry_date(
                                                expiry.text) if expiry is not None else "2020-12-31T00:00:00Z"

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

    def get_elems_by_field(self, prop_attr_sub_list):
        try:
            # for description
            descr_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'description']
            descr_attr = {descr_obj[0].get('prop'): descr_obj[0].get('search_key')}
            descr_tag_name = descr_obj[0].get('tag_name')

            # for coupon code
            coupon_code_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'code']
            coupon_code_attr = {coupon_code_obj[0].get('prop'): coupon_code_obj[0].get('search_key')}
            coupon_code_tag_name = coupon_code_obj[0].get('tag_name')

            # for terms details
            terms_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'terms']
            terms_attr = {terms_obj[0].get('prop'): terms_obj[0].get('search_key')}
            terms_tag_name = terms_obj[0].get('tag_name')

            # for expiry details
            exp_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'expiry']
            exp_attr = {exp_obj[0].get('prop'): exp_obj[0].get('search_key')}
            exp_tag_name = exp_obj[0].get('tag_name')

            result_obj = {
                "description": {"attr": descr_attr, "tag_name": descr_tag_name},
                "coupon_code": {"attr": coupon_code_attr, "tag_name": coupon_code_tag_name},
                "terms": {"attr": terms_attr, "tag_name": terms_tag_name},
                "expiry": {"attr": exp_attr, "tag_name": exp_tag_name}
            }
            return result_obj
        except Exception:
            msg = f'WebScrapeHandler=>get_elems_by_field()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
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

    def get_description(self, descr_text):
        try:
            result = ""
            if descr_text is not None:
                data_keys = promo_keyword_json["description"].get('keyword_list')
                result = descr_text if self.is_keyword_found(data_keys, descr_text.lower()) else ""
            return result
        except Exception:
            msg = f'WebScrapeHandler=>get_description()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def get_coupon_code(self, coupon_code_text):
        try:
            result = ""
            if coupon_code_text is not None:
                data_keys = promo_keyword_json["coupon_code"].get('keyword_list')
                result = coupon_code_text if self.is_keyword_found(data_keys, coupon_code_text.lower()) else ""
            return result
        except Exception:
            msg = f'WebScrapeHandler=>get_coupon_code()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def get_terms(self, terms_text):
        try:
            print(f"terms_text:{terms_text}")
            result = ""
            if terms_text is not None:
                data_keys = promo_keyword_json["terms"].get('keyword_list')
                result = terms_text if self.is_keyword_found(data_keys, terms_text.lower()) else ""
            return result
        except Exception:
            msg = f'WebScrapeHandler=>get_terms()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def get_expiry_date(self, exp_date_text):
        try:
            result = ""
            if exp_date_text is not None:
                data_keys = promo_keyword_json["expiry"].get('keyword_list')
                result = "2020-12-31T00:00:00Z" if self.is_keyword_found(data_keys, exp_date_text) else ""
                return result
        except Exception:
            msg = f'WebScrapeHandler=>get_expiry_date()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def send_promotion_data(self):
        try:
            result = self.fetch_site_data()
            res = json.dumps(result)

            # login to client API and get token
            access_token = self.get_access_token()

            if (access_token is not None and access_token != "error"):
                msg = f"Successfully received access_token={access_token}"
                print(msg)
                logger.info(msg)

                if self.post_web_scrape_data(auth_token=access_token, web_scrape_data=res):
                    # Successfully posted the web scrape data
                    success_msg = "Message:Publicó con éxito los datos del raspado de la web"
                    logger.error(f"{msg},{success_msg}")
                    return Response({f"{success_msg}"}, status=200)
                else:
                    # An Error occurred while posting the web scrape data
                    msg = "Se produjo un error al publicar los datos del web scrape"
                    print(msg)
                    logger.error(msg)
                    return Response({f"Message:{msg}"}, status=400)
        except Exception:
            msg = f'WebScrapeHandler=>send_promotion_data()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    def get_access_token(self):
        try:
            msg = f"Inside get_access_token()"
            access_token = ""
            req_url = f"{app_settings.CLIENT_API_URL_PREFIX}get_access_token"
            print(msg)
            logger.info(msg)
            data = {"grant_type": "authorization_code"}
            msg = f"request data=>req_url={req_url},data={data}"
            print(msg)
            logger.info(msg)
            res = requests.post(req_url, data=data)
            res_json = json.loads(res.text)
            msg = f"res_status={res.status_code}, res-reason={res.reason}, res_text={res.text}"
            print(msg)
            logger.info(msg)
            if res.status_code == 200:
                access_token = res_json["access_token"]
                return access_token
            else:
                access_token = "error"
            return access_token
        except Exception:
            msg = f'WebScrapeHandler=>get_access_token():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            return "error"

    def post_web_scrape_data(self, auth_token, web_scrape_data):
        try:
            msg = f"Inside publish_script_tag()=>auth_token={auth_token}"
            print(msg)
            logger.info(msg)
            req_url = f"{app_settings}post_web_scrapes"
            msg = f"req_url:{req_url}"
            print(msg)
            logger.info(msg)
            body_data = web_scrape_data
            msg = {"req_url": req_url, "auth_token": auth_token, "data": body_data}
            print(msg)
            logger.info(msg)
            res = requests.post(req_url, data=body_data,
                                headers={"Authorization": "Bearer %s" % auth_token, "Content-type": "application/json"})
            msg = f"res_status={res.status_code}, res-reason={res.reason}, res_text={res.text}"
            print(msg)
            logger.info(msg)
            if res.status_code == 200:
                return True
            else:
                return False
        except Exception:
            msg = f'WebScrapeHandler=>get_access_token():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            return False
