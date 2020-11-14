from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import difflib
from  selenium.common import exceptions

options = Options()
options.add_argument("--headless")

def googleSearch(query):

    # specifing browser web driver
    driver = webdriver.Chrome(chrome_options=options, executable_path='chromedriver')
    
    # search query
    search_engine = "https://www.google.com/search?q="
    query = query.replace(" ","+")
    
    # driver.get will open browser and enter the string we provide as argument
    driver.get(search_engine + query + "&start=" + "0")

    # all the needed data will be stored here 
    # which will be returned by this function
    data = {}
    
    # number of search reasult count of first page
    # cuz generally per page results are around 10-15

    s_len = 15
    
    for s_block in range(s_len):
        #  try to handle error 
        # if element based on xpath is not found ,
        # continue through the loop
        
        try:
            # store data collected of each s_block to block {}
            block = {}


            # find url of content
            xpath_url = f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a"""
            url = driver.find_element_by_xpath(xpath_url)
            url = url.get_attribute('href')
            
            # find domain name of web having content
            pattern =  r"""(https?:\/\/)?(([a-z0-9-_]+\.)?([a-z0-9-_]+\.[a-z0-9-_]+))"""
            domain = re.search(pattern, url)[0]


            # find title of content
            xpath_title = f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a/h3/span"""
            title = driver.find_element_by_xpath(xpath_title)
            title = title.get_attribute("innerText")
            
            # find description of content
            xpath_description = f"""//*[@id="rso"]/div[{s_block}]/div/div[2]/div/span"""
            description = driver.find_element_by_xpath(xpath_description)
            description = description.get_attribute("innerText")
            
            # save all data to block {}
            block["domain"] = domain
            block["url"] = url
            block["title"] = title
            block["description"] = description

            # save block dictionary to main dictionary
            data[f'{s_block}'] = block
        
        except exceptions.NoSuchElementException:
            continue

    driver.close()
    return data


def compareStr(str1,str2):
    
    # difflib.SequenceMatcher will compare 2 argument strings
    # and show us in form of float number between 0-1
    # 0 means no match , 1 means full match

    # multiplying result to 100 so it kinda looks like 0-100% based result
    return difflib.SequenceMatcher(None, f"""{str1}""", f"""{str2}""").ratio() * 100
