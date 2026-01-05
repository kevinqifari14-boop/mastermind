import streamlit as st
import google.generativeai as genai
import urllib.parse

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

# 3. KONSISTENSI KARAKTER (Base Prompt)
# Edit bagian ini untuk merubah penampilan karakter utama kamu!
BASE_CHARACTER = "A high school boy, black messy hair, square glasses, Indonesian white and grey high school uniform, anime style, high quality."

# 4. INISIALISASI SESSION STATE
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
            if key in st.session_state: del st.session_state[key]
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🎓 The Mastermind: School Takeover")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Tampilkan gambar jika ada di dalam pesan assistant
        if "image_url" in msg:
            st.image(msg["image_url"], use_container_width=True)

# 5. LOGIKA INPUT & GENERASI GAMBAR
# 5. LOGIKA INPUT & GENERASI GAMBAR (VERSI STABIL)
if prompt := st.chat_input("Ketik strategimu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun() # Refresh agar chat user muncul duluan

# Cek pesan terakhir, jika dari user, maka assistant harus jawab
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_prompt = st.session_state.messages[-1]["content"]
    
   import random
import time

# ... (kode lainnya tetap sama)

# Di dalam bagian "if prompt :=" atau "if messages last role user":
    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang menyusun skenario & ilustrasi..."): 
            try:
                # 1. Instruksi super ketat untuk AI
                system_prompt = (
                    "Kamu GM RPG Sekolah. TEMA: Strategi menggulingkan OSIS elit. "
                    "LOKASI: SMA Pelita Jaya. "
                    "WAJIB: Berikan satu baris di akhir pesan: IMAGE_PROMPT: [1 deskripsi suasana singkat dalam Bahasa Inggris]"
                )
                
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
                full_query = f"{system_prompt}\n\n{history}\n\nPemain: {user_prompt}"
                
                response = model.generate_content(full_query)
                ai_text = response.text
                
                # 2. Pisahkan Narasi dan Deskripsi Gambar
                if "IMAGE_PROMPT:" in ai_text:
                    parts = ai_text.split("IMAGE_PROMPT:")
                    narasi = parts[0].strip()
                    img_desc = parts[1].strip().replace("[", "").replace("]", "").replace(".", "")
                else:
                    narasi = ai_text
                    img_desc = "high school hallway students"

                # 3. GENERASI URL GAMBAR (Optimasi Link)
                # Gunakan seed acak agar gambar tidak macet di satu versi
                seed_val = random.randint(1, 99999)
                # Tambahkan parameter 'nologo=true' dan 'flux' agar lebih bagus
                clean_desc = urllib.parse.quote(f"{BASE_CHARACTER}, {img_desc}, cinematic anime style, 4k")
                image_url = f"https://pollinations.ai/p/{clean_desc}?width=1024&height=512&seed={seed_val}&model=flux&nologo=true"

                # 4. TAMPILKAN HASIL
                st.markdown(narasi)
                
                # Trik: Gunakan st.image dengan handle error sederhana
                placeholder = st.empty()
                placeholder.image(image_url, caption="Ilustrasi Kejadian (Sedang Memuat...)", use_container_width=True)
                
                # Simpan ke memori
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": narasi, 
                    "image_url": image_url
                })
                
            except Exception as e:
                st.error(f"Gagal memuat AI: {e}")

