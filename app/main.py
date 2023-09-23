import asyncio
import random
from datetime import date
from typing import List
from fastapi.encoders import jsonable_encoder
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
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

class OrderDTO(BaseModel):
    id: int
    address: str
    order_products: List[Menu]
class OrderiDTO(BaseModel):
    order_products: List[Menu]
    total:str

sql_schript1 = """
CREATE TABLE IF NOT EXISTS public.menu
(
    id integer NOT NULL DEFAULT nextval('menu_id_seq'::regclass),
    named character varying(255) COLLATE pg_catalog."default",
    types character varying(255) COLLATE pg_catalog."default",
    cost integer NOT NULL,
    CONSTRAINT menu_pkey PRIMARY KEY (id),
    CONSTRAINT menu_id_unique UNIQUE (id)
);
"""

sql_schript2 = """
CREATE TABLE IF NOT EXISTS public.orders
(
    id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
    created_date date NOT NULL,
    updated_date date NOT NULL,
    address character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT orders_pkey PRIMARY KEY (id)
);
"""

sql_schript3 = """
CREATE TABLE IF NOT EXISTS order_products (
    id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
    order_id integer,
    menu_id integer,
    CONSTRAINT order_products_pkey PRIMARY KEY (id),
    CONSTRAINT order_products_menu_id_fkey FOREIGN KEY (menu_id)
        REFERENCES public.menu (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT order_products_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
"""

sql_schript4 = """
CREATE TABLE IF NOT EXISTS public.order_messages
(
    id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
    order_id integer,
    assistant_messages character varying(1000) COLLATE pg_catalog."default",
    user_messages character varying(1000) COLLATE pg_catalog."default",
    CONSTRAINT order_messages_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)"""

@app.on_event("startup")
async def create_database():
    await asyncio.sleep(10)

    global con

    con = psycopg2.connect(dbname="postgres", user="postgres", host="db", password="1234")
    # con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

    cur = con.cursor()

    try:
        cur.execute(sql.SQL("CREATE DATABASE datalab_db;"))
        cur.execute(sql.SQL(sql_schript1))
        cur.execute(sql.SQL(sql_schript2))
        cur.execute(sql.SQL(sql_schript3))
        cur.execute(sql.SQL(sql_schript4))
        # cur.execute(sql.SQL(sql_schript5))
        # cur.execute(sql.SQL(sql_schript6))
        # cur.execute(sql.SQL(sql_schript7))
    #
    except:
        cur.execute(sql.SQL("DROP DATABASE datalab_db;"))
        cur.execute(sql.SQL("CREATE DATABASE datalab_db;"))
        cur.execute(sql.SQL(sql_schript1))
        cur.execute(sql.SQL(sql_schript2))
        cur.execute(sql.SQL(sql_schript3))
        cur.execute(sql.SQL(sql_schript4))
        # cur.execute(sql.SQL(sql_schript5))
        # cur.execute(sql.SQL(sql_schript6))
        # cur.execute(sql.SQL(sql_schript7))

    db_con = psycopg2.connect(dbname="test", user="postgres", host="db", password="1234")
    # db_con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")

    cur = db_con.cursor()
    db_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur.execute(sql.SQL("CREATE TABLE IF NOT EXISTS test_table (id int);"))

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

#
@app.get("/admin/setToDefault")
def startProgramMessege():
    global startAdmin
    startAdmin = True
    print(startAdmin)
    return True
