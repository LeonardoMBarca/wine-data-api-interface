import os
import logging
import pandas as pd
import re
from scripts.utils import split_column_value

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
    
    total_values = ["vinho_de_mesa", "vinho_fino_de_mesa_vinifera", "suco", "derivados"]
    attr_mapping = {}
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

            if tokens and tokens[0] in ["vinho", "suco", "derivados"]:
                attr["categoria"] = tokens[0]

                if original_value in total_values:
                    attr["total"] = 1
                    
                else:
                    attr["total"] = 0
                    # SECTION: VINHO
                    if attr["categoria"] == "vinho":
                        if "mesa" in tokens:
                            attr["subcategoria"] = "mesa"

                        for estilo in ["tinto", "branco", "rosado"]:
                            if estilo in tokens:
                                attr["tipo_estilo"] = estilo
                                break

                        if "fino" in tokens:
                            attr["processamento"] = "fino"

                        for var in ["vinifera", "viniferas"]:
                            if var in tokens:
                                attr["variedade_origem"] = var
                                break

                    # SECTION: SUCO
                    elif attr["categoria"] == "suco":
                        if "uva" in tokens:
                            attr["variedade_origem"] = "uva"

                        if "concentrado" in tokens:
                            attr["tipo_estilo"] = "concentrado"

                        for proc in ["simples", "adocado", "organico", "reconstituido"]:
                            if proc in tokens:
                                attr["processamento"] = proc
                                break

                    # SECTION: DERIVADOS
                    elif attr["categoria"] == "derivados":
                        subcat_list = [
                            "espumante", "base", "bebida", "polpa", "mosto", "mistelas", "nectar",
                            "licorosos", "compostos", "jeropiga", "filtrado", "frisante", "vinho",
                            "brandy", "destilado", "bagaceira", "licor", "vinagre", "borra", "pisco", "outros"
                        ]

                        for token in tokens:
                            if token in subcat_list:
                                attr["subcategoria"] = token
                                break

                        if "champenoise" in tokens:
                            attr["metodo_processo"] = "champenoise"

                        elif "charmat" in tokens:

                            attr["metodo_processo"] = "charmat"

                        for estilo in ["tinto", "branco", "rosado", "leve", "licoroso", "acidificado", "composto", "organico"]:
                            if estilo in tokens:
                                attr["tipo_estilo"] = estilo
                                break

                        if "parcialmente" in tokens and "fermentado" in tokens:
                            attr["processamento"] = "parcialmente fermentado"

                        else:
                            for proc in ["simples", "concentrado", "dessulfitado"]:
                                if proc in tokens:
                                    attr["processamento"] = proc
                                    break

            attr_mapping[original_value] = attr

        logging.info("Attribute mapping built for %d control values", len(attr_mapping))

    except Exception as e:
        logging.error("Error building attribute mapping: %s", e)
        raise RuntimeError("Failed to build attribute mapping") from e

    try:
        logging.info("Mapping attributes to DataFrame columns")

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
        logging.info("Starting process_prod.py")
        csv_path = os.path.join("data", "silver-layer", "producao.csv")
        gold_path = "data/gold-layer"
        output_file = os.path.join(gold_path, "producao.csv")
        
        logging.info("Starting dimensional modeling process")
        df = dimensional_modeling_csv(csv_path)
        
        os.makedirs(gold_path, exist_ok=True)
        df.to_csv(output_file, index=False)
        logging.info("Process completed successfully. Output saved to: %s", output_file)
        print(f"New processed data is in: {output_file}")

    except Exception as e:
        logging.error("Critical error in main: %s", e)
        print(f"ETL process failed: {e}")

if __name__ == "__main__":
    main()
