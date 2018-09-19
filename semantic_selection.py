# General modules
import json
import math
import re

# Command line options parser
from optparse import OptionParser

# Feature classes
from feature import GeneralFeature, MainFeature

# Main routine
def main():
    # Get executions parameters
    parser = OptionParser()
    parser.add_option('-f', '--file', action='store', type='string', dest='input_file',
            default='data/output.json', help='Define the name of file where the ' +
            'scraped data is stored. Default: %default')
    (options, args) = parser.parse_args()

    # Opens input file
    input_file = open(options.input_file, 'r')
    data = json.loads(input_file.read())

    # These words are blacklisted as they are too common in the english language
    # and, in the context of this algorithm, carry no meaning (stop words)
    blacklist = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for',
            'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such',
            'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this',
            'to', 'was', 'will', 'with']

    main = MainFeature('cancer')

    # TODO: Add all features
    features = [GeneralFeature('sex'), GeneralFeature('age'), GeneralFeature('race'),
            GeneralFeature('education level'), GeneralFeature('family cancer'),
            GeneralFeature('alcohol'), GeneralFeature('smoking'), GeneralFeature('tobacco'),
            GeneralFeature('address'), GeneralFeature('date first screening'),
            GeneralFeature('tumor location'), GeneralFeature('laterality'),
            GeneralFeature('multiple tumors'), GeneralFeature('tnm'),
            GeneralFeature('stage diagnosis'), GeneralFeature('reason non treatment'),
            GeneralFeature('date diagnosis'), GeneralFeature('treatment outcome'),
            GeneralFeature('date start treatment'), GeneralFeature('main treatment'),
            GeneralFeature('occupation'), GeneralFeature('time death')]

    # Iterate over all articles to calculate all the term frequencies and
    # document frequencies
    for article in data:
        d = {}
        # Clean up article data
        for key in article:
            # Remove all chars that are not letters or spaces
            regex = re.compile('[^a-zA-Z\s]')
            article[key] = regex.sub('', article[key]).lower()
            # Splits the string into a list
            article[key] = re.split('\s+', article[key])
            # Remove blacklisted words
            article[key] = [word for word in article[key] if word not in blacklist]
            d[key] = main.calculate_tf(article[key])

        main.add_frequency(d)

        # Iterate on all features
        for feature in features:
            d = {}
            for key in article:
                d[key] = feature.calculate_tf(article[key])
            # If at least one value in the dict is not zero, the feature is
            # present in the document
            if any(value != 0 for value in d.values()):
                feature.increase_doc_count()
            feature.add_frequency(d)

    weights = []
    norm = 0
    for feature in features:
        d = {}
        d["name"] = " ".join(feature.name)
        d["weight"] = feature.semantic_weight(len(data), main)
        norm += d["weight"]*d["weight"]
        weights.append(d)

    norm = math.sqrt(norm)

    for feature in weights:
        print(feature["name"], feature["weight"], feature["weight"]/norm)

if __name__ == '__main__':
    main()
