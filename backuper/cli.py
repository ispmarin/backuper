#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for backuper."""
import argparse
import datetime
from controllers import create_backup, rclone_sync
from getpass import getpass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use rclone do create encrypted backups.")

    parser.add_argument('--gdrive', '-g', required=True)
    parser.add_argument('--backup_folder', '-b', required=True)
    parser.add_argument('--remote_folder', '-r', required=True)
    parser.add_argument('--password', '-p', action='store_true')
    args = parser.parse_args()
    backup_time = datetime.datetime.now().strftime('%Y%m%d')

    if args.password:
        password = getpass()
    
    # rclone_sync(args.backup_folder, args.gdrive, args.remote_folder, backup_time)
    create_backup(args.backup_folder, args.gdrive, args.remote_folder, password)
