import numpy as np


if __name__ == '__main__':
    a = np.ones([3, 3])
    print(a)
    print()
    b = np.triu(a)
    print(b)
    print()
    c = np.where(b == 0)
    print(*c)

    print(list(zip(*c)))