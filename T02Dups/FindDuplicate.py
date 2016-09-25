import os
import sys
import hashlib


def hash_file(path, blocksize=65536):
    with open(path, 'r') as file:
        hash_sha = hashlib.sha1()
        buff = file.read(blocksize)
        while len(buff) > 0:
            hash_sha.update(buff)
            buff = file.read(blocksize)
    file.close()
    return hash_sha.hexdigest()


def find_duplicates(top_dir):
    dups = {}
    names = {}
    for dirpath, dirnames, filenames in os.walk(top_dir):
        filenames = filter(lambda x: not x.startswith(('.', '~')), filenames)
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if filename in names:
                dups[names[filename]] += ':' + path
            else:
                file_hash = hash_file(path)
                names[filename] = file_hash
                if file_hash in dups:
                    dups[file_hash] += ':' + path
                else:
                    dups[file_hash] = path
    return dups


def main():
    dups = find_duplicates(sys.argv[1])
    for hash, equals in dups.items():
        if ':' in equals:
            print(equals + '\n')

if __name__ == "__main__":
    main()