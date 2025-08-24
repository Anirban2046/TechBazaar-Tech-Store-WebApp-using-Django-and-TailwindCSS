from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('invoice/<int:order_id>/pdf/', views.invoice_pdf, name='invoice_pdf'),

    
    ## SSLCOMMERZ URLs
    path('sslcommerz/init/', views.sslcommerz_init, name='sslcommerz_init'),
    path('sslcommerz/success/', views.sslcommerz_success, name='sslcommerz_success'),
    path('sslcommerz/fail/', views.sslcommerz_fail, name='sslcommerz_fail'),
    path('sslcommerz/cancel/', views.sslcommerz_cancel, name='sslcommerz_cancel'),
    
]