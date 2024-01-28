from typing import List
from pydantic import BaseModel, HttpUrl

class BookDetailData(BaseModel):
    title: str
    author: str
    image_url: HttpUrl
    price: str
    description: str
    category:List[str]
    isbn: str
    