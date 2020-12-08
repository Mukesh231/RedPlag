import os
import io
import base64
import tarfile
import zipfile
import shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from django.utils import timezone
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings
from .models import FILE
from django.core.files.base import ContentFile, File
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from django.http import Http404
from django.core.files.storage import FileSystemStorage

@login_required
def form_upload(request):
    """!
    Contents of a compressed file uploaded by the user are extracted and checked for cases of copying.
    The program generates outputs in a csv file and a colormap in the form of a similarity matrix
    User can download the csv file.
    
    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser

    """

    if request.method=="POST":
        form=FileUploadForm(request.POST, request.FILES)
        time=str(timezone.now().strftime("%Y%m%d%H%M%S"))
        if form.is_valid():
            file=request.FILES['file']
            if (zipfile.is_zipfile(file)):
                try:
                    with zipfile.ZipFile(file) as zip_file:
                        info_list=zip_file.infolist()
                        for info in info_list:
                            spl=info.filename.split('/')
                            info.filename=spl[0]+''+request.user.username+''+time+'/'+spl[1]
                        path_dir=info_list[0].filename
                        zip_file.extractall(members=info_list,path=settings.UPLOAD_ROOT)
                except Exception as e:
                    print(e)
                    return render(request, 'home.html', {'msg': 'Please try uploading again'})
            elif file.name.endswith("tar.gz"):
                fs= FileSystemStorage(location=settings.UPLOAD_ROOT)
                fname=fs.save(file.name,file)
                tar = tarfile.open(os.path.join(settings.UPLOAD_ROOT,fname), "r:gz")
                for info in tar:
                    spl=info.name.split('/')
                    info.name=request.user.username+'_'+time
                    if len(spl)==2:
                        info.name+='/'+spl[1]
                path_dir=request.user.username+'_'+time  
                tar.extractall(path=settings.UPLOAD_ROOT)
                tar.close()
                os.remove(os.path.join(settings.UPLOAD_ROOT,fname))
                
            elif file.name.endswith("tar"):
                fs= FileSystemStorage(location=settings.UPLOAD_ROOT)
                fname=fs.save(file.name,file)
                tar = tarfile.open(os.path.join(settings.UPLOAD_ROOT,fname), "r:")
                for info in tar:
                    spl=info.name.split('/')
                    info.name=request.user.username+'_'+time
                    if len(spl)==2:
                        info.name+='/'+spl[1]
                path_dir=request.user.username+'_'+time
                tar.extractall(path=settings.UPLOAD_ROOT)
                tar.close()
                os.remove(os.path.join(settings.UPLOAD_ROOT,fname))
            temporary_inp="python3 testing.py ./uploads/" + str(path_dir)
            os.system(temporary_inp)

            fil=FILE()
            fil.user=request.user
            fil.timestamp=timezone.now()
            fil.name=file.name
            newfilename=request.user.username+'_'+time+'.csv'
            fil.file.save(newfilename, ContentFile(''))
            url1=fil.file.url

            f=open(os.path.join(settings.BASE_DIR,'results.csv'))
            titles=f.readline().split(',')[1:]
            titles=[title.split('/')[-1] for title in titles]
            data=np.genfromtxt(os.path.join(settings.BASE_DIR,'results.csv'), delimiter=',')
            data=np.delete(data,(0),axis=0)
            data=np.delete(data,(0),axis=1)
            data=np.around(data,2)

            fig= plt.figure(figsize=(10,8)) 
            ax = fig.add_subplot(111)
            im = ax.imshow(data, origin='lower', interpolation='None', cmap='viridis_r')

            ax.set_xticks(np.arange(len(titles)))
            ax.set_yticks(np.arange(len(titles)))
            ax.set_xticklabels(titles, fontsize="x-large")
            ax.set_yticklabels(titles, fontsize="x-large")

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor")

            for i in range(len(titles)):
                for j in range(len(titles)):
                    text = ax.text(j, i, data[i, j],
                                ha="center", va="center", color="w", fontsize="x-large")

            fig.colorbar(im)
            fig.tight_layout()
            plt.savefig(os.path.join(settings.MEDIA_ROOT,request.user.username+'_'+time+'.png'))
            
            temporary_inp2="cp results.csv ./media/"+ newfilename
            os.system(temporary_inp2)
            os.remove('results.csv')
            shutil.rmtree(os.path.join(settings.UPLOAD_ROOT, path_dir))
            url2='/media/'+request.user.username+'_'+time+'.png'
            return render(request, 'download.html', {'url': request.build_absolute_uri(url1),'url2':request.build_absolute_uri(url2), 'image':'/media/'+request.user.username+'_'+time+'.png'})
        else:
            return render(request, 'home.html', {'msg': 'Please try again' })

    else:
        raise Http404("Page Not Found")

@login_required
def prev_uploads(request):
    """!
    This is used to fetch all the previous submissions made by a user.
    
    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser
    
    """
    
    queryset=FILE.objects.filter(user=request.user)
    return render(request, 'prev.html', {'obj':queryset})