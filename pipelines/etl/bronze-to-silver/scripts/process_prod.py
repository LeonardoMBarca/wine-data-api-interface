import os
import logging
import pandas as pd
from scripts.utils import standardize_dataframe, accent_remove

def process_csv(path):
    """
    Loads and processes a CSV file by standardizing column names and values,
    removing unnecessary columns, melting the DataFrame to long format,
    and removing accents from the 'control' column.

    Parameters:
        path (str): The file path of the CSV file to be processed.

    Returns:
        pd.DataFrame: A processed and transformed DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the 'control' column is not found after standardization.
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
        "es_": "",
        "vm_": "vinho_mesa_",
        "su_": "",
        "ve_": "vinho_especial_",
        "ou_": "outros_",
        "_de_": "_",
        "vv_": "vinho_viniferas_",
        "__": "_",
        "de_": "derivados_",
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
    df.drop(columns=["id", "produto"], errors="ignore", inplace=True)

    if 'control' not in df.columns:
        logging.error("Column 'control' not found in DataFrame after standardization.")
        raise ValueError("Column 'control' not found in DF after the standardization")

    try:
        melted_df = df.melt(id_vars='control', var_name='ano', value_name='Litros')
        melted_df['control'] = melted_df['control'].apply(accent_remove)
        logging.info("DataFrame transformation successful.")
        
    except Exception as e:
        logging.error(f"Error during DataFrame transformation: {e}")
        raise ValueError(f"Error during DataFrame transformation: {e}")

    return melted_df

def main():
    """
    Main execution function for processing the production CSV file.
    Loads the input file, processes it, and saves the transformed data
    into the silver layer.
    """
    csv_path =  fr"{os.path.join("data", "bronze-layer", "Producao.csv")}"
    silver_path = "data/silver-layer"
    output_file = os.path.join(silver_path, f"producao.csv")
    
    try:
        df_processed = process_csv(csv_path)

        if os.path.exists(output_file):
            os.remove(output_file)
            logging.info(f"Existing output file removed: {output_file}")
            print(f"{output_file} was removed.")

        df_processed.to_csv(output_file, index=False)
        logging.info(f"Processed data saved to: {output_file}")
        print(f"New processed data is in: {output_file}")

    except Exception as e:
        logging.error(f"ETL process failed: {e}")
        print(f"ETL process failed: {e}")

if __name__ == "__main__":
    main()