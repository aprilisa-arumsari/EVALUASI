import json
import os
import threading
import tempfile
import zipfile
from datetime import time as datetime_time
from io import BytesIO
import re
from xml.sax.saxutils import escape

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.express as px
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image as PdfImage,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Config Halaman
st.set_page_config(
    page_title="Form Evaluasi Pembelajaran S1 Sistem Informasi UDBS",
    page_icon="📋",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --brand-navy: #17324d;
        --brand-blue: #2563eb;
        --brand-teal: #0f766e;
        --surface: #ffffff;
        --page-background: #f3f6fb;
        --border: #dce5ef;
        --muted: #64748b;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 12% 0%, #e8f1ff 0, transparent 34rem),
            var(--page-background);
        color: #23364a;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMain"] .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .app-hero {
        position: relative;
        overflow: hidden;
        margin: 0 0 1.6rem;
        padding: clamp(1.5rem, 4vw, 2.5rem);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 1.35rem;
        color: #ffffff;
        background:
            radial-gradient(circle at 88% 16%, rgba(255, 255, 255, 0.2), transparent 13rem),
            linear-gradient(118deg, #17324d 0%, #1d5680 58%, #0f766e 100%);
        box-shadow: 0 18px 42px rgba(23, 50, 77, 0.16);
    }

    .app-hero::after {
        position: absolute;
        right: -3rem;
        bottom: -7rem;
        width: 18rem;
        height: 18rem;
        border: 1px solid rgba(255, 255, 255, 0.13);
        border-radius: 50%;
        content: "";
        box-shadow: 0 0 0 2rem rgba(255, 255, 255, 0.035),
                    0 0 0 4rem rgba(255, 255, 255, 0.025);
        pointer-events: none;
    }

    .hero-eyebrow {
        margin-bottom: 0.65rem;
        color: #bfdbfe;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .app-hero h1 {
        position: relative;
        z-index: 1;
        max-width: 850px;
        margin: 0;
        color: #ffffff;
        font-size: clamp(1.8rem, 4vw, 2.65rem);
        line-height: 1.14;
    }

    .app-hero p {
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0.8rem 0 0;
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.65;
    }

    .hero-badges {
        position: relative;
        z-index: 1;
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 1.2rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.42rem 0.7rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 999px;
        color: #f8fafc;
        background: rgba(15, 23, 42, 0.18);
        font-size: 0.78rem;
        font-weight: 600;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0.45rem 0 1.25rem;
        padding: 0.8rem 0.7rem;
        border: 1px solid #dce5ef;
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.76);
    }

    .sidebar-brand-mark {
        display: grid;
        width: 2.65rem;
        height: 2.65rem;
        flex: 0 0 2.65rem;
        place-items: center;
        border-radius: 0.85rem;
        color: #ffffff;
        background: linear-gradient(135deg, #2563eb, #0f766e);
        font-size: 0.9rem;
        font-weight: 800;
        letter-spacing: 0.03em;
    }

    .sidebar-brand-copy strong,
    .sidebar-brand-copy span {
        display: block;
    }

    .sidebar-brand-copy strong {
        color: var(--brand-navy);
        font-size: 0.88rem;
    }

    .sidebar-brand-copy span {
        margin-top: 0.15rem;
        color: var(--muted);
        font-size: 0.72rem;
        line-height: 1.4;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #edf4fc 0%, #f8fafc 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #40556c;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: var(--brand-navy);
        font-weight: 700;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 0.55rem 0.7rem;
        border-radius: 0.7rem;
        transition: background-color 150ms ease;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #e1ebf8;
    }

    h1, h2, h3 {
        color: var(--brand-navy);
        letter-spacing: -0.025em;
    }

    h1 {
        font-weight: 800;
        line-height: 1.2;
    }

    h2, h3 {
        font-weight: 700;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
        line-height: 1.65;
    }

    [data-testid="stForm"] {
        padding: clamp(1rem, 3vw, 2rem);
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid var(--border);
        border-radius: 1.15rem;
        box-shadow: 0 12px 35px rgba(23, 50, 77, 0.07);
    }

    [data-testid="stForm"] h3 {
        margin-top: 0.5rem;
        padding-bottom: 0.65rem;
        border-bottom: 2px solid #e8eef6;
    }

    [data-testid="stForm"] [data-testid="stRadio"] {
        margin: 0.45rem 0 1rem;
        padding: 0.75rem 1rem;
        background: #f8fafc;
        border: 1px solid #e8eef6;
        border-radius: 0.8rem;
    }

    [data-testid="stForm"] [data-testid="stRadio"] label,
    [data-testid="stForm"] [data-testid="stMultiSelect"] label,
    [data-testid="stForm"] [data-testid="stTextArea"] label {
        color: #30465d;
    }

    [data-baseweb="select"] > div,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        border-color: #cbd8e6;
        border-radius: 0.7rem;
        background: #ffffff;
    }

    [data-baseweb="select"] > div:focus-within,
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--brand-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
    }

    [data-testid="stButton"] button,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stDownloadButton"] button {
        min-height: 2.7rem;
        border-radius: 0.7rem;
        font-weight: 650;
        transition: transform 150ms ease, box-shadow 150ms ease;
    }

    [data-testid="stFormSubmitButton"] button,
    [data-testid="stButton"] button[kind="primary"] {
        border: 0;
        color: #ffffff;
        background: linear-gradient(110deg, var(--brand-blue), var(--brand-teal));
        box-shadow: 0 5px 14px rgba(37, 99, 235, 0.2);
    }

    [data-testid="stButton"] button:hover,
    [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stDownloadButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(23, 50, 77, 0.14);
    }

    [data-testid="stMetric"] {
        padding: 1.15rem 1.25rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 1rem;
        box-shadow: 0 8px 24px rgba(23, 50, 77, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--brand-navy);
        font-weight: 800;
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"] {
        overflow: hidden;
        border: 1px solid var(--border);
        border-radius: 0.9rem;
        background: var(--surface);
        box-shadow: 0 6px 20px rgba(23, 50, 77, 0.045);
    }

    [data-testid="stAlert"] {
        border-radius: 0.85rem;
    }

    hr {
        border-color: #dce5ef;
    }

    @media (max-width: 768px) {
        [data-testid="stMain"] .block-container {
            padding: 1.1rem 1rem 2rem;
        }

        h1 {
            font-size: 1.8rem;
        }

        [data-testid="stForm"] {
            padding: 1rem;
        }

        .app-hero {
            border-radius: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def _ambil_password_admin():
    password = os.getenv("ADMIN_PASSWORD")
    if password:
        return password

    try:
        return st.secrets["ADMIN_PASSWORD"]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


PASSWORD_ADMIN = _ambil_password_admin()
if PASSWORD_ADMIN and len(PASSWORD_ADMIN) < 16:
    st.error("ADMIN_PASSWORD harus terdiri dari minimal 16 karakter.")
    st.stop()

DATA_EVALUASI_FILE = os.path.join(os.path.dirname(__file__), "data_evaluasi.csv")
PENGATURAN_EVALUASI_FILE = os.path.join(
    os.path.dirname(__file__),
    "pengaturan_evaluasi.json",
)
DATA_EVALUASI_LOCK = threading.Lock()
ZONA_WAKTU_EVALUASI = "Asia/Jakarta"


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

KOLOM_JSON_REPON = [
    "Metode Pembelajaran",
    "Dosen GMeet Selalu",
    "Dosen GMeet Tidak Pernah",
    "Dosen Favorit",
    "Dosen Kurang Disukai",
]

KOLOM_REPON = [
    "Timestamp",
    "Kelas",
    "Metode Pembelajaran",
    "Dosen GMeet Selalu",
    "Dosen GMeet Tidak Pernah",
    "Dosen Favorit",
    "Dosen Kurang Disukai",
    "Harapan Semester Depan",
    "Catatan Permasalahan",
]


def _siapkan_respon_untuk_csv(data_list):
    rows_to_save = []
    for row in data_list:
        prepared = row.copy()
        for key in KOLOM_JSON_REPON:
            if key in prepared and prepared[key] is not None:
                prepared[key] = json.dumps(prepared[key], ensure_ascii=False)
        rows_to_save.append(prepared)
    return rows_to_save


def _csv_respon_bytes(data_list):
    rows_to_save = _siapkan_respon_untuk_csv(data_list)
    return pd.DataFrame(rows_to_save, columns=KOLOM_REPON).to_csv(
        index=False
    ).encode("utf-8-sig")


def _csv_ke_respon(csv_bytes):
    try:
        df = pd.read_csv(BytesIO(csv_bytes))
    except pd.errors.EmptyDataError:
        return []
    records = df.to_dict(orient="records")
    for row in records:
        for key in KOLOM_JSON_REPON:
            value = row.get(key)
            if isinstance(value, str):
                try:
                    row[key] = json.loads(value)
                except (TypeError, ValueError):
                    row[key] = value
    return records


def _baca_cadangan_unggahan(nama_file, file_bytes):
    if nama_file.lower().endswith(".zip"):
        try:
            with zipfile.ZipFile(BytesIO(file_bytes)) as paket:
                file_bytes = paket.read("data/Cadangan_Semua_Respon.csv")
        except KeyError as error:
            raise ValueError(
                "ZIP tidak berisi data/Cadangan_Semua_Respon.csv."
            ) from error
        except (zipfile.BadZipFile, RuntimeError) as error:
            raise ValueError(f"File ZIP cadangan tidak dapat dibaca: {error}") from error

    try:
        df = pd.read_csv(BytesIO(file_bytes))
    except pd.errors.EmptyDataError as error:
        raise ValueError("File CSV cadangan kosong.") from error
    except (pd.errors.ParserError, UnicodeError) as error:
        raise ValueError(f"File CSV cadangan tidak dapat dibaca: {error}") from error

    kolom_hilang = sorted(set(KOLOM_REPON) - set(df.columns))
    kolom_tambahan = sorted(set(df.columns) - set(KOLOM_REPON))
    if kolom_hilang or kolom_tambahan:
        detail = []
        if kolom_hilang:
            detail.append(f"kolom yang kurang: {', '.join(kolom_hilang)}")
        if kolom_tambahan:
            detail.append(f"kolom yang tidak dikenal: {', '.join(kolom_tambahan)}")
        raise ValueError(
            "Format CSV tidak sesuai dengan cadangan aplikasi (" +
            "; ".join(detail) + ")."
        )
    if df.empty:
        raise ValueError("CSV cadangan tidak berisi respon.")

    records = _csv_ke_respon(file_bytes)
    kolom_list = KOLOM_JSON_REPON[1:]
    for nomor_baris, row in enumerate(records, start=2):
        for key in ("Timestamp", "Kelas"):
            value = row.get(key)
            if pd.isna(value) or not str(value).strip():
                raise ValueError(
                    f"Kolom {key} kosong pada baris CSV {nomor_baris}."
                )
        if not isinstance(row.get("Metode Pembelajaran"), dict):
            raise ValueError(
                "Format Metode Pembelajaran tidak valid pada baris CSV "
                f"{nomor_baris}."
            )
        for key in kolom_list:
            if not isinstance(row.get(key), list):
                raise ValueError(
                    f"Format {key} tidak valid pada baris CSV {nomor_baris}."
                )
    return records


def _baca_respon_lokal():
    if not os.path.exists(DATA_EVALUASI_FILE):
        return []
    with open(DATA_EVALUASI_FILE, "rb") as csv_file:
        return _csv_ke_respon(csv_file.read())


def load_respon_evaluasi():
    try:
        with DATA_EVALUASI_LOCK:
            return _baca_respon_lokal()
    except (OSError, UnicodeError, pd.errors.ParserError, ValueError) as error:
        st.error(f"Gagal memuat respon dari file lokal: {error}")
        st.stop()


def _tulis_respon_lokal(data_respon):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=os.path.dirname(DATA_EVALUASI_FILE),
            prefix=".data_evaluasi_",
            suffix=".tmp",
            delete=False,
        ) as csv_file:
            temporary_path = csv_file.name
            csv_file.write(_csv_respon_bytes(data_respon))
        os.replace(temporary_path, DATA_EVALUASI_FILE)
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        if temporary_path and os.path.exists(temporary_path):
            try:
                os.remove(temporary_path)
            except OSError as cleanup_error:
                raise RuntimeError(
                    "Respon gagal disimpan dan file sementara gagal dibersihkan."
                ) from cleanup_error
        raise RuntimeError(f"Respon gagal disimpan ke file lokal: {error}") from error


def simpan_respon_evaluasi(data_respon):
    try:
        with DATA_EVALUASI_LOCK:
            records = _baca_respon_lokal()
            records.append(data_respon)
            _tulis_respon_lokal(records)
    except (OSError, UnicodeError, pd.errors.ParserError, TypeError, ValueError) as error:
        raise RuntimeError(
            f"Respon gagal disimpan ke file lokal: {error}"
        ) from error


def pulihkan_respon_evaluasi(data_respon):
    with DATA_EVALUASI_LOCK:
        _tulis_respon_lokal(data_respon)


def load_batas_waktu_pengisian():
    if not os.path.exists(PENGATURAN_EVALUASI_FILE):
        return None

    try:
        with open(PENGATURAN_EVALUASI_FILE, "r", encoding="utf-8") as file:
            pengaturan = json.load(file)
        nilai_batas = pengaturan["batas_waktu"]
        if nilai_batas is None:
            return None
        batas_waktu = pd.Timestamp(nilai_batas)
        if batas_waktu.tzinfo is None:
            raise ValueError("Zona waktu batas pengisian tidak tersedia.")
        return batas_waktu.tz_convert(ZONA_WAKTU_EVALUASI)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise RuntimeError(
            f"Batas waktu pengisian tidak dapat dibaca: {error}"
        ) from error


def simpan_batas_waktu_pengisian(batas_waktu):
    nilai_batas = (
        batas_waktu.isoformat()
        if batas_waktu is not None
        else None
    )
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=os.path.dirname(PENGATURAN_EVALUASI_FILE),
            prefix=".pengaturan_evaluasi_",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = file.name
            json.dump({"batas_waktu": nilai_batas}, file)
        os.replace(temporary_path, PENGATURAN_EVALUASI_FILE)
    except (OSError, TypeError, ValueError) as error:
        if temporary_path and os.path.exists(temporary_path):
            try:
                os.remove(temporary_path)
            except OSError as cleanup_error:
                raise RuntimeError(
                    "Batas waktu gagal disimpan dan file sementara gagal dibersihkan."
                ) from cleanup_error
        raise RuntimeError(
            f"Batas waktu pengisian gagal disimpan: {error}"
        ) from error


def format_batas_waktu_indonesia(batas_waktu):
    nama_bulan = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )
    return (
        f"{batas_waktu.day} {nama_bulan[batas_waktu.month - 1]} "
        f"{batas_waktu.year} pukul {batas_waktu:%H:%M} WIB"
    )


