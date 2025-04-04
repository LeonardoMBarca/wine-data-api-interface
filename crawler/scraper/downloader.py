import os
import requests
import logging
import shutil
from config import CSV_LINKS, DOWNLOAD_DIR, LOG_FILE

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


# Efetua o download da base.
def download_base():
    clear_data()
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    for name, url in CSV_LINKS.items():
        filepath = os.path.join(DOWNLOAD_DIR, f"{name}.csv")

        if os.path.exists(filepath):
            msg = f"{name}.csv already exists"
            print(msg)
            logging.info(msg)
            continue

        try:
            print(f"Downloading {name}.csv  {url}...")
            response = requests.get(url)
            response.raise_for_status()  

            with open(filepath, "wb") as f:
                f.write(response.content)

            msg = f"{name}.csv download finished."
            logging.info(msg)

        except Exception as e:
            msg = f"Download error {name}.csv de {url} — {e}"
            print(msg)
            logging.error(msg)

    print("\nProcess finished check the logs in:", LOG_FILE)
