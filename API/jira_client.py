import os
import requests
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv
load_dotenv()


JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def search_jql(jql: str, fields: str = "summary,status,labels,reporter"):
    """
    Uses NEW Jira API: /rest/api/3/search/jql
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"

    params = {
        "jql": jql,
        "maxResults": 200,
        "fields": fields
    }

    response = requests.get(url, headers=headers, params=params, auth=auth)
    response.raise_for_status()

    data = response.json()
    issues = data.get("issues", [])

    return [
        {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "labels": issue["fields"].get("labels", []),
            "reporter": issue["fields"]["reporter"]["displayName"]
        }
        for issue in issues
    ]
