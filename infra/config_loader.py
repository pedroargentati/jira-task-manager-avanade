import os

def load_properties():
    props_path = os.path.join(os.getcwd(), "application.properties")
    props = {}

    if os.path.exists(props_path):
        with open(props_path, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    props[key.strip()] = value.strip()
    return props

def get_jira_config(props: dict) -> dict:
    return {
        "base_url": props.get("jira.base.url", "https://avanade.free.beeceptor.com/"),
        "email": props.get("jira.email"),
        "token": props.get("jira.token"),
        "project_key": props.get("jira.project.key")
    }

def get_db_config(props: dict) -> dict:
    return {
        "MYSQL_URL": props.get("MYSQL_URL"),
        "MYSQL_USERNAME": props.get("MYSQL_USERNAME"),
        "MYSQL_PASSWORD": props.get("MYSQL_PASSWORD"),
        "MYSQL_DATABASE_NAME": props.get("MYSQL_DATABASE_NAME"),
        "MYSQL_HOST": props.get("MYSQL_HOST", "localhost"),
        "MYSQL_PORT": int(props.get("MYSQL_PORT", 3306)),
        "provider": props.get("database.provider", "mysql").lower()
    }
