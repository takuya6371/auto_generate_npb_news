from io import TextIOWrapper
import os
import json
import glob

def file_write (file_path:str, text:TextIOWrapper):
    with open(file_path, 'w') as file:
        file.write(text)

def json_file_read (file):
    with open(file) as f:
       return json.load(f)

def create_folder (path: str):
    if not os.path.exists(path):
        os.mkdir(path)
        print('folder create:' + path)

def json_dump (json_file: str, data, mode: str):
    with open(json_file, mode) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def clear_directory (path):
    print(path)
    print(glob.glob(path + '/*'))
    if len(glob.glob(path + '/*')) > 0:
        print("exist")
        for p in glob.glob(path + '/*', recursive=True):
            print(p)
            if os.path.isfile(p):
                os.remove(p)

def list_file (path):
    return sorted(glob.glob(path + '/*'))
