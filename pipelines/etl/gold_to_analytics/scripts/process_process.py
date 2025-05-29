import os
import logging
import pandas as pd

def main():
    try:
        logging.info("Starting  process_process.py")
        base_path = "data/gold-layer"
        output_path = os.path.join("data/analytics", "processamento.csv")

        files = {
            "ProcessaAmericanas.csv": "Uvas Americanas e Híbridas",
            "ProcessaMesa.csv": "Uvas de Mesa",
            "ProcessaSemclass.csv": "Uvas sem Classificação",
            "ProcessaViniferas.csv": "Uvas Viníferas"
        }

        dfs = []

        logging.info("Starting process")

        for file, cat in files.items():
            source = os.path.join(base_path, file)
            df = pd.read_csv(source)
            df['categoria'] = cat
            dfs.append(df)
        
        unified_df = pd.concat(dfs, ignore_index=True)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        unified_df.to_csv(output_path, index=False)

        logging.info("Process completed successfully. Output saved to: %s", output_path)
        print(f"New processed data is in: {output_path}")

    except Exception as e:
        logging.error("Critical error in main: %s", e)
        print(f"process failed: {e}")

if __name__ == '__main__':
    main()