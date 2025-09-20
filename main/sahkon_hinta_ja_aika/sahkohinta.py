import requests
from datetime import datetime
import tkinter as tk

PRICE_UPDATE_INTERVAL = 60 * 1000  # sähkön hinta päivittyy 1 minuutin välein (ms)
TIME_UPDATE_INTERVAL = 1000        # kellonaika päivittyy sekunnin välein (ms)

def hae_nykyinen_hinta():
    nyt = datetime.now()
    paiva = nyt.strftime("%Y-%m-%d")
    tunti = nyt.hour
    url = f"https://api.porssisahko.net/v1/price.json?date={paiva}&hour={tunti}"

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            hinta = data.get("price")
            return hinta
        else:
            return None
    except Exception:
        return None

def paivita_hinta():
    hinta = hae_nykyinen_hinta()
    if hinta is not None:
        hinta_label.config(text=f"{hinta:.2f} snt/kWh")
    else:
        hinta_label.config(text="Ei saatavilla")
    # Suorita päivitys uudelleen määrätyn ajan kuluttua
    root.after(PRICE_UPDATE_INTERVAL, paivita_hinta)

def paivita_kello():
    nyt = datetime.now()
    aika_str = nyt.strftime("%H:%M:%S")
    paiva_str = nyt.strftime("%Y-%m-%d")
    aika_label.config(text=f"{paiva_str} {aika_str}")
    # Suorita päivitys uudelleen sekunnin kuluttua
    root.after(TIME_UPDATE_INTERVAL, paivita_kello)

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Nykynen pörssisähkön hinta")

root.geometry("300x150")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill=tk.BOTH)

hinta_label = tk.Label(frame, text="Ladataan...", font=("Helvetica", 32), fg="orange")
hinta_label.pack(pady=10)

aika_label = tk.Label(frame, text="", font=("Helvetica", 16))
aika_label.pack()

# Aloitetaan päivitykset
paivita_hinta()
paivita_kello()

root.mainloop()