# Inisialisasi Session State
if "respon_evaluasi" not in st.session_state:
    st.session_state["respon_evaluasi"] = load_respon_evaluasi()

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

try:
    batas_waktu_pengisian = load_batas_waktu_pengisian()
except RuntimeError as error:
    batas_waktu_pengisian = None
    kesalahan_batas_waktu = str(error)
else:
    kesalahan_batas_waktu = None

def _safe_text(value):
    if value is None or pd.isna(value):
        return "-"
    return str(value)


def _angkatan_dari_kelas(kelas):
    match = re.match(r"^SI\s*(\d{2})", str(kelas).strip().upper())
    return f"20{match.group(1)}" if match else "Tidak diketahui"


def buat_gambar_batang_png(
    data,
    kategori,
    nilai,
    kelompok,
    judul,
    horizontal=False,
    show_values=False,
):
    if data.empty:
        return b""

    kelompok_values = data[kelompok].drop_duplicates().tolist()
    kategori_values = data[kategori].drop_duplicates().tolist()
    colors = ["#2563EB", "#0F766E", "#F59E0B", "#8B5CF6", "#DB2777"]
    bar_size = 0.8 / len(kelompok_values)
    positions = list(range(len(kategori_values)))
    figure_height = max(6, len(kategori_values) * 0.45) if horizontal else 8
    figure, axis = plt.subplots(
        figsize=(14, figure_height),
        facecolor="#FFFFFF",
    )
    axis.set_facecolor("#FFFFFF")

    for index, kelompok_value in enumerate(kelompok_values):
        subset = data[data[kelompok] == kelompok_value]
        nilai_by_category = (
            subset.groupby(kategori, dropna=False)[nilai].sum().to_dict()
        )
        values = [nilai_by_category.get(value, 0) for value in kategori_values]
        offset = (index - (len(kelompok_values) - 1) / 2) * bar_size
        bar_positions = [position + offset for position in positions]
        if horizontal:
            bars = axis.barh(
                bar_positions,
                values,
                height=bar_size,
                label=str(kelompok_value),
                color=colors[index % len(colors)],
                edgecolor="#FFFFFF",
                linewidth=0.8,
            )
        else:
            bars = axis.bar(
                bar_positions,
                values,
                width=bar_size,
                label=str(kelompok_value),
                color=colors[index % len(colors)],
                edgecolor="#FFFFFF",
                linewidth=0.8,
            )
        if show_values:
            axis.bar_label(
                bars,
                labels=[
                    f"{value:g}" if value else ""
                    for value in values
                ],
                padding=3,
                fontsize=8,
                color="#334155",
            )

    if horizontal:
        figure.suptitle(
            judul,
            x=0.08,
            y=0.98,
            ha="left",
            fontsize=14,
            fontweight="bold",
            color="#17324D",
        )
        figure.legend(
            title=kelompok,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.88),
            ncol=min(2, len(kelompok_values)),
            frameon=False,
            fontsize=8,
            title_fontsize=9,
            columnspacing=1.2,
            handletextpad=0.55,
            labelspacing=0.3,
        )
    else:
        axis.set_title(
            judul,
            fontsize=14,
            fontweight="bold",
            color="#17324D",
            loc="left",
            pad=18,
        )
        axis.legend(
            title=kelompok,
            frameon=False,
            fontsize=9,
            title_fontsize=9,
        )
    axis.set_axisbelow(True)
    if horizontal:
        axis.set_yticks(positions, kategori_values)
        axis.set_xlabel(nilai, color="#475569", labelpad=8)
        axis.invert_yaxis()
        axis.grid(axis="x", color="#CBD5E1", linestyle="--", alpha=0.65)
        axis.tick_params(axis="y", labelsize=8, colors="#334155", length=0, pad=8)
        axis.tick_params(axis="x", labelsize=8, colors="#64748B")
        for spine in ("top", "right", "left"):
            axis.spines[spine].set_visible(False)
        axis.spines["bottom"].set_color("#CBD5E1")
    else:
        axis.set_xticks(positions, kategori_values, rotation=45, ha="right")
        axis.set_ylabel(nilai, color="#475569", labelpad=8)
        axis.grid(axis="y", color="#CBD5E1", linestyle="--", alpha=0.65)
        axis.tick_params(axis="both", labelsize=8, colors="#64748B")
        for spine in ("top", "right"):
            axis.spines[spine].set_visible(False)
        axis.spines["left"].set_color("#CBD5E1")
        axis.spines["bottom"].set_color("#CBD5E1")
    if show_values:
        axis.margins(x=0.16 if horizontal else 0, y=0.08)

    buffer = BytesIO()
    if horizontal:
        figure.tight_layout(rect=(0, 0.03, 1, 0.62))
    else:
        figure.tight_layout(rect=(0, 0, 1, 0.96))
    figure.savefig(buffer, format="png", dpi=160, bbox_inches="tight")
    plt.close(figure)
    return buffer.getvalue()


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
            "Laporan Evaluasi Pembelajaran<br/>"
            "Program Studi S1 Sistem Informasi<br/>"
            "Tahun Akademik 2026/2027 Ganjil",
            styles["Title"],
        )
    )
    if angkatan_label != "Semua Angkatan":
        story.append(
            Paragraph(f"Angkatan: {escape(angkatan_label)}", styles["BodyText"])
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

    dosen_per_kelas_matkul = {
        kelas: {
            item["matkul"]: item["dosen"]
            for item in jadwal
        }
        for kelas, jadwal in DATA_KELAS_JADWAL.items()
    }
    method_counts = {}
    method_graph_counts = {}
    for _, row in df_view.iterrows():
        for matkul, metode in row["Metode Pembelajaran"].items():
            kelas = row["Kelas"]
            key = (kelas, matkul, metode)
            method_counts[key] = method_counts.get(key, 0) + 1
            dosen = dosen_per_kelas_matkul.get(kelas, {}).get(
                matkul,
                "Dosen tidak diketahui",
            )
            graph_key = (matkul, dosen, metode)
            method_graph_counts[graph_key] = (
                method_graph_counts.get(graph_key, 0) + 1
            )
    story.append(Paragraph("2. Evaluasi Metode Pembelajaran", styles["Heading2"]))
    if method_graph_counts:
        story.append(
            Paragraph(
                "Ringkasan distribusi per mata kuliah dan dosen",
                styles["Heading3"],
            )
        )
        graph_rows = [
            ["Mata Kuliah", "Dosen", "Metode", "Jumlah Respon"]
        ]
        graph_rows.extend(
            [
                Paragraph(escape(str(matkul)), styles["BodyText"]),
                Paragraph(escape(str(dosen)), styles["BodyText"]),
                Paragraph(escape(str(metode)), styles["BodyText"]),
                str(jumlah),
            ]
            for (matkul, dosen, metode), jumlah in sorted(
                method_graph_counts.items()
            )
        )
        story.append(_tabel_pdf(graph_rows, [150, 170, 310, 60]))
        story.append(Spacer(1, 8))

        grafik_metode_df = pd.DataFrame(
            [
                {
                    "Mata Kuliah & Dosen": f"{matkul}\n({dosen})",
                    "Metode Pembelajaran": metode,
                    "Jumlah Respon": jumlah,
                }
                for (matkul, dosen, metode), jumlah
                in method_graph_counts.items()
            ]
        )
        kategori_grafik = grafik_metode_df[
            "Mata Kuliah & Dosen"
        ].drop_duplicates().tolist()
        story.append(
            Paragraph(
                "Grafik distribusi metode pembelajaran",
                styles["Heading3"],
            )
        )
        for offset in range(0, len(kategori_grafik), 12):
            kategori_chunk = kategori_grafik[offset : offset + 12]
            grafik_chunk = grafik_metode_df[
                grafik_metode_df["Mata Kuliah & Dosen"].isin(kategori_chunk)
            ]
            grafik_bytes = buat_gambar_batang_png(
                grafik_chunk,
                "Mata Kuliah & Dosen",
                "Jumlah Respon",
                "Metode Pembelajaran",
                "Distribusi Metode Pembelajaran per Mata Kuliah",
                horizontal=True,
                show_values=True,
            )
            tinggi_grafik = 680 * max(6, len(kategori_chunk) * 0.45) / 14
            story.append(
                PdfImage(
                    BytesIO(grafik_bytes),
                    width=680,
                    height=tinggi_grafik,
                )
            )
            story.append(Spacer(1, 8))

    if method_counts:
        story.append(
            Paragraph("Rincian distribusi per kelas", styles["Heading3"])
        )
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
    for kelas, kelas_df in df_view.groupby("Kelas", sort=True):
        story.append(
            Paragraph(f"Kelas {escape(str(kelas))}", styles["Heading3"])
        )
        comment_rows = [["Harapan Mahasiswa", "Permasalahan Mahasiswa"]]
        for _, row in kelas_df.iterrows():
            harapan = _safe_text(row["Harapan Semester Depan"]).strip()
            masalah = _safe_text(row["Catatan Permasalahan"]).strip()
            if harapan == "-" or not harapan:
                harapan = "-"
            if masalah == "-" or not masalah:
                masalah = "-"
            if harapan == "-" and masalah == "-":
                continue

            comment_rows.append(
                [
                    Paragraph(
                        escape(harapan).replace(chr(10), "<br/>"),
                        styles["BodyText"],
                    ),
                    Paragraph(
                        escape(masalah).replace(chr(10), "<br/>"),
                        styles["BodyText"],
                    ),
                ]
            )

        if len(comment_rows) > 1:
            story.append(_tabel_pdf(comment_rows, [340, 340]))
        else:
            story.append(
                Paragraph("Tidak ada catatan tambahan.", styles["BodyText"])
            )
        story.append(Spacer(1, 8))

    tanggal_laporan = pd.Timestamp.now(tz="Asia/Jakarta")
    nama_bulan = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )
    tanggal_indonesia = (
        f"Surakarta, {tanggal_laporan.day} "
        f"{nama_bulan[tanggal_laporan.month - 1]} {tanggal_laporan.year}"
    )
    style_tanda_tangan = ParagraphStyle(
        "TandaTangan",
        parent=styles["BodyText"],
        alignment=1,
        leading=14,
    )
    kolom_pengesahan = [
        [
            Paragraph(
                "Mengetahui,<br/>Dekan Fakultas Ilmu Komputer",
                style_tanda_tangan,
            ),
            Spacer(1, 58),
            Paragraph(
                "Eko Purwanto, S.Kom., M.Kom., Ph.D",
                style_tanda_tangan,
            ),
        ],
        [
            Paragraph(
                "Ketua Program Studi<br/>S1 Sistem Informasi",
                style_tanda_tangan,
            ),
            Spacer(1, 58),
            Paragraph(
                "Hanifah Permatasari, S.Kom., M.Kom",
                style_tanda_tangan,
            ),
        ],
    ]
    tabel_pengesahan = Table(
        [kolom_pengesahan],
        colWidths=[340, 340],
        hAlign="CENTER",
    )
    tabel_pengesahan.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                Spacer(1, 12),
                Paragraph(tanggal_indonesia, style_tanda_tangan),
                Spacer(1, 12),
                tabel_pengesahan,
            ]
        )
    )

    pdf.build(story)

    return buffer.getvalue()


