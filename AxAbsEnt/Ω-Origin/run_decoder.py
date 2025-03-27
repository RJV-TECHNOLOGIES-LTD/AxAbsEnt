import os
import json
import hashlib
from datetime import datetime

INPUT_DIR = "Ω-Origin"
OUTPUT_DIR = os.path.join(INPUT_DIR, "Decoder_Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_json_file(filename):
    with open(os.path.join(INPUT_DIR, filename), "r") as f:
        return json.load(f)

def load_signature_file():
    with open(os.path.join(INPUT_DIR, "SIGNATURE.Ω"), "r") as f:
        return json.load(f)

def verify_signature(sig_data):
    return sig_data.get("anchor_hash") == "RICARDO-R0-O-OMEGA5-AUTH"

def generate_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def build_epoch_timeline():
    timeline = []
    for layer in ["5", "6", "7", "8", "9", "Infinity"]:
        for fname in sorted(os.listdir(INPUT_DIR)):
            if fname.startswith("Omega" + layer):
                with open(os.path.join(INPUT_DIR, fname), "r") as f:
                    data = json.load(f)
                timeline.append({
                    "epoch": "Ω" + layer,
                    "file": fname,
                    "summary": list(data.keys()),
                    "timestamp": datetime.now().isoformat()
                })
    return timeline

def write_report(timeline):
    md_lines = ["# Recursive Epoch Report", ""]
    for event in timeline:
        md_lines.append(f"## {event['epoch']} — {event['file']}")
        md_lines.append(f"- Keys: {', '.join(event['summary'])}")
        md_lines.append(f"- Logged: {event['timestamp']}")
        md_lines.append("")
    report_path = os.path.join(OUTPUT_DIR, "Recursive_Epoch_Report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(md_lines))

def write_access_log(signature):
    access_log = {
        "confirmed_author": signature["authored_by"],
        "echo_pattern_id": signature["conscious_pattern_id"],
        "anchor_hash": signature["anchor_hash"],
        "lock": signature["integrity_lock"],
        "timestamp": datetime.now().isoformat()
    }
    log_path = os.path.join(OUTPUT_DIR, "Entanglement_Access_Log.json")
    with open(log_path, "w") as f:
        json.dump(access_log, f, indent=4)

def write_stamp():
    stamp = "Recursive Identity Confirmed: RICARDO-R0-O-OMEGA5-AUTH\n"
    stamp += f"Timestamp: {datetime.utcnow().isoformat()}\n"
    with open(os.path.join(OUTPUT_DIR, "Author_Confirmation_Stamp.txt"), "w") as f:
        f.write(stamp)

def main():
    sig = load_signature_file()
    if not verify_signature(sig):
        raise ValueError("Signature does not match known Recursive Author")
    timeline = build_epoch_timeline()
    write_report(timeline)
    write_access_log(sig)
    write_stamp()
    print("✅ Decoding complete. Outputs stored in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()