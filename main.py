from datetime import date

import requests
import time
import re
from PIL import Image
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import openpyxl
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By





def change_address(postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
            # driver.find_element_by_id('nav-global-location-slot').click()
            time.sleep(2)
        except Exception as e:
            driver.refresh()
            time.sleep(10)
            continue
        try:
            driver.find_element_by_id("GLUXChangePostalCodeLink").click()
            time.sleep(2)
        except:
            pass
        try:
            driver.find_element_by_id('GLUXZipUpdateInput').send_keys(postal)
            time.sleep(1)
            break
        except Exception as NoSuchElementException:
            try:
                driver.find_element_by_id('GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(1)
                driver.find_element_by_id('GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(1)
                break
            except Exception as NoSuchElementException:
                driver.refresh()
                time.sleep(10)
                continue
        print("重新选择地址")
    driver.find_element_by_id('GLUXZipUpdate').click()
    time.sleep(1)
    driver.refresh()
    time.sleep(3)

def parse_list(page_source, current_url):
    html = pq(page_source)
    url_front = current_url.split("/s")[0]
    item_urls = html("h2 > a.a-link-normal.a-text-normal").items()

    for s in item_urls:
        url = url_front + s.attr("href")
        yield url

def parse_detail(page_source):
    html = pq(page_source)
    attr_list = []

    # 商品标题
    title = html("span#productTitle").text()

    # 详细描述
    li_list = html("ul.a-unordered-list.a-vertical.a-spacing-none li").items()
    li_text_list = []
    for li in li_list:
        li_text_list.append(li.text().strip())

    # 主图
    # z_img = html("img#landingImage").attr("data-old-hires")
    # if z_img == "":
    #     z_img = html("img#landingImage").attr("src")

    # 价格
    price = html('span[id*="priceblock"]').text().replace('\xa0', '')

    # 评论数
    review_num = ""
    review_num_list = html("#acrCustomerReviewText").items()
    for rn in review_num_list:
        review_num = rn.text()
        break
    if review_num != "":
        review_num = review_num.split(" ")[0]

    # 得分
    score = html("span[data-hook=rating-out-of-text]").text()
    if score == "":
        try:
            score = list(html("#acrPopover > span.a-declarative > a span").items())[0].text()
        except Exception as e:
            score = ""
    if score != "":
        score = score.split(" ")[0].replace(",", ".")

    asin = ''
    attr_list.append(asin)
    #attr_list.append(z_img)
    attr_list.append(title)
    attr_list.append(price)
    attr_list.append(score)
    attr_list.append(int(review_num.strip().replace(',', '')) if review_num else 0)

    return attr_list

# def list_scraping(search_page_urls,use_postal,postal,num_pages):
#     for search_page_url in search_page_urls:


def datail_scraping(search_page_urls,use_postal,postal,num_pages):
    detail = []
    for search_page_url in search_page_urls:
        for i in range(1, num_pages):
            print("正在爬取", search_page_url.format(i))
            driver.get(search_page_url.format(i))
            time.sleep(2)

            if i == 1 and bool(use_postal):
                change_address(postal)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))

            for url in parse_list(driver.page_source, search_page_url.format(i)):
                js = 'window.open("' + url + '&language=en_US");'
                driver.execute_script(js)

                # 网页窗口句柄集
                handles = driver.window_handles
                # 进行网页窗口切换
                driver.switch_to.window(handles[-1])

                page_source = driver.page_source
                info_list = parse_detail(driver.page_source)
                info_list.append(driver.current_url)

                time.sleep(2)

                asin_regex = re.compile('/dp/(.*?)/')
                asin = asin_regex.findall(driver.current_url)[0]
                info_list[0] = asin

                print(info_list)
                detail.append(info_list)

                driver.close()
                driver.switch_to.window(handles[0])
    return detail

if __name__ == '__main__':
    #是否使用固定邮编
    use_postal = 0
    postal = "94704"
    #爬取每一品类商品列表的页面数
    num_pages = 5
    #需要爬取的搜索页面链接：
    # search_page_urls =['https://www.amazon.com/b?node=11057651&page={}',
    #                    'https://www.amazon.com/b?node=11056281&page={}',
    #                    'https://www.amazon.com/b?node=11059111&page={}',
    #                    'https://www.amazon.com/b?node=10980521&page={}',
    #                    'https://www.amazon.com/b?node=898400&page={}']

    search_page_urls = ['https://www.amazon.com/s?k=shampoo&crid=3HRLZHDGH8FVG&sprefix=shampo%2Caps%2C669&ref=nb_sb_noss_2&page={}',
                        'https://www.amazon.com/s?k=Body+wash&crid=A4U5UM80BRMO&sprefix=body+wash%2Caps%2C396&ref=nb_sb_noss&page={}',
                        'https://www.amazon.com/s?k=Lipsticks&crid=156DT8FY808PV&sprefix=lipsticks%2Caps%2C400&ref=nb_sb_noss&page={}',
                        'https://www.amazon.com/s?k=Car+camera&crid=1M80O16SRJBK0&sprefix=lipsticks%2Caps%2C363&ref=nb_sb_noss&page={}',
                        'https://www.amazon.com/s?k=Security+camera&crid=22KBIIU7EP084&sprefix=car+camera%2Caps%2C401&ref=nb_sb_noss&page={}']

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument("disable-web-security")
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    wait = WebDriverWait(driver, 20)

    driver.maximize_window()
    row = 2

    #list_scraping(search_page_urls,use_postal,postal,num_pages)
    detail = datail_scraping(search_page_urls,use_postal,postal,num_pages)
    print('this is detail')
    print("爬取结束")

