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
        # Calculate the total sum of all orders
        # total_orders = len(df)
        total_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalsum").json()
        average_orders_sum = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/averagesum").json()

        # Display total and average orders sum using a text element
        st.write(f"**Total Orders Sum:** {total_orders_sum[0]}")
        st.write(f"**Average Orders Sum:** {average_orders_sum[0]}")

        # Display the total sum above the table
        # st.write(f"**Total Orders:** {total_orders}")



        id = st.text_input("Check order's data by order id:")
        if(id.isalnum()):
            data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/orders/" + id).json()
            if len(data) == 0:
                st.write("Order with current id isn't exist!")
            else:
                df = pd.DataFrame(data, columns=["id", "created_date", "updated_date", "price"])
                df.rename(columns={"price": "total"}, inplace=True)  # Renaming the 'price' column to 'total'
                st.dataframe(df)
                chathistory = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/chathistory/" + id).json()
                with st.expander("Chat history"):
                    for messages in chathistory:
                        st.write("CUSTOMER: " + messages[0])
                        st.write("BOT: " + messages[1])
                with st.expander("products"):
                    products = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/orders/allproduct/" + id).json()
                    df_products = pd.DataFrame(products, columns=["name", "type", "price"])
                    st.dataframe(df_products)

        # Display the orders table using a DataTable
        # Convert the result to a DataFrame
        df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date", "price"])
        df.rename(columns={"price": "total"}, inplace=True)  # Renaming the 'price' column to 'total'
        st.write("**Orders Overview**")
        df.index = df.index + 1
        st.dataframe(df)

        # Fetch total sales data for each product
        total_sales_data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/totalevery").json()
        df_products = pd.DataFrame(total_sales_data, columns=["name", "total_sale", "price","stock"])
        df_products = df_products[["name", "stock", "price", "total_sale"]]

        # Visualize total sales data using a bar chart
        fig = px.bar(df_products, x="name", y="total_sale", text="total_sale", title="Total Sales by Product")
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        st.plotly_chart(fig)

        # Display the products table using a DataTable
        st.write("**Products Overview**")
        df_products.index = df_products.index + 1
        st.dataframe(df_products)

        # Display the products table using a DataTable
        st.write("**Upsell stats**")
        statistic = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/statistic").json()
        df = pd.DataFrame(statistic, columns=["total_asked", "accepted", "rejected", "price"])
        df.index = df.index + 1
        st.dataframe(df)
    else:
        st.write("No orders found")

# Call the function to display data and charts
display_all_orders()
