class AppSetting:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5
    USER_REC_SOURCE_FILE = 'data_model/user.json'
    LOG_CONFIG_JSON_FILE = 'app_configurations/logging_setup/logging_config.json'
    LOG_FILE_DIRECTORY = "logs"
    SELENIUM_WEB_DRIVER_PATH = 'web_drivers/windows/64_bit/geckodriver.exe'
    WEB_SCRAPE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    COMPANY_SITE_DETAILS_JSON_FILE = 'data_model/web_scrape_site_urls.json'
    PROMOTION_KEY_WORDS_JSON_FILE = 'data_model/promotion_key_words.json'
    CLIENT_API_URL_PREFIX = 'https://qoala-staging.herokuapp.com/'
    SITE_URL_MAX_REDIRECTS = 20
    SITE_LOAD_TIMEOUT = 30  # Page load timeout in seconds
    SITE_HOST = '127.0.0.1'
    SITE_HOST_PORT = 8000
    EXP_DATE_MAX_PARAGRAPH_LEN = 30
    HEADLESS_BROWSER = True # To determine whether or not to open browser window when content extraction is done per URL
