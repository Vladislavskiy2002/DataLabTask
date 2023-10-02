import streamlit as st
import psycopg2
import pandas as pd
import requests

# Create a Streamlit app
st.title('Admin vieW')

# Function to fetch and display all orders as a table
def display_all_orders():
    orders = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/orders").json()
    # orders = cursor.fetchall()
    if orders:
        # Convert the result to a DataFrame
        df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date"])
        # Calculate the total sum of all orders
        total_orders = len(df)
        total_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalsum").json()
        st.write(f"Total Orders sum : {total_orders_sum[0]}")
        average_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/averagesum").json()
        st.write(f"Average Orders sum : {average_orders_sum[0]}")
        # Display the total sum above the table
        st.write(f"Total Orders: {total_orders}")
        # Reset the index to start from 1
        df.index = df.index + 1

        st.dataframe(df)

        totalbyeveryproduct = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalevery").json()
        # Створюємо DataFrame зі збережених даних
        df_products = pd.DataFrame(totalbyeveryproduct, columns=["name","total sale","price"])
        # df_products = pd.DataFrame(data, columns=["name", "price", "total sale"])
        # df = pd.DataFrame(totalbyeveryproduct,pricebyeveryproduct,columns=["name", "total sale", "price"])
        df_products.index = df_products.index + 1

        st.dataframe(df_products)
    else:
        st.write("No orders found")

display_all_orders()