import logging
import random
from datetime import date
from typing import List
from fastapi.encoders import jsonable_encoder
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

# con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
con = psycopg2.connect(dbname="postgres", user="postgres", host="35.222.13.116", password="1234")
# con = psycopg2.connect(dbname="postgres", user="postgres", host="db", password="1234")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

class Menu(BaseModel):
    id: int
    named: str
    types: str
    cost: int

class OrderiDTO(BaseModel):
    order_products: List[Menu]
    total:str

# sql_schript1 = """
# CREATE SEQUENCE IF NOT EXISTS menu_id_seq;
# CREATE SEQUENCE IF NOT EXISTS order_products_id_seq;
# CREATE TABLE IF NOT EXISTS public.menu
# (
#     id integer NOT NULL DEFAULT nextval('menu_id_seq'::regclass),
#     named character varying(255) COLLATE pg_catalog."default",
#     types character varying(255) COLLATE pg_catalog."default",
#     cost integer NOT NULL,
#     CONSTRAINT menu_pkey PRIMARY KEY (id),
#     CONSTRAINT menu_id_unique UNIQUE (id)
# );
# """
#
# sql_schript2 = """
# CREATE TABLE IF NOT EXISTS public.orders
# (
#     id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
#     created_date date NOT NULL,
#     updated_date date NOT NULL,
#     # address character varying(255) COLLATE pg_catalog."default",
#     CONSTRAINT orders_pkey PRIMARY KEY (id)
# );
# """
#
# sql_schript3 = """
# CREATE TABLE IF NOT EXISTS order_products (
#     id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
#     order_id integer,
#     menu_id integer,
#     CONSTRAINT order_products_pkey PRIMARY KEY (id),
#     CONSTRAINT order_products_menu_id_fkey FOREIGN KEY (menu_id)
#         REFERENCES public.menu (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION,
#     CONSTRAINT order_products_order_id_fkey FOREIGN KEY (order_id)
#         REFERENCES public.orders (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
# );
# """
#
# sql_schript4 = """
# CREATE TABLE IF NOT EXISTS public.order_messages
# (
#     id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
#     order_id integer,
#     assistant_messages character varying(1000) COLLATE pg_catalog."default",
#     user_messages character varying(1000) COLLATE pg_catalog."default",
#     CONSTRAINT order_messages_order_id_fkey FOREIGN KEY (order_id)
#         REFERENCES public.orders (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
# )"""

# @app.on_event("startup")
# async def create_database():
#     await asyncio.sleep(10)
#
#     global con
#
#     con = psycopg2.connect(dbname="postgres", user="postgres", host="db", password="1234")
#     # con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
#
#     con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
#
#     cur = con.cursor()
#
#     try:
#         cur.execute(sql.SQL("CREATE DATABASE datalab_db;"))
#         cur.execute(sql.SQL(sql_schript1))
#         cur.execute(sql.SQL(sql_schript2))
#         cur.execute(sql.SQL(sql_schript3))
#         cur.execute(sql.SQL(sql_schript4))
#         # cur.execute(sql.SQL(sql_schript5))
#         # cur.execute(sql.SQL(sql_schript6))
#         # cur.execute(sql.SQL(sql_schript7))
#     #
#     except:
#         cur.execute(sql.SQL("DROP DATABASE datalab_db;"))
#         cur.execute(sql.SQL("CREATE DATABASE datalab_db;"))
#         cur.execute(sql.SQL(sql_schript1))
#         cur.execute(sql.SQL(sql_schript2))
#         cur.execute(sql.SQL(sql_schript3))
#         cur.execute(sql.SQL(sql_schript4))
        # cur.execute(sql.SQL(sql_schript5))
        # cur.execute(sql.SQL(sql_schript6))
        # cur.execute(sql.SQL(sql_schript7))

    # db_con = psycopg2.connect(dbname="test", user="postgres", host="db", password="1234")
    # # db_con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
    #
    # cur = db_con.cursor()
    # db_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # cur.execute(sql.SQL("CREATE TABLE IF NOT EXISTS test_table (id int);"))

products = []
newProductType = ""
newProductName = ""
newProductCost = ""
chatHistory = []
newRandomProduct = []

lastAdminAssistantResponce = ""

flag = False
start = False
startAdmin = True

import openai

openai.api_key = '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'

@app.get("/")
async def root():
    return {"message": "Hello World"}
#
@app.get("/admin/setToDefault")
async def setStartProgramMessegeAsAdminByDefault():
    global startAdmin
    startAdmin = True
    return True
