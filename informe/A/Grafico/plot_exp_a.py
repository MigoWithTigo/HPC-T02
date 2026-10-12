import csv
from collections import defaultdict
import matplotlib.pyplot as plt

def load_data(filepath):
    data = defaultdict(list)
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row['n'])
            t = float(row['tiempo_ms'])
            data[n].append(t)
    ns = sorted(data.keys(), reverse=True)
    means = [sum(data[n]) / len(data[n]) for n in ns]
    return ns, means

ns_local, means_local = load_data('results_exp_a.csv')
ns_remote, means_remote = load_data('results_exp_a_remote.csv')

plt.figure(figsize=(8, 5))
plt.plot([str(n) for n in ns_local], means_local, marker='o', label='PC1 Local (AMD Ryzen 7 PRO 7840U)', color='#1f77b4')
plt.plot([str(n) for n in ns_remote], means_remote, marker='s', label='PC2 Remoto (Intel Core i5-4210U)', color='#d62728')
plt.title('Tiempo de Ejecución Serial vs Tamaño de Bloque (N=2048)', fontsize=12)
plt.xlabel('Tamaño de bloque n', fontsize=11)
plt.ylabel('Tiempo promedio (ms)', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

plt.savefig('exp_a_tiempos.pdf')
plt.savefig('exp_a_tiempos.png', dpi=300)
print("Gráficos generados exitosamente.")
