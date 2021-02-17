# Introduction 
Qoala Scrape is a python-based web scrape API to extract promotion details, coupon codes and other discount related information from 20 leading E-Commerce sites.

# Getting Started
1.	API Backend technology used 
2.	Software dependencies
3.	Hardware dependencies
4.	Project structure
5.	Setting up the project for development/deployment
6.	Executing the API for web scrape
7.	Structure of JSON files
8.	Known issues 
9.	Log files 

## 1.) API Backend technology used 

The API code has been developed using the language Python(**Version 3.8.3**) along with a relatively new framework called **FastAPI**(https://fastapi.tiangolo.com/).

FastAPI was chosen as the framework over other frameworks like Flask API and Django because it provides **more functionality while maintaining a lightweight nature**. Another advantage is that it has **built-in swagger documentation**. 

After successfully setting up the FastAPI project we can navigate to the documentation page by using the **‘/docs’** route as below: 

<IMG  src="https://lh6.googleusercontent.com/70UCkU70nqx0RWN_uVdo712ZKecQYUCkWkZ1y9dfrmC-lSwlFmrALKxu_Y0KJDj4scwl2UtvtM9AqWd_t9meV0QRtjK3XFSnY6DYdAk3TXBq9VUnlPjmU2vAc_cJT9yw1enuaW5d"  width="636"  height="304" style="margin-left:0px;margin-top:0px"/>

 Here, in order to provide security for the API , Basic Authentication with Bearer token has  been used where the API calling party should first login with valid credentials(username and password) Using the following API method :

<IMG  src="https://lh4.googleusercontent.com/yoatyy61lhE7y4MJZ4kQe5Flp-Z6Sr8-MBJ8KsoFJDCKzfWkHXnG13iw7UZvKAE-BZuC0Sx9XWalt9cbo-1uCKvC9s5REXAnYEX7QdnYIbCbDcfRlEyihvF5h52DuUS0Z0gRxAcg"  width="452"  height="224" style="margin-left:0px;margin-top:0px"/>

Here, for a valid login, a JWT token will be provided. This token can then be used in the header when executing other API calls(NOTE: User details are maintained in a JSON file named ‘user.json’)

NOTE: For the moment the API **does not use any authentication for the web scrape method**.If required, the authentication can be applied as below :

<B style="font-weight:normal"  id="docs-internal-guid-4465227b-7fff-17e7-39ea-93c02a2d240f"><SPAN style="border:none;width:602px;height:191px"><IMG  src="https://lh4.googleusercontent.com/J85gmRB0O1IAtoCJWDYfHALAh2p20Jwj8Bk38g4G8TK6RNt3VQFjJB6uNNkbZ44fVGBoGHV3oFTiZZ3x3OE6b6goKULsQH8okh2LcFHZP_LaC5liHTAjS3QvfYHcbKABzWG_jWz3"  width="602"  height="191" style="margin-left:0px;margin-top:0px"/></SPAN></B>

## 2.) Software dependencies

In order to maintain the basic package dependencies required, a file named **‘requirements.txt’** is present with the following packages :

<IMG  src="https://lh5.googleusercontent.com/ha1Hfh-TAphf5hsIsZRgz6k_siEsrbN8kXeVArNIZnssiSijt02juiEdHM4AeuLltPNUMXHDiVcn95swZ1Zw7vtIFylEqTFkWVv__UljITa1ImiTOE8WptG1e2TILjuc7vrH6Uif"  width="602"  height="333" style="margin-left:0px;margin-top:0px"/>

Also, in order to maintain the **Python runtime version** of the application another text file named **‘runtime.txt’** is used at the root:

<IMG  src="https://lh4.googleusercontent.com/gh2q9VutnRSN-4kBNdW1088OmK_LHklZL6uMTTMarKzjxZ1IJG__2F4mgIEDbEsq25dPf2hgpWoaBICWUBhLgs_0KG72iIGkhLiB1pDNZfRBm3BRZQbqbrAzCQryfT2p5DZ6PPwH"  width="602"  height="307" style="margin-left:0px;margin-top:0px"/>

NOTE : In addition to this, the **_latest version of Mozilla Firefox_** should be installed in the server, since the library **‘selenium’** is used along with the **OS platform matching web driver named ‘geckodriver’** that extracts the HTML content from the given URL.

## 3.) Hardware dependencies

This application was initially tested using a local Windows 64 bit machine having **_16GB of RAM memory_**. 

The application is totally cross-platform enabled but since the web scraping process requires a considerable amount of memory to extract the **_details of 20 sites at once_** using a **_browser-dependent driver_**, it is highly recommended to have an **_isolated machine of at least 8GB RAM memory_**. 

If it is a non-isolated, **_multi-app_** running machine, **_16GB would be the minimum recommended RAM memory_**.

## 4.) Project structure

<IMG  src="https://lh6.googleusercontent.com/KQS5KnQswMWrGtxQiqBpAIwtY8rU1bh35rn7uvFGKbpCuEynQrcZwn7LVQfL_KWIT9uV9iT4Tj52jD957UKAYiVO16Q9Wk5BQh2d-QdGatv647hzjrMhEyUZ9TE7n-6Oe6kndlFK"  width="356"  height="489" style="margin-left:0px;margin-top:0px"/>


The main folders are :

**_1. app_configurations :_** Contains the appsettings file and the application logging configurations

**_2. controller :_** This is the main folder that contains the operational files that execute user authentication, token generation and the web scraping functionality

**_3. data_model :_** This folder contains all the data related  files required for different functions like user authentication and web scraping

**_4. ‘env’ and ‘logs’ :_** these are user specific folders where ‘env’ folder represents the virtual environment(This is created after executing some commands explained in the next section). ‘logs’ folder will have the log files generated while debugging.running the applications

**_5. templates :_** This folder contains the html files used for the home page and log view page

**_6. web_drivers:_** This folder contains the executable ‘geckodriver’ files for a given OS platform(The path to the correct driver should be modified in app_settings.py using this folder’s path). For example, if the API is deployed/used in **windows 64-Bit OS**:

<IMG  src="https://lh6.googleusercontent.com/TxMn6p6H0BAzUG_NB7KEW4VIdKewTd3GrssITVUVKkbSjYQbUDpysKgoXh-Eaz72STs0hwluQstBgyhPycKNCnOPc14POpl9dEhJoq9UpGVICnJLa9VDyKR6JWqM3-COaszYQ1kv"  width="431"  height="184" style="margin-left:0px;margin-top:0px"/>

The **_app_settings.py_** file’s the value for **_‘SELENIUM_WEB_DRIVER_PATH’_** should be changed as follows : 

<IMG  src="https://lh6.googleusercontent.com/2Bvuh0ZSxvSOGAQpJGAL7tBbShVkigMd4kaHQJgILoXetsfd4fhzXD72WWiqdv5XFgT0S_jnS3MTvJ6enAbe3v853VWPAZZd0p-8BHEHt4Vk3pRX--uWAmUfqwARgFo_HmVol8_8"  width="602"  height="195" style="margin-left:0px;margin-top:0px"/>

**_NOTE : the file ‘main.py’ is the file that initiates the application_**

## 5.) Setting up the project for development/deployment

In order to set up the project for the first time in a development machine, the following steps should be followed :

**Note :** 
1. If using **VS Code**, **close** VS code for the **_step 1_** (From **_step 2 onwards_** VS Code should be opened).

2. From **_step 5_** onwards, the missing packages should be installed to the **_virtual environment_**.

3. If it is the **_production deployment_** ,use the **_Command line window_** to execute the commands. Here, before starting the python package installing process **_install and create the virtual environment first after the initial runtime installations_**.

4. Make sure you have installed the **_latest_** version of **_Mozilla Firefox browser_**.

**_Steps :_**
1. First install Python 3.8.3 runtime (Do not forget to tick the **_'Add Environment Path' in the beginning of the setup_**)

(Python runtime URL:https://www.python.org/downloads/release/python-383/)

2. Install the virtual environment:

   **_pip install --upgrade virtualenv_**

3. Setup the virtual environment:

    **_python -m venv env_**

4. Shift to the virtual environment :

    **_-    For VS Code_** :

     Using the Command Palette (View > Command Palette or 
         (Ctrl+Shift+P))[For more information visit:https://code.visualstudio.com/docs/python/tutorial-django]

   **_-    For OS Command line or PyCharm IDE:_**    
      
   Just execute **_‘env\scripts\activate’_** to shift into the 
          virtual environment

5. Install the other referenced packages all at once : 

   **_pip install -r requirements.txt_** 
   or
   **_python -m pip install --target pythonFiles --implementation py --no-deps -r requirements.txt_**

6. Run the API (Default port is 8000):

      **_uvicorn main:app --reload_** 

      (Note : Here, uvicorn is the server engine that initiates the FastAPI application while **_'main'_** is the name of the **_main file_**(In our case, **'main.py'**) that you have created an instance of FastAPI(). Finally, **_'app'_** is the name you gave for the application to create a FastAPI instance)

<IMG  src="https://lh3.googleusercontent.com/RTXOsQlwj2fgV3wxIyV0b952SvbEn6V2tIVy1qsQYtoIZDDmmhd1vBO64hP05E2AGceZV6cOlwPZ7mKDfucJulu0c2cBusfySlH86bVl9B6QHiIhAzO6TSawbMQqfm7VRsJbcUOI"  width="491"  height="205" style="margin-left:0px;margin-top:0px"/>



## 6.) Executing the API for web scrape

The web scrape API call can be triggered using 2 methods :

   **_a.] Using the swagger documentation (using the API site itself):_**
       
When you go to the API home page using <url>:<port_number>(Ex:-
       localhost:8000) you will see the link for the swagger 
       documentation page(Or you can simply try localhost:8000/docs):  
      
     

<IMG  src="https://lh4.googleusercontent.com/fHcf7ciBZEHKAO32RPF9TGlwsmvSldMXUNpr2clgfh2yLsqDp5TmKYNeCk0UV7p_GLxKQBYNOmR2q92ZIwFgyX8xOZ0AlbUN-cspSEFdwzxLsIeMQ7vy6U6d-4CY7oe0J-KEN0rC"  width="430"  height="206" style="margin-left:30px;margin-top:0px"/>

<IMG  src="https://lh3.googleusercontent.com/xCC_JeddQWr6aQV8wVAOSbjhnTB-R9_rf28KMMomo2ZeZjCjlEWdVTq-uDFgjQ4bvyIQDeUa8gPdx3SBE_UaoUB4dpcG_uCWsICEzusZm0Hfjs3u9oVpompSc6RX2vmuM2IMnd9j"  width="400"  height="206" style="margin-left:40px;margin-top:0px"/>                                                                           
       
   In this documentation, go to the API call **POST ​/web_scrape​/send** and try it out:
 
<IMG  src="https://lh5.googleusercontent.com/AnviQWQaly6vH1vRbILlFGzui_dxSEpmYF5P1tlNMCr8AGUt2DqC7UZ_0FFPZtpXUaTt_BTt4u2yn9I3Qz4hVrog9hc4FvZqJN5efgh3Q5pAeKopPHhxnuQH0NlyoEmTPnlM0Iz6"  width="490"  height="260" style="margin-left:0px;margin-top:0px;margin-bottom:20px"/>

Here, the coupon code, promotion and discount details of the targeted sites will be extracted using the earlier mentioned driver **_using for-loops_** as the iteration mode.

The file '**_data_model/web_site_scrape_urls.json'_** will be used as the main file that has the site url related data for a given e-commerce site and this json file will be used for the web scrape for-loop(Refer the method **_‘fetch_site_data()’_** of the class **_‘WebScrapeHandler’_**).


   **_b.] Using Postman and other code-based approaches (using external sites to make remote API calls):_**

This is more or less similar to 1.) where the only difference is that the API call is done remotely using POST method where 3rd party applications like Postman,Fiddler and any code like C#, Python, Java, Javascript..etc. are used.
   
