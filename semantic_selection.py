from feature import Feature

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
