import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
import database as db

# https://www.youtube.com/watch?v=3egaMfE9388

# ----- SETTINGS -----
incomes = ["Salary", "Other"]
expenses = ["Mortage", "Loan", "Rent", "Bills", "Car",
            "Hobby", "Food", "Subscriptions", "Buddy", "Savings"]
currency = "PLN"
page_title = "Where is my money"
page_icon = ":moneybag:"
layout = "centered"
# --------------------

# ----- CONFIG -----
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
# --------------------


# Drop down values
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])

# ---- Db interface ---


def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


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
        db.insert_periods(period, incomes, expenses, comment)
        st.success("Data saved!")


st.header("Virtualization")
with st.form("saved_periods"):
    period = st.selectbox("Select Period:", get_all_periods())
    submitted = st.form_submit_button("Plot Period")
    if submitted:
        # get data from db
        period_data = db.get_periods(period)
        comment = period_data.get("comment")
        expenses = period_data.get("expenses")
        incomes = period_data.get("incomes")

        total_income = sum(incomes.values())
        total_expenses = sum(expenses.values())
        remaining_budget = total_income - total_expenses
        col1, col2, col3 = st.columns(3)
        col1.metric("Total income", f"{total_income} {currency}")
        col2.metric("Total expense", f"{total_expenses} {currency}")
        col3.metric("Remaining budget", f"{remaining_budget} {currency}")
        st.text(f"Comment: {comment}")

        # sanky chart
        label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
        source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
        target = [len(incomes)] * len(incomes) + [label.index(expense)
                                                  for expense in expenses]
        value = list(incomes.values()) + list(expenses.values())

        # data to dict, dict to sankey
        link = dict(source=source, target=target, value=value)
        node = dict(label=label, pad=20, thickness=30, color="#69b3a2")
        data = go.Sankey(link=link, node=node)

        # plot the chart
        fig = go.Figure(data)
        fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
        st.plotly_chart(fig, use_container_width=True)
