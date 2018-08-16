import json
import re
import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

base_url = 'https://www.ncbi.nlm.nih.gov'
url = base_url + '/pubmed/?term=cancer'

if len(sys.argv) < 2:
    print('This script requires one argument: an integer representing the number' +
            'of pages to be scraped')
    sys.exit(1)

# Create a new Firefox headless session
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
driver.implicitly_wait(30)
driver.get(url)

# Change to sort by best match
driver.find_element_by_css_selector('.relevancead_sort').click()

number_of_pages = int(sys.argv[1])

articles = set()
for i in range(number_of_pages):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.find_all('a', href=re.compile("^/pubmed/[0-9]+")):
        articles.add(base_url + link['href'])
    # Go to next page
    driver.find_element_by_css_selector('.active.page_link.next').click()

parsed = []
# Iterate over the chosen articles
for article in articles:
    driver.get(article)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Search the page for the desired infomation
    title = soup.find_all('h1')[1].text
    abstract = soup.find_all('div', class_='abstr')[0].text[8:]
    keywords = soup.find('div', class_='keywords')
    # Not all articles available have keywords
    if keywords != None:
        keywords = keywords.text[10:]
        parsed.append({'title': title, 'abstract': abstract, 'keywords': keywords})
    else:
        parsed.append({'title': title, 'abstract': abstract})

# Write results to an external file
output_file = open('articles.json', 'w')
output_file.write(json.dumps(parsed, sort_keys=True, indent=4))
output_file.close()

# Closes the session
driver.quit()