**_NOTE => If the API call is authenticated, it should be triggered as shown in the .gif image in the following link:_**

https://lh5.googleusercontent.com/8V5HWR0qtv4eEg9VrHHHRyR1-1B4u3RgJanFzHd9eGvRV57LXwAkHpez9OfBgcLBnm7zVFCmSfojyPSSdye246jWrXJGPqwsRhfrS-vhnGlfyV-8C-y89gVMNYcFqqFxYNoIPkf7

When using external applications/code to get the token, use **x-www-form-urlencoded parameters** to send the username and password.

## 7.) Structure of JSON files

**1. Main JSON file with site URLs and coupon details markers(HTML elements) to extract the coupon details :**

<IMG  src="https://lh4.googleusercontent.com/fEmFSUXcx6-7nyeCUuPjsuHrXp6ueU5esAIsh4BrKXbNGX1nxbOSoT_KbBKN5dwK0OK707TGbFZzGDY3nBz7SLF7XW2RSy6FtpmLkkwmpPepM4rEj2fgbcvNCqZMVi0CoRq-RLLO"  width="602"  height="179" style="margin-left:0px;margin-top:0px"/>

Now let us expand the above highlighted JSON and see how the web scrape extraction is organized :

<IMG  src="https://lh4.googleusercontent.com/2FSkIg8yCaVvBeWVrafoyuwTrga5BiCo6BxIuM5DhZuVJcWaqFg4C0qDZcWqC_sL7xOgCF_iD3XHvIRqhOApIJfGzbM3tCwxSiEaw7RShwN6QWou14ZFDbVsfJgDwBSTa4C4YWkN"  width="602"  height="360" style="margin-left:0px;margin-top:0px"/>

