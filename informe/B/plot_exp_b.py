import csv
import matplotlib.pyplot as plt

def read_csv(filename):
    ps, times, speedups, efficiencies = [], [], [], []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ps.append(int(row['p']))
            times.append(float(row['avg_time_ms']))
            speedups.append(float(row['speedup']))
            efficiencies.append(float(row['efficiency']))
    return ps, speedups, efficiencies

# File paths
local_csv = "../../results_exp_b.csv"
remote_csv = "../../results_exp_b_remote.csv"

# Read data
p_l, s_l, e_l = read_csv(local_csv)
p_r, s_r, e_r = read_csv(remote_csv)

# Create figure
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Speedup Local
axs[0, 0].plot(p_l, s_l, marker='o', color='blue', label='Real')
axs[0, 0].plot(p_l, p_l, linestyle='--', color='black', label='Ideal')
axs[0, 0].set_title('Speedup - PC1')
axs[0, 0].set_xlabel('Número de Threads (p)')
axs[0, 0].set_ylabel('Speedup')
axs[0, 0].set_xticks(p_l)
axs[0, 0].legend()
axs[0, 0].grid(True, linestyle=':', alpha=0.7)

# Speedup Remoto
axs[0, 1].plot(p_r, s_r, marker='o', color='red', label='Real')
axs[0, 1].plot(p_r, p_r, linestyle='--', color='black', label='Ideal')
axs[0, 1].set_title('Speedup - PC2')
axs[0, 1].set_xlabel('Número de Threads (p)')
axs[0, 1].set_ylabel('Speedup')
axs[0, 1].set_xticks(p_r)
axs[0, 1].legend()
axs[0, 1].grid(True, linestyle=':', alpha=0.7)

# Eficiencia Local
p_str_l = [str(x) for x in p_l]
axs[1, 0].bar(p_str_l, e_l, color='blue', alpha=0.7)
axs[1, 0].axhline(1.0, linestyle='--', color='black', label='Ideal')
axs[1, 0].set_title('Eficiencia - PC1')
axs[1, 0].set_xlabel('Número de Threads (p)')
axs[1, 0].set_ylabel('Eficiencia')
axs[1, 0].set_ylim(0, 1.1)
axs[1, 0].grid(axis='y', linestyle=':', alpha=0.7)

# Eficiencia Remoto
p_str_r = [str(x) for x in p_r]
axs[1, 1].bar(p_str_r, e_r, color='red', alpha=0.7)
axs[1, 1].axhline(1.0, linestyle='--', color='black', label='Ideal')
axs[1, 1].set_title('Eficiencia - PC2')
axs[1, 1].set_xlabel('Número de Threads (p)')
axs[1, 1].set_ylabel('Eficiencia')
axs[1, 1].set_ylim(0, 1.1)
axs[1, 1].grid(axis='y', linestyle=':', alpha=0.7)

plt.tight_layout()
plt.savefig("exp_b_plots.pdf", bbox_inches='tight')
