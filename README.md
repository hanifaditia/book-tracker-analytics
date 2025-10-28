# 📚 Dashboard Analisis Buku

Proyek analisis data yang mensimulasikan dan memvisualisasikan perilaku membaca pengguna.  
Proyek ini terdiri dari proses lengkap **ETL (Extract, Transform, Load)** serta **dashboard** menggunakan Streamlit dan Plotly.

---

## Gambaran Umum

Proyek ini menunjukkan alur kerja analisis data dari awal hingga akhir untuk memahami perilaku membaca buku:

1. **Ekstraksi & Transformasi Data (ETL)**  
   Membersihkan data buku mentah dari format JSON, mensimulasikan interaksi pengguna, dan menghasilkan berbagai dataset analisis.

2. **Visualisasi Dashboard**  
   Menggunakan Streamlit dan Plotly untuk menampilkan wawasan interaktif mengenai genre buku, progres membaca, tren aktivitas, dan segmentasi pembaca.

---

## Persyaratan

Sebelum menjalankan python, pastikan semua dependensi sudah terpasang:

```bash
pip install -r requirements.txt
```

---

## Cara Menjalankan

### 1. Jalankan Script ETL

Script ini akan membersihkan data mentah, mensimulasikan interaksi pengguna, dan menyimpan hasil olahan ke folder `data/processed`.

```bash
python data_preparation.py
```

```bash
python sample_data_generator.py
```

### 2. Jalankan Dashboard

Setelah data siap, jalankan dashboard Streamlit dengan perintah berikut:

```bash
streamlit run dashboard.py
```

## Pengembangan Selanjutnya

- Menambahkan integrasi data nyata
- Meningkatkan segmentasi pembaca dengan algoritma clustering
- Menyimpan data ke dalam database (PostgreSQL atau SQLite)

---
