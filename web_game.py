import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Mastermind School", page_icon="🏫")
st.title("🎓 The Mastermind: School Takeover")

# 1. MASUKKAN API KEY KAMU
API_KEY = "AIzaSyDAu43dIY8KANIsxoNs2HZxBJ8_-GAQrRI"
genai.configure(api_key=API_KEY)

# 2. INISIALISASI MODEL (OTOMATIS MENCARI YANG AKTIF)
@st.cache_resource
def load_model():
    # Mencari model yang tersedia agar tidak 404
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

model = load_model()

# 3. MEMORI CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
    intro = "Tahun ajaran baru dimulai. OSIS sekolah dikuasai oleh geng elit. Kamu duduk di pojok kelas, merencanakan sesuatu yang besar. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Tampilkan Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. INPUT PEMAIN
if prompt := st.chat_input("Ketik strategimu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Instruksi sistem agar AI tetap jadi Game Master
        full_prompt = (
            "Kamu adalah Game Master 'The Mastermind'. "
            "Tema: Strategi mengambil alih sekolah. "
            "Berikan narasi pendek, status Reputasi & Pengaruh, dan 3 opsi aksi. "
            f"Pesan pemain: {prompt}"
        )
        
        response = model.generate_content(full_prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
        
    except Exception as e:
        st.error(f"Terjadi masalah: {e}")
        st.info("Tips: Tunggu 10 detik lalu coba lagi (mungkin karena limit kuota gratis).")
