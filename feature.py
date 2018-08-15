from textblob.wordnet import Synset

class Feature:
    def __init__(self, feature_name, feature_synset):
        if not (isinstance(feature_name, str)):
            raise ValueError('The first argument must be a string')
        if not (isinstance(feature_synset, str)):
            raise ValueError('The second argument must be a string')
        self.name = feature_name.lower()
        self.synset = Synset(feature_synset)

    def __repr__(self):
        return '<Feature Name: %s; Synset: %s>' % (self.name, self.synset)

    def __str__(self):
        return '<Feature Name: %s; Synset: %s>' % (self.name, self.synset)

    def path_similarity(self, feature):
        if not (isinstance(feature, Feature)):
            raise ValueError('The first argument must be a Feature')
        return self.synset.path_similarity(feature.synset)

    def wup_similarity(self, feature):
        if not (isinstance(feature, Feature)):
            raise ValueError('The first argument must be a Feature')
        return self.synset.wup_similarity(feature.synset)

    def lch_similarity(self, feature):
        if not (isinstance(feature, Feature)):
            raise ValueError('The first argument must be a Feature')
        return self.synset.lch_similarity(feature.synset)
