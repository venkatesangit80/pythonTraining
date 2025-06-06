import hashlib
import base64

def jumble_server_name_atomic(server_name, salt="vega-secret"):
    # Combine with a salt to prevent reverse lookup
    combined = f"{salt}:{server_name}"
    hash_obj = hashlib.sha256(combined.encode())
    encoded = base64.urlsafe_b64encode(hash_obj.digest())[:8]
    return encoded.decode()
