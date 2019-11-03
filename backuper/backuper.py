# -*- coding: utf-8 -*-

import falcon

from interfaces import CreateBackup, ListBackups
import rq
import redis


redis_con = redis.Redis()
backup_queue = rq.Queue(connection=redis_con)

app = falcon.API()
create_backup = CreateBackup(backup_queue)
list_backup = ListBackups('gdrive_usp', 'backup')

app.add_route('/list', list_backup)
app.add_route('/create', create_backup)


