import pandas as pd
import dotenv
import os

from github import Github, GithubException, Auth, RateLimitExceededException
from urllib.parse import urlparse
from collections import deque

dotenv.load_dotenv(override=True)

df = pd.read_csv("data/rogue.csv", encoding="utf-8")

# Extract owner/repo from GitHub URLs (supports comma-separated URLs)
def extract_repo_from_url(repo_str):
    """
    Extract owner/repo from one or more GitHub URLs.
    Returns a list of repos (1-n elements).

    Args:
        repo_str: Single URL or comma-separated URLs
    Returns:
        List of owner/repo strings (e.g., ['owner1/repo1', 'owner2/repo2'])
    """
    if pd.isna(repo_str):
        return []

    # Split by comma to handle multiple URLs
    urls = [url.strip() for url in str(repo_str).split(',')]
    repos = []

    for url in urls:
        if not url:
            continue

        if url.startswith('http'):
            parsed = urlparse(url)
            parts = parsed.path.strip('/').split('/')
            if len(parts) >= 2:
                repos.append(f"{parts[0]}/{parts[1]}")
        else:
            # Already in owner/repo format
            repos.append(url)

    return repos

# Extract repos and expand rows with multiple repos
df['github_repos_list'] = df['github repo'].apply(extract_repo_from_url)

# Explode the DataFrame so each repo gets its own row
df_expanded = df.explode('github_repos_list').reset_index(drop=True)

# Filter out rows with no valid repos
df_expanded = df_expanded[df_expanded['github_repos_list'].notna() & (df_expanded['github_repos_list'] != '')]

# Create mapping from repo to harness name
linkage_name_mapping = dict(zip(df_expanded['github_repos_list'], df_expanded['harness name']))

# Collect all available GitHub tokens
github_tokens = {key: value for key, value in os.environ.items() if key.startswith('GITHUB_TOKEN_')}
print(f"Found {len(github_tokens)} unique GitHub token(s): {', '.join(github_tokens.keys())}")

# Create a rotating token manager
class TokenRotator:
    def __init__(self, tokens_dict):
        self.tokens = list(tokens_dict.items())  # [(name, value), ...]
        self.current_index = 0
        self.github_clients = {}  # Cache Github clients

    def get_current_token(self):
        """Get the current token name and value"""
        token_name, token_value = self.tokens[self.current_index]
        return token_name, token_value

    def get_github_client(self):
        """Get or create Github client for current token"""
        token_name, token_value = self.get_current_token()
        if token_name not in self.github_clients:
            self.github_clients[token_name] = Github(auth=Auth.Token(token_value))
        return self.github_clients[token_name], token_name

    def rotate(self):
        """Switch to the next token"""
        old_index = self.current_index
        self.current_index = (self.current_index + 1) % len(self.tokens)
        old_name = self.tokens[old_index][0]
        new_name = self.tokens[self.current_index][0]
        print(f"\n⟳ Rotating token: {old_name} → {new_name}")
        return self.current_index != old_index  # False if we've cycled through all

    def check_rate_limit(self, gh, token_name):
        """Check and display current rate limit status"""
        try:
            rate_limit = gh.get_rate_limit()
            core = rate_limit.core
            remaining = core.remaining
            total = core.limit
            reset_time = core.reset

            if remaining < 100:
                print(f"⚠ [{token_name}] Low rate limit: {remaining}/{total} remaining (resets at {reset_time})")
                return True
            return False
        except Exception as e:
            print(f"⚠ [{token_name}] Could not check rate limit: {e}")
            return False

