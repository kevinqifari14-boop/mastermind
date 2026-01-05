import streamlit as st
import google.generativeai as genai

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Mastermind School", page_icon="🏫", layout="wide")

# 1. API KEY
API_KEY = "AIzaSyDAu43dIY8KANIsxoNs2HZxBJ8_-GAQrRI"
genai.configure(api_key=API_KEY)

# 2. LOAD MODEL
@st.cache_resource
def load_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

model = load_model()

# 3. INISIALISASI STATUS GAME (SESSION STATE)
if "reputasi" not in st.session_state:
    st.session_state.reputasi = 10
if "pengaruh" not in st.session_state:
    st.session_state.pengaruh = 5
if "messages" not in st.session_state:
    st.session_state.messages = []
    intro = "Selamat datang, Mastermind. OSIS elit menguasai sekolah. Kamu mulai dari nol di pojok kelas. Apa langkah pertamamu?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# --- SIDEBAR: STATUS PLAYER (FITUR 1) ---
with st.sidebar:
    st.title("📊 Status Strategi")
    st.divider()
    
    # Menampilkan Bar Reputasi
    st.write(f"**Reputasi:** {st.session_state.reputasi}/100")
    st.progress(st.session_state.reputasi / 100)
    
    # Menampilkan Bar Pengaruh
    st.write(f"**Pengaruh:** {st.session_state.pengaruh}/100")
    st.progress(st.session_state.pengaruh / 100)
    
    st.divider()
    st.caption("Tips: Setiap tindakanmu mempengaruhi angka di atas. Jangan biarkan Reputasi menjadi 0!")
    
    if st.button("Mulai Ulang Game"):
        st.session_state.reputasi = 10
        st.session_state.pengaruh = 5
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🎓 The Mastermind: School Takeover")

# Tampilkan sejarah chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. INPUT PEMAIN DENGAN FITUR LOADING
if prompt := st.chat_input("Ketik strategimu di sini..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # FITUR LOADING: Spinner akan muncul saat AI sedang berpikir
    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang menyusun skenario..."): 
            try:
                # Instruksi sistem
                system_instruction = (
                    f"Kamu adalah Game Master 'The Mastermind'. "
                    f"Status saat ini: Reputasi {st.session_state.reputasi}, Pengaruh {st.session_state.pengaruh}. "
                    "Berikan narasi seru, tunjukkan perubahan status jika ada, dan berikan 3 opsi aksi."
                )
                
                # Panggil AI
                response = model.generate_content(f"{system_instruction}\n\nPemain: {prompt}")
                ai_response = response.text
                
                # Tampilkan jawaban
                st.markdown(ai_response)
                
                # Simpan ke memori
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Terjadi masalah: {e}")
