from dre_scraper import scrap
from dre_scraper.exporter import export_to_csv

if __name__ == "__main__":
    dre = scrap()
    export_to_csv(dre)
