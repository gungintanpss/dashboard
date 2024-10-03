import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

main_df = pd.read_csv("main_data.csv")

payment_cancel_count = main_df[['payment_type', 'order_status']].groupby('payment_type').agg(canceled_count=('order_status', lambda x: (x == 'canceled').sum())).reset_index()
payment_cancel_count_sorted = payment_cancel_count.sort_values(by="canceled_count", ascending=False)

delivery_counts = main_df['delivery_status'].value_counts().reset_index()
delivery_counts.columns = ['Delivery Status', 'Count']

st.title("Dashboard E-Commerce")
st.subheader("Pembatalan Pesanan Berdasarkan Metode Pembayaran")

plt.figure(figsize=(12, 6))
ax = sns.barplot(
    x="payment_type", 
    y="canceled_count", 
    data=payment_cancel_count_sorted, 
    color="#69b3a2"
)

plt.title('Jumlah Pembatalan Pesanan Berdasarkan Metode Pembayaran', fontsize=20, loc='center', pad=20)
plt.xlabel('Metode Pembayaran', fontsize=14)
plt.ylabel('Jumlah Pembatalan', fontsize=14)
plt.tick_params(axis='x', labelsize=12)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(plt)

plt.figure(figsize=(10, 10))
plt.pie(payment_cancel_count['canceled_count'], 
        labels=payment_cancel_count['payment_type'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plt.cm.Paired.colors)
plt.title('Pembatalan Pesanan Berdasarkan Metode Pembayaran', fontsize=20)
plt.axis('equal')  
st.pyplot(plt)

st.subheader("Jumlah Pengiriman Berdasarkan Status Pengiriman")

plt.figure(figsize=(10, 5))
sns.barplot(
    x="Count", 
    y="Delivery Status",
    data=delivery_counts.sort_values(by="Count", ascending=False),
    color="#72BCD4" 
)

plt.title("Jumlah Pengiriman Berdasarkan Status Pengiriman", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
st.pyplot(plt)

plt.figure(figsize=(8, 8))
plt.pie(
    delivery_counts['Count'],
    labels=delivery_counts['Delivery Status'],
    autopct='%1.1f%%',
    startangle=90,
    colors=["#72BCD4", "#D3D3D3", "#A2D9CE"]  
)

centre_circle = plt.Circle((0, 0), 0.65, fc='white') 
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Prosentase Pengiriman Berdasarkan Status Pengiriman", fontsize=15, loc='center', pad=20) 
plt.axis('equal')  
st.pyplot(plt)
