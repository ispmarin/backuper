=========
WebRclone
=========


.. image:: https://img.shields.io/pypi/v/webrclone.svg
        :target: https://pypi.python.org/pypi/webrclone

.. image:: https://img.shields.io/travis/ispmarin/webrclone.svg
        :target: https://travis-ci.org/ispmarin/webrclone

.. image:: https://readthedocs.org/projects/webrclone/badge/?version=latest
        :target: https://webrclone.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Backup to GDrive using RClone interface, with a command-line interface and a REST API. Uses
Falcon, RQ and Redis for queueing the backup jobs.



* Free software: MIT license
* Documentation: https://webrclone.readthedocs.io.


Features
--------

* Add media (JSON) validators for POST requests
* Verify job queue and clean when done
* Document Docker Redis container