We have taken the company **_‘Nike’_** as our example. Here, as you can see the JSON file is formed with a collection of objects as the highlighted one. A given site detail object consists of 4 main attribute values :

**_- company_no              :_** The sequence number of the company in the JSON list

**_- site_name               :_** The company/site name for which the extraction is done

**_- site_host               :_**  The name part of the site domain

**_- web_scrape_key_elements :_** The list of HTML element markers and the site URLs  required to extract the coupon details

Now let us see a single object/element in the list of **_‘web_scrape_key_elements’_**:

<B style="font-weight:normal"  id="docs-internal-guid-191ca7d8-7fff-4562-6a62-ea8825abc9d0"><SPAN style="border:none;width:602px;height:299px"><IMG  src="https://lh6.googleusercontent.com/2sOrb_FZZYJ9fs78a-O7Wdp4B8LsaLkr5v_DvcxejoOStVSkdj3rcXWyIFoyjt5cMBftJrMoTMNYTgiMgRpQtGPyF9Ma6Hdqlv_Uym-qagTIVl9xHUBk-aojLzPsn_jL_bH7dV4A"  width="602"  height="299" style="margin-left:0px;margin-top:0px"/></SPAN></B>

As shown above the attribute **_'web_scrape_key_elements'_** consists of a well-organized list of content extraction structure where the same URL may contain **_multiple parent HTML elements_** having the coupon code details. Here the attribute **_'prop'_** refers to the **_property of the HTML element_**(class,id,name..etc) while the attribute **_'tag_name'_** refers to the **_type of HTML element_** (HTML tags like div,span,section,h1,h2...etc). The **_'search_key'_** refers to the exact **_‘value’ text of the ‘prop’_**(Ex:- if 'tag-name'='div' and 'prop'='class' and 'search_key'= 'item_header', then we will extract the content of all the **_'div'_** HTML elements/tags where **_class='item_header'_**)

