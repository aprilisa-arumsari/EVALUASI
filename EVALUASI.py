import json
import os
from io import BytesIO
import re
from xml.sax.saxutils import escape

import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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

DATA_EVALUASI_FILE = os.path.join(os.path.dirname(__file__), "data_evaluasi.csv")


def load_respon_evaluasi():
    if not os.path.exists(DATA_EVALUASI_FILE):
        return []

    try:
        df = pd.read_csv(DATA_EVALUASI_FILE)
        if df.empty:
            return []

        records = df.to_dict(orient="records")
        for row in records:
            for key in ["Metode Pembelajaran", "Dosen GMeet Selalu", "Dosen GMeet Tidak Pernah", "Dosen Favorit", "Dosen Kurang Disukai"]:
                value = row.get(key)
                if isinstance(value, str):
                    try:
                        row[key] = json.loads(value)
                    except (TypeError, ValueError):
                        row[key] = value
        return records
    except Exception:
        return []


def simpan_respon_evaluasi(data_list):
    if not data_list:
        return

    rows_to_save = []
    for row in data_list:
        prepared = row.copy()
        for key in ["Metode Pembelajaran", "Dosen GMeet Selalu", "Dosen GMeet Tidak Pernah", "Dosen Favorit", "Dosen Kurang Disukai"]:
            if key in prepared and prepared[key] is not None:
                prepared[key] = json.dumps(prepared[key])
        rows_to_save.append(prepared)

    pd.DataFrame(rows_to_save).to_csv(DATA_EVALUASI_FILE, index=False)


# Inisialisasi Session State
if "respon_evaluasi" not in st.session_state:
    st.session_state["respon_evaluasi"] = load_respon_evaluasi()

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

def _safe_text(value):
    if value is None or pd.isna(value):
        return "-"
    return str(value)


def _angkatan_dari_kelas(kelas):
    match = re.match(r"^SI\s*(\d{2})", str(kelas).strip().upper())
    return f"20{match.group(1)}" if match else "Tidak diketahui"


