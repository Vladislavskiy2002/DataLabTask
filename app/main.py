import logging

import openai
import psycopg2
from fastapi import FastAPI
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE

from app.services.menu_service import *
from app.services.order_service import *

openai.organization = "org-2bXqWp423OEFqEdoPm8vbjAl"
openai.api_key = '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'

app = FastAPI()

# con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")
con = psycopg2.connect(dbname="postgres", user="postgres", host="34.28.70.151", password="1234")
# con = psycopg2.connect(dbname="postgres", user="postgres", host="db", password="1234")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


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
    lastAdminAssistantResponce = ""
    newProductType = ""
    newProductName = ""
    newProductCost = ""
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

    if startAdmin and message.lower() == "add" or message.lower() == "update" or message.lower() == "stock":
        status = message.lower()
        startAdmin = False
        lastAdminAssistantResponce = "Enter the type of product"
        return lastAdminAssistantResponce
    elif lastAdminAssistantResponce is "Enter the type of product":
        newProductType = message
        startAdmin = False
        lastAdminAssistantResponce = "Enter the name of product"
        return lastAdminAssistantResponce
    elif lastAdminAssistantResponce is "Enter the name of product":
        if await checkIfCurrentProductExistByName(message) and status == "add":
            logging.info(await checkIfCurrentProductExistByName(message))
            return "Product with current name has already exist. Try again to write the product's name:"
        if await checkIfCurrentProductExistByName(message) and await checkIfCurrentProductExistByType(
                newProductType) and status == "stock":
            logging.info(await checkIfCurrentProductExistByName(message))
            newProductName = message
            lastAdminAssistantResponce = "Set the stock:"
            return "Set the stock:"
        elif not await checkIfCurrentProductExistByName(message) and not await checkIfCurrentProductExistByType(
                newProductType) and status == "stock":
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
        await updateNewProductByStock(newProduct)
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
            await addNewProduct(newProduct)
            startAdmin = True
            return "The product has been successfully added. Choose update, add or stock"
        elif status == "update":
            startAdmin = True
            if await checkIfCurrentProductExistByName(
                    newProductName) == True and await checkIfCurrentProductExistByType(newProductType) == True:
                await updateNewProduct(newProduct)
                return "The product has been successfully updated. Choose update, add or stock"
            else:
                return "The product with name: " + newProductName + " and type: " + newProductType + " isn't exist. Choose update, add or stock"

    else:
        return "Something goes wrong ;("


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
        if message.lower() == "yes":
            flag = False
            product_id = await getMenuByName(newRandomProduct[0])
            await addMenuStatistic((product_id[0][0], True, product_id[0][3]))
            products.append(newRandomProduct[0])
            await reduceStockByProductNameAndType([newRandomProduct[0], newRandomProduct[1]])
            chatHistory.append(
                (message, "The " + str(newRandomProduct[0]) + " has been successfully added to your order"))
            return "The " + str(newRandomProduct[0]) + " has been successfully added to your order"
        elif message.lower() == "no":
            product_id = await getMenuByName(newRandomProduct[0])
            await addMenuStatistic((product_id[0][0], False, product_id[0][3]))
            flag = False
            chatHistory.append((message, "Would you like something else?"))
            return "Would you like something else?"
        else:
            chatHistory.append((message, "I don't understand you. Try again"))
            return "I don't understand you. Try again"

    if message.lower().startswith("i'd like a "):
        prompt = message.lower().replace("i'd like a ", '', 1)
        data = await getMenuByName(prompt)
        if data == prompt.__str__() + " isn't exist in our menu":
            chatHistory.append((message, prompt.__str__() + " isn't exist in our menu"))
            return prompt.__str__() + " isn't exist in our menu"
        if data == "I’m sorry but we’re out of " + str(prompt):
            chatHistory.append((message, "I’m sorry but we’re out of " + str(prompt)))
            return "I’m sorry but we’re out of " + str(prompt)
        products.append(prompt)
        await reduceStockByProductNameAndType([data[0][1], data[0][2]])
        flag = True
        newRandomProduct = await createRandomProduct()
        if newRandomProduct == "not found":
            flag = False
            chatHistory.append("Would you like something else?")
            return "Would you like something else?"
        chatHistory.append((message, "Would you like to add a " + str(newRandomProduct[0]) + " for $" + str(
            newRandomProduct[2]) + "?"))
        return "Would you like to add a " + str(newRandomProduct[0]) + " for $" + str(newRandomProduct[2]) + "?"
    elif message.startswith("I don't want a "):
        prompt = message.replace("I don't want a ", '', 1)
        if (products.__len__() == 0):
            chatHistory.append((message, "You can't do it because you haven't choose any product"))
            return "You can't do it because you haven't choose any product"
        chatHistory.append(
            (message, "The product with name: " + prompt + " has been successful removed from your list"))
        if products.__contains__(prompt):
            await removeProduct(prompt)
        else:
            return "You can't remove it because current product isn't exist in your list"
        return "The product with name: " + str(prompt) + " has been successful removed from your list"
    elif message.lower().startswith("show all"):
        result = await getAllProducts()
        chatHistory.append((message, str(result)))
        return await getAllProducts()
    elif message.lower().startswith("that's all"):
        total = await getTotalCost()
        chatHistory.append((message, "Your total is $" + total))
        await addOrder()
        await addChatHistory()
        return "Your total is $" + str(total)
    elif message.startswith("What's"):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    else:
        chatHistory.append((message, "Sorry, but i don't understand you"))
        return "Sorry, but i don't understand you"


