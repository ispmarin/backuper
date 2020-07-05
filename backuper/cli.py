#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for backuper."""
import argparse
import logging
from getpass import getpass
from controllers import create_backup

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Use rclone do create encrypted backups."
    )

    parser.add_argument(
        "--gdrive", "-g", required=True, help="The GDrive name in Rclone"
    )
    parser.add_argument(
        "--backup_folder", "-b", required=True, help="The folder to be backed up"
    )
    parser.add_argument(
        "--remote_folder", "-r", required=True, help="The remote folder to be used"
    )

    args = parser.parse_args()

    password = getpass()

    if password:
        logger.info("Creating password")
        create_backup(args.backup_folder, args.gdrive, args.remote_folder, password)
        logger.info("Backup created")
    else:
        logger.error("Password not provided. Please provide password to create backup.")
