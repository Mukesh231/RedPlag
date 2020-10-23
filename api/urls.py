from django.urls import path
from .views import *

urlpatterns = [
    path('', UploadFileView.as_view()),
]