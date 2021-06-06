#!/bin/bash
uwsgi --ini /SOM_PROJECT/SOM_PROJECT/uwsgi.ini
chmod 777 /SOM_PROJECT/SOM_PROJECT.sock
cp /SOM_PROJECT/nginx.conf /etc/nginx/sites-enabled/
service mongodb start
service nginx restart
