"""An example where we use an explicit global variable"""

from functools import lru_cache
from time import sleep

state = None

@lru_cache(maxsize=1)
def initialize(model_id):
    sleep(2)
    return model_id    


def function(model_id, x):
    weights = initialize(model_id)
    return x + weights
