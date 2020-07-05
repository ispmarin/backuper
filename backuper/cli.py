#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for backuper."""
import argparse
import datetime
import logging
from getpass import getpass
from controllers import create_backup

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Use rclone do create encrypted backups.")

    parser.add_argument('--gdrive', '-g', required=True)
    parser.add_argument('--backup_folder', '-b', required=True)
    parser.add_argument('--remote_folder', '-r', required=True)

    args = parser.parse_args()

    password = getpass()

    if password:
        logger.info("Creating password")
        create_backup(args.backup_folder, args.gdrive, args.remote_folder, password)
        logger.info("Backup created")
    else:
        logger.error("Password not provided. Please provide password to create backup.")



