"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/11/20

"""
import configparser
import os

CONFIG_FILE_NAME = 'config.ini'


def config_section_map(base_dir):
    conf_dir = os.path.join(base_dir, CONFIG_FILE_NAME)
    config = configparser.ConfigParser()
    config.read(conf_dir)
    dict1 = {}
    for item in config['constant']:
        dict1[item] = config['constant'][item]

    for item in config['planner']:
        list_item = config['planner'][item]
        list_item = list_item.strip()
        list_item = list_item.replace('\n', '')
        list_item = list_item.replace(' ', '')
        list_item = list_item.split(',')
        dict1[item] = list_item
    return dict1
