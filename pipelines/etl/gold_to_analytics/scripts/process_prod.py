import os
import logging
import shutil

def main():
    try:
        logging.info("Starting  process_prod.py")
        csv_path = os.path.join("data", "gold-layer", "producao.csv")
        analytics_path = "data/analytics"
        output_file = os.path.join(analytics_path, "producao.csv")

        logging.info("Starting the process")

        os.makedirs(analytics_path, exist_ok=True)

        shutil.copy(csv_path, output_file)
        logging.info("Process completed successfully. Output saved to: %s", output_file)
        print(f"New processed data is in: {output_file}")

    except Exception as e:
        logging.error("Critical error in main: %s", e)
        print(f"process failed: {e}")

if __name__ == '__main__':
    main()