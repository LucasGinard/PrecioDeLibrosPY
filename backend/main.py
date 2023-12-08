from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.params import Query

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

def validate_search_query(book: str = Query(..., alias="book")):
    if not book or not book.strip():
        raise HTTPException(status_code=400, detail="empty value search")
    return book.strip()

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title= titleDoc, swagger_favicon_url=urlIcon)

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url="/openapi.json", title= titleDoc, redoc_favicon_url=urlIcon)

@app.get("/search", response_model=List[BookData], tags=["Requests Public"])
async def search_books(book: str = Depends(validate_search_query)):
    scraped_books = scrape_books(book)
    return scraped_books