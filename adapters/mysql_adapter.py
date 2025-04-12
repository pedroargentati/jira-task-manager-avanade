import pymysql
import pandas as pd
from ports.db_port import DatabasePort

class MySQLAdapter(DatabasePort):
    def __init__(self, host, port, user, password, database):
        try:
            self.conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(f"[MySQLAdapter] Erro ao conectar: {e}")
            raise


    def buscar_tasks(self, tp_comp: str):
        print(f"[MySQLAdapter] Buscando tasks com tp_comp: {tp_comp}")
        if not tp_comp:
            print("[MySQLAdapter] tp_comp vazio, retornando DataFrame vazio.")
            return pd.DataFrame()
        with self.conn.cursor() as cursor:
            sql = """
                SELECT etapa, task, descricao, responsavel, esforco, tp_comp
                FROM tasks
                WHERE tp_comp LIKE %s
            """
            print(f"[MySQLAdapter] Executando SQL:\n{sql.strip()}\n[param: {tp_comp}]")

            cursor.execute(sql, (f"Tp_Comp:%{tp_comp}%",))
            result = cursor.fetchall()
            print(f"[MySQLAdapter] Resultados encontrados: {len(result)}")
            return pd.DataFrame(result)
