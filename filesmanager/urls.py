import hashlib
from django.urls import path

from . import views

app_name = 'filesmanager'

# URL function name
signout = hashlib.sha256(b'this URL is for sign out').hexdigest()
topublic = hashlib.sha256(b'make file public').hexdigest()
toprivate = hashlib.sha256(b'make file private').hexdigest()
godir = hashlib.sha256(b'go to directory').hexdigest()
upload = hashlib.sha256(b'upload file').hexdigest()
download = hashlib.sha256(b'download file').hexdigest()
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('drive/', views.Drive.as_view(), name='drive'),
    path('browser/', views.Browser.as_view(), name='browser'),
    path('browser/<str:id>', views.Browser.as_view(), name='browser'),
    path('{}/'.format(str(signout)), views.SignOut.as_view(), name='signout'),
    path('{}/<str:id>'.format(str(download)), views.DownUpload.as_view(), name='download'),
    path('{}/'.format(str(upload)), views.DownUpload.as_view(), name='upload'),
    path('{}/<str:id>'.format(str(topublic)), views.ToPublic.as_view(), name='topublic'),
    path('{}/<str:id>'.format(str(toprivate)), views.ToPrivate.as_view(), name='toprivate'),
    path('{}/'.format(str(godir)), views.GoDir.as_view(), name='godir'),
]