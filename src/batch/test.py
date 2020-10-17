# coding: UTF-8
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import glob
import json
import time

# abs path
abs_path = os.path.dirname(os.path.abspath(__file__))
print('sss')
print('/'.join(abs_path.split('/')[0:-2]))
