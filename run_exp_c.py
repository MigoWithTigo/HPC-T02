import subprocess
import re
import csv
import sys
import os

def run_experiment(output_csv="results_exp_c.csv", n_val=256):
    print(f"Compiling algo2_omp.cpp...")
    subprocess.run(["g++", "-O3", "-march=native", "-fopenmp", "algo2_omp.cpp", "-o", "algo2_omp"], check=True)
    
    ps = [1, 2, 4, 8]
    N = 2048
    runs = 10
    
    results = {}
    
    print(f"Running experiments (N={N}, n={n_val}, 10 runs per p)...")
    for p in ps:
        times = []
        for r in range(runs):
            env = os.environ.copy()
            env["OMP_NUM_THREADS"] = str(p)
            res = subprocess.run(["./algo2_omp", str(N), str(n_val)], env=env, capture_output=True, text=True)
            match = re.search(r'tiempo=([\d\.]+)\s*ms', res.stdout)
            if match:
                times.append(float(match.group(1)))
            else:
                print(f"Failed to parse output: {res.stdout} (stderr: {res.stderr})")
        
        avg_time = sum(times) / len(times)
        results[p] = avg_time
        print(f"p={p}, avg_time={avg_time:.2f} ms")
        
    t1 = results[1]
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["p", "avg_time_ms", "speedup", "efficiency"])
        for p in ps:
            t = results[p]
            speedup = t1 / t
            efficiency = speedup / p
            writer.writerow([p, f"{t:.2f}", f"{speedup:.4f}", f"{efficiency:.4f}"])
            
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "results_exp_c.csv"
    n_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 256
    run_experiment(out_file, n_arg)
