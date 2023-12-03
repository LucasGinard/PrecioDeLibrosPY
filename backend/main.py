from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from scraping import scrape_books

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

@app.get("/search/{search_query}", response_model=List[BookData])
async def search_books(search_query: str):
    scraped_books = scrape_books(search_query)
    return scraped_books