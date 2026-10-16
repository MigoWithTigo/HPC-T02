import subprocess
import re
import csv
import os
import sys

def run_algo2_sweep():
    # Compile algo2_omp
    print("Compiling algo2_omp.cpp...")
    subprocess.run(["g++", "-O3", "-march=native", "-fopenmp", "algo2_omp.cpp", "-o", "algo2_omp"], check=True)

    ns = [64, 128, 256, 512, 1024]
    ps = [1, 2, 4, 8]
    N = 2048
    runs = 5

    out_csv = "results_exp_e_algo2_n.csv"
    print(f"Running Algo 2 parameter sweep over n={ns} and p={ps} (N={N}, {runs} reps)...")

    results = []
    # To compute speedup per n, track T(1, n)
    t1_map = {}

    for n in ns:
        for p in ps:
            times = []
            for r in range(runs):
                env = os.environ.copy()
                env["OMP_NUM_THREADS"] = str(p)
                res = subprocess.run(["./algo2_omp", str(N), str(n)], env=env, capture_output=True, text=True)
                m = re.search(r'tiempo=([\d\.]+)\s*ms', res.stdout)
                if m:
                    times.append(float(m.group(1)))
                else:
                    print(f"Error parsing: {res.stdout} (err: {res.stderr})")
            avg_t = sum(times) / len(times)
            if p == 1:
                t1_map[n] = avg_t
            s = t1_map[n] / avg_t
            e = s / p
            print(f"n={n:4d} | p={p} | avg_time={avg_t:7.2f} ms | S={s:5.2f} | E={e:5.2f}")
            results.append({
                "n": n,
                "p": p,
                "avg_time_ms": round(avg_t, 2),
                "speedup": round(s, 4),
                "efficiency": round(e, 4)
            })

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "p", "avg_time_ms", "speedup", "efficiency"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved results to {out_csv}")

if __name__ == "__main__":
    run_algo2_sweep()
