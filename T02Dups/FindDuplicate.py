import os
import sys
import hashlib
import collections


def hash_file(path, blocksize=65536):
    with open(path, 'rb') as file:
        hasher = hashlib.sha1()
        buff = file.read(blocksize)
        while len(buff) > 0:
            hasher.update(buff)
            buff = file.read(blocksize)
        return hasher.hexdigest()


def find_duplicates(top_dir):
    dups = collections.defaultdict(list)
    for dirpath, _, filenames in os.walk(top_dir):
        filenames = filter(lambda x: not x.startswith(('.', '~')), filenames)
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if os.path.islink(path):
                continue
            dups[hash_file(path)].append(path)
    return dups


def main():
    assert len(sys.argv) == 2
    dups = find_duplicates(os.path.abspath(sys.argv[1]))
    for equal_files in dups.values():
        if len(equal_files) > 1:
            print(*equal_files, sep=':')


if __name__ == "__main__":
    main()
