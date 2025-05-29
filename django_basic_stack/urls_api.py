from django.urls import include, path

urlpatterns = [
    path('membership/', include('apps.membership.urls_api')),
]
