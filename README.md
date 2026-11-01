# Form Evaluasi Pembelajaran S1 Sistem Informasi

Aplikasi evaluasi pembelajaran berbasis Streamlit untuk mengumpulkan respon mahasiswa dan menampilkan dashboard laporan admin.

## Fitur
- Form evaluasi mahasiswa
- Dashboard laporan prodi untuk admin
- Laporan komprehensif dengan filter angkatan dan rincian per kelas
- Ringkasan metode pembelajaran, peringkat dosen, Google Meet, dan komentar
- Unduh semua hasil dalam satu ZIP: CSV, PDF, dan gambar grafik PNG
- Penyimpanan otomatis respon ke Google Drive agar tetap tersedia setelah aplikasi Streamlit Cloud dimulai ulang
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
Respon disimpan dan dibaca dari satu file `data_evaluasi.csv` di [folder Google
Drive tujuan](https://drive.google.com/drive/folders/1PQ1Ri52PYbGAlMlKMr0Q0Vad2kEDEL4K).
Dengan demikian, data tidak bergantung pada disk sementara Streamlit Cloud dan
tetap tersedia setelah aplikasi dimulai ulang atau diperbarui.

### Menyiapkan Google Drive
1. Di Google Cloud Console, buat project dan aktifkan **Google Drive API**.
2. Buat **service account**, lalu buat dan unduh key JSON-nya.
3. Buka key JSON, salin nilai `client_email`, lalu bagikan [folder Google
   Drive tujuan](https://drive.google.com/drive/folders/1PQ1Ri52PYbGAlMlKMr0Q0Vad2kEDEL4K)
   sebagai **Editor** ke alamat tersebut.
4. Unggah file `data_evaluasi_template.csv` dari repository ke folder itu dan
   ubah namanya menjadi `data_evaluasi.csv`. Unggah menggunakan akun Google
   Anda; aplikasi akan memperbarui file yang sudah ada.
5. Di **Streamlit Cloud → App settings → Secrets**, pertahankan
   `ADMIN_PASSWORD` yang sudah digunakan dan tambahkan konfigurasi berikut
   dengan seluruh isi JSON key:

```toml
[google_drive]
service_account_json = '''PASTE_SELURUH_ISI_FILE_JSON_SERVICE_ACCOUNT'''
```

Jangan kirim key JSON melalui chat atau commit ke repository. Folder harus
dibagikan hanya ke service account, bukan ke publik. Aplikasi akan menolak
memuat atau menerima respon jika file Drive atau aksesnya belum siap—agar
respon tidak dianggap tersimpan padahal belum tersimpan permanen.

Jika file Drive masih kosong dan terdapat `data_evaluasi.csv` lokal, aplikasi
akan memindahkan respon lokal tersebut ke Drive saat pertama dimuat. File
ekspor lain tidak diimpor otomatis.

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
