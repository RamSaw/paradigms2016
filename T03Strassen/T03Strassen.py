import numpy as np
import math


def read_matrix(size):
    matrix = np.array([list(map(int, input().split()))])
    for i in range(size - 1):
        row = list(map(int, input().split()))
        matrix = np.append(matrix, [row], axis=0)
    return matrix


def get_corrected_matr(matr):
    size = len(matr)
    correct_size = 2 ** int(math.ceil(math.log(size, 2)))
    correct_matr = np.zeros((correct_size, correct_size), dtype=int)
    correct_matr[:size, :size] += matr[:size, :size]
    return correct_matr


def mul_matr_cube(matr1, matr2):
    size = len(matr1)
    res = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            res[i][j] = sum(matr1[i][k] * matr2[k][j] for k in range(size))
    return res


def strassen_algorithm(matr1, matr2):
    size = len(matr1)

    if size < 64:
        return mul_matr_cube(matr1, matr2)

    A11 = matr1[:size // 2, :size // 2]
    A12 = matr1[:size // 2, size // 2:size]
    A21 = matr1[size // 2:size, :size // 2]
    A22 = matr1[size // 2:size, size // 2: size]

    B11 = matr2[:size // 2, :size // 2]
    B12 = matr2[:size // 2, size // 2:size]
    B21 = matr2[size // 2:size, :size // 2]
    B22 = matr2[size // 2:size, size // 2: size]

    P1 = strassen_algorithm(A11 + A22, B11 + B22)
    P2 = strassen_algorithm(A21 + A22, B11)
    P3 = strassen_algorithm(A11, B12 - B22)
    P4 = strassen_algorithm(A22, B21 - B11)
    P5 = strassen_algorithm(A11 + A12, B22)
    P6 = strassen_algorithm(A21 - A11, B11 + B12)
    P7 = strassen_algorithm(A12 - A22, B21 + B22)

    res_matr = np.zeros((size, size), dtype=int)
    res_matr[:size // 2, :size // 2] = P1 + P4 - P5 + P7
    res_matr[:size // 2, size // 2:size] = P3 + P5
    res_matr[size // 2:size, :size // 2] = P2 + P4
    res_matr[size // 2:size, size // 2: size] = P1 - P2 + P3 + P6

    return res_matr


def mul_matr_strassen(matr1, matr2):
    original_size = len(matr1)
    correct_matr1 = get_corrected_matr(matr1)
    correct_matr2 = get_corrected_matr(matr2)
    res_matr = strassen_algorithm(correct_matr1, correct_matr2)
    return res_matr[:original_size, :original_size]


def main():
    size = int(input())
    matr1 = read_matrix(size)
    matr2 = read_matrix(size)
    res_matr = mul_matr_strassen(matr1, matr2)

    for i in range(size):
        print(' '.join(map(str, res_matr[i])))

if __name__ == '__main__':
    main()
