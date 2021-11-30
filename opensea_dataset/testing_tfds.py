# Test the Custom TFDS Dataset loader

import os
import random
import math
import numpy as np
import matplotlib.pyplot as plt

from enum import Enum
from glob import glob
from functools import partial

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow_addons.layers import InstanceNormalization

import tensorflow_datasets as tfds


import opensea_dataset
ds = tfds.load('opensea_dataset')
list(ds.take(1))