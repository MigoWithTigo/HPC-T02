import csv
import matplotlib.pyplot as plt
import numpy as np

def read_algo_csv(path):
    ps, times, speedups, efficiencies = [], [], [], []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ps.append(int(row['p']))
            times.append(float(row['avg_time_ms']))
            speedups.append(float(row['speedup']))
            efficiencies.append(float(row['efficiency']))
    return ps, times, speedups, efficiencies

def plot_comparison():
    # Load Local (PC1)
    p_b, t_b, s_b, e_b = read_algo_csv('results_exp_b.csv')
    p_c, t_c, s_c, e_c = read_algo_csv('results_exp_c.csv')
    p_d, t_d, s_d, e_d = read_algo_csv('results_exp_d.csv')

    # Load Remote (PC2)
    p_br, t_br, s_br, e_br = read_algo_csv('results_exp_b_remote.csv')
    p_cr, t_cr, s_cr, e_cr = read_algo_csv('results_exp_c_remote.csv')
    p_dr, t_dr, s_dr, e_dr = read_algo_csv('results_exp_d_remote.csv')

    fig, axs = plt.subplots(2, 3, figsize=(15, 9))

    colors = {
        'algo1': '#1f77b4',  # blue
        'algo2': '#2ca02c',  # green
        'algo3': '#ff7f0e',  # orange
        'ideal': '#333333'   # dark gray
    }

    # Row 0: PC1 Local
    # T(p)
    axs[0, 0].plot(p_b, t_b, marker='o', linewidth=2, color=colors['algo1'], label='Algo 1 (OpenMP loops)')
    axs[0, 0].plot(p_c, t_c, marker='s', linewidth=2, color=colors['algo2'], label='Algo 2 (D&C, n=256)')
    axs[0, 0].plot(p_d, t_d, marker='^', linewidth=2, color=colors['algo3'], label='Algo 3 (Numba JIT)')
    axs[0, 0].set_title('Tiempo T(p) - PC1 Local (Ryzen 7 7840U)', fontsize=11, fontweight='bold')
    axs[0, 0].set_xlabel('Threads (p)', fontsize=10)
    axs[0, 0].set_ylabel('Tiempo (ms)', fontsize=10)
    axs[0, 0].set_xticks(p_b)
    axs[0, 0].grid(True, linestyle=':', alpha=0.6)
    axs[0, 0].legend(fontsize=9)

    # S(p)
    axs[0, 1].plot(p_b, s_b, marker='o', linewidth=2, color=colors['algo1'], label='Algo 1 (OpenMP)')
    axs[0, 1].plot(p_c, s_c, marker='s', linewidth=2, color=colors['algo2'], label='Algo 2 (D&C)')
    axs[0, 1].plot(p_d, s_d, marker='^', linewidth=2, color=colors['algo3'], label='Algo 3 (Numba)')
    axs[0, 1].plot(p_b, p_b, linestyle='--', color=colors['ideal'], label='Ideal (S=p)')
    axs[0, 1].set_title('Speedup S(p) - PC1 Local', fontsize=11, fontweight='bold')
    axs[0, 1].set_xlabel('Threads (p)', fontsize=10)
    axs[0, 1].set_ylabel('Speedup S(p)', fontsize=10)
    axs[0, 1].set_xticks(p_b)
    axs[0, 1].grid(True, linestyle=':', alpha=0.6)
    axs[0, 1].legend(fontsize=9)

    # E(p)
    axs[0, 2].plot(p_b, e_b, marker='o', linewidth=2, color=colors['algo1'], label='Algo 1 (OpenMP)')
    axs[0, 2].plot(p_c, e_c, marker='s', linewidth=2, color=colors['algo2'], label='Algo 2 (D&C)')
    axs[0, 2].plot(p_d, e_d, marker='^', linewidth=2, color=colors['algo3'], label='Algo 3 (Numba)')
    axs[0, 2].axhline(1.0, linestyle='--', color=colors['ideal'], label='Ideal (E=1.0)')
    axs[0, 2].set_title('Eficiencia E(p) - PC1 Local', fontsize=11, fontweight='bold')
    axs[0, 2].set_xlabel('Threads (p)', fontsize=10)
    axs[0, 2].set_ylabel('Eficiencia E(p)', fontsize=10)
    axs[0, 2].set_ylim(0, 1.1)
    axs[0, 2].set_xticks(p_b)
    axs[0, 2].grid(True, linestyle=':', alpha=0.6)
    axs[0, 2].legend(fontsize=9)

    # Row 1: PC2 Remoto
    # T(p)
    axs[1, 0].plot(p_br, t_br, marker='o', linewidth=2, color=colors['algo1'], label='Algo 1 (OpenMP)')
    axs[1, 0].plot(p_cr, t_cr, marker='s', linewidth=2, color=colors['algo2'], label='Algo 2 (D&C, n=256)')
    axs[1, 0].plot(p_dr, t_dr, marker='^', linewidth=2, color=colors['algo3'], label='Algo 3 (Numba)')
    axs[1, 0].set_title('Tiempo T(p) - PC2 Remoto (Core i5-4210U)', fontsize=11, fontweight='bold')
    axs[1, 0].set_xlabel('Threads (p)', fontsize=10)
    axs[1, 0].set_ylabel('Tiempo (ms)', fontsize=10)
    axs[1, 0].set_xticks(p_br)
    axs[1, 0].grid(True, linestyle=':', alpha=0.6)
    axs[1, 0].legend(fontsize=9)

    # S(p)
    axs[1, 1].plot(p_br, s_br, marker='o', linewidth=2, color=colors['algo1'], label='Algo 1 (OpenMP)')
    axs[1, 1].plot(p_cr, s_cr, marker='s', linewidth=2, color=colors['algo2'], label='Algo 2 (D&C)')
    axs[1, 1].plot(p_dr, s_dr, marker='^', linewidth=2, color=colors['algo3'], label='Algo 3 (Numba)')
    axs[1, 1].plot(p_br, p_br, linestyle='--', color=colors['ideal'], label='Ideal (S=p)')
    axs[1, 1].set_title('Speedup S(p) - PC2 Remoto', fontsize=11, fontweight='bold')
    axs[1, 1].set_xlabel('Threads (p)', fontsize=10)
    axs[1, 1].set_ylabel('Speedup S(p)', fontsize=10)
    axs[1, 1].set_xticks(p_br)
    axs[1, 1].grid(True, linestyle=':', alpha=0.6)
    axs[1, 1].legend(fontsize=9)

    # E(p)
    axs[1, 2].plot(p_br, e_br, marker='o', linewidth=2, color=colors['algo1'], label='Algo 1 (OpenMP)')
    axs[1, 2].plot(p_cr, e_cr, marker='s', linewidth=2, color=colors['algo2'], label='Algo 2 (D&C)')
    axs[1, 2].plot(p_dr, e_dr, marker='^', linewidth=2, color=colors['algo3'], label='Algo 3 (Numba)')
    axs[1, 2].axhline(1.0, linestyle='--', color=colors['ideal'], label='Ideal (E=1.0)')
    axs[1, 2].set_title('Eficiencia E(p) - PC2 Remoto', fontsize=11, fontweight='bold')
    axs[1, 2].set_xlabel('Threads (p)', fontsize=10)
    axs[1, 2].set_ylabel('Eficiencia E(p)', fontsize=10)
    axs[1, 2].set_ylim(0, 1.1)
    axs[1, 2].set_xticks(p_br)
    axs[1, 2].grid(True, linestyle=':', alpha=0.6)
    axs[1, 2].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('informe/E/Grafico/exp_e_comparacion.pdf', bbox_inches='tight')
    plt.savefig('informe/E/Grafico/exp_e_comparacion.png', dpi=300, bbox_inches='tight')
    plt.savefig('informe/E/exp_e_comparacion.pdf', bbox_inches='tight')
    plt.savefig('informe/E/exp_e_comparacion.png', dpi=300, bbox_inches='tight')
    print("exp_e_comparacion plots generated.")

