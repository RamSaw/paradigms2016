# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
#
# Example input: 'read'
# Example output: 'reading'


def verbing(s):
    if len(s) < 3:
        return s
    if s[-3::] == "ing":
        s += "ly"
    else:
        s += "ing"
    return s


# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
#
# Example input: 'This dinner is not that bad!'
# Example output: 'This dinner is good!'


def not_bad(s):
    n = s.find("not")
    b = s.find("bad")
    if n < b and n != -1:
        s = s[:n] + "good" + s[b + 3:]
    return s


# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
#
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
#
# Example input: 'abcd', 'xy'
# Example output: 'abxcdy'


def front_back(a, b):
    l1 = len(a)
    l2 = len(b)

    l1 = (l1 + 1) // 2
    l2 = (l2 + 1) // 2

    return a[:l1] + b[:l2] + a[l1:] + b[l2:]


def main():
    s1, s2 = 'abcd', 'xy'
    s = 'reading'
    s = verbing(s)
    print(s)
    s = front_back(s1, s2)
    print(s)

if __name__ == "__main__":
    main()