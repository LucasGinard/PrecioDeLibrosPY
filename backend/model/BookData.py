from pydantic import BaseModel, HttpUrl

class BookLibraryInfo(BaseModel):
    name: str
    website_url: HttpUrl

class BookData(BaseModel):
    title: str
    author: str
    image_url: HttpUrl
    price: str
    details_url: HttpUrl
    library:BookLibraryInfo