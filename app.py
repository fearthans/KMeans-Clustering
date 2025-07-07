import streamlit as st
import pandas as pd
from model import bersihkan_data

st.set_page_config(page_title="Customer Segmentation App", layout="wide")

st.markdown("<h1 style='font-size:36px;'>👋 Selamat Datang!</h1>", unsafe_allow_html=True)
st.markdown("### Aplikasi ini akan membantu kamu mengelompokkan pelanggan berdasarkan pola transaksi menggunakan K-Means Clustering.")

uploaded_file = st.file_uploader("📂 Upload file transaksi pelanggan (CSV)", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_clean = bersihkan_data(df_raw)

    st.session_state["data_awal"] = df_raw
    st.session_state["data_bersih"] = df_clean

    st.success("✅ File berhasil diupload dan data langsung dibersihkan!")
    st.markdown("👉 Silakan lanjut ke menu **RFM Analysis** di sidebar.")
else:
    st.warning("Silakan upload file CSV terlebih dahulu.")

st.markdown("---")
st.markdown("""
### 🚀 Alur Modul:
1. **RFM Analysis** – Membersihkan data & menghitung Recency, Frequency, Monetary
2. **Clustering** – Segmentasi pelanggan dengan K-Means, evaluasi hasil (DBI & Silhouette)
3. **Dashboard** – Visualisasi cluster, pelanggan bernilai tinggi & rekomendasi produk
""")