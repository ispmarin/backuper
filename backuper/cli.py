#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for backuper."""
import argparse
import datetime
from controllers import rclone_sync


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use rclone do create encrypted backups.")

    parser.add_argument('--gdrive', '-g')
    parser.add_argument('--backup_folder', '-b')
    parser.add_argument('--remote_folder', '-r')
    args = parser.parse_args()
    backup_time = datetime.datetime.now().strftime('%Y%m%d')

    rclone_sync(args.backup_folder, args.gdrive, args.remote_folder, backup_time)
