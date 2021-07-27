import numpy as np
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def feature(styles):
  feature = [style.name for style in styles]
  combine_features = " ".join(feature)
  return combine_features


def vectorize(data):
    vectors = CountVectorizer().fit_transform(data)
    return vectors
