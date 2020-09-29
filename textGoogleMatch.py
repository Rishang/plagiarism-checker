from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import difflib
from  selenium.common import exceptions

options = Options()
options.headless = True

def search(query):
    driver = webdriver.Chrome('chromedriver')

    search_engine = "https://www.google.com/search?q="
    query = query.replace(" ","+")
    driver.get(search_engine + query + "&start=" + "0")

    data = {}
    s_len = len(driver.find_elements_by_class_name('g')) + 2
    
    for s_block in range(s_len):
        try:
            # store data collected of each s_block to block {}
            block = {}

            # domain name of web having content
            domain_p = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a/div/cite""")
            domain_p = domain_p.get_attribute('innerText')
            pattern =  r"""(https?:\/\/)?(([a-z0-9-_]+\.)?([a-z0-9-_]+\.[a-z0-9-_]+))"""
            domain = re.search(pattern, domain_p)[0]
            block["domain"] = domain

            # url of content
            url = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a""")
            url = url.get_attribute('href')
            block["url"] = url

            # title of content
            title = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[1]/a/h3/span""")
            title = title.get_attribute("innerText")
            block["title"] = title
            
            # description of content
            description = driver.find_element_by_xpath(f"""//*[@id="rso"]/div[{s_block}]/div/div[2]/div/span""")
            description = description.get_attribute("innerText")
            block["description"] = description

            # save block dictionary to main dictionary
            data[f'{s_block}'] = block
        
        except exceptions.NoSuchElementException:
            continue

    driver.close()
    return data


def compareSentence(str1,str2):
    
    return difflib.SequenceMatcher(None, f"""{str1}""", f"""{str2}""").ratio() * 100
