import os
import glob
import filecmp
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .core import StringEncrypter
from .settings import PUBLIC_DIRECTORY
ENCRYPTER = StringEncrypter()

def login(request):
    if request.user.is_authenticated:
        return True
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return True
    else:
        return False
    
def logout(request):
    auth_logout(request)

def encrypt_id(files_name):
    return ENCRYPTER.encrypt(files_name)

def decrypt_id(id, get_dir=True):
    path = ENCRYPTER.decrypt(id)
    if os.path.isfile(path) and get_dir:
        return os.path.dirname(path)
    return path

def get_dict_files(path):
    # Get all public files in the directory
    public_ids = os.listdir(PUBLIC_DIRECTORY)
    # Get all files in the directory
    list_files = glob.glob(os.path.join(path, '*'))
    dict_files ={}
    for file_path in list_files:
        # get the file name
        file_name = os.path.basename(file_path)
        # set the init file size
        file_size = 'Dir'
        # get the id of the file
        file_id = encrypt_id(file_path)
        # check if the path is file
        if os.path.isfile(file_path):
            # calculate the file size
            file_size = os.path.getsize(file_path) / 1024 / 1024 # to MB
            file_size = round(file_size, 1)
            if file_size < 500.0:
                file_size = str(file_size) + 'MB'
            else:
                file_size = str(round(file_size / 1024, 1)) + 'GB'
        # check if the file is public
        if file_id in public_ids:
            status = 'public'
        else:
            status = 'private'
        dict_files.update({file_name:[file_path, file_id,file_size,status]})
    return dict_files
