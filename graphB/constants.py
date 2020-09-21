from os import listdir
from os.path import isfile, join, splitext, dirname, abspath

BASE_PATH = dirname(dirname(abspath(__file__))) + "/graphB/"

CONFIG_BASE = BASE_PATH + "configs/"