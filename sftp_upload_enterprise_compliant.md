
# Enterprise-Compliant SFTP Upload Script (Python)

This script securely uploads a file to an SFTP server using OpenSSH via Python's `subprocess` module.
It meets enterprise compliance requirements, does not rely on external Python libraries, and supports
key-based authentication.

---

## ✅ Script

```python
import subprocess
import os
from datetime import datetime

# === CONFIGURATION ===
remote_host = "sftp.yourserver.com"            # Replace with actual SFTP host
remote_user = "your_username"                  # SFTP username
private_key = "/secure/path/private_key.pem"   # Path to SSH private key (read-only access)
local_file = "/path/to/local/file.txt"         # Full path to the local file to upload
remote_path = "/upload/destination/"           # Remote path to place the file

# === GENERATE UNIQUE BATCH FILE ===
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
batch_file = f"/tmp/sftp_batch_{timestamp}.txt"

with open(batch_file, "w") as f:
    f.write(f"put {local_file} {remote_path}\n")
    f.write("bye\n")

# === BUILD SFTP COMMAND ===
sftp_command = [
    "sftp",
    "-o", "StrictHostKeyChecking=no",           # Optional: disable host key prompt
    "-i", private_key,
    "-b", batch_file,
    f"{remote_user}@{remote_host}"
]

# === EXECUTE AND CAPTURE OUTPUT ===
try:
    print(f"[INFO] Starting SFTP upload at {timestamp}")
    result = subprocess.run(
        sftp_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # === LOGGING AND STATUS ===
    if result.returncode == 0:
        print("[SUCCESS] File uploaded successfully.")
        print(result.stdout)
    else:
        print("[ERROR] SFTP upload failed.")
        print(result.stderr)

finally:
    # === CLEANUP ===
    if os.path.exists(batch_file):
        os.remove(batch_file)
```

---

## ✅ Compliance Mapping

| Compliance Requirement                             | Covered by Script?              |
|----------------------------------------------------|---------------------------------|
| SFTP using OpenSSH                                 | ✅ Yes                          |
| No third-party Python packages                     | ✅ Yes                          |
| Key-based authentication                           | ✅ Yes                          |
| Scriptable and auditable                           | ✅ Yes                          |
| Secure for VPN or dedicated lines (network layer)  | ✅ Yes                          |
| Suitable for Dagster or enterprise schedulers      | ✅ Yes                          |

---

## ℹ️ Notes

- Ensure the `sftp` binary is installed and accessible on the execution environment.
- Securely store the private key and set read-only permissions.
- For audit logging, consider redirecting outputs to a file or logging service.
