import falcon
from controllers import list_backups, start_backup


class StartBackup(object):
    def on_get(self, req, resp):
        resp.body = ('Answer')

    def on_post(self, req, resp):
        backup_path = req.media.get('backup_path')
        status = start_backup(backup_path)
        if status:
            resp.body = ("Backup folder {} successful".format(backup_path))
        else:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ("Failure to back up folder {}".format(backup_path))


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