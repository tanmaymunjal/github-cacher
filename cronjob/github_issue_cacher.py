import configparser
from github_connector.github import GithubConnector
from weaviate_connector.weaviate_client import Weaviate
from indexed_repos import index_repos
import hashlib

config = configparser.ConfigParser()
config.read("../config.ini")

weaviate_cluster_url = config["WEAVIATE"]["CLUSTER_URL"]
weaviate_bearer_token = config["WEAVIATE"]["BEARER_TOKEN"]
open_ai_api_key = config["OPENAI"]["API_KEY"]
github_key = config["GITHUB"]["BEARER_TOKEN"]
github_url = config["GITHUB"]["GITHUB_URL"]
github = GithubConnector(github_key, github_url)
weaviate_client = Weaviate(weaviate_cluster_url, weaviate_bearer_token, open_ai_api_key)

for repo in index_repos:
    issues = github.get_issues_by_repo(repo)
    for issue in issues:
        issue_id = hashlib.sha256(issue["html_url"].encode("utf-8")).hexdigest()
        issue["id"] = issue_id
        try:
            weaviate_client.create_issue(issue)
        except:
            weaviate_client.update_issue(issue_id, issue["title"], issue["description"])