Also, the child elements(The values for the attribute 'prop_list') are structured in a way to match the final JSON to be posted to the client API where the attribute **_'text-type'_** denotes the type of detail we want to extract for the following output : 

<B style="font-weight:normal"  id="docs-internal-guid-edd567b2-7fff-b215-c9ca-7bb2098048f6"><SPAN style="border:none;width:409px;height:266px"><IMG  src="https://lh3.googleusercontent.com/5KSRT-hFxl6Vyz_uIJmsBS_XqKeIfmiIOeg7Jmz75SvTVeHnDz5H-19TutQevzzkBFEEsKYFa0Tw3Cvl2KWHa8r8oeS_3Mun-GS54ROVfpCU2dDP4FZlEt--V0IpB6GmqB8RqMGt"  width="409"  height="266" style="margin-left:0px;margin-top:0px"/></SPAN></B>

Now let us see an example on how to extract the coupon details using the correct HTML elements and the correct properties:

Example URL : https://www.gearbest.com/coupon.html

<B style="font-weight:normal"  id="docs-internal-guid-b45bb840-7fff-4316-fee1-40d9c8b3a9ea"><SPAN style="border:none;width:602px;height:248px"><IMG  src="https://lh4.googleusercontent.com/kMCf078l-zvoBvoueiwWKXWFdpR_tFb4QOUW3pUE2TTTp2_v9qTuGGpmafnQ_GltIjVIcFt40g78iimMs4hLduN7NJtyEbOqWx12HiGv_KsbfEvuB34vdjRr-W1Ugg6cVB5fzm9U"  width="602"  height="248" style="margin-left:0px;margin-top:0px"/></SPAN></B>

As shown above, if we need to get the coupon code of a given item/offer, we need to inspect the element using **_F12 key developer options_**. The **_first_** aim should be to **_find the parent element as denoted in (1.)_** . Then we will get the **_child elements_** as denoted from (2.) to (8.). The most important part thereafter is to **_group/categorize the child elements by mapping to the target text_** , namely **_description, code, terms_** and **_expiry_**. In the above example we can take the element (4.) as the description and element (8.) as the code(coupon code). As there is no significant mention of  terms  and expiry, we can neglect them and construct our JSON object as below :