async def getTotalCost():
    global products
    return await get_total_cost(con, products)


@app.get("/product/remove/{name}")
async def removeProduct(name: str):
    global products
    products.remove(name)
    return True


@app.get("/product/all")
async def getAllProducts():
    global products
    nameOfProducts = []
    for product in products:
        nameOfProducts.append(product)
    json_compatible_item_data = jsonable_encoder(products)
    return nameOfProducts


@app.get("/orders")
async def getOrders():
    return await get_orders(con)


@app.get("/statistic")
async def getStatistic():
    return await get_statistic(con)


@app.get("/orders/{id}")
async def getOrdersById(id: str):
    return await get_orders_by_id(con, id)


@app.get("/orders/allproduct/{id}")
async def getAllOrdersProductsById(id):
    return await get_all_orders_products_by_id(con, id)


@app.get("/menus")
async def getMenu():
    return await get_menu(con)


@app.get("/menus/{message}")
async def getMenuByName(message: str):
    return await get_menu_by_name(con, message)


@app.post("/orders")
async def addOrder():
    global products
    products = await add_order(con, products)


@app.get("/allproducts/totalsum")
async def getTotalSum():
    return await get_total_sum(con)


@app.get("/allproducts/averagesum")
async def getAverageSum():
    return await get_average_sum(con)


@app.get("/allproducts/totalevery")
async def getTotalByEveryProduct():
    return await get_total_by_every_product(con)


@app.get("/allproducts/priceEvery")
async def getTotalByEveryProduct():
    return await get_total_by_every_product(con)


@app.get("/allproducts/chathistory")
async def getChatHistory():
    return await get_ChatHistory(con)


@app.get("/allproducts/chathistory/{id}")
async def getChatHistoryById(id: int):
    return await get_chatHistory_by_id(con, id)


@app.post("/addChatHistory/")
async def addChatHistory():
    global chatHistory
    chatHistory = await add_chat_history(con, chatHistory)


@app.post("/addNewProduct/")
async def addNewProduct(newProduct):
    await add_new_product(con, newProduct)


@app.post("/addMenuStatistic/")
async def addMenuStatistic(statistic):
    await add_menu_statistic(con, statistic)


@app.put("/addNewProduct/")
async def updateNewProduct(newProduct):
    await update_new_product(con, newProduct)


@app.put("/addNewProduct/")
async def updateNewProductByStock(newProduct):
    await update_new_product_by_stock(con, newProduct)


@app.get("/check/{message}")
async def checkIfCurrentProductExistByName(message):
    await check_if_current_product_exist_by_name(con, message)


@app.get("/checke/{message}")
async def checkIfCurrentProductExistByType(message):
    return await check_if_current_product_exist_by_type(con, message)


async def createRandomProduct():
    return await create_random_product(con)


async def reduceStockByProductNameAndType(someProduct):
    await reduce_stock_by_product_name_and_type(con, someProduct)
