import requests
from requests.auth import HTTPBasicAuth

class JiraApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_issue_details(self, email, token, issue_key):
        url = f"{self.base_url}/issue/{issue_key}"
        print(f"[JiraApi] Consultando estória: {url}")

        auth = HTTPBasicAuth(email, token)
        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, auth=auth)
            print(f"[JiraApi] Status Code: {response.status_code}")
            print(f"[JiraApi] Response Text: {response.text}")

            if response.status_code == 200:
                return response.json()  # retorna o dicionário da estória
            else:
                return None
        except Exception as e:
            print(f"[JiraApi] Erro: {e}")
            return None
        
def create_bulk_subtasks(self, email, token, project_key, parent_key, tasks):
    """
    tasks: lista de strings ou dicts com título da subtask
    """
    from requests.auth import HTTPBasicAuth
    import requests

    url = f"{self.base_url}/rest/api/3/issue/bulk"

    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    issue_updates = []
    for task in tasks:
        summary = task.get("summary")
        if not summary:
            continue

        issue_updates.append({
            "fields": {
                "summary": summary,
                "issuetype": { "name": "Sub-task" },
                "project": { "key": project_key },
                "parent": { "key": parent_key }
            }
        })

    payload = {
        "issueUpdates": issue_updates
    }

    response = requests.post(url, headers=headers, auth=auth, json=payload)
    print(f"[JiraAPI] Status: {response.status_code}")
    print(f"[JiraAPI] Response: {response.text}")

    if response.status_code == 201:
        return True, response.json()
    else:
        return False, response.text


