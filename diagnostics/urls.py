from django.urls import path
from .views import create_report, list_reports

app_name = "diagnostics"
urlpatterns = [
    path("", list_reports, name="list"),
    path("new/", create_report, name="new"),
]
