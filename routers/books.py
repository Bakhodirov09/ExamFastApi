from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from general import db_dependencies, JWTBearer
from models import BooksModel, WishListModel

router = APIRouter(prefix='/books', tags=['Books'])

@router.get('/all', status_code=status.HTTP_200_OK)
async def get_all_books(db: db_dependencies, user: Depends(JWTBearer)):
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not authenticated')
    books = db.query(BooksModel).all()
    return {'books': books}

@router.get('/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(db: db_dependencies, user: Depends(JWTBearer), book_id: int):
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not authenticated')
    try:
        book = db.query(BooksModel).filter_by(id=book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        return {'book': book}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

@router.post('/add-to-wish-list/{book_id}', status_code=status.HTTP_200_OK)
async def add_to_wish_list(db: db_dependencies, book_id: int, user: Annotated[dict, Depends(JWTBearer)]):
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not authenticated')
    try:
        book = db.query(BooksModel).filter_by(id=book_id)
        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        add_wish = WishListModel(book_id=book.get('id'), user_id=user.get('id'))
        db.add(add_wish)
        db.commit()
        return {'message': 'Successfully created'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error occurred: {str(e)}")

@router.post('/delete-to-wish-list/{wish_id}', status_code=status.HTTP_200_OK)
async def add_to_wish_list(db: db_dependencies, wish_id: int, user: Annotated[dict, Depends(JWTBearer)]):
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not authenticated')
    try:
        wish_book = db.query(WishListModel).filter_by(id=wish_id, user_id=user.get('id'))
        if wish_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wish book not found')
        delete_wish = WishListModel(book_id=wish_book.get('id'), user_id=user.get('id'))
        db.delete(delete_wish)
        db.commit()
        return {'message': 'Successfully deleted'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")