import streamlit as st
import pandas as pd
from model import bersihkan_data

import streamlit as st

st.set_page_config(page_title="Qaraa Segmentation App", layout="wide")

# Konfigurasi halaman dan font Inter
st.set_page_config(page_title="Qaraa Segmentation App", layout="wide")

st.markdown("""
    <style>
    /* Import font Inter dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #F4F4F4;
    }

    /* Responsif: Sesuaikan ukuran heading di mobile */
    @media (max-width: 768px) {
        h1, h2, h3 {
            font-size: 22px !important;
        }
        .small-text {
            font-size: 14px !important;
        }
    }

    @media (min-width: 769px) {
        h1 {
            font-size: 32px !important;
        }
    }

    /* Styling tombol */
    .stButton > button {
        background-color: #A78BFA;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }

    /* Padding kontainer biar pas di desktop & mobile */
    .main .block-container {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Garis pemisah */
    hr {
        border: none;
        border-top: 1px solid #A78BFA;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.image("assets/favicon.png", width=150)
    st.markdown("Qaraa Segmentation App")

    
# Konfigurasi halaman
st.set_page_config(page_title="Customer Segmentation App", layout="wide")
st.set_page_config(
    page_title="Customer Segmentation App",
    page_icon="assets/favicon.png",  # Ganti sesuai path file
    layout="wide"
)
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
            st.markdown(f"📦 Jumlah data awal: **{len(df_raw)}** baris")

        with st.expander("✅ Lihat Data Bersih (Siap Olah)"):
            st.dataframe(df_clean, use_container_width=True, height=400)
            st.markdown(f"🧹 Jumlah data setelah dibersihkan: **{len(df_clean)}** baris")
            st.markdown(f"❌ Data yang dibuang: **{len(df_raw) - len(df_clean)}** baris")


    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.warning("⚠️ Silakan upload file CSV terlebih dahulu.")

# Divider
st.markdown("---")

# Panduan Alur Aplikasi
st.markdown("### 🚀 Alur Analisis:")
st.markdown("""
<ol style='font-size:17px;'>
  <li><b>RFM Analysis</b> – Hitung Recency, Frequency, dan Monetary</li>
  <li><b>Clustering</b> – Segmentasi pelanggan menggunakan K-Means, evaluasi DBI & Silhouette</li>
  <li><b>Customer Segmentation</b> – Tampilkan nama pelanggan, produk, dan segmen berdasarkan perilaku</li>
  <li><b>Dashboard & Insight</b> – Visualisasi dan ringkasan hasil segmentasi</li>
</ol>
""", unsafe_allow_html=True)