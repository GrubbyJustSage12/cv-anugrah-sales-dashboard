#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
import locale


# In[7]:


st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard for CV. Anugerah Agung")


# In[8]:


uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


# In[11]:


if uploaded_file:
    # Load CSV with proper separator and encoding
    df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")

    # Clean and convert
    df["FORM_DATE"] = pd.to_datetime(df["FORM_DATE"])
    df["Year"] = df["FORM_DATE"].dt.year
    df["Month_Name"] = df["FORM_DATE"].dt.month_name()
    df["Month_Year"] = df["FORM_DATE"].dt.to_period("M").astype(str)
    df["SALES_AMOUNT"] = df["SALES_AMOUNT"].astype(str).str.replace(",", ".").astype(float)

    # Filter by year and month
    st.sidebar.header("Filter Data")
    selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(df["Year"].unique()))
    selected_month = st.sidebar.selectbox(
        "Pilih Bulan", 
        sorted(
            df[df["Year"] == selected_year]["Month_Name"].unique(), 
            key=lambda x: list(calendar.month_name).index(x)
        )
    )

    filtered_df = df[(df["Year"] == selected_year) & (df["Month_Name"] == selected_month)]

    # 1. Penjualan Tiap Customer Tiap Bulan
    st.subheader("1. Penjualan Tiap Customer Tiap Bulan")
    monthly = (
        filtered_df.groupby("CUSTOMER_NAME")["SALES_AMOUNT"]
        .sum()
        .reset_index()
        .sort_values(by="SALES_AMOUNT", ascending=False)
    )
    st.dataframe(monthly)

    # 2. Filter Berdasarkan Kota Customer
    st.subheader("2. Filter Berdasarkan Kota Customer")
    city = st.selectbox("Pilih Kota", filtered_df["CUSTOMER_CITY"].unique())
    filtered_by_city = filtered_df[filtered_df["CUSTOMER_CITY"] == city]
    st.dataframe(
        filtered_by_city.drop(columns=["Year", "Month_Name", "Month_Year"])
    )

    # 3. Filter Berdasarkan Salesperson
    st.subheader("3. Filter Berdasarkan Salesperson")
    salesperson = st.selectbox("Pilih Salesperson", filtered_df["SALESMAN_NAME"].unique())
    sp_data = filtered_df[filtered_df["SALESMAN_NAME"] == salesperson]

    st.write("Daftar Customer yang Dipegang:")
    st.dataframe(sp_data[["CUSTOMER_NAME", "CUSTOMER_CITY"]].drop_duplicates())

    total_sales = sp_data["SALES_AMOUNT"].sum()
    st.metric("Total Penjualan", f"Rp {total_sales:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    chart_data = (
        sp_data.groupby("CUSTOMER_NAME")["SALES_AMOUNT"]
        .sum()
        .reset_index()
        .sort_values(by="SALES_AMOUNT", ascending=False)
    )

    chart = px.bar(
        chart_data,
        x="CUSTOMER_NAME",
        y="SALES_AMOUNT",
        title=f"Penjualan per Customer oleh {salesperson}",
        labels={"SALES_AMOUNT": "Total Penjualan"},
    )
    st.plotly_chart(chart)


# In[ ]:




