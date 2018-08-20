import json
import re
import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

def main():
    # Define URL to be scraped: the implementation of this web scraper is website
    # dependent as we have a very specific objective and this should be hardcoded.
    base_url = 'https://www.ncbi.nlm.nih.gov'
    url = base_url + '/pubmed/?term=cancer'

    # Fails if wrong arguments are passed
    # TODO: make this better: make the name of the file optional and add a help
    if len(sys.argv) != 3:
        print('This script requires exactly two arguments: the first being an ' +
                'integer representing the number of pages to be scraped and the ' +
                'second being the path of the output json file')
        sys.exit(1)

    # Create a new Firefox headless session
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.implicitly_wait(30)
    driver.get(url)

    # Change to sort by best match
    driver.find_element_by_css_selector('.relevancead_sort').click()

    # Article is defined as a set as there must be no repetition of links. In the
    # case of repetition, we would have: slower performance (increase of requests)
    # and a bigger influence of some articles over others.
    articles = set()

    number_of_pages = int(sys.argv[1])
    print('Start reading website pages')
    for i in range(number_of_pages):
        print('Reading page', i+1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Find all the links for articles in the page
        for link in soup.find_all('a', href=re.compile("^/pubmed/[0-9]+")):
            articles.add(base_url + link['href'])
        # Go to next page
        driver.find_element_by_css_selector('.active.page_link.next').click()

    print('Found', len(articles), 'articles')

    parsed = []
    print('Start processing articles')
    i = 1
    ignored = 0
    # Iterate over the chosen articles
    for article in articles:
        print('Reading article', i, '-', article)
        driver.get(article)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Search the page for the desired infomation
        title = soup.find_all('h1')[1].text
        abstract = soup.find('div', class_='abstr')
        # Ignore articles without abstract
        if abstract == None:
            ignored += 1
            continue
        abstract = abstract.text[8:]
        # Not all available articles have keywords
        keywords = soup.find('div', class_='keywords')
        if keywords != None:
            keywords = keywords.text[10:]
            parsed.append({'title': title, 'abstract': abstract, 'keywords': keywords})
        else:
            parsed.append({'title': title, 'abstract': abstract})
        i += 1

    print('Ignored', ignored, 'articles')

    # Write results to an external file
    print('Write results to output file')
    output_file = open(sys.argv[2], 'w')
    output_file.write(json.dumps(parsed, sort_keys=True, indent=4))
    output_file.close()

    # Closes the session
    driver.quit()

if __name__ == "__main__":
    main()
