import os
import logging

# Setup logging
LOG_FILE = os.path.abspath(os.path.join("pipelines", "etl", "silver-to-gold", "logs", "etl_gold.log"))
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='w',
    force=True
) 

from scripts.process_prod import main as process_prod
from scripts.process_com import main as process_com
# from scripts.process_exp import main as process_exp
# from scripts.process_imp import main as process_imp
# from scripts.process_process import main as process_process

def main():
    process_prod()
    process_com()
    # process_exp()
    # process_imp()
    # process_process()

if __name__ == "__main__":
    main()