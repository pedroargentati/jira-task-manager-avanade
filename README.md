# 🛠️ Jira Task Manager (v0.1.0)

Uma aplicação de interface gráfica feita com **Python + Streamlit**, empacotada com **Electron**, que permite integrar com o **Jira Cloud** para gerenciar subtasks de forma produtiva e personalizada.

---

## 🚀 Funcionalidades

### ✅ Integração com Jira
- Conexão via **Token + E-mail**
- Consulta e validação de uma **Estória (Issue)**
- Listagem de **subtasks já existentes**
- Criação de **subtasks em lote**
- Edição de **subtasks já criadas** (título e descrição)

### 📥 Fontes de tarefas suportadas
- **Importação de planilha CSV**
- **Consulta ao banco de dados (MySQL)** com filtro por tipo de aplicação

### 🗂️ Filtragem por Tipo de Aplicação
- A aplicação permite filtrar as tasks por **Tipo de Aplicação** como `TF`, `SRV`, `BFF`, `Mobile`, `API`, etc.

---

## 🧱 Arquitetura

Utilizamos a **Arquitetura Hexagonal (Ports & Adapters)** com separação clara de responsabilidades:

```
📁 app/            → Views (UI) do Streamlit
📁 adapters/       → Conectores com APIs externas (Jira, MySQL)
📁 usecases/       → Casos de uso da regra de negócio
📁 services/       → Serviços auxiliares (ex: tratamento de CSV)
📁 ports/          → Interfaces (protocolos) para os adapters
📁 infra/          → Configuração e loaders (application.properties)
```

---

## ⚙️ Como rodar localmente

### 1. Clone o repositório e entre na pasta

```bash
git clone https://github.com/seu-user/jira-task-manager.git
cd jira-task-manager
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o projeto

```bash
streamlit run streamlit_app.py
```

Ou, se estiver usando `run_app.py`:

```bash
python run_app.py
```

---

## 🧪 Configuração

Crie o arquivo `application.properties` na raiz do projeto com:

```properties
jira.email=seu_email@empresa.com
jira.token=seu_token_aqui
jira.base.url=https://seu-dominio.atlassian.net/rest/api/3
jira.project.key=AVA

database.provider=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USERNAME=root
MYSQL_PASSWORD=root
MYSQL_DATABASE_NAME=jiradb
MYSQL_URL=mysql+pymysql://root:root@localhost:3306/jiradb
```

---

## 📦 Gerar executável (com Electron)

Esse projeto usa **Electron + Stlite** para empacotar a aplicação como `.exe`.

### 1. Instale as dependências globais:

```bash
npm install
```

### 2. Gere os artefatos com Stlite

```bash
npm run dump
```

### 3. Rode local via Electron

```bash
npm run serve
```

### 4. Gere o executável

```bash
npm run app:dist
```

---

## 📋 TODO / Próximos passos

- [ ] Edição de status / labels da subtask
- [ ] Suporte a outros bancos de dados (SQL Server na Azure)
- [ ] Histórico de execuções
- [ ] Autenticação com OAuth 2.0 no Jira

---
