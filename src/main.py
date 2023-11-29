from typing import Annotated
from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from mysql.connector import Error
import mysql.connector

app = FastAPI()

templates = Jinja2Templates(directory="./templates")

# CREATE SERVER CONNECTION
def create_server_connection():
    cnx = None
    DB_USER="todo"
    DB_PASSWORD="1234"
    DB_HOST="127.0.0.1"
    DB_DATABASE="todo"
    try:
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
        print("Database connection successful")
    except Error as err:
        print("Error, `{err}`")
    return cnx

def insertIntoDB(cnx, item):   
    cursor = cnx.cursor()
    query = "INSERT INTO items (item) VALUES (%s)"
    data = [item]
    try:
        cursor.execute(query, data)
        cnx.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=RedirectResponse)
def post_db(item: Annotated[str, Form()]):
    cnx = create_server_connection()
    print("CONNECTION", cnx)
    insertIntoDB(cnx, item)
    return RedirectResponse(url="http://127.0.0.1:8000", status_code=303)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

