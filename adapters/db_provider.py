from adapters.mysql_adapter import MySQLAdapter

def get_db_instance(props: dict):
    print(f"[DB Provider] Lendo propriedades: {props}")
    provider = props.get("provider", "").lower()
    print(f"[DB Provider] Provider detectado: {provider}")

    if provider == "mysql":
        if props.get("MYSQL_URL"):
            print("[DB Provider] Usando MYSQL_URL para configuração")
            conf = parse_mysql_url(props.get("MYSQL_URL"))
        else:
            print("[DB Provider] Usando parâmetros separados para configuração do MySQL")
            conf = {
                "host": props.get("MYSQL_HOST", "localhost"),
                "port": int(props.get("MYSQL_PORT", 3306)),
                "user": props.get("MYSQL_USERNAME"),
                "password": props.get("MYSQL_PASSWORD"),
                "database": props.get("MYSQL_DATABASE_NAME")
            }

        print(f"[DB Provider] Configuração final: {conf}")
        return MySQLAdapter(**conf)

    raise ValueError(f"[DB Provider] Provider '{provider}' não suportado.")


from urllib.parse import urlparse

def parse_mysql_url(url):
    print(f"[DB Provider] Parsing MYSQL_URL: {url}")
    parsed = urlparse(url)
    conf = {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path.lstrip('/')
    }
    print(f"[DB Provider] Resultado do parse: {conf}")
    return conf

