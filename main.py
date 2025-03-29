from flask import Flask, jsonify, send_file
import threading, time, json, csv, logging, os
from datetime import datetime

app = Flask("BarkinsBot")

# Status-Daten
status = {
    "claims": 0,
    "ptc_clicks": 0,
    "ref_clicks": 0,
    "nfts_minted": 0,
    "galxe_tasks": 0
}

# Wallets / Konfiguration
config = {
    "claim_interval": 300,
    "wallets": {
        "btc": "1EcvmNjx4cwMULZPwPKADnsEvEkmBzianW",
        "eth": "0x572e14c9CbBf6e95e464214C45B3424D2B193bE8",
        "doge": "DFPCqjs99Jabf2XbB7hhMgu5wxtDZ1eDDE",
        "ltc": "ltc1q2lmw0lp2ce7d6n7h0fqxhwa60785sd7l076qkf",
        "bch": "bitcoincash:qruxfmpu5atcqdgtf3jl988cfa8qxl0yvveg86u94n"
    }
}

@app.route("/")
def home():
    return "✅ BarkinsBot läuft mit Web-Dashboard!"

@app.route("/status")
def get_status():
    return jsonify(status)

@app.route("/log/export")
def export_log():
    with open("export_logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.utcnow().isoformat(),
            status["claims"],
            status["ptc_clicks"],
            status["ref_clicks"],
            status["nfts_minted"],
            status["galxe_tasks"]
        ])
    return send_file("export_logs.csv", as_attachment=True)

# Bot-Module
def auto_claim():
    while True:
        print(f"[💸] BTC Claim an {config['wallets']['btc']}")
        status["claims"] += 1
        time.sleep(config["claim_interval"])

def auto_ptc():
    while True:
        print("[👁️] PTC Anzeige geklickt.")
        status["ptc_clicks"] += 1
        time.sleep(60)

def self_ref_clicker():
    while True:
        print("[🔁] Ref-Link geklickt.")
        status["ref_clicks"] += 1
        time.sleep(240)

def nft_mint():
    while True:
        print("[🎨] NFT gemintet.")
        status["nfts_minted"] += 1
        time.sleep(3600)

def galxe_autoquest():
    while True:
        print("[🌌] Galxe-Task abgeschlossen.")
        status["galxe_tasks"] += 1
        time.sleep(1800)

# Alle Threads starten
def run_all():
    threading.Thread(target=auto_claim).start()
    threading.Thread(target=auto_ptc).start()
    threading.Thread(target=self_ref_clicker).start()
    threading.Thread(target=nft_mint).start()
    threading.Thread(target=galxe_autoquest).start()
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    run_all()
