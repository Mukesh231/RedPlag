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
    """!
    User can upload a file. This is where the core logic is applied.

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser
    
    
    
    
    
    """
    if request.method=="POST":
        form=FileUploadForm(request.POST, request.FILES)
        time=timezone.now()
        if form.is_valid():
            file=request.FILES['file']
            if (zipfile.is_zipfile(file)):
                try:
                    with zipfile.ZipFile(file) as zip_file:
                        zip_name=zip_file.filename            #zipfile name
                        names=zip_file.namelist()             #list of file names in zip
                        info_list=zip_file.infolist()
                        #print(info_list)
                        for info in info_list:
                            spl=info.filename.split('/')
                            info.filename=spl[0]+''+request.user.username+''+str(timezone.now().strftime("%Y%m%d%H%M%S"))+'/'+spl[1]
                        path_dir=info_list[0].filename
                        zip_file.extractall(members=info_list,path=settings.UPLOAD_ROOT)
                except Exception as e:
                    return render(request, 'home.html', {'msg': 'Please try uploading again'})
            
                
                temporary_inp="python3 testing.py ./uploads/" + str(path_dir)
                os.system(temporary_inp)

                fil=FILE()
                fil.user=request.user
                fil.timestamp=time
                fil.name=zip_name
                newfilename=request.user.username+'_'+str(time.strftime("%Y%m%d%H%M%S"))+'.csv'
                fil.file.save(newfilename, ContentFile(''))
                url1=fil.file.url

                temporary_inp2="cp results.csv ./media/"+ newfilename

                os.system(temporary_inp2)
                f=open(os.path.join(settings.BASE_DIR,'results.csv'))
                titles=f.readline().split(',')[1:]
                data=np.genfromtxt(os.path.join(settings.BASE_DIR,'results.csv'), delimiter=',')
                data=np.delete(data,(0),axis=0)
                data=np.delete(data,(0),axis=1)
                data=np.around(data,2)

                fig= plt.figure(figsize=(16,12)) 
                ax = fig.add_subplot(111)
                im = ax.imshow(data, origin='lower', interpolation='None', cmap='viridis_r')

                ax.set_xticks(np.arange(len(titles)))
                ax.set_yticks(np.arange(len(titles)))
                ax.set_xticklabels(titles)
                ax.set_yticklabels(titles)

                plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                        rotation_mode="anchor")

                for i in range(len(titles)):
                    for j in range(len(titles)):
                        text = ax.text(j, i, data[i, j],
                                    ha="center", va="center", color='black')

                fig.colorbar(im)
                fig.tight_layout()
                plt.savefig(os.path.join(settings.MEDIA_ROOT,request.user.username+'_'+str(time.strftime("%Y%m%d%H%M%S"))+'.png'))
                
                os.remove('results.csv')
                shutil.rmtree(os.path.join(settings.UPLOAD_ROOT,path_dir))
                return render(request, 'download.html', {'url': request.build_absolute_uri(url1), 'image':os.path.join(settings.MEDIA_ROOT,request.user.username+'_'+str(time.strftime("%Y%m%d%H%M%S"))+'.png')})
    
        else:
            return render(request, 'home.html', {'msg': 'Please try again' })

    else:
        raise Http404("Page Not Found")

@login_required
def prev_uploads(request):
    """!
    This is used to fetch all the previous submissions made by the user.    
    
    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser
    
    
    """
    queryset=FILE.objects.filter(user=request.user)
    return render(request, 'prev.html', {'obj':queryset})
