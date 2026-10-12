import subprocess
import re
import csv
import sys
import os

def run_experiment(python_bin=sys.executable, output_csv="results_exp_d.csv"):
    ps = [1, 2, 4, 8]
    N = 2048
    runs = 10
    results = {}
    
    print(f"Running Numba experiments (N={N}, 10 runs per p)...")
    for p in ps:
        times = []
        env = os.environ.copy()
        env["NUMBA_NUM_THREADS"] = str(p)
        for r in range(runs):
            res = subprocess.run([python_bin, "algo3_numba.py", str(N), str(p)], env=env, capture_output=True, text=True)
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
    py_exec = sys.argv[1] if len(sys.argv) > 1 else sys.executable
    out_file = sys.argv[2] if len(sys.argv) > 2 else "results_exp_d.csv"
    run_experiment(py_exec, out_file)
