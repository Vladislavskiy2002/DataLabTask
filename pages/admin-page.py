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
        total_orders_sum = requests.get("http://127.0.0.1:8000/allproducts/totalsum").json()
        st.write(f"Total Orders sum : {total_orders_sum[0]}")
        average_orders_sum = requests.get("http://127.0.0.1:8000/allproducts/averagesum").json()
        st.write(f"Average Orders sum : {average_orders_sum[0]}")
        # Display the total sum above the table
        st.write(f"Total Orders: {total_orders}")
        # Reset the index to start from 1
        df.index = df.index + 1

        st.dataframe(df)

        totalbyeveryproduct = requests.get("http://127.0.0.1:8000/allproducts/totalevery").json()
        df = pd.DataFrame(totalbyeveryproduct, columns=["name", "total sale"])
        df.index = df.index + 1

        st.dataframe(df)
    else:
        st.write("No orders found")

display_all_orders()
conn.close()

# df = pd.DataFrame(orders, columns=["id", "created_date", "updated_date", "address"])
