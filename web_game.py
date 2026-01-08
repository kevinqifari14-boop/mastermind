import streamlit as st
import time

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="The Mastermind: Moriarty Protocol", page_icon="🕷️", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    text-align: left;
    white-space: pre-wrap;
    height: auto;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- GAME CONSTANTS ---
# Moriarty-level difficulty requires hidden flags (state)
# Kita simpan inventory/clue di session_state['flags']

GAME_SCENES = {
    # --- PROLOGUE: THE SPIDER'S WEB ---
    "start": {
        "text": (
            "🌑 **THE MASTERMIND: MORIARTY PROTOCOL**\n\n"
            "SMA Pelita Jaya bukan sekadar sekolah. Ini adalah miniatur negara korup.\n"
            "Ketua OSIS, **Kevin 'The King'**, bukan preman biasa. Dia jenius manipulatif. "
            "Dia punya mata-mata di setiap kelas. Dia tahu kamu datang sebelum kamu mendaftar.\n\n"
            "Kamu, **The Consultant**, harus menghancurkannya tanpa terdeteksi.\n"
            "Langkah pertama: Observasi. Jangan bertindak bodoh."
        ),
        "choices": {
            "1": "Masuk kelas dan perkenalkan diri dengan lantang (Cari perhatian).",
            "2": "Duduk di pojok, pura-pura baca buku, amati pola interaksi siswa.",
            "3": "Langsung ke ruang OSIS, tantang Kevin (Assertive)."
        },
        "next_logic": {
            "1": "game_over_instan_1", # Too loud
            "2": "phase1_observation", # Correct: Silent observer
            "3": "game_over_instan_2"  # Too arrogant
        }
    },
    
    # --- BAD ENDINGS (INSTANT) ---
    "game_over_instan_1": {
        "text": (
            "💀 **GAME OVER: THE FOOL**\n\n"
            "Kamu berteriak lantang. 5 menit kemudian, tasmu digeledah guru BP atas tuduhan membawa narkoba.\n"
            "Tentu saja itu palsu, ditaruh oleh anak buah Kevin. Kamu langsung dikeluarkan.\n"
            "**Pelajaran:** Jangan mencolok sebelum punya kuasa."
        ),
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
    "game_over_instan_2": {
        "text": (
            "💀 **GAME OVER: THE BUG**\n\n"
            "Kamu masuk ruang OSIS. Kevin tersenyum ramah, menyuguhkan teh.\n"
            "Besoknya kamu terbangun di Rumah Sakit dengan kaki patah. 'Kecelakaan', katanya.\n"
            "**Pelajaran:** Jangan menyerang raja tanpa pasukan."
        ),
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },

    # --- PHASE 1: OBSERVATION ---
    "phase1_observation": {
        "text": (
            "👁️ Kamu mengamati dalam diam. Kamu menemukan 3 anomali:\n"
            "A. Bendahara OSIS (Sarah) sering gugup saat melihat Kevin.\n"
            "B. Preman sekolah (Boim) diam-diam menerima amplop dari Kevin tiap Jumat.\n"
            "C. CCTV di lorong belakang selalu mati jam 2 siang.\n\n"
            "Mana titik lemah yang akan kamu eksploitasi? (Pilih dengan bijak, ini menentukan 'Senjata' akhirmu)."
        ),
        "choices": {
            "1": "Dekati Sarah (Eksploitasi Ketakutan).",
            "2": "Adu domba Boim (Eksploitasi Keserakahan).",
            "3": "Hacking CCTV (Eksploitasi Keamanan)."
        },
        "next_logic": {
            "1": "path_psychology",
            "2": "path_chaos",
            "3": "path_cyber"
        }
    },

    #Path 1: Psychology (Sarah)
    "path_psychology": {
        "text": (
            "🧠 Kamu mendekati Sarah. Bukan dengan ancaman, tapi empati palsu.\n"
            "Kamu tahu dia menggelapkan uang karena dipaksa Kevin.\n"
            "Kamu butuh bukti fisik. Sarah menyimpannya di buku harian di lokernya.\n\n"
            "Bagaimana cara mengambilnya?"
        ),
        "choices": {
            "1": "Bobol lokernya paksa saat sepi.",
            "2": "Tukar kunci lokernya saat dia lengah di jam olahraga.",
            "3": "Yakinkan dia untuk menyerahkannya demi 'keadilan'."
        },
        "next_logic": {
            "1": "game_over_trap_loker",
            "2": "get_intel_sarah",  # Success
            "3": "game_over_betrayal" # Sarah cepu
        }
    },
    "get_intel_sarah": {
        "text": (
            "🔑 Kunci tertukar sempurna. Kamu dapat buku hariannya.\n"
            "Isinya detail aliran dana pencucian uang Kevin ke rekening judi online.\n"
            "**[ITEM DIDAPAT: BUKU HITAM]**\n\n"
            "Tiba-tiba HP-mu berbunyi. Pesan dari nomor tak dikenal (Kevin).\n"
            "'Aku tahu kau mengambilnya. Temui aku di Rooftop atau Sarah kena akibatnya.'"
        ),
        "effects": {"flag": "buku_hitam", "intel": 100},
        "choices": {"1": "Ke Rooftop (Konfrontasi)"},
        "next": "phase2_confrontation"
    },

    # Path 2: Chaos (Boim)
    "path_chaos": {
        "text": (
            "🔥 Kamu mengirim surat kaleng ke Boim, seolah-olah dari Kevin, yang isinya menghina 'otot kecil' Boim.\n"
            "Boim mengamuk. Dia ingin menghajar Kevin. Ini kesempatanmu mengendalikan kekacauan.\n\n"
            "Apa instruksimu ke Boim?"
        ),
        "choices": {
            "1": "Suruh dia serang Kevin sekarang juga.",
            "2": "Tahan dia. Suruh dia kumpulkan preman lain untuk kudeta terstruktur.",
            "3": "Beri dia senjata tajam (Eskalasi)."
        },
        "next_logic": {
            "1": "game_over_chaos_failed",
            "2": "get_army_boim",
            "3": "game_over_criminal"
        }
    },
    "get_army_boim": {
        "text": (
            "🛡️ Boim tunduk padamu karena kamu terlihat tenang. Kamu sekarang punya pasukan bayangan.\n"
            "**[ITEM DIDAPAT: LOYALITAS PREMAN]**\n\n"
            "Kevin menyadari pergerakan massa. Dia memblokir semua akses pintu sekolah.\n"
            "Perang terbuka dimulai."
        ),
        "effects": {"flag": "pasukan", "intel": 50},
        "choices": {"1": "Mulai Revolusi"},
        "next": "phase2_war"
    },

    # Path 3: Cyber (CCTV) - HARD MODE
    "path_cyber": {
        "text": (
            "💻 Kamu mencoba meretas server sekolah lewat celah keamanan CCTV.\n"
            "Firewall Kevin ternyata berlapis. Ada *Honey Pot* (jebakan).\n"
            "Muncul pop-up: 'PASSWORD REQUIRED'.\n\n"
            "Hint dari observasi awal: Kevin narsis. Apa passwordnya?"
        ),
        "choices": {
            "1": "Admin123",
            "2": "TheKingKevin",
            "3": "PelitaJayaJaya"
        },
        "next_logic": {
            "1": "game_over_hacked",
            "2": "get_access_cyber",
            "3": "game_over_hacked"
        }
    },
    "get_access_cyber": {
        "text": (
            "🔓 AKSES DITERIMA. Kamu masuk ke database OSIS.\n"
            "Kamu menemukan rekaman CCTV Kevin sedang menyuap Kepala Sekolah.\n"
            "**[ITEM DIDAPAT: REKAMAN SKANDAL]**\n\n"
            "Sistem mendeteksi intrusi. Lokasimu terlacak. Satpam menuju ke arahmu."
        ),
        "effects": {"flag": "rekaman", "intel": 150}, # Strongest intel
        "choices": {"1": "Upload ke Cloud dan Kabur"},
        "next": "phase2_escape"
    },

    # --- PHASE 2: THE TRAP (MID GAME) ---
    "phase2_confrontation": {
        "text": (
            "🌪️ **PHASE 2: THE TRAP**\n\n"
            "Di Rooftop, Kevin tidak sendirian. Dia bersama polisi.\n"
            "'Dia mencuri buku harian Sarah!' teriak Kevin.\n"
            "Polisi menatapmu. Kamu memegang barang buktinya.\n\n"
            "Ini jebakan! Berpikir cepat!"
        ),
        "choices": {
            "1": "Serahkan buku itu dan menyerah.",
            "2": "Lempar buku itu ke bawah gedung (Hilangkan bukti).",
            "3": "Buka halaman 45, tunjukkan transaksi atas nama Pak Polisi itu sendiri (Bluff/Gambit)."
        },
        "next_logic": {
            "1": "game_over_jail",
            "2": "game_over_no_proof",
            "3": "win_gambit" # Only work if you have high insight from observation logic? (simplified here)
        }
    },
    "phase2_war": {
        "text": (
            "⚔️ **PHASE 2: CIVIL WAR**\n\n"
            "Pasukan Boim vs Pasukan OSIS. Tawuran massal di koridor.\n"
            "Kepala Sekolah histeris. Kevin mencoba kabur lewat pintu belakang membawa uang kas.\n\n"
            "Keputusan Jenderal?"
        ),
        "choices": {
            "1": "Perintahkan Boim menghancurkan segalanya (Burn it down).",
            "2": "Cegat Kevin sendiri di pintu belakang (Duel).",
            "3": "Lindungi Guru-guru agar mendapat simpati publik."
        },
        "next_logic": {
            "1": "game_over_anarchy",
            "2": "ending_duel",
            "3": "ending_political_victory"
        }
    },
    "phase2_escape": {
        "text": (
            "🏃 **PHASE 2: MANHUNT**\n\n"
            "Satu sekolah memburumu. Satpam, Guru, OSIS.\n"
            "Video sedang di-upload... 80%...\n"
            "Jalan buntu. Di depan ada Kevin memegang tongkat baseball.\n\n"
            "Tindakan?"
        ),
        "choices": {
            "1": "Lawan Kevin (Fisik).",
            "2": "Ulur waktu dengan dialog filosofis (Verbal).",
            "3": "Lompat ke pohon di sebelah jendela (Parkour)."
        },
        "next_logic": {
            "1": "game_over_beatdown", # Kevin is stronger
            "2": "ending_cyber_victory", # Time allows upload to finish
            "3": "game_over_fall"
        }
    },

    # --- ENDINGS ---
    "win_gambit": {
        "text": (
            "♟️ **TRUE ENDING: THE PUPPET MASTER**\n\n"
            "Kamu membuka halaman transaksi suap polisi. Wajah polisi itu pucat.\n"
            "Kevin terkejut. Kamu tersenyum, 'Gilliranmu, Pak Polisi. Tangkap anak ini atau karir Bapak tamat.'\n"
            "Kevin diseret pergi. Kamu tidak jadi Ketua OSIS. Kamu menjadi orang yang menunjuk Ketua OSIS.\n"
            "Kamu adalah Penguasa Bayangan SMA Pelita Jaya."
        ),
        "choices": {"1": "Main Lagi (Restart)"}, "next": "restart"
    },
    "ending_political_victory": {
        "text": (
            "🕊️ **GOOD ENDING: THE SAVIOR**\n\n"
            "Pasukanmu melindungi guru. Kevin tertangkap basah membawa uang kabur.\n"
            "Kamu dipuji sebagai pahlawan yang meredam kerusuhan.\n"
            "Kamu terpilih secara aklamasi. Sekolah damai."
        ),
        "choices": {"1": "Main Lagi (Restart)"}, "next": "restart"
    },
    "ending_cyber_victory": {
        "text": (
            "📺 **TECH ENDING: EXPOSED**\n\n"
            "'Kejahatan,' katamu, 'adalah masalah perspektif...'\n"
            "*PING!* Upload selesai. Seluruh HP siswa berbunyi notifikasi.\n"
            "Video Kevin menyuap Kepsek tayang live. Game over buat Kevin.\n"
            "Kamu menghilang dari sekolah, menjadi legenda urban hacker."
        ),
        "choices": {"1": "Main Lagi (Restart)"}, "next": "restart"
    },
    "ending_duel": {
        "text": (
            "🗡️ **NEUTRAL ENDING: MUTUALLY ASSURED DESTRUCTION**\n\n"
            "Kamu dan Kevin baku hantam. Keduanya babak belur masuk RS.\n"
            "Keduanya dikeluarkan. OSIS dibubarkan. Sekolah jadi anarkis tanpa pemimpin.\n"
            "Kamu menang, tapi dengan harga segalanya."
        ),
        "choices": {"1": "Main Lagi (Restart)"}, "next": "restart"
    },
    

    # --- MORE DEATH TRAPS ---
    "game_over_trap_loker": {
        "text": "Alarm berbunyi. Itu jebakan magnetik. Kamu tertangkap basah maling. Tamat.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
    "game_over_betrayal": {
        "text": "Sarah terlalu takut pada Kevin. Dia melaporkanmu. Kamu dikepung.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
    "game_over_chaos_failed": {
        "text": "Boim menyerang tanpa rencana dan dikeroyok massa OSIS. Kamu kehilangan pion.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
    "game_over_hacked": {
        "text": "Password Salah. Sistem mengunci ruangan. Gas tidur dilepaskan (oke ini agak lebay untuk sekolah, tapi Kevin itu gila).",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
    "game_over_beatdown": {
        "text": "Kamu bukan petarung. Kevin menghajarmu habis-habisan.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
     "game_over_jail": {
        "text": "Kamu ditangkap Polisi karena menyerahkan bukti curian. Kevin tertawa. Tamat.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
     "game_over_no_proof": {
        "text": "Kamu membuang bukti. Polisi tidak menemukan apa-apa, tapi Kevin menuduhmu mencemarkan nama baik. Kamu dikeluarkan.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
     "game_over_anarchy": {
        "text": "Sekolah terbakar habis. Semua orang ditangkap. Kamu menjadi raja abu.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    },
     "game_over_fall": {
        "text": "Kamu melompat ke pohon... dan rantingnya patah. Kamu jatuh. Kevin memotretmu yang sedang kesakitan.",
        "choices": {"1": "Ulangi Misi"},
        "next": "restart"
    }

}

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.inventory = []
    st.session_state.messages = []
    st.session_state.current_scene = "start"
    
    # Pesan awal
    intro = GAME_SCENES["start"]["text"]
    st.session_state.messages.append({"role": "assistant", "content": intro})

def reset_game():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

# --- UI ---
st.title("🕷️ Mastermind: Moriarty Protocol")
st.caption("Difficulty: EXTREME. Satu kesalahan = Game Over.")

# Container chat agar tombol selalu di bawah
chat_container = st.container()

# Logic Display Chat
with chat_container:
    for msg in st.session_state.messages:
        color = "red" if msg["role"] == "assistant" else "blue"
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- INPUT AREA (BUTTONS) ---
st.divider()
current_id = st.session_state.current_scene
scene_data = GAME_SCENES.get(current_id)
user_choice = None

if scene_data and "choices" in scene_data:
    st.write("👉 **Tentukan Langkahmu:**")
    # Buat tombol secara dinamis
    choices = scene_data["choices"]
    # Sorting keys agar urut 1, 2, 3
    sorted_keys = sorted(choices.keys())
    
    # Gunakan columns biar rapi kalau pendek, atau vertical stack kalau panjang
    # Untuk deskripsi panjang, lebih baik vertical stack (tanpa columns)
    for key in sorted_keys:
        desc = choices[key]
        if st.button(f"{desc}", key=f"btn_{key}_{current_id}", type="secondary"):
            user_choice = key

# --- CORE LOGIC PROCESSOR ---
if user_choice:
    # Simpan pilihan user ke chat
    choice_text = scene_data["choices"][user_choice]
    st.session_state.messages.append({"role": "user", "content": choice_text})
    
    next_id = None
    
    # Logic Handling
    # 1. Handle Restart
    if scene_data.get("next") == "restart":
        reset_game()
    
    # 2. Check Next Logic
    elif "next_logic" in scene_data and user_choice in scene_data["next_logic"]:
        next_id = scene_data["next_logic"][user_choice]
    
    # 3. Check Linear Next
    elif "next" in scene_data and user_choice == "1":
        next_id = scene_data["next"]
        
    # Process Next Scene
    if next_id:
        new_scene = GAME_SCENES.get(next_id)
        if new_scene:
            st.session_state.current_scene = next_id
            
            # Update Inventory/Flags if any
            if "effects" in new_scene:
                eff = new_scene["effects"]
                if "flag" in eff:
                    if "inventory" not in st.session_state: st.session_state.inventory = []
                    st.session_state.inventory.append(eff["flag"])
                    st.toast(f"ITEM DIDAPAT: {eff['flag']}")
            
            # Show Response
            response_text = new_scene["text"]
            
            # Animasi 'Thinking'
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("Menganalisis probabilitas..."):
                        time.sleep(0.5)
                        st.markdown(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            st.rerun() # Refresh agar tombol update
        else:
             st.error(f"Bug: Scene {next_id} not found.")
