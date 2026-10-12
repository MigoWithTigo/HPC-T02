# (a) Base serial y tamaño de bloque

## Metodología
Compilamos con:
```bash
g++ -O3 -march=native -fopenmp serial.cpp -o serial
```
Ejecutamos 10 repeticiones para cada tamaño de bloque $n \in \{2048, 1024, 512, 256, 128, 64, 32\}$ con $N=2048$ en ambas máquinas y promediamos los tiempos.
Checksum verificado: `172.331627` en todas las ejecuciones.

## Resultados

| $n$ | PC1 Local (ms) | PC2 Remoto (ms) | Ratio Remoto/Local |
|----:|---------------:|----------------:|-------------------:|
| 2048 | 4802.73 | 6498.86 | 1.35× |
| 1024 | 3323.12 | 6792.88 | 2.04× |
| 512 | **1483.54** | 5422.03 | 3.65× |
| 256 | 1850.04 | **4619.62** | 2.50× |
| 128 | 1596.87 | **4553.88** | 2.85× |
| 64 | 1880.20 | 4837.25 | 2.57× |
| 32 | 2584.43 | 5574.71 | 2.16× |

## Análisis
El parámetro $n$ controla el tamaño de los bloques en los casos base de la recursión; es decir, la matriz original se divide hasta llegar a submatrices de $n \times n$, generando un total de $(N/n)^2$ hojas donde se ejecuta la multiplicación y luego se suman los resultados.

Los tiempos forman una **curva en forma de U** debido a dos factores:
1. **$n$ grande ($2048, 1024$)**: Los bloques no caben en la memoria caché L1/L2, causando continuos *cache misses* y accesos lentos a memoria RAM.
2. **$n$ pequeño ($64, 32$)**: Aunque los bloques caben en caché, la cantidad de subproblemas y el overhead de la recursión crecen excesivamente (ej: $n=32$ genera 4096 hojas y 6 niveles de profundidad en el árbol de llamadas).
3. **Valores óptimos**: $n=512$ en PC1 (AMD Ryzen 7 PRO 7840U, L2 de 1 MiB/core) y $n=128$–$256$ en PC2 (Intel Core i5-4210U, L2 de 256 KiB/core). Coinciden con los tamaños de bloque cuyo conjunto de datos de trabajo (*working set*) cabe adecuadamente en la caché L2 de cada arquitectura.
