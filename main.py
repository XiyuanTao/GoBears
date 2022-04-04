# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
 try:
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        wait = WebDriverWait(driver, 20)
        driver.maximize_window()
        row = 2
        search_page_urls = ['https://www.amazon.com/s?k=Hair+Shampoo&i=beauty&rh=n%3A11057651&page={}']
        datail_scraping(search_page_urls, use_postal, postal_berkeley, num_pages,0)
        #driver.quit
        #driver.quit
        print("shampoo爬取结束")
    except:
        driver.quit
        driver.quit
        print("出现错误，重试")
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        wait = WebDriverWait(driver, 20)
        driver.maximize_window()
        row = 2
        search_page_urls = ['https://www.amazon.com/s?k=Hair+Shampoo&i=beauty&rh=n%3A11057651&page={}']
        datail_scraping(search_page_urls, use_postal, postal_berkeley, num_pages,0)
        driver.quit
        driver.quit
        print("重试后shampoo爬取结束")

    try:
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        wait = WebDriverWait(driver, 20)
        driver.maximize_window()
        row = 2
        search_page_urls = ['https://www.amazon.com/s?k=Body+Cleansers&i=beauty&rh=n%3A11056281&page={}']
        datail_scraping(search_page_urls, use_postal, postal_berkeley, num_pages,1)
        driver.quit
        driver.quit
        print("body cleanser爬取结束")
    except:
        driver.quit
        driver.quit
        print("出现错误，重试")
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        wait = WebDriverWait(driver, 20)
        driver.maximize_window()
        row = 2
        search_page_urls = ['https://www.amazon.com/s?k=Body+Cleansers&i=beauty&rh=n%3A11056281&page={}']
        datail_scraping(search_page_urls, use_postal, postal_berkeley, num_pages,1)
        driver.quit
        driver.quit
        print("重试后body cleanser爬取结束")