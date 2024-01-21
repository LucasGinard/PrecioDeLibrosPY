from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.params import Query
from fastapi.staticfiles import StaticFiles

from model.LibraryEnum import LibraryEnum, LibraryInfo,scraping_functions,libraries_info,scraping_detail_functions, validate_library_detail

from scraping.scrapingListBooks import scrape_book

from model.BookData import BookData

from typing import List

titleDoc = "PrecioDeLibrosPY API"
urlIcon = "/static/books.256x256.png"

app = FastAPI(
	title= "📚" + titleDoc,
    description= "",
    version= "0.0.1",
	docs_url= None,
	redoc_url= None,
	redoc_favicon_url=urlIcon
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title= titleDoc, swagger_favicon_url=urlIcon,swagger_css_url="/static/swagger-dark-mode.css")

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url="/openapi.json", title= titleDoc, redoc_favicon_url=urlIcon)

def validate_search_query(book: str = Query(..., alias="book")):
    if not book or not book.strip():
        raise HTTPException(status_code=400, detail="empty value search")
    return book.strip()

@app.get("/search", response_model=List[BookData], tags=["Requests Public 🌎"])
async def search_book(book: str = Depends(validate_search_query)):
    scraped_books = scrape_book(book)
    return scraped_books

valid_libraries = list(library.value for library in LibraryEnum)

async def validate_library(library: str = Path(..., title="Library", 
                                               description=f"Librerías disponibles para buscar: [ {', '.join(valid_libraries)} ] puedes utilizar /libraries para obtener el listado")):
    if library not in valid_libraries:
        raise HTTPException(status_code=400, detail=f"No ingresaste una librería válida. Las opciones disponibles son: [ {', '.join(valid_libraries)}]")
    return library

@app.get("/search/{library}", response_model=List[BookData], tags=["Requests Public 🌎"])
async def search_books_in_specif_library(
     library: LibraryEnum = Depends(validate_library),
     search_query: str = Depends(validate_search_query)
     ):
    scraped_books = scraping_functions[library](search_query)
    return scraped_books

@app.get("/libraries", response_model=List[LibraryInfo], tags=["Requests Public 🌎"])
async def get_libraries_availables():
    """
   Obtén la lista de **librerías disponibles** 📚.\n
   usa el response **library_path** para facilitar el listado de librerías disponibles de /search/{library}.\n
    """
    return libraries_info

def validate_search_link(detail_link: str = Query(..., alias="Link Book")):
    if not detail_link or not detail_link.strip():
        raise HTTPException(status_code=400, detail="Empty value search")

    return detail_link


@app.get("/detail/{library}", response_model=List[BookData], tags=["Requests Public 🌎"])
async def detail_book_in_specif_library(
     search_query: str = Depends(validate_search_link)
     ):
    library = validate_library_detail(search_query)
    if library == None:
         raise HTTPException(status_code=400, detail="Invalid url")
    
    return scraping_detail_functions[library](search_query)