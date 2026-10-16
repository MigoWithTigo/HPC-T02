import subprocess
import re
import csv
import os
import sys

def run_f_experiment():
    print("Compiling algo1_omp.cpp and algo2_omp.cpp...")
    subprocess.run(["g++", "-O3", "-march=native", "-fopenmp", "algo1_omp.cpp", "-o", "algo1_omp"], check=True)
    subprocess.run(["g++", "-O3", "-march=native", "-fopenmp", "algo2_omp.cpp", "-o", "algo2_omp"], check=True)

    Ns = [1024, 2048, 4096]
    ps = [1, 2, 4, 8]
    n_dc = 256  # Base block size for Algo 2

    results = []

    # 1. Run Algoritmo 2 (Dividir y Conquistar)
    print("\n=== Medición Algoritmo 2 (Dividir y Conquistar, n=256) ===")
    for N in Ns:
        reps = 3 if N == 4096 else 5
        t1_algo2 = None
        for p in ps:
            times = []
            for r in range(reps):
                env = os.environ.copy()
                env["OMP_NUM_THREADS"] = str(p)
                res = subprocess.run(["./algo2_omp", str(N), str(n_dc)], env=env, capture_output=True, text=True)
                m = re.search(r'tiempo=([\d\.]+)\s*ms', res.stdout)
                if m:
                    times.append(float(m.group(1)))
                else:
                    print(f"Error parsing: {res.stdout}")
            avg_t = sum(times) / len(times)
            if p == 1:
                t1_algo2 = avg_t
            s = t1_algo2 / avg_t
            e = s / p
            print(f"Algo2 | N={N:4d} | p={p} | t={avg_t:8.2f} ms | S={s:5.2f} | E={e:5.2f}")
            results.append({
                "algo": "algo2_omp",
                "N": N,
                "p": p,
                "avg_time_ms": round(avg_t, 2),
                "speedup": round(s, 4),
                "efficiency": round(e, 4)
            })

    # 2. Run Algoritmo 1 (OpenMP Loops)
    print("\n=== Medición Algoritmo 1 (OpenMP Loops) ===")
    for N in Ns:
        reps = 3 if N == 4096 else 5
        t1_algo1 = None
        for p in ps:
            times = []
            for r in range(reps):
                env = os.environ.copy()
                env["OMP_NUM_THREADS"] = str(p)
                res = subprocess.run(["./algo1_omp", str(N)], env=env, capture_output=True, text=True)
                m = re.search(r'tiempo=([\d\.]+)\s*ms', res.stdout)
                if m:
                    times.append(float(m.group(1)))
                else:
                    print(f"Error parsing: {res.stdout}")
            avg_t = sum(times) / len(times)
            if p == 1:
                t1_algo1 = avg_t
            s = t1_algo1 / avg_t
            e = s / p
            print(f"Algo1 | N={N:4d} | p={p} | t={avg_t:8.2f} ms | S={s:5.2f} | E={e:5.2f}")
            results.append({
                "algo": "algo1_omp",
                "N": N,
                "p": p,
                "avg_time_ms": round(avg_t, 2),
                "speedup": round(s, 4),
                "efficiency": round(e, 4)
            })

    out_csv = "results_exp_f.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["algo", "N", "p", "avg_time_ms", "speedup", "efficiency"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResultados guardados exitosamente en {out_csv}")

if __name__ == "__main__":
    run_f_experiment()
