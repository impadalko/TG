# General modules
import json
import math
import re

# Command line options parser
from optparse import OptionParser

# Feature classes
from feature import GeneralFeature, MainFeature


def similar_features(features, threshold):
    selected_features = []
    for feature in features:
        for selected_feature in selected_features:
            # We use path similarity because we are looking for hypernyms
            if feature.path_similarity(selected_feature) > threshold:
                break
        else:
            # If no similar enough feature is found among the already selected
            # ones, add the current synset to the current one
            selected_features.append(feature)
    return selected_features


# Main routine
def main():
    # Get executions parameters
    parser = OptionParser()
    parser.add_option('-f', '--file', action='store', type='string', dest='input_file',
            default='data/output.json', help='Define the name of file where the ' +
            'scraped data is stored. Default: %default')
    (options, args) = parser.parse_args()

    # TODO: hypernims stuff (add a file with the features?)

    # Opens input file
    input_file = open(options.input_file, 'r')
    data = json.loads(input_file.read())

    # These words are blacklisted as they are too common in the english language
    # and, in the context of this algorithm, carry no meaning (stop words)
    blacklist = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for',
            'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such',
            'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this',
            'to', 'was', 'will', 'with']

    # Add all features (cancer should be treated separately though)
    features = [MainFeature('cancer')]

    # TODO: Add ids to the articles? Not sure if needed in the case there is no
    # reference to the feature in the text

    # Iterate over all articles
    for article in data:
        # Clean up article data
        for key in article:
            # Remove all chars that are not letters or spaces
            regex = re.compile('[^a-zA-Z\s]')
            article[key] = regex.sub('', article[key]).lower()
            # Splits the string into a list
            article[key] = re.split('\s+', article[key])
            # Remove blacklisted words
            article[key] = [word for word in article[key] if word not in blacklist]

        # Iterate on all features
        for feature in features:
            d = {}
            for key in article:
                # Count frequencies on each key of this article
                d[key] = article[key].count(feature.name)/len(article[key])
            feature.add_frequency(d)


    # TODO: Remove this print
    print(features[0].frequencies)


if __name__ == '__main__':
    main()
