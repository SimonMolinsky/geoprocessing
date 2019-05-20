import fiona as fio


def get_features_list(vector_file, feature_key_name):
    """Function creates feature list in the multipolygon based on the given unique property (feature_key_name)
    such as ID.
    :param vector_file: multipolygon file,
    :param feature_key_name: unique key for features differentiation,
    :return features_list: list of unique features in the multipolygon."""
    features_list = []
    with fio.open(vector_file, 'r') as multipolygon:
        for poly in multipolygon:
            features_list.append(poly['properties'][feature_key_name])
    return features_list