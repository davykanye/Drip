import numpy as np
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def feature(style):
    feature = [i.name for i in style]
    combine_features = " ".join(feature)
    return combine_features

def extract(photo):
    style = photo.styles
    return feature(style)

def get_styles(photos):
    styles = {photo.id: extract(photo) for photo in photos}

    return styles

def vectorize(data):
    vectors = CountVectorizer().fit_transform(data)
    return vectors
