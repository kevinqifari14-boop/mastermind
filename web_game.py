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

# 3. INISIALISASI SESSION STATE
if "reputasi" not in st.session_state:
    st.session_state.reputasi = 10
if "pengaruh" not in st.session_state:
    st.session_state.pengaruh = 5
if "messages" not in st.session_state:
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
            del st.session_state[key]
        st.rerun()

# --- MAIN CHAT ---
st.title("🎓 The Mastermind: School Takeover")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. INPUT PEMAIN DENGAN LOGIKA KONSISTENSI
if prompt := st.chat_input("Ketik strategimu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang berpikir..."): 
            try:
                # KUNCI TEMA DI SINI (System Instruction yang diperketat)
                system_prompt = (
                    "KAMU ADALAH GAME MASTER UNTUK RPG SEKOLAH. "
                    "TEMA: Strategi menggulingkan kekuasaan OSIS elit di sekolah menengah. "
                    "LOKASI: Hanya di lingkungan sekolah (kelas, kantin, lapangan, ruang guru). "
                    "DILARANG KERAS berpindah ke tema futuristik, perusahaan, atau sci-fi. "
                    f"STATUS SAAT INI: Reputasi {st.session_state.reputasi}, Pengaruh {st.session_state.pengaruh}. "
                    "Gunakan gaya bahasa remaja yang serius tapi dramatis tentang politik sekolah."
                )

                # MENGIRIM SELURUH RIWAYAT (Agar AI ingat cerita sebelumnya)
                # Kita ambil 5 pesan terakhir saja agar tidak terlalu berat
                history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
                
                full_query = f"{system_prompt}\n\nRIWAYAT CERITA:\n{history_context}\n\nAKSI TERBARU PEMAIN: {prompt}"
                
                response = model.generate_content(full_query)
                ai_response = response.text
                
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Terjadi masalah: {e}")
