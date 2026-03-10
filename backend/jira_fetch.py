import requests
from requests.auth import HTTPBasicAuth
import psycopg2

JIRA_URL = "https://your-domain.atlassian.net"
EMAIL = "your-email"
TOKEN = "your-api-token"

url = f"{JIRA_URL}/rest/api/3/search/jql"

query = {
    "jql": "created >= -30d ORDER BY created DESC",
    "maxResults": 50
}

auth = HTTPBasicAuth(EMAIL, TOKEN)

headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers, params=query, auth=auth)

if response.status_code != 200:
    print("Failed to fetch Jira data:", response.text)
    exit()

data = response.json()

conn = psycopg2.connect(
    database="jira_reports",
    user="postgres",
    password="sassy",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

for issue in data["issues"]:
    issue_id = issue["id"]
    status = issue["fields"]["status"]["name"]

    assignee = "Unassigned"

    if issue["fields"]["assignee"]:
        assignee = issue["fields"]["assignee"]["displayName"]

    cur.execute(
        "INSERT INTO issues (id,status,assignee) VALUES (%s,%s,%s)",
        (issue_id, status, assignee)
    )

conn.commit()

print("Jira data inserted successfully")

cur.close()
conn.close()