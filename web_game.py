import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Mastermind: School Takeover", page_icon="🎓")
st.title("🎓 The Mastermind")
st.subheader("Misi: Kuasai Sekolah dengan Strategi")

# Mengambil API Key dari Secrets Streamlit (Wajib diisi di Dashboard Streamlit)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("🚨 API Key tidak ditemukan di Secrets!")
    st.stop()

# Inisialisasi Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    intro = "Tahun ajaran baru dimulai. OSIS dikuasai oleh elit yang arogan. Kamu berdiri di depan gerbang sekolah dengan rencana rahasia. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Tampilkan Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Pemain
if prompt := st.chat_input("Masukkan aksimu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gabungkan instruksi dengan input user
            full_query = f"Instruksi: Kamu GM Game RPG Sekolah. Berikan narasi pendek, status, dan 3 opsi. Pesan pemain: {prompt}"
            response = model.generate_content(full_query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
