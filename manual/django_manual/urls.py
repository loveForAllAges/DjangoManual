from django.urls import path, include
from .views import *


views_urlpatterns = [
    path('View', CustomView.as_view(), name='class-view'),
    path('TemplateView', CustomTemplateView.as_view(), name='class-template-view'),
    path('RedirectView', CustomRedirectView.as_view(), name='class-redirect-view'),
]


urlpatterns = [
    path('', upload_file),
    path('2', FileFieldFormView.as_view()),
    path('views/', include(views_urlpatterns)),
]
