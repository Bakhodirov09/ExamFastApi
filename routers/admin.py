from fastapi import APIRouter, HTTPException, Depends, status
from models import BooksModel
from general import db_dependencies, JWTBearer
from schema import AddBookSchema

router = APIRouter(prefix='/admin', tags=['Admin'])

@router.get('/books/all', status_code=status.HTTP_200_OK)
async def get_all_admin_books(db: db_dependencies, user: Depends(JWTBearer)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return {'books': db.query(BooksModel).all()}

@router.get('/books/all/my', status_code=status.HTTP_200_OK)
async def get_admin_books(db: db_dependencies, user: Depends(JWTBearer)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return {'books': db.query(BooksModel).filter_by(creator_id=user.get('id'))}

@router.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(user: Depends(JWTBearer), db: db_dependencies, book_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    book = db.query(BooksModel).filter_by(id=book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return {'book': book}

@router.post('/books/create', status_code=status.HTTP_201_CREATED)
async def create_book(user: Depends(JWTBearer), add_book_request: AddBookSchema, db: db_dependencies):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    try:
        add_book = BooksModel(**add_book_request.dict(), creator_id=user.get('id'))
        db.add(add_book)
        db.commit()
        return {'message': 'Book successfully created', 'success': True}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Book already exists or Bad request: {e}')
@router.delete('/books/delete/{book_id}', status_code=status.HTTP_200_OK)
async def delete_book(user: Depends(JWTBearer), db: db_dependencies, book_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    try:
        db.query(BooksModel).filter_by(id=book_id, creator_id=user.get('id')).delete()
        db.commit()
        return {'message': 'Book successfully deleted'}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book not found or bad request. Error: {e}')

