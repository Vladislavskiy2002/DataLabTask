
from datetime import date
from typing import List

from fastapi.encoders import jsonable_encoder
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE
import asyncio
import psycopg2

from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()

con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
cur = con.cursor()

class Menu(BaseModel):
    id: int
    named: str
    types: str
    cost: int

class Orderi(BaseModel):
    id:int
    created_date: date
    updated_date: date
    address: str

class OrderDTO(BaseModel):
    id: int
    address: str
    products: List[Menu]


sql_schript1 = """  
CREATE TABLE IF NOT EXISTS menu (
    id integer PRIMARY KEY,
    named character varying(255) COLLATE pg_catalog."default",
    types character varying(255) COLLATE pg_catalog."default",
    cost integer NOT NULL
);
"""

sql_schript2 = """
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY,
    created_date DATE NOT NULL,
    updated_date DATE NOT NULL,
    address character varying(255) COLLATE pg_catalog."default"
);
"""

sql_schript3 = """
CREATE TABLE IF NOT EXISTS order_menu (
    id INT PRIMARY KEY,
    order_id INT,
    menu_id INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_id) REFERENCES menu(id)
);
"""

sql_schript4 = """
INSERT INTO menu(
	id, named, types, cost)
	VALUES (365, 'hot-dog', 'bread', 32);
"""
sql_schript5 = """
INSERT INTO orders(
	id, created_date, updated_date, address)
	VALUES (251, '2023-09-05', '2023-09-05', 'Князя Романа 23');
"""
sql_schript6 = """
INSERT INTO order_menu(id, order_id, menu_id)
	VALUES (2,2, 1);
"""
sql_schript7 = """	
INSERT INTO order_menu(
	id, order_id, menu_id)
	VALUES (2, 1);
);"""

# @app.on_event("startup")
# async def create_database():
#     await asyncio.sleep(10)
#
#     global con
#
#     # con = psycopg2.connect(dbname="postgres", user="postgres", host="db", password="1234")
#     con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
#
#     con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
#
#     cur = con.cursor()
#
#     # try:
#         # cur.execute(sql.SQL("CREATE DATABASE datalab_db;"))
#         # cur.execute(sql.SQL(sql_schript3))
#         # cur.execute(sql.SQL(sql_schript4))
#         # cur.execute(sql.SQL(sql_schript5))
#         # cur.execute(sql.SQL(sql_schript6))
#         # cur.execute(sql.SQL(sql_schript7))
#     #
#     # except:
#         # cur.execute(sql.SQL("DROP DATABASE datalab_db;"))
#         # cur.execute(sql.SQL("CREATE DATABASE datalab_db;"))
#         # cur.execute(sql.SQL(sql_schript1))
#         # cur.execute(sql.SQL(sql_schript2))
#         # cur.execute(sql.SQL(sql_schript3))
#         # cur.execute(sql.SQL(sql_schript4))
#         # cur.execute(sql.SQL(sql_schript5))
#         # cur.execute(sql.SQL(sql_schript6))
#         # cur.execute(sql.SQL(sql_schript7))
#
#     # db_con = psycopg2.connect(dbname="test", user="postgres", host="db", password="1234"
#     db_con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
#
#     cur = db_con.cursor()
#     db_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur.execute(sql.SQL("CREATE TABLE IF NOT EXISTS test_table (id int);"))

global order
products = []
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/product/remove/{name}")
async def root(name: str):
    global products
    select_value = (name,)
    select_script = "SELECT * FROM menu where named = %s"
    products.remove(name)
    print(products)
    return JSONResponse(status_code=status.HTTP_200_OK)
@app.get("/product/all")
async def root():
    global products
    return products
@app.get("/orders")
async def root():
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    result = cur.fetchall()
    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/menus")
async def root():
    global products
    cur = con.cursor()
    cur.execute("SELECT * FROM menu")
    result = cur.fetchall()
    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
@app.get("/menus/{message}")
async def root(message:str):
    global products
    cur = con.cursor()
    newmessege = message
    select_value = (newmessege,)
    select_script = "SELECT * FROM menu where named = %s"
    cur.execute(select_script, select_value)
    result = cur.fetchall()
    if result is None:
        return message + "isn't exist"
    # con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    products.append(message)
    return JSONResponse(content=json_compatible_item_data)
@app.post("/orders")
def add_orderdto(order: OrderDTO):
    cur = con.cursor()

    # insert_menu_script = "Insert into menu(id,named,types,cost) VALUES (%s,%s,%s,%s)"
    insert_orders_script = "Insert into orders(created_date,updated_date,address) VALUES (%s,%s,%s)"
    select_script = "SELECT MAX(id) FROM orders"
    cur.execute(select_script)
    insert_menu_orders_script = "Insert into order_products(order_id, menu_id) VALUES (%s,%s)"
    order.id = cur.fetchone()
    insert_orders_value = (date.today().isoformat(),date.today().isoformat(), order.address)
    cur.execute(insert_orders_script, insert_orders_value)
    con.commit()

    for product in order.products:
        insert_menu_orders_value = (order.id, product.id)
        cur.execute(insert_menu_orders_script, insert_menu_orders_value)
        con.commit()

    con.commit()

orderdto = OrderDTO
@app.post("/orders/{address}")
def add_order(address: str):
    global orderdto
    orderdto.address = address
    if(products.__sizeof__() == 0):
        for product in products:
            print(product)
            select_value = (product,)
            select_script = "SELECT * FROM menu where named = %s"
            cur.execute(select_script, select_value)
            orderdto.products.append(Menu.parse_obj(cur.fetchone()))
    add_orderdto(orderdto)

    # cur.execute("SELECT types from menu");
    # result = cur.fetchall()
    # if result is None:
    #     return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    # products : List
    # while True :
    #     for type in result:
    #         if str == ("I'd like a " + type):
    #             print("which do you prefer?")
    #             cur.execute("SELECT named from menu");
    #             result2 = cur.fetchall()
    #             if result is None:
    #                 return JSONResponse(content="product haven't found", status_code=status.HTTP_404_NOT_FOUND)
    #             for name in result2:
    #                 if (str == "I'd like a " + name):
    #                     products.append(name)
    #         elif str == ("I don't want a " + name):
    #             products.remove(name)
    #         elif str == "That's all":
    #             print("Enter address: ")
    #             address = "ANY ADDRESS"
    #             order = OrderDTO
    #             order.address = address
    #             for product in products:
    #                 select_script = cur.execute("SELECT * from menu where name = %s");
    #                 select_value = (product,)
    #                 cur.execute(select_script, select_value)
    #                 order.products.append(cur.fetchone())
    #             add_order(order)
    #             break
    #         elif str == ("Yes, please"):
    #             name = "dsd"
    #         elif str == ("No, thank you"):
    #             name = "dsd"
    #         else:
    #             print("Sorry, i don't understand you!")
    #             print("Try again :)")
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
