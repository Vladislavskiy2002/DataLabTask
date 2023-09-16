# import streamlit as st
# import time
# import numpy as np
#
# st.set_page_config(page_title="Plotting Demo", page_icon="📈")
#
# st.markdown("# Plotting Demo")
# st.sidebar.header("Plotting Demo")
# st.write(
#     """This demo illustrates a combination of plotting and animation with
# Streamlit. We're generating a bunch of random numbers in a loop for around
# 5 seconds. Enjoy!"""
# )
#
# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)
#
# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)
#
# progress_bar.empty()
#
# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")
import streamlit as st
import psycopg2
import pandas as pd
import requests

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='1234',
    host='localhost'
)
# Function to fetch and display user orders
# def display_user_orders(user_id):
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM orders")
#         orders = cursor.fetchall()
#         if orders:
#             st.subheader(f'Orders for User {user_id}')
#             for order in orders:
#                 st.write(order)
#         else:
#             st.write(f"No orders found for User {user_id}")
# #
# # Get a list of distinct user IDs
# with conn.cursor() as cursor:
#     cursor.execute("SELECT DISTINCT user_id FROM orders")
#     user_ids = [row[0] for row in cursor.fetchall()]
#
# # Select a user to display their orders
# selected_user = st.selectbox("Select User", user_ids)

# Create a Streamlit app
st.title('Admin view')

# Function to fetch and display all orders as a table
def display_all_orders():
    orders = requests.get("http://127.0.0.1:8000/orders").json()
    # orders = cursor.fetchall()
    if orders:
        # Convert the result to a DataFrame
        df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date", "address"])
        # Calculate the total sum of all orders
        total_orders = len(df)

        # Display the total sum above the table
        st.write(f"Total Orders: {total_orders}")

        # Reset the index to start from 1
        df.index = df.index + 1

        st.dataframe(df)
    else:
        st.write("No orders found")

# Display all orders as a table
display_all_orders()

# Close the database connection
conn.close()

# df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date", "address"])
