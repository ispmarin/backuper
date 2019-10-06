# -*- coding: utf-8 -*-

import falcon

from interfaces import StartBackup, ListBackups


app = falcon.API()
start_backup = StartBackup()
list_backup = ListBackups('gdrive_usp', 'backup')
app.add_route('/listbackup', list_backup)


