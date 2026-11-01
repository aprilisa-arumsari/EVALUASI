# Form Evaluasi Pembelajaran S1 Sistem Informasi

Aplikasi evaluasi pembelajaran berbasis Streamlit untuk mengumpulkan respon mahasiswa dan menampilkan dashboard laporan admin.

## Fitur
- Form evaluasi mahasiswa
- Dashboard laporan prodi untuk admin
- Laporan komprehensif dengan filter angkatan dan rincian per kelas
- Ringkasan metode pembelajaran, peringkat dosen, Google Meet, dan komentar
- Export laporan angkatan ke CSV dan PDF
- Login admin sederhana

## Cara Menjalankan
```bash
pip install streamlit pandas plotly
streamlit run EVALUASI.py
```

## Admin Login
Atur `ADMIN_PASSWORD` sebagai secret di pengaturan aplikasi Streamlit Cloud,
atau sebagai environment variable saat menjalankan aplikasi sendiri. Gunakan
password acak minimal 16 karakter. Password tidak disimpan di kode dan login
admin tidak akan aktif jika secret belum dikonfigurasi.

Jangan memasukkan password ke repository atau membagikannya melalui chat.

## Penyimpanan dan Cadangan Data
Respon disimpan pada file `data_evaluasi.csv` di folder aplikasi. Pada Streamlit
Cloud, file lokal dapat hilang saat aplikasi dimulai ulang atau diperbarui.
Karena itu, admin perlu mengunduh **Cadangan Semua Data (CSV)** minimal setiap
hari saat survei aktif dan sebelum aplikasi diperbarui, lalu menyimpannya di
lokasi pribadi yang aksesnya dibatasi.

Tombol cadangan mencakup semua respon, terlepas dari filter angkatan laporan.
File CSV dapat berisi masukan mahasiswa, jadi jangan membagikannya secara
publik. Unduhan ini adalah cadangan manual; data tidak otomatis tersimpan di
penyimpanan permanen.
## Akses
Buka URL yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```
