from sqlalchemy.orm import Session
from src import models, schemas
from datetime import datetime


def create_reader(db: Session, reader: schemas.ReaderCreate):

    db_reader = models.Reader(name=reader.name, telephone=reader.telephone, address=reader.address)
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


def get_reader_by_phone(db: Session, telephone: str):

    return db.query(models.Reader).filter(models.Reader.telephone == telephone).first()


def get_reader(db: Session, reader_id: int):

    return db.query(models.Reader).filter(models.Reader.id == reader_id).first()


def get_readers(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Reader).offset(skip).limit(limit).all()


def update_product_amount(db: Session, book_id: int, product_amount: int):
    db_book = get_book_by_id(db=db, book_id=book_id)
    db_book.quantity += product_amount
    if db_book.quantity >= 0:
        db.commit()
    return db_book


def get_book_by_id(db: Session, book_id: int):

    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_publishing_by_id(db: Session, publishing_id: int):

    return db.query(models.Publishing).filter(models.Publishing.id == publishing_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_publishing = get_publishing_by_id(db=db, publishing_id=book.publishing_id)
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):

    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Book).offset(skip).limit(limit).all()


def create_giving(db: Session, giving: schemas.GivingCreate):

    # date = datetime.now()
    db_book = get_book_by_id(db=db, book_id=giving.book_id)
    db_reader = get_reader(db=db, reader_id=giving.reader_id)
    db_giving = models.Giving(date=giving.date, mark=db_reader.name, book_id=db_book.id, reader_id=db_reader.id)

    if 1 <= db_book.quantity:
        update_product_amount(db=db,
                              book_id=db_giving.book_id,
                              product_amount=-1)

    db.add(db_giving)
    db.commit()
    db.refresh(db_giving)
    return db_giving


def get_giving(db: Session, giving_id: int):

    return db.query(models.Giving).filter(models.Giving.id == giving_id).first()


def get_givings(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Giving).offset(skip).limit(limit).all()


def create_publishing(db: Session, publishing: schemas.PublishingCreate):

    db_publishing = models.Publishing(name=publishing.name, city=publishing.city)
    db.add(db_publishing)
    db.commit()
    db.refresh(db_publishing)
    return db_publishing


def get_publishing(db: Session, publishing_id: int):

    return db.query(models.Publishing).filter(models.Publishing.id == publishing_id).first()


def get_publishings(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Publishing).offset(skip).limit(limit).all()


