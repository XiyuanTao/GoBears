from datetime import date

import requests
import time
import re
#from PIL import Image
#from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import openpyxl
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree, html
from datetime import datetime
import csv
import numpy

def change_address(postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
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

def parse_list(page_source, current_url,num_pages,category,allurls):
    order_in_page = 1
    search_result = []

    html = etree.HTML(page_source)
    trs = html.xpath('//div[@data-component-type="s-search-result"]')
    for tr in trs:
        good_info = []
        # URL
        href = tr.xpath(".//a[@class = 'a-link-normal s-no-outline']/@href")[0]
        # print(len(href))
        fullurl = 'http://amazon.com' + href
        print('获得商品详情页', fullurl)

        # ASIN
        asin = re.search('(?<=(dp/))(.+?){10}', fullurl)[0] if re.search('(?<=(dp/))(.+?){10}', fullurl) else \
        re.search('(?<=(dp%2F))(.+?){10}', fullurl)[0]

        # TITLE



        title = tr.xpath('.//span[contains(@class,"a-size-base-plus a-color-base a-text-normal")]/text()')[0] if tr.xpath('.//span[contains(@class,"a-size-base-plus a-color-base a-text-normal")]/text()') else tr.xpath('.//span[@class = "a-size-medium a-color-base a-text-normal"]/text()')[0]

        # PRICE
        price = tr.xpath('.//span[@class="a-price"]/span[@class="a-offscreen"]/text()')[0].replace(',', '').replace('$',
                                                                                                                    '') if tr.xpath(
            './/span[@class="a-price"]/span[@class="a-offscreen"]/text()') else 'NOPRICE'

        # ORIGINAL_PRICE
        original_price = tr.xpath('.//span[@class="a-price a-text-price"]/span[contains(@class,"a-offscreen")]/text()')[
            0].replace(',', '').replace('$', '') if tr.xpath(
            './/span[@class="a-price a-text-price"]/span[contains(@class,"a-offscreen")]/text()') else 0

        # SPECIFICATION
        specification = tr.xpath('.//span[contains(@class,"a-text-bold")]/text()')[0] if tr.xpath(
            './/span[contains(@class,"a-text-bold")]/text()') else 0

        # PRICE_OF_SPECIFICATION
        price_of_sepcification = tr.xpath('.//span[contains(@class,"a-size-base a-color-secondary")]/text()')[
            0] if tr.xpath('.//span[contains(@class,"a-size-base a-color-secondary")]/text()') else 0

        # RATING_OUT_OF_5_STARS
        rating_5 = tr.xpath('.//span[contains(@class,"a-icon-alt")]/text()')[0].split(" ")[0].replace(",",
                                                                                                      ".") if tr.xpath(
            './/span[contains(@class,"a-icon-alt")]/text()') else 0

        # RATINGS_NUM
        ratings_num = tr.xpath('.//div[@class="a-row a-size-small"]/span[2]/@aria-label')[
            0].replace(",", "") if tr.xpath('.//div[@class="a-row a-size-small"]/span[2]/@aria-label')  else 0

        # ratings_num = tr.xpath('.//span[@class="a-size-base a-color-base s-underline-text"]/text()')[
        #     0].replace(",", "") if tr.xpath('.//span[@class="a-size-base a-color-base s-underline-text"]/text()') else 0

        # SPONSORED
        sponsored = 1 if tr.xpath(
            './/a[@class = "s-label-popover s-sponsored-label-text"]//span[@class="a-color-base"]/text()') else 0

        # SUBSCRIBE
        subscribe = tr.xpath(
            './/div[@class="a-section a-spacing-none a-spacing-top-small s-price-instructions-style"]/div[contains(@class,"a-row a-size-base a-color-secondary")]//span[1]/text()')[
            0] if tr.xpath(
            './/div[@class="a-section a-spacing-none a-spacing-top-small s-price-instructions-style"]/div[contains(@class,"a-row a-size-base a-color-secondary")]//span[1]/text()') else 0

        # PRIME
        prime = 1 if tr.xpath('.//div[contains(@class,"a-row s-align-children-center")]/span[2]/span[1]/text()') else 0

        # DELIVERY_TIME
        delivery_time = tr.xpath('.//div[contains(@class,"a-row s-align-children-center")]/span[2]/span[2]/text()')[
            0] if tr.xpath('.//div[contains(@class,"a-row s-align-children-center")]/span[2]/span[2]/text()') else 0

        # FREE_SHIPPING
        free_shipping = 1 if tr.xpath(
            './/div[contains(@class,"a-row a-size-base a-color-secondary s-align-children-center")]/div[2]/span[1]/span[1]/text()') else 0

        # COUPON
        coupons = tr.xpath('.//span[@class="s-coupon-unclipped"]//text()') if tr.xpath('.//span[@class="s-coupon-unclipped"]//text()') else '0'
        coupon = "".join([each for each in coupons])

        # JUST_SAVE
        just_save_in_red = tr.xpath('.//span[@class="a-badge-text" and contains(text(),"Save")]/text()')[0].split(" ")[1] if tr.xpath('.//span[@class="a-badge-text" and contains(text(),"Save")]/text()') else 0

        # BEST_SELLER
        best_sell = 1 if tr.xpath('.//span[@class="a-badge-text" and contains(text(),"Best")]') else 0

        # AMAZON'S CHOICE
        amazon_choice = 1 if tr.xpath('.//span[contains(@id,"amazons-choice")]') else 0

        # Limited time deal
        limited_time_deal = 1 if tr.xpath('.//span[@class="a-badge-text" and contains(text(),"Limited")]') else 0

        # amazon brand
        amazon_brand = 1 if tr.xpath(
            './/span[@class="a-size-micro a-color-secondary" and contains(text(),"Featured from our brands")]') else 0

        # ORDER_IN_PAGE
        now_order = order_in_page
        order_in_page += 1

        # TIME
        time_year = datetime.today().year
        time_month = datetime.today().month
        time_day = datetime.today().day
        time = datetime.today()

        #allurls.append([fullurl,category,num_pages,order_in_page])
        allurls.append(fullurl)
        good_info.append(asin)
        good_info.append(time_year)
        good_info.append(time_month)
        good_info.append(time_day)
        good_info.append(category)
        good_info.append(num_pages)
        good_info.append(now_order)
        good_info.append(ratings_num)
        good_info.append(rating_5)
        good_info.append(price)
        good_info.append(original_price)
        good_info.append(sponsored)
        good_info.append(prime)
        good_info.append(free_shipping)
        good_info.append(just_save_in_red)
        good_info.append(amazon_brand)
        good_info.append(best_sell)
        good_info.append(amazon_choice)
        good_info.append(limited_time_deal)
        good_info.append(subscribe)
        good_info.append(coupon)
        good_info.append(specification)
        good_info.append(delivery_time)
        good_info.append(price_of_sepcification)
        good_info.append(title)
        good_info.append(fullurl)
        good_info.append(time)
        with open('search_result.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(good_info)


        search_result.append(good_info)

    # yield fullurl
    return allurls

def parse_detail(page_source):
    html = etree.HTML(page_source)
    attr_list = []
    fullurl = driver.current_url
    asin = re.search('(?<=(dp/))(.+?){10}', fullurl)[0] if re.search('(?<=(dp/))(.+?){10}', fullurl) else \
        re.search('(?<=(dp%2F))(.+?){10}', fullurl)[0]

    # TIME
    time_year = datetime.today().year
    time_month = datetime.today().month
    time_day = datetime.today().day
    time = datetime.today()

    # RATING_DISTRIBUTION
    rating_dist = []
    star_5 = \
    html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[1]/td[3]/span[2]/a[1]/text()')[0] if html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[1]/td[3]/span[2]/a[1]/text()') else '0'
    star_4 = \
    html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[2]/td[3]/span[2]/a[1]/text()')[0] if html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[2]/td[3]/span[2]/a[1]/text()') else '0'
    star_3 = \
    html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[3]/td[3]/span[2]/a[1]/text()')[0] if html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[3]/td[3]/span[2]/a[1]/text()') else '0'
    star_2 = \
    html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[4]/td[3]/span[2]/a[1]/text()')[0] if html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[4]/td[3]/span[2]/a[1]/text()') else '0'
    star_1 = \
    html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[5]/td[3]/span[2]/a[1]/text()')[0] if html.xpath('//table[@class="a-normal a-align-center a-spacing-base"]/tbody[1]/tr[5]/td[3]/span[2]/a[1]/text()') else '0'
    star_avg = html.xpath('//span[@class="a-size-medium a-color-base"]/text()')[0].split(" ")[0] if html.xpath('//span[@class="a-size-medium a-color-base"]/text()') else '0'
    rating_dist.append(asin)
    star_5 = re.sub(u"([^\u0030-\u0039])", "", star_5)
    star_4 = re.sub(u"([^\u0030-\u0039])", "", star_4)
    star_3 = re.sub(u"([^\u0030-\u0039])", "", star_3)
    star_2 = re.sub(u"([^\u0030-\u0039])", "", star_2)
    star_1 = re.sub(u"([^\u0030-\u0039])", "", star_1)
    star_avg = star_avg.replace(",", "")


    rating_dist.append(time_year)
    rating_dist.append(time_month)
    rating_dist.append(time_day)

    rating_dist.append(star_5)
    rating_dist.append(star_4)
    rating_dist.append(star_3)
    rating_dist.append(star_2)
    rating_dist.append(star_1)
    rating_dist.append(star_avg)
    rating_dist.append(time)

    with open('rating_distribution.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(rating_dist)
    rating_dist = []

    #BY_FEATURE
    by_feature = []
    trs=html.xpath('//div[@id="cr-summarization-attributes-list"]//div[@class="a-section a-spacing-none"]')
    i=1
    for tr in trs:
        by_feature.append(asin)
        by_feature.append(time_year)
        by_feature.append(time_month)
        by_feature.append(time_day)
        by_feature.append(i)
        i += 1
        feature = tr.xpath('.//span[@class="a-size-base a-color-base"]/text()')[0]
        star = tr.xpath('.//span[@class="a-size-base a-color-tertiary"]/text()')[0]
        by_feature.append(feature)
        by_feature.append(star)
        by_feature.append(time)

        with open('by_feature.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(by_feature)
        by_feature = []


    # KEY_WORDS
    keyword = []
    trs = html.xpath('//span[@data-hook="lighthouse-term"]')
    keyword.append(asin)
    keyword.append(time_year)
    keyword.append(time_month)
    keyword.append(time_day)
    for tr in trs:
        keyword.append(tr.xpath('./text()')[0].replace('\r','').strip())
    keyword = list(numpy.array(keyword).flat)
    keyword.append(time)
    with open('key_words.csv', 'a', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keyword)
    keyword = []


    # REVIEW
    review = []
    trs = html.xpath('//div[@class="a-section review aok-relative"]') if html.xpath('//div[@class="a-section review aok-relative"]') else []
    i=1
    for tr in trs:
        title = tr.xpath('.//a[@data-hook="review-title"]/span/text()')[0] if tr.xpath(
            './/a[@data-hook="review-title"]/span/text()') else ''
        star = tr.xpath('.//span[@class="a-icon-alt"]/text()')[0] if tr.xpath(
            './/span[@class="a-icon-alt"]/text()') else ''
        helpful = tr.xpath('.//span[@data-hook="helpful-vote-statement"]/text()')[0] if tr.xpath(
            './/span[@data-hook="helpful-vote-statement"]/text()') else ''
        time_loc = tr.xpath('.//span[@data-hook="review-date"]/text()')[0] if tr.xpath(
            './/span[@data-hook="review-date"]/text()') else ''
        owner = tr.xpath('.//span[@class="a-profile-name"]/text()')[0] if tr.xpath(
            './/span[@class="a-profile-name"]/text()') else ''

        owner_titles = tr.xpath('.//div[@class="badges-genome-widget"]//text()') if tr.xpath(
            './/div[@class="badges-genome-widget"]//text()') else ''
        owner_title = "".join([each for each in owner_titles])

        verfied = tr.xpath('.//span[@data-hook="avp-badge-linkless"]/text()')[0] if tr.xpath(
            './/span[@data-hook="avp-badge-linkless"]/text()') else ''
        vine = tr.xpath('.//span[@data-hook="linkless-vine-review-badge"]/text()')[0] if tr.xpath(
            './/span[@data-hook="linkless-vine-review-badge"]/text()') else ''
        component = tr.xpath('.//span[@class="a-size-base review-text"]/div/div/span/text()')[0].replace('\n','').replace('\r','').strip() if tr.xpath(
            './/span[@class="a-size-base review-text"]/div/div/span/text()') else ''
        review.append(asin)
        review.append(time_year)
        review.append(time_month)
        review.append(time_day)
        review.append(i)
        i += 1
        review.append(title)
        review.append(star)
        review.append(helpful)
        review.append(time_loc)
        review.append(owner)
        review.append(owner_title)
        review.append(verfied)
        review.append(vine)
        review.append(component)
        review.append(time)
        with open('reviews.csv', 'a', newline='' , encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(review)
        review = []

    return attr_list

def Main_scraping(search_page_urls,use_postal,postal,num_pages,cate):
    #detail = []
    #cate = 0
    allurls = []
    for search_page_url in search_page_urls:
        if cate == 0:
            category = 'shampoo'
        elif cate == 1:
            category = 'body wash'
            #print("休眠600s")
            #time.sleep(1000)
        elif cate == 2:
            category = 'lipstick'
            #print("休眠600s")
            #time.sleep(1000)
        elif cate == 3:
            category = 'car camera'
            #print("休眠600s")
            #time.sleep(1000)


        for i in range(1, num_pages):
            #if i == 10: time.sleep(600)
            print("正在爬取", search_page_url.format(i))
            driver.get(search_page_url.format(i))
            time.sleep(2)

            if i == 1 and bool(use_postal):
                change_address(postal)

            time.sleep(2)
            js = "return action=document.body.scrollHeight"
            new_height = driver.execute_script(js)
            for k in range(0, new_height, 100):
                driver.execute_script('window.scrollTo(0, %s)' % (k))
            time.sleep(1)
            parse_list(driver.page_source, search_page_url.format(i), i, category,allurls)
            #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))
        cate+=1
    order = 1
    while allurls!=[]:
        if order%800 == 0:time.sleep(1000)

        item = allurls.pop(0)
        url = item
        try:
            js = 'window.open("' + url + '&language=en_US");'
            driver.execute_script(js)

            # 网页窗口句柄集
            handles = driver.window_handles
            # 进行网页窗口切换
            driver.switch_to.window(handles[-1])

            # 下划
            js = "return action=document.body.scrollHeight"
            new_height = driver.execute_script(js)
            # time.sleep(1)
            for i in range(0, new_height, 200):
                time.sleep(0.05)
                driver.execute_script('window.scrollTo(0, %s)' % (i))

            # 翻页
            info_list = parse_detail(driver.page_source)
            info_list.append(driver.current_url)

            time.sleep(1)

            asin_regex = re.compile('/dp/(.*?)/')
            asin = asin_regex.findall(driver.current_url)[0]
            print(asin,order)
            #info_list[0] = asin

            #print(info_list)
            #detail.append(info_list)

            driver.close()
            driver.switch_to.window(handles[0])
            order += 1
        except:
            #driver.close()
            allurls.append(item)


    #return detail

if __name__ == '__main__':
    #是否使用固定邮编
    use_postal = 0
    postal_berkeley = "94704"
    postal_nyc = '10027'
    #爬取每一品类商品列表的页面数
    num_pages = 21


    search_page_urls = ['https://www.amazon.com/s?k=Hair+Shampoo&i=beauty&rh=n%3A11057651&page={}',
                        'https://www.amazon.com/s?k=Body+Cleansers&i=beauty&rh=n%3A11056281&page={}',
                        'https://www.amazon.com/s?k=Lipstick&i=beauty&rh=n%3A11059111&page={}',
                        'https://www.amazon.com/s?k=Car+Video&i=car-electronics&rh=n%3A10980521&page={}']


    options = webdriver.ChromeOptions()
    option = webdriver.ChromeOptions()
    # linux服务器
    #options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('blink-settings=imagesEnabled=false')
    # 静默模式mj

    options.add_argument('--disable-gpu')
    options.add_argument("disable-web-security")
    options.add_argument('disable-infobars')
    #options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}  # 设置无图模式
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #driver = webdriver.Chrome('/usr/GoBears/chromedriver', chrome_options=options)

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    row = 2

    Main_scraping(search_page_urls, use_postal, postal_berkeley, num_pages, 0)
    driver.quit
    driver.quit

    print("全部结束")