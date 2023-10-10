from datetime import date

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


async def add_order(con, products):
    cur = con.cursor()

    insert_orders_script = "Insert into orders(created_date,updated_date) VALUES (%s,%s)"

    idProducts = []

    for product in products:
        select_value = (product,)
        select_script = "SELECT * FROM menu where named = %s"
        cur.execute(select_script, select_value)

        result = cur.fetchone()

        idProducts.append((result[0], result[3]))

    products.clear()
    insert_menu_orders_script = "Insert into order_products(order_id, menu_id,price) VALUES (%s,%s,%s)"
    insert_orders_value = (date.today().isoformat(), date.today().isoformat())
    cur.execute(insert_orders_script, insert_orders_value)

    select_script = "SELECT MAX(id) FROM orders"
    cur.execute(select_script)
    orders_result = cur.fetchone()

    con.commit()
    for id in idProducts:
        insert_menu_orders_value = (int.__int__(orders_result[0]), id[0], id[1])
        cur.execute(insert_menu_orders_script, insert_menu_orders_value)
        con.commit()

    con.commit()
    return products


async def get_all_orders_products_by_id(con, id):
    cur = con.cursor()
    selectValue = (int(id),)
    select_script = "SELECT menu.named, menu.types,order_products.price FROM menu JOIN order_products on order_products.menu_id = menu.id where order_products.order_id = %s"
    cur.execute(select_script, selectValue)
    result = cur.fetchall()
    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)


async def get_orders_by_id(con, id: str):
    if not id.isdecimal():
        return "ID must be num!"
    cur = con.cursor()
    selectValue = (int(id),)
    selectScript = "SELECT orders.*, sum(order_products.price) AS totalprice FROM orders JOIN order_products ON orders.id = order_products.order_id where orders.id = %s GROUP BY orders.id;"
    cur.execute(selectScript, selectValue)
    result = cur.fetchall()
    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)


async def get_orders(con):
    cur = con.cursor()
    cur.execute(
        "SELECT orders.*, sum(order_products.price) AS avg_order_number FROM orders JOIN order_products ON orders.id = order_products.order_id GROUP BY orders.id;")
    result = cur.fetchall()

    if result is None:
        return JSONResponse(content="orders haven't found", status_code=status.HTTP_404_NOT_FOUND)
    con.commit()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)


async def get_total_cost(con, products):
    cur = con.cursor()
    total = 0
    for product in products:
        select_value = (product,)
        select_script = "SELECT cost FROM menu where named = %s"
        cur.execute(select_script, select_value)
        data = cur.fetchone()
        total += int(data[0])
    return total.__str__()
