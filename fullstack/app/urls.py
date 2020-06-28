from django.urls import path
from . import views
urlpatterns = [
    path('paymentPortal', views.paymentPortal, name='paymentPortal'),
    path('paymentDesk',views.paymentDesk,name='paymentDesk'),
    path('otpDesk',views.otpDesk,name='otpDesk')
]
