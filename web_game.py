import streamlit as st
import google.generativeai as genai

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Mastermind School", page_icon="🏫", layout="wide")

# 1. API KEY GEMINI
API_KEY = "AIzaSyDAu43dIY8KANIsxoNs2HZxBJ8_-GAQrRI"
genai.configure(api_key=API_KEY)

# 2. LOAD MODEL GEMINI
@st.cache_resource
def load_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

model = load_model()

# 3. INISIALISASI SESSION STATE
if "messages" not in st.session_state:
    st.session_state.reputasi = 10
    st.session_state.pengaruh = 5
    st.session_state.messages = []
    intro = "Selamat datang, Mastermind. OSIS elit menguasai sekolah. Kamu mulai dari nol di pojok kelas. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# --- SIDEBAR: STATUS PLAYER ---
with st.sidebar:
    st.title("📊 Status Strategi")
    st.divider()
    st.write(f"**Reputasi:** {st.session_state.reputasi}/100")
    st.progress(st.session_state.reputasi / 100)
    st.write(f"**Pengaruh:** {st.session_state.pengaruh}/100")
    st.progress(st.session_state.pengaruh / 100)
    st.divider()
    if st.button("Mulai Ulang Game"):
        for key in ["reputasi", "pengaruh", "messages"]:
            if key in st.session_state: 
                del st.session_state[key]
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🎓 The Mastermind: School Takeover")

# Tampilkan sejarah chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. LOGIKA INPUT PEMAIN
if prompt := st.chat_input("Ketik strategimu..."):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Logika Assistant menjawab
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang berpikir..."): 
            try:
                # Instruksi sistem yang diperketat agar tetap di tema sekolah
                system_prompt = (
                    "Kamu GM RPG Sekolah. TEMA: Strategi menggulingkan OSIS elit. "
                    "LOKASI: SMA Pelita Jaya. DILARANG sci-fi atau tema luar sekolah. "
                    "Gunakan Bahasa Indonesia yang dramatis."
                )
                
                # Mengirimkan riwayat agar AI konsisten
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
                full_query = f"{system_prompt}\n\nRIWAYAT:\n{history}\n\nPemain: {user_prompt}"
                
                response = model.generate_content(full_query)
                ai_response = response.text
                
                # Tampilkan jawaban
                st.markdown(ai_response)
                
                # Simpan ke memori
                st.session_state.messages.append({"role": "assistant", "content
