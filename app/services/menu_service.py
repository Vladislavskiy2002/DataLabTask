import random

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


async def check_if_current_product_exist_by_type(con, message):
    cur = con.cursor()
    selectScript = "select types from menu where types = %s"
    selectValue = (message,)
    cur.execute(selectScript, selectValue)
    result = cur.fetchall()
    if result.__len__() == 0:
        return False
    else:
        return True


async def create_random_product(con):
    cur = con.cursor()
    selectScript = "select named,types, cost from menu where stock > 0"
    cur.execute(selectScript)
    result = cur.fetchall()
    if result is None or len(result) == 0:
        return "not found"
    result = random.choice(result)
    return result


async def reduce_stock_by_product_name_and_type(con, someProduct):
    cur = con.cursor()
    selectScript = "SELECT stock from menu WHERE named = %s and types = %s;"
    updateValue = (someProduct[0], someProduct[1],)
    cur.execute(selectScript, updateValue)
    stock = cur.fetchone()

    selectScript = "UPDATE menu SET stock = %s WHERE named = %s and types = %s;"

    updateValue = (stock[0] - 1, someProduct[0], someProduct[1])
    cur.execute(selectScript, updateValue)


async def check_if_current_product_exist_by_name(con, message):
    cur = con.cursor()
    selectScript = "select named from menu where named = %s"
    selectValue = (message,)
    cur.execute(selectScript, selectValue)
    result = cur.fetchall()
    if result.__len__() == 0:
        return False
    else:
        return True


async def update_new_product_by_stock(con, newProduct):
    cur = con.cursor()
    updateScript = "UPDATE menu SET stock = %s WHERE named = %s and types = %s;"
    updateValue = (int(newProduct[2]), newProduct[0], newProduct[1],)
    cur.execute(updateScript, updateValue)
    con.commit()


async def update_new_product(con, newProduct):
    cur = con.cursor()
    updateScript = "UPDATE menu SET cost = %s WHERE named = %s and types = %s;"
    updateValue = (int(newProduct[2]), newProduct[0], newProduct[1],)
    cur.execute(updateScript, updateValue)
    con.commit()


async def add_menu_statistic(con, statistic):
    cur = con.cursor()
    insertScript = "Insert into menu_statistic(menu_id,accepted,price) VALUES (%s, %s,%s)"
    insertValue = (statistic[0], statistic[1], statistic[2])
    cur.execute(insertScript, insertValue)
    con.commit()


async def add_new_product(con, newProduct):
    cur = con.cursor()
    insertScript = "Insert into menu(named, types, cost,stock) VALUES (%s, %s,%s,%s)"
    insertValue = (newProduct[0], newProduct[1], int(newProduct[2]), 0,)
    cur.execute(insertScript, insertValue)
    con.commit()


async def add_chat_history(con, chatHistory):
    cur = con.cursor()
    cur.execute("SELECT max(id) FROM orders")
    id = cur.fetchone()
    insert_order_messages_script = "Insert into order_messages(order_id, user_messages, assistant_messages) VALUES (%s, %s,%s)"
    for message in chatHistory:
        insert_orders_value = (id[0], message[0], message[1],)
        cur.execute(insert_order_messages_script, insert_orders_value)
    chatHistory.clear()
    return chatHistory


async def get_chatHistory_by_id(con, id: int):
    cur = con.cursor()
    selectScript = "select user_messages, assistant_messages from order_messages where order_id = %s"
    selectValue = (id,)
    cur.execute(selectScript, selectValue)
    result = cur.fetchall()
    return result


async def get_ChatHistory(con):
    cur = con.cursor()
    cur.execute("select user_messages, assistant_messages from order_messages")
    result = cur.fetchall()
    return result


async def get_total_by_every_product(con):
    cur = con.cursor()
    cur.execute("SELECT cost from menu")
    result = cur.fetchall()
    return result


async def get_total_by_every_product(con):
    cur = con.cursor()
    cur.execute("SELECT * from menu")
    result = cur.fetchall()
    items = []
    for r in result:
        select_script = (
            "SELECT SUM(price) FROM order_products JOIN menu on order_products.menu_id = menu.id where menu.id = %s")
        select_value = (r[0],)
        cur.execute(select_script, select_value)
        sum = cur.fetchone()
        twoitem = [r[1], sum[0], r[3], r[4]]
        items.append(twoitem)
    return items


async def get_average_sum(con):
    cur = con.cursor()
    cur.execute(
        "SELECT SUM(order_products.price) / COUNT(DISTINCT orders.id) AS avg_order_number FROM orders JOIN order_products ON orders.id = order_products.order_id;")
    result = cur.fetchone()
    result = [str(round(result[0], 2))]
    return result


async def get_total_sum(con):
    cur = con.cursor()
    cur.execute("SELECT SUM(price) FROM order_products  join menu on order_products.menu_id = menu.id")
    result = cur.fetchone()
    return result


async def get_menu_by_name(con, message: str):
    cur = con.cursor()

    global products

    select_value = (message,)
    select_script = "SELECT * FROM menu where named = %s"
    cur.execute(select_script, select_value)
    result = cur.fetchall()

    if result is None or result.__len__() == 0:
        return message + " isn't exist in our menu"
    if result[0][4] == None or int(result[0][4]) == 0:
        return "I’m sorry but we’re out of " + message
    return result


async def get_menu(con):
    global products
    cur = con.cursor()
    cur.execute("SELECT * FROM menu")
    result = cur.fetchall()
    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)


async def get_statistic(con):
    cur = con.cursor()
    cur.execute(
        """
        SELECT 
        COUNT(menu_statistic.id) AS total_asked,
        SUM(CASE WHEN menu_statistic.accepted = true THEN 1 ELSE 0 END) AS accepted,
        SUM(CASE WHEN menu_statistic.accepted = false THEN 1 ELSE 0 END) AS rejected,
         SUM(CASE WHEN menu_statistic.accepted = true THEN menu_statistic.price ELSE 0 END) AS total_upsell_revenue 
        FROM menu_statistic"""
    )
    result = cur.fetchall()

    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