def plot_algo2_blocks():
    # Read results_exp_e_algo2_n.csv
    # Format: n, p, avg_time_ms, speedup, efficiency
    data = {}
    with open('results_exp_e_algo2_n.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row['n'])
            p = int(row['p'])
            t = float(row['avg_time_ms'])
            s = float(row['speedup'])
            e = float(row['efficiency'])
            if n not in data:
                data[n] = {'p': [], 't': [], 's': [], 'e': []}
            data[n]['p'].append(p)
            data[n]['t'].append(t)
            data[n]['s'].append(s)
            data[n]['e'].append(e)

    ns = sorted(data.keys())
    ps = sorted(list(set(data[ns[0]]['p'])))

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.5))

    # Panel 1: T vs n for each p
    cmap = plt.get_cmap('viridis')
    p_colors = [cmap(i) for i in np.linspace(0.1, 0.9, len(ps))]

    for idx, p in enumerate(ps):
        times_for_p = [dict(zip(data[n]['p'], data[n]['t']))[p] for n in ns]
        axs[0].plot(ns, times_for_p, marker='o', linewidth=2, color=p_colors[idx], label=f'p = {p}')

    axs[0].set_title('Algoritmo 2: Tiempo T vs Tamaño de Bloque (n)', fontsize=11, fontweight='bold')
    axs[0].set_xlabel('Tamaño de bloque n (caso base)', fontsize=10)
    axs[0].set_ylabel('Tiempo promedio (ms)', fontsize=10)
    axs[0].set_xticks(ns)
    axs[0].grid(True, linestyle=':', alpha=0.6)
    axs[0].legend(fontsize=9)

    # Panel 2: Speedup S(p) vs p for each n
    n_colors = [plt.get_cmap('plasma')(i) for i in np.linspace(0.1, 0.85, len(ns))]
    for idx, n in enumerate(ns):
        s_vals = data[n]['s']
        axs[1].plot(ps, s_vals, marker='s', linewidth=2, color=n_colors[idx], label=f'n = {n}')
    axs[1].plot(ps, ps, linestyle='--', color='black', label='Ideal (S=p)')

    axs[1].set_title('Algoritmo 2: Speedup S(p) según Tamaño de Bloque n', fontsize=11, fontweight='bold')
    axs[1].set_xlabel('Número de Threads (p)', fontsize=10)
    axs[1].set_ylabel('Speedup S(p)', fontsize=10)
    axs[1].set_xticks(ps)
    axs[1].grid(True, linestyle=':', alpha=0.6)
    axs[1].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('informe/E/Grafico/exp_e_algo2_bloques.pdf', bbox_inches='tight')
    plt.savefig('informe/E/Grafico/exp_e_algo2_bloques.png', dpi=300, bbox_inches='tight')
    plt.savefig('informe/E/exp_e_algo2_bloques.pdf', bbox_inches='tight')
    plt.savefig('informe/E/exp_e_algo2_bloques.png', dpi=300, bbox_inches='tight')
    print("exp_e_algo2_bloques plots generated.")

if __name__ == "__main__":
    plot_comparison()
    plot_algo2_blocks()
