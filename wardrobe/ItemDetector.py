import time

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


def predict(term):
    class_names = {'headwear': [], 'jacket': [], 'top': [], 'lower': [], 'shoes': []}
    category = ''
    for key, value in class_names.items():
        if check(term, value) == True:
            category = str(key)
        else:
            pass
    return category
