import xml.etree.ElementTree as ET
from datetime import datetime
import statistics
from collections import Counter

def parse_xml_data(filename):
    """Parse XML file and extract repository data"""
    tree = ET.parse(filename)
    root = tree.getroot()
    
    repositories = []
    for repo in root.findall('repository'):
        data = {
            'name': repo.find('name').text,
            'stars': int(repo.find('stars').text),
            'created_at': repo.find('created_at').text,
            'updated_at': repo.find('updated_at').text,
            'primary_language': repo.find('primary_language').text,
            'releases': int(repo.find('releases').text),
            'open_issues': int(repo.find('open_issues').text),
            'closed_issues': int(repo.find('closed_issues').text),
            'closed_issues_ratio': float(repo.find('closed_issues_ratio').text),
            'merged_pull_requests': int(repo.find('merged_pull_requests').text)
        }
        repositories.append(data)
    
    return repositories

def calculate_age_in_years(created_at):
    """Calculate repository age in years"""
    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    current_date = datetime.now(created_date.tzinfo)
    age_years = (current_date - created_date).days / 365.25
    return age_years

def calculate_days_since_update(updated_at):
    """Calculate days since last update"""
    updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
    current_date = datetime.now(updated_date.tzinfo)
    days_since = (current_date - updated_date).days
    return days_since

def analyze_repositories(repositories):
    """Analyze repository data and answer research questions"""
    
    print("=" * 80)
    print("ANÁLISE DOS 1000 REPOSITÓRIOS MAIS POPULARES DO GITHUB")
    print("=" * 80)
    
    # RQ01: Idade dos repositórios
    ages = [calculate_age_in_years(repo['created_at']) for repo in repositories]
    median_age = statistics.median(ages)
    
    print(f"\nRQ01 - Sistemas populares são maduros/antigos?")
    print(f"Idade mediana: {median_age:.1f} anos")
    print(f"Idade mínima: {min(ages):.1f} anos")
    print(f"Idade máxima: {max(ages):.1f} anos")
    
    # RQ02: Pull requests aceitas
    pull_requests = [repo['merged_pull_requests'] for repo in repositories]
    median_prs = statistics.median(pull_requests)
    
    print(f"\nRQ02 - Sistemas populares recebem muita contribuição externa?")
    print(f"Pull requests aceitas (mediana): {median_prs}")
    print(f"Pull requests aceitas (mínimo): {min(pull_requests)}")
    print(f"Pull requests aceitas (máximo): {max(pull_requests)}")
    
    # RQ03: Releases
    releases = [repo['releases'] for repo in repositories]
    median_releases = statistics.median(releases)
    
    print(f"\nRQ03 - Sistemas populares lançam releases com frequência?")
    print(f"Total de releases (mediana): {median_releases}")
    print(f"Total de releases (mínimo): {min(releases)}")
    print(f"Total de releases (máximo): {max(releases)}")
    
    # RQ04: Tempo desde última atualização
    days_since_update = [calculate_days_since_update(repo['updated_at']) for repo in repositories]
    median_days = statistics.median(days_since_update)
    
    print(f"\nRQ04 - Sistemas populares são atualizados com frequência?")
    print(f"Dias desde última atualização (mediana): {median_days}")
    print(f"Dias desde última atualização (mínimo): {min(days_since_update)}")
    print(f"Dias desde última atualização (máximo): {max(days_since_update)}")
    
    # RQ05: Linguagens mais populares
    languages = [repo['primary_language'] for repo in repositories]
    language_counts = Counter(languages)
    
    print(f"\nRQ05 - Sistemas populares são escritos nas linguagens mais populares?")
    print("Top 10 linguagens:")
    for lang, count in language_counts.most_common(10):
        percentage = (count / len(repositories)) * 100
        print(f"  {lang}: {count} repositórios ({percentage:.1f}%)")
    
    # RQ06: Percentual de issues fechadas
    closed_ratios = [repo['closed_issues_ratio'] for repo in repositories if repo['closed_issues_ratio'] > 0]
    median_closed_ratio = statistics.median(closed_ratios)
    
    print(f"\nRQ06 - Sistemas populares possuem um alto percentual de issues fechadas?")
    print(f"Razão de issues fechadas (mediana): {median_closed_ratio:.2f}")
    print(f"Razão de issues fechadas (mínima): {min(closed_ratios):.2f}")
    print(f"Razão de issues fechadas (máxima): {max(closed_ratios):.2f}")
    
    # Estatísticas adicionais
    print(f"\n" + "=" * 80)
    print("ESTATÍSTICAS ADICIONAIS")
    print("=" * 80)
    
    # Repositórios sem issues
    repos_no_issues = len([r for r in repositories if r['open_issues'] + r['closed_issues'] == 0])
    print(f"Repositórios sem issues: {repos_no_issues} ({(repos_no_issues/len(repositories)*100):.1f}%)")
    
    # Repositórios sem releases
    repos_no_releases = len([r for r in repositories if r['releases'] == 0])
    print(f"Repositórios sem releases: {repos_no_releases} ({(repos_no_releases/len(repositories)*100):.1f}%)")
    
    # Repositórios sem PRs
    repos_no_prs = len([r for r in repositories if r['merged_pull_requests'] == 0])
    print(f"Repositórios sem PRs aceitas: {repos_no_prs} ({(repos_no_prs/len(repositories)*100):.1f}%)")

