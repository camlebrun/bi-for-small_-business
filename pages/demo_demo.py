import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Revenue Comparison Tool",
    page_icon="📊",
    layout="wide"
)

# Header
st.markdown("<h1 style='text-align: center;'>Revenue Comparison Tool</h1>", unsafe_allow_html=True)

# Seasonality parameters
seasonality_period = st.number_input("Enter Seasonality Period", min_value=1, value=12)
seasonality_trend = st.selectbox("Select Seasonality Trend", ["Positive", "Negative"])

# Generate random dataframe if button is clicked
@st.cache_data(persist="disk")
def generate_random_data():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 1, 1)
    sales_data = []
    current_date = start_date
    while current_date < end_date:
        if seasonality_period == 3:
            seasonality = np.sin((current_date.month % 3) * (2 * np.pi / 3)) * 1000
        elif seasonality_period == 12:
            seasonality = np.sin((current_date.month - 1) * (2 * np.pi / 12)) * 1000
        if seasonality_trend == "Negative":
            seasonality *= -1
        sales_revenue = random.randint(5000, 20000)
        sales_data.append({'Date': current_date.strftime('%Y-%m-%d'), 'Sales Revenue': sales_revenue + seasonality})
        current_date += timedelta(days=random.randint(28, 35))
    df = pd.DataFrame(sales_data)
    return df
button_clicked = st.button("Generate Random Data")

# Generate random data and display success message
df = generate_random_data()
if button_clicked:
    st.cache_data.clear()
    button_clicked = True
    st.success("Data generated successfully.")

tab_1, tab_2, tab_3, tab_4 = st.tabs(["Generated Data", "General Statistics", "Time Series", "Download Data"])

# Calculate statistics
min_val = df["Sales Revenue"].min().round(2)
min_date = df.loc[df["Sales Revenue"].idxmin()]["Date"]
max_val = df["Sales Revenue"].max().round(2)
max_date = df.loc[df["Sales Revenue"].idxmax()]["Date"]
mean_val = df["Sales Revenue"].mean().round(2)
mean_date = df.iloc[df['Sales Revenue'].sub(mean_val).idxmin()]["Date"]
median_val = df["Sales Revenue"].median().round(2)
median_date = df.iloc[df['Sales Revenue'].sub(median_val).idxmin()]["Date"]

with tab_1: 
    st.markdown("<h3 style='text-align: center;'>Overview of generated Data</h3>", unsafe_allow_html=True)
    st.plotly_chart(go.Figure(data=[go.Scatter(x=df["Date"], y=df["Sales Revenue"], mode='lines', name="Revenue")]), use_container_width=True)
    st.dataframe(df, use_container_width=True)

with tab_2:
    st.markdown("<h3 style='text-align: center;'>Revenue Statistics</h3>", unsafe_allow_html=True)
    st.write(f"Minimum Revenue: ${min_val} (Date: {min_date})")
    st.write(f"Maximum Revenue: ${max_val} (Date: {max_date})")
    st.write(f"Mean Revenue: ${mean_val} (Date: {mean_date})")
    st.write(f"Median Revenue: ${median_val} (Date: {median_date})")

with tab_3:
    st.markdown("<h3 style='text-align: center;'>Time Series</h3>", unsafe_allow_html=True)
    st.info("The window is the number of months for comparison.")
    window_size = st.number_input("Number of Months for Comparison", min_value=1, value=3)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Sales Revenue"], mode='lines', name="Revenue"))
    growth_column_name = f"Revenue Growth ({window_size}-Period Window)"
    df[growth_column_name] = df['Sales Revenue'].diff(periods=window_size)
    bar_color = ['green' if diff > 0 else 'red' for diff in df[growth_column_name]]
    fig.add_trace(go.Bar(x=df["Date"], y=df[growth_column_name], name="Revenue Growth", marker_color=bar_color))
    fig.update_layout(title="Revenue and Revenue Growth", xaxis_title="Date", yaxis_title="Value")
    st.plotly_chart(fig, use_container_width=True)
with tab_4: 
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        workbook = writer.book
        worksheet = writer.sheets['Data']
        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({'values': '=Data!$B$2:$B$' + str(len(df) + 1), 'categories': '=Data!$A$2:$A$' + str(len(df) + 1), 'name': 'Revenue'})
        worksheet.insert_chart('D2', chart)
    excel_buffer.seek(0)
    st.download_button(label="Download Results", data=excel_buffer, file_name="results.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
