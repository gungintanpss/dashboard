import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn
sns.set(style='darkgrid')

# Load data
@st.cache
def load_data():
    data = pd.read_csv("main_data.csv")
    return data

# Main function to create the dashboard
def main():
    st.title("Dashboard Visualisasi Data Pesanan")
    
    # Load dataset
    df = load_data()

    # Filter data if necessary
    st.sidebar.header("Filter")
    payment_type = st.sidebar.multiselect("Pilih Metode Pembayaran:", options=df['payment_type'].unique(), default=df['payment_type'].unique())
    filtered_df = df[df['payment_type'].isin(payment_type)]

    # Visualisasi: Jumlah Pembatalan Pesanan Berdasarkan Metode Pembayaran
    st.subheader("Jumlah Pembatalan Pesanan Berdasarkan Metode Pembayaran")
    payment_cancel_count = filtered_df['order_status'].value_counts().reset_index()
    payment_cancel_count.columns = ['order_status', 'canceled_count']

    plt.figure(figsize=(12, 6))
    payment_cancel_count_sorted = payment_cancel_count.sort_values(by="canceled_count", ascending=False)

    ax = sns.barplot(x="order_status", y="canceled_count", data=payment_cancel_count_sorted, color="#69b3a2")
    plt.title('Jumlah Pembatalan Pesanan Berdasarkan Status Pesanan', fontsize=20, loc='center', pad=20)
    plt.xlabel('Status Pesanan', fontsize=14)
    plt.ylabel('Jumlah Pembatalan', fontsize=14)
    plt.tick_params(axis='x', labelsize=12)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    st.pyplot(plt)

    # Visualisasi: Pembatalan Pesanan Berdasarkan Metode Pembayaran
    st.subheader("Pembatalan Pesanan Berdasarkan Metode Pembayaran")
    payment_cancel_count = filtered_df['payment_type'].value_counts().reset_index()
    payment_cancel_count.columns = ['payment_type', 'canceled_count']

    plt.figure(figsize=(10, 10))
    plt.pie(payment_cancel_count['canceled_count'], labels=payment_cancel_count['payment_type'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Pembatalan Pesanan Berdasarkan Metode Pembayaran', fontsize=20)
    plt.axis('equal')  
    st.pyplot(plt)

    # Menghitung status pengiriman
    st.subheader("Status Pengiriman")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['delivery_diff'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days  # Menghitung selisih hari

    def categorize_delivery(diff):
        if diff > 0:
            return 'Terlambat'  
        elif diff == 0:
            return 'Tepat Waktu'  
        else:
            return 'Lebih Cepat'  

    df['delivery_status'] = df['delivery_diff'].apply(categorize_delivery)
    delivery_counts = df['delivery_status'].value_counts().reset_index()
    delivery_counts.columns = ['Delivery Status', 'Count']

    plt.figure(figsize=(10, 5))
    sns.barplot(x="Count", y="Delivery Status", data=delivery_counts.sort_values(by="Count", ascending=False), color="#72BCD4")
    plt.title("Jumlah Pengiriman Berdasarkan Status Pengiriman", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=12)
    st.pyplot(plt)

if __name__ == "__main__":
    main()
