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
if prompt := st.chat_input("Ketik strategimu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Game Master sedang menyusun skenario & ilustrasi..."): 
            try:
                # Prompt untuk Cerita
                system_prompt = (
                    "Kamu GM RPG Sekolah. TEMA: Strategi menggulingkan OSIS. "
                    "LOKASI: Hanya di sekolah. DILARANG sci-fi/perusahaan. "
                    "WAJIB: Berikan satu baris singkat di akhir pesan dengan format: "
                    "IMAGE_PROMPT: [deskripsi suasana adegan dalam bahasa inggris]"
                )
                
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
                full_query = f"{system_prompt}\n\n{history}\n\nPemain: {prompt}"
                
                response = model.generate_content(full_query)
                ai_text = response.text
                
                # Pemisahan teks narasi dan prompt gambar
                narasi = ai_text.split("IMAGE_PROMPT:")[0]
                image_desc = "high school hallway" # default jika gagal parse
                if "IMAGE_PROMPT:" in ai_text:
                    image_desc = ai_text.split("IMAGE_PROMPT:")[1].strip()

                # Membuat URL Gambar (Pollinations AI)
                combined_prompt = f"{BASE_CHARACTER} {image_desc}, cinematic lighting, detailed background"
                encoded_prompt = urllib.parse.quote(combined_prompt)
                image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=512&seed=42&model=flux"

                # Tampilkan Hasil
                st.markdown(narasi)
                st.image(image_url, caption="Ilustrasi Kejadian")
                
                # Simpan ke history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": narasi, 
                    "image_url": image_url
                })
                
            except Exception as e:
                st.error(f"Terjadi masalah: {e}")