def fetch_issues_pygithub(gh, owner, repo, token_name):
    """Fetch all issues from a repository using PyGithub"""
    issues_data = []
    page_num = 0

    try:
        repository = gh.get_repo(f"{owner}/{repo}")
        issues = repository.get_issues(state='all', sort='created', direction='desc')

        for issue in issues:
            # Skip pull requests
            if issue.pull_request:
                continue

            page_num += 1

            # Collect cross-referenced issues/PRs
            cross_referenced_urls = []
            try:
                for event in issue.get_timeline():
                    if str(event.event) == 'cross-referenced':
                        # Get the source issue/PR that referenced this issue
                        if hasattr(event, 'source') and event.source:
                            if hasattr(event.source, 'issue') and event.source.issue:
                                cross_referenced_urls.append(event.source.issue.html_url)
            except Exception as e:
                # If timeline fails, just continue with empty list
                print(f"[{token_name}] ⚠ Could not fetch timeline for issue {issue.number}: {e}")

            issues_data.append({
                'github_repo': f"{owner}/{repo}",
                'issue_title': issue.title,
                'issue_body': issue.body,
                'issue_created_at': issue.created_at.isoformat() if issue.created_at else None,
                'issue_closed_at': issue.closed_at.isoformat() if issue.closed_at else None,
                'issue_url': issue.html_url,
                'issue_labels': [label.name for label in issue.labels],
                'issue_comments': issue.comments,
                'issue_cross_referenced': cross_referenced_urls,
            })

            if page_num % 50 == 0:
                print(f"[{token_name}] {owner}/{repo}: Fetched {page_num} issues...")

        return issues_data, False  # False = no rate limit hit

    except RateLimitExceededException as e:
        print(f"[{token_name}] ⚠ {owner}/{repo}: Rate limit exceeded!")
        return issues_data, True  # True = rate limit hit
    except GithubException as e:
        if e.status == 404:
            print(f"[{token_name}] ✗ {owner}/{repo}: Repository not found (HTTP 404)")
        elif e.status == 403:
            # Check if it's a rate limit issue
            if 'rate limit' in str(e).lower():
                print(f"[{token_name}] ⚠ {owner}/{repo}: Rate limit exceeded (HTTP 403)")
                return issues_data, True  # Rate limit hit
            else:
                print(f"[{token_name}] ✗ {owner}/{repo}: Access denied (HTTP 403)")
        else:
            print(f"[{token_name}] ✗ {owner}/{repo}: Error (HTTP {e.status})")
        return issues_data, False
    except Exception as e:
        print(f"[{token_name}] ✗ {owner}/{repo}: Unexpected error: {e}")
        return issues_data, False

# Mine all issues sequentially with token rotation
all_issues_data = []
repos_list = list(linkage_name_mapping.items())
repos_queue = deque(repos_list)

print(f"\nProcessing {len(repos_list)} repositories sequentially with {len(github_tokens)} token(s)")
print("=" * 80)

# Initialize token rotator
token_rotator = TokenRotator(github_tokens)

processed_count = 0
failed_repos = []

while repos_queue:
    repo_name, harness_name = repos_queue.popleft()

    try:
        owner, repo = repo_name.split('/')
        gh, token_name = token_rotator.get_github_client()

        print(f"\n[{token_name}] [{processed_count + 1}/{len(repos_list)}] Processing {repo_name}...")

        # Fetch issues for this repo
        issues_data, rate_limit_hit = fetch_issues_pygithub(gh, owner, repo, token_name)

        # If rate limit was hit, rotate token and retry this repo
        if rate_limit_hit:
            token_rotator.rotate()
            # Put the repo back at the front of the queue to retry
            repos_queue.appendleft((repo_name, harness_name))
            print(f"↻ Retrying {repo_name} with new token...")
            continue

        # Add harness name to each issue
        for issue in issues_data:
            issue['harness_name'] = harness_name
            all_issues_data.append(issue)

        if issues_data:
            print(f"[{token_name}] ✓ {repo_name}: {len(issues_data)} issues collected")
        else:
            print(f"[{token_name}] ○ {repo_name}: 0 issues found")

        processed_count += 1

        # Periodically check rate limit
        if processed_count % 10 == 0:
            token_rotator.check_rate_limit(gh, token_name)

    except ValueError:
        print(f"✗ Invalid repo format: {repo_name}")
        failed_repos.append(repo_name)
        processed_count += 1
    except Exception as e:
        print(f"✗ Unexpected error processing {repo_name}: {e}")
        failed_repos.append(repo_name)
        processed_count += 1

print("\n" + "=" * 80)
print(f"✓ Processed: {processed_count}/{len(repos_list)} repositories")
if failed_repos:
    print(f"✗ Failed: {len(failed_repos)} repositories")
    print(f"  Failed repos: {', '.join(failed_repos[:5])}{'...' if len(failed_repos) > 5 else ''}")

# Create DataFrame and save to JSONL
issues_df = pd.DataFrame(all_issues_data)
if not issues_df.empty:
    issues_df = issues_df[['harness_name', 'github_repo', 'issue_title', 'issue_body',
                            'issue_labels', 'issue_created_at', 'issue_closed_at',
                            'issue_comments', 'issue_url', 'issue_cross_referenced']]
    issues_df.to_json("data/github_issues.jsonl", orient="records", lines=True, force_ascii=False)
    print(f"\n✓ Total issues fetched: {len(issues_df)}")
    print("✓ Issues saved to data/github_issues.jsonl")
else:
    print("\n✗ No issues fetched")