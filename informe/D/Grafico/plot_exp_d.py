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

# Read data
p_l, s_l, e_l = read_csv('results_exp_d.csv')
p_r, s_r, e_r = read_csv('results_exp_d_remote.csv')

# Create figure
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Speedup Local
axs[0, 0].plot(p_l, s_l, marker='o', color='purple', linewidth=2, label='Real (Numba)')
axs[0, 0].plot(p_l, p_l, linestyle='--', color='black', label='Ideal (S=p)')
axs[0, 0].set_title('Speedup - PC1 Local (Ryzen 7 7840U)', fontsize=11, fontweight='bold')
axs[0, 0].set_xlabel('Número de Threads (p)', fontsize=10)
axs[0, 0].set_ylabel('Speedup S(p)', fontsize=10)
axs[0, 0].set_xticks(p_l)
axs[0, 0].legend()
axs[0, 0].grid(True, linestyle=':', alpha=0.7)

# Speedup Remoto
axs[0, 1].plot(p_r, s_r, marker='o', color='orange', linewidth=2, label='Real (Numba)')
axs[0, 1].plot(p_r, p_r, linestyle='--', color='black', label='Ideal (S=p)')
axs[0, 1].set_title('Speedup - PC2 Remoto (i5-4210U)', fontsize=11, fontweight='bold')
axs[0, 1].set_xlabel('Número de Threads (p)', fontsize=10)
axs[0, 1].set_ylabel('Speedup S(p)', fontsize=10)
axs[0, 1].set_xticks(p_r)
axs[0, 1].legend()
axs[0, 1].grid(True, linestyle=':', alpha=0.7)

# Eficiencia Local
p_str_l = [str(x) for x in p_l]
axs[1, 0].bar(p_str_l, e_l, color='purple', alpha=0.7)
axs[1, 0].axhline(1.0, linestyle='--', color='black', label='Ideal (E=1.0)')
axs[1, 0].set_title('Eficiencia - PC1 Local', fontsize=11, fontweight='bold')
axs[1, 0].set_xlabel('Número de Threads (p)', fontsize=10)
axs[1, 0].set_ylabel('Eficiencia E(p)', fontsize=10)
axs[1, 0].set_ylim(0, 1.1)
axs[1, 0].grid(axis='y', linestyle=':', alpha=0.7)
axs[1, 0].legend()

# Eficiencia Remoto
p_str_r = [str(x) for x in p_r]
axs[1, 1].bar(p_str_r, e_r, color='orange', alpha=0.7)
axs[1, 1].axhline(1.0, linestyle='--', color='black', label='Ideal (E=1.0)')
axs[1, 1].set_title('Eficiencia - PC2 Remoto', fontsize=11, fontweight='bold')
axs[1, 1].set_xlabel('Número de Threads (p)', fontsize=10)
axs[1, 1].set_ylabel('Eficiencia E(p)', fontsize=10)
axs[1, 1].set_ylim(0, 1.1)
axs[1, 1].grid(axis='y', linestyle=':', alpha=0.7)
axs[1, 1].legend()

plt.tight_layout()
plt.savefig("exp_d_plots.pdf", bbox_inches='tight')
plt.savefig("exp_d_plots.png", dpi=300, bbox_inches='tight')
print("Gráficos de D generados exitosamente.")
