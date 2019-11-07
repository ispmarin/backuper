# -*- coding: utf-8 -*-

import falcon

from interfaces import CreateBackup, ListBackups, CheckBackupProgress, GetJobIDs, CancelJob
import rq
import redis


redis_con = redis.Redis()
backup_queue = rq.Queue(connection=redis_con, timeout='6h')

app = falcon.API()
create_backup = CreateBackup(backup_queue)
list_backup = ListBackups('gdrive_usp', 'backup')
check_backup_progress = CheckBackupProgress(backup_queue)
get_job_ids = GetJobIDs(backup_queue)
cancel_job = CancelJob(backup_queue)

app.add_route('/list_backups', list_backup)
app.add_route('/create', create_backup)
app.add_route('/check', check_backup_progress)
app.add_route('/ids', get_job_ids)
app.add_route('/cancel', cancel_job)