<B style="font-weight:normal"  id="docs-internal-guid-864de5e9-7fff-2360-7914-c97736aba05e"><SPAN style="border:none;width:602px;height:289px"><IMG  src="https://lh6.googleusercontent.com/GPebAj6hxoOR40KHi3SGAMSAzt2VRK4oyEFUo4Nv9pEVoqWAPVCxbmEy1CS6mNjzWy7c3FVAqtMKZVPq43_p8bPM6GfI0GLZCdfznLfO_XUExc35zraQjVHXbSqd4OpKUWzENLf6"  width="602"  height="289" style="margin-left:0px;margin-top:0px"/></SPAN></B>

 **2. Sample JSON file with site URLs and coupon details markers(HTML elements) to extract the coupon details:**

<B style="font-weight:normal"  id="docs-internal-guid-3ca447e9-7fff-6518-33f5-e8b0ae8b6645"><SPAN style="border:none;width:602px;height:269px"><IMG  src="https://lh4.googleusercontent.com/-m2OUK382YtD4kkJXN1H6AVToayyG5ngMhNT5RHeteN5k3e6wrq9tkEIWhuwAmloKz5C0jkn9GclaGsoZMd-uu3SnzAzDpmOQ66hCd5q8WCzBav-NE1jIy1U8tsvamj7egPDNrQh"  width="602"  height="269" style="margin-left:0px;margin-top:0px"/></SPAN></B>

This is the same as the JSON file as explained in 1.) where the only difference is    that  we have the extraction marker details of **only 1 or 2 companies/sites**. This can be used for quick developer testing and is useful to check the functionality of the extraction using 1 or 2 companies  rather than iterating through the 20 sites in the main JSON file.

NOTE: To change the JSON file used for the extraction, just change the JSON file name at **_appsettings.py_** :

<B style="font-weight:normal"  id="docs-internal-guid-405f0a1c-7fff-d7e3-2cf9-0fd81704c95c"><SPAN style="border:none;width:602px;height:257px"><IMG  src="https://lh5.googleusercontent.com/70SQNcr1IPAHUSLq_PpEIkd7tEbyZvNr1WiMJcTmVmIWvAVZCFIn1wePWdBEiQtVs1R0nomgUoigjDriX0H1pbcS2u9XovqKZeaOLBakNm5i9dwTG_6UfoxXZ-Rci9my7nzBiIYt"  width="602"  height="257" style="margin-left:0px;margin-top:0px"/></SPAN></B>

**3. Keyword JSON file with keywords to filter the coupon code details:**

<B style="font-weight:normal"  id="docs-internal-guid-c60b0a21-7fff-46bb-9c26-77f78670189f"><SPAN style="border:none;width:602px;height:207px"><IMG  src="https://lh6.googleusercontent.com/v06jT5n3K995REkX-hEF-PkLS4g_JtP_FqF9yWMfqiHYsNVNMaHMKkTmTUNVHzY6CiVjjxI91C_IhrLdboZLX_Sco7YHjncMgTDx2B3o9m_qIC7YcKz8moOhk8cuRHP_LhDnT0pH"  width="602"  height="207" style="margin-left:0px;margin-top:0px"/></SPAN></B>

This is the keyword JSON file having the keywords for each text type (that is description, code, terms and expiry) used to refine and filter the search for the coupon details as much as possible. As highlighted above, the keywords are grouped as lists for each text type so that they can be used independently in different functions.

These keywords are used in the following functions :

<B style="font-weight:normal"  id="docs-internal-guid-0ba06ab3-7fff-a8e1-5fd1-0aec65b19904"><SPAN style="border:none;width:602px;height:203px"><IMG  src="https://lh5.googleusercontent.com/ads0aCsoJ4m0I0HNV4kvOXzuSnCamGv5gMjJjelbjp7eQydCs7iPf7o66aPzgrkgRMCSTxMGfRIXjeY_MlQByW-uJINP9x1ez9RbERTwxp8cERcAE-Cs6zQUEeccF6AhwyBMDVWr"  width="602"  height="203" style="margin-left:0px;margin-top:0px"/></SPAN></B>



