import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel('covid_dataset.xlsx')
    df = df[df['nama_kecamatan'] == 'CEMPAKA PUTIH']
    df = df.pivot_table(index='tanggal', values=['suspek', 'positif', 'discarded'], aggfunc='sum')
    df = df[['suspek', 'positif', 'discarded']]
    return df

df = load_data()

st.header("Kelompok 1 - IF3")
st.write(f"""
    - 10123090 - Raihan Fathir Muhammad
    - 10123091 - Alghifari Raspati
    - 10123115 - Muhammad Favian Jiwani
""")

st.title("Simulasi Jumlah Kasus COVID-19 di Kecamatan Cempaka Putih, Kota Jakarta Pusat Berdasarkan Data Bulan Oktober 2020 dengan Metode Monte Carlo")

tab1, tab2, tab3, tab4 = st.tabs([
    "Pengolahan Data", 
    "Persiapan Monte Carlo", 
    "Simulasi Monte Carlo", 
    "Simulasi Input Pengguna"
])

# Tab 1: Pengolahan Data
with tab1:
    st.header("Pengolahan Data")
    
    # Proses import data
    st.subheader("1. Import Data")
    st.write("Dataset yang digunakan:")
    st.dataframe(pd.read_excel('covid_dataset.xlsx'))
    
    # Proses filter data untuk Kecamatan Cempaka Putih
    st.subheader("2. Filter Data untuk Kecamatan Cempaka Putih")
    st.write("Data setelah difilter untuk Kecamatan Cempaka Putih:")
    st.dataframe(
        pd.read_excel('covid_dataset.xlsx')[
            pd.read_excel('covid_dataset.xlsx')['nama_kecamatan'] == 'CEMPAKA PUTIH'
        ]
    )
    
    # Proses pivot tabel berdasarkan tanggal
    st.subheader("3. Pivot Tabel Berdasarkan Tanggal")
    st.write("Variable yang akan digunakan adalah suspek, positif, dan discarded.")
    st.write("Data setelah dipivot berdasarkan tanggal dan dijumlahkan:")
    
    df = df.reset_index() 
    st.dataframe(df)  