def generate_report(repositories):
    """Generate detailed analysis report"""
    
    report = """
# RELATÓRIO DE ANÁLISE DOS 1000 REPOSITÓRIOS MAIS POPULARES DO GITHUB

## 1. INTRODUÇÃO

Este relatório apresenta uma análise das características dos 1000 repositórios open-source mais populares do GitHub, baseado no número de estrelas. O objetivo é compreender os padrões de desenvolvimento, manutenção e popularidade desses projetos.

### Hipóteses Informais:
- **H1**: Repositórios populares tendem a ser projetos maduros (mais antigos)
- **H2**: Repositórios populares recebem muitas contribuições externas (alto número de PRs)
- **H3**: Repositórios populares lançam releases frequentemente
- **H4**: Repositórios populares são atualizados regularmente (baixo tempo desde última atualização)
- **H5**: Repositórios populares usam linguagens mainstream (JavaScript, Python, Java)
- **H6**: Repositórios populares mantêm boa qualidade (alto percentual de issues fechadas)

## 2. METODOLOGIA

Os dados foram coletados através da API GraphQL do GitHub, obtendo informações sobre:
- Data de criação e última atualização
- Número de pull requests aceitas
- Total de releases
- Linguagem primária
- Issues abertas e fechadas

A análise utilizou valores medianos para reduzir o impacto de outliers.

## 3. RESULTADOS

"""
    
    # Calcular métricas
    ages = [calculate_age_in_years(repo['created_at']) for repo in repositories]
    pull_requests = [repo['merged_pull_requests'] for repo in repositories]
    releases = [repo['releases'] for repo in repositories]
    days_since_update = [calculate_days_since_update(repo['updated_at']) for repo in repositories]
    languages = [repo['primary_language'] for repo in repositories]
    closed_ratios = [repo['closed_issues_ratio'] for repo in repositories if repo['closed_issues_ratio'] > 0]
    
    language_counts = Counter(languages)
    
    report += f"""
### RQ01 - Maturidade dos Sistemas
- **Idade mediana**: {statistics.median(ages):.1f} anos
- **Resultado**: Repositórios populares são relativamente maduros

### RQ02 - Contribuição Externa
- **PRs aceitas (mediana)**: {statistics.median(pull_requests):.0f}
- **Resultado**: Alto nível de contribuição externa

### RQ03 - Frequência de Releases
- **Releases (mediana)**: {statistics.median(releases):.0f}
- **Resultado**: Muitos projetos não fazem releases formais

### RQ04 - Frequência de Atualizações
- **Dias desde última atualização (mediana)**: {statistics.median(days_since_update):.0f}
- **Resultado**: Projetos são atualizados regularmente

### RQ05 - Linguagens Populares
**Top 5 linguagens:**
"""
    
    for lang, count in language_counts.most_common(5):
        percentage = (count / len(repositories)) * 100
        report += f"- {lang}: {count} repositórios ({percentage:.1f}%)\n"
    
    report += f"""
### RQ06 - Qualidade (Issues Fechadas)
- **Razão de issues fechadas (mediana)**: {statistics.median(closed_ratios):.2f}
- **Resultado**: Alto percentual de resolução de issues

## 4. DISCUSSÃO

### Confirmação das Hipóteses:
- **H1 ✓**: Confirmada - idade mediana de {statistics.median(ages):.1f} anos indica maturidade
- **H2 ✓**: Confirmada - mediana de {statistics.median(pull_requests):.0f} PRs indica alta colaboração
- **H3 ✗**: Parcialmente refutada - muitos projetos não fazem releases formais
- **H4 ✓**: Confirmada - atualizações recentes indicam manutenção ativa
- **H5 ✓**: Confirmada - JavaScript e TypeScript dominam
- **H6 ✓**: Confirmada - alta razão de issues fechadas ({statistics.median(closed_ratios):.2f})

### Insights Principais:
1. Repositórios populares são projetos estabelecidos e bem mantidos
2. A colaboração externa é fundamental para o sucesso
3. Linguagens web (JS/TS) dominam o ecossistema open-source
4. A qualidade é mantida através da resolução eficiente de issues
"""
    
    # Salvar relatório
    with open("relatorio_analise.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nRelatório detalhado salvo em: relatorio_analise.md")

if __name__ == "__main__":
    # Analisar dados dos 1000 repositórios
    repositories = parse_xml_data("Resultados/top_1000_repositories.xml")
    analyze_repositories(repositories)
    generate_report(repositories)
