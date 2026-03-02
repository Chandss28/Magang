import pandas as pd

def load_jadwal():
    return pd.read_csv("data/jadwal.csv")

def load_tarif():
    return pd.read_csv("data/tarif.csv")

def find_tarif(rute, golongan):
    df = load_tarif()
    result = df[(df["rute"] == rute) & (df["golongan"] == golongan)]
    if not result.empty:
        return int(result.iloc[0]["harga"])
    return None

def find_jadwal(rute):
    df = load_jadwal()
    result = df[df["rute"] == rute]
    if not result.empty:
        return result.to_dict("records")
    return None