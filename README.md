# Form Evaluasi Pembelajaran S1 Sistem Informasi

Aplikasi evaluasi pembelajaran berbasis Streamlit untuk mengumpulkan respon mahasiswa dan menampilkan dashboard laporan admin.

## Fitur
- Form evaluasi mahasiswa
- Dashboard laporan prodi untuk admin
- Filter kelas
- Export data ke CSV
- Login admin sederhana

## Cara Menjalankan
```bash
pip install streamlit pandas plotly
streamlit run EVALUASI.py
```

## Admin Login
Atur password admin di environment variable berikut:

```bash
set ADMIN_PASSWORD=your_password
```

Untuk Streamlit Cloud, tambahkan secret dengan nama `ADMIN_PASSWORD` di panel Secrets.

## Akses
Buka URL yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```
