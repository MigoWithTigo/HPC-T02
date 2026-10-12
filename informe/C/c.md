# (c) Algoritmo 2: Dividir y Conquistar con OpenMP

## 1. Detalles de la Implementación
A partir de `serial.cpp`, se implementó la paralelización de dividir y conquistar utilizando el modelo de **tareas de OpenMP** (`#pragma omp task`):

1. **Descomposición por cuadrantes independientes:**
   La multiplicación por bloques divide la matriz resultante en 4 cuadrantes disjuntos:
   $$\begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix} \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$
   donde:
   - $C_{11} = A_{11}B_{11} + A_{12}B_{21}$
   - $C_{12} = A_{11}B_{12} + A_{12}B_{22}$
   - $C_{21} = A_{21}B_{11} + A_{22}B_{21}$
   - $C_{22} = A_{21}B_{12} + A_{22}B_{22}$

2. **Ausencia de condiciones de carrera (*Race-Free*):**
   Como cada cuadrante $C_{ij}$ ocupa posiciones continuas y disjuntas en memoria, se asigna una tarea de OpenMP para calcular los dos términos acumulativos de cada cuadrante en secuencia. De este modo, **no existe contención ni concurrencia sobre los mismos datos en $C$**, eliminando por completo la necesidad de sincronizaciones costosas (locks, operaciones atómicas) o buffers temporales de memoria.

3. **Corte de recursión y control de overhead:**
   Cuando el tamaño del sub-bloque actual $s$ es menor o igual al umbral $n$, se invoca directamente `multiply_leaf` sin generar nuevas tareas, evitando el overhead de gestión del runtime de OpenMP en los niveles más profundos del árbol.

```cpp
#pragma omp task default(none) firstprivate(A, B, C, h, n)
{
    multiply_rec_omp(A.sub(0, 0, h), B.sub(0, 0, h), C.sub(0, 0, h), n);
    multiply_rec_omp(A.sub(0, h, h), B.sub(h, 0, h), C.sub(0, 0, h), n);
}
// Análogo para C12, C21, C22
#pragma omp taskwait
```

---

## 2. Justificación de la Elección de $n$

Se seleccionó $n = 256$ para las mediciones por las siguientes razones:

1. **Ajuste a la jerarquía de memoria caché:**
   - Un bloque de $256 \times 256$ elementos `double` ocupa $256 \times 256 \times 8\text{ B} = 512\text{ KiB}$.
   - En **PC1** (AMD Ryzen 7 PRO 7840U), cada núcleo cuenta con $1\text{ MiB}$ de caché L2, por lo que el bloque cabe cómodamente dentro de la caché rápida privada del núcleo.
   - En **PC2** (Intel Core i5-4210U), cada núcleo cuenta con $256\text{ KiB}$ de L2 y comparte $3\text{ MiB}$ de L3. Con $n=512$ ($2\text{ MiB}$ por bloque), los bloques desbordan severamente la caché rápida (como se evidenció en la parte A con un salto a $5422\text{ ms}$); en cambio, $n=256$ rindió prácticamente en el óptimo serial ($4619\text{ ms}$ frente a $4553\text{ ms}$ en $n=128$).
2. **Granularidad de tareas y balanceo de carga:**
   - Para $N=2048$ y $n=256$, la profundidad del árbol es $\log_2(2048/256) = 3$ niveles, generando un total de $(2048/256)^2 = 64$ sub-bloques/tareas a nivel de hojas.
   - 64 tareas es divisible de forma exacta entre $p \in \{1, 2, 4, 8\}$ threads ($64/8 = 8$ tareas por thread para $p=8$), garantizando que todos los núcleos se mantengan ocupados sin sufrir desbalance ni saturar la cola de tareas del planificador.
3. **¿Debería usarse un $n$ distinto por máquina?**
   - Idealmente, si se pudiera parametrizar por máquina, PC1 podría aprovechar $n=512$ debido a su mayor caché L2 ($1\text{ MiB}$), mientras que PC2 se beneficia de $n=128$ o $n=256$. Sin embargo, al exigir el enunciado la elección de un valor único de $n$, **$n=256$ representa el punto de compromiso óptimo transversal**: evita la degradación crítica en PC2 y maximiza el paralelismo de tareas y localidad en PC1.

---

## 3. Resultados Experimentales ($N=2048, n=256$)

### PC1 Local (AMD Ryzen 7 PRO 7840U — 8 cores físicos, 16 threads)
| $p$ | Tiempo Promedio (ms) | Speedup $S(p)$ | Eficiencia $E(p)$ |
|----:|---------------------:|---------------:|------------------:|
| 1   | 1195.60              | 1.0000         | 1.0000            |
| 2   | 661.41               | 1.8076         | 0.9038            |
| 4   | 394.84               | 3.0281         | 0.7570            |
| 8   | 313.49               | 3.8138         | 0.4767            |

### PC2 Remoto (Intel Core i5-4210U — 2 cores físicos, 4 threads)
| $p$ | Tiempo Promedio (ms) | Speedup $S(p)$ | Eficiencia $E(p)$ |
|----:|---------------------:|---------------:|------------------:|
| 1   | 4371.64              | 1.0000         | 1.0000            |
| 2   | 3669.95              | 1.1912         | 0.5956            |
| 4   | 4417.29              | 0.9897         | 0.2474            |
| 8   | 4543.87              | 0.9621         | 0.1203            |

---

## 4. Análisis y Comparación

1. **Rendimiento Absoluto vs Algoritmo 1:**
   - La versión de dividir y conquistar con bloqueo por caché es **dramáticamente más rápida** que el Algoritmo 1 tradicional en ambas máquinas:
     - En PC1: a $p=1$ baja de $4579.82\text{ ms}$ a $1195.60\text{ ms}$ ($3.83\times$ más rápido en base serial); y a $p=8$ pasa de $1179.62\text{ ms}$ a **$313.49\text{ ms}$** ($3.76\times$ más rápido).
     - En PC2: a $p=1$ baja de $6271.94\text{ ms}$ a $4371.64\text{ ms}$, y a $p=2$ baja de $5569.35\text{ ms}$ a $3669.95\text{ ms}$.
   - Esto demuestra que reestructurar el algoritmo para respetar la jerarquía de memoria (cache-blocking recursivo) aporta un beneficio de rendimiento superior o comparable al paralelismo multihilo ingenuo.

2. **Escalabilidad y Eficiencia:**
   - **PC1**: Muestra una eficiencia sobresaliente para $p=2$ ($90.4\%$) y $p=4$ ($75.7\%$), con un speedup de $3.81\times$ en $p=8$. La reducción de eficiencia en $p=8$ se debe al ancho de banda del bus de memoria y a la ligera competencia de caché compartida en el CCX.
   - **PC2**: Logra su mejor tiempo en $p=2$ ($S(2)=1.19\times$), pero al aumentar a $p=4$ y $p=8$, el tiempo se degrada ($S < 1$). Como se identificó en la parte B, esto responde a las limitaciones físicas del i5-4210U: solo tiene 2 núcleos físicos, el TDP de 15W provoca *downclocking* térmico al encender múltiples hilos, y el overhead del runtime de tareas sobrecarga los recursos virtuales de Hyper-Threading.
