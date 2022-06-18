FROM debian:bullseye

# Install dependencies
RUN apt-get update -y && \
    apt-get install gcc nginx python3-certbot-nginx -y && \
    apt-get install python3.9 python3-pip -y &&\
    apt-get clean -y

# Install python for uwsgi and django project
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install --no-cache-dir uwsgi==2.0.20 django==3.2.13

# Copy the Django project to the container
COPY ./secret_key.txt /home/Server/secret_key.txt
COPY ./filesmanager /home/Server/filesmanager
COPY ./nginx_uwsgi /home/Server/nginx_uwsgi
COPY ./server /home/Server/server
COPY ./manage.py /home/Server/manage.py

# Copy the nginx config
RUN rm /etc/nginx/sites-enabled/default &&\
    rm /etc/nginx/sites-available/default &&\
    ln -s /home/Server/nginx_uwsgi/server.conf /etc/nginx/sites-enabled/server.conf && \
    ln -s /home/Server/nginx_uwsgi/server.conf /etc/nginx/sites-available/server.conf 
RUN /etc/init.d/nginx restart

# Config server data
RUN mkdir /home/Server/logs
RUN mkdir /home/ServerData
RUN mkdir /home/Public

# Config the uwsgi
RUN mkdir /usr/vassals
RUN ln -s /home/Server/nginx_uwsgi/uwsgi.ini /usr/vassals/

# Migration
RUN python3 /home/Server/manage.py makemigrations
RUN python3 /home/Server/manage.py migrate
RUN python3 /home/Server/manage.py collectstatic
RUN python3 /home/Server/manage.py createsuperuser
RUN python3 /home/Server/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

COPY ./run.sh /home/Server/run.sh

WORKDIR /

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]