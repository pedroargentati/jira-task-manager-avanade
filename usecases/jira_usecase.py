from adapters.jira_api import JiraApi

class JiraUseCase:
    def __init__(self, base_url, email, token):
        self.api = JiraApi(base_url)
        self.email = email
        self.token = token

    def get_issue_details(self, issue_key: str):
        return self.api.get_issue_details(self.email, self.token, issue_key)

    def create_subtasks(self, project_id, parent_key, tasks):
        return self.api.create_bulk_subtasks(
            email=self.email,
            token=self.token,
            project_id=project_id,
            parent_key=parent_key,
            tasks=tasks
        )
