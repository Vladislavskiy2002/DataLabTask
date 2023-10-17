import logging
import openai
import psycopg2
from fastapi import FastAPI
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE

from services.menu_service import *
from services.order_service import *
from models.models import CoffeeShopStatus

openai.organization = "org-2bXqWp423OEFqEdoPm8vbjAl"
openai.api_key = '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'

app = FastAPI()

# con = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", password="1234")

# !!!!!При Push на гітхаб забрав актуальний конекшн, щоб боти не взламували мою БД!!!!

# con = psycopg2.connect(dbname="postgres", user="postgres", host="db", password="1234")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

coffeeShopStatus = CoffeeShopStatus()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/admin/setToDefault")
async def setStartProgramMessegeAsAdminByDefault():
    coffeeShopStatus.startAdmin = True
    return True


@app.get("/setToDefault")
async def setStartProgramMessegeAsUserByDefault():
    coffeeShopStatus.reset_variables()

@app.get("/startprogram")
async def getStartProgramMessege():
    # global start
    if coffeeShopStatus.start:
        coffeeShopStatus.start = False
        return "Welcome at the coffee shoP What would you like?"


@app.get("/admin/handler/{message}")
async def handler(message: str):
    if coffeeShopStatus.startAdmin:
        if message.lower() in ["add", "update", "stock"]:
            coffeeShopStatus.status = message.lower()
            coffeeShopStatus.startAdmin = False
            coffeeShopStatus.lastAdminAssistantResponce = "Enter the type of product"
            return coffeeShopStatus.lastAdminAssistantResponce

    elif coffeeShopStatus.lastAdminAssistantResponce == "Enter the type of product":
        coffeeShopStatus.newProductType = message
        coffeeShopStatus.startAdmin = False
        coffeeShopStatus.lastAdminAssistantResponce = "Enter the name of product"
        return coffeeShopStatus.lastAdminAssistantResponce

    elif coffeeShopStatus.lastAdminAssistantResponce == "Enter the name of product":
        if await checkIfCurrentProductExistByName(message):
            if coffeeShopStatus.status == "add":
                return "Product with current name already exists. Please enter a different product name:"
            elif coffeeShopStatus.status == "stock" and await checkIfCurrentProductExistByType(
                    coffeeShopStatus.newProductType):
                coffeeShopStatus.newProductName = message
                coffeeShopStatus.lastAdminAssistantResponce = "Set the stock:"
                return coffeeShopStatus.lastAdminAssistantResponce

        elif coffeeShopStatus.status == "stock":
            coffeeShopStatus.startAdmin = True
            return f"The product with name: {message} and type: {coffeeShopStatus.newProductType} doesn't exist. Choose update, add, or stock."

        coffeeShopStatus.newProductName = message
        coffeeShopStatus.lastAdminAssistantResponce = "Enter the costs:"
        return coffeeShopStatus.lastAdminAssistantResponce

    elif coffeeShopStatus.lastAdminAssistantResponce == "Set the stock:":
        if not message.isdecimal():
            return "The stock must be a number. Please try again."
        elif len(message) > 100:
            return "The stock must be less than 100."
        newProductStock = message
        newProduct = (coffeeShopStatus.newProductName, coffeeShopStatus.newProductType, newProductStock,)
        await updateNewProductByStock(newProduct)
        coffeeShopStatus.startAdmin = True
        coffeeShopStatus.lastAdminAssistantResponce = ""
        return "The stock has been successfully set."

    elif coffeeShopStatus.lastAdminAssistantResponce == "Enter the costs:":
        if not message.isdecimal():
            return "The cost must be a number. Please try again."
        coffeeShopStatus.newProductCost = message
        newProduct = (
        coffeeShopStatus.newProductName, coffeeShopStatus.newProductType, coffeeShopStatus.newProductCost,)
        coffeeShopStatus.lastAdminAssistantResponce = ""
        if coffeeShopStatus.status == "add":
            await addNewProduct(newProduct)
            coffeeShopStatus.startAdmin = True
            return "The product has been successfully added. Choose update, add, or stock."
        elif coffeeShopStatus.status == "update":
            coffeeShopStatus.startAdmin = True
            if await checkIfCurrentProductExistByName(
                    coffeeShopStatus.newProductName) and await checkIfCurrentProductExistByType(
                    coffeeShopStatus.newProductType):
                await updateNewProduct(newProduct)
                return "The product has been successfully updated. Choose update, add, or stock."
            else:
                return f"The product with name: {coffeeShopStatus.newProductName} and type: {coffeeShopStatus.newProductType} doesn't exist. Choose update, add, or stock."

    return "Not a valid input. Choose update, add, or stock."

