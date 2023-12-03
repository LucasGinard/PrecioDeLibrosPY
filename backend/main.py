from fastapi import Depends, FastAPI, HTTPException
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

def validate_search_query(search_query: str = ""):
    if not search_query or not search_query.strip():
        raise HTTPException(status_code=400, detail="empty value search")
    return search_query.strip()

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title= titleDoc, swagger_favicon_url=urlIcon)

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url="/openapi.json", title= titleDoc, redoc_favicon_url=urlIcon)

@app.get("/search/{search_query}", response_model=List[BookData], tags=["Request Public"])
async def search_books(search_query: str = Depends(validate_search_query)):
    scraped_books = scrape_books(search_query)
    return scraped_books