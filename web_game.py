import streamlit as st
import google.generativeai as genai

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Mastermind: School Takeover", page_icon="🎓", layout="centered")

# --- KUNCI API ---
# Jika menggunakan Streamlit Secrets (Disarankan):
# API_KEY = st.secrets["GEMINI_API_KEY"]
# Jika cara biasa (Paste langsung):
API_KEY = "AIzaSyDAu43dIY8KANIsxoNs2HZxBJ8_-GAQrRI"

genai.configure(api_key=API_KEY)

# --- FUNGSI AI (ANTI-ERROR 404) ---
def get_ai_response(user_prompt):
    # Mencoba daftar model yang paling mungkin tersedia
    model_variants = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    
    instruction = (
        "Kamu adalah Game Master 'The Mastermind'. "
        "Tema: Strategi mengambil alih sekolah. "
        "Aturan: Berikan narasi seru, tunjukkan status (Reputasi & Pengaruh), "
        "dan berikan 3 pilihan aksi (A, B, C) di akhir balasan."
    )

    for model_name in model_variants:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=instruction
            )
            response = model.generate_content(user_prompt)
            return response.text
        except Exception:
            continue
    
    return "🚨 Server AI sedang sibuk atau API Key bermasalah. Coba refresh halaman."

# --- INTERFACE GAME ---
st.title("🎓 The Mastermind")
st.subheader("Misi: Kuasai Sekolah dengan Strategi")

# Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Pesan pembuka otomatis
    intro = "Tahun ajaran baru dimulai. OSIS dikuasai oleh elit yang arogan. Kamu berdiri di depan gerbang sekolah dengan rencana rahasia. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Menampilkan Riwayat Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Pemain
if prompt := st.chat_input("Masukkan aksimu..."):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang mengetik..."):
            jawaban = get_ai_response(prompt)
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})

# Tombol Reset Game di Sidebar
if st.sidebar.button("Mulai Ulang Game"):
    st.session_state.messages = []
    st.rerun()
