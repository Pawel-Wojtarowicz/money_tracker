import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime


# ----- SETTINGS -----
incomes = ["Salary", "Other"]
expenses = ["Mortage", "Loan", "Rent", "Bills", "Car",
            "Hobby", "Food", "Subscriptions", "Buddy", "Savings"]
currency = "PLN"
page_title = "Where is my money"
page_icon = ":moneybag:"
layout = "centered"  # check wide
# --------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# Drop down values
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])

# input
st.header(f"Data entry in {currency}")
with st.form("Entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month", months, key="month")
    col2.selectbox("Select Year", years, key="year")

    with st.expander("Income"):
        for income in incomes:
            st.number_input(f"{income}:", min_value=0,
                            format="%i", step=10, key=income)
    with st.expander("Expenses"):
        for expense in expenses:
            st.number_input(f"{expense}:", min_value=0,
                            format="%i", step=10, key=expense)
    with st.expander("Comment"):
        comment = st.text_area("", placeholder="Enter a comment here ...")

    submitted = st.form_submit_button("Save data")
    if submitted:
        period = str(st.session_state['year']) + \
            "-" + str(st.session_state['month'])
        incomes = {income: st.session_state[income] for income in incomes}
        expenses = {expense: st.session_state[expense]
                    for expense in expenses}

        st.write(f"incomes: {incomes}")
        st.write(f"expenses: {expenses}")
        st.success("Data saved!")


st.header("Virtualization")
with st.form("saved_periods"):
    period = st.selectbox("Select Period:", ["2022_March"])
    submitted = st.form_submit_button("Plot Period")
    if submitted:
        comment = "Some comment"
        incomes = {"Salary": 5000, "Other": 2000}
        expenses = {"Mortage": 2200, "Food": 500, "Buddy": 300}

        total_income = sum(incomes.values())
        total_expenses = sum(expenses.values())
        remaining_budget = total_income - total_expenses
        col1, col2, col3 = st.columns(3)
        col1.metric("Total income", f"{total_income} {currency}")
        col2.metric("Total expense", f"{total_expenses} {currency}")
        col3.metric("Remaining budget", f"{remaining_budget} {currency}")
        st.text(f"Comment: {comment}")
