import re
import time
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def track(keyword, asin):
    options = Options()
    options.add_argument("-incognito")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    url = "https://www.amazon.co.uk/"

    search_keyword = keyword

    driver.get(url)
    address = driver.find_element_by_xpath('//*[@id="nav-global-location-slot"]/span/a')
    address.click()
    time.sleep(2)
    address_f = driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]')
    address_f.send_keys("OL11 1NU")
    time.sleep(1.5)
    apply_btn = driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input')
    apply_btn.click()
    time.sleep(2)
    search_bar = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    search_bar.send_keys(search_keyword)
    search_bar_btn = driver.find_element_by_xpath('//*[@id="nav-search-submit-text"]/input')
    search_bar_btn.click()
    filename = 'C:\\Users\\Bilal\\Pictures\\printed\\foo.png'
    driver.get_screenshot_as_file(filename)

    body_el = driver.find_element_by_css_selector("body")
    html_str = body_el.get_attribute("innerHTML")
    html_obj = HTML(html=html_str)

    sel = 'a.a-link-normal'
    links = html_obj.links
    new_links = [f"https://www.amazon.co.uk{x}" for x in links]

    regex_options = [
        #     r"https://www.amazon.com/gp/product/(?P<product_id>[\w-]+)/",
        #     r"https://www.amazon.com/dp/(?P<product_id>[\w-]+)/",
        #     r"https://www.amazon.com/(?P<slug>[\w-]+)/dp/(?P<product_id>[\w-]+)/",
        #      r"https://www.amazon.co.uk/gp/product/(?P<product_id>[\w-]+)/",
        #     r"https://www.amazon.co.uk/dp/(?P<product_id>[\w-]+)/",
        r"https://www.amazon.co.uk/(?P<slug>[\w-]+)/dp/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
        r"https://www.amazon.co.uk/(?P<slug>[\w-]+)/dp/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
    ]

    def extract_product_id_from_url(url):
        product_id = None
        rank_str = None
        for regex_str in regex_options:
            regex = re.compile(regex_str)
            match = regex.match(url)
            if match != None:
                try:
                    # product_id = match['rank']
                    product_id = match['product_id']
                except:
                    pass
        return product_id

    final_page_links = [x for x in new_links if extract_product_id_from_url(x)]
    final_page_links = [x for x in final_page_links if "#customerReviews" not in x]


    def get_product_rank(url):
        regex_options = [
            # r"https://www.amazon.com/gp/product/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
            #         r"https://www.amazon.com/dp/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
            #         r"https://www.amazon.com/(?P<slug>[\w-]+)/dp/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
            #          r"https://www.amazon.co.uk/gp/product/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
            # r"https://www.amazon.co.uk/dp/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
            r"https://www.amazon.co.uk/(?P<slug>[\w-]+)/dp/(?P<product_id>[\w-]+)/(?P<rank>[^&?]*?=[^&?]*)",
        ]
        rank_str = None
        for regex_str in regex_options:
            regex = re.compile(regex_str)
            match = regex.match(url)
            rank_str = match['rank']
            return rank_str

    def get_product_url_and_rank(final_page_links):
        data = []
        for url in final_page_links:
            split_fSlash = get_product_rank(url)
            split_userscore = split_fSlash.split('_')[2]
            #         spilit_slash = split_userscore.split('/')[0]
            data.append({'url': url, 'rank': split_userscore})
        return data

    data= get_product_url_and_rank(final_page_links)
    asin_number = asin

    def find_product_rank(asin_number, data):
        rank_data = None
        for d in data:
            if asin_number in d['url']:
                rank_data = {'rank': d['rank'], 'url': d['url']}
            else:
                range_data = {'rank': d['rank'], 'url': d['url']}
        if rank_data == None:
            return "Not Available"
        else:
            return rank_data
    driver.quit()
    return find_product_rank(asin_number, data)



# #print(track("pillow protector", 'B07GKYSHB4'))
print(track('pillows protector', 'B07GKYSHB4'))