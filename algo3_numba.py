# algo3_numba.py - Algoritmo 3: Multiplicacion densa N x N en Python con Numba
import sys
import time
import math
import numpy as np
import numba
from numba import njit, prange

@njit(fastmath=False)
def det_value(i, j, offset):
    return math.sin(i * 0.1 + j * 0.3 + offset)

@njit(parallel=True, fastmath=False)
def init_matrix(N, offset):
    M = np.empty((N, N), dtype=np.float64)
    for i in prange(N):
        for j in range(N):
            M[i, j] = det_value(i, j, offset)
    return M

# Algoritmo 3: Paralelismo de datos con Numba
@njit(parallel=True, fastmath=False)
def multiply_numba(A, B, N):
    C = np.zeros((N, N), dtype=np.float64)
    for i in prange(N):
        for k in range(N):
            a = A[i, k]
            for j in range(N):
                C[i, j] += a * B[k, j]
    return C

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
    p = int(sys.argv[2]) if len(sys.argv) > 2 else numba.get_num_threads()

    try:
        numba.set_num_threads(p)
    except ValueError:
        numba.set_num_threads(numba.config.NUMBA_NUM_THREADS)

    # Warm-up para compilar JIT antes de medir
    warm_N = 64
    wA = np.ones((warm_N, warm_N), dtype=np.float64)
    wB = np.ones((warm_N, warm_N), dtype=np.float64)
    _ = multiply_numba(wA, wB, warm_N)

    # Inicializacion de matrices
    A = init_matrix(N, 1.0)
    B = init_matrix(N, 2.0)

    # Medicion de tiempo excluyendo compilacion JIT
    t0 = time.perf_counter()
    C = multiply_numba(A, B, N)
    t1 = time.perf_counter()
    ms = (t1 - t0) * 1000.0

    checksum = float(np.sum(C))
    print(f"N={N} p={p} tiempo={ms:.2f} ms checksum={checksum:.6f}")

if __name__ == "__main__":
    main()
