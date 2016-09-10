# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
# [1, 2, 2, 3, 2, 3, 3, 5, 0]


def remove_adjacent(lst):
    if not lst:
        return lst
    prev = lst[0]
    added = 0
    lstres = []
    for num in lst[1:]:
        if not lstres:
            added = 1
            if lst[0] != lst[1]:
                lstres.append(lst[0])
        if prev != num:
            lstres.append(num)
            prev = num
    if not added:
        lstres.append(lst[0])
    return lstres

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

    while j < len2 and i < len1:
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
    return lst


def main():
    lst1 = []
    lst1 = remove_adjacent(lst1)
    print(lst1)
    lst1 = [2, 4, 6, 120]
    lst2 = [1, 3, 5, 6, 7]
    lst = linear_merge(lst1, lst2)
    print(lst)

if __name__ == "__main__":
    main()


