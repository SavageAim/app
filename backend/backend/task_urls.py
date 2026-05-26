from django.urls import path, include

urlpatterns = [
    path('tasks/', include('django_cloud_tasks.urls')),
]
