import numpy as np


def read_matrix(size):
    matrix = np.empty((0, size), int)
    for _ in range(size):
        row = list(map(int, input().split()))
        matrix = np.vstack((matrix, row))
    return matrix


def get_extended_matr(matr):
    size = len(matr)
    if 2 ** (size.bit_length() - 1) == size:
        correct_size = size
    else:
        correct_size = 2 ** size.bit_length()
    correct_matr = np.zeros((correct_size, correct_size), dtype=int)
    correct_matr[:size, :size] = matr[:size, :size]
    return correct_matr


def divide_matr_to_four(matr):
    hsplited = np.hsplit(matr, 2)
    return np.vsplit(hsplited[0], 2) + np.vsplit(hsplited[1], 2)


def strassen_algorithm(matr1, matr2):
    size = len(matr1)

    if size == 1:
        return np.array(matr1[0][0] * matr2[0][0])

    divided_matr1 = divide_matr_to_four(matr1)
    a11 = divided_matr1[0]
    a12 = divided_matr1[2]
    a21 = divided_matr1[1]
    a22 = divided_matr1[3]

    divided_matr2 = divide_matr_to_four(matr2)
    b11 = divided_matr2[0]
    b12 = divided_matr2[2]
    b21 = divided_matr2[1]
    b22 = divided_matr2[3]

    p1 = strassen_algorithm(a11 + a22, b11 + b22)
    p2 = strassen_algorithm(a21 + a22, b11)
    p3 = strassen_algorithm(a11, b12 - b22)
    p4 = strassen_algorithm(a22, b21 - b11)
    p5 = strassen_algorithm(a11 + a12, b22)
    p6 = strassen_algorithm(a21 - a11, b11 + b12)
    p7 = strassen_algorithm(a12 - a22, b21 + b22)

    res = np.zeros((size, size), dtype=int)
    res[:size // 2, :size // 2] = p1 + p4 - p5 + p7
    res[:size // 2, size // 2:size] = p3 + p5
    res[size // 2:size, :size // 2] = p2 + p4
    res[size // 2:size, size // 2: size] = p1 - p2 + p3 + p6

    # I suppose that it should look like this, but it throws an error
    # #res = np.empty((size // 2, size // 2), int)
    # #res = np.vstack((res, p1 + p4 - p5 + p7))
    # #res = np.hstack((res, p3 + p5))
    # #res = np.vstack((res, p2 + p4))
    # #res = np.hstack((res, p1 - p2 + p3 + p6))

    return res


def mul_matr_strassen(matr1, matr2):
    original_size = len(matr1)
    correct_matr1 = get_extended_matr(matr1)
    correct_matr2 = get_extended_matr(matr2)
    res = strassen_algorithm(correct_matr1, correct_matr2)
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
