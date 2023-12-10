
from enum import Enum

from scraping import scrape_el_lector, scrape_lpt, scrape_mundo_libros_py


class LibraryEnum(str, Enum):
    lpt = "lpt"
    lector = "lector"
    mundo = "mundo"

scraping_functions = {
    "lpt": scrape_lpt,
    "lector": scrape_el_lector,
    "mundo": scrape_mundo_libros_py,
}