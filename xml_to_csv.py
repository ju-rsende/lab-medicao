import xml.etree.ElementTree as ET
import csv
from datetime import datetime

def xml_to_csv(xml_file, csv_file):
    """Convert XML data to CSV format"""
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Open CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'name', 'owner', 'repo_name', 'stars', 'created_at', 'updated_at',
            'primary_language', 'releases', 'open_issues', 'closed_issues',
            'closed_issues_ratio', 'merged_pull_requests', 'age_years', 'days_since_update'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each repository
        for repo in root.findall('repository'):
            # Extract basic data
            created_at = repo.find('created_at').text
            updated_at = repo.find('updated_at').text
            
            # Calculate age and days since update
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            current_date = datetime.now(created_date.tzinfo)
            
            age_years = (current_date - created_date).days / 365.25
            days_since_update = (current_date - updated_date).days
            
            # Write row to CSV
            writer.writerow({
                'name': repo.find('name').text,
                'owner': repo.find('owner').text,
                'repo_name': repo.find('repo_name').text,
                'stars': int(repo.find('stars').text),
                'created_at': created_at,
                'updated_at': updated_at,
                'primary_language': repo.find('primary_language').text,
                'releases': int(repo.find('releases').text),
                'open_issues': int(repo.find('open_issues').text),
                'closed_issues': int(repo.find('closed_issues').text),
                'closed_issues_ratio': float(repo.find('closed_issues_ratio').text),
                'merged_pull_requests': int(repo.find('merged_pull_requests').text),
                'age_years': round(age_years, 2),
                'days_since_update': days_since_update
            })
    
    print(f"Arquivo CSV gerado: {csv_file}")

if __name__ == "__main__":
    # Convert 1000 repositories
    xml_to_csv("Resultados/top_1000_repositories.xml", "github_1000_repositories.csv")
    
    # Convert 100 repositories
    xml_to_csv("Resultados/top_100_repositories.xml", "github_100_repositories.csv")