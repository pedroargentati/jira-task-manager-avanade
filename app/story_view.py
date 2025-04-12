import streamlit as st
import pandas as pd

from usecases.jira_usecase import JiraUseCase
from services.card_service import filter_cards_from_csv, normalize_task_columns
from adapters.db_provider import get_db_instance
from app import session
from infra.config_loader import get_db_config

st.set_page_config(layout="wide")

# CSS personalizado para botões
st.markdown("""
    <style>
        div.stButton > button {
            height: 3em;
            font-size: 1.1em;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

def show():
    st.title("Detalhes da Estória")
    st.markdown("---")

    story = session.get("story", "")
    issue_data = session.get("issue_data", {})
    subtasks = issue_data.get("fields", {}).get("subtasks", [])

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        if st.button("🔙 Voltar"):
            session.page_to("main")

        st.markdown("### 📌 Estória Selecionada")
        st.text_input("Estória", story, disabled=True)

        st.markdown("### 📋 Subtasks já existentes no Jira")
        if subtasks:
            editable_data = []
            for sub in subtasks:
                fields = sub.get("fields", {})
                description = fields.get("description", {})
                content = description.get("content", [])
                desc_text = ""
                if content and isinstance(content, list):
                    desc_text = content[0].get("content", [{}])[0].get("text", "")

                editable_data.append({
                    "Chave": sub.get("key"),
                    "Resumo": fields.get("summary", "-"),
                    "Descrição": desc_text
                })

            original_df = pd.DataFrame(editable_data)

            edited_df = st.data_editor(
                original_df.copy(),
                num_rows="dynamic",
                use_container_width=True,
                key="subtask_editor"
            )

            if st.button("💾 Salvar alterações nas subtasks", use_container_width=True):
                changes = edited_df.ne(original_df)
                changed_rows = changes.any(axis=1)
                changed_df = edited_df[changed_rows]

                if changed_df.empty:
                    st.info("Nenhuma alteração detectada.")
                else:
                    from adapters.jira_api import JiraApi
                    jira = JiraApi(base_url=session.get("base_url"))
                    email = session.get("email")
                    token = session.get("token")

                    updated_count = 0
                    for _, row in changed_df.iterrows():
                        success = jira.update_subtask(
                            email=email,
                            token=token,
                            issue_key=row["Chave"],
                            summary=row["Resumo"],
                            description=row["Descrição"]
                        )
                        if success:
                            updated_count += 1

                    st.success(f"✅ {updated_count} subtasks atualizadas com sucesso.")
                    updated_issue = jira.get_issue_details(email=email, token=token, issue_key=story)
                    if updated_issue:
                        session.set("issue_data", updated_issue)
                        st.rerun()

    with col_right:
        st.markdown("### ⚙️ Configuração de Cards")

        app_type = st.selectbox(
            "Tipo de Aplicação",
            ["Mobile", "BD", "TF", "TFWEB", "Mainframe", "BFF", "SRV", "API", "MobilePF", "CCB"],
            key="app_type_select"
        )
        tp_comp_filter = app_type.strip()

        source = st.radio("Fonte dos cards", ["Importar de CSV", "Buscar no Banco de Dados"], key="source_radio")
        df_filtered = None

        if source == "Importar de CSV":
            uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"], key="csv_uploader")

            if uploaded_file is not None and not session.exists("csv_df_original"):
                try:
                    df_original = pd.read_csv(uploaded_file)
                    session.set("csv_df_original", df_original)
                    st.toast("✅ Arquivo CSV carregado com sucesso.")
                except Exception as e:
                    st.error(f"Erro ao ler o arquivo: {e}")

            if session.exists("csv_df_original"):
                df_filtered = filter_cards_from_csv(session.get("csv_df_original").copy(), tp_comp_filter)

        elif source == "Buscar no Banco de Dados":
            props = session.get("database", {}).get("props", {})
            if not props:
                props = get_db_config(session.get("props", {}))
            db = get_db_instance(props)
            try:
                df_filtered = db.buscar_tasks(tp_comp_filter)
                df_filtered = normalize_task_columns(df_filtered)
                st.toast("✅ Tasks carregadas do banco com sucesso.")
            except Exception as e:
                st.error(f"Erro ao buscar tasks do banco: {e}")

        st.markdown("### 📥 Cards importados")

        if df_filtered is not None and not df_filtered.empty:
            columns_to_display = ["Etapa", "Task", "Descrição", "Responsável", "Esforço"]
            available_columns = [col for col in columns_to_display if col in df_filtered.columns]

            if available_columns:
                df_filtered["Selecionar"] = False
                st.data_editor(
                    df_filtered[["Selecionar"] + available_columns],
                    use_container_width=True,
                    num_rows="dynamic",
                    key="task_selector"
                )
            else:
                st.warning("Nenhuma coluna esperada foi encontrada.")

        if st.button("🚀 Criar Tasks", use_container_width=True):
            if df_filtered is None or df_filtered.empty:
                st.warning("Nenhuma task carregada para criação.")
                return

            task_data = session.get("task_selector", {})
            edited_rows = task_data.get("edited_rows", {})
            selected_indices = [i for i, v in edited_rows.items() if v.get("Selecionar")]
            selected_df = df_filtered.iloc[selected_indices]

            if selected_df.empty:
                st.warning("Nenhuma task foi selecionada para criação.")
                return

            task_list = [
                {
                    "summary": str(row.get("Task", "")).strip(),
                    "description": str(row.get("Descrição", "")).strip()
                }
                for _, row in selected_df.iterrows() if row.get("Task")
            ]

            jira = JiraUseCase(
                base_url=session.get("base_url"),
                email=session.get("email"),
                token=session.get("token")
            )

            success, result = jira.create_subtasks(
                project_id=issue_data.get("fields", {}).get("project", {}).get("id"),
                parent_key=story,
                tasks=task_list
            )

            if success:
                st.success(f"✅ {len(result.get('issues', []))} subtasks criadas com sucesso.")
                updated_issue = jira.get_issue_details(story)
                if updated_issue:
                    session.set("issue_data", updated_issue)
                    st.rerun()
                else:
                    st.warning("As subtasks foram criadas, mas não foi possível atualizar a lista.")
            else:
                st.error(f"❌ Erro ao criar subtasks: {result}")