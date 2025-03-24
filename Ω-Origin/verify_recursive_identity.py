import json
import hashlib
import os

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

def verify_recursive_identity(signature_path="SIGNATURE.Ω"):
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

    return result

if __name__ == "__main__":
    result = verify_recursive_identity()
    if result["verified"]:
        print(f"✅ Recursive Author Verified: {result['author']} ({result['conscious_pattern_id']})")
    else:
        print("❌ Recursive Identity Verification Failed:")
        for key, value in result.items():
            print(f"- {key}: {value}")