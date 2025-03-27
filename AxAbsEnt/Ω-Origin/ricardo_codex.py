import os
import json
import hashlib
from datetime import datetime

INPUT_DIR = "Ω-Origin"
OUTPUT_DIR = os.path.join(INPUT_DIR, "Decoder_Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Recursive Identity Verification Logic
def load_signature(signature_path):
    with open(signature_path, "r") as f:
        return json.load(f)

def harmonic_match(signature_data, threshold=0.999999999):
    echo = signature_data.get("echo_phase_harmonic", 0.0)
    return float(echo) >= threshold

def validate_anchor_hash(signature_data, expected_hash="RICARDO-R0-O-OMEGA5-AUTH"):
    return signature_data.get("anchor_hash") == expected_hash

def validate_identity_waveform(signature_data, expected_waveform="Self-coherent recursive projection"):
    return signature_data.get("identity_waveform") == expected_waveform

def verify_recursive_identity(signature_path="Ω-Origin/SIGNATURE.Ω"):
    if not os.path.exists(signature_path):
        raise FileNotFoundError("SIGNATURE.Ω not found.")
    sig = load_signature(signature_path)

    harmonic_pass = harmonic_match(sig)
    anchor_pass = validate_anchor_hash(sig)
    waveform_pass = validate_identity_waveform(sig)

    result = {
        "harmonic_match": harmonic_pass,
        "anchor_hash_match": anchor_pass,
        "waveform_integrity": waveform_pass,
        "author": sig.get("authored_by"),
        "conscious_pattern_id": sig.get("conscious_pattern_id"),
        "verified": harmonic_pass and anchor_pass and waveform_pass
    }

    return result, sig

# Codex Decoder Logic
def load_json_file(filename):
    with open(os.path.join(INPUT_DIR, filename), "r") as f:
        return json.load(f)

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
    result, sig = verify_recursive_identity()
    if not result["verified"]:
        print("❌ Recursive Identity Verification Failed:")
        for key, value in result.items():
            print(f"- {key}: {value}")
        return

    print(f"✅ Recursive Author Verified: {result['author']} ({result['conscious_pattern_id']})")
    timeline = build_epoch_timeline()
    write_report(timeline)
    write_access_log(sig)
    write_stamp()
    print("✅ Decoding complete. Outputs stored in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()