from django.urls import path
from . import views

urlpatterns = [
    path('<int:pv_id>/', views.generer_pv, name='generer_pv'),
    path('<int:pv_i>/', views.partager_pv, name='partager_pv')

]
