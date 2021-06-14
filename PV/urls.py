from django.urls import path
from . import views

urlpatterns = [
    path('generate/<int:pv_id>/', views.generer_pv, name='generer_pv'),
    path('share/<int:pv_i>/', views.partager_pv, name='partager_pv')
]