def _tabel_pdf(rows, col_widths):
    table = Table(rows, colWidths=col_widths, repeatRows=1, splitByRow=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), "#1f4e78"),
                ("TEXTCOLOR", (0, 0), (-1, 0), "#ffffff"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.35, "#9aa7b2"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), ["#ffffff", "#edf3f8"]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def generate_pdf_laporan_kelas(df_view, angkatan_label):
    if df_view.empty:
        return b""

    styles = getSampleStyleSheet()
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    story = []
    story.append(
        Paragraph(
            f"Laporan Evaluasi Pembelajaran<br/>{escape(angkatan_label)}",
            styles["Title"],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            f"Jumlah respon: {len(df_view)} | Jumlah kelas: {df_view['Kelas'].nunique()}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. Jumlah Respon per Kelas", styles["Heading2"]))
    class_counts = df_view["Kelas"].value_counts().sort_index()
    class_rows = [["Kelas", "Jumlah Respon"]]
    class_rows.extend(
        [escape(str(kelas)), str(jumlah)]
        for kelas, jumlah in class_counts.items()
    )
    story.append(_tabel_pdf(class_rows, [430, 250]))
    story.append(Spacer(1, 12))

    method_counts = {}
    for _, row in df_view.iterrows():
        for matkul, metode in row["Metode Pembelajaran"].items():
            key = (row["Kelas"], matkul, metode)
            method_counts[key] = method_counts.get(key, 0) + 1
    story.append(Paragraph("2. Evaluasi Metode Pembelajaran", styles["Heading2"]))
    if method_counts:
        method_rows = [["Kelas", "Mata Kuliah", "Metode", "Jumlah"]]
        method_rows.extend(
            [
                escape(str(kelas)),
                escape(str(matkul)),
                escape(str(metode)),
                str(jumlah),
            ]
            for (kelas, matkul, metode), jumlah in sorted(method_counts.items())
        )
        story.append(_tabel_pdf(method_rows, [100, 190, 325, 65]))
    else:
        story.append(Paragraph("Data metode pembelajaran tidak tersedia.", styles["BodyText"]))
    story.append(Spacer(1, 12))

    vote_sections = [
        ("3. Peringkat Dosen Favorit", "Dosen Favorit"),
        ("4. Peringkat Dosen Tidak Disukai", "Dosen Kurang Disukai"),
        ("5. Penggunaan Google Meet", "Dosen GMeet Selalu"),
        ("6. Tidak Menggunakan Google Meet", "Dosen GMeet Tidak Pernah"),
    ]
    for heading, column in vote_sections:
        vote_counts = {}
        for _, row in df_view.iterrows():
            for dosen in row[column]:
                key = (row["Kelas"], dosen)
                vote_counts[key] = vote_counts.get(key, 0) + 1

        story.append(Paragraph(escape(heading), styles["Heading2"]))
        if vote_counts:
            vote_rows = [["Kelas", "Dosen", "Jumlah Suara"]]
            vote_rows.extend(
                [escape(str(kelas)), escape(str(dosen)), str(jumlah)]
                for (kelas, dosen), jumlah in sorted(
                    vote_counts.items(), key=lambda item: (-item[1], item[0])
                )
            )
            story.append(_tabel_pdf(vote_rows, [150, 440, 90]))
        else:
            story.append(Paragraph("Belum ada jawaban untuk bagian ini.", styles["BodyText"]))
        story.append(Spacer(1, 12))

    story.append(Paragraph("7. Harapan dan Permasalahan Mahasiswa", styles["Heading2"]))
    has_comments = False
    for _, row in df_view.iterrows():
        harapan = _safe_text(row["Harapan Semester Depan"])
        masalah = _safe_text(row["Catatan Permasalahan"])
        story.append(
            Paragraph(
                f"{escape(_safe_text(row['Timestamp']))} — "
                f"{escape(_safe_text(row['Kelas']))}",
                styles["Heading3"],
            )
        )
        story.append(
            Paragraph(
                f"<b>Harapan:</b> {escape(harapan).replace(chr(10), '<br/>')}",
                styles["BodyText"],
            )
        )
        story.append(
            Paragraph(
                f"<b>Permasalahan:</b> {escape(masalah).replace(chr(10), '<br/>')}",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 6))
        has_comments = has_comments or harapan != "-" or masalah != "-"
    if not has_comments:
        story.append(Paragraph("Tidak ada catatan tambahan.", styles["BodyText"]))

    pdf.build(story)

    return buffer.getvalue()


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
                simpan_respon_evaluasi(st.session_state["respon_evaluasi"])
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
            
            df_respon["Angkatan"] = df_respon["Kelas"].map(_angkatan_dari_kelas)
            angkatan_options = sorted(
                angkatan
                for angkatan in df_respon["Angkatan"].dropna().unique()
                if angkatan != "Tidak diketahui"
            )
            angkatan_filter = st.selectbox(
                "Pilih Angkatan Laporan:",
                ["Semua Angkatan"] + angkatan_options,
            )
            if angkatan_filter != "Semua Angkatan":
                df_view = df_respon[df_respon["Angkatan"] == angkatan_filter]
            else:
                df_view = df_respon

            metric_cols = st.columns(3)
            metric_cols[0].metric("Total Respon", len(df_view))
            metric_cols[1].metric("Jumlah Kelas", df_view["Kelas"].nunique())
            metric_cols[2].metric("Angkatan", angkatan_filter)
            st.markdown("---")

            st.subheader("📊 Partisipasi Respon per Kelas")
            respon_per_kelas = (
                df_view.groupby("Kelas")
                .size()
                .rename("Jumlah Respon")
                .reset_index()
                .sort_values("Kelas")
            )
            st.dataframe(respon_per_kelas, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("📚 Evaluasi Metode Pembelajaran per Mata Kuliah")
            metode_rows = [
                {
                    "Kelas": row["Kelas"],
                    "Mata Kuliah": matkul,
                    "Metode Pembelajaran": metode,
                }
                for _, row in df_view.iterrows()
                for matkul, metode in row["Metode Pembelajaran"].items()
            ]
            if metode_rows:
                metode_summary = (
                    pd.DataFrame(metode_rows)
                    .value_counts(["Kelas", "Mata Kuliah", "Metode Pembelajaran"])
                    .reset_index(name="Jumlah")
                    .sort_values(["Kelas", "Mata Kuliah", "Jumlah"], ascending=[True, True, False])
                )
                st.dataframe(metode_summary, use_container_width=True, hide_index=True)
            else:
                st.info("Belum ada data metode pembelajaran untuk angkatan ini.")

            # Visualisasi Dosen Favorit
            st.subheader("🏆 Peringkat Dosen Favorit Mahasiswa")
            fav_rows = [
                {"Dosen": dosen, "Kelas": row["Kelas"]}
                for _, row in df_view.iterrows()
                for dosen in row["Dosen Favorit"]
            ]
            if fav_rows:
                df_fav = (
                    pd.DataFrame(fav_rows)
                    .value_counts(["Dosen", "Kelas"])
                    .reset_index(name="Jumlah Suara")
                )
                fig_fav = px.bar(
                    df_fav,
                    x="Dosen",
                    y="Jumlah Suara",
                    color="Kelas",
                    barmode="group",
                    title="Jumlah Suara Dosen Favorit per Kelas",
                )
                fig_fav.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_fav, use_container_width=True)
            else:
                st.info("Belum ada suara dosen favorit untuk filter kelas ini.")

            st.markdown("---")
            st.subheader("⚠️ Peringkat Dosen Tidak Disukai Mahasiswa")
            not_fav_rows = [
                {"Dosen": dosen, "Kelas": row["Kelas"]}
                for _, row in df_view.iterrows()
                for dosen in row["Dosen Kurang Disukai"]
            ]
            if not_fav_rows:
                df_not_fav = (
                    pd.DataFrame(not_fav_rows)
                    .value_counts(["Dosen", "Kelas"])
                    .reset_index(name="Jumlah Suara")
                )
                fig_not_fav = px.bar(
                    df_not_fav,
                    x="Dosen",
                    y="Jumlah Suara",
                    color="Kelas",
                    barmode="group",
                    title="Jumlah Suara Dosen Tidak Disukai per Kelas",
                )
                fig_not_fav.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_not_fav, use_container_width=True)
            else:
                st.info("Belum ada mahasiswa yang menandai dosen tidak disukai untuk filter ini.")

            # Tabulasi Pembelajaran GMeet
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📹 Dosen Selalu Menggunakan GMeet")
                gmeet_rows = [
                    {"Kelas": row["Kelas"], "Dosen": dosen}
                    for _, row in df_view.iterrows()
                    for dosen in row["Dosen GMeet Selalu"]
                ]
                if gmeet_rows:
                    df_gm = (
                        pd.DataFrame(gmeet_rows)
                        .value_counts(["Kelas", "Dosen"])
                        .reset_index(name="Jumlah Suara")
                    )
                    st.dataframe(df_gm, use_container_width=True, hide_index=True)
                else:
                    st.info("Belum ada respon untuk bagian ini.")

            with col2:
                st.subheader("⚠️ Dosen Tanpa GMeet (Hanya Share E-learning/WA)")
                nogmeet_rows = [
                    {"Kelas": row["Kelas"], "Dosen": dosen}
                    for _, row in df_view.iterrows()
                    for dosen in row["Dosen GMeet Tidak Pernah"]
                ]
                if nogmeet_rows:
                    df_nogm = (
                        pd.DataFrame(nogmeet_rows)
                        .value_counts(["Kelas", "Dosen"])
                        .reset_index(name="Jumlah Suara")
                    )
                    st.dataframe(df_nogm, use_container_width=True, hide_index=True)
                else:
                    st.info("Belum ada respon untuk bagian ini.")

            st.markdown("---")
            st.subheader("💬 Masukan Permasalahan & Harapan Mahasiswa")
            kelas_masukan_options = ["Semua Kelas"] + sorted(
                df_view["Kelas"].dropna().unique().tolist()
            )
            kelas_masukan_filter = st.selectbox(
                "Filter Masukan berdasarkan Kelas:",
                kelas_masukan_options,
                key="filter_kelas_masukan",
            )
            if kelas_masukan_filter == "Semua Kelas":
                df_masukan = df_view
            else:
                df_masukan = df_view[
                    df_view["Kelas"] == kelas_masukan_filter
                ]

            st.markdown("#### A. Metode Pembelajaran Dosen Pengampu")
            hasil_metode_rows = [
                {
                    "Kelas": row["Kelas"],
                    "Mata Kuliah": matkul,
                    "Metode Pembelajaran": metode,
                }
                for _, row in df_masukan.iterrows()
                for matkul, metode in row["Metode Pembelajaran"].items()
            ]
            if hasil_metode_rows:
                hasil_metode = (
                    pd.DataFrame(hasil_metode_rows)
                    .value_counts(["Kelas", "Mata Kuliah", "Metode Pembelajaran"])
                    .reset_index(name="Jumlah Respon")
                    .sort_values(
                        ["Kelas", "Mata Kuliah", "Jumlah Respon"],
                        ascending=[True, True, False],
                    )
                )
                st.dataframe(
                    hasil_metode,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "Belum ada hasil metode pembelajaran untuk kelas ini."
                )

            st.markdown("#### Harapan dan Catatan Permasalahan")
            df_komentar = df_masukan[
                ["Kelas", "Harapan Semester Depan", "Catatan Permasalahan"]
            ]
            st.dataframe(df_komentar, use_container_width=True, hide_index=True)

            # Unduh CSV
            st.subheader("📥 Export Laporan Evaluasi")
            csv_bytes = df_view.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Data Evaluasi (CSV)",
                data=csv_bytes,
                file_name="Laporan_Hasil_Evaluasi_Pembelajaran_UDBS.csv",
                mime="text/csv"
            )

            st.markdown("---")
            st.subheader("📄 Download Laporan PDF per Angkatan")
            report_label = angkatan_filter
            nama_angkatan_pdf = (
                angkatan_filter.replace(" ", "_")
                if angkatan_filter != "Semua Angkatan"
                else "Semua_Angkatan"
            )
            pdf_file_name = f"Laporan_Evaluasi_Angkatan_{nama_angkatan_pdf}.pdf"
            pdf_bytes = generate_pdf_laporan_kelas(df_view, report_label)
            if pdf_bytes:
                st.download_button(
                    label="Download Laporan PDF",
                    data=pdf_bytes,
                    file_name=pdf_file_name,
                    mime="application/pdf"
                )
            else:
                st.warning("Data evaluasi belum cukup untuk membuat laporan PDF.")