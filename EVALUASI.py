import os

import streamlit as st
import pandas as pd
import plotly.express as px

# Config Halaman
st.set_page_config(
    page_title="Form Evaluasi Pembelajaran S1 Sistem Informasi UDBS",
    page_icon="📋",
    layout="wide"
)

# Password Admin
PASSWORD_ADMIN = os.getenv("ADMIN_PASSWORD") or st.secrets.get("ADMIN_PASSWORD", "aprilcantik")

# Database Pemetaan Kelas -> Mata Kuliah & Dosen Pengampu dari Jadwal Kuliah FIK UDBS
DATA_KELAS_JADWAL = {
    "SI 26A1": [
        {"matkul": "Pengantar Teknologi Informasi", "dosen": "Moh. Muhtarom, SE, S.Kom., M.Kom"},
        {"matkul": "Sistem Operasi", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Bahasa Inggris I", "dosen": "Marginingsih, S.Pd., M.Pd"},
        {"matkul": "Matematika Dasar", "dosen": "Herliyani Hasanah, S.T., M.T"},
        {"matkul": "Konsep Sistem Informasi", "dosen": "Sri Sumarlinda, M.Kom., PhD"},
        {"matkul": "Sistem Informasi Manajemen", "dosen": "Agustina Srirahayu, S.Kom., M.Kom"},
        {"matkul": "Algoritma dan Struktur Data", "dosen": "Pipin Widyaningsih, S.Kom., M.Kom"},
        {"matkul": "Dasar Pemrograman", "dosen": "Triyono, M.Kom"}
    ],
    "SI 26A2": [
        {"matkul": "Sistem Operasi", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Pengantar Teknologi Informasi", "dosen": "Moh. Muhtarom, SE, S.Kom., M.Kom"},
        {"matkul": "Bahasa Inggris I", "dosen": "Marginingsih, S.Pd., M.Pd"},
        {"matkul": "Sistem Informasi Manajemen", "dosen": "Agustina Srirahayu, S.Kom., M.Kom"},
        {"matkul": "Matematika Dasar", "dosen": "Herliyani Hasanah, S.T., M.T"},
        {"matkul": "Konsep Sistem Informasi", "dosen": "Sri Sumarlinda, M.Kom., PhD"},
        {"matkul": "Algoritma dan Struktur Data", "dosen": "Pipin Widyaningsih, S.Kom., M.Kom"},
        {"matkul": "Dasar Pemrograman", "dosen": "Sopingi, S.Kom., M.Kom"}
    ],
    "SI 25A1": [
        {"matkul": "Sistem Basis Data", "dosen": "Hanifah Permatasari, M.Kom"},
        {"matkul": "Statistika dan Probabilitas", "dosen": "Ratna Puspita Indah, S.Si, M.Pd"},
        {"matkul": "Pemrograman Berorientasi Objek", "dosen": "Sopingi, S.Kom., M.Kom"},
        {"matkul": "Desain & Manajemen Jaringan Komputer", "dosen": "Eko Purwanto, M.Kom., Ph.D"},
        {"matkul": "Manajemen Sains", "dosen": "Wiji Lestari, S.Si., M.Kom"},
        {"matkul": "Arsitektur Perusahaan", "dosen": "Intan Oktaviani, M.Kom"},
        {"matkul": "Bahasa Inggris III", "dosen": "Anindhiasti Ayu K, S.Pd, M.Pd"},
        {"matkul": "Metodologi Penelitian dan Penulisan Ilmiah", "dosen": "Vihi Atina, S.Kom., M.Kom"}
    ],
    "SI 25A2": [
        {"matkul": "Statistika dan Probabilitas", "dosen": "Ratna Puspita Indah, S.Si, M.Pd"},
        {"matkul": "Sistem Basis Data", "dosen": "Hanifah Permatasari, M.Kom"},
        {"matkul": "Desain & Manajemen Jaringan Komputer", "dosen": "Eko Purwanto, M.Kom., Ph.D"},
        {"matkul": "Pemrograman Berorientasi Objek", "dosen": "Sopingi, S.Kom., M.Kom"},
        {"matkul": "Manajemen Sains", "dosen": "Ahmad Rifai, S.Kom., M.Kom"},
        {"matkul": "Arsitektur Perusahaan", "dosen": "Intan Oktaviani, M.Kom"},
        {"matkul": "Bahasa Inggris III", "dosen": "Anindhiasti Ayu K, S.Pd, M.Pd"},
        {"matkul": "Metodologi Penelitian dan Penulisan Ilmiah", "dosen": "Vihi Atina, S.Kom., M.Kom"}
    ],
    "SI 25A3": [
        {"matkul": "Desain & Manajemen Jaringan Komputer", "dosen": "Eko Purwanto, M.Kom., Ph.D"},
        {"matkul": "Manajemen Sains", "dosen": "Ahmad Rifai, S.Kom., M.Kom"},
        {"matkul": "Pemrograman Berorientasi Objek", "dosen": "Sopingi, S.Kom., M.Kom"},
        {"matkul": "Sistem Basis Data", "dosen": "Pipin Widyaningsih, S.Kom., M.Kom"},
        {"matkul": "Statistika dan Probabilitas", "dosen": "Ratna Puspita Indah, S.Si, M.Pd"},
        {"matkul": "Arsitektur Perusahaan", "dosen": "Intan Oktaviani, M.Kom"},
        {"matkul": "Metodologi Penelitian dan Penulisan Ilmiah", "dosen": "Vihi Atina, S.Kom., M.Kom"},
        {"matkul": "Bahasa Inggris III", "dosen": "Anindhiasti Ayu K, S.Pd, M.Pd"}
    ],
    "SI 24A1": [
        {"matkul": "Proyek Sistem Aplikasi", "dosen": "Marta Ardiyanto, M.Kom"},
        {"matkul": "Manajemen Proyek Sistem Informasi", "dosen": "Wijiyanto, S.Kom., M.Pd., M.Kom"},
        {"matkul": "Tata Kelola TI", "dosen": "Herin Dwibima Aprianto, M.Kom"},
        {"matkul": "Interaksi Manusia dan Komputer", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Agama", "dosen": "Dr. Nur Hadi, S.Pd.I., M.Ag"},
        {"matkul": "Pancasila", "dosen": "Widi Nugrahaningsih, SH.,MH"},
        {"matkul": "Kewarganegaraan", "dosen": "Peter Guntara, SH.,MH.Li"},
        {"matkul": "Inovasi dan Kreatifitas", "dosen": "Hanifah Permatasari, M.Kom"},
        {"matkul": "Bahasa Indonesia", "dosen": "Margaretha Evi Yuliana, S.S.,M.Si"}
    ],
    "SI 24A2": [
        {"matkul": "Tata Kelola TI", "dosen": "Lubna, M.Kom"},
        {"matkul": "Proyek Sistem Aplikasi", "dosen": "Marta Ardiyanto, M.Kom"},
        {"matkul": "Manajemen Proyek Sistem Informasi", "dosen": "Sri Sumarlinda, S.Kom., M.Kom., PhD"},
        {"matkul": "Interaksi Manusia dan Komputer", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Agama", "dosen": "Dr. Nur Hadi, S.Pd.I., M.Ag"},
        {"matkul": "Pancasila", "dosen": "Widi Nugrahaningsih, SH.,MH"},
        {"matkul": "Kewarganegaraan", "dosen": "Peter Guntara, SH.,MH.Li"},
        {"matkul": "Inovasi dan Kreatifitas", "dosen": "Hanifah Permatasari, M.Kom"},
        {"matkul": "Bahasa Indonesia", "dosen": "Margaretha Evi Yuliana, S.S.,M.Si"}
    ],
    "SI 24A3": [
        {"matkul": "Manajemen Proyek Sistem Informasi", "dosen": "Dr. Wijiyanto, S.Kom., M.Pd., M.Kom"},
        {"matkul": "Tata Kelola TI", "dosen": "Lubna, M.Kom"},
        {"matkul": "Proyek Sistem Aplikasi", "dosen": "Marta Ardiyanto, M.Kom"},
        {"matkul": "Interaksi Manusia dan Komputer", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Agama", "dosen": "Dr. Nur Hadi, S.Pd.I., M.Ag"},
        {"matkul": "Pancasila", "dosen": "Widi Nugrahaningsih, SH.,MH"},
        {"matkul": "Kewarganegaraan", "dosen": "Dr. Hery Dwi Utomo, SH.,MH"},
        {"matkul": "Inovasi dan Kreatifitas", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Bahasa Indonesia", "dosen": "Margaretha Evi Yuliana, S.S.,M.Si"}
    ],
    "SI 23A1": [
        {"matkul": "Pengembangan Data", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Audit SI", "dosen": "Ridwan Dwi Irawan, M.Kom"},
        {"matkul": "Manajemen Hubungan Pelanggan", "dosen": "Hanifah Permatasari, M.Kom"}
    ],
    "SI 23A2": [
        {"matkul": "Pengembangan Data", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Audit SI", "dosen": "Ridwan Dwi Irawan, M.Kom"},
        {"matkul": "Manajemen Hubungan Pelanggan", "dosen": "Hanifah Permatasari, M.Kom"}
    ],
    "SI 26B1": [
        {"matkul": "Algoritma dan Struktur Data", "dosen": "Eko Purwanto, M.Kom., Ph.D"},
        {"matkul": "Pengantar Teknologi Informasi", "dosen": "Moh. Muhtarom, SE, S.Kom., M.Kom"},
        {"matkul": "Konsep Sistem Informasi", "dosen": "Dery Hartoro, S.T., M.Hum"},
        {"matkul": "Sistem Informasi Manajemen", "dosen": "Muslim Heri K, M.Kom"},
        {"matkul": "Sistem Operasi", "dosen": "Bondan Wahyu Pamekas, M.Kom"},
        {"matkul": "Bahasa Inggris I", "dosen": "Aris Hidayatulloh, S.Hum, M.A"},
        {"matkul": "Dasar Pemrograman", "dosen": "Sopingi, S.Kom., M.Kom"},
        {"matkul": "Matematika Dasar", "dosen": "Arif Setiawan, S.Si, MT"}
    ],
    "SI 25B1": [
        {"matkul": "Bahasa Inggris III", "dosen": "Aris Hidayatulloh, S.Hum, M.A"},
        {"matkul": "Statistika dan Probabilitas", "dosen": "Nurmalitasari, S.Si., M.Pd, Ph.D"},
        {"matkul": "Sistem Basis Data", "dosen": "Muslim Heri K, M.Kom"},
        {"matkul": "Arsitektur Perusahaan", "dosen": "Herin Dwibima Aprianto, M.Kom"},
        {"matkul": "Desain & Manajemen Jaringan Komputer", "dosen": "Andi Novianto, S.Kom., M.Hum., M.Kom"},
        {"matkul": "Metodologi Penelitian dan Penulisan Ilmiah", "dosen": "Vihi Atina, S.Kom., M.Kom"},
        {"matkul": "Manajemen Sains", "dosen": "Wiji Lestari, S.Si., M.Kom"},
        {"matkul": "Pemrograman Berorientasi Objek", "dosen": "Sopingi, S.Kom., M.Kom"}
    ],
    "SI 24B1": [
        {"matkul": "Pancasila", "dosen": "Dr. Aris Prio Agus Santoso, SH.,MH"},
        {"matkul": "Bahasa Indonesia", "dosen": "Mira Erlinawati, M.Pd"},
        {"matkul": "Tata Kelola TI", "dosen": "Lubna, M.Kom"},
        {"matkul": "Agama", "dosen": "Dr. Nur Hadi, S.Pd.I., M.Ag"},
        {"matkul": "Interaksi Manusia dan Komputer", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Proyek Sistem Aplikasi", "dosen": "Marta Ardiyanto, M.Kom"},
        {"matkul": "Kewarganegaraan", "dosen": "Dr. Hery Dwi Utomo, SH.,MH"},
        {"matkul": "Manajemen Proyek Sistem Informasi", "dosen": "Yafie Miftah Imani, S.Kom., M.Eng"},
        {"matkul": "Inovasi dan Kreatifitas", "dosen": "Hanifah Permatasari, M.Kom"}
    ],
    "SI 23B1": [
        {"matkul": "Pengembangan Data", "dosen": "Aprilisa Arum Sari, S.T, M.Kom"},
        {"matkul": "Audit SI", "dosen": "Yafie Miftah Imani, S.Kom., M.Eng"},
        {"matkul": "Etika Profesi SI", "dosen": "Mira Erlinawati, M.Pd"},
        {"matkul": "Visualisasi Data", "dosen": "Marta Ardiyanto, M.Kom"},
        {"matkul": "Manajemen Hubungan Pelanggan", "dosen": "Dery Hartoro, S.T., M.Hum"},
        {"matkul": "Manajemen Proyek Sistem Informasi", "dosen": "Wijiyanto, S.Kom., M.Pd., M.Kom"}
    ]
}

OPSI_METODE = [
    "Selalu Offline Di Kelas",
    "Sering Offline di Kelas daripada Online",
    "Sering Online daripada Offline di Kelas",
    "Jumlah Pertemuan Online SAMA DENGAN Pertemuan Offline",
    "Sering Tidak Masuk Dan Tidak Memberikan Materi"
]

# Inisialisasi Session State
if "respon_evaluasi" not in st.session_state:
    st.session_state["respon_evaluasi"] = []

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Navigation Sidebar
st.sidebar.title("📌 Menu Navigasi")
mode = st.sidebar.radio("Pilih Tampilan:", ["Form Evaluasi Mahasiswa", "Dashboard Laporan Prodi (Admin)"])

st.sidebar.markdown("---")
st.sidebar.caption("**Fakultas Ilmu Komputer**  \nUniversitas Duta Bangsa Surakarta")

# ==========================================
# 1. FORM EVALUASI MAHASISWA
# ==========================================
if mode == "Form Evaluasi Mahasiswa":
    st.title("Form Evaluasi Pembelajaran S1 Sistem Informasi")
    st.caption("Mohon Diisi Sesuai Keadaan Yang Sebenarnya. Hasil respon Anda bersifat rahasia (anonim) dan digunakan sebagai bahan evaluasi program studi.")
    st.markdown("---")

    # Pilih Kelas Perkuliahan
    kelas_terpilih = st.selectbox("Pilih Kelas Perkuliahan *", list(DATA_KELAS_JADWAL.keys()))

    list_matkul = DATA_KELAS_JADWAL[kelas_terpilih]
    list_dosen_label = [f"{m['matkul']} ({m['dosen']})" for m in list_matkul]

    with st.form("form_evaluasi_pembelajaran", clear_on_submit=True):
        st.markdown("### A. Metode Pembelajaran Dosen Pengampu")
        
        jawaban_metode = {}
        for idx, item in enumerate(list_matkul, start=1):
            st.write(f"**{idx}. Bagaimana metode pembelajaran yang dilakukan oleh dosen pengampu matakuliah \"{item['matkul']}\" ({item['dosen']})? ***")
            jawaban_metode[item['matkul']] = st.radio(
                label=f"Opsi {item['matkul']}",
                options=OPSI_METODE,
                key=f"metode_{kelas_terpilih}_{item['matkul']}",
                label_visibility="collapsed"
            )
            st.markdown("---")

        st.markdown("### B. Penggunaan Media Pembelajaran Online")
        
        idx_meet_selalu = len(list_matkul) + 1
        gmeet_selalu = st.multiselect(
            f"{idx_meet_selalu}. Siapakah Dosen Yang Jika Online, Selalu Menggunakan Google Meet? [Jawaban Bisa Lebih Dari Satu]",
            options=list_dosen_label
        )

        idx_meet_tidak = idx_meet_selalu + 1
        gmeet_tidak = st.multiselect(
            f"{idx_meet_tidak}. Siapakah Dosen Yang Jika Online, Tidak Pernah Menggunakan Google Meet? Hanya share materi via elearning/WA [Jawaban Bisa Lebih Dari Satu]",
            options=list_dosen_label
        )

        st.markdown("---")
        st.markdown("### C. Apresiasi & Evaluasi Dosen")

        idx_fav = idx_meet_tidak + 1
        dosen_favorit = st.multiselect(
            f"{idx_fav}. Siapakah Dosen Favorit Anda dalam Pembelajaran? [Jawaban Bisa Lebih Dari Satu] *",
            options=list_dosen_label
        )

        idx_kurang = idx_fav + 1
        dosen_kurang_suka = st.multiselect(
            f"{idx_kurang}. Siapakah Dosen Yang Kurang Anda Sukai dalam Pembelajaran? [Jawaban Bisa Lebih Dari Satu]",
            options=list_dosen_label
        )

        idx_harapan = idx_kurang + 1
        harapan_satu_semester = st.text_area(
            f"{idx_harapan}. Harapan Anda untuk Pembelajaran Semester Depan *",
            placeholder="Tuliskan harapan Anda untuk semester depan..."
        )

        idx_masalah = idx_harapan + 1
        permasalahan_dosen = st.text_area(
            f"{idx_masalah}. Jika ada permasalahan dengan Dosen dalam hal pembelajaran, bisa disampaikan di sini (sebagai bahan evaluasi program studi ke depannya)",
            placeholder="Sampaikan kendala atau permasalahan pembelajaran jika ada..."
        )

        submit_btn = st.form_submit_button(" Submit Evaluasi")

        if submit_btn:
            if not harapan_satu_semester or not dosen_favorit:
                st.error("Mohon isi seluruh bidang pertanyaan yang wajib (*).")
            else:
                data_respon = {
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Kelas": kelas_terpilih,
                    "Metode Pembelajaran": jawaban_metode,
                    "Dosen GMeet Selalu": gmeet_selalu,
                    "Dosen GMeet Tidak Pernah": gmeet_tidak,
                    "Dosen Favorit": dosen_favorit,
                    "Dosen Kurang Disukai": dosen_kurang_suka,
                    "Harapan Semester Depan": harapan_satu_semester,
                    "Catatan Permasalahan": permasalahan_dosen
                }
                st.session_state["respon_evaluasi"].append(data_respon)
                st.success(" Respon Anda berhasil dikirim. Terima kasih atas partisipasinya!")

# ==========================================
# 2. DASHBOARD LAPORAN PRODI (KHUSUS ADMIN)
# ==========================================
elif mode == "Dashboard Laporan Prodi (Admin)":
    st.title("🔒 Login Admin Evaluasi Program Studi")

    # Autentikasi Password Admin
    if not st.session_state["admin_logged_in"]:
        col_pass, col_btn = st.columns([3, 1])
        input_password = col_pass.text_input("Masukkan Password Admin:", type="password", placeholder="Password...")
        
        if col_btn.button(" Login"):
            if input_password == PASSWORD_ADMIN:
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("Password salah! Silakan coba lagi.")
        st.info("ℹ️ Dashboard ini khusus untuk Kaprodi / Tim Penjaminan Mutu Program Studi.")
    else:
        # Tombol Logout Admin
        if st.sidebar.button("🚪 Logout Admin"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

        st.success(" Kredensial Terverifikasi. Selamat Datang Admin.")
        st.markdown("---")
        
        respon_list = st.session_state["respon_evaluasi"]
        
        if not respon_list:
            st.info("Belum ada respon evaluasi yang masuk dari mahasiswa.")
        else:
            df_respon = pd.DataFrame(respon_list)
            
            # Filter Kelas Laporan
            kelas_filter = st.selectbox("Filter Kelas Laporan:", ["Semua Kelas"] + list(DATA_KELAS_JADWAL.keys()))
            if kelas_filter != "Semua Kelas":
                df_view = df_respon[df_respon["Kelas"] == kelas_filter]
            else:
                df_view = df_respon

            st.metric("Total Respon Masuk", len(df_view))
            st.markdown("---")

            # Visualisasi Dosen Favorit
            st.subheader("🏆 Peringkat Dosen Favorit Mahasiswa")
            all_fav = [d for sublist in df_view["Dosen Favorit"] for d in sublist]
            if all_fav:
                df_fav = pd.DataFrame(all_fav, columns=["Dosen"]).value_counts().reset_index(name="Jumlah Suara")
                fig_fav = px.bar(df_fav, x="Dosen", y="Jumlah Suara", color="Jumlah Suara", title="Jumlah Suara Dosen Favorit")
                fig_fav.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_fav, use_container_width=True)

            # Tabulasi Pembelajaran GMeet
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📹 Dosen Selalu Menggunakan GMeet")
                all_gmeet = [d for sublist in df_view["Dosen GMeet Selalu"] for d in sublist]
                if all_gmeet:
                    df_gm = pd.DataFrame(all_gmeet, columns=["Dosen"]).value_counts().reset_index(name="Jumlah Suara")
                    st.dataframe(df_gm, use_container_width=True)

            with col2:
                st.subheader("⚠️ Dosen Tanpa GMeet (Hanya Share E-learning/WA)")
                all_nogmeet = [d for sublist in df_view["Dosen GMeet Tidak Pernah"] for d in sublist]
                if all_nogmeet:
                    df_nogm = pd.DataFrame(all_nogmeet, columns=["Dosen"]).value_counts().reset_index(name="Jumlah Suara")
                    st.dataframe(df_nogm, use_container_width=True)

            st.markdown("---")
            st.subheader("💬 Masukan Permasalahan & Harapan Mahasiswa")
            st.dataframe(
                df_view[["Timestamp", "Kelas", "Harapan Semester Depan", "Catatan Permasalahan"]], 
                use_container_width=True
            )

            # Unduh CSV
            st.subheader("📥 Export Laporan Evaluasi")
            csv_bytes = df_view.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Data Evaluasi (CSV)",
                data=csv_bytes,
                file_name="Laporan_Hasil_Evaluasi_Pembelajaran_UDBS.csv",
                mime="text/csv"
            )