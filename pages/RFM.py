import streamlit as st
import pandas as pd
from model import hitung_rfm

st.title("📦 RFM Analysis")

if "data_bersih" not in st.session_state:
    st.warning("Silakan upload data terlebih dahulu di halaman Home.")
    st.stop()

df_clean = st.session_state["data_bersih"]
df_rfm = hitung_rfm(df_clean)

st.success("✅ Data berhasil dihitung RFM-nya.")
st.subheader("📟 Data RFM")
st.dataframe(df_rfm.head(15), use_container_width=True)

st.markdown("---")
st.subheader("⬇️ Unduh Data")
with open("assets/rfm_result.csv", "rb") as f:
    st.download_button("Download RFM (CSV)", f, file_name="rfm_result.csv", mime="text/csv")
with open("assets/data_bersih.csv", "rb") as f:
    st.download_button("Download Data Bersih (CSV)", f, file_name="data_bersih.csv", mime="text/csv")
