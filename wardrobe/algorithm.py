import numpy as np
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract(photo):
    return photo.styles

def feature(style):
  feature = [i.name for i in style]
  combine_features = " ".join(feature)
  return combine_features


def get_styles(photos):
    styles = dict()
    for photo in photos:
        id = photo.id
        style = extract(photo)
        features = feature(style)
        styles[id] = features
    return styles

def vectorize(data):
    vectors = CountVectorizer().fit_transform(data)
    return vectors


def compute_data(data):
    vectors = vectorize(data)
    matrix = cosine_similarity(vectors)

    return matrix


def get_index(id, data):
    list_index = data[data['id']==id].index.values
    index = list_index[0]

    return index

def get_category(index, data):
    tip = data["category"][index]

    return tip
