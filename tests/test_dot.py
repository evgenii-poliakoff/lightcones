import numpy as np
from lightcones.linalg import dot

def test_dot():
    a = np.array([1.0 + 1j, 2.0], dtype = complex)
    b = np.array([3.0, 1.0 - 1j * 2], dtype = complex)
    c = dot(a, b)
    assert np.isclose(c, (1.0 - 1j) * 3.0 + 2.0 * (1.0 - 1j *2))
    
def test_dot_2():
    a = np.array([1.0 + 1j, 2.0], dtype = complex)
    b = [[np.array([3.0, 1.0], dtype = complex), np.array([1.0, 2.0], dtype = complex)],
         [np.array([0.0, 1.0], dtype = complex), np.array([1.0, 0.0], dtype = complex)]]
    c = dot(a, b)
    c_expected = [[dot(a, b[0][0]), dot(a, b[0][1])],
                  [dot(a, b[1][0]), dot(a, b[1][1])]]
    for i in range(2):
        for j in range(2):
            np.isclose(c[i][j], c_expected[i][j], rtol=1e-5, atol=1e-8), \
                f"c not match the ethalon"