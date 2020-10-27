from django.urls import path
from .views import *

urlpatterns = [
    path('',form_upload),
    path('prev/', prev_uploads, name='prev'),
]