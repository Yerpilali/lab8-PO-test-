from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):

    name: str
    author: str
    year: int
    price: int
    quantity: int
    publishing_id: int

class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int


    class Config:
        orm_mode = True


class ReaderBase(BaseModel):

    name: str
    telephone: str
    address: str


class ReaderCreate(ReaderBase):

    pass


class Reader(ReaderBase):

    id: int

    class Config:

        orm_mode = True


class PublishingBase(BaseModel):

    name: str
    city: str


class PublishingCreate(PublishingBase):

    pass


class Publishing(PublishingBase):

    id: int

    class Config:

        orm_mode = True


class GivingBase(BaseModel):

    reader_id: int
    book_id: int
    date: date


class GivingCreate(GivingBase):
    pass


class Giving(GivingBase):
    id: int
    mark: str

    class Config:
        orm_mode = True

