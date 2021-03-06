import shlex
import gnupg
import subprocess
import tarfile

import logging

logger = logging.getLogger(__name__)


def list_backups(remote_gdrive: str, remote_folder: str):
    rclone_cmd_ls = "rclone lsjson {}:{}".format(remote_gdrive, remote_folder)
    rclone_cmd_ls_parsed = shlex.split(rclone_cmd_ls)
    results = subprocess.run(
        rclone_cmd_ls_parsed, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return results.stdout


def rclone_copy_file(backup_file: str, remote_gdrive: str, remote_folder: str):
    logger.info("RClone copying file {}".format(backup_file))
    rclone_cmd = "rclone copy {} {}:{}".format(
        backup_file, remote_gdrive, remote_folder
    )
    rclone_cmd_parsed = shlex.split(rclone_cmd)
    subprocess.run(rclone_cmd_parsed)


def rclone_sync(
    backup_folder: str, remote_gdrive: str, remote_folder: str, backup_dir_date: str
):
    rclone_cmd = "rclone sync {bf} {rgd}:{rmf} --backup-dir {rgd}:{rmf}-{bdr}".format(
        bf=backup_folder, rgd=remote_gdrive, rmf=remote_folder, bdr=backup_dir_date
    )
    rclone_cmd_parsed = shlex.split(rclone_cmd)
    subprocess.run(rclone_cmd_parsed)


def compress_backup(backup_file: str):
    logger.info("Compressing backup {}".format(backup_file))
    backup_file_name = backup_file + ".tar.gz"
    with tarfile.open(backup_file_name, "w:gz") as tar:
        tar.add(backup_file)
    return backup_file_name


def encrypt_backup(backup_file_tar: str, passphrase: str):
    logger.info("Encrypting backup {}".format(backup_file_tar))
    gpg = gnupg.GPG()
    with open(backup_file_tar, "rb") as f:
        gpg.encrypt_file(
            f,
            output=backup_file_tar + ".gpg",
            passphrase=passphrase,
            symmetric=True,
            recipients=None,
        )
    return backup_file_tar + ".gpg"


def decrypt_backup(backup_file_tar_gpg: str, passphrase: str):
    gpg = gnupg.GPG()
    with open(backup_file_tar_gpg, "rb") as ff:
        gpg.decrypt_file(ff, output=backup_file_tar_gpg, passphrase=passphrase)


def create_backup(
    backup_file: str, remote_gdrive: str, remote_folder: str, passphrase: str
):
    logger.info("Creating backup {} {}".format(remote_gdrive, remote_folder))
    try:
        backup_file_name = compress_backup(backup_file)
        backup_file_name = encrypt_backup(backup_file_name, passphrase)
        rclone_copy_file(backup_file_name, remote_gdrive, remote_folder)
    except FileNotFoundError:
        logger.critical("RClone command not found - Backup not executed")
