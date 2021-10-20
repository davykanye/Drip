import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wardrobe.models import *

def extract(photo):
    return photo.styles

def feature(style):
  feature = [i.name for i in style]
  combine_features = " ".join(feature)
  return combine_features

def get_features(photo):
    style = extract(photo)
    features = feature(style)

    return features

def get_styles(photos):
    styles = dict()
    for photo in photos:
        id = photo.id
        style = extract(photo)
        features = feature(style)
        styles[id] = features
    return styles

def get_category(id):
    item = Photos.objects.get(id=id)

    return item.category.name

def get_ids(query):
    ids = []
    for i in query:
        ids.append(i.id)
    return ids

def item(id):
    return Photos.objects.get(id=id)

def outfit_template(items):
    headwear = items.filter(category__name='headwear')
    top = items.filter(category__name='top')
    lower = items.filter(category__name='lower')
    shoes = items.filter(category__name='shoes')

    hashmap = {'headwear': get_ids(headwear), 'top': get_ids(top), 'lower': get_ids(lower), 'shoes': get_ids(shoes)}

    return hashmap

def get_best(seed, array):
    matches = []
    for i in array:
        if compare(seed, i) == True:
            matches.append(i)
        else:
            pass
    return random.choice(matches)

def make_outfit(seed, items):
    outfit = {get_category(seed): Photos.objects.get(id=seed)}
    hashmap = outfit_template(items)
    hashmap.pop(get_category(seed))
    cats = [hashmap[i] for i in hashmap]
    for i in cats:
        best = get_best(seed, i)
        outfit[get_category(best)] = item(best)

    return outfit



def compare(seed, pair):
    seed_item = Photos.objects.get(id=seed)
    pair_item = Photos.objects.get(id=pair)

    seed_feature = get_features(seed_item)
    pair_feature = get_features(pair_item)

    vectors = CountVectorizer().fit_transform([seed_feature, pair_feature])
    matrix = cosine_similarity(vectors)

    output = round(matrix[1][0] * 100, 2)
    if output > 30:
        truth = True
    else:
        truth = False

    return truth
