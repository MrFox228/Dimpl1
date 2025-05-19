from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    conn = sqlite3.connect("database.db")  
    conn.row_factory = sqlite3.Row 
    return conn

@app.get('/')
def empty():
    return RedirectResponse(url="/login")

@app.get("/login")
def get_login(request: Request):
    token = request.cookies.get("access_token")
    if token == 'yes':
        return RedirectResponse(url="/index")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/login')
def auth(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT login, password FROM auth WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    conn.close()

    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email не найден"})

    db_username, db_password = user 
    
    if db_username != username:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверное имя пользователя"})
    
    if db_password != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный пароль"})

    response = RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value="yes", httponly=True)
    return response


@app.get("/token")
def token_is_see(request: Request):
    token = request.cookies.get("access_token")
    if token == 'yes':
        return RedirectResponse(url="/index")
    return RedirectResponse(url="/login")

@app.post("/token")
def get_token():
    response = RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value="yes", httponly=True)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value="no", httponly=True)
    return response

@app.get('/index')
def index(request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'index'")
    index_ = cursor.fetchall()  
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "data": index_})

@app.get('/add-index/{id}/{description}/{quantity}/{price}')
def add_index(id, description, quantity, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'index' (id, description, quantity, price) VALUES (?,?,?,?)", (id, description, quantity, price))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/index")
@app.get('/del-index/{id}/{description}/{quantity}/{price}')
def del_index(id, description, quantity, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    print('asd')
    cursor.execute("DELETE FROM 'index' WHERE id = ? AND description = ?", (id, description))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/index")

@app.get('/edit-index/{id}/{description}/{quantity}/{price}/{oldId}/{oldDescription}/{oldPrice}/{oldQuantity}/')
def edit_index(id,description, quantity, price, oldId, oldDescription, oldPrice, oldQuantity, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( """
        UPDATE 'index' 
        SET id = ?, description = ?, quantity = ?, price = ? 
        WHERE id = ? AND description = ? AND quantity = ? AND price = ?
        """, (id, description, quantity, price, oldId, oldDescription, oldQuantity, oldPrice),
    ) 
    conn.commit()
    conn.close()
    return RedirectResponse(url="/index")

@app.get('/products')
def products(request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'products'")
    index_ = cursor.fetchall()  
    conn.close()
    return templates.TemplateResponse("products.html", {"request": request, "data": index_})

@app.get('/add-products/{id}/{name}/{quantity}/{price}')
def add_products(id, name, quantity, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'products' (id, name, quantity, price) VALUES (?,?,?,?)", (id, name, quantity, price))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/products")
@app.get('/del-products/{id}/{name}/{quantity}/{price}')
def del_products(id, name, quantity, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    print('asd')
    cursor.execute("DELETE FROM 'products' WHERE id = ? AND name = ?", (id, name))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/products")

@app.get('/edit-products/{id}/{name}/{quantity}/{price}/{oldId}/{oldName}/{oldPrice}/{oldQuantity}/')
def edit_products(id,name, quantity, price, oldId, oldName, oldPrice, oldQuantity,request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( """
        UPDATE 'products' 
        SET id = ?, name = ?, quantity = ?, price = ? 
        WHERE id = ? AND name = ? AND quantity = ? AND price = ?
        """, (id, name, quantity, price, oldId, oldName, oldQuantity, oldPrice),
    ) 
    conn.commit()
    conn.close()
    return RedirectResponse(url="/products")


@app.get('/purchases')
def purchases(request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'purchases'")
    index_ = cursor.fetchall()  
    conn.close()
    return templates.TemplateResponse("purchases.html", {"request": request, "data": index_})


@app.get('/add-purchases/{id}/{data}/{provider}/{products}/{quantity}/{price}')
def add_purchases(id, data, provider,products ,quantity, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'purchases' (id, data, provider,products,quantity, price) VALUES (?,?,?,?,?,?)", (id, data, provider,products,quantity,price))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/purchases")
@app.get('/del-purchases/{id}/{data}/{provider}/{products}/{quantity}/{price}')
def del_purchases(id, data, price, quantity, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()  
    cursor.execute("DELETE FROM 'purchases' WHERE id = ? AND data = ?", (id, data))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/purchases")

@app.get('/edit-purchases/{id}/{data}/{provider}/{products}/{quantity}/{price}/{oldId}/{oldData}/{oldPrice}/{oldProducts}/{oldProvider}/{oldQuantity}')
def edit_purchases(id,data, provider,products,quantity,price ,oldId,oldData , oldPrice, oldProvider,oldProducts,oldQuantity, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( """
        UPDATE 'purchases' 
        SET id = ?, data = ?, provider = ?,products = ?, quantity = ?,price = ? 
        WHERE id = ? AND data = ? AND provider = ? AND products = ? AND quantity = ? AND price = ?
        """, (id, data, provider,products,quantity, price, oldId, oldData, oldProvider, oldProducts,oldQuantity, oldPrice),
    ) 
    conn.commit()
    conn.close()
    return RedirectResponse(url="/purchases")


@app.get('/sales')
def sales(request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'sales'")
    index_ = cursor.fetchall()  
    conn.close()
    return templates.TemplateResponse("sales.html", {"request": request, "data": index_})


@app.get('/add-sales/{id}/{data}/{products}/{price}')
def add_sales(id, data, products, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'sales' (id, data, products, price) VALUES (?,?,?,?)", (id, data, products, price))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/sales")
@app.get('/del-sales/{id}/{data}/{products}/{price}')
def del_sales(id, data, products, price, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    print('asd')
    cursor.execute("DELETE FROM 'sales' WHERE id = ? AND data = ?", (id, data))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/sales")

@app.get('/edit-sales/{id}/{data}/{products}/{price}/{oldId}/{oldData}/{oldPrice}/{oldProducts}/')
def edit_sales(id,data, products, price, oldId, oldData, oldPrice, oldProducts, request: Request):
    token = request.cookies.get("access_token")
    if token != 'yes':
        return RedirectResponse(url="/login")    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( """
        UPDATE 'sales' 
        SET id = ?, data = ?, products = ?, price = ? 
        WHERE id = ? AND data = ? AND products = ? AND price = ?
        """, (id, data, products, price, oldId, oldData, oldProducts, oldPrice),
    ) 
    conn.commit()
    conn.close()
    return RedirectResponse(url="/sales")