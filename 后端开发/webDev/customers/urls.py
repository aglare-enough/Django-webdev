from django.urls import path,re_path
from customers import views
urlpatterns=[
    path('login/',views.login_page),
    path('register/',views.rigister_page),
    path('register',views.rigister),
    path('login',views.login_),
    path('order',views.order),
    path('order/pay',views.pay),
    path('order/make',views.make),
    path('order/query_order',views.query_order),
    path('order/query_hisorder',views.query_hisorder),
    re_path(r'^(\d+)/info/$',views.personal_info),
    re_path(r'^\d+/logout/$',views.signout),
    re_path(r'^(\d+)/topup',views.topup)
]