@app.get("/setToDefault")
def startProgramMessege():
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
def startProgramMessege():
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

    if startAdmin and message == "add" or message == "update":
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
        if checkIfCurrentProductExistByName(message) and status != "update":
            return "Product with current name has already exist. Try again to write the product's name:"
        newProductName = message
        lastAdminAssistantResponce = "Enter the costs:"
        return lastAdminAssistantResponce
    elif lastAdminAssistantResponce == "Enter the costs:":
        newProductCost = message
        if not message.isdecimal():
            return "the cost's must be num. Try again"
        newProduct = (newProductName, newProductType, newProductCost,)
        lastAdminAssistantResponce = ""
        if status == "add":
            addNewProduct(newProduct)
            startAdmin = True
            return "The product has been successfully added. Choose update or add"
        elif status == "update":
            startAdmin = True
            if checkIfCurrentProductExistByName(newProductName) == True and checkIfCurrentProductExistByType(newProductType) == True:
                updateNewProduct(newProduct)
                return "The product has been successfully updated. Choose update or add"
            else:
                return "The product with name: " + newProductName + " and type: " + newProductType + " isn't exist. Choose update or add"

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
            products.append(str(newRandomProduct))
            chatHistory.append((message, "The " + str(newRandomProduct) + " has been successfully added to your order"))
            return "The " + str(newRandomProduct) + " has been successfully added to your order"
        elif message == "no":
            flag = False
            chatHistory.append((message,"Would you like something else?"))
            return "Would you like something else?"
        else:
            chatHistory.append((message, "I don't understand you. Try again"))
            return "I don't understand you. Try again"

    if message.startswith("I'd like a "):
        prompt = message.replace("I'd like a ", '', 1)
        print("start")
        data = menusByName(prompt)
        if data == prompt.__str__() + " isn't exist in our menu":
            chatHistory.append((message,prompt.__str__() + " isn't exist in our menu"))
            return prompt.__str__() + " isn't exist in our menu"
        flag = True
        newRandomProduct = createRandomProduct()
        chatHistory.append((message,"Would you like to add a " + str(newRandomProduct) + " to your " + prompt.__str__() + "?"))
        return "Would you like to add a " + str(newRandomProduct) + " to your " + prompt.__str__() + "?"
    elif message.startswith("I don't want a "):
        prompt = message.replace("I don't want a ", '', 1)
        if(products.__len__() ==0):
            chatHistory.append((message, "You can't do it because you haven't choose any product"))
            return "You can't do it because you haven't choose any product"
        chatHistory.append((message, "The product with name: "+ prompt +" has been successful removed from your list"))
        print("adasdasd")
        print(prompt)
        removeProduct(prompt)
        print("promptgfdgfdg")
        return "The product with name: "+ str(prompt) +" has been successful removed from your list"
    elif message.startswith("Show all"):
        result = allproducts()
        chatHistory.append((message,str(result)))
        return allproducts()
    elif message.startswith("That's all"):
        total = totalcost()
        chatHistory.append((message, "Total cost $" + total))
        add_orderdto(OrderiDTO)
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
@app.get("/")
async def root():
    return {"message": "Hello World"}
def totalcost():
    cur = con.cursor()

    global products
    total = 0
    for product in products:
        select_value = (product,)
        print(product)
        select_script = "SELECT cost FROM menu where named = %s"
        cur.execute(select_script, select_value)
        data = cur.fetchone()
        total += data[0]
    print("Totali" + total.__str__())
    return total.__str__()
@app.get("/product/remove/{name}")
def removeProduct(name: str):
    global products
    select_value = (name,)
    select_script = "SELECT * FROM menu where named = %s"
    products.remove(name)
    print(products)
    # return JSONResponse(status_code=status.HTTP_200_OK)
    return True
@app.get("/product/all")
def allproducts():
    global products
    print(products)
    json_compatible_item_data = jsonable_encoder(products)
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
#
@app.get("/menus")
def menus():
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
def menusByName(message:str):
    cur = con.cursor()

    global products
    # print("fdfdff")
    # return JSONResponse(status_code=status.HTTP_200_OK)    # cur = con.cursor()
    select_value = (message,)
    select_script = "SELECT * FROM menu where named = %s"
    cur.execute(select_script, select_value)
    result = cur.fetchall()
    if result is None or result.__len__() == 0:
        return message + " isn't exist in our menu"
    json_compatible_item_data = jsonable_encoder(result)
    products.append(message)
    print(products)
    return JSONResponse(content=json_compatible_item_data)
@app.post("/orders")
def add_orderdto(orders: OrderiDTO):
    cur = con.cursor()

    # insert_menu_script = "Insert into menu(id,named,types,cost) VALUES (%s,%s,%s,%s)"
    insert_orders_script = "Insert into orders(created_date,updated_date) VALUES (%s,%s)"

    idProducts = []

    for product in products:
        print(product)
        select_value = (product,)
        select_script = "SELECT * FROM menu where named = %s"
        cur.execute(select_script, select_value)

        result = cur.fetchone()
        # temp = Menu
        idProducts.append(result[0])

    products.clear()
    insert_menu_orders_script = "Insert into order_products(order_id, menu_id) VALUES (%s,%s)"
    insert_orders_value = (date.today().isoformat(),date.today().isoformat())
    cur.execute(insert_orders_script, insert_orders_value)

    select_script = "SELECT MAX(id) FROM orders"
    cur.execute(select_script)
    orders_result = cur.fetchone()
    print(orders_result[0])

    print(idProducts)
    con.commit()
    for id in idProducts:
        insert_menu_orders_value = (int.__int__(orders_result[0]), id)
        cur.execute(insert_menu_orders_script, insert_menu_orders_value)
        con.commit()

    con.commit()


