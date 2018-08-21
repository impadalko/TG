# General modules
import json
import math
import re

# Wordnet module for verifying features relations
from textblob.wordnet import Synset

# Command line options parser
from optparse import OptionParser

class Feature:
    def __init__(self, feature_name, feature_synset):
        if not (isinstance(feature_name, str)):
            raise ValueError('The first argument must be a string')
        # TODO: Not all features can be associated with a synset => Make this
        # check and the synset attribute "optional"
        if not (isinstance(feature_synset, str)):
            raise ValueError('The second argument must be a string')
        self.name = feature_name.lower()
        self.synset = Synset(feature_synset)
        # self.frequencies stores how many times the feature appears in each
        # document divided bt the total quantity of words (term frequencies)
        # TODO: think about this: array of objects?
        self.frequencies = []
        # self.doc_count stores the amount of documents containing the feature
        self.doc_count = 0

    def __repr__(self):
        return '<Feature Name: %s; Synset: %s>' % (self.name, self.synset)

    def __str__(self):
        return '<Feature Name: %s; Synset: %s>' % (self.name, self.synset)

    # TODO: Verify if the other feature has a synset
    def path_similarity(self, feature):
        if not (isinstance(feature, Feature)):
            raise ValueError('The first argument must be a Feature')
        return self.synset.path_similarity(feature.synset)

    def add_frequency(self, frequency):
        self.frequencies.append(frequency)

    def increase_doc_count(self):
        self.doc_count += 1

    def get_idf(self, total_count):
        return math.log(total_count/self.doc_count)

    # TODO: add method get_tf_idf


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
    features = [Feature('cancer', 'cancer.n.01')]

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
            for key in article:
                # Count frequencies on each key of this article
                feature.add_frequency(article[key].count(feature.name)/len(article[key]))

if __name__ == '__main__':
    main()
