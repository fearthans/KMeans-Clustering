import streamlit as st
import pandas as pd
from model import bersihkan_data

# Konfigurasi halaman
st.set_page_config(page_title="Customer Segmentation App", layout="wide")

# Judul utama
st.markdown("<h1 style='font-size:36px;'>👋 Selamat Datang!</h1>", unsafe_allow_html=True)
st.markdown("### Aplikasi ini membantu mengelompokkan pelanggan berdasarkan pola transaksi menggunakan K-Means Clustering.")

# Upload file
uploaded_file = st.file_uploader("📂 Upload file transaksi pelanggan (format: .csv)", type=["csv"])

st.markdown("### 📂 Contoh Format File Transaksi yang Diterima")

with open("assets/sample_transaksi.csv", "rb") as file:
    st.download_button(
        label="📥 Download Contoh File CSV",
        data=file,
        file_name="contoh_transaksi.csv",
        mime="text/csv"
    )

st.caption("Gunakan file ini sebagai referensi format untuk mengupload data pelanggan.")

if uploaded_file:
    try:
        df_raw = pd.read_csv(uploaded_file)
        df_clean = bersihkan_data(df_raw)

        # Simpan ke session_state
        st.session_state["data_awal"] = df_raw
        st.session_state["data_bersih"] = df_clean

        st.success("✅ File berhasil diupload dan data berhasil dibersihkan!")
        st.markdown("👉 Silakan lanjut ke menu **RFM Analysis** di sidebar untuk langkah selanjutnya.")

        # Tampilkan data awal & bersih
        with st.expander("🔍 Lihat Data Asli (Raw)"):
            st.dataframe(df_raw, use_container_width=True, height=400)

        with st.expander("✅ Lihat Data Bersih (Siap Olah)"):
            st.dataframe(df_clean, use_container_width=True, height=400)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.warning("⚠️ Silakan upload file CSV terlebih dahulu.")

# Divider
st.markdown("---")

# Panduan Alur Aplikasi
st.markdown("### 🚀 Alur Analisis:")
st.markdown("""
1. **RFM Analysis** – Membersihkan data & menghitung Recency, Frequency, Monetary (RFM)
2. **Clustering** – Segmentasi pelanggan menggunakan K-Means, termasuk evaluasi DBI & Silhouette Score
3. **Dashboard & Rekomendasi** – Visualisasi hasil, lihat pelanggan bernilai tinggi, dan rekomendasi produk terbaik tiap cluster
""")
