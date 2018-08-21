# Wordnet module for verifying features relations
from textblob.wordnet import Synset

class Feature:
    def __init__(self, feature_name):
        if not (isinstance(feature_name, str)):
            raise ValueError('The first argument must be a string')
        self.name = feature_name.lower()

        # self.frequencies stores how many times the feature appears in each
        # document divided bt the total quantity of words (term frequencies)
        self.frequencies = []


    def add_frequency(self, frequency):
        self.frequencies.append(frequency)

    # TODO: add method get_tf

class MainFeature(Feature):
    def __init__(self, feature_name):
        super().__init__(feature_name)

    def __repr__(self):
        return '<Main Feature Name: %s>' % (self.name)

    def __str__(self):
        return '<Main Feature Name: %s>' % (self.name)

class GeneralFeature(Feature):
    def __init__(self, feature_name, feature_synset):
        super().__init__(feature_name)

        self.synset = None
        if isinstance(feature_synset, str):
            self.synset = Synset(feature_synset)

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

    def increase_doc_count(self):
        self.doc_count += 1

    def get_idf(self, total_count):
        return math.log(total_count/self.doc_count)

    # TODO: add method get_tf_idf

    # TODO: add method semantic weight
