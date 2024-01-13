
from enum import Enum

from pydantic import BaseModel

from scraping.scrapingListBooks import scrape_el_lector, scrape_lpt, scrape_mundo_libros_py

class LibraryEnum(str, Enum):
    lpt = "lpt"
    lector = "lector"
    mundo = "mundo"

class LibraryInfo(BaseModel):
    name: str
    website_url: str
    icon_url: str
    library_path: str

libraries_info = [
    LibraryInfo(name="Libros para todos", website_url="https://lpt.com.py", icon_url="https://lpt.com.py/images/logo/logo-simple-or.png", library_path="lpt"),
    LibraryInfo(name="El Lector", website_url="https://ellector.com.py", icon_url="https://ellector.com.py/assets/images/logo.png", library_path="lector"),
    LibraryInfo(name="Mundo Libros", website_url="https://www.mundolibrospy.com", icon_url="http://www.mundolibrospy.com/img/cms/Mundo%20Libros.png", library_path="mundo"),
]

scraping_functions = {
    "lpt": scrape_lpt,
    "lector": scrape_el_lector,
    "mundo": scrape_mundo_libros_py,
}