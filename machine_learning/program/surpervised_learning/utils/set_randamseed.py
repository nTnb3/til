import random
import  numpy as np


def set_ramdomseed(seed=0):
    random.seed(seed)
    np.random.seed(seed)