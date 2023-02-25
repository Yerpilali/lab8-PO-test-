from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from src.models import Base
from datetime import date
from os import environ

SQLALCHEMY_DATABASE_URL = environ.get('DATABASE_URL') # тестовая бд

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_reader():
    """
    Тест на создание нового пользователя
    """
    response = client.post(
        "/readers/",
        json={"telephone": "88005553535", "name": "Акакий", "address": "Улица Пушкина"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["telephone"] == "88005553535"


def test_get_readers():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/readers/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["telephone"] == "88005553535"


def test_create_exist_reader():
    """
    Проверка случая, когда мы пытаемся добавить существующего пользователя
    в БД, т.е. когда данный email уже присутствует в БД.
    """
    response = client.post(
        "/readers/",
        json={"telephone": "88005553535", "name": "Акакий", "address": "Улица Пушкина"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Telephone already registered"



def test_get_readers_by_id():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/readers/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["telephone"] == "88005553535"


def test_readers_not_found():
    """
    Проверка случая, если пользователь с таким id отсутствует в БД
    """
    response = client.get("/readers/100")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_publishing():
    """
    Тест на создание нового пользователя
    """
    response = client.post(
        "/publishings/",
        json={"name": "Азбука", "city": "Москва"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Азбука"


def test_get_publishings():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/publishings/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "Азбука"


def test_get_publishings_by_id():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/publishing/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Азбука"


def test_publishings_not_found():
    """
    Проверка случая, если пользователь с таким id отсутствует в БД
    """
    response = client.get("/publishing/100")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "publishing not found"


def test_book():
   response = client.post(
       "/books/",
      json={"name": "тихий дон", "author": "Шолохов", "year": 1940, "price": 150, "quantity": 98, "publishing_id":1, "id": 1}
   )
   assert response.status_code == 200, response.text
   data = response.json()
   assert data["name"] == "тихий дон"


def test_books_not_found():
    """
    Проверка случая, если пользователь с таким id отсутствует в БД
    """
    response = client.get("/books/100")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_get_books():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/books/")
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    assert data[0]["name"] == "тихий дон"
    assert data[0]["author"] == "Шолохов"
    assert data[0]["year"] == 1940
    assert data[0]["price"] == 150
    assert data[0]["quantity"] == 98
    assert data[0]["publishing_id"] == 1


def test_giving():
    """
    Тест на создание нового пользователя
    """
    response = client.post(
        "/givings/",
        json={"date": str(date.today()), "mark": "Акакий", "reader_id": 1, "book_id": 1, "id": 1}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["mark"] == "Акакий"


def test_givings_not_found():
    """
    Проверка случая, если пользователь с таким id отсутствует в БД
    """
    response = client.get("/giving/100")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "giving not found"


def test_get_givings():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/givings/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["mark"] == "Акакий"


def test_book_2():
   response = client.post(
       "/books/",
      json={"name": "тихий дон", "author": "Шолохов", "year": 1940, "price": 150, "quantity": 98, "publishing_id":5453451, "id": 1}
   )
   assert response.status_code == 404, response.text
   assert response.text == '{"detail":"Издателя с таким кодом не существует"}'


def test_books_found_1():
    response = client.get("/books/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "тихий дон"


def test_books__found_2():
    response = client.get("/books/32424")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_giving_2():
    """
    Тест на создание нового пользователя
    """
    response = client.post(
        "/givings/",
        json={"date": str(date.today()), "mark": "Акакий", "reader_id": 1000, "book_id": 1, "id": 1}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Читателя с таким кодом не существует"


def test_giving_3():
    """
    Тест на создание нового пользователя
    """
    response = client.post(
        "/givings/",
        json={"date": str(date.today()), "mark": "Акакий", "reader_id": 1, "book_id": 1000, "id": 1}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Книги с таким кодом не существует"


def test_get_givings_2():
    response = client.get("/giving/21342")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "giving not found"


def test_get_givings_3():
    response = client.get("/giving/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["mark"] == "Акакий"
