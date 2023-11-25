from typing import Union

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

titleDoc = "PrecioLibrosPY API"
urlIcon = "📚"

app = FastAPI(
	title= titleDoc,
    description= "",
    version= "0.0.1",
	docs_url= None,
	redoc_url= None
)

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title= titleDoc, swagger_favicon_url=urlIcon)

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url="/openapi.json", title= titleDoc, redoc_favicon_url=urlIcon)

@app.get("/")
def read_root():
    return {"Hello": "World"}