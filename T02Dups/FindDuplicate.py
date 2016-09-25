import os
import sys
import hashlib


def hash_file(path, blocksize=65536):
    with open(path, 'rb') as file:
        hash_sha = hashlib.sha1()
        buff = file.read(blocksize)
        while len(buff) > 0:
            hash_sha.update(buff)
            buff = file.read(blocksize)
        return hash_sha.hexdigest()


def find_duplicates(top_dir):
    dups = {}
    names_to_hash = {}
    for dirpath, _dirnames, filenames in os.walk(top_dir):
        filenames = filter(lambda x: not x.startswith(('.', '~')), filenames)
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if filename in names_to_hash:
                dups[names_to_hash[filename]] += ':' + path
            else:
                file_hash = hash_file(path)
                names_to_hash[filename] = file_hash
                if file_hash in dups:
                    dups[file_hash] += ':' + path
                else:
                    dups[file_hash] = path
    return dups


def main():
    if len(sys.argv) > 1:
        dups = find_duplicates(os.path.abspath(sys.argv[1]))
        for equals in dups.values():
            if ':' in equals:
                print(equals)

if __name__ == "__main__":
    main()
