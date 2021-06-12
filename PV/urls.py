
from django.urls import path
from . import views
urlpatterns = [
    path('<int:pv_id>/',views.generer_pv,name='generer_pv'),
]