def buat_paket_hasil_laporan(
    df_view,
    respon_list,
    grafik_list,
    pdf_bytes,
    nama_angkatan,
):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as paket:
        paket.writestr(
            "data/Laporan_Hasil_Evaluasi.csv",
            _csv_respon_bytes(df_view.to_dict(orient="records")),
        )
        paket.writestr(
            "data/Cadangan_Semua_Respon.csv",
            _csv_respon_bytes(respon_list),
        )
        if pdf_bytes:
            paket.writestr(
                f"Laporan_Evaluasi_Angkatan_{nama_angkatan}.pdf",
                pdf_bytes,
            )
        for nama_grafik, gambar_png in grafik_list:
            paket.writestr(
                f"grafik/{nama_grafik}.png",
                gambar_png,
            )
    return buffer.getvalue()


# Navigation Sidebar
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-brand-mark">SI</div>
        <div class="sidebar-brand-copy">
            <strong>Evaluasi Akademik</strong>
            <span>Program Studi Sistem Informasi</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("#### Navigasi")
mode = st.sidebar.radio("Pilih Tampilan:", ["Form Evaluasi Mahasiswa", "Dashboard Laporan Prodi (Admin)"])

st.sidebar.markdown("---")
st.sidebar.caption("**Fakultas Ilmu Komputer**  \nUniversitas Duta Bangsa Surakarta")

