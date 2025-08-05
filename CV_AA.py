#!/usr/bin/env python
# coding: utf-8

# In[13]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[14]:


st.title("Sales Dashboard for CV. Anugerah Agung")


# In[15]:


uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


# In[16]:


if uploaded_file:
    # Load with proper separator and encoding
    df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")

    # Clean and convert
    df["FORM_DATE"] = pd.to_datetime(df["FORM_DATE"])
    df["Month"] = df["FORM_DATE"].dt.to_period("M").astype(str)
    df["SALES_AMOUNT"] = df["SALES_AMOUNT"].astype(str).str.replace(",", ".").astype(float)

    st.subheader("1. Penjualan Tiap Customer Tiap Bulan")
    monthly = df.groupby(["CUSTOMER_NAME", "Month"])["SALES_AMOUNT"].sum().reset_index()
    st.dataframe(monthly)

    st.subheader("2. Filter Berdasarkan Kota Customer")
    city = st.selectbox("Pilih Kota", df["CUSTOMER_CITY"].unique())
    filtered_by_city = df[df["CUSTOMER_CITY"] == city]
    st.dataframe(filtered_by_city)

    st.subheader("3. Filter Berdasarkan Salesperson")
    salesperson = st.selectbox("Pilih Salesperson", df["SALESMAN_NAME"].unique())
    sp_data = df[df["SALESMAN_NAME"] == salesperson]

    st.write("Daftar Customer yang Dipegang:")
    st.dataframe(sp_data[["CUSTOMER_NAME", "CUSTOMER_CITY"]].drop_duplicates())

    st.metric("Total Penjualan", f"{sp_data['SALES_AMOUNT'].sum():,.2f}")

    chart = px.bar(sp_data, x="CUSTOMER_NAME", y="SALES_AMOUNT",
                   title=f"Penjualan per Customer oleh {salesperson}",
                   labels={"SALES_AMOUNT": "Total Penjualan"})
    st.plotly_chart(chart)


# In[ ]:




