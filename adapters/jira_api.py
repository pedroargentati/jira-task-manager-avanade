import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPBasicAuth
import requests

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
            self.print_response(response)

            print(f"[JiraApi] Status Code: {response.status_code}")
            print(f"[JiraApi] Response Text: {response.text}")

            if response.status_code == 200:
                return response.json()  # retorna o dicionário da estória
            else:
                return None
        except Exception as e:
            print(f"[JiraApi] Erro: {e}")
            return None
        
    def get_project_id(self, email, token, project_key):
        from requests.auth import HTTPBasicAuth
        import requests

        url = f"{self.base_url}/project/{project_key}"
        auth = HTTPBasicAuth(email, token)
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, auth=auth)
        self.print_response(response)
        if response.status_code == 200:
            project_data = response.json()
            return project_data.get("id")  # retorna o ID do projeto
        else:
            print(f"Erro ao buscar ID do projeto: {response.status_code}")
            print(response.text)
            return None

        
    def create_bulk_subtasks(self, email, token, project_id, parent_key, tasks):
        """
        Cria subtasks em lote via Jira API.
        """
        url = f"{self.base_url}/issue/bulk"
        auth = HTTPBasicAuth(email, token)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Atlassian-Token": "no-check"  # <- evita erro XSRF no Electron/local
        }

        issue_updates = []
        for task in tasks:
            summary = task.get("summary")
            description = task.get("description", "")
            if not summary:
                print(f"[JiraApi] Ignorando task sem título: {task}")
                continue

            issue_updates.append({
                "fields": {
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": description}]
                            }
                        ]
                    },
                    "issuetype": {"id": 10010},  # Sub-task ID (ajuste se necessário)
                    "project": {"id": project_id},
                    "parent": {"key": parent_key}
                }
            })

        payload = {
            "issueUpdates": issue_updates
        }

        response = requests.post(url, headers=headers, auth=auth, json=payload)
        self.print_response(response)

        if response.status_code == 201:
            return True, response.json()
        else:
            return False, response.text


    def update_subtask(self, email, token, issue_key, summary, description):
        url = f"{self.base_url}/issue/{issue_key}"
        auth = HTTPBasicAuth(email, token)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "fields": {
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": description}
                            ]
                        }
                    ]
                }
            }
        }

        response = requests.put(url, json=payload, headers=headers, auth=auth)
        self.print_response(response)
        return response.status_code == 204


    def print_response(self, response):
        print("---------------------REQUEST---------------------")
        print(f"[JiraAPI] URL: {response.url}")
        print(f"[JiraAPI] Status: {response.status_code}")
        print(f"[JiraAPI] Response: {response.text}")
        print("--------------------------------------------------")
