import falcon
from controllers import list_backups, create_backup


class CreateBackup(object):
    def on_get(self, req, resp):
        resp.body = ('Answer')

    def on_post(self, req, resp):
        backup_folder = req.media.get('backup_folder')
        remote_gdrive = req.media.get('remote_gdrive')
        remote_folder = req.media.get('remote_folder')
        passphrase    = req.media.get('passphrase')
        backup_file_tar_gpg = create_backup(backup_folder, remote_gdrive, remote_folder, passphrase)
        if backup_file_tar_gpg:
            resp.body = ("Backup folder {} successful".format(backup_file_tar_gpg))
        else:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ("Failure to back up folder {}".format(backup_file_tar_gpg))


class ListBackups(object):

    def __init__(self, remote_gdrive: str, remote_folder: str):
        self.remote_gdrive = remote_gdrive
        self.remote_folder = remote_folder

    def on_get(self, req, resp):
        try:
            backup_list = list_backups(self.remote_gdrive, self.remote_folder)
            
            if backup_list:
                resp.body = backup_list
            else:
                resp.body = ("No backups found. \n")
        except Exception as e:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ("Error accessing Gdrive backups, {}".format(e))