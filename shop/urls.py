from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name="shop/home.html"), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
	path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('invoice_create/', invoice_create, name='invoice_create'),
    path('invoice_list/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice_detail/<int:invoice_id>/', InvoiceDetailView.as_view(), name='invoice_detail'),

    path('goods_list/', goods_list, name='goods_list'),
]
