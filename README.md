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
pip install -r requirements.txt
streamlit run EVALUASI.py
```

## Penyimpanan Respon di GitHub

Respon disimpan otomatis sebagai `data_evaluasi.csv` melalui GitHub Contents API
dan dimuat kembali saat aplikasi dijalankan. Gunakan repository **private** khusus
untuk data respon; jangan arahkan penyimpanan ke repository kode yang publik.
Aplikasi menolak menyimpan data jika repository yang dikonfigurasi bersifat publik.

1. Buat repository GitHub private untuk data, misalnya `evaluasi-data`, dan
   inisialisasi dengan README pada branch `main`.
2. Buat fine-grained personal access token yang hanya diberi akses ke repository
   tersebut, dengan izin **Contents: Read and write**.
3. Di Streamlit Community Cloud, buka **App settings → Secrets** dan tambahkan:

   ```toml
   GITHUB_TOKEN = "token-anda"
   GITHUB_REPOSITORY = "aprilisa-arumsari/evaluasi-data"
   GITHUB_BRANCH = "main"
   GITHUB_DATA_FILE = "data_evaluasi.csv"
   ```

Token hanya disimpan di Secrets, jangan ditulis di kode atau commit ke Git.
Setelah menyimpan Secrets, restart aplikasi. Jika penyimpanan gagal, aplikasi
menampilkan error dan tidak melaporkan respon sebagai berhasil tersimpan.

Jika file GitHub masih kosong, admin dapat memulihkan CSV ekspor dari dashboard.
Pemulihan hanya menerima CSV dengan kolom `Timestamp`, `Kelas`,
`Harapan Semester Depan`, dan `Catatan Permasalahan`. Isian lain disimpan kosong
dan setiap baris ditandai sebagai arsip parsial; data tersebut tidak dapat
merekonstruksi jawaban yang tidak ada di ekspor.

## Admin Login
Password default: `aprilcantik`

## Akses
Buka URL yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```
