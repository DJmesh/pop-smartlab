from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_reports, name="list"),
    path("new/", views.create_report, name="new"),
    path("<int:pk>/", views.report_detail, name="detail"),
]
