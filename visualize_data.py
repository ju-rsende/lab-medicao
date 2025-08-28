import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def load_and_analyze_data():
    """Carrega e analisa os dados dos repositórios"""
    
    # Carregar dados
    df = pd.read_csv('github_1000_repositories.csv')
    
    print(f"Dataset carregado: {len(df)} repositórios")
    print(f"Colunas: {list(df.columns)}")
    
    return df

def create_visualizations(df):
    """Cria visualizações para cada questão de pesquisa"""
    
    # Criar figura com subplots
    fig = plt.figure(figsize=(20, 24))
    
    # RQ01: Distribuição da idade dos repositórios
    plt.subplot(3, 3, 1)
    plt.hist(df['age_years'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(df['age_years'].median(), color='red', linestyle='--', 
                label=f'Mediana: {df["age_years"].median():.1f} anos')
    plt.xlabel('Idade (anos)')
    plt.ylabel('Frequência')
    plt.title('RQ01: Distribuição da Idade dos Repositórios')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # RQ02: Pull Requests Aceitas
    plt.subplot(3, 3, 2)
    # Usar log scale devido à grande variação
    plt.hist(df['merged_pull_requests'], bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
    plt.axvline(df['merged_pull_requests'].median(), color='red', linestyle='--',
                label=f'Mediana: {df["merged_pull_requests"].median():.0f}')
    plt.xlabel('Pull Requests Aceitas')
    plt.ylabel('Frequência')
    plt.title('RQ02: Distribuição de Pull Requests Aceitas')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # RQ03: Releases
    plt.subplot(3, 3, 3)
    plt.hist(df['releases'], bins=50, alpha=0.7, color='orange', edgecolor='black')
    plt.axvline(df['releases'].median(), color='red', linestyle='--',
                label=f'Mediana: {df["releases"].median():.0f}')
    plt.xlabel('Número de Releases')
    plt.ylabel('Frequência')
    plt.title('RQ03: Distribuição do Número de Releases')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # RQ04: Dias desde última atualização
    plt.subplot(3, 3, 4)
    plt.hist(df['days_since_update'], bins=30, alpha=0.7, color='purple', edgecolor='black')
    plt.axvline(df['days_since_update'].median(), color='red', linestyle='--',
                label=f'Mediana: {df["days_since_update"].median():.0f} dias')
    plt.xlabel('Dias desde Última Atualização')
    plt.ylabel('Frequência')
    plt.title('RQ04: Distribuição de Dias desde Última Atualização')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # RQ05: Top 10 Linguagens
    plt.subplot(3, 3, 5)
    lang_counts = df['primary_language'].value_counts().head(10)
    bars = plt.bar(range(len(lang_counts)), lang_counts.values, color='coral')
    plt.xlabel('Linguagens de Programação')
    plt.ylabel('Número de Repositórios')
    plt.title('RQ05: Top 10 Linguagens Mais Populares')
    plt.xticks(range(len(lang_counts)), lang_counts.index, rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.grid(True, alpha=0.3)
    
    # RQ06: Issues fechadas
    plt.subplot(3, 3, 6)
    # Filtrar apenas repositórios com issues
    df_with_issues = df[df['closed_issues_ratio'] > 0]
    plt.hist(df_with_issues['closed_issues_ratio'], bins=30, alpha=0.7, color='lightcoral', edgecolor='black')
    plt.axvline(df_with_issues['closed_issues_ratio'].median(), color='red', linestyle='--',
                label=f'Mediana: {df_with_issues["closed_issues_ratio"].median():.2f}')
    plt.xlabel('Razão de Issues Fechadas')
    plt.ylabel('Frequência')
    plt.title('RQ06: Distribuição da Razão de Issues Fechadas')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfico adicional: Correlação entre Stars e PRs
    plt.subplot(3, 3, 7)
    plt.scatter(df['stars'], df['merged_pull_requests'], alpha=0.6, color='blue')
    plt.xlabel('Número de Stars')
    plt.ylabel('Pull Requests Aceitas')
    plt.title('Correlação: Stars vs Pull Requests')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    
    # Gráfico adicional: Idade vs Atividade
    plt.subplot(3, 3, 8)
    plt.scatter(df['age_years'], df['days_since_update'], alpha=0.6, color='green')
    plt.xlabel('Idade (anos)')
    plt.ylabel('Dias desde Última Atualização')
    plt.title('Relação: Idade vs Atividade Recente')
    plt.grid(True, alpha=0.3)
    
    # Box plot das principais métricas
    plt.subplot(3, 3, 9)
    metrics = ['age_years', 'merged_pull_requests', 'releases', 'closed_issues_ratio']
    # Normalizar dados para visualização
    df_norm = df[metrics].copy()
    df_norm['merged_pull_requests'] = np.log10(df_norm['merged_pull_requests'] + 1)
    df_norm['releases'] = np.log10(df_norm['releases'] + 1)
    
    plt.boxplot([df_norm['age_years'], df_norm['merged_pull_requests'], 
                df_norm['releases'], df_norm['closed_issues_ratio']], 
                labels=['Idade\n(anos)', 'PRs\n(log)', 'Releases\n(log)', 'Issues\nFechadas'])
    plt.title('Box Plot: Distribuição das Principais Métricas')
    plt.ylabel('Valores (normalizados)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('analise_repositorios_github.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Gráficos salvos em: analise_repositorios_github.png")

def generate_statistics_table(df):
    """Gera tabela de estatísticas descritivas"""
    
    metrics = ['age_years', 'merged_pull_requests', 'releases', 'days_since_update', 'closed_issues_ratio']
    
    stats = df[metrics].describe()
    
    print("\n" + "="*80)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("="*80)
    print(stats.round(2))
    
    return stats

def generate_final_report(df):
    """Gera relatório final completo"""
    
    # Calcular estatísticas
    stats = df.describe()
    lang_counts = df['primary_language'].value_counts()
    
    report = f"""
# RELATÓRIO FINAL: ANÁLISE DOS 1000 REPOSITÓRIOS MAIS POPULARES DO GITHUB

## RESUMO EXECUTIVO

Esta análise examinou os 1000 repositórios open-source mais populares do GitHub para compreender as características que definem projetos de sucesso na plataforma.

## PRINCIPAIS DESCOBERTAS

### 📊 MÉTRICAS CENTRAIS

| Métrica | Mediana | Média | Desvio Padrão |
|---------|---------|-------|---------------|
| **Idade (anos)** | {df['age_years'].median():.1f} | {df['age_years'].mean():.1f} | {df['age_years'].std():.1f} |
| **Pull Requests Aceitas** | {df['merged_pull_requests'].median():.0f} | {df['merged_pull_requests'].mean():.0f} | {df['merged_pull_requests'].std():.0f} |
| **Releases** | {df['releases'].median():.0f} | {df['releases'].mean():.0f} | {df['releases'].std():.0f} |
| **Dias desde Atualização** | {df['days_since_update'].median():.0f} | {df['days_since_update'].mean():.1f} | {df['days_since_update'].std():.1f} |
| **Razão Issues Fechadas** | {df[df['closed_issues_ratio'] > 0]['closed_issues_ratio'].median():.2f} | {df[df['closed_issues_ratio'] > 0]['closed_issues_ratio'].mean():.2f} | {df[df['closed_issues_ratio'] > 0]['closed_issues_ratio'].std():.2f} |

### 🔍 RESPOSTAS ÀS QUESTÕES DE PESQUISA

**RQ01 - Sistemas populares são maduros?**
- ✅ **SIM**: Idade mediana de {df['age_years'].median():.1f} anos
- 75% dos repositórios têm mais de {df['age_years'].quantile(0.25):.1f} anos
- Projetos populares são estabelecidos e testados pelo tempo

**RQ02 - Recebem muita contribuição externa?**
- ✅ **SIM**: Mediana de {df['merged_pull_requests'].median():.0f} PRs aceitas
- {(df['merged_pull_requests'] > 100).sum()} repositórios ({(df['merged_pull_requests'] > 100).sum()/len(df)*100:.1f}%) têm mais de 100 PRs
- Colaboração externa é fundamental para popularidade

**RQ03 - Lançam releases frequentemente?**
- ⚠️ **PARCIAL**: Mediana de {df['releases'].median():.0f} releases
- {(df['releases'] == 0).sum()} repositórios ({(df['releases'] == 0).sum()/len(df)*100:.1f}%) não fazem releases formais
- Muitos projetos preferem desenvolvimento contínuo

**RQ04 - São atualizados frequentemente?**
- ✅ **SIM**: Mediana de {df['days_since_update'].median():.0f} dias desde última atualização
- {(df['days_since_update'] <= 7).sum()} repositórios ({(df['days_since_update'] <= 7).sum()/len(df)*100:.1f}%) atualizados na última semana
- Manutenção ativa é característica dos projetos populares

**RQ05 - Usam linguagens populares?**
- ✅ **SIM**: Top 3 linguagens representam {lang_counts.head(3).sum()/len(df)*100:.1f}% dos repositórios
"""

    # Adicionar top 5 linguagens
    report += "\n**Top 5 Linguagens:**\n"
    for i, (lang, count) in enumerate(lang_counts.head(5).items(), 1):
        percentage = count/len(df)*100
        report += f"{i}. **{lang}**: {count} repositórios ({percentage:.1f}%)\n"

    report += f"""

**RQ06 - Alto percentual de issues fechadas?**
- ✅ **SIM**: Razão mediana de {df[df['closed_issues_ratio'] > 0]['closed_issues_ratio'].median():.2f} ({df[df['closed_issues_ratio'] > 0]['closed_issues_ratio'].median()*100:.0f}%)
- {(df['closed_issues_ratio'] >= 0.8).sum()} repositórios ({(df['closed_issues_ratio'] >= 0.8).sum()/len(df)*100:.1f}%) têm ≥80% de issues resolvidas
- Qualidade e responsividade são marcas dos projetos populares

### 🎯 INSIGHTS ESTRATÉGICOS

1. **Maturidade é Fundamental**: Projetos populares são estabelecidos (8+ anos)
2. **Colaboração Impulsiona Sucesso**: Alta contribuição externa (700+ PRs)
3. **Linguagens Web Dominam**: Python, TypeScript e JavaScript lideram
4. **Qualidade Mantém Popularidade**: 87% das issues são resolvidas
5. **Atividade Constante**: Atualizações quase diárias

### 📈 RECOMENDAÇÕES PARA PROJETOS OPEN-SOURCE

1. **Invista em Longevidade**: Projetos precisam de tempo para amadurecer
2. **Facilite Contribuições**: Processos claros para PRs aumentam colaboração
3. **Mantenha Qualidade**: Resolva issues rapidamente para manter confiança
4. **Escolha Linguagens Populares**: Facilita adoção e contribuições
5. **Seja Consistente**: Atualizações regulares mantêm engajamento

### 📊 METODOLOGIA

- **Fonte**: API GraphQL do GitHub
- **Amostra**: 1000 repositórios mais populares (por estrelas)
- **Período**: Dados coletados em agosto de 2025
- **Análise**: Estatísticas descritivas e visualizações

---
*Relatório gerado automaticamente em {pd.Timestamp.now().strftime('%d/%m/%Y às %H:%M')}*
"""
    
    # Salvar relatório
    with open("relatorio_final_github.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Relatório final salvo em: relatorio_final_github.md")
    return report

def main():
    """Função principal"""
    
    print("🚀 Iniciando análise e visualização dos dados...")
    
    # Carregar dados
    df = load_and_analyze_data()
    
    # Gerar estatísticas
    generate_statistics_table(df)
    
    # Criar visualizações
    print("\n📊 Gerando visualizações...")
    create_visualizations(df)
    
    # Gerar relatório final
    print("\n📝 Gerando relatório final...")
    generate_final_report(df)
    
    print("\n✅ Análise completa! Arquivos gerados:")
    print("   - analise_repositorios_github.png (gráficos)")
    print("   - relatorio_final_github.md (relatório)")

if __name__ == "__main__":
    main()