# Form Evaluasi Pembelajaran S1 Sistem Informasi

Aplikasi evaluasi pembelajaran berbasis Streamlit untuk mengumpulkan respon mahasiswa dan menampilkan dashboard laporan admin.

## Fitur
- Form evaluasi mahasiswa
- Dashboard laporan prodi untuk admin
- Laporan komprehensif dengan filter angkatan dan rincian per kelas
- Ringkasan metode pembelajaran, peringkat dosen, Google Meet, dan komentar
- Export laporan angkatan ke CSV dan PDF
- Penyimpanan otomatis respon ke Supabase
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
Respon baru disimpan otomatis di Supabase dan dimuat dari database untuk
dashboard. Untuk menyiapkan tabel:

1. Buat project di Supabase.
2. Buka **SQL Editor → New query**, salin isi [`supabase_setup.sql`](./supabase_setup.sql),
   lalu jalankan query.
3. Di **Streamlit Cloud → App settings → Secrets**, tambahkan konfigurasi
   berikut. Masukkan URL project dan `service_role` key dari Supabase sendiri:

```toml
ADMIN_PASSWORD = "isi-sendiri-dengan-password-kuat"

[supabase]
url = "https://PROJECT_REF.supabase.co"
service_role_key = "isi-sendiri-dengan-service-role-key"
```

4. Simpan Secrets, lalu reboot aplikasi Streamlit.

Jangan membagikan atau memasukkan `service_role` key ke repository. Gunakan
hanya di Secrets server-side Streamlit. Skrip SQL mengaktifkan RLS dan tidak
memberikan akses tabel kepada `anon` atau `authenticated`; aplikasi memakai
`service_role` hanya dari Secrets server-side. Aplikasi berhenti dengan pesan
error jika Supabase belum dikonfigurasi atau database tidak dapat diakses, dan
tidak akan mengonfirmasi respon berhasil sebelum penyimpanan selesai.

Data lama tidak diimpor otomatis; migrasi dimulai dari respon baru. Tombol
**Cadangan Semua Data (CSV)** tetap tersedia untuk mengunduh salinan berkala.
Simpan CSV di lokasi pribadi yang aksesnya dibatasi karena dapat berisi
masukan mahasiswa.
## Akses
Buka URL yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```