# ==========================================
# 1. FORM EVALUASI MAHASISWA
# ==========================================
if mode == "Form Evaluasi Mahasiswa":
    if kesalahan_batas_waktu:
        st.error(
            f"{kesalahan_batas_waktu} Pengisian dinonaktifkan sampai admin "
            "memperbaiki pengaturan batas waktu."
        )
        st.stop()

    pengisian_ditutup = (
        batas_waktu_pengisian is not None
        and pd.Timestamp.now(tz=ZONA_WAKTU_EVALUASI) >= batas_waktu_pengisian
    )
    if pengisian_ditutup:
        st.warning(
            "Pengisian kuesioner telah ditutup pada "
            f"{format_batas_waktu_indonesia(batas_waktu_pengisian)}."
        )
        st.stop()

    st.markdown(
        """
        <section class="app-hero">
            <div class="hero-eyebrow">Fakultas Ilmu Komputer · UDB Surakarta</div>
            <h1>Evaluasi Pembelajaran</h1>
            <p>
                Sampaikan pengalaman belajar Anda dengan jujur. Masukan ini
                membantu program studi meningkatkan kualitas pembelajaran.
            </p>
            <div class="hero-badges">
                <span class="hero-badge">🔒 Respon bersifat anonim</span>
                <span class="hero-badge">📚 Program Studi S1 Sistem Informasi</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if batas_waktu_pengisian is not None:
        st.info(
            "Batas akhir pengisian: "
            f"{format_batas_waktu_indonesia(batas_waktu_pengisian)}."
        )

    # Pilih Kelas Perkuliahan
    with st.container(border=True):
        st.markdown("#### Mulai evaluasi")
        kelas_terpilih = st.selectbox(
            "Pilih kelas perkuliahan *",
            list(DATA_KELAS_JADWAL.keys()),
        )
        st.caption(
            "Pilih kelas Anda untuk menampilkan mata kuliah dan dosen pengampu."
        )

    list_matkul = DATA_KELAS_JADWAL[kelas_terpilih]
    list_dosen_label = [f"{m['matkul']} ({m['dosen']})" for m in list_matkul]

    with st.form("form_evaluasi_pembelajaran", clear_on_submit=True):
        st.markdown("### A. Metode Pembelajaran Dosen Pengampu")
        
        jawaban_metode = {}
        for idx, item in enumerate(list_matkul, start=1):
            st.markdown(
                f"**{idx}. Bagaimana metode pembelajaran yang dilakukan oleh "
                f"dosen pengampu mata kuliah \"{item['matkul']}\" "
                f"({item['dosen']})?**"
            )
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
            batas_waktu_terbaru = load_batas_waktu_pengisian()
            waktu_sekarang = pd.Timestamp.now(tz=ZONA_WAKTU_EVALUASI)
            if (
                batas_waktu_terbaru is not None
                and waktu_sekarang >= batas_waktu_terbaru
            ):
                st.error(
                    "Kuesioner sudah ditutup pada "
                    f"{format_batas_waktu_indonesia(batas_waktu_terbaru)}. "
                    "Respon Anda belum dikirim."
                )
            elif not harapan_satu_semester or not dosen_favorit:
                st.error("Mohon isi seluruh bidang pertanyaan yang wajib (*).")
            else:
                data_respon = {
                    "Timestamp": waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S"),
                    "Kelas": kelas_terpilih,
                    "Metode Pembelajaran": jawaban_metode,
                    "Dosen GMeet Selalu": gmeet_selalu,
                    "Dosen GMeet Tidak Pernah": gmeet_tidak,
                    "Dosen Favorit": dosen_favorit,
                    "Dosen Kurang Disukai": dosen_kurang_suka,
                    "Harapan Semester Depan": harapan_satu_semester,
                    "Catatan Permasalahan": permasalahan_dosen
                }
                try:
                    simpan_respon_evaluasi(data_respon)
                except (RuntimeError, OSError, TypeError, ValueError) as error:
                    st.error(
                        "Respon belum tersimpan ke file lokal. Periksa "
                        f"akses penyimpanan, lalu coba kembali. Detail: {error}"
                    )
                else:
                    st.session_state["respon_evaluasi"].append(data_respon)
                    st.success(
                        "Respon Anda berhasil dikirim. Terima kasih atas "
                        "partisipasinya!"
                    )

# ==========================================
# 2. DASHBOARD LAPORAN PRODI (KHUSUS ADMIN)
# ==========================================
elif mode == "Dashboard Laporan Prodi (Admin)":
    st.markdown(
        """
        <section class="app-hero">
            <div class="hero-eyebrow">Ruang administrasi · Fakultas Ilmu Komputer</div>
            <h1>Dashboard Evaluasi</h1>
            <p>
                Pantau hasil evaluasi pembelajaran dan unduh laporan program
                studi dengan mudah.
            </p>
            <div class="hero-badges">
                <span class="hero-badge">🔐 Akses khusus admin</span>
                <span class="hero-badge">📊 Ringkasan respon mahasiswa</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # Autentikasi Password Admin
    if not st.session_state["admin_logged_in"]:
        if not PASSWORD_ADMIN:
            st.error(
                "Login admin belum aktif. Admin harus mengatur ADMIN_PASSWORD "
                "melalui Streamlit Secrets atau environment variable."
            )
        else:
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
        if kesalahan_batas_waktu:
            st.error(
                f"{kesalahan_batas_waktu} Simpan pengaturan di bawah untuk "
                "memperbaiki konfigurasi."
            )
        st.subheader("Batas Waktu Pengisian Kuesioner")
        batas_aktif = batas_waktu_pengisian is not None
        if batas_aktif:
            st.info(
                "Batas saat ini: "
                f"{format_batas_waktu_indonesia(batas_waktu_pengisian)}."
            )
        else:
            st.caption("Belum ada batas waktu; kuesioner tetap terbuka.")

        tanggal_default = (
            batas_waktu_pengisian.date()
            if batas_aktif
            else (
                pd.Timestamp.now(tz=ZONA_WAKTU_EVALUASI)
                + pd.Timedelta(days=7)
            ).date()
        )
        waktu_default = (
            batas_waktu_pengisian.time().replace(tzinfo=None)
            if batas_aktif
            else datetime_time(23, 59)
        )
        with st.form("pengaturan_batas_waktu"):
            batas_aktif_baru = st.checkbox(
                "Aktifkan batas akhir pengisian",
                value=batas_aktif,
            )
            kolom_tanggal, kolom_jam = st.columns(2)
            tanggal_batas = kolom_tanggal.date_input(
                "Tanggal terakhir (DD/MM/YYYY)",
                value=tanggal_default,
                format="DD/MM/YYYY",
            )
            jam_batas = kolom_jam.time_input(
                "Jam terakhir (HH:MM)",
                value=waktu_default,
                step=60,
            )
            simpan_pengaturan = st.form_submit_button(
                "Simpan Batas Waktu",
                type="primary",
            )

        if simpan_pengaturan:
            batas_baru = None
            if batas_aktif_baru:
                batas_baru = (
                    pd.Timestamp(tanggal_batas)
                    .replace(
                        hour=jam_batas.hour,
                        minute=jam_batas.minute,
                        second=0,
                        microsecond=0,
                    )
                    .tz_localize(ZONA_WAKTU_EVALUASI)
                )
                if batas_baru <= pd.Timestamp.now(tz=ZONA_WAKTU_EVALUASI):
                    st.error("Pilih tanggal dan waktu yang masih akan datang.")
                    st.stop()

            try:
                simpan_batas_waktu_pengisian(batas_baru)
            except RuntimeError as error:
                st.error(str(error))
            else:
                st.success("Pengaturan batas waktu berhasil disimpan.")
                st.rerun()

        st.markdown("---")
        
        st.session_state["respon_evaluasi"] = load_respon_evaluasi()
        respon_list = st.session_state["respon_evaluasi"]

        st.subheader("Pulihkan Data dari Cadangan")
        st.warning(
            "Pemulihan akan mengganti semua respon yang saat ini tersimpan. "
            "Simpan cadangan data saat ini terlebih dahulu jika ingin "
            "mempertahankannya."
        )
        if respon_list:
            st.download_button(
                label="Unduh Data Saat Ini sebelum Pemulihan",
                data=_csv_respon_bytes(respon_list),
                file_name="Cadangan_Sebelum_Pemulihan.csv",
                mime="text/csv",
                key="download_before_restore",
            )

        file_cadangan = st.file_uploader(
            "Pilih file CSV cadangan atau ZIP hasil unduhan aplikasi",
            type=["csv", "zip"],
            help=(
                "Untuk ZIP, aplikasi akan memakai "
                "data/Cadangan_Semua_Respon.csv."
            ),
            key="restore_backup_upload",
        )
        if file_cadangan is not None:
            try:
                respon_cadangan = _baca_cadangan_unggahan(
                    file_cadangan.name,
                    file_cadangan.getvalue(),
                )
            except ValueError as error:
                st.error(f"Cadangan tidak dapat dipulihkan: {error}")
            else:
                st.info(
                    f"File berisi {len(respon_cadangan)} respon. "
                    "Pemulihan akan mengganti seluruh data saat ini."
                )
                if st.button(
                    "Pulihkan dan Ganti Semua Data",
                    type="primary",
                    key="restore_backup_button",
                ):
                    try:
                        pulihkan_respon_evaluasi(respon_cadangan)
                    except (RuntimeError, OSError, TypeError, ValueError) as error:
                        st.error(
                            "Data cadangan gagal dipulihkan. "
                            f"Detail: {error}"
                        )
                    else:
                        respon_list = respon_cadangan
                        st.session_state["respon_evaluasi"] = respon_cadangan
                        st.success(
                            f"Berhasil memulihkan {len(respon_cadangan)} respon."
                        )

        st.markdown("---")
        
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
            grafik_unduhan = []
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
                grafik_unduhan.append(
                    (
                        "dosen_favorit",
                        buat_gambar_batang_png(
                            df_fav,
                            "Dosen",
                            "Jumlah Suara",
                            "Kelas",
                            "Jumlah Suara Dosen Favorit per Kelas",
                        ),
                    )
                )
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
                grafik_unduhan.append(
                    (
                        "dosen_tidak_disukai",
                        buat_gambar_batang_png(
                            df_not_fav,
                            "Dosen",
                            "Jumlah Suara",
                            "Kelas",
                            "Jumlah Suara Dosen Tidak Disukai per Kelas",
                        ),
                    )
                )
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
                dosen_per_kelas_matkul = {
                    kelas: {
                        item["matkul"]: item["dosen"]
                        for item in jadwal
                    }
                    for kelas, jadwal in DATA_KELAS_JADWAL.items()
                }
                hasil_metode_grafik = hasil_metode.copy()
                hasil_metode_grafik["Mata Kuliah & Dosen"] = (
                    hasil_metode_grafik.apply(
                        lambda row: (
                            f'{row["Mata Kuliah"]}\n'
                            f'({dosen_per_kelas_matkul.get(row["Kelas"], {}).get(row["Mata Kuliah"], "Dosen tidak diketahui")})'
                        ),
                        axis=1,
                    )
                )
                hasil_metode_grafik = (
                    hasil_metode_grafik.groupby(
                        ["Mata Kuliah & Dosen", "Metode Pembelajaran"],
                        as_index=False,
                        sort=False,
                    )["Jumlah Respon"]
                    .sum()
                )
                fig_metode = px.bar(
                    hasil_metode_grafik,
                    x="Jumlah Respon",
                    y="Mata Kuliah & Dosen",
                    color="Metode Pembelajaran",
                    barmode="group",
                    orientation="h",
                    title="Distribusi Metode Pembelajaran per Mata Kuliah",
                    labels={
                        "Jumlah Respon": "Jumlah Respon",
                        "Mata Kuliah & Dosen": "Mata Kuliah (Dosen)",
                        "Metode Pembelajaran": "Metode",
                    },
                )
                fig_metode.update_layout(
                    yaxis={
                        "categoryorder": "array",
                        "categoryarray": hasil_metode_grafik[
                            "Mata Kuliah & Dosen"
                        ].drop_duplicates().tolist(),
                    },
                    legend_title_text="Metode Pembelajaran",
                )
                st.plotly_chart(fig_metode, use_container_width=True)
                grafik_unduhan.append(
                    (
                        "metode_pembelajaran",
                        buat_gambar_batang_png(
                            hasil_metode_grafik,
                            "Mata Kuliah & Dosen",
                            "Jumlah Respon",
                            "Metode Pembelajaran",
                            "Distribusi Metode Pembelajaran per Mata Kuliah",
                            horizontal=True,
                            show_values=True,
                        ),
                    )
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

            report_label = angkatan_filter
            nama_angkatan_pdf = (
                angkatan_filter.replace(" ", "_")
                if angkatan_filter != "Semua Angkatan"
                else "Semua_Angkatan"
            )
            pdf_file_name = f"Laporan_Evaluasi_Angkatan_{nama_angkatan_pdf}.pdf"
            pdf_bytes = generate_pdf_laporan_kelas(df_view, report_label)
            try:
                paket_bytes = buat_paket_hasil_laporan(
                    df_view,
                    respon_list,
                    grafik_unduhan,
                    pdf_bytes,
                    nama_angkatan_pdf,
                )
            except (OSError, RuntimeError, ValueError) as error:
                st.error(
                    "Paket unduhan lengkap gagal dibuat. Pastikan dependensi "
                    f"ekspor grafik sudah terpasang. Detail: {error}"
                )
            else:
                st.download_button(
                    label="Download Semua Hasil (ZIP)",
                    data=paket_bytes,
                    file_name=f"Semua_Hasil_Evaluasi_{nama_angkatan_pdf}.zip",
                    mime="application/zip",
                    help=(
                        "Berisi CSV laporan, cadangan seluruh respon, PDF, "
                        "dan gambar grafik yang tersedia."
                    ),
                )

            st.markdown("#### Cadangan Data Lengkap")
            st.warning(
                "Data disimpan di file lokal aplikasi. Di Streamlit Cloud, file "
                "dapat hilang saat aplikasi dimulai ulang atau diperbarui. Unduh "
                "cadangan sesering mungkin dan simpan di perangkat Anda."
            )
            cadangan_csv = (
                pd.DataFrame(_siapkan_respon_untuk_csv(respon_list))
                .to_csv(index=False)
                .encode("utf-8-sig")
            )
            waktu_cadangan = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="Download Cadangan Semua Data (CSV)",
                data=cadangan_csv,
                file_name=f"Cadangan_Evaluasi_Lengkap_{waktu_cadangan}.csv",
                mime="text/csv",
                help="Mencadangkan semua respon, tidak hanya angkatan yang sedang dipilih.",
            )

            st.markdown("---")
            st.subheader("📄 Download Laporan PDF per Angkatan")
            if pdf_bytes:
                st.download_button(
                    label="Download Laporan PDF",
                    data=pdf_bytes,
                    file_name=pdf_file_name,
                    mime="application/pdf"
                )
            else:
                st.warning("Data evaluasi belum cukup untuk membuat laporan PDF.")