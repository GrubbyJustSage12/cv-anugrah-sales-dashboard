{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "16e36504-e6bf-4c7c-904e-4b798800306f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "3e27ea62-cbc8-4065-b242-01c0fde48cc9",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-08-05 20:01:40.983 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:40.984 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:40.984 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "st.title(\"Sales Dashboard for CV. Anugerah Agung\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "eb595110-4c36-4a3d-bb22-6909996a2259",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-08-05 20:01:41.481 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:41.482 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:41.482 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:41.483 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:41.484 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-08-05 20:01:41.486 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "uploaded_file = st.file_uploader(\"Upload CSV file\", type=[\"csv\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "e07f4c56-950c-47ed-ba92-4d37d79fe1ba",
   "metadata": {},
   "outputs": [],
   "source": [
    "if uploaded_file:\n",
    "    # Load with proper separator and encoding\n",
    "    df = pd.read_csv(uploaded_file, sep=\";\", encoding=\"utf-8\")\n",
    "\n",
    "    # Clean and convert\n",
    "    df[\"FORM_DATE\"] = pd.to_datetime(df[\"FORM_DATE\"])\n",
    "    df[\"Month\"] = df[\"FORM_DATE\"].dt.to_period(\"M\").astype(str)\n",
    "    df[\"SALES_AMOUNT\"] = df[\"SALES_AMOUNT\"].astype(str).str.replace(\",\", \".\").astype(float)\n",
    "\n",
    "    st.subheader(\"1. Penjualan Tiap Customer Tiap Bulan\")\n",
    "    monthly = df.groupby([\"CUSTOMER_NAME\", \"Month\"])[\"SALES_AMOUNT\"].sum().reset_index()\n",
    "    st.dataframe(monthly)\n",
    "\n",
    "    st.subheader(\"2. Filter Berdasarkan Kota Customer\")\n",
    "    city = st.selectbox(\"Pilih Kota\", df[\"CUSTOMER_CITY\"].unique())\n",
    "    filtered_by_city = df[df[\"CUSTOMER_CITY\"] == city]\n",
    "    st.dataframe(filtered_by_city)\n",
    "\n",
    "    st.subheader(\"3. Filter Berdasarkan Salesperson\")\n",
    "    salesperson = st.selectbox(\"Pilih Salesperson\", df[\"SALESMAN_NAME\"].unique())\n",
    "    sp_data = df[df[\"SALESMAN_NAME\"] == salesperson]\n",
    "\n",
    "    st.write(\"Daftar Customer yang Dipegang:\")\n",
    "    st.dataframe(sp_data[[\"CUSTOMER_NAME\", \"CUSTOMER_CITY\"]].drop_duplicates())\n",
    "\n",
    "    st.metric(\"Total Penjualan\", f\"{sp_data['SALES_AMOUNT'].sum():,.2f}\")\n",
    "\n",
    "    chart = px.bar(sp_data, x=\"CUSTOMER_NAME\", y=\"SALES_AMOUNT\",\n",
    "                   title=f\"Penjualan per Customer oleh {salesperson}\",\n",
    "                   labels={\"SALES_AMOUNT\": \"Total Penjualan\"})\n",
    "    st.plotly_chart(chart)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "0f37c296-72be-488e-9885-7f3bb098a396",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
