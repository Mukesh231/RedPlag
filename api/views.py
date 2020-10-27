# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from .serializers import FileSerializer
# from django.http import HttpResponse
# from django.conf import settings
# from .models import FILE
# from django.core.files.base import ContentFile, File
# import tarfile
# import zipfile

# class UploadFileView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file=request.FILES['file']
#         if (zipfile.is_zipfile(file)):
#             with zipfile.ZipFile(file) as zip_file:
#                 names=zip_file.namelist()
#                 zip_file.extractall(settings.MEDIA_ROOT)
#                 st=''
#                 for name in names:
#                     st+=name+ ', '
#         elif tarfile.is_tarfile(file):
#             with TarFile(file) as tar_file:
#                 names=tar_file.namelist()
#                 tar_file.extractall(settings.MEDIA_ROOT)
#                 st=''
#                 for name in names:
#                     st+=name+ ', '
#         # #curTime=strftime("__%Y_%m_%d", time.localtime())
#         fil=FILE()
#         fil.file.save('response.csv',ContentFile(st))
#         url1=fil.file.url
#         return Response(request.build_absolute_uri(url1))
#         #return Response(file.name)