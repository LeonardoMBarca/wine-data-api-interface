import os
import logging
import pandas as pd
import re
from pipelines.etl.silver_to_gold.scripts.utils  import split_column_value  # This function returns a list: [original_value, [tokens]]

def dimensional_modeling_csv(path):
    """
    Reads the CSV file from the silver layer, processes it by extracting tokens from the "pais" column,
    maps these tokens into six dimensional attributes:
      - nao_consta
    Returns the transformed DataFrame.
    """
    try:
        logging.info("Reading CSV file from path: %s", path)

        df = pd.read_csv(path, sep=',')
        
        logging.info("CSV file read successfully with %d rows", len(df))

    except Exception as e:
        logging.error("Error reading CSV file: %s", e)
        raise RuntimeError("Failed to read CSV file") from e

    try:
        logging.info("Extracting tokens from 'pais' column using split_column_value")

        columns_value_list = split_column_value(df, column_name="pais")

        logging.info("Token extraction completed for %d unique pais values", len(columns_value_list))

    except Exception as e:
        logging.error("Error during token extraction: %s", e)
        raise RuntimeError("Failed to extract tokens from 'pais' column") from e

    attr_mapping = {}
    try:
        logging.info("Building attribute mapping based on tokens")
        logging.info("Attribute mapping built for %d pais values", len(attr_mapping))

    except Exception as e:
        logging.error("Error building attribute mapping: %s", e)
        raise RuntimeError("Failed to build attribute mapping") from e

    try:
        logging.info("Mapping attributes to DataFrame columns")
        
        df["pais"] = df["pais"].fillna("outros")

        logging.info("Attribute mapping applied successfully to DataFrame")

    except Exception as e:
        logging.error("Error mapping attributes to DataFrame columns: %s", e)
        raise RuntimeError("Failed to map attributes to DataFrame") from e

    return df

def main():
    """
    Main execution function.
    Reads the production CSV file from the silver layer, applies dimensional modeling to create
    enriched attributes, and saves the transformed data into the gold layer.
    """
    logging.info("Starting process_com.py")
    csv_path = [os.path.join("data", "silver-layer", f"Exp{i}.csv") for i in ["Uva", "Suco", "Vinho", "Espumantes"]]
    gold_path = "data/gold-layer"
    output_file = [os.path.join(gold_path, f"Exp{i}.csv") for i in ["Uva", "Suco", "Vinho", "Espumantes"]]

    try:        
        for i, e in enumerate(csv_path):
            df = dimensional_modeling_csv(e)
            
            os.makedirs(gold_path, exist_ok=True)
            df.to_csv(output_file[i], index=False)
            logging.info("Process completed successfully. Output saved to: %s", output_file[i])
            print(f"New processed data is in: {output_file[i]}")

    except Exception as e:
        logging.error("Critical error in main: %s", e)
        print(f"ETL process failed: {e}")

if __name__ == '__main__':
    main()
