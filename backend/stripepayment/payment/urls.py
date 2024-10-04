from django.urls import path
from . import views  # Assuming your views are in the same app

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    
]