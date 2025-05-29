import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# Setup logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "etl_analytics.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='w',
    force=True
) 

from pipelines.etl.gold_to_analytics.scripts.process_prod import main as process_prod
from pipelines.etl.gold_to_analytics.scripts.process_com import main as process_com
from pipelines.etl.gold_to_analytics.scripts.process_exp import main as process_exp
from pipelines.etl.gold_to_analytics.scripts.process_imp import main as process_imp
from pipelines.etl.gold_to_analytics.scripts.process_process import main as process_process

def main():
    process_prod()
    process_com()
    process_exp()
    process_imp()
    process_process()

if __name__ == "__main__":
    main()