# (b) Algoritmo 1: Paralelismo de datos con OpenMP

## Metodología
Implementamos el Algoritmo 1 en C++ (`algo1_omp.cpp`) aplicando paralelismo de datos en el bucle exterior de la multiplicación densa de $N \times N$ ($N=2048$):
```cpp
#pragma omp parallel for schedule(static)
for (int i = 0; i < N; ++i) {
    for (int k = 0; k < N; ++k) {
        double a = A[i * N + k];
        for (int j = 0; j < N; ++j) {
            C[i * N + j] += a * B[k * N + j];
        }
    }
}
```
Compilamos con:
```bash
g++ -O3 -march=native -fopenmp algo1_omp.cpp -o algo1_omp
```
Ejecutamos 10 repeticiones para cada número de threads $p \in \{1, 2, 4, 8\}$ con la variable de entorno `OMP_NUM_THREADS=p`, promediando los tiempos y calculando:
- Speedup: $S(p) = \frac{T(1)}{T(p)}$
- Eficiencia: $E(p) = \frac{S(p)}{p}$

## Resultados

### PC1 Local (AMD Ryzen 7 PRO 7840U — 8 cores físicos, 16 threads)
| $p$ | Tiempo Promedio (ms) | Speedup $S(p)$ | Eficiencia $E(p)$ |
|----:|---------------------:|---------------:|------------------:|
| 1   | 4579.82              | 1.0000         | 1.0000            |
| 2   | 3130.26              | 1.4631         | 0.7315            |
| 4   | 1658.09              | 2.7621         | 0.6905            |
| 8   | 1179.62              | 3.8824         | 0.4853            |

### PC2 Remoto (Intel Core i5-4210U — 2 cores físicos, 4 threads)
| $p$ | Tiempo Promedio (ms) | Speedup $S(p)$ | Eficiencia $E(p)$ |
|----:|---------------------:|---------------:|------------------:|
| 1   | 6271.94              | 1.0000         | 1.0000            |
| 2   | 5569.35              | 1.1262         | 0.5631            |
| 4   | 5720.83              | 1.0963         | 0.2741            |
| 8   | 6143.11              | 1.0210         | 0.1276            |

## Análisis
1. **Escalabilidad en PC1 (Ryzen 7 7840U)**:
   - Presenta un escalamiento sostenido al aumentar los hilos, alcanzando un speedup de casi $4\times$ ($3.88\times$) con 8 hilos.
   - La eficiencia disminuye de $1.0$ a $0.48$ con 8 hilos debido a la saturación del ancho de banda de memoria (*memory-bound*), ya que el orden de loops `i-k-j` accede a $B$ repetidamente, requiriendo un alto caudal de datos desde la caché L3/RAM que satura los canales de memoria al competir 8 núcleos.

2. **Comportamiento en PC2 (Intel i5-4210U)**:
   - El speedup prácticamente se estanca ($1.13\times$ con 2 hilos) e incluso retrocede con 4 y 8 hilos ($1.02\times$).
   - **Causas**:
     1. **Límite de núcleos físicos**: El procesador posee solo 2 núcleos físicos con Hyper-Threading. Con $p \ge 4$, los hilos compiten por las mismas unidades de ejecución.
     2. **Throttling térmico y de energía**: El i5-4210U es un procesador de bajo consumo (15W TDP). Al poner múltiples hilos al 100%, la frecuencia decae desde el Turbo máximo (2.7 GHz en 1 core) hacia frecuencias más bajas para no exceder el TDP.
     3. **Caché reducida (3 MiB L3) y cuello de botella en RAM**: Las matrices ($2048 \times 2048 \times 8 \text{ bytes} = 32 \text{ MB}$) exceden la caché, haciendo que los núcleos pasen la mayor parte del tiempo esperando datos de la memoria principal.
