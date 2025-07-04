import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score
import os

# Judul halaman
st.title("Customer Segmentation - KMeans Clustering")

# Upload file CSV
uploaded_file = st.file_uploader("Upload file CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Bersihkan kolom Price
    df['Price_clean'] = (
        df['Price']
        .str.replace('Rp', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )
    df['Price_clean'] = pd.to_numeric(df['Price_clean'], errors='coerce')

    # Isi Order_id kosong
    df['Order_id'] = df['Order_id'].fillna(method='ffill')
    for i in range(len(df)):
        if pd.isna(df.loc[i, 'Order_id']):
            df.loc[i, 'Order_id'] = f"Missing-{i}"

    # Hapus baris kosong
    df_clean = df.dropna(subset=['Customer_id', 'Order_date', 'Price_clean']).copy()

    # Hitung total transaksi
    df_clean['Total_Transaksi'] = df_clean['Quantity'] * df_clean['Price_clean']
    df_clean = df_clean[df_clean['Total_Transaksi'] > 0]

    # Format tanggal
    df_clean['Order_date'] = pd.to_datetime(df_clean['Order_date'], errors='coerce')

    # RFM
    ref_date = df_clean['Order_date'].max()
    df_agg = df_clean.groupby('Customer_id').agg({
        'Order_id': 'count',
        'Total_Transaksi': 'sum',
        'Order_date': 'max'
    }).reset_index()

    df_agg.rename(columns={
        'Order_id': 'Frequency',
        'Order_date': 'Last_Order_Date'
    }, inplace=True)

    df_agg['Recency'] = (ref_date - df_agg['Last_Order_Date']).dt.days
    df_agg['Avg_Transaction'] = (df_agg['Total_Transaksi'] / df_agg['Frequency']).fillna(0).round(0).astype(int)

    # Standarisasi
    features = df_agg[['Frequency', 'Total_Transaksi', 'Recency', 'Avg_Transaction']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Slider jumlah cluster
    k = st.slider("Pilih jumlah cluster", min_value=2, max_value=10, value=4)

    # KMeans
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_agg['Cluster'] = kmeans.fit_predict(X_scaled)
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)

    st.subheader("Hasil Clustering")
    st.dataframe(df_agg.head())

    # Visualisasi scatter plot
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df_agg,
        x='Total_Transaksi',
        y='Avg_Transaction',
        hue='Cluster',
        palette='tab10',
        s=100,
        ax=ax1
    )
    ax1.scatter(
        centroids[:, 1],
        centroids[:, 3],
        marker='X',
        s=200,
        color='black',
        label='Centroids'
    )
    ax1.set_title('Cluster Pelanggan')
    ax1.set_xlabel('Total Transaksi (Rp)')
    ax1.set_ylabel('Rata-rata Transaksi (Rp)')
    ax1.legend()
    st.pyplot(fig1)

    # Centroid table
    centroid_df = pd.DataFrame({
        'Cluster': list(range(k)),
        'Frequency': centroids[:, 0],
        'Total_Transaksi': centroids[:, 1],
        'Recency': centroids[:, 2],
        'Avg_Transaction': centroids[:, 3]
    })
    st.subheader("Centroid dari Setiap Cluster")
    st.dataframe(centroid_df.round(2))

    # Evaluasi DBI & Silhouette
    db_index = davies_bouldin_score(X_scaled, df_agg['Cluster'])
    sil_score = silhouette_score(X_scaled, df_agg['Cluster'])
    st.markdown(f"**Davies-Bouldin Index:** {db_index:.4f}")
    st.markdown(f"**Silhouette Score:** {sil_score:.4f}")

    # Rekomendasi produk terakhir dari pelanggan bernilai tinggi
    high_value_clusters = st.multiselect(
        "Pilih Cluster Bernilai Tinggi",
        options=df_agg['Cluster'].unique().tolist(),
        default=[0]
    )

    df_high_value = df_agg[df_agg['Cluster'].isin(high_value_clusters)].copy()
    df_merged = df_clean.merge(df_high_value[['Customer_id', 'Cluster']], on='Customer_id', how='inner')
    df_latest_orders = df_merged.sort_values('Order_date').groupby('Customer_id').tail(1)
    df_latest_orders['Order_date'] = df_latest_orders['Order_date'].dt.strftime('%d %B %Y')
    df_latest_orders['Total_Transaksi'] = df_latest_orders['Total_Transaksi'].apply(lambda x: f"Rp {x:,.0f}")
    st.subheader("Pelanggan Bernilai Tinggi - Transaksi Terakhir")
    st.dataframe(df_latest_orders[['Customer_id', 'Cluster', 'Order_date', 'Total_Transaksi']])
else:
    st.warning("Silakan upload file CSV terlebih dahulu.")
