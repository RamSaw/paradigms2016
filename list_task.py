# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    lst.sort()
    prev = lst[0]
    for i in lst[1:]:
        if i == prev:
            lst.remove(i)
        else:
            prev = i
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
    print(lst)
    return

def main():
    lst1 = [2, 4, 6]
    lst2 = [1, 3, 5, 5, 6, 7]
    linear_merge(lst1, lst2)

if __name__ == "__main__":
    main()


