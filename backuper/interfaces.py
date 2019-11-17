import falcon
import uuid

from controllers import list_backups, create_backup, rclone_sync


class CreateBackup(object):

    def __init__(self, backup_queue):
        self.backup_queue = backup_queue

    def on_get(self, req, resp):
        resp.body = ('Answer')

    def on_post(self, req, resp):

        job_id = uuid.uuid4().hex
        backup_folder = req.media.get('backup_folder')
        remote_gdrive = req.media.get('remote_gdrive')
        remote_folder = req.media.get('remote_folder')
        passphrase    = req.media.get('passphrase')
        backup_job = self.backup_queue.enqueue(
            create_backup, 
            args=(backup_folder, remote_gdrive, remote_folder, passphrase,),
            kwags={
                'description':'Backup process: folder {} gdrive {}'.format(backup_folder, remote_folder),
                'job_id': job_id
            },
            job_timeout='6h'
        )

        if backup_job.result is None:
            resp.body = ('{}'.format(job_id))
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


class SyncBackup(object):

    def __init__(self, backup_queue):
        self.backup_queue = backup_queue

    def on_post(self, req, resp):

        job_id = uuid.uuid4().hex

        backup_folder = req.media.get('backup_folder')
        remote_gdrive = req.media.get('remote_gdrive')
        remote_folder = req.media.get('remote_folder')
        passphrase    = req.media.get('passphrase')
        backup_dir    = req.media.get('backup_dir')

        backup_job = self.backup_queue.enqueue(
            rclone_sync, 
            args=(backup_folder, remote_gdrive, remote_folder, passphrase, backup_dir),
            kwags={
                'description':'Sync process: folder {} gdrive {}'.format(backup_folder, remote_folder),
                'job_id': job_id
            },
            job_timeout='6h'
        )

        if backup_job.result is None:
            resp.body = ('{}'.format(job_id))
        else:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ('Failure on queue')



class CheckBackupProgress(object):

    def __init__(self, backup_queue):
        self.backup_queue = backup_queue

    def on_post(self, req, resp):

        try:
            job_id = req.media.get('job_id')
            job_checked = self.backup_queue.fetch_job(job_id)
            
            if job_checked == "Done":
                resp.body = {"job_id :{} \n {} \n Done".format(job_id, job_checked.description)}
            else:
                resp.body = ("Still running. \n")
        except Exception as e:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ("Error {}".format(e))

class GetJobIDs(object):

    def __init__(self, backup_queue):
        self.backup_queue = backup_queue

    def on_get(self, req, resp):
        try:
            jobs_list = self.backup_queue.job_ids
            jobs_count = self.backup_queue.count
            
            resp.body = ("job_ids :{} \n Total jobs in queue {}".format(jobs_list, jobs_count))
        except Exception as e:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ("Error {}".format(e))


class CancelJob(object):

    def __init__(self, backup_queue):
        self.backup_queue = backup_queue

    def on_post(self, req, resp):
        try:
            job_id = req.media.get('job_id')
            job_running = self.backup_queue.fetch_job(job_id)
            job_running.cancel()
            resp.body = ("job_id {} cancelled".format(job_id))
        except Exception as e:
            resp.status = falcon.status_codes.HTTP_500
            resp.body = ("Error {}".format(e))


