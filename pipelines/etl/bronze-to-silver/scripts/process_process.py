from scripts.utils import standardize_dataframe, accent_remove
import os
import pandas as pd
import logging

def process_csv(path, sep):
    """
    
    """
    if not os.path.exists(path):
        logging.error(f"CSV file not found at path: {path}")
        raise FileNotFoundError(f"CSV file not found at path: {path}")
    
    try:
        df = pd.read_csv(path, sep=f"{sep}")
        logging.info(f"CSV file successfully read from: {path}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise ValueError(f"Error reading CSV file: {e}")
    
    standardize_dict = {
    '\*':'',
    'nd':'',
    'br_':'brancaserosadas_',
    '\(':'_',
    '\"':'',
    '\)': '',
    'à':'a',
    'é':'e',
    'í':'i',
    'ó':'o',
    'ú':'u',
    'á':'a',
    'ç':'c',
    'ã':'a',
    'õ':'o',
    'ti_':'tintas_',
    ' ':'_',
    }

    df = standardize_dataframe(df, standardize_dict)
    df.drop(columns=["id", "cultivar"], errors='ignore', inplace=True)

    logging.info(f"The dataframe head: {df.head()}")

    if 'control' not in df.columns:
        logging.error("Column 'control' not found in DataFrame after standardization.")
        raise ValueError("Column 'control' not found in DataFrame after standardization.")

    try:
        melted_df = df.melt(id_vars='control', var_name='ano', value_name='kilogram')

        standardize_dict2 = {
            "__": "_",
            "\"": ''
        }

        melted_df = standardize_dataframe(melted_df, standardize_dict2)

        melted_df['ano'] = melted_df['ano'].astype('int32')

        logging.info(f"Final DF head: {melted_df.head()}")
    
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
    csv_path =  [fr"{os.path.join("data", "bronze-layer", f"Processa{i}.csv")}" for i in ["Americanas", "Mesa", "Semclass", "Viniferas"]]
    silver_path = "data/silver-layer"

    output_file = [fr"{os.path.join(silver_path, f"Processa{i}.csv")}" for i in ["Americanas", "Mesa", "Semclass", "Viniferas"]]

    try:
        for i, e in enumerate(csv_path):
            if output_file[i] == fr"{os.path.join(silver_path, f"ProcessaViniferas.csv")}":
                df_processed = process_csv(e, sep=';')
            else:
                df_processed = process_csv(e, sep='\t')

            if os.path.exists(output_file[i]):
                os.remove(output_file[i]) 
                logging.info(f"Existing output file removed: {output_file[i]}")
                print(f"{output_file[i]} was removed.")

            df_processed.to_csv(output_file[i], index=False)
            logging.info(f"Processed data saved to: {output_file[i]}")
            print(f"New processed data is in: {output_file[i]}")

    except Exception as e:
        logging.error(f"ETL process failed: {e}")
        print(f"ETL process failed: {e}")

if __name__ == '__main__':
    main()