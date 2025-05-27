import os
import requests
import logging
import shutil
from crawler.config import CSV_LINKS, DOWNLOAD_DIR, LOG_FILE

# Verifica se o diretório de logs existe, caso contrário, cria-o
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configuração de logs
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Evita duplicidades nos arquivos
def clear_data():
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR)


def download_base():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Primeiro: verifica se todos os links estão acessíveis
    for name, url in CSV_LINKS.items():
        try:
            response = requests.head(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            msg = f"[ERRO] Não foi possível acessar o link de {name}.csv ({url}): {e}"
            print(msg)
            logging.error(msg)
            return False  # Impede o ETL e a exclusão de arquivos

    # Se todos os links estiverem OK, então limpa a pasta e faz o download
    clear_data()

    for name, url in CSV_LINKS.items():
        filepath = os.path.join(DOWNLOAD_DIR, f"{name}.csv")

        try:
            print(f"Baixando {name}.csv de {url}...")
            response = requests.get(url)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            logging.info(f"{name}.csv baixado com sucesso.")

        except Exception as e:
            msg = f"[ERRO] Falha ao baixar {name}.csv: {e}"
            print(msg)
            logging.error(msg)
            return False  # Parar se algum download falhar após clear_data()

    print("Download finalizado. Veja os logs em:", LOG_FILE)
    return True
