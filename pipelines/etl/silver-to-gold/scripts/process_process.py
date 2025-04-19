import os
import logging
import pandas as pd
import re
from scripts.utils import split_column_value  # This function returns a list: [original_value, [tokens]]

def dimensional_modeling_csv(path):
    """
    Reads the CSV file from the silver layer, processes it by extracting tokens from the "control" column,
    maps these tokens into six dimensional attributes:
      - categoria
      - subcategoria
      - tipo_estilo
      - processamento
      - variedade_origem
      - metodo_processo
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
        logging.info("Extracting tokens from 'control' column using split_column_value")

        columns_value_list = split_column_value(df, column_name="control")

        logging.info("Token extraction completed for %d unique control values", len(columns_value_list))

    except Exception as e:
        logging.error("Error during token extraction: %s", e)
        raise RuntimeError("Failed to extract tokens from 'control' column") from e

    attr_mapping = {}
    total_values = ["brancas_rosadas", "tintas", "brancas", "sem_classificacao"]
    try:
        logging.info("Building attribute mapping based on tokens")

        for entry in columns_value_list:
            original_value, tokens = entry
            attr = {
                "categoria": None,
                "subcategoria": None,
                "tipo_estilo": None,
                "processamento": None,
                "variedade_origem": None,
                "metodo_processo": None,
                "total": None
            }

            if tokens and tokens[0] in ["tintas", "brancas", "rosadas", "outros"]:
                attr["categoria"] = "brancas_rosadas" if "brancas" in original_value and "rosadas" in original_value else tokens[0]

                attr["total"] = 1 if original_value in total_values else 0



            else:
                attr["total"] = 1

            attr_mapping[original_value] = attr

        logging.info("Attribute mapping built for %d control values", len(attr_mapping))

    except Exception as e:
        logging.error("Error building attribute mapping: %s", e)
        raise RuntimeError("Failed to build attribute mapping") from e

    try:
        logging.info("Mapping attributes to DataFrame columns")
        
        df["control"] = df["control"].fillna("outros_produtos_comercializados")
        df["categoria"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("categoria"))
        df["subcategoria"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("subcategoria"))
        df["tipo_estilo"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("tipo_estilo"))
        df["processamento"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("processamento"))
        df["variedade_origem"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("variedade_origem"))
        df["metodo_processo"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("metodo_processo"))
        df["total"] = df["control"].map(lambda x: attr_mapping.get(x, {}).get("total"))

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
    try:
        logging.info("Starting process_com.py")
        csv_path = os.path.join("data", "silver-layer", "comercio.csv")
        gold_path = "data/gold-layer"
        output_file = os.path.join(gold_path, "comercio.csv")
        
        logging.info("Starting dimensional modeling process")
        df = dimensional_modeling_csv(csv_path)
        
        os.makedirs(gold_path, exist_ok=True)
        df.to_csv(output_file, index=False)
        logging.info("Process completed successfully. Output saved to: %s", output_file)
        print(f"New processed data is in: {output_file}")

    except Exception as e:
        logging.error("Critical error in main: %s", e)
        print(f"ETL process failed: {e}")

if __name__ == '__main__':
    processed_df = main()
    print(processed_df.head())
