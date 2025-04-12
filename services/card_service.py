import pandas as pd

def filter_cards_from_csv(df, app_type):
    if "Tp_Comp" not in df.columns:
        return pd.DataFrame()

    df["Tp_Comp"] = df["Tp_Comp"].fillna("").astype(str)
    return df[df["Tp_Comp"].str.contains(app_type, case=False, na=False)]


def normalize_task_columns(df):
    return df.rename(columns={
        "etapa": "Etapa",
        "task": "Task",
        "descricao": "Descrição",
        "responsavel": "Responsável",
        "esforco": "Esforço",
        "tp_comp": "Tp_Comp"
    })
