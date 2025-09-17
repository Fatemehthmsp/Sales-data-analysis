import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar

st.set_page_config(page_title="📊 Sales Pro Dashboard", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv", parse_dates=["Date"])
    if "Month" not in df.columns:
        df["Month"] = df["Date"].dt.month
    if "DayOfWeek" not in df.columns:
        df["DayOfWeek"] = df["Date"].dt.dayofweek
    return df

df = load_data()

st.sidebar.header("🔍 Filters")
date_min, date_max = df["Date"].min(), df["Date"].max()

raw_date_input = st.sidebar.date_input(
    "Select Date Range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

if not isinstance(raw_date_input, (list, tuple)):
    start_date = end_date = pd.to_datetime(raw_date_input)
elif len(raw_date_input) == 2:
    start_date, end_date = pd.to_datetime(raw_date_input[0]), pd.to_datetime(raw_date_input[1])
else:
    start_date = pd.to_datetime(min(raw_date_input))
    end_date = pd.to_datetime(max(raw_date_input))

if start_date > end_date:
    start_date, end_date = end_date, start_date

promo_filter = st.sidebar.multiselect(
    "Promo Status",
    options=sorted(df["Promo"].unique()),
    default=sorted(df["Promo"].unique())
) if "Promo" in df.columns else None

mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
if promo_filter is not None:
    mask &= df["Promo"].isin(promo_filter)
df_filtered = df.loc[mask]

total_sales = df_filtered["Sales"].sum()
avg_daily = df_filtered.groupby("Date")["Sales"].sum().mean()
max_day_row = df_filtered.groupby("Date")["Sales"].sum().idxmax()
max_day_value = df_filtered.groupby("Date")["Sales"].sum().max()
min_day_row = df_filtered.groupby("Date")["Sales"].sum().idxmin()
min_day_value = df_filtered.groupby("Date")["Sales"].sum().min()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
col2.metric("📆 Avg Daily", f"{avg_daily:,.0f}")
col3.metric("📈 Best Day", f"{max_day_row.date()} ({max_day_value:,.0f})")
col4.metric("📉 Worst Day", f"{min_day_row.date()} ({min_day_value:,.0f})")

st.subheader("📈 Daily Sales Trend with Highlights")
daily_sales = df_filtered.groupby("Date")["Sales"].sum().reset_index()
fig = go.Figure()
fig.add_trace(go.Scatter(x=daily_sales["Date"], y=daily_sales["Sales"],
                         mode="lines+markers", line=dict(color="royalblue"), name="Daily Sales"))
fig.add_trace(go.Scatter(x=[max_day_row], y=[max_day_value], mode="markers+text", text=["⬆"],
                         textposition="top center", marker=dict(color="green", size=12), name="Peak"))
fig.add_trace(go.Scatter(x=[min_day_row], y=[min_day_value], mode="markers+text", text=["⬇"],
                         textposition="bottom center", marker=dict(color="red", size=12), name="Low"))
fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="#f9f9f9")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🗓️ Monthly Sales Heatmap")
cal_data = df_filtered.groupby(["Month", "DayOfWeek"])["Sales"].mean().reset_index()
cal_data["DayName"] = cal_data["DayOfWeek"].apply(lambda x: calendar.day_name[x])
heatmap = px.density_heatmap(cal_data, x="DayName", y="Month", z="Sales", color_continuous_scale="YlGnBu")
heatmap.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(heatmap, use_container_width=True)

if "Promo" in df_filtered.columns:
    st.subheader("🏷️ Promo vs Non-Promo Sales")
    promo_avg = df_filtered.groupby("Promo")["Sales"].mean().reset_index()
    fig2 = px.bar(promo_avg, x="Promo", y="Sales", text_auto=".0f", color="Promo",
                  color_continuous_scale="Sunset")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("⭐ Top 10 Days by Sales")
top10 = daily_sales.sort_values("Sales", ascending=False).head(10)
st.table(top10)
