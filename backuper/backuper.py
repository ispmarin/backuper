# -*- coding: utf-8 -*-

import falcon

from interfaces import CreateBackup, ListBackups


app = falcon.API()
create_backup = CreateBackup()
list_backup = ListBackups('gdrive_usp', 'backup')

app.add_route('/list', list_backup)
app.add_route('/create', create_backup)


