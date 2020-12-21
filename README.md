# Introduction 
Qoala Scrape is a python-based web scrape API to extract promotion details, coupon codes and other discount related information from 20 leading E-Commerce sites.

# Getting Started
1.	API Backend technology used 
2.	Software dependencies
3.	Hardware dependencies
4.	Project structure
5.	Setting up the project for development/deployment
6.	Executing the API for web scrape
7.	Known issues 

## 1.) API Backend technology used 

The API code has been developed using the language Python(**Version 3.8.3**) along with a relatively new framework called **FastAPI**(https://fastapi.tiangolo.com/).

FastAPI was chosen as the framework over other frameworks like Flask API and Django because it provides **more functionality while maintaining a lightweight nature**. Another advantage is that it has **built-in swagger documentation**. 

After successfully setting up the FastAPI project we can navigate to the documentary=ion page by using the **‘/docs’** route as below: 

<IMG  src="https://lh6.googleusercontent.com/70UCkU70nqx0RWN_uVdo712ZKecQYUCkWkZ1y9dfrmC-lSwlFmrALKxu_Y0KJDj4scwl2UtvtM9AqWd_t9meV0QRtjK3XFSnY6DYdAk3TXBq9VUnlPjmU2vAc_cJT9yw1enuaW5d"  width="636"  height="304" style="margin-left:0px;margin-top:0px"/>

 Here, in order to provide security for the API , Basic Authentication with Bearer token has  been used where the API calling party should first login with valid credentials(username and password) Using the following API method :

<IMG  src="https://lh4.googleusercontent.com/yoatyy61lhE7y4MJZ4kQe5Flp-Z6Sr8-MBJ8KsoFJDCKzfWkHXnG13iw7UZvKAE-BZuC0Sx9XWalt9cbo-1uCKvC9s5REXAnYEX7QdnYIbCbDcfRlEyihvF5h52DuUS0Z0gRxAcg"  width="452"  height="224" style="margin-left:0px;margin-top:0px"/>

Here, for a valid login, a JWT token will be provided. This token can then be used in the header when executing other API calls(NOTE: User details are maintained in a JSON file named ‘user.json’)

NOTE: For the moment the API **does not use any authentication**.If required, the authentication can be applied as below :

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

   **_pip install -r requirement.txt_** 
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
   
**_NOTE => If the API call is authenticated, it should be triggered as follows:_**
      
<IMG  src="https://lh3.googleusercontent.com/q4e9tm65ODa6lJBEdKHoJKDS79Oy2xBgmpZ5bAdo2MbZxfbYrdDxMkbXGYfb7mDe78ZX7ii6qYAevKRCO9Hj3LQ-TkqxjcF0FSaMSYfHUUrK0is4ulfMyQwAsLe3PM7mI-qE8exa"  width="403"  height="213" style="margin-left:0px;margin-top:0px"/>


When using external applications/code to get the token, use **x-www-form-urlencoded parameters** to send the username and password.

## 7.) Known issues

If the RAM memory is not enough for the web scrape process, the following error will be given:

<B style="font-weight:normal"  id="docs-internal-guid-051fe871-7fff-3210-00b9-7760c79c0ea4"><SPAN style="border:none;width:602px;height:271px"><IMG  src="https://lh5.googleusercontent.com/picN_ZVYLEddfUao20uOFKcrDvJOPt_saCkL8caqrliCOO4D8dKrPX26kmAY11x1pgYSVH6snOHCNQLkb3DSGPUEa1f_O4cNOn3zCjCdPhvVpSmKeG6gwXRbiIWAScMwlrnqVSl5"  width="602"  height="271" style="margin-left:0px;margin-top:0px"/></SPAN></B>