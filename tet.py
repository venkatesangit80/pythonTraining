import pysftp

def upload_file_sftp(host, port, username, password, local_path, remote_path):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key checking if needed

    with pysftp.Connection(host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
        sftp.makedirs(remote_path)  # creates folders if not exists
        sftp.cwd(remote_path)
        sftp.put(local_path)
        print(f"Uploaded {local_path} to {remote_path}")

# Example usage
upload_file_sftp(
    host='your.server.com',
    port=10022,
    username='your_username',
    password='your_password',
    local_path='test.txt',
    remote_path='/upload/folder'
)