import requests
from requests.auth import HTTPBasicAuth

class JiraApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_issue_details(self, email, token, issue_key):
        url = f"{self.base_url}/{issue_key}"
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
