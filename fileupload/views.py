from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
#from .serializers import FileSerializer
from django.http import HttpResponse
from django.conf import settings
from .models import FILE
from django.core.files.base import ContentFile, File
import tarfile
import zipfile
from .forms import FileUploadForm

def form_upload(request):
    if request.method=="POST":
        form=FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #print('valid')
            file=request.FILES['file']
            if (zipfile.is_zipfile(file)):
                with zipfile.ZipFile(file) as zip_file:
                    names=zip_file.namelist()
                    path_to_file=zip_file.extractall(settings.MEDIA_ROOT)
                    st=''
                    for name in names:
                        st+=name+ ', '
            elif tarfile.is_tarfile(file):
                with TarFile(file) as tar_file:
                    names=tar_file.namelist()
                    path_to_file=tar_file.extractall(settings.MEDIA_ROOT)
                    st=''
                    for name in names:
                        st+=name+ ', '
            # #curTime=strftime("__%Y_%m_%d", time.localtime())
            #print(path_to_file)
            fil=FILE()
            fil.file.save('response.csv',ContentFile(st))
            url1=fil.file.url
            return render(request, 'download.html', {'url': request.build_absolute_uri(url1)})
        else:
            print('shit happens')