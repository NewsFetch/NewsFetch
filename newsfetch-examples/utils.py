import os
from glob import glob


def list_files(root_dir: str, pattern: str):
    path_pattern = os.path.join(root_dir, pattern)
    print(path_pattern)
    files = glob(path_pattern, recursive=True)
    return files