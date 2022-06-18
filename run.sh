#!/bin/bash --login
/etc/init.d/nginx start
uwsgi --ini /usr/vassals/uwsgi.ini
uwsgi --emperor /usr/vassals/ --uid www-data --gid www-data -d