@app.get("/setToDefault")
async def setStartProgramMessegeAsUserByDefault():
    global start
    global flag
    global lastAdminAssistantResponce
    global newProductType
    global newProductName
    global newProductCost
    global products
    global chatHistory
    global newRandomProduct
    global status
    start = False
    flag = False
    lastAdminAssistantResponce=""
    newProductType=""
    newProductName=""
    newProductCost=""
    status = ""
    products = []
    chatHistory = []
    newRandomProduct = []
@app.get("/startprogram")
async def getStartProgramMessege():
    global start
    if start:
        start = False
        return "Welcome at the coffee shoP What would you like?"
@app.get("/admin/handler/{message}")
async def handler(message: str):
    global startAdmin
    global lastAdminAssistantResponce
    global newProductType
    global newProductName
    global newProductCost
    global status

    if startAdmin and message == "add" or message == "update" or message == "stock":
        status = message
        startAdmin = False
        lastAdminAssistantResponce = "Enter the type of product"
        return lastAdminAssistantResponce
    elif lastAdminAssistantResponce is "Enter the type of product":
        newProductType = message
        startAdmin = False
        lastAdminAssistantResponce = "Enter the name of product"
        return lastAdminAssistantResponce
    elif lastAdminAssistantResponce is "Enter the name of product":
        if checkIfCurrentProductExistByName(message) and status == "add":
            logging.info(checkIfCurrentProductExistByName(message))
            return "Product with current name has already exist. Try again to write the product's name:"
        if checkIfCurrentProductExistByName(message) and checkIfCurrentProductExistByType(newProductType) and status == "stock":
            logging.info(checkIfCurrentProductExistByName(message))
            newProductName = message
            lastAdminAssistantResponce = "Set the stock:"
            return "Set the stock:"
        elif not checkIfCurrentProductExistByName(message) and not checkIfCurrentProductExistByType(newProductType) and status == "stock":
            lastAdminAssistantResponce = ""
            startAdmin = True
            return "The product with name: " + message + " and type: " + newProductType + " isn't exist. Choose update, add or stock"

        newProductName = message
        lastAdminAssistantResponce = "Enter the costs:"
        return lastAdminAssistantResponce
    elif lastAdminAssistantResponce == "Set the stock:":
        if not message.isdecimal():
            return "the stock must be num. Try again"
        elif len(message) > 100:
            return "the stock must be less that 100"
        newProductStock = message
        newProduct = (newProductName, newProductType, newProductStock,)
        updateNewProductByStock(newProduct)
        startAdmin = True
        lastAdminAssistantResponce = ""
        return "The stock has been successfully set"
    elif lastAdminAssistantResponce == "Enter the costs:":
        newProductCost = message
        if not message.isdecimal():
            return "the cost's must be num. Try again"
        newProduct = (newProductName, newProductType, newProductCost,)
        lastAdminAssistantResponce = ""
        if status == "add":
            addNewProduct(newProduct)
            startAdmin = True
            return "The product has been successfully added. Choose update, add or stock"
        elif status == "update":
            startAdmin = True
            if checkIfCurrentProductExistByName(newProductName) == True and checkIfCurrentProductExistByType(newProductType) == True:
                updateNewProduct(newProduct)
                return "The product has been successfully updated. Choose update, add or stock"
            else:
                return "The product with name: " + newProductName + " and type: " + newProductType + " isn't exist. Choose update, add or stock"

    else:
        return "Something goes wrong ;("
#

