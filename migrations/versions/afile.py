"""empty message
Revision ID: afile
Revises: 15fb78103251
Create Date: 2022-11-21 15:488:02.606415
"""
from alembic import op
from sqlalchemy.orm import Session
from datetime import datetime

from src.models import Book, Giving, Reader, Publishing

revision = 'afile'
down_revision = '15fb78103251'
branch_labels = None
depends_on = None


def upgrade() -> None:

    bind = op.get_bind()
    session = Session(bind=bind)

    book_a = Book(name='тихий дон', author='Шолохов', year=1940, price=150, quantity=5)
    book_b = Book(name='Мастер и Маргарита', author='Булгаков', year=1966, price=150, quantity=9)
    session.add_all([book_a,book_b])
    session.flush()

    read_a = Reader(name='Акакий', telephone='88005553535', address='Улица Пушкина')
    read_b = Reader(name='Гоша', telephone='88002345675', address='дом Колотушкина')
    session.add_all([read_a,read_b])
    session.flush()

    publ_a = Publishing(name='Азбука', city='Москва')
    publ_b = Publishing(name='АСТ', city='Москва')
    session.add_all([publ_a,publ_b])
    session.flush()

    giv_a = Giving(mark= 'dfdf')
    giv_b = Giving(mark='asa')
    session.add_all([giv_a,giv_b])
    session.flush()

def downgrade() -> None:
    pass
