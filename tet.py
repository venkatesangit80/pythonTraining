from ftplib import FTP_TLS
import os

def upload_file_ftps(host, port, username, password, local_file_path, remote_folder):
    # Ensure the local file exists
    if not os.path.isfile(local_file_path):
        raise FileNotFoundError(f"Local file not found: {local_file_path}")
    
    filename = os.path.basename(local_file_path)

    # Connect to FTPS server
    ftps = FTP_TLS()
    ftps.connect(host=host, port=port)
    ftps.login(user=username, passwd=password)
    ftps.prot_p()  # Secure data connection

    # Change to the desired upload folder
    ftps.cwd(remote_folder)

    # Upload the file
    with open(local_file_path, 'rb') as file:
        ftps.storbinary(f'STOR {filename}', file)

    # Close the connection
    ftps.quit()
    print(f"Uploaded {filename} to {host}/{remote_folder}")

# Example usage
upload_file_ftps(
    host='ftps.example.com',
    port=21,  # usually 21 or 990 for FTPS
    username='your_username',
    password='your_password',
    local_file_path='path/to/your/file.txt',
    remote_folder='/upload/path/on/server'
)