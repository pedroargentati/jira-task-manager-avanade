import streamlit as st
import pandas as pd

def show():
    st.title("Detalhes da Estória")

    # Dados da estória e subtasks existentes do Jira
    story = st.session_state.get("story", "")
    issue_data = st.session_state.get("issue_data", {})
    subtasks = issue_data.get("fields", {}).get("subtasks", [])

    st.text_input("Estória", story, disabled=True)

    # Tipo de aplicação
    app_type = st.selectbox(
        "Tipo de Aplicação",
        ["Mobile", "BD", "TF", "TFWEB", "Mainframe", "BFF", "SRV", "API", "MobilePF", "CCB"],
        key="app_type_select"
    )
    tp_comp_filter = app_type.strip()

    # Exibir subtasks do Jira
    if subtasks:
        st.subheader("Subtasks já existentes no Jira")
        subtask_data = []
        for subtask in subtasks:
            fields = subtask.get("fields", {})
            status = fields.get("status", {})
            subtask_data.append({
                "Chave": subtask.get("key"),
                "Status": status.get("name", ""),
                "Ícone": status.get("iconUrl", "")
            })

        subtask_df = pd.DataFrame(subtask_data)
        st.dataframe(subtask_df, use_container_width=True)

    # Escolha da fonte dos cards
    source = st.radio(
        "Fonte dos cards",
        ["Importar de CSV", "Buscar no Banco de Dados"],
        key="source_radio"
    )

    df_filtered = None

    if source == "Importar de CSV":
        uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"], key="csv_uploader")

        if uploaded_file is not None and "csv_df_original" not in st.session_state:
            try:
                df_original = pd.read_csv(uploaded_file)
                st.session_state.csv_df_original = df_original
                st.success("Arquivo carregado com sucesso.")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

        # Refiltrar ao trocar tipo de aplicação
        if "csv_df_original" in st.session_state:
            df = st.session_state.csv_df_original.copy()
            if "Tp_Comp" in df.columns:
                df["Tp_Comp"] = df["Tp_Comp"].fillna("").astype(str)
                df_filtered = df[df["Tp_Comp"].str.contains(tp_comp_filter, case=False, na=False)]

    elif source == "Buscar no Banco de Dados":
        st.info("Integração com banco ainda será implementada.")
        # Aqui você poderá conectar e aplicar o mesmo filtro

    # Exibir a tabela filtrada
    if df_filtered is not None and not df_filtered.empty:
        st.subheader("Cards importados")
        columns_to_display = ["Etapa", "Task", "Descrição", "Responsável", "Esforço"]
        available_columns = [col for col in columns_to_display if col in df_filtered.columns]

        if available_columns:
            st.dataframe(df_filtered[available_columns], use_container_width=True)
        else:
            st.warning("Nenhuma coluna esperada foi encontrada no CSV.")

    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar"):
            st.session_state.page = 'main'
            st.rerun()
    with col2:
        st.button("Criar Tasks (em breve)")
