
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from scraping.scrapingListBooks import scrape_el_lector, scrape_lpt, scrape_mundo_libros_py
from scraping.scrapingDetailBook import scrape_detail_book_lpt, scrape_detail_book_el_lector, scrape_detail_book_mundo_libros_py

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
    LibraryInfo(name="El Lector", website_url="https://ellector.com.py", icon_url="https://ellector.com.py/assets/img/logo_ellector_v2.svg", library_path="lector"),
    LibraryInfo(name="Mundo Libros", website_url="https://www.mundolibrospy.com", icon_url="http://www.mundolibrospy.com/img/cms/Mundo%20Libros.png", library_path="mundo"),
]

scraping_functions = {
    "lpt": scrape_lpt,
    "lector": scrape_el_lector,
    "mundo": scrape_mundo_libros_py,
}

scraping_detail_functions = {
    libraries_info[0].website_url : scrape_detail_book_lpt,
    libraries_info[1].website_url: scrape_detail_book_el_lector,
    libraries_info[2].website_url: scrape_detail_book_mundo_libros_py,
}

def validate_library_detail(detailLink: str) -> Optional[str]:
    for library in libraries_info:
        if library.website_url in detailLink:
            return library.website_url
    return None