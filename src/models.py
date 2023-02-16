from sqlalchemy import Date, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self): # pragma: no cover
        return f"<{type(self).__name__}(id={self.id}"


class Reader(BaseModel):
    __tablename__ = "reader"
    name = Column(String)
    telephone = Column(String)
    address = Column(String)
    giving = relationship("Giving", back_populates="reader")


class Book(BaseModel):
    __tablename__ = "book"
    name = Column(String)
    author = Column(String)
    year = Column(Integer)
    price = Column(Integer)
    quantity = Column(Integer)
    publishing_id = Column(Integer, ForeignKey("publishing.id"))
    publishing = relationship("Publishing", back_populates="book")
    giving = relationship("Giving", back_populates="book")


class Publishing(BaseModel):
    __tablename__ = "publishing"
    name = Column(String)
    city = Column(String)
    book = relationship("Book", back_populates="publishing")


class Giving(BaseModel):
    __tablename__ = "giving"
    date = Column(Date)
    mark = Column(String)
    reader_id = Column(Integer, ForeignKey("reader.id"))
    book_id = Column(Integer, ForeignKey("book.id"))
    reader = relationship("Reader", back_populates="giving")
    book = relationship("Book", back_populates="giving")

