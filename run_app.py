# run_app.py
import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "streamlit_app.py"]  # ajuste o nome do seu app aqui
    sys.exit(stcli.main())
