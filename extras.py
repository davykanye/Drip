import time
import random

slots = {'one':[1,2,3,4], 'two':[5,10,15], 'three':[10,20,33]}
array = [slots[i] for i in slots]

# I am trying to pick an event a person is going for

# STEPS
# have an array of  possible events
# pick the event with the most frequency or pick a random event

events = ['party', 'office', 'church']

def project(events):
    guess = random.choice(events)

    return guess

if __name__ == '__main__':
    test = project(events)

    print(test)
