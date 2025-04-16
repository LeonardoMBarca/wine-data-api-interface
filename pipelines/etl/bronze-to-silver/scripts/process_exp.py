from scripts.utils import standardize_dataframe, accent_remove
import os
import logging
import pandas as pd

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
        'õ':'o',
        '\(':'_', 
        "\)": '', 
        ',':'_'
    }

    df = standardize_dataframe(df, standardize_dict)
    df.drop(columns=["id"], errors='ignore', inplace=True)


    logging.info(f"The dataframe head: {df.head()}")

    if 'país' not in df.columns:
        logging.error("Column 'país' not found in DataFrame after standardization.")
        raise ValueError("Column 'país' not found in DataFrame after standardization.")

    try:
        df_kg_years = df.iloc[:, 1::2]
        df_dollar_years = df.iloc[:, 2::2]
        df_country = df.iloc[:, 0:1]

        df_kg_country = df_country.join(df_kg_years)
        df_dollar_country = df_country.join(df_dollar_years)

        logging.info(f"df_kg_country: {df_kg_country.head()}")
        logging.info(f"df_dollar_country: {df_dollar_country.head()}")

        df_melted = df_kg_country.melt(id_vars='país', var_name='ano', value_name='kilograms')
        df_melted_dollar =df_dollar_country.melt(id_vars='país', var_name='ano', value_name='dollars')

        df_melted_dollar['ano'] = df_melted_dollar['ano'].str[:4].astype('int32')
        df_melted['ano'] = df_melted['ano'].astype('int32')

        df_final = df_melted.merge(df_melted_dollar)

        logging.info(f"Final df after merge: {df_final}")

        df_final = df_final.rename(columns={'país': 'pais'})
        df_final['pais'] = df_final['pais'].apply(accent_remove)

        standardize_dict2 = {
            '__':'_',
            '\"':''
        }
        df_final = standardize_dataframe(df_final, standardize_dict2)

        logging.info(f"Final DF head: {df_final.head()}")
    
    except Exception as e:
        logging.error(f"Error during DataFrame transformation: {e}")
        raise ValueError(f"Error during DataFrame transformation: {e}")

    return df_final
    
def main():
    """
    Main execution function for processing the production CSV file.
    Loads the input file, processes it, and saves the transformed data
    into the silver layer.
    """
    csv_path =  [fr"{os.path.join("data", "bronze-layer", f"Exp{i}.csv")}" for i in ["Uva", "Suco", "Vinho", "Espumantes"]]
    silver_path = "data/silver-layer"

    output_file = [fr"{os.path.join(silver_path, f"Exp{i}.csv")}" for i in ["Uva", "Suco", "Vinho", "Espumantes"]]

    try:
        for i, e in enumerate(csv_path):
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