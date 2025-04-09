from scripts.process_prod import main as process_prod
from scripts.process_com import main as process_com
from scripts.process_exp import main as process_exp
from scripts.process_imp import main as process_imp
from scripts.process_process import main as process_process

def main():
    process_prod()
    process_com()
    process_exp()
    process_imp()
    process_process()

if __name__ == "__main__":
    main()