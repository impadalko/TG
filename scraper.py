# General modules
import json
import re

# Browser helper
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# HTML parser
from bs4 import BeautifulSoup

# Command line options parser
from optparse import OptionParser

def main():
    # Get executions parameters
    parser = OptionParser()
    parser.add_option('-f', '--file', action='store', type='string', dest='output_file',
            default='data/output.json', help='Define the name of file where the ' +
            'scraped data will be stored. Default: %default')
    parser.add_option('-n', action='store', type='int', dest='number_of_pages',
            default=1, help='Define the number of pages to be scraped. Default: ' +
            '%default')
    (options, args) = parser.parse_args()

    # Define URL to be scraped: the implementation of this web scraper is website
    # dependent as we have a very specific objective and this should be hardcoded.
    base_url = 'https://www.ncbi.nlm.nih.gov'
    url = base_url + '/pubmed/?term=cancer'

    # Create a new Firefox headless session
    f_options = Options()
    f_options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=f_options)
    driver.implicitly_wait(30)
    driver.get(url)

    # Change to sort by best match
    driver.find_element_by_css_selector('.relevancead_sort').click()

    # 'Article' is defined as a set as there must be no repetition of links. In
    # the case of repetition, we would have: slower performance (increase of
    # requests) and a bigger influence of some articles over others.
    articles = set()

    print('Start reading website pages')
    for i in range(options.number_of_pages):
        print('Reading page', i+1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Find all the links for articles in the page
        for link in soup.find_all('a', href=re.compile('^/pubmed/[0-9]+')):
            articles.add(base_url + link['href'])
        # Go to next page
        driver.find_element_by_css_selector('.active.page_link.next').click()

    print('Found', len(articles), 'articles')

    print('Start processing articles')
    parsed = []
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
    output_file = open(options.output_file, 'w')
    output_file.write(json.dumps(parsed, sort_keys=True, indent=4))
    output_file.close()

    # Closes the session
    driver.quit()

if __name__ == '__main__':
    main()
