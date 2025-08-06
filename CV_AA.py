#!/usr/bin/env python
# coding: utf-8

# In[15]:


import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
import locale


# In[16]:


st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard for CV. Anugerah Agung")


# In[17]:


uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


# In[18]:


def format_rupiah(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# In[19]:


if uploaded_file:
    # Load CSV with proper separator and encoding
    df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")

    # Parse FORM_DATE and add date columns
    df["FORM_DATE"] = pd.to_datetime(df["FORM_DATE"])
    df["Year"] = df["FORM_DATE"].dt.year
    df["Month_Name"] = df["FORM_DATE"].dt.month_name()
    df["Month_Year"] = df["FORM_DATE"].dt.to_period("M").astype(str)

    # ✅ Clean SALES_AMOUNT (Indonesian format)
    df["SALES_AMOUNT"] = (
        df["SALES_AMOUNT"]
        .astype(str)
        .str.replace(".", "", regex=False)       # Remove thousands separator
        .str.replace(",", ".", regex=False)      # Replace decimal comma
        .astype(float)
    )

    # Sidebar filters
    st.sidebar.header("Filter Data")
    selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(df["Year"].unique()))
    selected_month = st.sidebar.selectbox(
        "Pilih Bulan",
        sorted(
            df[df["Year"] == selected_year]["Month_Name"].unique(),
            key=lambda x: list(calendar.month_name).index(x)
        )
    )

    # Filter dataset by year and month
    filtered_df = df[(df["Year"] == selected_year) & (df["Month_Name"] == selected_month)]

    # 1. Penjualan Tiap Customer Tiap Bulan
    st.subheader("1. Penjualan Tiap Customer Tiap Bulan")
    monthly = (
        filtered_df.groupby("CUSTOMER_NAME")["SALES_AMOUNT"]
        .sum()
        .reset_index()
        .sort_values(by="SALES_AMOUNT", ascending=False)
    )
    monthly["SALES_AMOUNT"] = monthly["SALES_AMOUNT"].apply(format_rupiah)
    st.dataframe(monthly)

    # 2. Filter Berdasarkan Kota Customer
    st.subheader("2. Filter Berdasarkan Kota Customer")
    city = st.selectbox("Pilih Kota", filtered_df["CUSTOMER_CITY"].unique())
    filtered_by_city = filtered_df[filtered_df["CUSTOMER_CITY"] == city]

    # Group by CUSTOMER_NAME and sum SALES_AMOUNT
    city_summary = (
        filtered_by_city.groupby("CUSTOMER_NAME")["SALES_AMOUNT"]
        .sum()
        .reset_index()
        .sort_values(by="SALES_AMOUNT", ascending=False)
    )
    city_summary["SALES_AMOUNT"] = city_summary["SALES_AMOUNT"].apply(format_rupiah)

    st.dataframe(city_summary)

    # Show total for city
    city_total = filtered_by_city["SALES_AMOUNT"].sum()
    formatted_city_total = format_rupiah(city_total)
    st.markdown(f"**Total Penjualan Kota {city}: Rp {formatted_city_total}**")

    # 3. Filter Berdasarkan Salesperson
    st.subheader("3. Filter Berdasarkan Salesperson")
    salesperson = st.selectbox("Pilih Salesperson", filtered_df["SALESMAN_NAME"].unique())
    sp_data = filtered_df[filtered_df["SALESMAN_NAME"] == salesperson]

    st.write("Daftar Customer yang Dipegang:")
    st.dataframe(sp_data[["CUSTOMER_NAME", "CUSTOMER_CITY"]].drop_duplicates())

    # Total sales for selected salesperson
    total_sales = sp_data["SALES_AMOUNT"].sum()
    formatted_total = f"Rp {format_rupiah(total_sales)}"
    st.metric("Total Penjualan", formatted_total)

    # Group by customer for chart
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




