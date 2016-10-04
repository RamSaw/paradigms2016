import numpy as np


def read_matrix(size):
    matrix = np.empty((0, size), int)
    for _ in range(size):
        row = list(map(int, input().split()))
        matrix = np.vstack((matrix, row))
    return matrix


def extend_matrix(matr):
    size = len(matr)
    extended_size = 2 ** (size - 1).bit_length()
    extended_matr = np.zeros((extended_size, extended_size), dtype=int)
    extended_matr[:size, :size] = matr[:size, :size]
    return extended_matr


def divide_matr_to_four(matr):
    vsplited = np.vsplit(matr, 2)
    return np.hsplit(vsplited[0], 2) + np.hsplit(vsplited[1], 2)


def strassen(matr1, matr2):
    size = len(matr1)

    if size == 1:
        return np.array([[matr1[0][0] * matr2[0][0]]])

    a11, a12, a21, a22 = divide_matr_to_four(matr1)
    b11, b12, b21, b22 = divide_matr_to_four(matr2)

    p1 = strassen(a11 + a22, b11 + b22)
    p2 = strassen(a21 + a22, b11)
    p3 = strassen(a11, b12 - b22)
    p4 = strassen(a22, b21 - b11)
    p5 = strassen(a11 + a12, b22)
    p6 = strassen(a21 - a11, b11 + b12)
    p7 = strassen(a12 - a22, b21 + b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 - p2 + p3 + p6

    return np.vstack((np.hstack((c11, c12)),
                      np.hstack((c21, c22))))


def mul_matr_strassen(matr1, matr2):
    original_size = len(matr1)
    extended_matr1 = extend_matrix(matr1)
    extended_matr2 = extend_matrix(matr2)
    res = strassen(extended_matr1, extended_matr2)
    return res[:original_size, :original_size]


def main():
    size = int(input())
    matr1 = read_matrix(size)
    matr2 = read_matrix(size)
    result = mul_matr_strassen(matr1, matr2)
    for row in result:
        print(' '.join(map(str, row)))

if __name__ == '__main__':
    main()