# Tab 2: Tabel Distribusi Frekuensi
with tab2:
    st.header("Persiapan Monte Carlo")
    
    # Fungsi untuk Tabel Suspek
    def tabel_distribusi_frekuensi_suspek(data):
        column_name = 'suspek'
        data = data[column_name].dropna()
        n = len(data)
        min_val = data.min()
        max_val = data.max()
        k = int(1 + 3.3 * np.log10(n) + 1)
        p = int(np.ceil((max_val - min_val) / k))
        
        intervals = []
        b_bawah = min_val
        for i in range(k):
            b_atas = b_bawah + p - 1
            intervals.append((b_bawah, b_atas))
            b_bawah = b_atas + 1
        
        nilai_tengah = [round((b + a) / 2) for b, a in intervals]
        
        frequencies = [
            len(data[(data >= b) & (data <= a)])
            for b, a in intervals
        ]
        
        probabilitas = [round(f / n, 2) for f in frequencies]
        persentase_prob = [round(p * 100) for p in probabilitas]
        
        total = sum(persentase_prob)
        if total != 100:
            diff = 100 - total
            persentase_prob[0] += diff
        
        prob_kumulatif = np.cumsum(probabilitas)
        
        random_number_intervals = []
        batas_bawah = 1
        for persentase in persentase_prob:
            batas_atas = batas_bawah + persentase - 1
            random_number_intervals.append((batas_bawah, batas_atas))
            batas_bawah = batas_atas + 1
        
        frequency_table_data = {
            'No': list(range(1, k + 1)),
            'Interval': [f'{b} - {a}' for b, a in intervals],
            'Nilai Tengah': nilai_tengah,
            'Frekuensi': frequencies,
            'Probabilitas': probabilitas,
            'Probabilitas (%)': persentase_prob,
            'Probabilitas Kumulatif': prob_kumulatif,
            'Interval Angka Acak': [f'{b} - {a}' for b, a in random_number_intervals]
        }
        
        return pd.DataFrame(frequency_table_data)
    
    # Fungsi untuk Tabel Positif
    def tabel_distribusi_frekuensi_positif(data):
        column_name = 'positif'
        data = data[column_name].dropna()
        n = len(data)
        min_val = data.min()
        max_val = data.max()
        k = int(1 + 3.3 * np.log10(n) + 1)
        p = int(np.ceil((max_val - min_val) / k))
        
        intervals = []
        b_bawah = min_val
        for i in range(k):
            b_atas = b_bawah + p - 1
            intervals.append((b_bawah, b_atas))
            b_bawah = b_atas + 1
        
        nilai_tengah = [round((b + a) / 2) for b, a in intervals]
        
        frequencies = [
            len(data[(data >= b) & (data <= a)])
            for b, a in intervals
        ]
        
        probabilitas = [round(f / n, 2) for f in frequencies]
        persentase_prob = [round(p * 100) for p in probabilitas]
        
        total = sum(persentase_prob)
        if total != 100:
            diff = 100 - total
            persentase_prob[0] += diff
        
        prob_kumulatif = np.cumsum(probabilitas)
        
        random_number_intervals = []
        batas_bawah = 1
        for persentase in persentase_prob:
            batas_atas = batas_bawah + persentase - 1
            random_number_intervals.append((batas_bawah, batas_atas))
            batas_bawah = batas_atas + 1
        
        frequency_table_data = {
            'No': list(range(1, k + 1)),
            'Interval': [f'{b} - {a}' for b, a in intervals],
            'Nilai Tengah': nilai_tengah,
            'Frekuensi': frequencies,
            'Probabilitas': probabilitas,
            'Probabilitas (%)': persentase_prob,
            'Probabilitas Kumulatif': prob_kumulatif,
            'Interval Angka Acak': [f'{b} - {a}' for b, a in random_number_intervals]
        }
        
        return pd.DataFrame(frequency_table_data)
    
    # Fungsi untuk Tabel Discarded
    def tabel_distribusi_frekuensi_discarded(data):
        column_name = 'discarded'
        data = data[column_name].dropna()
        n = len(data)
        min_val = data.min()
        max_val = data.max()
        k = int(1 + 3.3 * np.log10(n))
        p = int(np.ceil((max_val - min_val) / k))
        
        intervals = []
        b_bawah = min_val
        for i in range(k):
            b_atas = b_bawah + p - 1
            intervals.append((b_bawah, b_atas))
            b_bawah = b_atas + 1
        
        nilai_tengah = [round((b + a) / 2) for b, a in intervals]
        
        frequencies = [
            len(data[(data >= b) & (data <= a)])
            for b, a in intervals
        ]
        
        probabilitas = [f / n for f in frequencies]
        persentase_prob = [round(p * 100) for p in probabilitas]
        selisih = 100 - sum(persentase_prob)
        persentase_prob[0] += selisih

        total = sum(persentase_prob)
        if total != 100:
            diff = 100 - total
            persentase_prob[0] += diff
        
        prob_kumulatif = np.cumsum(probabilitas)
        
        random_number_intervals = []
        batas_bawah = 1
        for persentase in persentase_prob:
            batas_atas = batas_bawah + persentase - 1
            random_number_intervals.append((batas_bawah, batas_atas))
            batas_bawah = batas_atas + 1
        
        frequency_table_data = {
            'No': list(range(1, k + 1)),
            'Interval': [f'{b} - {a}' for b, a in intervals],
            'Nilai Tengah': nilai_tengah,
            'Frekuensi': frequencies,
            'Probabilitas': [round(p, 2) for p in probabilitas],
            'Probabilitas (%)': persentase_prob,
            'Probabilitas Kumulatif': [round(p, 2) for p in prob_kumulatif],
            'Interval Angka Acak': [f'{b} - {a}' for b, a in random_number_intervals]
        }
        
        return pd.DataFrame(frequency_table_data)
    
    # Tampilkan tabel 
    st.subheader("Tabel Suspek")
    suspek_table = tabel_distribusi_frekuensi_suspek(df)
    st.dataframe(suspek_table)
    
    st.subheader("Tabel Positif")
    positif_table = tabel_distribusi_frekuensi_positif(df)
    st.dataframe(positif_table)
    
    st.subheader("Tabel Discarded")
    discarded_table = tabel_distribusi_frekuensi_discarded(df)
    st.dataframe(discarded_table)

