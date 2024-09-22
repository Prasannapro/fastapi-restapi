from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from fastapi import HTTPException


app = FastAPI()


class Book(BaseModel):
    id : str = Field(default_factory=uuid4, unique=True)
    title : str = Field(min_length=3)
    author : str = Field(min_length=1 , max_length=40)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=-1,lt=101)

BOOKS = []

@app.get("/")
def readApi():
    return BOOKS

@app.post("/")
def createBook(book:Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
def updateBook(book_id: UUID,book:Book):
    cnt = 0
    for x in BOOKS:
        cnt+=1
        if x.id == book_id:
            BOOKS[cnt-1] = book
            return BOOKS[cnt-1]
    raise HTTPException(status_code=404,
                        detail=f"ID {book_id} : Does not exist")

@app.delete("/{book_id}")
def deleteBook(book_id:UUID):
    cnt =0
    for x in BOOKS:
        cnt+=1
        if x.id == book_id:
            del BOOKS[cnt-1]
            return f"ID : {book_id} deleted"
    raise HTTPException(status_code=404,
                        detail=f"ID {book_id} : Does not exist")