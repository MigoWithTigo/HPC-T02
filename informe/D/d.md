# (d) Algoritmo 3: Numba en Python

## 1. Implementación en Python con Numba
Se implementó desde cero en Python la versión de paralelismo de datos (Algoritmo 1) sobre matrices densas de $N \times N$ ($N=2048$) usando el compilador JIT **Numba** (`algo3_numba.py`).

1. **Paralelización de bucles de datos:**
   Se utilizó el decorador `@njit(parallel=True)` junto con la función `prange` en el bucle exterior para distribuir las iteraciones sobre las filas de la matriz entre los hilos:
   ```python
   @njit(parallel=True)
   def multiply_numba(A, B, N):
       C = np.zeros((N, N), dtype=np.float64)
       for i in prange(N):
           for k in range(N):
               a = A[i, k]
               for j in range(N):
                   C[i, j] += a * B[k, j]
       return C
   ```

2. **Exclusión del tiempo de compilación JIT (Warm-up):**
   Para medir estrictamente el tiempo de ejecución paralelo sin contaminar la métrica con la fase de compilación e inferencia de tipos de LLVM, se ejecutó una llamada previa de precalentamiento (*warm-up*) con matrices pequeñas ($64 \times 64$) antes de iniciar la toma de tiempos:
   ```python
   warm_N = 64
   wA = np.ones((warm_N, warm_N), dtype=np.float64)
   wB = np.ones((warm_N, warm_N), dtype=np.float64)
   _ = multiply_numba(wA, wB, warm_N)
   ```

3. **Control del número de hilos:**
   Se controló la concurrencia dinámicamente mediante `numba.set_num_threads(p)` y la variable de entorno `NUMBA_NUM_THREADS=p`.

4. **Verificación de correctitud:**
   El checksum resultante fue exactamente **`172.331627`**, idéntico al de las versiones de referencia en C++.

---

## 2. Resultados Experimentales ($N=2048$, 10 repeticiones)

### PC1 Local (AMD Ryzen 7 PRO 7840U — 8 cores físicos, 16 threads)
| $p$ | Tiempo Promedio (ms) | Speedup $S(p)$ | Eficiencia $E(p)$ |
|----:|---------------------:|---------------:|------------------:|
| 1   | 2014.47              | 1.0000         | 1.0000            |
| 2   | 1075.38              | 1.8733         | 0.9366            |
| 4   | 663.36               | 3.0368         | 0.7592            |
| 8   | 523.67               | 3.8468         | 0.4809            |

### PC2 Remoto (Intel Core i5-4210U — 2 cores físicos, 4 threads)
| $p$ | Tiempo Promedio (ms) | Speedup $S(p)$ | Eficiencia $E(p)$ |
|----:|---------------------:|---------------:|------------------:|
| 1   | 5651.67              | 1.0000         | 1.0000            |
| 2   | 5394.04              | 1.0478         | 0.5239            |
| 4   | 6052.48              | 0.9338         | 0.2334            |
| 8   | 6308.52              | 0.8959         | 0.1120            |

---

## 3. Comparación Integral con las Otras Versiones (para $N=2048$)

Comparando los tiempos absolutos (ms) y speedups en **PC1 Local**:

| Versión | $p=1$ (ms) | $p=2$ (ms) | $p=4$ (ms) | $p=8$ (ms) | Speedup $S(8)$ | Eficiencia $E(8)$ |
|:---|---:|---:|---:|---:|---:|---:|
| **Algoritmo 1: C++ OpenMP (Data Par.)** | 4579.82 | 3130.26 | 1658.09 | 1179.62 | $3.88\times$ | $48.5\%$ |
| **Algoritmo 2: C++ OpenMP (Dividir y Conquistar, $n=256$)** | **1195.60** | **661.41** | **394.84** | **313.49** | $3.81\times$ | $47.7\%$ |
| **Algoritmo 3: Python Numba (Data Par.)** | 2014.47 | 1075.38 | 663.36 | 523.67 | $3.85\times$ | $48.1\%$ |

### Conclusiones de la Comparación:
1. **Numba vs C++ OpenMP ingenuo (Algoritmo 1):**
   - Sorprendentemente, **Numba es más del doble de rápido que C++ OpenMP básico** en todos los niveles de hilos ($2014\text{ ms}$ vs $4579\text{ ms}$ en $p=1$, y $523\text{ ms}$ vs $1179\text{ ms}$ en $p=8$).
   - Esto se debe a que el optimizador LLVM integrado en Numba aplica vectorización automática agresiva (instrucciones AVX2/FMA) y un desenrollado de bucles más eficiente en el loop más interno que el código base de C++ compilado sin directivas explícitas de vectorización.
2. **Dividir y Conquistar (Algoritmo 2) sigue siendo el más rápido:**
   - A pesar del gran desempeño de Numba, el **Algoritmo 2 en C++ supera a Numba por un $67\%$ de ventaja** a 8 hilos ($313.49\text{ ms}$ vs $523.67\text{ ms}$). Esto confirma que la optimización algorítmica de la jerarquía de memoria (cache-blocking en submatrices de $256 \times 256$) es superior a la paralelización plana de filas.
3. **Comportamiento en PC2 (Intel Core i5-4210U):**
   - En PC2, Numba exhibe el mismo cuello de botella que el Algoritmo 1 de OpenMP: un estancamiento en $p=2$ ($5394\text{ ms}$) y una degradación a $p=4$ y $p=8$ ($6052\text{ ms}$ y $6308\text{ ms}$). Esto ratifica que la saturación de memoria RAM y la limitación física a 2 núcleos reales es independiente del lenguaje/runtime utilizado.
