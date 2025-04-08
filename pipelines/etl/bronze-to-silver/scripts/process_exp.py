from scripts.utils import standardize_dataframe, accent_remove
import os
import logging
import pandas as pd

LOG_FILE = os.path.abspath(os.path.join("..", "..", "logs", "etl_exp_silver.log"))
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_csv(path):
    """

    """
    if not os.path.exists(path):
        logging.error(f"CSV file not found at path: {path}")
        raise FileNotFoundError(f"CSV file not found at path: {path}")
    
    try:
        df = pd.read_csv(path, sep=";")
        logging.info(f"CSV file successfully read from: {path}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise ValueError(f"Error reading CSV file: {e}")
    
    standardize_dict = {
        "__": "_",
        '\"': "",
        "-": "_",
        " ": "_",
        'à':'a',
        'á':'a',
        'ç':'c',
        'é':'e',
        'í':'i',
        'ó':'o',
        'ú':'u',
        'ã':'a',
        'õ':'o'
    }

    df = standardize_dataframe(df, standardize_dict)

    # df_
        