from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/xml/', views.export_xml, name='export_xml'),
]