**_NOTE :_** For the moment the **_keywords are not used for 'description' and 'code(coupon code)'_** because the description and code in the 20 sites are very much different from each other and thus applying keyword filters **_may skip some required details during the content extraction process_**. However, keywords are used for **_'expiry' and 'terms'_** since they follow a identifiable text pattern where 'expiry' may have a month and year  while 'terms' will have have text like 'terms & conditions apply','limited',..etc


## 8.) Known issues

If the RAM memory is not enough for the web scrape process, the following error will be given:

<B style="font-weight:normal"  id="docs-internal-guid-051fe871-7fff-3210-00b9-7760c79c0ea4"><SPAN style="border:none;width:602px;height:271px"><IMG  src="https://lh5.googleusercontent.com/picN_ZVYLEddfUao20uOFKcrDvJOPt_saCkL8caqrliCOO4D8dKrPX26kmAY11x1pgYSVH6snOHCNQLkb3DSGPUEa1f_O4cNOn3zCjCdPhvVpSmKeG6gwXRbiIWAScMwlrnqVSl5"  width="602"  height="271" style="margin-left:0px;margin-top:0px"/></SPAN></B>

## 9.) Log files

Each and every action executed by the application or runtime error occurred can be viewed through the log file by navigating to :

<B style="font-weight:normal"  id="docs-internal-guid-0f443340-7fff-5484-87fa-66b798bfa9c7"><SPAN style="border:none;width:334px;height:158px"><IMG  src="https://lh5.googleusercontent.com/UJyMA9Os01iBQQRR4vn_UNGzGL8RRWmgUD-5nlOrN5AGsS0BewT1WoNAKOp2Y5lq77r-3XCReYuPkfXn5AtZ3DFpBSRt9TjhnkUt36dGV9tH2OYMMjuJkOn96ZA0r3mCogM40KoP"  width="334"  height="158" style="margin-left:0px;margin-top:0px"/></SPAN></B>

<B style="font-weight:normal"  id="docs-internal-guid-7ac4c279-7fff-aa2b-539c-db75a28471d8"><SPAN style="border:none;width:295px;height:94px"><IMG  src="https://lh4.googleusercontent.com/RmXRXp-W1PcimDQ83M6kW0OEhVXCTsEv5it_sn5uc8jJtE0vC87H6OSJbumKOjMyhMceBRROxzqUYVi3xC6J6BcQZsyiDWYjuaOhYXO2avrvh_kfpvtJgjYsUgBV6kOm8zfu1JFh"  width="295"  height="94" style="margin-left:0px;margin-top:0px"/></SPAN></B>

<B style="font-weight:normal"  id="docs-internal-guid-0b9ff7a9-7fff-4bf6-bfd8-fbdecfe2a5a1"><SPAN style="border:none;width:320px;height:109px"><IMG  src="https://lh5.googleusercontent.com/KjIRurrraHWXhwmIFTYz3HfuQnQ_sW4q0bJ1HjlCozV9CPmflX2YxWXSnmOd5x9790Chd71APzRslFW7qrWvvPj541WrchH8VtDA7z6GOPT0OVdWMtLD09Z-cwz1WVWYhkM0YD6t"  width="320"  height="109" style="margin-left:0px;margin-top:0px"/></SPAN></B>

<B style="font-weight:normal"  id="docs-internal-guid-580ea3b9-7fff-8163-029f-9d589ed661d5"><SPAN style="border:none;width:275px;height:142px"><IMG  src="https://lh3.googleusercontent.com/2m8g3j_BBqJ8RnWqJbl-2HKg4jtCS4s3onQ7chSr6Mk1GoBS7ZDaq1YlmNndKweBsGJ-Nkap-QwIUQCN5C7JI41IxQgZF4mdd1Y1spy8VWNjvjLKnX5wkA2dw5jdtx1VThz4OK3k"  width="275"  height="142" style="margin-left:0px;margin-top:0px"/></B>

As shown above, log files are created as date-specific files and are very useful to check any runtime error.

The path for the log file is configured at:

<B style="font-weight:normal"  id="docs-internal-guid-75afd449-7fff-60d5-6608-87654d03fb08"><SPAN style="border:none;width:602px;height:207px"><IMG  src="https://lh3.googleusercontent.com/a607EUGULSlv1urjzdru63wzWJFnTpSBwLgoiVdi-_RtyTL0dW-bp0U5bki7jvRe8sTZgsyGw-50oe1X-cZJ9qPyd8CNuj1sdHNcrgZchOCe58x23paqrRPxvCmHhcCw8Vht-dBe"  width="602"  height="207" style="margin-left:0px;margin-top:0px"/></SPAN></B>
