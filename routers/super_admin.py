from fastapi import APIRouter, HTTPException, Depends, status
from models import UsersModel, WishListModel, BooksModel
from general import JWTBearer, db_dependencies
from routers.auth import bcrypt_context
from schema import AddBookSchema, RegisterSchema, AdminCreateUserSchema

router = APIRouter(prefix='/super-admin', tags=['Super admin'])

@router.get('/books/all', status_code=status.HTTP_200_OK)
async def get_al_books(user: Depends(JWTBearer), db: db_dependencies):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    books = db.query(BooksModel).all()
    return {'books': books}

@router.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(user: Depends(JWTBearer), db: db_dependencies, book_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    try:
        book = db.query(BooksModel).filter_by(id=book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        return {'book': book}
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

@router.post('/books/create', status_code=status.HTTP_201_CREATED)
async def create_book(user: Depends(JWTBearer), add_book_request: AddBookSchema, db: db_dependencies):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    try:
        add_book = BooksModel(**add_book_request.dict(), creator_id=user.get('id'))
        db.add(add_book)
        db.commit()
        return {'message': 'Book successfully created'}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Book already exists or Bad request: {e}')
@router.delete('/books/delete/{book_id}', status_code=status.HTTP_200_OK)
async def delete_book(user: Depends(JWTBearer), db: db_dependencies, book_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    try:
        db.query(BooksModel).filter_by(id=book_id).delete()
        db.commit()
        return {'message': 'Book successfully deleted'}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book not found or bad request. Error: {e}')

@router.patch('/books/update/{book_id}', status_code=status.HTTP_200_OK)
async def update_book(user: Depends(JWTBearer), db: db_dependencies, book_request: AddBookSchema, book_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    book = db.query(BooksModel).filter_by(id=book_id)
    if not book:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    book.update({'title': book_request.title, 'description': book_request.description})
    db.commit()
    return {'message': 'Updated', 'success': True}

@router.get('/users/all', status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependencies, user: Depends(JWTBearer)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return {'count': db.query(UsersModel).count()}

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_in_model(db: db_dependencies, user: Depends(JWTBearer), user_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    get_user = db.query(UsersModel).filter_by(id=user_id)
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return {'user': get_user}

@router.patch('/users/update/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(db: db_dependencies, user: Depends(JWTBearer), user_id: int, update_request: RegisterSchema):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    get_user = db.query(UsersModel).filter_by(id=user_id)
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    get_user.update({
        'first_name': update_request.first_name,
        'last_name': update_request.last_name,
        'username': update_request.last_name,
        'password': bcrypt_context.hash(update_request.password),
        'email': update_request.email,
        'phone_number': update_request.phone_number,
        'gander': update_request.gander,
    })
    db.commit()
    return {'success': True, 'message': 'Updated'}

@router.delete('/users/delete/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependencies, user: Depends(JWTBearer), user_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    db.query(UsersModel).filter_by(id=user_id).delete()
    return {'success': True, 'message': 'Deleted'}

@router.post('/users/create-user', status_code=status.HTTP_201_CREATED)
async def super_admin_create_user(db: db_dependencies, user: Depends(JWTBearer), user_request: AdminCreateUserSchema):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authenticated')
    if user.get('role') != 'super-admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    new_user = UsersModel(**user_request.dict())
    db.add(new_user)
    db.commit()
    return {'success': True, 'message': 'Usercreated'}
