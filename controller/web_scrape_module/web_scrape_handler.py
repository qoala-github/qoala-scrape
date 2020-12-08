import datetime
import sys
import traceback
import requests
import json
import logging
import uuid
import http3

from bs4 import BeautifulSoup
from fastapi import HTTPException
from app_configurations.app_settings import AppSetting
from selenium import webdriver

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

web_driver_path = app_settings.SELENIUM_WEB_DRIVER_PATH
options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
page_load_timeout = app_settings.SITE_LOAD_TIMEOUT
max_exp_date_para_len = app_settings.EXP_DATE_MAX_PARAGRAPH_LEN

# Get 2 weeks future date from today=>Client requirement
current_utc = datetime.datetime.strptime(str(datetime.datetime.utcnow().date()), "%Y-%m-%d")
current_utc_with_time = datetime.datetime.utcnow()
date_diff = datetime.timedelta(weeks=2)
exp_date_utc = current_utc + date_diff
exp_date_split = str(exp_date_utc).split(' ')
formatted_exp_date = f"{exp_date_split[0]}T{exp_date_split[1]}Z"


class WebScrapeHandler:
    error_list = []
    main_list = []
    site_coupon_list = []

    async def fetch_site_data(self):
        loop_ref = ""
        error_guid = uuid.uuid1()
        try:
            user_agent = app_settings.WEB_SCRAPE_USER_AGENT
            # headers = {"user-agent": user_agent}
            # max_redirects = int(app_settings.SITE_URL_MAX_REDIRECTS)
            company_site_list = []
            company_no = ""
            site_name = ""

            data_count = len(company_json)
            for csl in range(data_count):
                company_site_list.append(company_json[csl])

            for c in range(len(company_site_list)):
                try:
                    com_obj = company_site_list[c]
                    print(com_obj)
                    company_no = com_obj.get('company_no')
                    site_name = com_obj.get('site_name')
                    site_host = com_obj.get('site_host')
                    target_elem = com_obj.get('web_scrape_key_elements')
                    await self.read_web_scrape_elements(company_no, site_name, site_host, target_elem)
                    self.main_list.append()
                except Exception:  # company loop exception
                    msg = f'WebScrapeHandler=>fetch_site_data()=>company_loop=>{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    self.error_list.append(
                        {'error_loop_level': 'company', 'company_no': company_no, 'company_name': site_name,
                         'error_msg': msg})
                    print(msg)
                    logger.error(msg)
        except Exception:
            msg = f'WebScrapeHandler=>fetch_site_data()=>before_loop=>error_guid:{error_guid},loop_number:{loop_ref}:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            self.error_list.append(msg)
            error_list_obj = {'error_guid': error_guid, 'error_list': self.error_list}
            print(msg)
            logger.error(msg)
            self.error_list.append(
                {'error_loop_level': 'company', 'company_no': company_no, 'company_name': site_name,
                 'error_msg': msg})

        finally:
            print(f"error_list:{self.error_list}")
            if len(self.error_list) > 0:
                error_list_obj = {'error_guid': str(error_guid), 'error_list': self.error_list}
                await self.save_json_as_file(error_list_obj, f'logs/{str(error_guid)}.json')

            print(f"main_list:{self.main_list},no_of_items:{len(self.main_list)}")
            if len(self.main_list) > 0:
                error_list_obj = {'time_stamp': str(current_utc_with_time), 'site_coupon_list': self.main_list}
                await self.save_json_as_file(error_list_obj, f'logs/{str(error_guid)}_payload.json')

            return self.main_list

    # region "Sub functions for for-loops"

    async def read_web_scrape_elements(self, company_no, site_name, site_host, target_elem_list):
        try:
            for i in range(len(target_elem_list)):
                try:
                    self.site_coupon_list = []  # NOTE : The coupon list should be reset for each site URL
                    target_elem_obj = target_elem_list[i]
                    site_url = target_elem_obj.get('site_url')
                    print(f"{company_no}:{site_url}")
                    scrape_filters = target_elem_obj.get('scrape_filters')
                    soup = await self.get_html_content(site_url)
                    res_coupon_list = await self.read_scrape_filters(company_no, site_name, site_url, scrape_filters,
                                                                     soup)
                except Exception:
                    msg = f'WebScrapeHandler=>fetch_site_data()=>company_loop=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    print(msg)
                    self.error_list.append(
                        {'error_loop_level': 'web_scrape_element_loop', 'company_no': company_no,
                         'company_name': site_name, 'site_url': site_url,
                         'error_msg': msg})
                    logger.error(msg)
                    res_coupon_list = []
                finally:
                    self.main_list.append(
                        {"host": site_host, "url": site_url, "name": site_name, "coupons": res_coupon_list})
        except Exception:
            msg = f'WebScrapeHandler=>web_scrape_element_loop():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            self.error_list.append(
                {'error_loop_level': 'scrape_filter_loop', 'company_no': company_no,
                 'company_name': site_name, 'site_url': site_url,
                 'error_msg': msg})
            return "error", "Se produjo un error al publicar los datos del web scrape"

    async def read_scrape_filters(self, company_no, site_name, site_url, scrape_filters, html_soup):
        result_scrape_list = []
        try:
            for sf in range(len(scrape_filters)):
                try:
                    sf_obj = scrape_filters[sf]
                    parent_node = sf_obj.get('parent_node')
                    parent_tag = parent_node.get('tag_name')
                    parent_attr = {
                        parent_node.get('prop'): parent_node.get('search_key').replace("Â", "")}
                    prop_attr_sub_list = []
                    prop_attr_sub_list = sf_obj.get('prop_list')

                    # get all elements from parent node
                    ele_list = html_soup.find_all(parent_tag, attrs=parent_attr)
                    print(f"parent_tag(new):{parent_tag},ele_list:{ele_list}")

                    # get actual descendant elements
                    elem_by_field = await self.get_elems_by_field(prop_attr_sub_list)
                    descr_node = elem_by_field["description"]
                    coupon_code_node = elem_by_field["coupon_code"]
                    terms_node = elem_by_field["terms"]
                    expiry_node = elem_by_field["expiry"]

                    if ele_list is not None:
                        site_data = {'company_no': company_no, 'site_name': site_name, 'site_url': site_url}
                        result_scrape_list = await self.read_child_elements(ele_list, descr_node, coupon_code_node,
                                                                            terms_node, expiry_node,
                                                                            site_data)
                except Exception:
                    msg = f'WebScrapeHandler=>fetch_site_data()=>company_loop=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    print(msg)
                    self.error_list.append(
                        {'error_loop_level': 'parent element', 'company_no': company_no,
                         'company_name': site_name, 'site_url': site_url,
                         'error_msg': msg})
                    logger.error(msg)
        except Exception:
            msg = f'WebScrapeHandler=>scrape_filter_loop():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            self.error_list.append(
                {'error_loop_level': 'scrape_filter_loop', 'company_no': company_no,
                 'company_name': site_name, 'site_url': site_url,
                 'error_msg': msg})
        return result_scrape_list

    async def read_child_elements(self, ele_list, descr_node, coupon_code_node, terms_node, expiry_node, site_data):
        try:
            descr_attr = descr_node.get("attr")
            descr_tag_name = descr_node.get("tag_name")
            coupon_code_attr = coupon_code_node.get("attr")
            coupon_code_tag_name = coupon_code_node.get("tag_name")
            terms_attr = terms_node.get("attr")
            terms_tag_name = terms_node.get("tag_name")
            exp_attr = expiry_node.get("attr")
            exp_tag_name = expiry_node.get("tag_name")

            for el in range(len(ele_list)):
                try:
                    el_obj = ele_list[el]
                    description = el_obj.find(descr_tag_name, descr_attr)
                    coupon_code = el_obj.find(coupon_code_tag_name, coupon_code_attr)
                    terms = el_obj.find(terms_tag_name, terms_attr)
                    expiry = el_obj.find(exp_tag_name, exp_attr)

                    # Note : Sometimes the coupon code is available as an input value
                    coupon_code_txt = coupon_code.text if coupon_code is not None else ""
                    coupon_code_txt = coupon_code.get(
                        'value') if coupon_code is not None and len(
                        coupon_code_txt.strip()) == 0 else coupon_code_txt
                    coupon_code_txt = "" if coupon_code_txt is None else coupon_code_txt

                    descr_text = await self.get_description(
                        description.text) if description is not None else ""
                    cc_text = await self.get_coupon_code(
                        coupon_code_txt) if coupon_code is not None else ""
                    terms_text = await self.get_terms(terms.text) if terms is not None else ""
                    exp_text = await self.get_expiry_date(
                        expiry.text) if expiry is not None else ""

                    if len(cc_text) > 0 or len(descr_text) > 0:
                        self.site_coupon_list.append(
                            {"description": descr_text, "code": cc_text, "terms": terms_text,
                             "expiry": exp_text})
                except Exception:
                    msg = f'WebScrapeHandler=>read_child_elements(),inside loop:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    print(msg)
                    logger.error(msg)
                    self.error_list.append(
                        {'error_loop_level': 'read_child_elements(),inside loop',
                         'company_no': site_data.get('company_no'),
                         'company_name': site_data.get('site_name'), 'site_url': site_data.get('site_url'),
                         'error_msg': msg})
            return self.site_coupon_list
        except Exception:
            msg = f'WebScrapeHandler=>child_element_loop():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            self.error_list.append(
                {'error_loop_level': 'child_element_loop', 'company_no': site_data.get('company_no'),
                 'company_name': site_data.get('site_name'), 'site_url': site_data.get('site_url'),
                 'error_msg': msg})
            empty_list = []
            return empty_list

    # endregion

    # region "Functions to extract and format target text by type"

    async def get_html_content(self, site_url):
        try:
            driver = webdriver.Firefox(executable_path=web_driver_path,
                                       firefox_options=options)
            driver.set_page_load_timeout(page_load_timeout)
            driver.get(site_url)
            html_content = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html_content, "html.parser")
            return soup
        except Exception:
            msg = f'WebScrapeHandler=>get_html_content()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    async def get_elems_by_field(self, prop_attr_sub_list):
        try:
            # for description
            descr_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'description']
            descr_attr = {descr_obj[0].get('prop'): descr_obj[0].get('search_key').replace("Â", "")}
            descr_tag_name = descr_obj[0].get('tag_name')

            # for coupon code
            coupon_code_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'code']
            coupon_code_attr = {coupon_code_obj[0].get('prop'): coupon_code_obj[0].get('search_key').replace("Â", "")}
            coupon_code_tag_name = coupon_code_obj[0].get('tag_name')

            # for terms details
            terms_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'terms']
            terms_attr = {terms_obj[0].get('prop'): terms_obj[0].get('search_key').replace("Â", "")}
            terms_tag_name = terms_obj[0].get('tag_name')

            # for expiry details
            exp_obj = [d for d in prop_attr_sub_list if d.get('text_type') == 'expiry']
            exp_attr = {exp_obj[0].get('prop'): exp_obj[0].get('search_key').replace("Â", "")}
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

    async def is_keyword_found(self, keyword_list, element_text):
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

    async def get_description(self, descr_text):
        try:
            result = ""
            if descr_text is not None:
                data_keys = promo_keyword_json["description"].get('keyword_list')
                result = descr_text  # descr_text if self.is_keyword_found(data_keys, descr_text.lower()) else ""
            return result.replace("\n", "").replace("\n\n", "").strip()
        except Exception:
            msg = f'WebScrapeHandler=>get_description()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    async def get_coupon_code(self, coupon_code_text):
        try:
            result = coupon_code_text
            return result.replace("\n", "").replace("\n\n", "").strip()
        except Exception:
            msg = f'WebScrapeHandler=>get_coupon_code()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    async def get_terms(self, terms_text):
        try:
            print(f"terms_text:{terms_text}")
            result = ""
            if terms_text is not None:
                data_keys = promo_keyword_json["terms"].get('keyword_list')
                result = terms_text if await self.is_keyword_found(data_keys, terms_text.lower()) else ""
            return result.replace("\n", "").replace("\n\n", "").strip()
        except Exception:
            msg = f'WebScrapeHandler=>get_terms()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    async def get_expiry_date(self, exp_date_text):
        try:
            result = ""

            if exp_date_text is not None:
                data_keys = promo_keyword_json["expiry"].get('keyword_list')
                result = exp_date_text if await self.is_keyword_found(data_keys, exp_date_text) else ""
                result = formatted_exp_date if len(exp_date_text) > max_exp_date_para_len else result
                return result.replace("\n", "").replace("\n\n", "").strip()
        except Exception:
            msg = f'WebScrapeHandler=>get_expiry_date()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    # endregion

    # region "File saving"

    async def save_json_as_file(self, json_obj, file_path):
        try:
            logger.info(json_obj)
            with open(file_path, 'w') as outfile:
                json.dump(json_obj, outfile)
        except Exception:
            msg = f'WebScrapeHandler=>save_json_as_file()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)

    # endregion

    # region "Post data to client API"

    async def get_access_token(self):
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

    async def post_web_scrape_data(self, auth_token, web_scrape_data):
        try:
            msg = f"Inside post_web_scrape_data()=>auth_token={auth_token}"
            print(msg)
            logger.info(msg)
            req_url = f"{app_settings.CLIENT_API_URL_PREFIX}brands"
            msg = f"req_url:{req_url}"
            print(msg)
            logger.info(msg)
            body_data = web_scrape_data
            msg = {"req_url": req_url, "auth_token": auth_token, "data": body_data}
            print(msg)
            logger.info(msg)
            res = None
            headers_param = {"Content-type": "application/json"} if auth_token == "not_required" else {
                "Authorization": f"Bearer {auth_token}", "Content-type": "application/json"}
            msg = f"headers_param:{headers_param}"
            print(msg)
            logger.info(msg)

            client = http3.AsyncClient()
            post_data_batch_list = await self.get_data_batches(body_data)
            batch_error_count: int = 0

            for i in range(len(post_data_batch_list)):
                try:
                    data_batch = post_data_batch_list[i]
                    # NOTE : If the list is empty then the string is '[]' which is a string of length 2
                    if data_batch is not None and len(data_batch) > 2:
                        res = await client.post(url=req_url, data=data_batch,
                                                headers=headers_param)
                        print(f"res:{res}")
                        msg = f"res_status={res.status_code}, res-reason={res.reason_phrase}, res_text={res.text}"
                        print(msg)
                        logger.info(msg)
                        if res.status_code == 200:
                            batch_error_count += 0
                        else:
                            batch_error_count += 1
                except Exception:
                    msg = f'WebScrapeHandler=>post_web_scrape_data():Data batch loop=>Data batch{i + 1}{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
                    print(msg)
                    logger.error(msg)

            result_message = "Publicó con éxito los datos del raspado de la web" if batch_error_count == 0 else f"{batch_error_count} de cada {len(post_data_batch_list)} lotes de datos no se cargaron"
            result_status = "success" if batch_error_count == 0 else "error"
            return result_status, result_message
        except Exception:
            msg = f'WebScrapeHandler=>post_web_scrape_data():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            return "error", "Se produjo un error al publicar los datos del web scrape"

    async def get_data_batches(self, body_data):
        try:
            post_data_batch_list = []
            data_batch_01 = json.dumps(json.loads(body_data)[0:11])
            post_data_batch_list.append(data_batch_01)
            data_batch_02 = json.dumps(json.loads(body_data)[11:21])
            post_data_batch_list.append(data_batch_02)
            return post_data_batch_list
        except Exception:
            msg = f'WebScrapeHandler=>get_data_batches():{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            raise Exception

    async def send_promotion_data(self):
        try:
            result = await self.fetch_site_data()
            res = json.dumps(result)

            # login to client API and get token
            # NOTE : Currently, no access token is required
            access_token = "not_required"  # await self.get_access_token()

            if access_token is not None and access_token != "error":
                msg = f"Successfully received access_token={access_token}"
                print(msg)
                logger.info(msg)

                result_status, result_msg = await self.post_web_scrape_data(auth_token=access_token,
                                                                            web_scrape_data=res)

                if result_status == "success":
                    # Successfully posted the web scrape data
                    logger.info(f"{msg},{result_msg}")
                    return {"Message": result_msg}
                else:
                    # An Error occurred while posting the web scrape data
                    print(result_msg)
                    logger.error(result_msg)
                    raise HTTPException(status_code=400, detail=result_msg)
            else:
                msg = "Ficha de acceso inválida"
                print(msg)
                raise HTTPException(status_code=400, detail=msg)
            return response
        except Exception:
            msg = f'WebScrapeHandler=>send_promotion_data()=>{sys.exc_info()[2]}/n{traceback.format_exc()} occurred'
            print(msg)
            logger.error(msg)
            raise HTTPException(status_code=400, detail=msg)

    # endregion
