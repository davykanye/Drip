import time
from wardrobe.models import Term

def check(term, list):
    state = False
    for i in list:
        for j in term.split():
            if i == j:
                state = True
                break
            else:
                state = False
        break
    return state        

def get_terms(category):
    terms = Term.objects.get(category__name=category)

    output = [str(i.name) for i in terms]
    return output

def predict(term):
    class_names = {'headwear': get_terms('headwear'), 'jacket': get_terms('jacket'), 'top': get_terms('top'), 'lower': get_terms('lower'), 'shoes': get_terms('shoes')}
    category = ''
    for key, value in class_names.items():
        if check(term, value) == True:
            category = str(key)
        else:
            pass
    return category
