import os
import re
import mimetypes

from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, StreamingHttpResponse
from django.views import View
from django.urls import reverse

from wsgiref.util import FileWrapper

from . import utils

from .core import RangeFileWrapper
from .settings import SERVER_DATA_DIR, PUBLIC_DIRECTORY

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)

# Create your views here.
class Home(View):
    """Home page"""
    def get(self, request):
        return render(request, 'home.html')
    
class SignIn(View):
    """Basic sign in view"""
    def get(self, request):
        # check if user is logged in
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('filesmanager:drive'))
        return render(request, 'signin.html')
    # API for sign in
    def post(self, request):
        # Get username and password from form
        verify = utils.login(request)
        if verify:
            return HttpResponseRedirect(reverse('filesmanager:drive'))
        return render(request, 'signin.html', {'message': 'Wrong username or password!'})
    
class Drive(View):
    """Base drive view"""
    def get(self, request):
        # check if user is logged in
        if request.user.is_authenticated:
            return render(request, 'drive.html')
        return render(request, 'redirect.html')
    
class SignOut(View):
    """API for sign out"""
    def get(self, request):
        utils.logout(request)
        return HttpResponseRedirect(reverse('filesmanager:signin'))
    
class Browser(View):
    """ The main view for the browser """
    def get(self, request, id=None):
        # check if the user is logged in
        if request.user.is_authenticated:
            # add base directory
            if id is None:
                base_dir = SERVER_DATA_DIR
            else:
                base_dir = utils.decrypt_id(id)
            # check if the directory exists
            if not os.path.exists(base_dir):
                return HttpResponseNotFound()
            # create base directory to context
            context = {'base_dir':base_dir}
            # get the parent directory
            context.update({'parent_dir':utils.encrypt_id(os.path.dirname(base_dir))})
            # add current files in the directory
            list_files = utils.get_dict_files(base_dir)
            context.update({'list_files':list_files})
            return render(request, 'browser.html', context)
        return render(request, 'redirect.html')

class DownUpload(View):
    """API for download and upload files"""
    def get(self, request, id=None):
        # check if the request provided a file id
        if id is None:
            return HttpResponseNotFound()  
        # get the path from the id
        path = utils.decrypt_id(id, get_dir=False)
        # check if the file exists
        if not os.path.exists(path):
            return HttpResponseNotFound()  
        # check if user is logged in or the file is public
        if request.user.is_authenticated or os.path.exists(os.path.join(PUBLIC_DIRECTORY, id)):
            # if the path is the directory, redirect to the browser
            if os.path.isdir(path):
                return HttpResponseRedirect(reverse('filesmanager:browser', args=(id,)))
            # process resume download stream
            range_header = request.META.get('HTTP_RANGE', '').strip()
            range_match = range_re.match(range_header)
            size = os.path.getsize(path)
            content_type, encoding = mimetypes.guess_type(path)
            content_type = content_type or 'application/octet-stream'
            if range_match:
                first_byte, last_byte = range_match.groups()
                first_byte = int(first_byte) if first_byte else 0
                last_byte = int(last_byte) if last_byte else size - 1
                if last_byte >= size:
                    last_byte = size - 1
                length = last_byte - first_byte + 1
                resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
                resp['Content-Length'] = str(length)
                resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
            else:
                resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
                resp['Content-Length'] = str(size)
            resp['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(path))
            resp['Accept-Ranges'] = 'bytes'
            return resp
        # require login or public access
        else:
            return HttpResponseForbidden() 
    def post(self, request):
        file = os.path.join(request.POST["base_dir"],request.FILES['file_upload'].name)
        i = 1
        while os.path.exists(file):
            filename, filext = os.path.splitext(request.FILES['file_upload'].name)
            file = os.path.join(request.POST["base_dir"], filename + f"({i})" + filext)
            i+=1
        with open(file, 'wb+') as destination:
            for chunk in request.FILES['file_upload'].chunks():
                destination.write(chunk)
        return HttpResponseRedirect(reverse('filesmanager:browser', args=(utils.encrypt_id(request.POST["base_dir"]),)))
    
    
class ToPublic(View):
    """API for make a file public"""
    def get(self, request, id=None):
        if request.user.is_authenticated and id is not None:
            file_path = os.path.join(PUBLIC_DIRECTORY, id)
            with open(file_path,'w') as f:
                f.write('This is public files')
            return HttpResponseRedirect(reverse('filesmanager:browser', args=(id,)))
            

class ToPrivate(View):
    """API for make a file private"""
    def get(self, request, id=None):
        if request.user.is_authenticated and id is not None:
            path = os.path.join(PUBLIC_DIRECTORY, id)
            if os.path.exists(path):
                os.remove(path)
            return HttpResponseRedirect(reverse('filesmanager:browser', args=(id,)))
        
class GoDir(View):
    """API for go to a directory by enter the path"""
    def post(self, request):
        dir_path = request.POST['directory']
        if dir_path.endswith('/'):
            dir_path = dir_path[:-1]
        dir_id = utils.encrypt_id(dir_path)
        return HttpResponseRedirect(reverse('filesmanager:browser', args=(dir_id,)))