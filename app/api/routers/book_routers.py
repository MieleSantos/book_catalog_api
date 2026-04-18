from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.book_model import Book
from app.repositories.book_service import create_book
from app.schemas.book_schemas import BookCreate, BookResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/books/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)) -> BookResponse:
    """Cria um novo livro no banco de dados"""
    return create_book(db, book.titulo, book.autor, book.data_publicacao, book.resumo)


@router.get(
    "/books/",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
)
def read_books(db: Session = Depends(get_db)):
    """Retorna uma lista de todos os livros no banco de dados"""
    return db.query(Book).all()


@router.get(
    "/books/author",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
)
def read_author_books(author: str, db: Session = Depends(get_db)):
    """Retorna uma lista de livros escritos por um autor específico"""
    query = db.query(Book)

    if author:
        query = query.filter(func.lower(Book.autor).like(f"%{author.lower()}%"))

    return query.all()


@router.get(
    "/books/titulo",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
)
def read_titulo_books(titulo: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Book)

    if titulo:
        query = query.filter(func.lower(Book.titulo).like(f"%{titulo.lower()}%"))

    return query.all()
