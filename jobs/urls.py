from django.urls import path
from .views import match_jobs

urlpatterns = [
    path('api/match-jobs/', match_jobs, name='match-jobs'),
]