@app.get("/handler/{message}")
async def handler(message: str):
    if coffeeShopStatus.start:
        coffeeShopStatus.start = False
        coffeeShopStatus.chatHistory.append(("Welcome at the coffee shop \n What would you like?"))
        return "Welcome at the coffee shop \n What would you like?"

    if coffeeShopStatus.flag:
        if message.lower() == "yes":
            product_id = await getMenuByName(coffeeShopStatus.newRandomProduct[0])
            await addMenuStatistic((product_id[0][0], True, product_id[0][3]))
            coffeeShopStatus.products.append(coffeeShopStatus.newRandomProduct[0])
            await reduceStockByProductNameAndType(
                [coffeeShopStatus.newRandomProduct[0], coffeeShopStatus.newRandomProduct[1]])
            coffeeShopStatus.chatHistory.append(
                (message, f"The {coffeeShopStatus.newRandomProduct[0]} has been successfully added to your order"))
            return f"The {coffeeShopStatus.newRandomProduct[0]} has been successfully added to your order"

        elif message.lower() == "no":
            product_id = await getMenuByName(coffeeShopStatus.newRandomProduct[0])
            await addMenuStatistic((product_id[0][0], False, product_id[0][3]))
            coffeeShopStatus.flag = False
            coffeeShopStatus.chatHistory.append((message, "Would you like something else?"))
            return "Would you like something else?"

        else:
            coffeeShopStatus.chatHistory.append((message, "I don't understand you. Try again"))
            return "I don't understand you. Try again"

    elif message.lower().startswith("i'd like a "):
        prompt = message.lower().replace("i'd like a ", '', 1)
        data = await getMenuByName(prompt)

        if data == f"{prompt} isn't exist in our menu":
            coffeeShopStatus.chatHistory.append((message, f"{prompt} isn't exist in our menu"))
            return f"{prompt} isn't exist in our menu"

        if data == f"I’m sorry but we’re out of {prompt}":
            coffeeShopStatus.chatHistory.append((message, f"I’m sorry but we’re out of {prompt}"))
            return f"I’m sorry but we’re out of {prompt}"

        coffeeShopStatus.products.append(prompt)
        await reduceStockByProductNameAndType([data[0][1], data[0][2]])
        coffeeShopStatus.flag = True
        coffeeShopStatus.newRandomProduct = await createRandomProduct()

        if coffeeShopStatus.newRandomProduct == "not found":
            coffeeShopStatus.flag = False
            coffeeShopStatus.chatHistory.append("Would you like something else?")
            return "Would you like something else?"

        coffeeShopStatus.chatHistory.append((message,
                                             f"Would you like to add a {coffeeShopStatus.newRandomProduct[0]} for ${coffeeShopStatus.newRandomProduct[2]}?"))
        return f"Would you like to add a {coffeeShopStatus.newRandomProduct[0]} for ${coffeeShopStatus.newRandomProduct[2]}?"

    elif message.startswith("I don't want a "):
        prompt = message.replace("I don't want a ", '', 1)

        if not coffeeShopStatus.products:
            coffeeShopStatus.chatHistory.append((message, "You can't do it because you haven't chosen any product"))
            return "You can't do it because you haven't chosen any product"

        coffeeShopStatus.chatHistory.append(
            (message, f"The product with name: {prompt} has been successfully removed from your list"))

        if prompt in coffeeShopStatus.products:
            await removeProduct(prompt)
        else:
            return f"You can't remove it because the product {prompt} isn't in your list"

        return f"The product with name: {prompt} has been successfully removed from your list"

    elif message.lower().startswith("show all"):
        result = await getAllProducts()
        coffeeShopStatus.chatHistory.append((message, str(result)))
        return str(result)

    elif message.lower().startswith("that's all"):
        total = await getTotalCost()
        coffeeShopStatus.chatHistory.append((message, f"Your total is ${total}"))
        await addOrder()
        await addChatHistory()
        return f"Your total is ${total}"

    elif message.startswith("What's"):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    else:
        coffeeShopStatus.chatHistory.append((message, "Sorry, but I don't understand you"))
        return "Sorry, but I don't understand you"


async def getTotalCost():
# global products
    return await get_total_cost(con, coffeeShopStatus.products)


@app.get("/product/remove/{name}")
async def removeProduct(name: str):
    # global products
    coffeeShopStatus.products.remove(name)
    return True


@app.get("/product/all")
async def getAllProducts():
    nameOfProducts = []
    for product in coffeeShopStatus.products:
        nameOfProducts.append(product)
    json_compatible_item_data = jsonable_encoder(coffeeShopStatus.products)
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
    coffeeShopStatus.products = await add_order(con, coffeeShopStatus.products)


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
    coffeeShopStatus.chatHistory = await add_chat_history(con, coffeeShopStatus.chatHistory)


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
    return await check_if_current_product_exist_by_name(con, message)


@app.get("/checke/{message}")
async def checkIfCurrentProductExistByType(message):
    return await check_if_current_product_exist_by_type(con, message)


async def createRandomProduct():
    return await create_random_product(con)


async def reduceStockByProductNameAndType(someProduct):
    await reduce_stock_by_product_name_and_type(con, someProduct)
