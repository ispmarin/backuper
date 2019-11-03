import falcon
from controllers import list_backups, create_backup


class CreateBackup(object):

    def __init__(self, backup_queue):
        self.backup_queue = backup_queue

    def on_get(self, req, resp):
        resp.body = ('Answer')

    def on_post(self, req, resp):
        backup_folder = req.media.get('backup_folder')
        remote_gdrive = req.media.get('remote_gdrive')
        remote_folder = req.media.get('remote_folder')
        passphrase    = req.media.get('passphrase')
        backup_job = self.backup_queue.enqueue(create_backup, args=(backup_folder, remote_gdrive, remote_folder, passphrase), timeout='6h')

        if backup_job.result is None:
            resp.body = ('Backup process started')
        else:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ('Failure on queue')


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