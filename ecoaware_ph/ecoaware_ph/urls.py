from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from core.views import home

urlpatterns = [

    path('admin/', admin.site.urls),


    path('', home, name='home'),


    path('users/', include('users.urls', namespace='users')),
    path('articles/', include('articles.urls', namespace='articles')),
    path('campaigns/', include('campaigns.urls', namespace='campaigns')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
    path('about/', login_required(TemplateView.as_view(template_name='pages/about.html')), name='about'),


    path('api/chat/', include('core.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)