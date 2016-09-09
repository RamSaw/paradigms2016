# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
# [1, 2, 2, 3, 2, 3, 3, 5, 0]


def remove_adjacent(lst):
    prev = lst[0]
    i = 1
    length = len(lst)
    while i != length:
        if lst[i] == prev:
            del lst[i]
            length -= 1
        else:
            prev = lst[i]
            i += 1
    print(lst)
    return

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]


def linear_merge(lst1, lst2):
    j = 0
    i = 0
    lst = []
    len1 = len(lst1)
    len2 = len(lst2)
    if len2 > len1:
        t = lst1
        lst1 = lst2
        lst2 = t
        t = len1
        len1 = len2
        len2 = t

    while i < len1:
        if j == len2:
            break
        if lst1[i] >= lst2[j]:
            lst.append(lst2[j])
            j += 1
        else:
            lst.append(lst1[i])
            i += 1
    if i < len1:
        lst += lst1[i:]
    elif j < len2:
        lst += lst2[j:]
    print(lst)
    return


def main():
    lst1 = [1, 2, 2, 3, 2, 3, 3, 3, 5, 0]
    remove_adjacent(lst1)
    lst1 = [2, 4, 6, 120]
    lst2 = [1, 3, 5, 6, 7]
    linear_merge(lst1, lst2)

if __name__ == "__main__":
    main()


