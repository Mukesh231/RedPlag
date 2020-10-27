from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup),
    #path('api/', include('api.urls')),
    path('file/', include('fileupload.urls')),
   # path('api-auth/', include('rest_framework.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name ='login'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),       
    path('home/', views.home, name='home'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name ='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

