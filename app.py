import streamlit as st

st.set_page_config(
    page_title="CINESET | Rekomendasi Film",
    page_icon="🎬",
    layout="wide"
)

# =====================================================
# DATABASE FILM LOKAL
# Genre setiap film disimpan menggunakan set Python.
# Untuk menambah film, ikuti format data di bawah ini.
# =====================================================
FILMS = [
    {"title": "The Dark Knight", "year": 2008, "genres": {"Action", "Crime", "Drama", "Thriller"}},
    {"title": "Inception", "year": 2010, "genres": {"Action", "Adventure", "Sci-Fi", "Thriller"}},
    {"title": "Interstellar", "year": 2014, "genres": {"Adventure", "Drama", "Sci-Fi"}},
    {"title": "The Matrix", "year": 1999, "genres": {"Action", "Sci-Fi"}},
    {"title": "Avengers: Endgame", "year": 2019, "genres": {"Action", "Adventure", "Drama", "Sci-Fi"}},
    {"title": "John Wick", "year": 2014, "genres": {"Action", "Crime", "Thriller"}},
    {"title": "Jumanji: Welcome to the Jungle", "year": 2017, "genres": {"Action", "Adventure", "Comedy", "Fantasy"}},
    {"title": "The Hangover", "year": 2009, "genres": {"Comedy"}},
    {"title": "Home Alone", "year": 1990, "genres": {"Comedy", "Family"}},
    {"title": "La La Land", "year": 2016, "genres": {"Comedy", "Drama", "Music", "Romance"}},
    {"title": "The Notebook", "year": 2004, "genres": {"Drama", "Romance"}},
    {"title": "Titanic", "year": 1997, "genres": {"Drama", "Romance"}},
    {"title": "A Quiet Place", "year": 2018, "genres": {"Drama", "Horror", "Sci-Fi", "Thriller"}},
    {"title": "The Conjuring", "year": 2013, "genres": {"Horror", "Mystery", "Thriller"}},
    {"title": "Get Out", "year": 2017, "genres": {"Horror", "Mystery", "Thriller"}},
    {"title": "Coco", "year": 2017, "genres": {"Adventure", "Animation", "Comedy", "Family", "Fantasy"}},
    {"title": "Spider-Man: Into the Spider-Verse", "year": 2018, "genres": {"Action", "Adventure", "Animation", "Sci-Fi"}},
    {"title": "Frozen", "year": 2013, "genres": {"Adventure", "Animation", "Comedy", "Family", "Fantasy"}},
    {"title": "Harry Potter and the Sorcerer's Stone", "year": 2001, "genres": {"Adventure", "Family", "Fantasy"}},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001, "genres": {"Action", "Adventure", "Drama", "Fantasy"}},
    {"title": "Knives Out", "year": 2019, "genres": {"Comedy", "Crime", "Drama", "Mystery", "Thriller"}},
    {"title": "Shutter Island", "year": 2010, "genres": {"Drama", "Mystery", "Thriller"}},
    {"title": "Finding Nemo", "year": 2003, "genres": {"Adventure", "Animation", "Comedy", "Family"}},
    {"title": "Toy Story", "year": 1995, "genres": {"Adventure", "Animation", "Comedy", "Family", "Fantasy"}},
    {"title": "Mad Max: Fury Road", "year": 2015, "genres": {"Action", "Adventure", "Sci-Fi", "Thriller"}},
]

ALL_GENRES = sorted(set().union(*(film["genres"] for film in FILMS)))


# =====================================================
# PERHITUNGAN TEORI HIMPUNAN
# =====================================================
def analyze_sets(user_genres: set, movie_genres: set) -> dict:
    """Menghitung irisan, gabungan, kardinalitas, dan Jaccard."""
    intersection = user_genres & movie_genres
    union = user_genres | movie_genres

    intersection_count = len(intersection)
    union_count = len(union)

    similarity = intersection_count / union_count if union_count else 0.0

    return {
        "intersection": intersection,
        "union": union,
        "intersection_count": intersection_count,
        "union_count": union_count,
        "similarity": similarity,
    }


def match_label(score: float) -> str:
    if score >= 0.60:
        return "Sangat Cocok"
    if score >= 0.30:
        return "Cocok"
    return "Kurang Cocok"


def set_text(values: set) -> str:
    return "{ " + ", ".join(sorted(values)) + " }" if values else "∅ (himpunan kosong)"


