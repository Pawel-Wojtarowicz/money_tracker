import streamlit as st
import plotly.graph_objects as go 
import calendar
from datetime import datetime


# ----- SETTINGS -----
income = ["Salary", "Other"]
expenses = ["Mortage", "Loan", "Rent", "Bills", "Car", "Hobby", "Food", "Subscriptions", "Buddy", "Savings"]
currency = "PLN"
page_title = "Where is my money"
page_icon = ":moneybag:"
layout = "centered" #check wide
# -------------------- 

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# Drop down values 
years = [datetime.today().year, datetime.today().year -1]
months = list(calendar.month_name[1:])

# input 
st.header(f"Data entry in {currency}")
with st.form("Entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month", months, key="month")
    col2.selectbox("Select Year", years, key="year")
    
    




