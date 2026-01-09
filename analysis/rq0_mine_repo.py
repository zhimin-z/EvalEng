import pandas as pd
import dotenv
from github import Github, Auth
import time
import os
from tqdm import tqdm

dotenv.load_dotenv(override=True)

auth = Auth.Token(os.getenv('GITHUB_TOKEN_1'))
g = Github(auth=auth)

df = pd.read_csv("data/rq0_harness_metadata.csv", encoding="utf-8")

# Initialize list to collect repo metadata
repo_metadata_list = []

print(f"Processing {len(df)} repositories...")

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Fetching repo info"):
    repo_url = row['github repo'].split(',')[0].strip() if pd.notna(row['github repo']) else ''
    
    if repo_url and repo_url.startswith('https://github.com/'):
        try:
            repo_name = repo_url.replace("https://github.com/", "").strip()
            repo = g.get_repo(repo_name)
            
            repo_dict = {
                'harness name': row['harness name'],
                'github repo': repo_url,
                'creation date': repo.created_at,
                'major programming language': "Python" if repo.language == 'Jupyter Notebook' else repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'commits': repo.get_commits().totalCount,
                'contributors': repo.get_contributors().totalCount
            }
            repo_metadata_list.append(repo_dict)
                
        except Exception as e:
            print(f"\nError fetching info for {repo_name}: {e}")
    
    time.sleep(0.1)  # Be nice to the API

# Create dataframe from collected metadata and save
df_repo = pd.DataFrame(repo_metadata_list)
df_repo.to_csv("../data/rq0_harness_repo.csv", index=False, encoding="utf-8")