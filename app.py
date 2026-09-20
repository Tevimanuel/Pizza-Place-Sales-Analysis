# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 00:23:34 2026

@author: USER
"""

# ============================================
# PIZZA PLACE SALES DASHBOARD
# ============================================

import streamlit as st
import pandas as pd
import os

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Pizza Sales Dashboard",
    layout="wide"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))

    df_orders = pd.read_csv(os.path.join(base_path, "orders.csv"), encoding='latin-1')
    df_details = pd.read_csv(os.path.join(base_path, "order_details.csv"), encoding='latin-1')
    df_pizzas = pd.read_csv(os.path.join(base_path, "pizzas.csv"), encoding='latin-1')
    df_types = pd.read_csv(os.path.join(base_path, "pizza_types.csv"), encoding='latin-1')

    df = df_details.merge(df_pizzas, on='pizza_id', how='left')
    df = df.merge(df_types, on='pizza_type_id', how='left')
    df = df.merge(df_orders, on='order_id', how='left')

    df['revenue'] = df['quantity'] * df['price']
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['hour'] = pd.to_datetime(df['time']).dt.hour

    return df

try:
    df = load_data()
except FileNotFoundError as e:
    st.error("File not found: " + str(e))
    st.info("Make sure all 4 CSV files are in the SAME folder as app.py")
    st.stop()
except Exception as e:
    st.error("Error loading data: " + str(e))
    st.stop()

# ============================================
# HEADER
# ============================================
st.title("Pizza Place Sales Dashboard")
st.markdown("### One Year of Sales Data - Complete Analysis")
st.markdown("---")

# ============================================
# KPI METRICS
# ============================================
total_revenue = df['revenue'].sum()
total_orders = df['order_id'].nunique()
total_pizzas = df['quantity'].sum()
avg_order_value = df.groupby('order_id')['revenue'].sum().mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", "${:,.2f}".format(total_revenue))
col2.metric("Total Orders", "{:,}".format(total_orders))
col3.metric("Pizzas Sold", "{:,}".format(total_pizzas))
col4.metric("Avg Order Value", "${:,.2f}".format(avg_order_value))

st.markdown("---")

# ============================================
# TOP PIZZAS & SALES BY DAY
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 Bestselling Pizzas")
    top5 = df.groupby('name')['quantity'].sum().nlargest(5)
    st.bar_chart(top5)

with col2:
    st.subheader("Sales by Day of Week")
    day_sales = df.groupby('day_of_week')['revenue'].sum()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']
    day_sales = day_sales.reindex(day_order)
    st.bar_chart(day_sales)

st.markdown("---")

# ============================================
# MONTHLY TREND & PEAK HOURS
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue Trend")
    monthly = df.groupby('month')['revenue'].sum()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly = monthly.reindex(month_order)
    st.line_chart(monthly)

with col2:
    st.subheader("Peak Sales Hours")
    hourly = df.groupby('hour')['order_id'].nunique()
    st.bar_chart(hourly)

st.markdown("---")

# ============================================
# CATEGORY & SIZE
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    category = df.groupby('category')['revenue'].sum()
    st.bar_chart(category)

with col2:
    st.subheader("Revenue by Pizza Size")
    size_sales = df.groupby('size')['revenue'].sum()
    size_order = ['S', 'M', 'L', 'XL', 'XXL']
    size_sales = size_sales.reindex(size_order).dropna()
    st.bar_chart(size_sales)

st.markdown("---")

# ============================================
# UNDERPERFORMING PIZZAS
# ============================================
st.subheader("Underperforming Pizzas (Bottom 5)")
bottom5 = df.groupby('name')['quantity'].sum().nsmallest(5)
st.bar_chart(bottom5)

st.markdown("---")

# ============================================
# RAW DATA
# ============================================
with st.expander("View Raw Data (Click to expand)"):
    st.dataframe(df.head(100))
    st.write("Total rows: {:,}".format(len(df)))

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("Built with Python, Pandas & Streamlit")