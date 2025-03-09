import streamlit as st
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")

file_path = os.path.abspath("day.csv")
day_df = pd.read_csv(file_path)

day_df["year"] = day_df["yr"].apply(lambda x: 2011 if x == 0 else 2012)
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_df["season_name"] = day_df["season"].map(season_map)
month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
             7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
day_df["month_name"] = day_df["mnth"].map(month_map)

st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        color: #2c3e50;
        font-weight: bold;
    }
    .conclusion-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .highlight {
        font-size: 18px;
        color: #2980b9;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔍 Navigasi")
    page = st.radio("Pilih Halaman:", ["Tren Penyewaan Sepeda", "Penyewaan Berdasarkan Musim", "Kesimpulan"],
                    label_visibility="collapsed")

    st.markdown("<div style='padding-bottom: 200px;'></div>",
                unsafe_allow_html=True)

    st.markdown("""
        <p style='font-size: 14px; color: #7f8c8d;'>Evelyn Eunike Aritonang<br>MC189D5X1561</p>
    """, unsafe_allow_html=True)

# Halaman Dashboard Utama (Diperbaiki sesuai Notebook)
if page == "Tren Penyewaan Sepeda":
    st.markdown('<p class="main-title">📊 Bike Sharing Dashboard</p>',
                unsafe_allow_html=True)

    # Filter Tahun
    year_selected = st.selectbox("Pilih Tahun untuk Filter", [
                                 2011, 2012, "Kedua Tahun"], key="main_year")

    if year_selected == "Kedua Tahun":
        df_filtered = day_df
    else:
        df_filtered = day_df[day_df["year"] == year_selected]

    # Visualisasi Tren Bulanan seperti di Notebook
    st.subheader("📈 Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
    monthly_trend = df_filtered.groupby(["year", "mnth"])[
        "cnt"].sum().unstack(level=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_trend.plot(ax=ax, marker="o", linewidth=2)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May",
                       "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Penyewaan")
    ax.set_title("Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
    ax.legend(title="Tahun", labels=["2011", "2012"])
    ax.grid(True)
    # Format angka pada sumbu Y agar lebih rapi (misalnya menggunakan koma)
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    st.pyplot(fig)

elif page == "Penyewaan Berdasarkan Musim":
    st.markdown('<p class="main-title">🌦 Penyewaan Sepeda Berdasarkan Musim</p>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        year_selected = st.selectbox(
            "Pilih Tahun", [2011, 2012], key="season_year")
    with col2:
        season_selected = st.multiselect("Pilih Musim", options=["Spring", "Summer", "Fall", "Winter"],
                                         default=["Spring", "Summer", "Fall", "Winter"])

    df_filtered = day_df[(day_df["year"] == year_selected) & (
        day_df["season_name"].isin(season_selected))]

    st.subheader(f"📊 Penyewaan per Musim ({year_selected})")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x="season_name", y="cnt",
                data=df_filtered, palette="viridis", ax=ax)
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xlabel("Musim")
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10)
    st.pyplot(fig)

    st.subheader("🥧 Persentase Penyewaan per Musim")
    pie_data = df_filtered.groupby("season_name")["cnt"].sum()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%',
           startangle=90, colors=sns.color_palette("pastel"))
    ax.axis('equal')
    st.pyplot(fig)

elif page == "Kesimpulan":
    st.markdown('<p class="main-title">✨ Kesimpulan:</p>',
                unsafe_allow_html=True)

    st.markdown("""
        <div class='conclusion-box'>
            <h3 style='color: #2c3e50;'>Apa yang Kita Pelajari?</h3>
            <p>Data penyewaan sepeda dari 2011 hingga 2012 memberikan wawasan menarik tentang pola penggunaan sepeda. Berikut adalah poin-poin utama yang bisa kita simpulkan:</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div class='conclusion-box'>
                <p><span class='highlight'>1. Tren Tahunan:</span> Penyewaan sepeda meningkat signifikan dari tahun 2011 ke 2012, menunjukkan popularitas yang terus bertambah.</p>
                <p><span class='highlight'>2. Musim Favorit:</span> Musim <b>Fall</b> menjadi periode dengan penyewaan tertinggi, diikuti oleh <b>Summer</b>. Spring cenderung lebih sepi.</p>
                <p><span class='highlight'>3. Bulan Puncak:</span> Bulan <b>Agustus 2011</b> dan <b>September 2012</b> sering menjadi puncak penyewaan, mungkin karena cuaca yang mendukung.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🚴 Total Penyewaan per Tahun")
        total_per_year = day_df.groupby("year")["cnt"].sum()
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(total_per_year, labels=total_per_year.index, autopct='%1.1f%%',
               colors=['#3498db', '#e74c3c'], startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    with st.expander("🔍 Insight Lebih Lanjut", expanded=True):
        st.markdown("""
            - **Cuaca Berpengaruh Besar:** Hari-hari dengan cuaca cerah (dari kolom `weathersit`) memiliki penyewaan jauh lebih tinggi dibandingkan hari hujan.
            - **Potensi Bisnis:** Fokus pada musim Fall dan Summer untuk promosi atau penambahan sepeda.
        """)

    st.markdown("""
        <div class='conclusion-box' style='text-align: center;'>
            <h4 style='color: #2c3e50;'>Kesimpulan Akhir</h4>
            <p>Pada analisis saya, Penyewaan sepeda sangat dipengaruhi oleh kondisi <b>cuaca</b> dan <b>musim</b> . Cuaca cerah (dari kolom `weathersit`) memiliki penyewaan jauh lebih tinggi dibandingkan hari hujan.Musim Fall (gugur) diikuti oleh Summer (Panas) juga menjadi musim dengan penyewaan sepeda tertinggi.</p>
        </div>
    """, unsafe_allow_html=True)
