# coding: UTF-8
import os

# abs path
abs_path = os.path.dirname(os.path.abspath(__file__))
print('sss')
print('/'.join(abs_path.split('/')[0:-2]))
