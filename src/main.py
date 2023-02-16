from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import SessionLocal, engine
from typing import List
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():# pragma: no cover
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/readers/", response_model=schemas.Reader)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    db_reader = crud.get_reader_by_phone(db, telephone=reader.telephone)
    if db_reader:
        raise HTTPException(status_code=400, detail="Telephone already registered")
    return crud.create_reader(db=db, reader=reader)


@app.get("/readers/", response_model=List[schemas.Reader])
def read_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    readers = crud.get_readers(db, skip=skip, limit=limit)
    return readers


@app.get("/readers/{reader_id}", response_model=schemas.Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = crud.get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_reader


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate,  db: Session = Depends(get_db)):
    db_book_publishing = crud.get_publishing(db, publishing_id=book.publishing_id)
    if not db_book_publishing:
        raise HTTPException(status_code=404, detail="Издателя с таким кодом не существует")
    return crud.create_book(db, book=book)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_book


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.post("/publishings/", response_model=schemas.Publishing)
def create_publishing(publishing: schemas.PublishingCreate, db: Session = Depends(get_db)):
    db_publishing = crud.create_publishing(db, publishing=publishing)
    return db_publishing


@app.get("/publishings/", response_model=List[schemas.Publishing])
def read_publishings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    publishings = crud.get_publishings(db, skip=skip, limit=limit)
    return publishings


@app.get("/publishing/{publishing_id}", response_model=schemas.Publishing)
def read_publishing(publishing_id: int, db: Session = Depends(get_db)):
    db_publishing = crud.get_publishing(db, publishing_id=publishing_id)
    if db_publishing is None:
        raise HTTPException(status_code=404, detail="publishing not found")
    return db_publishing


@app.post("/givings/", response_model=schemas.Giving)
def create_giving(giving: schemas.Giving, db: Session = Depends(get_db)):
    db_giving_reader = crud.get_reader(db, reader_id=giving.reader_id)
    db_giving_book = crud.get_book(db, book_id=giving.book_id)
    if not db_giving_reader:
        raise HTTPException(status_code=404, detail="Читателя с таким кодом не существует")
    if not db_giving_book:
        raise HTTPException(status_code=404, detail="Книги с таким кодом не существует")
    return crud.create_giving(db, giving=giving)


@app.get("/givings/", response_model=List[schemas.Giving])
def read_givings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    givings = crud.get_givings(db, skip=skip, limit=limit)
    return givings


@app.get("/giving/{giving_id}", response_model=schemas.Giving)
def read_giving(giving_id: int, db: Session = Depends(get_db)):
    db_giving = crud.get_giving(db, giving_id=giving_id)
    if db_giving is None:
        raise HTTPException(status_code=404, detail="giving not found")
    return db_giving


