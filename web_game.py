import streamlit as st
import google.generativeai as genai

# --- KUNCI API ---
API_KEY = "AIzaSyDAu43dIY8KANIsxoNs2HZxBJ8_-GAQrRI"
genai.configure(api_key=API_KEY)

# --- TAMPILAN WEB ---
st.set_page_config(page_title="Mastermind School", page_icon="🏫")
st.title("🎓 The Mastermind: School Takeover")
st.sidebar.info("Tujuan: Ambil alih sekolah dengan strategi otak.")

# Inisialisasi Model Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

# Inisialisasi Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Narasi Pembuka
    intro = "Tahun ajaran baru dimulai. OSIS sekolah dikuasai oleh geng elit. Kamu duduk di pojok kelas, merencanakan sesuatu yang besar. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Tampilkan Sejarah Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input Pemain
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Respon AI
    try:
        # Kita tambahkan instruksi sistem langsung di setiap pesan agar AI tetap jadi GM
        full_prompt = f"Instruksi: Kamu GM Game RPG Sekolah. Berikan narasi pendek dan 3 opsi. Pesan Pemain: {prompt}"
        response = model.generate_content(full_prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Terjadi masalah: {e}")