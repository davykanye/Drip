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

    options = [{'headwear': get_ids(headwear),'top': get_ids(top), 'lower': get_ids(lower), 'shoes': get_ids(shoes)}, {'top': get_ids(top), 'lower': get_ids(lower), 'shoes': get_ids(shoes)}]
    hashmap = random.choice(options)  #{'headwear': get_ids(headwear),'top': get_ids(top), 'lower': get_ids(lower), 'shoes': get_ids(shoes)}

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

################ THIS SECTION IS FOR PICKING SEEDS AND EVENTS ##############

def get_profile(look):
    styles = look.styles.all()
    feature = [i.name for i in styles]
    combine_features = " ".join(feature)

    return combine_features

def check(look_profile, item):
    item_profile = get_features(item)

    vectors = CountVectorizer().fit_transform([look_profile, item_profile])
    matrix = cosine_similarity(vectors)

    output = round(matrix[1][0] * 100, 2)
    if output > 60:
        truth = True
    else:
        truth = False

    return truth

def pick_seeds(items):
    looks = Occassion.objects.all()
    seeds = {}
    for look in looks:
        seed = get_seed(look, items)
        seeds.update(seed)
    return split_dict(seeds)

def split_dict(foo):
    first = dict(list(foo.items())[len(foo)//2:])
    second = dict(list(foo.items())[:len(foo)//2])
    a = [first, second]
    return random.choice(a)


def get_seed(look, items):
    look_profile = get_profile(look)
    seed = []
    for i in items:
        if check(look_profile, i) == True:
            seed.append(i)
        else:
            pass
    return {str(look.name): seed}
