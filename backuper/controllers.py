import shlex
import subprocess
import gnupg
import tarfile



def list_backups(remote_gdrive: str, remote_folder: str):
    rclone_cmd_ls = "rclone lsjson {}:{}".format(remote_gdrive, remote_folder)
    rclone_cmd_ls_parsed = shlex.split(rclone_cmd_ls)
    results = subprocess.run(rclone_cmd_ls_parsed, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return results.stdout


def rclone_copy_file(backup_file: str, remote_gdrive: str, remote_folder: str):
    rclone_cmd = "rclone copy {} {}:{}".format(backup_file, remote_gdrive, remote_folder)
    rclone_cmd_parsed = shlex.split(rclone_cmd)
    subprocess.run(rclone_cmd_parsed)


def compress_backup(backup_file:str):
    with tarfile.open(backup_file, 'w:gz') as tar:
        tar.add(backup_file)


def encrypt_backup(backup_file_tar: str, passphrase: str):
    gpg = gnupg.GPG()
    with open(backup_file_tar, 'rb') as f: 
        gpg.encrypt_file(f, output=backup_file_tar + '.gpg', passphrase=passphrase, symmetric=True, recipients=None) 
    

def decrypt_backup(backup_file_tar_gpg: str, passphrase: str):
    gpg = gnupg.GPG()
    with open(backup_file_tar_gpg, 'rb') as ff: 
        gpg.decrypt_file(ff, output=backup_file_tar_gpg, passphrase=passphrase)


def create_backup(backup_file: str, remote_gdrive: str, remote_folder: str, passphrase: str):
    compress_backup(backup_file)
    backup_file_tar_gz = backup_file + '.tar.gz'
    encrypt_backup(backup_file_tar_gz, passphrase)  
    return str(backup_file)