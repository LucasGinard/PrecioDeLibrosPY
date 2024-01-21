from pydantic import BaseModel, HttpUrl

class BookDetailData(BaseModel):
    title: str
    author: str
    image_url: HttpUrl
    price: str
    description: str
    category:str
    isbn: str
    