# Tab 3: Simulasi Monte Carlo
with tab3:
    st.header("Simulasi Monte Carlo")
    
    # Buat tabel frekuensi
    suspek_table = tabel_distribusi_frekuensi_suspek(df)
    positif_table = tabel_distribusi_frekuensi_positif(df)
    discarded_table = tabel_distribusi_frekuensi_discarded(df)
    
    # Fungsi untuk mencari nilai tengah berdasarkan angka acak
    def cari_nilai_tengah(angka_acak, tabel_frekuensi):
        for _, baris in tabel_frekuensi.iterrows():
            awal, akhir = map(int, baris['Interval Angka Acak'].split(' - '))
            if awal <= angka_acak <= akhir:
                return baris['Nilai Tengah']
        return None
    
    # Generate angka acak RNG Python
    angka_acak_suspek = random.sample(range(1, 101), 31)
    angka_acak_positif = random.sample(range(1, 101), 31)
    angka_acak_discarded = random.sample(range(1, 101), 31)
    
    # Lakukan simulasi
    simulasi_suspek = [cari_nilai_tengah(i, suspek_table) for i in angka_acak_suspek]
    simulasi_positif = [cari_nilai_tengah(i, positif_table) for i in angka_acak_positif]
    simulasi_discarded = [cari_nilai_tengah(i, discarded_table) for i in angka_acak_discarded]
    
    # Buat dataframe hasil
    hasil_simulasi = pd.DataFrame({
        'Hari': range(1, 32),
        'Angka Acak Suspek': angka_acak_suspek,
        'Angka Acak Positif': angka_acak_positif,
        'Angka Acak Discarded': angka_acak_discarded,
        'Simulasi Suspek': simulasi_suspek,
        'Simulasi Positif': simulasi_positif,
        'Simulasi Discarded': simulasi_discarded
    })
    
    hasil_simulasi['Kasus Aktif'] = hasil_simulasi['Simulasi Suspek'] - (hasil_simulasi['Simulasi Positif'] + hasil_simulasi['Simulasi Discarded'])
    hasil_simulasi['Tingkat Positif'] = ((hasil_simulasi['Simulasi Positif'] / hasil_simulasi['Simulasi Suspek']) * 100).round().astype(int).astype(str) + '%'
    
    st.subheader("Hasil Simulasi Monte Carlo")
    st.dataframe(hasil_simulasi)
    
    # Visualisasi
    st.subheader("Visualisasi Hasil Simulasi")

    # Suspek
    st.subheader("Suspek (Simulasi)")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(hasil_simulasi['Hari'], hasil_simulasi['Simulasi Suspek'], 'b-', marker='o')
    ax1.set_title('Suspek (Simulasi)')
    ax1.set_xlabel('Hari')
    ax1.set_ylabel('Suspek')
    ax1.grid(True)
    st.pyplot(fig1)

    # Positif
    st.subheader("Positif (Simulasi)")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(hasil_simulasi['Hari'], hasil_simulasi['Simulasi Positif'], 'r-', marker='o')
    ax2.set_title('Positif (Simulasi)')
    ax2.set_xlabel('Hari')
    ax2.set_ylabel('Positif')
    ax2.grid(True)
    st.pyplot(fig2)

    # Discarded
    st.subheader("Discarded (Simulasi)")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(hasil_simulasi['Hari'], hasil_simulasi['Simulasi Discarded'], 'c-', marker='o')
    ax3.set_title('Discarded (Simulasi)')
    ax3.set_xlabel('Hari')
    ax3.set_ylabel('Discarded')
    ax3.grid(True)
    st.pyplot(fig3)

    # Kasus Aktif
    st.subheader("Kasus Aktif (Simulasi)")
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.plot(hasil_simulasi['Hari'], hasil_simulasi['Kasus Aktif'], 'm-', marker='o')
    ax4.set_title('Kasus Aktif (Simulasi)')
    ax4.set_xlabel('Hari')
    ax4.set_ylabel('Kasus Aktif')
    ax4.grid(True)
    st.pyplot(fig4)

    # Tingkat Positif
    st.subheader("Tingkat Positif (Simulasi)")
    fig5, ax5 = plt.subplots(figsize=(5, 3))
    ax5.plot(hasil_simulasi['Hari'], [float(x.strip('%')) for x in hasil_simulasi['Tingkat Positif']], 'g-', marker='o')
    ax5.set_title('Tingkat Positif (Simulasi)')
    ax5.set_xlabel('Hari')
    ax5.set_ylabel('Tingkat Positif (%)')
    ax5.grid(True)
    st.pyplot(fig5)



