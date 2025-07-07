import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from model import gabung_final, rekomendasi_produk

st.title("📊 Customer Dashboard & Rekomendasi Produk")

# Validasi data
if "data_bersih" not in st.session_state or "df_clustered" not in st.session_state:
    st.warning("Silakan selesaikan proses RFM & Clustering terlebih dahulu.")
    st.stop()

# Ambil dari session
df_clean = st.session_state["data_bersih"]
df_clustered = st.session_state["df_clustered"]
df_final = gabung_final(df_clean, df_clustered)

st.subheader("📌 Data Final Cluster + Transaksi")
st.dataframe(df_final.head(20), use_container_width=True)

# Pelanggan bernilai tinggi
top_cluster = df_clustered.groupby('Cluster')['Total_Transaksi'].mean().idxmax()
df_high_value = df_final[df_final['Cluster'] == top_cluster]
st.subheader(f"🏆 Pelanggan Bernilai Tinggi (Cluster {top_cluster})")
st.dataframe(df_high_value[['Customer_id', 'Order_date', 'Total_Transaksi', 'Product_Name']], use_container_width=True)

# Rekomendasi produk
st.subheader("🎯 Rekomendasi Produk Tiap Cluster")
df_rekomendasi = rekomendasi_produk(df_final)
st.dataframe(df_rekomendasi, use_container_width=True)

# Visualisasi
st.subheader("👥 Jumlah Pelanggan per Cluster")
fig1, ax1 = plt.subplots()
sns.countplot(data=df_final, x='Cluster', palette='viridis', ax=ax1)
ax1.set_title("Distribusi Pelanggan per Cluster")
st.pyplot(fig1)

st.subheader("💰 Rata-rata Transaksi per Cluster")
fig2, ax2 = plt.subplots()
sns.barplot(
    data=df_final,
    x='Cluster',
    y='Total_Transaksi',
    estimator='mean',
    ci=None,
    palette='rocket',
    ax=ax2
)
ax2.set_title("Average Spending per Cluster")
st.pyplot(fig2)

# Export
st.subheader("⬇️ Unduh Data Akhir")
df_final.to_csv("assets/final_clustered.csv", index=False)
with open("assets/final_clustered.csv", "rb") as f:
    st.download_button("Download Data Final Cluster", f, file_name="final_clustered.csv", mime="text/csv")