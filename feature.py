# General imports
import math

# Wordnet module for verifying features relations
from textblob.wordnet import Synset

class Feature:
    def __init__(self, feature_name):
        self.name = feature_name.lower()

        # self.frequencies stores how many times the feature appears in each
        # document divided bt the total quantity of words (term frequencies)
        self.frequencies = []

    def add_frequency(self, frequency):
        self.frequencies.append(frequency)

    def get_tf(self):
        return self.frequencies

class MainFeature(Feature):
    def __init__(self, feature_name):
        super().__init__(feature_name)
        self.total_df = {}

    def get_total_tf(self):
        # Verify if the total term frequency has already been calculated and
        # calculates it if necessary (this done to avoid calculating this
        # multiple times)
        if len(self.total_df) == 0:
            for f in self.frequencies:
                for key in f:
                    if key in self.total_df:
                        self.total_df[key] += f[key]
                    else:
                        self.total_df[key] = f[key]

        return self.total_df


    def __repr__(self):
        return '<Main Feature Name: %s>' % (self.name)

    def __str__(self):
        return '<Main Feature Name: %s>' % (self.name)

class GeneralFeature(Feature):
    def __init__(self, feature_name, feature_synset=None):
        super().__init__(feature_name)

        self.synset = None
        try:
            self.synset = Synset(feature_synset)
        except:
            print('An error has occuring on creating the Synset for', feature_name)

        # self.doc_count stores the amount of documents containing the feature
        self.doc_count = 0

    def __repr__(self):
        return '<Feature Name: %s; Synset: %s>' % (self.name, self.synset)

    def __str__(self):
        return '<Feature Name: %s; Synset: %s>' % (self.name, self.synset)

    def path_similarity(self, feature):
        if isinstance(feature, GeneralFeature) and feature.synset and self.synset:
            return feature.synset.path_similarity(self.synset)
        return 0

    def increase_doc_count(self):
        self.doc_count += 1

    def get_idf(self, total_count):
        return math.log(total_count/(1 + self.doc_count))

    def get_tf_idf(self, total_count):
        idf = self.get_idf(total_count)
        tf_idf = []
        for f in self.frequencies:
            d = {}
            for key in f:
                d[key] = f[key]*idf
            tf_idf.append(d)
        return tf_idf

    def semantic_weight(self, total_count, main_feature):
        tf_idf = self.get_tf_idf(total_count)
        main_tf = main_feature.get_tf()
        den = main_feature.get_total_tf()

        # Get the weigthed mean for each key
        num = {}
        for i in range(len(tf_idf)):
            # If tf_idf has one key, main_tf will have it too
            for key in tf_idf[i]:
                if key in num:
                    num[key] += tf_idf[i][key]*main_tf[i][key]
                else:
                    num[key] = tf_idf[i][key]*main_tf[i][key]

        weight = 0
        for key in num:
            weight += math.pow(num[key]/den[key], 2)

        return math.sqrt(weight)

