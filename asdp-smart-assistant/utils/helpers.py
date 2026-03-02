import re
from datetime import datetime

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def get_timestamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def detect_rute(text):
    text = text.lower()
    if "merak" in text and "bakauheni" in text:
        return "Merak-Bakauheni"
    if "ketapang" in text and "gilimanuk" in text:
        return "Ketapang-Gilimanuk"
    return None

def detect_golongan(text):
    if "mobil" in text or "golongan iv" in text:
        return "Golongan IV (Mobil)"
    if "penumpang" in text or "dewasa" in text:
        return "Penumpang Dewasa"
    return None