import streamlit as st
import google.generativeai as genai

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Mastermind: School Takeover", page_icon="🎓", layout="centered")

# --- KUNCI API (MENGGUNAKAN SECRETS) ---
# Di lokal, ini akan mencari di .streamlit/secrets.toml
# Di web, ini akan mencari di menu Settings > Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("🚨 API Key tidak ditemukan! Pastikan sudah memasukkan GEMINI_API_KEY di menu Secrets Streamlit.")
    st.stop()

# --- FUNGSI AI ---
def get_ai_response(user_prompt):
    # Gunakan model yang paling stabil
    model_name = 'gemini-1.5-flash'
    
    instruction = (
        "Kamu adalah Game Master 'The Mastermind'. "
        "Tema: Strategi mengambil alih sekolah. "
        "Aturan: Berikan narasi seru, tunjukkan status (Reputasi & Pengaruh), "
        "dan berikan 3 pilihan aksi (A, B, C) di akhir balasan."
    )

    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=instruction
        )
        # Mengambil riwayat chat untuk konteks
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"🚨 Terjadi kesalahan: {str(e)}"

# --- INTERFACE GAME ---
st.title("🎓 The Mastermind")
st.subheader("Misi: Kuasai Sekolah dengan Strategi")

# Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    intro = "Tahun ajaran baru dimulai. OSIS dikuasai oleh elit yang arogan. Kamu berdiri di depan gerbang sekolah dengan rencana rahasia. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Menampilkan Riwayat Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Pemain
if prompt := st.chat_input("Masukkan aksimu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang mengetik..."):
            jawaban = get_ai_response(prompt)
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})

# Tombol Reset
if st.sidebar.button("Mulai Ulang Game"):
    st.session_state.messages = []
    st.rerun()
