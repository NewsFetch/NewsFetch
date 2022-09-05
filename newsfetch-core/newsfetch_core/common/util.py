import json
import os
from typing import List

from newsfetch_core.common import constants


def list_files(dir_name: str, limit: bool = False, limit_value: int = constants.DEFAULT_LIMIT_FOR_TESTING):
    files = list()
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        files += [os.path.join(dirpath, file) for file in filenames]
    print(f"{len(files)} to process...")

    if limit:
        files = files[:limit_value]
        print(f"limit is True... processing {limit_value} files... probably in TEST mode!!")

    return files


def list_files_filter_suffix(directory_name, file_suffix):
    list_of_files = list()
    for root, dirs, files in os.walk(directory_name):
        for file in files:
            if file.endswith(file_suffix):
                list_of_files.append(os.path.join(root, file))
    return list_of_files


def get_warc_file_name(warc_file_path):
    return warc_file_path.split(".warc")[0]

def is_camel_case(word):
    count = 0
    for i in range(0, len(word) - 1):
        if (word[i].isupper()):
            count += 1
    return count > 1

def num_camel_case_words(text):
    counter = 0
    for word in text.split(" "):
        if is_camel_case(word):
            counter = counter + 1

    return counter

def write_json_to_file(dirs: List, file_name, data):
    dir_path = os.path.join(*dirs)
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, file_name)
    print(f"saving data to {path}...")
    with(open(path, "w+")) as out_file:
        out_file.writelines(json.dumps(data))


