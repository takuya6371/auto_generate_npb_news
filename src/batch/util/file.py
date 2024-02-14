# coding: UTF-8
from io import TextIOWrapper
import os
import json
import glob

def fileWrite (filePath:str, text:TextIOWrapper):
    with open(filePath, 'w') as file:
        file.write(text)

def fileRead (file):
    with open(file) as f:
       return f.read()

def jsonFileRead (file):
    with open(file) as f:
       return json.load(f)

def createFolder (path: str):
    if not os.path.exists(path):
        os.mkdir(path)
        print('folder create:' + path)

def jsonDump (jsonFile: str, data, mode: str):
    with open(jsonFile, mode) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def clearDirectory (path):
    print(path)
    print(glob.glob(path + '/*'))
    if len(glob.glob(path + '/*')) > 0:
        print("exist")
        for p in glob.glob(path + '/*', recursive=True):
            print(p)
            if os.path.isfile(p):
                os.remove(p)

def listFiles (path):
    return sorted(glob.glob(path + '/*'))
