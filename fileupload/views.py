import os
import tarfile
import zipfile
import shutil
from django.utils import timezone
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
#from .serializers import FileSerializer
from django.http import HttpResponse
from django.conf import settings
from .models import FILE
from django.core.files.base import ContentFile, File
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from django.http import Http404

@login_required
def form_upload(request):
    if request.method=="POST":
        form=FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file=request.FILES['file']
            if (zipfile.is_zipfile(file)):
                try:
                    with zipfile.ZipFile(file) as zip_file:
                        zip_name=zip_file.filename            #zipfile name
                        names=zip_file.namelist()             #list of file names in zip
                        info_list=zip_file.infolist()
                        for info in info_list:
                            spl=info.filename.split('/')
                            info.filename=spl[0]+'_'+request.user.username+'_'+str(timezone.now().strftime("%Y%m%d%H%M%S"))+'/'+spl[1]
                        path_dir=info_list[0].filename
                        zip_file.extractall(members=info_list,path=settings.UPLOAD_ROOT)
                        st=''
                        for name in names:
                            st+=name+ ', '
                except(KeyError, BadZipFile):
                    return render(request, 'home.html', {'msg': 'BadZipFile, try uploading again'})
            # elif tarfile.is_tarfile(file):
            #     with TarFile(file) as tar_file:
            #         names=tar_file.namelist()
            #         path_to_file=tar_file.extractall(settings.MEDIA_ROOT)
            #         st=''
            #         for name in names:
            #             st+=name+ ', '
                time=timezone.now()
                fil=FILE()
                fil.user=request.user
                fil.timestamp=time
                fil.name=zip_name
                fil.file.save(request.user.username+'_'+str(time.strftime("%Y%m%d%H%M%S"))+'.csv',ContentFile(st))
                url1=fil.file.url
                shutil.rmtree(os.path.join(settings.UPLOAD_ROOT,path_dir))
                return render(request, 'download.html', {'url': request.build_absolute_uri(url1)})
    
        else:
            return render(request, 'home.html', {'msg': 'Please try again'})

    else:
        raise Http404("Page Not Found")

def prev_uploads(request):
    queryset=FILE.objects.filter(user=request.user)
    return render(request, 'prev.html', {'obj':queryset})