from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
  
# importing views from views..py
from .views import *
  
urlpatterns = [
    path('', PersonView.as_view()),
    path('attend', AttendanceView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

# https://241d-2405-201-17-f0cc-b498-3c83-3820-1a9c.ngrok.io