import streamlit as st
from adapters.jira_api import JiraApi
import os

def read_properties():
    props_path = os.path.join(os.getcwd(), "application.properties")
    props = {}

    if os.path.exists(props_path):
        with open(props_path, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    props[key.strip()] = value.strip()
    return props

def show():
    st.title("Validação do Jira")

    props = read_properties()

    base_url = props.get("jira.base.url", "https://avanade.free.beeceptor.com/")
    email = props.get("jira.email")
    token = props.get("jira.token")
    project_key = props.get("jira.project.key")
    mysql_url = props.get("MYSQL_URL")
    mysql_username = props.get("MYSQL_USERNAME")
    mysql_password = props.get("MYSQL_PASSWORD")
    mysql_database_name = props.get("MYSQL_DATABASE_NAME")
    mysql_host = props.get("MYSQL_HOST", "localhost")
    mysql_port = int(props.get("MYSQL_PORT", 3306))
    provider = props.get("database.provider", "mysql").lower()

    if email and token:
        st.success("Credenciais carregadas automaticamente.")
    else:
        email = st.text_input("E-mail do Jira")
        token = st.text_input("Token do Jira", type="password")

    story_input = ""
    if project_key:
        story_input = st.text_input(f"Número da Estória ({project_key}-###):")
        story = f"{project_key}-{story_input}" if story_input else ""
    else:
        story = st.text_input("Chave da Estória (ex: TESTE-123)")

    if st.button("Avançar"):
        if not email or not token or not story:
            st.error("Preencha todos os campos obrigatórios.")
            return

        jira = JiraApi(base_url=base_url)
        issue_data = jira.get_issue_details(email=email, token=token, issue_key=story)
        if not issue_data:
            st.error(f"Estória '{story}' não encontrada. Verifique os dados.")
        else:
            st.session_state.email = email
            st.session_state.token = token
            st.session_state.story = story
            st.session_state.base_url = base_url
            st.session_state.issue_data = issue_data
            st.session_state.page = 'story'
            st.session_state["database"] = {
                "props": {
                    "MYSQL_URL": mysql_url,
                    "MYSQL_USERNAME": mysql_username,
                    "MYSQL_PASSWORD": mysql_password,
                    "MYSQL_DATABASE_NAME": mysql_database_name,
                    "MYSQL_HOST": mysql_host,
                    "MYSQL_PORT": mysql_port,
                    "provider": provider
                }
            }
            st.rerun()