# Tab 4: Simulasi Input Pengguna
with tab4:
    st.header("Simulasi dari Input Pengguna")
    
    st.subheader("Simulasi Jumlah Kasus COVID-19 Berdasarkan Input Pengguna")
    jumlah_hari = st.number_input("Jumlah Hari untuk Disimulasikan", min_value=1, max_value=100, value=31)
    
    if st.button("Jalankan Simulasi"):
        random.seed(42)
        
        # Generate angka acak berdasarkan input pengguna
        angka_acak_suspek_user = random.sample(range(1, 101), jumlah_hari)
        angka_acak_positif_user = random.sample(range(1, 101), jumlah_hari)
        angka_acak_discarded_user = random.sample(range(1, 101), jumlah_hari)
        
        # Lakukan simulasi
        simulasi_suspek_user = [cari_nilai_tengah(i, suspek_table) for i in angka_acak_suspek_user]
        simulasi_positif_user = [cari_nilai_tengah(i, positif_table) for i in angka_acak_positif_user]
        simulasi_discarded_user = [cari_nilai_tengah(i, discarded_table) for i in angka_acak_discarded_user]
        
        # Buat dataframe hasil
        hasil_simulasi_user = pd.DataFrame({
            'Hari': range(1, jumlah_hari + 1),
            'Angka Acak Suspek': angka_acak_suspek_user,
            'Angka Acak Positif': angka_acak_positif_user,
            'Angka Acak Discarded': angka_acak_discarded_user,
            'Simulasi Suspek': simulasi_suspek_user,
            'Simulasi Positif': simulasi_positif_user,
            'Simulasi Discarded': simulasi_discarded_user
        })
        
        hasil_simulasi_user['Kasus Aktif'] = hasil_simulasi_user['Simulasi Suspek'] - (hasil_simulasi_user['Simulasi Positif'] + hasil_simulasi_user['Simulasi Discarded'])
        hasil_simulasi_user['Tingkat Positif'] = ((hasil_simulasi_user['Simulasi Positif'] / hasil_simulasi_user['Simulasi Suspek']) * 100).round().astype(int).astype(str) + '%'
        
        st.subheader("Hasil Simulasi")
        st.dataframe(hasil_simulasi_user)
        
        # Visualisasi
        st.subheader("Visualisasi Hasil Simulasi")

        # Suspek
        st.subheader("Suspek (Simulasi)")
        fig1, ax1 = plt.subplots()
        ax1.plot(hasil_simulasi['Hari'], hasil_simulasi['Simulasi Suspek'], 'b-', marker='o')
        ax1.set_title('Suspek (Simulasi)')
        ax1.set_xlabel('Hari')
        ax1.set_ylabel('Suspek')
        ax1.grid(True)
        st.pyplot(fig1)

        # Positif
        st.subheader("Positif (Simulasi)")
        fig2, ax2 = plt.subplots()
        ax2.plot(hasil_simulasi['Hari'], hasil_simulasi['Simulasi Positif'], 'r-', marker='o')
        ax2.set_title('Positif (Simulasi)')
        ax2.set_xlabel('Hari')
        ax2.set_ylabel('Positif')
        ax2.grid(True)
        st.pyplot(fig2)

        # Discarded
        st.subheader("Discarded (Simulasi)")
        fig3, ax3 = plt.subplots()
        ax3.plot(hasil_simulasi['Hari'], hasil_simulasi['Simulasi Discarded'], 'c-', marker='o')
        ax3.set_title('Discarded (Simulasi)')
        ax3.set_xlabel('Hari')
        ax3.set_ylabel('Discarded')
        ax3.grid(True)
        st.pyplot(fig3)

        # Kasus Aktif
        st.subheader("Kasus Aktif (Simulasi)")
        fig4, ax4 = plt.subplots()
        ax4.plot(hasil_simulasi['Hari'], hasil_simulasi['Kasus Aktif'], 'm-', marker='o')
        ax4.set_title('Kasus Aktif (Simulasi)')
        ax4.set_xlabel('Hari')
        ax4.set_ylabel('Kasus Aktif')
        ax4.grid(True)
        st.pyplot(fig4)

        # Tingkat Positif
        st.subheader("Tingkat Positif (Simulasi)")
        fig5, ax5 = plt.subplots()
        ax5.plot(hasil_simulasi['Hari'], [float(x.strip('%')) for x in hasil_simulasi['Tingkat Positif']], 'g-', marker='o')
        ax5.set_title('Tingkat Positif (Simulasi)')
        ax5.set_xlabel('Hari')
        ax5.set_ylabel('Tingkat Positif (%)')
        ax5.grid(True)
        st.pyplot(fig5)