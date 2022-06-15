# Server

replace
server_name user.com www.user.com;  in nginx_uwsgi/server.conf
FROM python:3.9.13-bullseye AS BUILD

# Install dependencies
RUN apt-get update -y && \
    apt-get install gcc nginx python3.8-dev certbot systemd -y && \
    apt-get clean
RUN pip install --no-cache-dir uwsgi==2.0.20 django==3.2.12

# Copy the Django project to the container
COPY ./secret_key.txt /Server/secret_key.txt
COPY ./filesmanager /Server/filesmanager
COPY ./nginx_uwsgi /Server/nginx_uwsgi
COPY ./server /Server/server
COPY ./manage.py /Server/manage.py

# Copy the nginx config
RUN rm /etc/nginx/sites-enabled/default &&\
    rm /etc/nginx/sites-available/default
RUN ln -s /Server/nginx_uwsgi/server.conf /etc/nginx/sites-enabled/server.conf && \
    ln -s /Server/nginx_uwsgi/server.conf /etc/nginx/sites-available/server.conf 
RUN /etc/init.d/nginx restart

# Config server data
RUN mkdir /Server/logs
RUN mkdir /ServerData
RUN mkdir /Public

# Config the uwsgi
RUN uwsgi --ini /Server/nginx_uwsgi/uwsgi.ini
RUN mkdir /usr/local/vassals
RUN ln -s /Server/nginx_uwsgi/uwsgi.ini /usr/local/
COPY ./run.sh .

# Migration
RUN python /Server/manage.py makemigrations
RUN python /Server/manage.py migrate
RUN python /Server/manage.py collectstatic
RUN python /Server/manage.py createsuperuser
RUN python /Server/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
# Run the Django server
ENTRYPOINT [ "bash", "run.sh"]
