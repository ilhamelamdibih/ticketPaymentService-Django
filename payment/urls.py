from django.urls import path
from .views import PaymentList,PaymentDetail,PaymentCreate

urlpatterns = [

    path('payment/', PaymentList),
    path('payment/<int:pk>/', PaymentDetail),
    path('payment-create/', PaymentCreate),

]