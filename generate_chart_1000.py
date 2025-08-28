import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Ler dados dos top 1000
df = pd.read_csv('Resultados/github_1000_repositories.csv')

# Configurar estilo
plt.style.use('default')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# 1. Top 20 repositórios por estrelas
top_20 = df.nlargest(20, 'stars')
ax1.barh(range(len(top_20)), top_20['stars'], color='gold')
ax1.set_yticks(range(len(top_20)))
ax1.set_yticklabels([name.split('/')[-1][:15] for name in top_20['name']], fontsize=8)
ax1.set_xlabel('Número de Estrelas')
ax1.set_title('Top 20 Repositórios por Estrelas (1000 repos)')
ax1.invert_yaxis()

# 2. Distribuição por linguagem (top 10)
lang_counts = df['primary_language'].value_counts().head(10)
colors = plt.cm.Set3(np.linspace(0, 1, len(lang_counts)))
ax2.pie(lang_counts.values, labels=lang_counts.index, autopct='%1.1f%%', 
        startangle=90, colors=colors)
ax2.set_title('Top 10 Linguagens Principais')

# 3. Relação entre idade e estrelas
ax3.scatter(df['age_years'], df['stars'], alpha=0.5, color='blue', s=20)
ax3.set_xlabel('Idade do Repositório (anos)')
ax3.set_ylabel('Número de Estrelas')
ax3.set_title('Idade vs Popularidade (1000 repos)')
ax3.set_yscale('log')

# 4. Distribuição de estrelas por faixas
bins = [0, 1000, 5000, 10000, 50000, 100000, 500000]
labels = ['<1K', '1K-5K', '5K-10K', '10K-50K', '50K-100K', '>100K']
df['star_range'] = pd.cut(df['stars'], bins=bins, labels=labels, include_lowest=True)
star_dist = df['star_range'].value_counts().sort_index()
ax4.bar(range(len(star_dist)), star_dist.values, color='red', alpha=0.7)
ax4.set_xticks(range(len(star_dist)))
ax4.set_xticklabels(star_dist.index, rotation=45)
ax4.set_ylabel('Número de Repositórios')
ax4.set_title('Distribuição por Faixas de Estrelas')

plt.tight_layout()
plt.savefig('Resultados/github_1000_analysis_chart.png', dpi=300, bbox_inches='tight')
plt.show()

# Estatísticas resumidas
print("\n=== ESTATÍSTICAS DOS TOP 1000 REPOSITÓRIOS ===")
print(f"Total de repositórios: {len(df)}")
print(f"Média de estrelas: {df['stars'].mean():.0f}")
print(f"Mediana de estrelas: {df['stars'].median():.0f}")
print(f"Repositório mais popular: {df.loc[df['stars'].idxmax(), 'name']} ({df['stars'].max():,} estrelas)")
print(f"Idade média: {df['age_years'].mean():.1f} anos")
print(f"Linguagem mais popular: {df['primary_language'].mode()[0]} ({df['primary_language'].value_counts().iloc[0]} repos)")

print("\nGráfico salvo em: Resultados/github_1000_analysis_chart.png")