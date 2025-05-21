from crawler.scraper.downloader import download_base
from pipelines.etl.bronze_to_silver.main import main as run_bronze_to_silver


from pipelines.etl.silver_to_gold.main import main as run_silver_to_gold   

if __name__ == "__main__":
    download_base()
    run_bronze_to_silver() 
    run_silver_to_gold()
