from django.urls import path
from . import views

urlpatterns = [
    path('enseignants/', views.list_enseignants, name='enseignants_list'),
    path('enseignant/<int:enseignant_id>/', views.enseignant_timetable, name='enseignant_timetable'),
    path('classes/', views.list_classes, name='classes_list'),
    path('classe/<int:classe_id>/', views.classe_timetable, name='classe_timetable'),
]