# @app.post("/orders/{address}")
# def add_order(address: str):
#     OrderDTO.address = address
#     add_orderdto(OrderDTO)

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

@app.get("/allproducts/totalsum")
async def totalsum():
    cur = con.cursor()

    cur.execute("SELECT SUM(cost) FROM menu join order_products on order_products.menu_id = menu.id")
    result = cur.fetchone()
    print(result)
    return result

@app.get("/allproducts/averagesum")
async def averagesum():
    cur = con.cursor()

    cur.execute("SELECT AVG(cost) FROM menu join order_products on order_products.menu_id = menu.id")
    result = cur.fetchone()
    print(result)
    return result

@app.get("/allproducts/totalevery")
async def totalbyeveryproduct():
    cur = con.cursor()

    cur.execute("SELECT * from menu")
    result = cur.fetchall()

    items = []

    for r in result:
        select_script = ("SELECT SUM(cost) FROM menu JOIN order_products on order_products.menu_id = menu.id where menu.id = %s")
        select_value = (r[0],)
        print("ID:")
        print(r[0])
        cur.execute(select_script, select_value)
        sum = cur.fetchone()
        print("sum:")
        print(sum)
        twoitem = [r[1], sum]
        items.append(twoitem)

    print(items)
    return items


@app.get("/allproducts/chathistory")
async def getChatHistory():
    cur = con.cursor()

    cur.execute("select user_messages, assistant_messages from order_messages")
    result = cur.fetchall()
    print(result)
    return result

@app.get("/allproducts/chathistory/{id}")
async def getChatHistory(id : int):
    cur = con.cursor()
    selectScript = "select user_messages, assistant_messages from order_messages where order_id = %s"
    selectValue = (id,)
    print("ID" + id.__str__())
    cur.execute(selectScript,selectValue)
    result = cur.fetchall()
    print(result)
    return result

@app.post("/addChatHistory/")
def addChatHistory():
    cur = con.cursor()

    cur.execute("SELECT max(id) FROM orders")
    id = cur.fetchone()
    insert_order_messages_script = "Insert into order_messages(order_id, user_messages, assistant_messages) VALUES (%s, %s,%s)"
    for message in chatHistory:
        print("MESSEGE")
        print(message[0])
        insert_orders_value = (id[0], message[0], message[1],)
        cur.execute(insert_order_messages_script, insert_orders_value)

@app.post("/addNewProduct/")
def addNewProduct(newProduct):
    cur = con.cursor()

    insertScript = "Insert into menu(named, types, cost) VALUES (%s, %s,%s)"
    print("newProduct[2]")
    print(newProduct[2])
    print(newProduct[1])
    print(newProduct[1])
    insertValue = (newProduct[0],newProduct[1],int(newProduct[2]),)
    cur.execute(insertScript,insertValue)
    con.commit()
@app.put("/addNewProduct/")
def updateNewProduct(newProduct):
    cur = con.cursor()

    updateScript = "UPDATE menu SET cost = %s WHERE named = %s and types = %s;"
    print(newProduct[0])
    print(newProduct[1])
    print(newProduct[2])
    updateValue = (int(newProduct[2]),newProduct[0],newProduct[1],)
    cur.execute(updateScript,updateValue)
    con.commit()

def checkIfCurrentProductExistByName(message):
    cur = con.cursor()

    selectScript = "select named from menu where named = %s"
    selectValue = (message,)
    cur.execute(selectScript,selectValue)
    result = cur.fetchall()
    print(result)
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
    print(result)
    if result.__len__() == 0:
        print("FALSE")
        return False
    else:
        print("TRUE")
        return True

def createRandomProduct():
    cur = con.cursor()

    selectScript = "select named from menu"
    cur.execute(selectScript)
    result = cur.fetchall()
    result = random.choice(result)
    print("RANDOM NAME: " + str(result))
    return result[0]
#