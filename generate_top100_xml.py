import requests
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom

TOKEN = "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"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
URL = "https://api.github.com/graphql"

def run_query(query, variables=None, retries=3):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(retries):
        response = requests.post(URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                raise Exception(f"GraphQL errors: {data['errors']}")
            return data
        elif response.status_code in [502, 503, 504]:
            print(f"Erro {response.status_code}, tentando novamente ({attempt+1}/{retries})...")
            time.sleep(5)
        else:
            raise Exception(f"Query failed: {response.status_code} {response.text}")

    raise Exception(f"Query failed after {retries} attempts")

def get_top_repo_ids(total_repos=100):
    repos = []
    cursor = None
    per_page = 100

    while len(repos) < total_repos:
        query = """
        query($cursor: String, $perPage: Int!) {
          search(query: "stars:>1 sort:stars-desc is:public", type: REPOSITORY, first: $perPage, after: $cursor) {
            pageInfo { endCursor hasNextPage }
            edges {
              node {
                ... on Repository {
                  name
                  owner { login }
                }
              }
            }
          }
        }
        """
        variables = {"cursor": cursor, "perPage": per_page}
        result = run_query(query, variables)
        search = result["data"]["search"]

        for edge in search["edges"]:
            repos.append(edge["node"])
            if len(repos) >= total_repos:
                break

        if not search["pageInfo"]["hasNextPage"]:
            break
        cursor = search["pageInfo"]["endCursor"]

    return repos[:total_repos]

def get_repo_details(owner, name):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        stargazerCount
        createdAt
        updatedAt
        primaryLanguage { name }
        releases { totalCount }
        issues(states: OPEN) { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        pullRequests(states: MERGED) { totalCount }
      }
    }
    """
    variables = {"owner": owner, "name": name}
    result = run_query(query, variables)
    return result["data"]["repository"]

def collect_and_generate_xml():
    repos = get_top_repo_ids(100)
    
    # Criar elemento raiz
    root = ET.Element("repositories")
    root.set("total", str(len(repos)))
    root.set("generated_at", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    for repo in repos:
        details = get_repo_details(repo["owner"]["login"], repo["name"])
        primary_language = details['primaryLanguage']['name'] if details['primaryLanguage'] else 'Unknown'
        open_issues = details['issues']['totalCount']
        closed_issues = details['closedIssues']['totalCount']
        total_issues = open_issues + closed_issues
        closed_ratio = (closed_issues / total_issues) if total_issues > 0 else 0
        
        # Criar elemento repositório
        repo_elem = ET.SubElement(root, "repository")
        
        ET.SubElement(repo_elem, "name").text = f"{repo['owner']['login']}/{repo['name']}"
        ET.SubElement(repo_elem, "owner").text = repo['owner']['login']
        ET.SubElement(repo_elem, "repo_name").text = repo['name']
        ET.SubElement(repo_elem, "stars").text = str(details['stargazerCount'])
        ET.SubElement(repo_elem, "created_at").text = details['createdAt']
        ET.SubElement(repo_elem, "updated_at").text = details['updatedAt']
        ET.SubElement(repo_elem, "primary_language").text = primary_language
        ET.SubElement(repo_elem, "releases").text = str(details['releases']['totalCount'])
        ET.SubElement(repo_elem, "open_issues").text = str(open_issues)
        ET.SubElement(repo_elem, "closed_issues").text = str(closed_issues)
        ET.SubElement(repo_elem, "closed_issues_ratio").text = f"{closed_ratio:.2f}"
        ET.SubElement(repo_elem, "merged_pull_requests").text = str(details['pullRequests']['totalCount'])
        
        print(f"Processado: {repo['owner']['login']}/{repo['name']}")
    
    # Formatar XML
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    
    # Salvar arquivo
    with open("top_100_repositories.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
    
    print(f"\nArquivo XML gerado: top_100_repositories.xml")
    return root

if __name__ == "__main__":
    start_time = time.time()
    collect_and_generate_xml()
    print(f"Tempo total de execução: {time.time() - start_time:.2f} segundos")