# =====================================================
# CSS TEMA MONOKROM
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: radial-gradient(circle at 85% 0%, #292929 0, #111111 38%, #090909 100%);
    color: #f5f5f5;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: #111111; border-right: 1px solid #303030; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px; }
.hero {
    padding: 30px 32px; border: 1px solid #383838; border-radius: 24px;
    background: linear-gradient(125deg, #242424, #111111 68%);
    box-shadow: 0 18px 55px #0008; margin-bottom: 24px;
}
.eyebrow { color: #bdbdbd; letter-spacing: 3px; font-size: 11px; font-weight: 800; }
.hero h1 { font-family: 'Space Grotesk', sans-serif; font-size: clamp(34px, 5vw, 58px); line-height: 1.04; margin: 10px 0; color: white; }
.hero p { color: #bdbdbd; max-width: 760px; margin-bottom: 0; }
.metric-card {
    background: linear-gradient(145deg, #252525, #151515);
    border: 1px solid #383838; padding: 18px 20px; border-radius: 18px; min-height: 105px;
}
.metric-label { color: #a3a3a3; font-size: 12px; text-transform: uppercase; letter-spacing: 1.2px; }
.metric-value { font-family: 'Space Grotesk'; color: #fff; font-size: 30px; font-weight: 700; margin-top: 7px; }
.movie-card {
    background: linear-gradient(145deg, #252525, #151515);
    border: 1px solid #393939; border-radius: 18px; padding: 18px; margin-bottom: 10px;
    transition: all .2s ease;
}
.movie-card:hover { border-color: #bdbdbd; transform: translateY(-2px); box-shadow: 0 12px 30px #0007; }
.movie-title { font-family: 'Space Grotesk'; font-weight: 700; font-size: 18px; color: #fff; }
.movie-meta { color: #a3a3a3; font-size: 12px; }
.score { font-family: 'Space Grotesk'; font-size: 27px; font-weight: 700; color: #fff; }
.genre-chip {
    display: inline-block; border: 1px solid #555; color: #e5e5e5; background: #303030;
    padding: 4px 9px; border-radius: 30px; margin: 3px 4px 3px 0; font-size: 11px;
}
div.stButton > button {
    border-radius: 12px; border: 1px solid #777; background: #f2f2f2;
    color: #111; font-weight: 800; min-height: 45px; transition: .2s;
}
div.stButton > button:hover { background: #cfcfcf; border-color: white; color: #000; transform: translateY(-1px); }
.stProgress > div > div > div > div { background: linear-gradient(90deg, #777, #fff); }
div[data-baseweb="select"] > div { background: #202020; border-color: #555; }
.stTextInput input { background: #202020; color: white; border-color: #555; }
hr { border-color: #333; }
[data-testid="stExpander"] { border: 1px solid #393939; border-radius: 14px; background: #171717; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR DAN HEADER
# =====================================================
with st.sidebar:
    st.markdown("## 🎬 CINESET")
    st.caption("MOVIE DISCOVERY • SET THEORY")
    st.divider()
    st.markdown("**Tentang aplikasi**")
    st.write("Rekomendasi film berdasarkan kemiripan genre menggunakan Teori Himpunan.")
    st.divider()
    st.caption(f"Database lokal: {len(FILMS)} film")
    st.caption("Python + Streamlit")

st.markdown("""
<div class="hero">
    <div class="eyebrow">SMART MOVIE DISCOVERY / SET THEORY</div>
    <h1>Temukan film<br>yang satu selera.</h1>
    <p>Pilih genre favoritmu. CINESET membandingkan preferensimu dengan genre film menggunakan Himpunan, Irisan, Gabungan, Kardinalitas, dan Jaccard Similarity.</p>
</div>
""", unsafe_allow_html=True)

all_movie_genres = set().union(*(film["genres"] for film in FILMS))
col1, col2, col3 = st.columns(3)

for col, label, value in [
    (col1, "TOTAL FILM", len(FILMS)),
    (col2, "GENRE TERSEDIA", len(all_movie_genres)),
    (col3, "METODE REKOMENDASI", "Jaccard"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div></div>',
            unsafe_allow_html=True
        )


# =====================================================
# INPUT GENRE PENGGUNA (HIMPUNAN A)
# =====================================================
st.markdown("---")
st.caption("01 / PERSONAL PREFERENCE")
st.subheader("Genre favorit kamu")
st.write("Pilih satu atau beberapa genre. Genre tambahan juga bisa dimasukkan manual.")

selected_genres = st.multiselect(
    "Pilih genre",
    options=ALL_GENRES,
    default=["Action", "Sci-Fi"],
    placeholder="Pilih genre favorit..."
)

manual_input = st.text_input(
    "Tambah genre manual (pisahkan dengan koma)",
    placeholder="Contoh: Western, Documentary"
)

manual_genres = {
    item.strip().title()
    for item in manual_input.split(",")
    if item.strip()
}

# Set A: gabungan pilihan daftar dan input manual
user_genres = set(selected_genres) | manual_genres

if user_genres:
    st.markdown("**Himpunan genre pengguna (A):**")
    chips = " ".join(
        f'<span class="genre-chip">{genre}</span>'
        for genre in sorted(user_genres)
    )
    st.markdown(chips, unsafe_allow_html=True)
else:
    st.info("Pilih minimal satu genre untuk mendapatkan rekomendasi.")

col_a, col_b = st.columns(2)
with col_a:
    display_count = st.slider("Jumlah rekomendasi", 5, 20, 10)
with col_b:
    only_matches = st.checkbox("Sembunyikan film tanpa genre yang sama", value=True)


# =====================================================
# PERHITUNGAN DAN HASIL REKOMENDASI
# =====================================================
if user_genres:
    results = []

    for film in FILMS:
        analysis = analyze_sets(user_genres, film["genres"])
        results.append({**film, **analysis})

    # Urutkan dari nilai Jaccard tertinggi
    results.sort(
        key=lambda item: (item["similarity"], item["intersection_count"]),
        reverse=True
    )

    if only_matches:
        results = [item for item in results if item["intersection_count"] > 0]

    shown_results = results[:display_count]

    st.markdown("---")
    st.caption("02 / YOUR MATCHES")
    st.subheader("🎬 Rekomendasi film")
    st.caption("Urutan rekomendasi berdasarkan Jaccard Similarity tertinggi.")

    if not shown_results:
        st.warning("Belum ada film yang memiliki genre sama. Coba pilih genre lainnya.")
    else:
        for number, film in enumerate(shown_results, start=1):
            percentage = film["similarity"] * 100
            genre_chips = " ".join(
                f'<span class="genre-chip">{genre}</span>'
                for genre in sorted(film["genres"])
            )

            st.markdown(f"""
            <div class="movie-card">
                <div style="display:flex;justify-content:space-between;gap:15px;align-items:center;">
                    <div>
                        <div class="movie-title">{number:02d}. {film['title']}</div>
                        <div class="movie-meta">{film['year']} • {match_label(film['similarity'])}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="score">{percentage:.1f}%</div>
                        <div class="movie-meta">Jaccard Similarity</div>
                    </div>
                </div>
                <div style="margin-top:12px;">{genre_chips}</div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(film["similarity"], text=f"Tingkat kemiripan: {percentage:.1f}%")

            with st.expander(f"Lihat analisis himpunan — {film['title']}"):
                left, right = st.columns(2)

                with left:
                    st.markdown("**Himpunan A — Genre pengguna**")
                    st.code(set_text(user_genres))
                    st.markdown("**Himpunan B — Genre film**")
                    st.code(set_text(film["genres"]))

                with right:
                    st.markdown("**Irisan A ∩ B**")
                    st.code(set_text(film["intersection"]))
                    st.markdown("**Gabungan A ∪ B**")
                    st.code(set_text(film["union"]))

                metric1, metric2, metric3 = st.columns(3)
                metric1.metric("|A ∩ B|", film["intersection_count"])
                metric2.metric("|A ∪ B|", film["union_count"])
                metric3.metric("J(A,B)", f"{percentage:.1f}%")

                st.latex(r"J(A,B)=\frac{|A\cap B|}{|A\cup B|}")
                st.write(
                    f"Substitusi: {film['intersection_count']} ÷ "
                    f"{film['union_count']} = {film['similarity']:.4f} "
                    f"atau **{percentage:.1f}%**."
                )

    # Grafik bawaan Streamlit
    if shown_results:
        st.markdown("---")
        st.caption("03 / DATA INSIGHT")
        st.subheader("Perbandingan kemiripan")
        for film in shown_results:
            percentage = film["similarity"] * 100
            st.write(f"**{film['title']}** — {percentage:.1f}%")
            st.progress(film["similarity"])

st.markdown("---")
with st.expander("📘 Ringkasan penerapan materi Teori Himpunan"):
    st.markdown("""
    | Materi | Penerapan | Operasi Python |
    |---|---|---|
    | Himpunan | Genre pengguna (A) dan film (B) | `set()` |
    | Irisan (∩) | Genre yang sama | `A & B` |
    | Gabungan (∪) | Semua genre unik | `A | B` |
    | Kardinalitas | Jumlah anggota irisan dan gabungan | `len()` |
    | Jaccard Similarity | Perbandingan irisan terhadap gabungan | `len(A & B) / len(A | B)` |
    """)
    st.info("Jika gabungan kosong, program menetapkan nilai Jaccard menjadi 0 agar tidak terjadi pembagian dengan nol.")

st.caption("CINESET • Implementasi Teori Himpunan menggunakan Python")
