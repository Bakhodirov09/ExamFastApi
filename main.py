from fastapi import FastAPI
from routers import auth, books, super_admin

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(super_admin.router)