from feature import Feature

def similar_features(features, threshold):
    selected_features = []
    for i in range(len(features)):
        for j in range(len(selected_features)):
            # We use path similarity because we are looking for hypernyms
            if features[i].path_similarity(selected_features[j]) > threshold:
                break
        else:
            # If no similar enough feature is found among the already selected
            # ones, add the current synset to the current one
            selected_features.append(features[i])
    return selected_features
