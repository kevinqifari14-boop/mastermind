import streamlit as st
import time
import os

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Moriarty School: Gothic Edition", page_icon="🕸️", layout="wide")

# --- CUSTOM CSS: GOTHIC / SPIDER AESTHETIC ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=Metal+Mania&family=Roboto+Mono:wght@400;700&display=swap');

/* BACKGROUND & GLOBAL TEXT */
.stApp {
    background-color: #0a0a0a;
    background-image: radial-gradient(circle at 50% 50%, #1a0505 0%, #000000 100%);
    color: #e0e0e0;
}

/* HEADERS */
h1, h2, h3 {
    font-family: 'Metal Mania', cursive !important;
    color: #ff3333 !important;
    text-shadow: 2px 2px 4px #000000;
    letter-spacing: 2px;
}

/* CHAT BUBBLES */
.stChatMessage {
    background-color: rgba(20, 0, 0, 0.6) !important;
    border: 1px solid #4a0000;
    border-radius: 5px;
    font-family: 'Roboto Mono', monospace;
}
[data-testid="stChatMessageContent"] {
    color: #dcdcdc !important;
}

/* BUTTONS */
div.stButton > button {
    width: 100%;
    text-align: left;
    margin-bottom: 8px;
    height: auto;
    padding: 15px;
    border-radius: 0px;
    background: linear-gradient(90deg, #1a0000 0%, #330000 100%);
    color: #ffcccc !important;
    border: 1px solid #660000;
    font-family: 'Roboto Mono', monospace;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #4d0000 0%, #800000 100%);
    border-color: #ff0000;
    transform: translateX(5px);
    box-shadow: -2px 0 10px rgba(255, 0, 0, 0.3);
}

/* LOCKED BUTTONS */
.locked-button {
    background-color: #111 !important;
    color: #444 !important;
    border: 1px dashed #333 !important;
    cursor: not-allowed;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #050505;
    border-right: 1px solid #330000;
}
[data-testid="stSidebar"] h1 {
    font-family: 'Creepster', cursive !important;
    font-size: 40px;
    background: -webkit-linear-gradient(#ff0000, #550000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div {
    background-color: #cc0000;
}

/* SPIDER WEB DECORATION (CSS ART) */
.spider-web-corner {
    position: fixed;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: repeating-radial-gradient(
        circle at 100% 0%, 
        transparent 0, 
        transparent 10px, 
        #330000 11px, 
        #330000 12px
    );
    opacity: 0.5;
    pointer-events: none;
    z-index: 999;
}
</style>

<div class="spider-web-corner"></div>
""", unsafe_allow_html=True)

# --- GAME DATA (SAME LOGIC, JUST VISUAL UPDATE) ---
# Struktur: 25 Acts Linear Progression with Branching Outcomes

# --- ILLUSTRATION SYSTEM ---
ILLUSTRATIONS = {
    # ACT 1-3: Introduction
    "start": "assets/illustrations/act_01_arrival.png",
    "act1_win": "assets/illustrations/act_01_arrival.png",
    "act1_safe": "assets/illustrations/act_01_arrival.png",
    "act1_rich": "assets/illustrations/act_01_arrival.png",
    
    "act2": "assets/illustrations/act_02_invitation.png",
    "act2_boss": "assets/illustrations/act_02_invitation.png",
    "act2_spy": "assets/illustrations/act_02_invitation.png",
    
    "act3": "assets/illustrations/act_01_arrival.png",  # Reuse arrival for Act 3
    "act3_win": "assets/illustrations/act_01_arrival.png",
    "act3_lose": "assets/illustrations/act_01_arrival.png",
    "act3_smart": "assets/illustrations/act_01_arrival.png",
    
    # ACT 4-10: Building the Empire
    "act4": "assets/illustrations/act_04_basketball.png",
    "act4_tutor": "assets/illustrations/act_04_basketball.png",
    "act4_cheat": "assets/illustrations/act_04_basketball.png",
    "act4_fail": "assets/illustrations/act_04_basketball.png",
    
    "act5": "assets/illustrations/act_04_basketball.png",  # Reuse for science club
    "act5_hack": "assets/illustrations/act_04_basketball.png",
    "act5_good": "assets/illustrations/act_04_basketball.png",
    "act5_skip": "assets/illustrations/act_04_basketball.png",
    
    "act6": "assets/illustrations/act_06_sabotage.png",
    "act6_spy": "assets/illustrations/act_06_sabotage.png",
    "act6_psycho": "assets/illustrations/act_06_sabotage.png",
    "act6_petty": "assets/illustrations/act_06_sabotage.png",
    
    "act7": "assets/illustrations/act_04_basketball.png",  # Exam scene
    "act7_rival": "assets/illustrations/act_04_basketball.png",
    "act7_expose": "assets/illustrations/act_04_basketball.png",
    "act7_ignore": "assets/illustrations/act_04_basketball.png",
    
    "act8": "assets/illustrations/act_04_basketball.png",  # Futsal scene
    "act8_chaos": "assets/illustrations/act_04_basketball.png",
    "act8_rich": "assets/illustrations/act_04_basketball.png",
    "act8_lose": "assets/illustrations/act_04_basketball.png",
    
    "act9": "assets/illustrations/act_06_sabotage.png",  # Canteen
    "act9_boikot": "assets/illustrations/act_06_sabotage.png",
    "act9_demo": "assets/illustrations/act_06_sabotage.png",
    "act9_skip": "assets/illustrations/act_06_sabotage.png",
    
    "act10": "assets/illustrations/act_02_invitation.png",  # Elara scene
    "act10_ally": "assets/illustrations/act_02_invitation.png",
    "act10_check": "assets/illustrations/act_02_invitation.png",
    "act10_date": "assets/illustrations/act_02_invitation.png",
    
    # ACT 11-15: Dismantling Lieutenants
    "act11": "assets/illustrations/act_11_sarah.png",
    "act11_safe": "assets/illustrations/act_11_sarah.png",
    "act11_attack": "assets/illustrations/act_11_sarah.png",
    "act11_fail": "assets/illustrations/act_11_sarah.png",
    
    "act12": "assets/illustrations/act_06_sabotage.png",  # Leo scene
    "act12_fight": "assets/illustrations/act_06_sabotage.png",
    "act12_cruel": "assets/illustrations/act_06_sabotage.png",
    "act12_bribe": "assets/illustrations/act_06_sabotage.png",
    
    "act13": "assets/illustrations/act_13_principals_office.png",
    "act13_stealth": "assets/illustrations/act_13_principals_office.png",
    "act13_bribe": "assets/illustrations/act_13_principals_office.png",
    "act13_skip": "assets/illustrations/act_13_principals_office.png",
    
    "act14": "assets/illustrations/act_02_invitation.png",  # Pensi - use party image
    "act14_video": "assets/illustrations/act_02_invitation.png",
    "act14_sound": "assets/illustrations/act_02_invitation.png",
    "act14_boring": "assets/illustrations/act_02_invitation.png",
    
    "act15": "assets/illustrations/act_11_sarah.png",  # Budget leak
    "act15_hero": "assets/illustrations/act_11_sarah.png",
    "act15_coward": "assets/illustrations/act_11_sarah.png",
    
    # ACT 16-20: Escalation
    "act16": "assets/illustrations/act_06_sabotage.png",  # War scene
    "act16_war": "assets/illustrations/act_06_sabotage.png",
    "act16_diplo": "assets/illustrations/act_06_sabotage.png",
    "act16_hide": "assets/illustrations/act_06_sabotage.png",
    
    "act17": "assets/illustrations/act_13_principals_office.png",  # Propaganda
    "act17_press": "assets/illustrations/act_13_principals_office.png",
    "act17_hack": "assets/illustrations/act_13_principals_office.png",
    "act17_fail": "assets/illustrations/act_13_principals_office.png",
    
    "act18": "assets/illustrations/act_11_sarah.png",  # Teacher strike
    "act18_lead": "assets/illustrations/act_11_sarah.png",
    "act18_traitor": "assets/illustrations/act_11_sarah.png",
    "act18_kind": "assets/illustrations/act_11_sarah.png",
    
    "act19": "assets/illustrations/act_06_sabotage.png",  # Frame up
    "act19_reverse": "assets/illustrations/act_06_sabotage.png",
    "act19_flush": "assets/illustrations/act_06_sabotage.png",
    "act19_crazy": "assets/illustrations/act_06_sabotage.png",
    
    "act20": "assets/illustrations/act_01_arrival.png",  # Suspension
    
    # ACT 21-25: Endgame
    "act21": "assets/illustrations/act_01_arrival.png",  # Return of King
    "act21_march": "assets/illustrations/act_01_arrival.png",
    "act21_car": "assets/illustrations/act_01_arrival.png",
    "act21_police": "assets/illustrations/act_01_arrival.png",
    
    "act22": "assets/illustrations/act_13_principals_office.png",  # Debate prep
    "act23_nuke": "assets/illustrations/act_02_invitation.png",  # Grand debate
    "act23_logic": "assets/illustrations/act_02_invitation.png",
    
    "act24": "assets/illustrations/act_11_sarah.png",  # Voting day
    "act25_result": "assets/illustrations/act_11_sarah.png",
    "ending_calc": "assets/illustrations/act_11_sarah.png",
    
    # Endings
    "end_victory": "assets/illustrations/act_01_arrival.png",
    "end_close": "assets/illustrations/act_01_arrival.png",
    "end_lose": "assets/illustrations/act_01_arrival.png",
}

def display_illustration(scene_id):
    """Display illustration for current scene with gothic border"""
    if scene_id in ILLUSTRATIONS:
        img_path = ILLUSTRATIONS[scene_id]
        if os.path.exists(img_path):
            # Display with custom styling
            st.markdown("""
                <style>
                .illustration-frame {
                    border: 3px solid #660000;
                    border-radius: 5px;
                    box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
                    margin: 10px 0;
                }
                </style>
            """, unsafe_allow_html=True)
            st.image(img_path, use_container_width=True)

GAME_SCENES = {
    # --- ACT 1-3: INTRODUCTION ---
    "start": {
        "act": 1,
        "text": "**ACT 1: THE ARRIVAL**\n\nSMA Pelita Jaya. Kamu murid baru. Kevin 'The King' adalah penguasa mutlak sekolah ini.\nTugas pertamamu: Cari perhatian atau cari aman?",
        "choices": {
            "1": "Cari masalah dengan preman kantin (Risk: High).",
            "2": "Kerjakan PR teman sekelas (Safe).",
            "3": "Sogok Admin TU untuk data siswa (Money)."
        },
        "next_logic": {"1": "act1_win", "2": "act1_safe", "3": "act1_rich"}
    },
    "act1_win": {"act": 1, "text": "Kamu menghajar preman kantin. Satu sekolah kaget. (Rep +30)", "effects": {"rep": 30}, "next": "act2"},
    "act1_safe": {"act": 1, "text": "Kamu membangun jaringan lewat jasa joki PR. (Rep +10)", "effects": {"rep": 10}, "next": "act2"},
    "act1_rich": {"act": 1, "text": "Kamu punya data alamat semua siswa. Aset berharga. (Rep +10, Intel+1)", "effects": {"rep": 10, "flag": "data_siswa"}, "next": "act2"},

    "act2": {
        "act": 2, 
        "text": "**ACT 2: THE INVITATION**\n\nKevin mengundangmu ke pesta VIP-nya. Dia ingin mengetesmu.",
        "choices": {"1": "Datamg bergaya Bos (Butuh Rep 20).", "2": "Menyusup jadi pelayan."},
        "req_rep": {"1": 20},
        "next_logic": {"1": "act2_boss", "2": "act2_spy"}
    },
    "act2_boss": {"act": 2, "text": "Kamu mendominasi pesta. Kevin mulai waspada. (Rep +20)", "effects": {"rep": 20}, "next": "act3"},
    "act2_spy": {"act": 2, "text": "Kamu merekam percakapan Kevin dengan bandar judi. (Intel+1)", "effects": {"flag": "rekaman_judi"}, "next": "act3"},

    "act3": {
        "act": 3,
        "text": "**ACT 3: THE FIRST CLASH**\n\nKevin mengirim anak buahnya untuk 'memberi peringatan' di parkiran.",
        "choices": {"1": "Lawan keroyokan (Butuh Rep 50).", "2": "Kabur dan lapor Guru.", "3": "Jebak mereka ke area CCTV."},
        "req_rep": {"1": 50},
        "next_logic": {"1": "act3_win", "2": "act3_lose", "3": "act3_smart"}
    },
    "act3_win": {"act": 3, "text": "Kamu menghabisi 5 orang sendirian. Legenda lahir. (Rep +50)", "effects": {"rep": 50}, "next": "act4"},
    "act3_lose": {"act": 3, "text": "Kamu dianggap cepu. Reputasi turun. (Rep -10)", "effects": {"rep": -10}, "next": "act4"},
    "act3_smart": {"act": 3, "text": "Mereka tertangkap CCTV dan diskors. Kemenangan taktis. (Rep +20)", "effects": {"rep": 20}, "next": "act4"},

    # --- ACT 4-10: BUILDING THE EMPIRE (CLUBS & INFLUENCE) ---
    "act4": {
        "act": 4,
        "text": "**ACT 4: BASKETBALL DIPLOMACY**\n\nKapten Basket, Rio, adalah idola sekolah tapi bodoh akademik. Dia terancam tidak naik kelas.\nJika kamu membantunya, kamu dapat dukungan atlet.",
        "choices": {"1": "Jadi tutor privatnya.", "2": "Curi kunci jawaban ujian buat dia.", "3": "Biarkan dia tidak naik (Singkirkan saingan)."},
        "next_logic": {"1": "act4_tutor", "2": "act4_cheat", "3": "act4_fail"}
    },
    "act4_tutor": {"act": 4, "text": "Rio lulus. Tim Basket sekarang melindungimu. (Rep +20)", "effects": {"rep": 20, "flag": "dukungan_basket"}, "next": "act5"},
    "act4_cheat": {"act": 4, "text": "Rio lulus tapi kamu memegang rahasianya. Blackmail material. (Rep +10, Intel+1)", "effects": {"rep": 10, "flag": "kartu_as_rio"}, "next": "act5"},
    "act4_fail": {"act": 4, "text": "Rio tinggal kelas. Satu masalah hilang, tapi tim basket membencimu.", "next": "act5"},

    "act5": {
        "act": 5,
        "text": "**ACT 5: THE SCIENCE CLUB**\n\nKlub Sains sedang merakit robot tapi kekurangan dana. Kevin menolak proposal mereka.",
        "choices": {"1": "Galang dana dari siswa lain.", "2": "Hack rekening OSIS untuk transfer dana 'siluman'.", "3": "Abaikan."},
        "next_logic": {"1": "act5_good", "2": "act5_hack", "3": "act5_skip"}
    },
    "act5_hack": {"act": 5, "text": "Risky tapi sukses! Klub Sains memberimu gadget sadap. (Intel+2, Gadget Get)", "effects": {"flag": "alat_sadap", "rep": 10}, "next": "act6"},
    "act5_good": {"act": 5, "text": "Kamu pahlawan kaum nerd. (Rep +15)", "effects": {"rep": 15}, "next": "act6"},
    "act5_skip": {"act": 5, "text": "Kamu melewatkan peluang.", "next": "act6"},

    "act6": {
        "act": 6,
        "text": "**ACT 6: SABOTAGE**\n\nMotor Ninja kesayangan Kevin parkir sembarangan. CCTV area ini mati (kamu cek di Act 1/5).",
        "choices": {"1": "Gores catnya (Petty).", "2": "Potong kabel rem (Moriarty Style).", "3": "Pasang pelacak GPS (Intel)."},
        "next_logic": {"1": "act6_petty", "2": "act6_psycho", "3": "act6_spy"}
    },
    "act6_spy": {"act": 6, "text": "Pelacak terpasang. Sekarang kamu tahu kemana Kevin pergi sepulang sekolah. (Intel+1)", "effects": {"flag": "lokasi_kevin"}, "next": "act7"},
    "act6_psycho": {"act": 6, "text": "Kevin kecelakaan ringan. Dia jadi paranoid. Sekolah diperketat. (Chaos +1)", "effects": {"rep": 10}, "next": "act7"},
    "act6_petty": {"act": 6, "text": "Kevin marah-marah di story IG. Tidak berdampak besar.", "next": "act7"},

    "act7": {
        "act": 7,
        "text": "**ACT 7: MIDTERM EXAMS**\n\nUjian Tengah Semester. Nilai adalah mata uang lain di sini.\nKevin menjual kunci jawaban palsu ke siswa bodoh.",
        "choices": {"1": "Bongkar penipuan Kevin.", "2": "Buat kunci jawaban tandingan yang akurat (Gratis).", "3": "Fokus ujian sendiri (Nerd)."},
        "next_logic": {"1": "act7_expose", "2": "act7_rival", "3": "act7_ignore"}
    },
    "act7_rival": {"act": 7, "text": "Kunci jawabanmu benar! Siswa beralih memuja otakmu. (Rep +30)", "effects": {"rep": 30}, "next": "act8"},
    "act7_expose": {"act": 7, "text": "Kevin berkilah 'itu cuma prediksi'. Kamu kurang bukti kuat.", "next": "act8"},
    "act7_ignore": {"act": 7, "text": "Kamu dapat Rangking 1. Guru sayang padamu. (Rep +10)", "effects": {"rep": 10}, "next": "act8"},

    "act8": {
        "act": 8,
        "text": "**ACT 8: CLASS MEETING**\n\nLomba futsal antar kelas. Tensi tinggi. Wasitnya disogok Kevin.",
        "choices": {"1": "Main jujur walaupun dicurangi.", "2": "Bayar wasit lebih tinggi (Butuh Uang/Rep).", "3": "Provokasi tawuran penonton."},
        "next_logic": {"1": "act8_lose", "2": "act8_rich", "3": "act8_chaos"}
    },
    "act8_chaos": {"act": 8, "text": "Tawuran pecah! Lomba bubar. Otoritas OSIS dipertanyakan karena gagal jaga keamanan. (Rep +15)", "effects": {"rep": 15}, "next": "act9"},
    "act8_rich": {"act": 8, "text": "Kamu menang lomba. Uang adalah raja. (Rep +20)", "effects": {"rep": 20}, "next": "act9"},
    "act8_lose": {"act": 8, "text": "Kamu kalah terhormat. Simpati publik naik sedikit. (Rep +5)", "effects": {"rep": 5}, "next": "act9"},

    "act9": {
        "act": 9,
        "text": "**ACT 9: THE CANTOR MONOPOLY**\n\nIbu Kantin curhat lagi. Uang sewa dinaikkan 200%. Kevin mau mengganti kantin dengan franchise milik bapaknya.",
        "choices": {"1": "Demo masak di lapangan (Protes Kreatif).", "2": "Ancam boikot total seluruh siswa.", "3": "Biarkan (Siapa peduli kantin?)."},
        "next_logic": {"1": "act9_demo", "2": "act9_boikot", "3": "act9_skip"}
    },
    "act9_boikot": {"act": 9, "text": "Boikot berhasil! Omzet kantin 0 rupiah. Kevin terpaksa batalkan kenaikan sewa. (Rep +25)", "effects": {"rep": 25}, "next": "act10"},
    "act9_demo": {"act": 9, "text": "Viral di TikTok. Alumni sekolah ikut mengecam Kevin. (Rep +20)", "effects": {"rep": 20}, "next": "act10"},
    "act9_skip": {"act": 9, "text": "Kantin diganti burger mahal. Siswa miskin kelaparan. Kamu kehilangan dukungan rakyat kecil.", "effects": {"rep": -10}, "next": "act10"},

    "act10": {
        "act": 10,
        "text": "**ACT 10: THE TRANSFER STUDENT**\n\nAnak baru bernama 'Elara' masuk. Dia cantik, kaya, dan benci Kevin. Potensi sekutu atau rival?",
        "choices": {"1": "Ajak dia kencan (Romance).", "2": "Ajak aliansi politik.", "3": "Selidiki latar belakangnya dulu (Paranoid)."},
        "next_logic": {"1": "act10_date", "2": "act10_ally", "3": "act10_check"}
    },
    "act10_ally": {"act": 10, "text": "Elara setuju. Bapaknya donatur yayasan. Kamu dapat suntikan dana. (Rep +20)", "effects": {"rep": 20, "flag": "dana_elara"}, "next": "act11"},
    "act10_check": {"act": 10, "text": "Ternyata dia sepupu jauh Kevin yang mau kudeta! Info bagus. (Intel+1)", "effects": {"flag": "rahasia_elara"}, "next": "act11"},
    "act10_date": {"act": 10, "text": "Dia menolakmu. Fokus ke misi, jangan bucin!", "choices": {"1": "Lanjut"}, "next": "act11"},

    # --- ACT 11-15: DISMANTLING THE LIEUTENANTS ---
    "act11": {
        "act": 11,
        "text": "**ACT 11: TARGET - SARAH (BENDAHARA)**\n\nSarah adalah kunci keuangan. Kita perlu menyingkirkannya.",
        "choices": {"1": "Teror mental (Kirim paket bangkai tikus).", "2": "Pendekatan persuasif (Tawarkan perlindungan).", "3": "Fitnah dia menggelapkan uang (Padahal emang iya)."},
        "next_logic": {"1": "act11_fail", "2": "act11_safe", "3": "act11_attack"}
    },
    "act11_safe": {"act": 11, "text": "Sarah luluh. Dia menyerahkan buku kas asli padamu diam-diam. (Intel+++)", "effects": {"flag": "buku_kas_asli", "rep": 10}, "next": "act12"},
    "act11_attack": {"act": 11, "text": "Sarah dipecat Kevin. Tapi dia tidak memberimu info apa-apa. Musuh berkurang satu.", "next": "act12"},
    "act11_fail": {"act": 11, "text": "Sarah lapor polisi. Kamu hampir tertangkap. (Rep -20)", "effects": {"rep": -20}, "next": "act12"},

    "act12": {
        "act": 12,
        "text": "**ACT 12: TARGET - LEO (KEAMANAN)**\n\nLeo si kepala keamanan sekolah (Siswa). Badannya besar, otaknya kecil. Dia tameng fisik Kevin.",
        "choices": {"1": "Adu domba dia dengan anak STM sebelah.", "2": "Sogok dia dengan voucher game.", "3": "Jebak dia dengan narkoba (Extreme)."},
        "next_logic": {"1": "act12_fight", "2": "act12_bribe", "3": "act12_cruel"}
    },
    "act12_fight": {"act": 12, "text": "Leo babak belur dihajar anak STM. Dia masuk RS. Kevin kehilangan ototnya. (Rep +15)", "effects": {"rep": 15}, "next": "act13"},
    "act12_cruel": {"act": 12, "text": "**MORIARTY MOVE.** Leo ditangkap polisi. Sekolah gempar. Kevin mulai ketakutan setengah mati padamu. (Rep +40, Fear +Max)", "effects": {"rep": 40}, "next": "act13"},
    "act12_bribe": {"act": 12, "text": "Leo mau info, tapi jasanya mahal. Tidak worth it.", "next": "act13"},

    "act13": {
        "act": 13,
        "text": "**ACT 13: THE PRINCIPAL'S OFFICE**\n\nMalam hari. Kantor Kepsek kosong. Ada rumor Kepsek juga korup.",
        "choices": {"1": "Menyusup masuk (Stealth).", "2": "Bayar penjaga sekolah.", "3": "Urungkan niat (Safe)."},
        "next_logic": {"1": "act13_stealth", "2": "act13_bribe", "3": "act13_skip"}
    },
    "act13_stealth": {"act": 13, "text": "Kamu menemukan kwitansi palsu pembangunan gedung! Ini bom atom buat Kevin & Kepsek. (Intel+++)", "effects": {"flag": "kwitansi_palsu"}, "next": "act14"},
    "act13_bribe": {"act": 13, "text": "Penjaga sekolah cepu ke Kevin. Kamu ketahuan! Kabur! (Rep -30)", "effects": {"rep": -30}, "next": "act14"},
    "act13_skip": {"act": 13, "text": "Main aman. Tidak ada info didapat.", "next": "act14"},

    "act14": {
        "act": 14,
        "text": "**ACT 14: PENTAS SENI (PENSI)**\n\nAjang pencitraan terbesar Kevin. Dia mengundang artis Ibu Kota.",
        "choices": {"1": "Sabotase sound system saat Kevin pidato.", "2": "Bajak layar proyektor dengan video aib Kevin.", "3": "Nikmati acara (Normies)."},
        "req_flag": {"2": ["rekaman_judi", "lokasi_kevin"]}, # Butuh intel
        "next_logic": {"1": "act14_sound", "2": "act14_video", "3": "act14_boring"}
    },
    "act14_video": {"act": 14, "text": "BOOM! Video Kevin main judi tayang di layar led raksasa. Sponsor marah. Pensi hancur. Kevin malu besar! (Rep +50)", "effects": {"rep": 50}, "next": "act15"},
    "act14_sound": {"act": 14, "text": "Mic mati. Kevin teriak-teriak lucu. Receh tapi menghibur. (Rep +10)", "effects": {"rep": 10}, "next": "act15"},
    "act14_boring": {"act": 14, "text": "Acara sukses. Popularitas Kevin naik lagi. Bahaya! (Rep -10)", "effects": {"rep": -10}, "next": "act15"},

    "act15": {
        "act": 15,
        "text": "**ACT 15: THE BUDGET LEAK**\n\nPasca Pensi gagal/sukses, isu uang hilang mencuat. Kevin menyalahkan panitia (kambing hitam).",
        "choices": {"1": "Bela panitia yang disalahkan.", "2": "Ikut menyalahkan panitia (Cari aman)."},
        "next_logic": {"1": "act15_hero", "2": "act15_coward"}
    },
    "act15_hero": {"act": 15, "text": "Kamu membela korban fitnah. Kamu menyatukan semua ekskul melawan OSIS. (Rep +20)", "effects": {"rep": 20}, "next": "act16"},
    "act15_coward": {"act": 15, "text": "Kamu diam saja. Panitia itu dikeluarkan. Semangat pemberontakan padam.", "effects": {"rep": -10}, "next": "act16"},

    # --- ACT 16-20: ESCALATION (EXTERNAL & SURVIVAL) ---
    "act16": {
        "act": 16,
        "text": "**ACT 16: TAWURAN BESAR**\n\nSekolah sebelah menyerang karena provokasi (mungkin ulah Kevin untuk mengalihkan isu).",
        "choices": {"1": "Pimpin pertahanan garis depan.", "2": "Sembunyi di perpus.", "3": "Negosiasi damai dengan pemimpin musuh."},
        "next_logic": {"1": "act16_war", "2": "act16_hide", "3": "act16_diplo"}
    },
    "act16_war": {"act": 16, "text": "Kamu berdarah-darah tapi sekolah selamat. Kamu dianggap Jenderal Perang. (Rep +40)", "effects": {"rep": 40}, "next": "act17"},
    "act16_diplo": {"act": 16, "text": "Kamu berhasil mencegah perang lewat diplomasi rokok & kopi. Kharisma level dewa. (Rep +50)", "effects": {"rep": 50}, "next": "act17"},
    "act16_hide": {"act": 16, "text": "Sekolah hancur. Kaca pecah. Siswa kecewa padamu.", "effects": {"rep": -20}, "next": "act17"},

    "act17": {
        "act": 17,
        "text": "**ACT 17: PROPAGANDA WAR**\n\nMajalah Dinding dan Akun Gosip sekolah dikuasai Kevin. Dia menyebarkan hoax tentangmu (Dituduh anak haram, dll).",
        "choices": {"1": "Hack akun IG sekolah.", "2": "Buat majalah tandingan 'VOICE OF TRUTH'.", "3": "Diam adalah emas."},
        "next_logic": {"1": "act17_hack", "2": "act17_press", "3": "act17_fail"}
    },
    "act17_press": {"act": 17, "text": "Majalahmu laku keras! Opini publik berbalik. (Rep +20)", "effects": {"rep": 20}, "next": "act18"},
    "act17_hack": {"act": 17, "text": "Akun IG sekolah pulih, postingan Kevin dihapus. Perang Cyber! (Rep +15)", "effects": {"rep": 15}, "next": "act18"},
    "act17_fail": {"act": 17, "text": "Hoax menyebar. Orang mulai meragukanmu.", "effects": {"rep": -10}, "next": "act18"},

    "act18": {
        "act": 18,
        "text": "**ACT 18: TEACHER STRIKE**\n\nGuru honorer mogok kerja karena gaji dipotong (uangnya dimakan Kepsek & OSIS). Sekolah lumpuh.",
        "choices": {"1": "Pimpin demo guru.", "2": "Bantu Kevin membubarkan demo.", "3": "Belikan guru nasi bungkus (Solidaritas)."},
        "next_logic": {"1": "act18_lead", "2": "act18_traitor", "3": "act18_kind"}
    },
    "act18_lead": {"act": 18, "text": "Kamu berdiri bersama Guru. Sekarang Guru ada di pihakmu. (Power +Max)", "effects": {"rep": 30}, "next": "act19"},
    "act18_traitor": {"act": 18, "text": "Kamu mengkhianati guru demi simpati Kevin? Rendah. (Rep -50)", "effects": {"rep": -50}, "next": "act19"},
    "act18_kind": {"act": 18, "text": "Guru tersentuh. Hubungan personal membaik. (Rep +10)", "effects": {"rep": 10}, "next": "act19"},

    "act19": {
        "act": 19,
        "text": "**ACT 19: THE FRAME UP**\n\nKevin terdesak. Dia menaruh narkoba di tasmu dan memanggil polisi beneran.\nPolisi sudah di gerbang. Kamu punya 5 menit.",
        "choices": {"1": "Buang ke toilet.", "2": "Masukan ke tas Kevin balik (Sleight of Hand).", "3": "Makan barang buktinya (Insane)."},
        "next_logic": {"1": "act19_flush", "2": "act19_reverse", "3": "act19_crazy"}
    },
    "act19_reverse": {"act": 19, "text": "**MASTERPIECE.** Polisi menggeledah tasmu: Bersih. Tas Kevin: Ada barang bukti.\nKevin ditahan sementara (tapi bakal ditebus bapaknya). (Kevin Rep Hancur)", "effects": {"rep": 50}, "next": "act20"},
    "act19_flush": {"act": 19, "text": "Kamu selamat, tapi toilet mampet. Hampir saja.", "next": "act20"},
    "act19_crazy": {"act": 19, "text": "Kamu... memakannya? Kamu overdosis dan masuk UKS. Selamat sih, tapi reputasimu jadi 'Si Gila'. (Rep -10)", "effects": {"rep": -10}, "next": "act20"},

    "act20": {
        "act": 20,
        "text": "**ACT 20: THE SUSPENSION**\n\nAkibat insiden polisi, sekolah dalam status darurat. Pemilihan dimajukan minggu depan.\nKevin kembali dari kantor polisi (ditebus). Dia marah besar. 'INI PERANG!', teriaknya.",
        "choices": {"1": "Siapkan pidato kemenangan.", "2": "Kumpulkan 'Pasukan' (Preman & Ekskul)."},
        "next_logic": {"1": "act21", "2": "act21"}
    },

    # --- ACT 21-25: THE ENDGAME (REVOLUTION) ---
    "act21": {
        "act": 21,
        "text": "**ACT 21: THE RETURN OF THE KING**\n\nKevin kembali dengan preman bayaran dari luar sekolah. Dia memblokir gerbang.\n'Siapa yang mau masuk, harus hormat ke gue!'",
        "choices": {"1": "Terobos blokade dengan mobil.", "2": "Pimpin seluruh siswa menerobos jalan kaki.", "3": "Lapor polisi lagi."},
        "next_logic": {"1": "act21_car", "2": "act21_march", "3": "act21_police"}
    },
    "act21_march": {"act": 21, "text": "Pemandangan epik. 500 siswa berjalan di belakangmu. Preman Kevin takut dan minggir. (Rep +100)", "effects": {"rep": 100}, "next": "act22"},
    "act21_car": {"act": 21, "text": "Nabrak gerbang? Heroik tapi mobilmu rusak.", "next": "act22"},
    "act21_police": {"act": 21, "text": "Polisi bosan dengan sekolah ini. Mereka datang lambat.", "next": "act22"},

    "act22": {
        "act": 22,
        "text": "**ACT 22: DEBATE PREPARATION**\n\nBesok debat kandidat terbuka. Kamu butuh materi mematikan.",
        "choices": {"1": "Susun visi misi logis.", "2": "Siapkan semua kartu truf (Bukti korupsi, selingkuh, dll)."},
        "req_flag": {"2": ["buku_kas_asli", "kwitansi_palsu", "rekaman_judi"]},
        "next_logic": {"1": "act23_logic", "2": "act23_nuke"}
    },
    "act23_nuke": {"act": 23, "text": "**ACT 23: THE GRAND DEBATE (NUKE)**\n\nDi panggung, kamu tidak berdebat. Kamu menyalakan proyektor.\nKamu menunjukan: Kwitansi Palsu, Rekaman Judi, Buku Kas Ganda.\nKevin terdiam. Wajahnya pucat pasi.", "effects": {"rep": 200}, "next": "act24"},
    "act23_logic": {"act": 23, "text": "**ACT 23: THE GRAND DEBATE (LOGIC)**\n\nKamu berdebat sengit soal anggaran. Kevin pintar ngeles. Skor imbang.", "next": "act24"},

    "act24": {
        "act": 24,
        "text": "**ACT 24: VOTING DAY**\n\nHari pencoblosan. Suasana tegang. Serangan fajar Kevin sangat masif (bagi-bagi iPhone).",
        "choices": {"1": "Pasrah pada hati nurani siswa.", "2": "Gerakkan tim sukses untuk jaga TPS (Cegah curang)."},
        "next_logic": {"1": "act25_result", "2": "act25_result"}
    },

    "act25_result": {
        "act": 25,
        "text": "**ACT 25: THE CORONATION**\n\nPenghitungan suara selesai...",
        "choices": {"1": "Lihat Hasil Akhir"},
        "next": "ending_calc"
    },

    # --- FINAL CALCULATION ---
    "ending_calc": {
        "act": 25,
        "text": "Menghitung validasi suara...",
        "special": "calc_ending"
    },

    "end_victory": {"text": "🏆 **VICTORY: THE SUPREME LEADER**\n\nKamu menang mutlak (70%+ suara). Kevin di-drop out. Kamu mereformasi sekolah.\nLegendamu akan diceritakan turun temurun.", "next": "restart"},
    "end_close": {"text": "⚖️ **VICTORY: PYRRHIC VICTORY**\n\nKamu menang tipis (51% suara). Sekolah terbelah dua kubu. Masa jabatanmu akan penuh demo.", "next": "restart"},
    "end_lose": {"text": "💀 **DEFEAT**\n\nUang Kevin terlalu kuat. Dia menang 60%. Kamu dikeluarkan atas tuduhan palsu minggu depan.", "next": "restart"},
}

# --- LOGIC RESET ---
def reset_game():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.reputasi = 0
    st.session_state.flags = []
    st.session_state.messages = []
    st.session_state.current_scene = "start"
    # Intro
    st.session_state.messages.append({"role": "assistant", "content": GAME_SCENES["start"]["text"]})

# --- SIDEBAR PROGRESS ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/spider.png", width=50) # Just a placeholder icon
    st.title("🕷️ Moriarty Protocol")
    
    # Hitung progress Act
    curr_scene_data = GAME_SCENES.get(st.session_state.current_scene, {})
    curr_act = curr_scene_data.get("act", 0)
    
    st.write(f"**ACT {curr_act} / 25**")
    st.progress(min(curr_act/25, 1.0))
    
    st.divider()
    st.metric("Reputasi Hitam", st.session_state.reputasi)
    st.write("🚩 **Aset Intelijen:**")
    for f in st.session_state.flags:
        st.caption(f"- {f.replace('_', ' ').title()}")
        
    if st.button("Hancurkan Ego (Reset)"): reset_game()

# --- MAIN UI ---
st.title("🕷️ The Long War: Gothic Edition")
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- INPUT LOGIC (BUTTONS) ---
curr_id = st.session_state.current_scene
scene = GAME_SCENES.get(curr_id)

# Display illustration for current scene
if curr_id:
    display_illustration(curr_id)

if scene:
    # Handler Ending Calculation
    if scene.get("special") == "calc_ending":
        rep = st.session_state.reputasi
        final_text = ""
        final_scene = ""
        
        time.sleep(1)
        if rep >= 150:
            final_scene = "end_victory"
        elif rep >= 50:
            final_scene = "end_close"
        else:
            final_scene = "end_lose"
        
        # Auto redirect
        st.session_state.current_scene = final_scene
        st.rerun()

    elif "choices" in scene:
        st.divider()
        st.markdown(f"**Keputusan Act {scene.get('act', '?')}:**")
        
        for key, text in scene["choices"].items():
            # LOCK LOGIC
            is_locked = False
            lock_msg = ""
            
            # Rep Check
            if "req_rep" in scene and key in scene["req_rep"]:
                needed = scene["req_rep"][key]
                if st.session_state.reputasi < needed:
                    is_locked = True
                    lock_msg = f"🔒 [Butuh Rep {needed}]"
            
            # Flag Check
            if "req_flag" in scene and key in scene["req_flag"]:
                needed_list = scene["req_flag"][key]
                has_any = any(f in st.session_state.flags for f in needed_list)
                if not has_any:
                    is_locked = True
                    lock_msg = "🔒 [Butuh Intel]"

            # Render
            if is_locked:
                st.button(f"{lock_msg} {text}", key=f"locked_{key}", disabled=True, type="primary")
            else:
                if st.button(f"�️ {text}", key=f"btn_{key}_{curr_id}"):
                    # Execute
                    st.session_state.messages.append({"role": "user", "content": text})
                    
                    next_id = None
                    if "next_logic" in scene and key in scene["next_logic"]:
                        next_id = scene["next_logic"][key]
                    elif "next" in scene:
                        next_id = scene["next"]
                    
                    # Fallback special logic for Act 22 (dynamic branch check)
                    if curr_id == "act22" and key == "2" and not next_id:
                        pass 

                    if next_id:
                        new_scene = GAME_SCENES.get(next_id)
                        # Apply Effects
                        if new_scene and "effects" in new_scene:
                            eff = new_scene["effects"]
                            if "rep" in eff: st.session_state.reputasi += eff["rep"]
                            if "flag" in eff: 
                                if eff["flag"] not in st.session_state.flags:
                                    st.session_state.flags.append(eff["flag"])
                                    st.toast(f"DAPAT: {eff['flag']}")
                        
                        st.session_state.current_scene = next_id
                        
                        if new_scene:
                            st.session_state.messages.append({"role": "assistant", "content": new_scene["text"]})
                        st.rerun()
    
    # Linear continuation (No choices, just text/next)
    elif "next" in scene:
         target = scene["next"]
         # Ubah teks tombol jika targetnya adalah restart
         btn_text = "🔄 Main Lagi (Restart)" if target == "restart" else "Lanjutkan Teror..."
         
         if st.button(btn_text):
            if target == "restart":
                reset_game()
            else:
                st.session_state.current_scene = target
                new_s = GAME_SCENES.get(target)
                if new_s:
                    st.session_state.messages.append({"role": "assistant", "content": new_s["text"]})
                st.rerun()
