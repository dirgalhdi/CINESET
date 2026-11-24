CINESET — Rekomendasi Film dengan Teori Himpunan
=================================================

CARA MEMBUKA DI VISUAL STUDIO CODE
1. Ekstrak file ZIP ini.
2. Buka Visual Studio Code.
3. Pilih File > Open Folder.
4. Pilih folder CINESET_VSCode hasil ekstrak.
5. Buka app.py untuk melihat atau mengedit kode.

CARA MENJALANKAN
Cara paling mudah:
1. Pastikan Python sudah terpasang.
2. Klik dua kali JALANKAN_CINESET.bat.
3. Tunggu instalasi Streamlit selesai.
4. Browser akan membuka aplikasi. Jika tidak, buka http://localhost:8501.
5. Jangan tutup jendela terminal selama aplikasi digunakan.

Menjalankan dari terminal VS Code:
1. Buka Terminal > New Terminal.
2. Jalankan:
   py -3.15 -m venv .venv
3. Jalankan:
   .venv\Scripts\python.exe -m pip install -r requirements.txt
4. Jalankan:
   .venv\Scripts\python.exe -m streamlit run app.py

Jika perintah py -3.15 tidak tersedia, gunakan interpreter Python 3.15 yang terpasang:
   python -m venv .venv
Lalu gunakan dua perintah .venv di atas.

CATATAN
- Instalasi library pertama kali memerlukan koneksi internet.
- Setelah library terpasang, aplikasi dan database film berjalan lokal.
- JALANKAN_CINESET.bat mencoba Python Launcher 3.15, perintah python, lalu lokasi Python pada screenshot pengguna.
- Jangan pindahkan app.py keluar dari folder proyek karena file BAT menjalankannya dari folder yang sama.

ISI PROYEK
app.py                  Program aplikasi.
requirements.txt        Daftar library.
JALANKAN_CINESET.bat    Instalasi dan menjalankan otomatis.
README.txt              Panduan ini.

MATERI TEORI HIMPUNAN
A. Himpunan: set genre pengguna dan set genre film.
B. Irisan: A & B.
C. Gabungan: A | B.
D. Kardinalitas: len(irisan) dan len(gabungan).
E. Jaccard Similarity: |A ∩ B| / |A ∪ B|.
