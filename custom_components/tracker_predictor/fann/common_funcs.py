from math import *
from random import random

RAND_MAX = 1


def ann_rand(min: float, max: float) -> float:
    return min + ((max - min) * random() / (RAND_MAX + 1))


def ann_random_weight() -> float:
    return ann_rand(-0.1, 0.1)


def ann_random_bias_weight() -> float:
    return ann_rand(-0.1, 0.1)
