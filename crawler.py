import json
import re

from selenium import webdriver
from bs4 import BeautifulSoup

base_url = 'https://www.ncbi.nlm.nih.gov'
url = base_url + '/pubmed/?term=cancer'

# Create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

# Change to sort by best match
driver.find_element_by_css_selector('.relevancead_sort').click()

number_of_pages = 1
articles = set()
for i in range(number_of_pages):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.find_all('a', href=re.compile("^/pubmed/[0-9]+")):
        articles.add(base_url + link['href'])
    # Go to next page
    driver.find_element_by_css_selector('.active.page_link.next').click()

out = []
# Iterate over the chosen articles
for article in articles:
    driver.get(article)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find_all('h1')[1].text
    abstract = soup.find_all('div', class_='abstr')[0].text[8:]
    keywords = soup.find('div', class_='keywords')
    if keywords != None:
        keywords = keywords.text[10:]
    out.append({'title': title, 'abstract': abstract, 'keywords': keywords})

print(json.dumps(out))

driver.quit()
