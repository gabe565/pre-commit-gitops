#!/usr/bin/env python3

import re
import yaml
from os.path import abspath
from lib.paths import *

env_mac_key = re.compile("^sops_mac=")


def check_env(path: str) -> bool:
    with open(path) as file:
        for line in file:
            if env_mac_key.search(line):
                return True
    print(f"Env file decrypted: {abspath(path)}")
    return False


def check_secret(path: str) -> bool:
    with open(path) as file:
        for doc in yaml.safe_load_all(file):
            if "kind" not in doc or doc["kind"] != "Secret":
                continue
            if "stringData" not in doc and "data" not in doc:
                continue
            if "sops" not in doc:
                print(f"Secret file decrypted: {abspath(path)}")
                return False
    return True


def main():
    success = True
    for path in argv_or_glob(glob_env):
        success = check_env(path) and success
    for path in argv_or_glob(glob_yaml):
        success = check_secret(path) and success
    if not success:
        exit(1)


if __name__ == "__main__":
    main()
