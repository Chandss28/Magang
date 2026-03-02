import streamlit as st
import pandas as pd
from services.ai_service import get_ai_response
from services.data_service import find_tarif, find_jadwal
from utils.helpers import format_rupiah, detect_rute, detect_golongan, get_timestamp
from utils.logger import save_log

st.set_page_config(page_title="ASDP Smart Assistant", page_icon="🚢", layout="wide")

menu = st.sidebar.radio("Navigasi", ["Chatbot", "Dashboard"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

if "logs" not in st.session_state:
    st.session_state.logs = []

# ================= CHATBOT =================
if menu == "Chatbot":

    st.title("🚢 ASDP Smart Assistant")
    st.caption("Informasi Jadwal & Tarif Penyeberangan")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Tanyakan jadwal atau tarif...")

    if prompt:
        st.session_state.chat_count += 1
        timestamp = get_timestamp()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        lower_prompt = prompt.lower()

        # ===== Intent Detection =====
        is_tarif_question = any(word in lower_prompt for word in ["harga", "tarif", "biaya"])
        is_jadwal_question = any(word in lower_prompt for word in ["jadwal", "jam", "berangkat"])

        rute = detect_rute(prompt)
        golongan = detect_golongan(prompt)

        known_routes = ["Merak-Bakauheni", "Ketapang-Gilimanuk"]

        with st.spinner("Memproses..."):

            # ================= TARIF =================
            if is_tarif_question:

                if not rute:
                    response = "Mohon sebutkan rute penyeberangan (contoh: Merak-Bakauheni)."

                elif not golongan:
                    response = "Mohon sebutkan jenis tiket (Penumpang Dewasa / Golongan IV Mobil)."

                else:
                    harga = find_tarif(rute, golongan)

                    if harga:
                        response = f"""
**Informasi Tarif**
Rute: {rute}  
Golongan: {golongan}  
Harga: {format_rupiah(harga)}
"""
                    else:
                        response = "Data tarif tidak tersedia dalam sistem. Hubungi Call Center 191."

            # ================= JADWAL =================
            elif is_jadwal_question:

                if not rute:
                    response = "Mohon sebutkan rute penyeberangan yang dimaksud."

                else:
                    jadwal = find_jadwal(rute)

                    if jadwal:
                        response = "**Jadwal Kapal:**\n\n"
                        for j in jadwal:
                            response += f"- {j['kapal']} | {j['jam_berangkat']} - {j['jam_tiba']}\n"
                    else:
                        response = "Data jadwal tidak tersedia dalam sistem. Hubungi Call Center 191."

            # ================= LUAR KONTEKS =================
            else:
                response = get_ai_response(st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": response})

        log_entry = {
            "timestamp": timestamp,
            "user": prompt,
            "assistant": response
        }

        st.session_state.logs.append(log_entry)
        save_log(log_entry)

        with st.chat_message("assistant"):
            st.markdown(response)