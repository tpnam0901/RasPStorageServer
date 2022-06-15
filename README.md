# Server

# Install dependencies
sudo apt-get update -y 
sudo apt-get install python3-venv
sudo apt-get install gcc nginx python3.8-dev certbot -y
sudo apt-get clean
pip install django==3.2.12
pip install uwsgi==2.0.20
python -m venv env
source activate env/bin/activate
source env/bin/activate

# Change config
replace
server_name user.com www.user.com;  in nginx_uwsgi/server.conf
ALLOWED_HOSTS = ["yourserver.com","www.yourserver.com"] in settings.py

MEDIA_ROOT = "/home/user/DriveServer/server/media"
STATIC_ROOT= "/home/user/DriveServer/server/static"

replace 
server.conf

replace
uwsgi.ini

create
secret_key.txt


# Copy the nginx config
ln -s ./nginx_uwsgi/server.conf /etc/nginx/sites-enabled/server.conf && \
ln -s ./nginx_uwsgi/server.conf /etc/nginx/sites-available/server.conf 
/etc/init.d/nginx restart

# Config server data
RUN mkdir ./logs

# Config the uwsgi
RUN uwsgi --ini /Server/nginx_uwsgi/uwsgi.ini
RUN mkdir /usr/local/vassals
RUN ln -s /Server/nginx_uwsgi/uwsgi.ini /usr/local/
COPY ./run.sh .

# Migration
python /Server/manage.py makemigrations
python /Server/manage.py migrate
python /Server/manage.py collectstatic
python /Server/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
