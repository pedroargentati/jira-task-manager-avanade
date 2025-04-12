import streamlit as st
from adapters.jira_api import JiraApi
from app import session
from infra.config_loader import load_properties, get_jira_config, get_db_config

def show():
    st.title("Validação do Jira")

    props = load_properties()
    jira_config = get_jira_config(props)
    db_config = get_db_config(props)

    base_url = jira_config["base_url"]
    email = jira_config.get("email")
    token = jira_config.get("token")
    project_key = jira_config.get("project_key")

    if email and token:
        st.success("Credenciais carregadas automaticamente.")
    else:
        email = st.text_input("E-mail do Jira")
        token = st.text_input("Token do Jira", type="password")

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
            session.set_many({
                "email": email,
                "token": token,
                "story": story,
                "base_url": base_url,
                "project_key": project_key,
                "issue_data": issue_data,
                "database": {"props": db_config}
            })
            session.page_to("story")
