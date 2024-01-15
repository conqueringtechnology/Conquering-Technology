from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views as user_views
from .views import DownloadResumeView


app_name = 'app'

urlpatterns = [
    path('', user_views.home, name='home'),
    path('home/', user_views.home, name='app_home'),  
    path('projects/', user_views.projects, name='app_projects'),  
    path('resume/', user_views.resume, name='app_resume'),
    path('contact/', user_views.contact, name='app_contact'),
    path('generate-qr-code/', user_views.generate_qr_code, name='app_generate_qr_code'),
    path('project-files/<str:pdf_filename>/', user_views.project_files, name='project_files'),
    path('download-resume/', DownloadResumeView.as_view(), name='app_download_resume'),
]

## Serve static files for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
