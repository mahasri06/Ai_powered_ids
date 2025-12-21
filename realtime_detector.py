# realtime_detector.py
from pyexpat import features
import joblib
import numpy as np
from scapy.all import sniff, IP, TCP, UDP

# Load model and scaler
model, scaler = joblib.load("model/ids_model.joblib")

print("🚀 Starting real-time intrusion detection...")

def process_packet(packet):
    if IP not in packet:
        return

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    length = len(packet)
    proto = packet[IP].proto

    src_port = 0
    dst_port = 0
    proto_name = "OTHER"

    if TCP in packet:
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        proto_name = "TCP"
    elif UDP in packet:
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        proto_name = "UDP"

    # Feature vector (same order as training)
    import pandas as pd

    features = pd.DataFrame([{
        "len": length,
        "src_port": src_port,
        "dst_port": dst_port,
        "proto": proto
    }])

    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]

    # 🔍 DISPLAY EXACT PACKET DETAILS
    if prediction == 0:
        print(
            f"⚠️ ATTACK | {proto_name} | "
            f"{src_ip}:{src_port} → {dst_ip}:{dst_port} | "
            f"Len={length}"
        )
    else:
        print(
            f"✅ NORMAL | {proto_name} | "
            f"{src_ip}:{src_port} → {dst_ip}:{dst_port} | "
            f"Len={length}"
        )

sniff(prn=process_packet, store=False)