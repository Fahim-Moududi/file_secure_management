from django.urls import path
from .views import RegisterView, UploadFileView, ListFilesView, DownloadFileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view()),        # login
    path('token/refresh/', TokenRefreshView.as_view()),   # refresh
    path('upload/', UploadFileView.as_view()),
    path('files/', ListFilesView.as_view()),
    # path('download/<int:pk>/', DownloadFileView.as_view()),
    path("download/", DownloadFileView.as_view()),
]
