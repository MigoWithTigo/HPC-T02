import subprocess
import re
import csv
import sys
import os

def run_experiment():
    print("Compiling algo1_omp.cpp...")
    subprocess.run(["g++", "-O3", "-march=native", "-fopenmp", "algo1_omp.cpp", "-o", "algo1_omp"], check=True)
    
    ps = [1, 2, 4, 8]
    N = 2048
    runs = 10
    
    results = {}
    
    print("Running experiments...")
    for p in ps:
        times = []
        for r in range(runs):
            env = os.environ.copy()
            env["OMP_NUM_THREADS"] = str(p)
            res = subprocess.run(["./algo1_omp", str(N)], env=env, capture_output=True, text=True)
            match = re.search(r'tiempo=([\d\.]+)\s*ms', res.stdout)
            if match:
                times.append(float(match.group(1)))
            else:
                print(f"Failed to parse output: {res.stdout}")
        
        avg_time = sum(times) / len(times)
        results[p] = avg_time
        print(f"p={p}, avg_time={avg_time:.2f} ms")
        
    t1 = results[1]
    
    csv_file = "results_exp_b.csv" if len(sys.argv) == 1 else sys.argv[1]
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["p", "avg_time_ms", "speedup", "efficiency"])
        for p in ps:
            t = results[p]
            speedup = t1 / t
            efficiency = speedup / p
            writer.writerow([p, f"{t:.2f}", f"{speedup:.4f}", f"{efficiency:.4f}"])
            
    print(f"Results saved to {csv_file}")

if __name__ == "__main__":
    run_experiment()
