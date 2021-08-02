from django.urls import path
from products import views
urlpatterns=[
    path('info/',views.product_info)
]