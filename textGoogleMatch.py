from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import difflib
from  selenium.common import exceptions

options = Options()
options.headless = True

def googleSearch(query):

    # specifing browser web driver
    driver = webdriver.Chrome('chromedriver')
    
    # search query
    search_engine = "https://www.google.com/search?q="
    query = query.replace(" ","+")
    
    # driver.get will open browser and enter the string we provide as argument
    driver.get(search_engine + query + "&start=" + "0")

    # all the needed data will be stored here 
    # which will be returned by this function
    data = {}
    
    s_len = len(driver.find_elements_by_class_name('g')) + 2
    
    for s_block in range(s_len):
        try:
            # store data collected of each s_block to block {}
            block = {}

            # find domain name of web having content
            domain_p = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a/div/cite""")
            domain_p = domain_p.get_attribute('innerText')
            
            # regex pattern for selectiong domain name
            pattern =  r"""(https?:\/\/)?(([a-z0-9-_]+\.)?([a-z0-9-_]+\.[a-z0-9-_]+))"""
            domain = re.search(pattern, domain_p)[0]

            # find url of content
            url = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a""")
            url = url.get_attribute('href')            

            # find title of content
            title = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a/h3/span""")
            title = title.get_attribute("innerText")
            
            # find description of content
            description = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[2]/div/span""")
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