@app.get("/handler/{message}")
async def handler(message: str):
    global flag
    global start
    global newRandomProduct
    global status
    if start:
        start = False
        chatHistory.append(("Welcome at the coffee shop \n What would you like?"))
        return "Welcome at the coffee shop \n What would you like? "
    if flag:
        if message == "yes":
            flag = False

            products.append(newRandomProduct[0])
            reduceStockByProductNameAndType([newRandomProduct[0], newRandomProduct[1]])
            chatHistory.append((message, "The " + str(newRandomProduct[0]) + " has been successfully added to your order"))
            return "The " + str(newRandomProduct[0]) + " has been successfully added to your order"
        elif message == "no":
            flag = False
            chatHistory.append((message,"Would you like something else?"))
            return "Would you like something else?"
        else:
            chatHistory.append((message, "I don't understand you. Try again"))
            return "I don't understand you. Try again"

    if message.startswith("I'd like a "):
        prompt = message.replace("I'd like a ", '', 1)
        data = getMenuByName(prompt)
        if data == prompt.__str__() + " isn't exist in our menu":
            chatHistory.append((message,prompt.__str__() + " isn't exist in our menu"))
            return prompt.__str__() + " isn't exist in our menu"
        if data == "I’m sorry but we’re out of " + str(prompt):
            chatHistory.append((message,"I’m sorry but we’re out of " + str(prompt)))
            return "I’m sorry but we’re out of " + str(prompt)
        reduceStockByProductNameAndType([data[0][1],data[0][2]])
        flag = True
        newRandomProduct = createRandomProduct()
        if newRandomProduct == "not found":
            flag = False
            chatHistory.append("Would you like something else?")
            return "Would you like something else?"
        chatHistory.append((message,"Would you like to add a " + str(newRandomProduct[0]) + " for $" + str(newRandomProduct[2])+ "?"))
        return "Would you like to add a " + str(newRandomProduct[0]) + " for $" + str(newRandomProduct[2]) + "?"
    elif message.startswith("I don't want a "):
        prompt = message.replace("I don't want a ", '', 1)
        if(products.__len__() ==0):
            chatHistory.append((message, "You can't do it because you haven't choose any product"))
            return "You can't do it because you haven't choose any product"
        chatHistory.append((message, "The product with name: "+ prompt +" has been successful removed from your list"))
        removeProduct(prompt)
        return "The product with name: "+ str(prompt) +" has been successful removed from your list"
    elif message.startswith("Show all"):
        result = getAllProducts()
        chatHistory.append((message,str(result)))
        return getAllProducts()
    elif message.startswith("That's all"):
        total = getTotalCost()
        chatHistory.append((message, "Your total is $" + total))
        addOrder(OrderiDTO)
        addChatHistory()
        return "Your total is $" + str(total)
    elif message.startswith("What's"):
        response = openai.Completion.create(
            chat = "gpt-3.5-turbo",
            engine="text-davinci-003",
            prompt= message,
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    else:
        chatHistory.append((message, "Sorry, but i don't understand you"))
        return "Sorry, but i don't understand you"
def getTotalCost():
    cur = con.cursor()

    global products
    total = 0
    for product in products:
        select_value = (product,)
        select_script = "SELECT cost FROM menu where named = %s"
        cur.execute(select_script, select_value)
        data = cur.fetchone()
        print(data)
        total += int(data[0])
    return total.__str__()
@app.get("/product/remove/{name}")
def removeProduct(name: str):
    global products
    select_value = (name,)
    select_script = "SELECT * FROM menu where named = %s"
    products.remove(name)

    return True
@app.get("/product/all")
def getAllProducts():
    global products
    nameOfProducts = []
    for product in products:
        nameOfProducts.append(product)
    json_compatible_item_data = jsonable_encoder(products)
    return nameOfProducts
@app.get("/orders")
async def getOrders():
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    # print("before")
    result = cur.fetchall()
    # print("after")

    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
#
@app.get("/menus")
async def getMenu():
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
def getMenuByName(message:str):
    cur = con.cursor()

    global products

    select_value = (message,)
    select_script = "SELECT * FROM menu where named = %s"
    # select_script = "select named,cost,stock FROM menu where named = %s"
    cur.execute(select_script, select_value)
    result = cur.fetchall()

    if result is None or result.__len__() == 0:
        return message + " isn't exist in our menu"
    if result[0][4] == None or int(result[0][4]) == 0:
        return "I’m sorry but we’re out of " + message

    json_compatible_item_data = jsonable_encoder(result)
    print("RESULT" + str(result[0][1]))
    products.append(str(result[0][1]))
    return result
    # return JSONResponse(content=json_compatible_item_data)
@app.post("/orders")
def addOrder(orders: OrderiDTO):
    cur = con.cursor()

    insert_orders_script = "Insert into orders(created_date,updated_date) VALUES (%s,%s)"

    idProducts = []

    for product in products:
        select_value = (product,)
        select_script = "SELECT * FROM menu where named = %s"
        cur.execute(select_script, select_value)

        result = cur.fetchone()
        # temp = Menu
        idProducts.append((result[0],result[3]))

    products.clear()
    insert_menu_orders_script = "Insert into order_products(order_id, menu_id,price) VALUES (%s,%s,%s)"
    insert_orders_value = (date.today().isoformat(),date.today().isoformat())
    cur.execute(insert_orders_script, insert_orders_value)

    select_script = "SELECT MAX(id) FROM orders"
    cur.execute(select_script)
    orders_result = cur.fetchone()

    con.commit()
    for id in idProducts:
        insert_menu_orders_value = (int.__int__(orders_result[0]), id[0],id[1])
        cur.execute(insert_menu_orders_script, insert_menu_orders_value)
        con.commit()

    con.commit()

@app.get("/allproducts/totalsum")
async def getTotalSum():
    cur = con.cursor()

    cur.execute("SELECT SUM(price) FROM order_products  join menu on order_products.menu_id = menu.id")
    result = cur.fetchone()
    return result
#
@app.get("/allproducts/averagesum")
async def getAverageSum():
    cur = con.cursor()

    cur.execute("SELECT AVG(price) FROM order_products join menu on order_products.menu_id = menu.id")
    result = cur.fetchone()
    return result

@app.get("/allproducts/totalevery")
async def getTotalByEveryProduct():
    cur = con.cursor()

    cur.execute("SELECT * from menu")
    result = cur.fetchall()

    items = []

    for r in result:
        select_script = ("SELECT SUM(price) FROM order_products JOIN menu on order_products.menu_id = menu.id where menu.id = %s")
        select_value = (r[0],)
        cur.execute(select_script, select_value)
        sum = cur.fetchone()
        twoitem = [r[1], sum[0], r[3],r[4]]
        items.append(twoitem)

    return items
@app.get("/allproducts/priceEvery")
async def getTotalByEveryProduct():
    cur = con.cursor()

    cur.execute("SELECT cost from menu")
    result = cur.fetchall()
    return result

@app.get("/allproducts/chathistory")
async def getChatHistory():
    cur = con.cursor()

    cur.execute("select user_messages, assistant_messages from order_messages")
    result = cur.fetchall()
    return result

@app.get("/allproducts/chathistory/{id}")
async def getChatHistoryById(id : int):
    cur = con.cursor()
    selectScript = "select user_messages, assistant_messages from order_messages where order_id = %s"
    selectValue = (id,)
    cur.execute(selectScript,selectValue)
    result = cur.fetchall()
    return result

@app.post("/addChatHistory/")
def addChatHistory():
    cur = con.cursor()

    cur.execute("SELECT max(id) FROM orders")
    id = cur.fetchone()
    insert_order_messages_script = "Insert into order_messages(order_id, user_messages, assistant_messages) VALUES (%s, %s,%s)"
    for message in chatHistory:
        insert_orders_value = (id[0], message[0], message[1],)
        cur.execute(insert_order_messages_script, insert_orders_value)
    chatHistory.clear()

@app.post("/addNewProduct/")
def addNewProduct(newProduct):
    cur = con.cursor()
    insertScript = "Insert into menu(named, types, cost,stock) VALUES (%s, %s,%s,%s)"
    insertValue = (newProduct[0],newProduct[1],int(newProduct[2]),0,)
    cur.execute(insertScript,insertValue)
    con.commit()
@app.put("/addNewProduct/")
def updateNewProduct(newProduct):
    cur = con.cursor()
    updateScript = "UPDATE menu SET cost = %s WHERE named = %s and types = %s;"
    updateValue = (int(newProduct[2]),newProduct[0],newProduct[1],)
    cur.execute(updateScript,updateValue)
    con.commit()
@app.put("/addNewProduct/")
def updateNewProductByStock(newProduct):
    cur = con.cursor()
    updateScript = "UPDATE menu SET stock = %s WHERE named = %s and types = %s;"
    updateValue = (int(newProduct[2]),newProduct[0],newProduct[1],)
    cur.execute(updateScript,updateValue)
    con.commit()

@app.get("/check/{message}")
def checkIfCurrentProductExistByName(message):
    cur = con.cursor()
    selectScript = "select named from menu where named = %s"
    selectValue = (message,)
    cur.execute(selectScript,selectValue)
    result = cur.fetchall()
    if result.__len__() == 0:
        print("FALSE")
        return False
    else:
        print("TRUE")
        return True
def checkIfCurrentProductExistByType(message):
    cur = con.cursor()
    selectScript = "select types from menu where types = %s"
    selectValue = (message,)
    cur.execute(selectScript,selectValue)
    result = cur.fetchall()
    if result.__len__() == 0:
        print("FALSE")
        return False
    else:
        print("TRUE")
        return True

def createRandomProduct():
    cur = con.cursor()

    selectScript = "select named,types, cost from menu where stock > 0"
    cur.execute(selectScript)
    result = cur.fetchall()
    if result is None or len(result) == 0:
        return "not found"
    result = random.choice(result)
    print("RANDOM NAME: " + str(result))

    return result

def reduceStockByProductNameAndType(someProduct):
    cur = con.cursor()
    selectScript = "SELECT stock from menu WHERE named = %s and types = %s;"
    updateValue = (someProduct[0],someProduct[1],)
    cur.execute(selectScript,updateValue)
    stock = cur.fetchone()

    selectScript = "UPDATE menu SET stock = %s WHERE named = %s and types = %s;"

    print(someProduct[0])
    print(someProduct[1])
    updateValue = (stock[0]-1,someProduct[0],someProduct[1])
    cur.execute(selectScript,updateValue)