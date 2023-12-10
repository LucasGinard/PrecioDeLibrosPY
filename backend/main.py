from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.params import Query
from model.LibraryEnum import LibraryEnum,scraping_functions

from scraping import scrape_book

from model.BookData import BookData

from typing import List

titleDoc = "PrecioDeLibrosPY API"
urlIcon = "📚"

app = FastAPI(
	title= "📚" + titleDoc,
    description= "",
    version= "0.0.1",
	docs_url= None,
	redoc_url= None,
	redoc_favicon_url=urlIcon
)

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title= titleDoc, swagger_favicon_url=urlIcon)

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

async def validate_library(library: str = Path(..., title="Library", description=f"Librarys to search available: {', '.join(valid_libraries)}")):
    if library not in valid_libraries:
        raise HTTPException(status_code=400, detail=f"Invalid library. Valid options are: {', '.join(valid_libraries)}")
    return library

@app.get("/search/{library}", response_model=List[BookData], tags=["Requests Public 🌎"])
async def search_books_in_specif_library(
     library: LibraryEnum = Depends(validate_library),
     search_query: str = Depends(validate_search_query)
     ):
    scraped_books = scraping_functions[library](search_query)
    return scraped_books

@app.get("/libraries", response_model=list, tags=["Requests Public 🌎"])
async def get_libraries_availables():
    """
    Get a list of **available libraries** 📚.

    Returns a list of valid library options.
    """
    return valid_libraries