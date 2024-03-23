from pydantic import BaseModel, HttpUrl

from model.LibraryEnum import LibraryInfo

class BookData(BaseModel):
    title: str
    author: str
    image_url: HttpUrl
    price: str
    details_url: HttpUrl
    library:LibraryInfo