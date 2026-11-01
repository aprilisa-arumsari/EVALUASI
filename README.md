# Form Evaluasi Pembelajaran S1 Sistem Informasi

Aplikasi evaluasi pembelajaran berbasis Streamlit untuk mengumpulkan respon mahasiswa dan menampilkan dashboard laporan admin.

## Fitur
- Form evaluasi mahasiswa
- Dashboard laporan prodi untuk admin
- Laporan komprehensif dengan filter angkatan dan rincian per kelas
- Ringkasan metode pembelajaran, peringkat dosen, Google Meet, dan komentar
- Unduh semua hasil dalam satu ZIP: CSV, PDF, dan gambar grafik PNG
- Penyimpanan otomatis respon ke Google Sheets agar tetap tersedia setelah aplikasi Streamlit Cloud dimulai ulang
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
Respon disimpan ke tab `Respon` pada Google Spreadsheet, sehingga tidak
bergantung pada disk sementara Streamlit Cloud dan tetap tersedia setelah
aplikasi dimulai ulang atau diperbarui.

### Menyiapkan Google Sheets
1. Buat Google Spreadsheet baru. Tab pertamanya harus bernama `Respon`.
   Letakkan spreadsheet di folder Drive evaluasi bila diinginkan.
2. Di Google Cloud Console, aktifkan **Google Sheets API** dan buat **service
   account**. Buat key JSON untuk service account tersebut.
3. Buka file JSON, salin alamat `client_email`, lalu bagikan spreadsheet
   sebagai **Editor** kepada alamat tersebut.
4. Salin URL spreadsheet dari browser.
5. Di **Streamlit Cloud → App settings → Secrets**, pertahankan
   `ADMIN_PASSWORD` yang sudah digunakan dan tambahkan konfigurasi berikut.
   Ganti URL contoh dengan URL spreadsheet Anda dan tempel seluruh isi file
   JSON di antara tiga tanda kutip:

```toml
[google_sheets]
spreadsheet_id = "https://docs.google.com/spreadsheets/d/ID_SPREADSHEET_ANDA/edit"
service_account_json = '''PASTE_SELURUH_ISI_FILE_JSON_SERVICE_ACCOUNT'''
```

Spreadsheet dapat dibuat dari akun Google Anda; aplikasi hanya menambahkan
respon pada spreadsheet yang dibagikan. Jangan kirim file JSON/key melalui
chat atau commit ke repository. Aplikasi membuat header tab `Respon` otomatis
jika tab masih kosong. Aplikasi akan menolak memuat atau menerima respon jika
spreadsheet atau aksesnya belum siap—agar respon tidak dianggap tersimpan
padahal belum tersimpan permanen.

Jika spreadsheet masih kosong dan terdapat `data_evaluasi.csv` lokal, aplikasi
akan memindahkan respon lokal tersebut ke spreadsheet saat pertama dimuat.
Untuk mengimpor CSV lama yang tersimpan di Drive, impor CSV itu ke tab `Respon`
sebelum aplikasi pertama kali dijalankan.

Dashboard admin tetap menyediakan tombol **Download Semua Hasil (ZIP)**,
berisi CSV laporan sesuai angkatan, cadangan semua respon, PDF, dan gambar
grafik PNG. Simpan cadangan berkala di lokasi pribadi yang aksesnya dibatasi.
File cadangan dapat berisi masukan mahasiswa; jangan membagikannya secara
publik.

## Akses
Buka URL yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```
