import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ler dados
df = pd.read_csv('Resultados/github_100_repositories.csv')

# Configurar estilo
plt.style.use('default')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. Top 10 repositórios por estrelas
top_10 = df.nlargest(10, 'stars')
ax1.barh(range(len(top_10)), top_10['stars'], color='gold')
ax1.set_yticks(range(len(top_10)))
ax1.set_yticklabels([name.split('/')[-1] for name in top_10['name']], fontsize=8)
ax1.set_xlabel('Número de Estrelas')
ax1.set_title('Top 10 Repositórios por Estrelas')
ax1.invert_yaxis()

# 2. Distribuição por linguagem
lang_counts = df['primary_language'].value_counts().head(8)
ax2.pie(lang_counts.values, labels=lang_counts.index, autopct='%1.1f%%', startangle=90)
ax2.set_title('Distribuição por Linguagem Principal')

# 3. Issues fechadas vs abertas
ax3.scatter(df['open_issues'], df['closed_issues'], alpha=0.6, color='blue')
ax3.set_xlabel('Issues Abertas')
ax3.set_ylabel('Issues Fechadas')
ax3.set_title('Issues Abertas vs Fechadas')
ax3.set_xscale('log')
ax3.set_yscale('log')

# 4. Idade vs Estrelas
ax4.scatter(df['age_years'], df['stars'], alpha=0.6, color='red')
ax4.set_xlabel('Idade do Repositório (anos)')
ax4.set_ylabel('Número de Estrelas')
ax4.set_title('Idade vs Popularidade')

plt.tight_layout()
plt.savefig('Resultados/github_analysis_chart.png', dpi=300, bbox_inches='tight')
plt.show()

print("Gráfico salvo em: Resultados/github_analysis_chart.png")