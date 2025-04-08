from scripts.process_prod import main as process_prod
from scripts.process_com import main as process_com

def main():
    process_prod()
    process_com()

if __name__ == "__main__":
    main()