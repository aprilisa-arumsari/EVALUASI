# Form Evaluasi Pembelajaran S1 Sistem Informasi

Aplikasi evaluasi pembelajaran berbasis Streamlit untuk mengumpulkan respon mahasiswa dan menampilkan dashboard laporan admin.

## Fitur
- Form evaluasi mahasiswa
- Dashboard laporan prodi untuk admin
- Laporan komprehensif dengan filter angkatan dan rincian per kelas
- Ringkasan metode pembelajaran, peringkat dosen, Google Meet, dan komentar
- Unduh semua hasil dalam satu ZIP: CSV, PDF, dan gambar grafik PNG
- Pulihkan respon dari CSV cadangan atau ZIP hasil unduhan aplikasi
- Penyimpanan respon di CSV lokal dengan unduhan cadangan manual
- Login admin sederhana

## Cara Menjalankan
```bash
pip install -r requirements.txt
streamlit run EVALUASI.py
```

## Admin Login
Atur `ADMIN_PASSWORD` sebagai secret di pengaturan aplikasi Streamlit Cloud,
atau sebagai environment variable saat menjalankan aplikasi sendiri. Gunakan
password acak minimal 16 karakter. Password tidak disimpan di kode dan login
admin tidak akan aktif jika secret belum dikonfigurasi.

Jangan memasukkan password ke repository atau membagikannya melalui chat.

## Penyimpanan dan Cadangan Data
Respon disimpan ke `data_evaluasi.csv` di folder aplikasi. Dashboard admin
menyediakan tombol **Download Semua Hasil (ZIP)** berisi CSV laporan sesuai
angkatan, cadangan semua respon, PDF, dan gambar grafik PNG. Unduhan CSV
cadangan seluruh respon juga tersedia secara terpisah.

Untuk memulihkan data, buka dashboard admin, unggah CSV cadangan atau ZIP
hasil unduhan aplikasi, periksa jumlah respon yang terdeteksi, lalu pilih
**Pulihkan dan Ganti Semua Data**. ZIP harus berisi
`data/Cadangan_Semua_Respon.csv`. Pemulihan mengganti seluruh respon yang saat
ini tersimpan; unduh data saat ini terlebih dahulu jika masih ingin
menyimpannya.

**Penting untuk Streamlit Cloud:** penyimpanan lokal tidak permanen dan dapat
hilang jika aplikasi dimulai ulang atau diperbarui. Karena Anda memilih
mengunduh sendiri, admin perlu sering mengunduh ZIP/CSV dan menyimpan salinannya
di perangkat pribadi. File cadangan dapat berisi masukan mahasiswa; jangan
membagikannya secara publik.

## Akses
Buka URL yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```
