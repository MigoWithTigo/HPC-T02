import csv
import matplotlib.pyplot as plt
import numpy as np

def generate_f_plots():
    # Read results_exp_f.csv
    # Columns: algo, N, p, avg_time_ms, speedup, efficiency
    data = {}
    with open('results_exp_f.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            algo = row['algo']
            N = int(row['N'])
            p = int(row['p'])
            t = float(row['avg_time_ms'])
            s = float(row['speedup'])
            e = float(row['efficiency'])
            key = (algo, N)
            if key not in data:
                data[key] = {'p': [], 't': [], 's': [], 'e': []}
            data[key]['p'].append(p)
            data[key]['t'].append(t)
            data[key]['s'].append(s)
            data[key]['e'].append(e)

    fig, axs = plt.subplots(1, 3, figsize=(16, 5))

    colors = {1024: '#1f77b4', 2048: '#2ca02c', 4096: '#d62728'}
    markers = {1024: 'o', 2048: 's', 4096: '^'}

    # 1. Panel 1: Speedup S(p) for Algo 2 across N
    for N in [1024, 2048, 4096]:
        ps = data[('algo2_omp', N)]['p']
        ss = data[('algo2_omp', N)]['s']
        axs[0].plot(ps, ss, marker=markers[N], linewidth=2, color=colors[N], label=f'N = {N}')
    axs[0].plot([1, 2, 4, 8], [1, 2, 4, 8], linestyle='--', color='black', label='Ideal (S=p)')
    axs[0].set_title('Speedup S(p) según Tamaño de Matriz (N)', fontsize=11, fontweight='bold')
    axs[0].set_xlabel('Número de Threads (p)', fontsize=10)
    axs[0].set_ylabel('Speedup S(p)', fontsize=10)
    axs[0].set_xticks([1, 2, 4, 8])
    axs[0].grid(True, linestyle=':', alpha=0.6)
    axs[0].legend(fontsize=9)

    # 2. Panel 2: Eficiencia Paralela E(p) for Algo 2 across N
    for N in [1024, 2048, 4096]:
        ps = data[('algo2_omp', N)]['p']
        es = data[('algo2_omp', N)]['e']
        axs[1].plot(ps, es, marker=markers[N], linewidth=2, color=colors[N], label=f'N = {N}')
    axs[1].axhline(1.0, linestyle='--', color='black', label='Ideal (E=1.0)')
    axs[1].set_title('Eficiencia E(p) vs Tamaño N (Algoritmo 2)', fontsize=11, fontweight='bold')
    axs[1].set_xlabel('Número de Threads (p)', fontsize=10)
    axs[1].set_ylabel('Eficiencia E(p)', fontsize=10)
    axs[1].set_ylim(0, 1.1)
    axs[1].set_xticks([1, 2, 4, 8])
    axs[1].grid(True, linestyle=':', alpha=0.6)
    axs[1].legend(fontsize=9)

    # 3. Panel 3: Comparación de Eficiencia Débil (W/p = cte)
    # Case A: N=1024 at p=1 vs N=2048 at p=8 (Work increases 8x, p increases 8x)
    # Case B: N=2048 at p=1 vs N=4096 at p=8 (Work increases 8x, p increases 8x)
    # For Algo2:
    t_1024_1 = dict(zip(data[('algo2_omp', 1024)]['p'], data[('algo2_omp', 1024)]['t']))[1]
    t_2048_8 = dict(zip(data[('algo2_omp', 2048)]['p'], data[('algo2_omp', 2048)]['t']))[8]
    ew_a2_1 = t_1024_1 / t_2048_8

    t_2048_1 = dict(zip(data[('algo2_omp', 2048)]['p'], data[('algo2_omp', 2048)]['t']))[1]
    t_4096_8 = dict(zip(data[('algo2_omp', 4096)]['p'], data[('algo2_omp', 4096)]['t']))[8]
    ew_a2_2 = t_2048_1 / t_4096_8

    # For Algo1:
    t1_1024_1 = dict(zip(data[('algo1_omp', 1024)]['p'], data[('algo1_omp', 1024)]['t']))[1]
    t1_2048_8 = dict(zip(data[('algo1_omp', 2048)]['p'], data[('algo1_omp', 2048)]['t']))[8]
    ew_a1_1 = t1_1024_1 / t1_2048_8

    t1_2048_1 = dict(zip(data[('algo1_omp', 2048)]['p'], data[('algo1_omp', 2048)]['t']))[1]
    t1_4096_8 = dict(zip(data[('algo1_omp', 4096)]['p'], data[('algo1_omp', 4096)]['t']))[8]
    ew_a1_2 = t1_2048_1 / t1_4096_8

    labels = ['N: 1024 (p=1) → 2048 (p=8)', 'N: 2048 (p=1) → 4096 (p=8)']
    x = np.arange(len(labels))
    width = 0.35

    bars1 = axs[2].bar(x - width/2, [ew_a2_1, ew_a2_2], width, label='Algoritmo 2 (D&C)', color='#2ca02c')
    bars2 = axs[2].bar(x + width/2, [ew_a1_1, ew_a1_2], width, label='Algoritmo 1 (OpenMP)', color='#1f77b4')

    axs[2].axhline(1.0, linestyle='--', color='black', label='Ideal (E_weak=1.0)')
    axs[2].set_title('Eficiencia Débil E_weak (Trabajo/Hilo = cte)', fontsize=11, fontweight='bold')
    axs[2].set_ylabel('Eficiencia Débil (T(1) / T(p))', fontsize=10)
    axs[2].set_xticks(x)
    axs[2].set_xticklabels(labels, fontsize=9)
    axs[2].set_ylim(0, 1.2)
    axs[2].grid(axis='y', linestyle=':', alpha=0.6)
    axs[2].legend(fontsize=9)

    # Add values on top of bars
    for bar in bars1:
        yval = bar.get_height()
        axs[2].text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in bars2:
        yval = bar.get_height()
        axs[2].text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig('informe/F/Grafico/exp_f_escalabilidad.pdf', bbox_inches='tight')
    plt.savefig('informe/F/Grafico/exp_f_escalabilidad.png', dpi=300, bbox_inches='tight')
    plt.savefig('informe/F/exp_f_escalabilidad.pdf', bbox_inches='tight')
    plt.savefig('informe/F/exp_f_escalabilidad.png', dpi=300, bbox_inches='tight')
    print("exp_f_escalabilidad plots generated successfully.")

if __name__ == "__main__":
    generate_f_plots()
