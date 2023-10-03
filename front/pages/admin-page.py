# import streamlit as st
# import psycopg2
# import pandas as pd
# import requests
#
# # Create a Streamlit app
# st.title('Admin vieW')
#
# # Function to fetch and display all orders as a table
# def display_all_orders():
#     orders = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/orders").json()
#     # orders = cursor.fetchall()
#     if orders:
#         # Convert the result to a DataFrame
#         df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date"])
#         # Calculate the total sum of all orders
#         total_orders = len(df)
#         total_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalsum").json()
#         st.write(f"Total Orders sum : {total_orders_sum[0]}")
#         average_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/averagesum").json()
#         st.write(f"Average Orders sum : {average_orders_sum[0]}")
#         # Display the total sum above the table
#         st.write(f"Total Orders: {total_orders}")
#         # Reset the index to start from 1
#         df.index = df.index + 1
#
#         st.dataframe(df)
#
#         totalbyeveryproduct = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalevery").json()
#         # Створюємо DataFrame зі збережених даних
#         df_products = pd.DataFrame(totalbyeveryproduct, columns=["name","total sale","price","stock"])
#         # df_products = pd.DataFrame(data, columns=["name", "price", "total sale"])
#         # df = pd.DataFrame(totalbyeveryproduct,pricebyeveryproduct,columns=["name", "total sale", "price"])
#         df_products.index = df_products.index + 1
#
#         st.dataframe(df_products)
#     else:
#         st.write("No orders found")
#
# display_all_orders()

import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Title of the application
st.title('Admin View')

# Function to fetch and display all orders as a table and visualize data
def display_all_orders():
    orders = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/orders").json()

    if orders:
        # Convert the result to a DataFrame
        df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date"])

        # Calculate the total sum of all orders
        total_orders = len(df)
        total_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalsum").json()
        average_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/averagesum").json()

        # Display total and average orders sum using a text element
        st.write(f"**Total Orders Sum:** {total_orders_sum[0]}")
        st.write(f"**Average Orders Sum:** {average_orders_sum[0]}")

        # Display the total sum above the table
        st.write(f"**Total Orders:** {total_orders}")

        # Display the orders table using a DataTable
        st.write("**Orders Overview**")
        df.index = df.index + 1
        st.dataframe(df)

        # Fetch total sales data for each product
        total_sales_data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalevery").json()
        df_products = pd.DataFrame(total_sales_data, columns=["name", "total_sale", "price","stock"])

        # Visualize total sales data using a bar chart
        fig = px.bar(df_products, x="name", y="total_sale", text="total_sale", title="Total Sales by Product")
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        st.plotly_chart(fig)

        # Display the products table using a DataTable
        st.write("**Products Overview**")
        df_products.index = df_products.index + 1
        st.dataframe(df_products)

    else:
        st.write("No orders found")

# Call the function to display data and charts
display_all_orders()
