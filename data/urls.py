from django.urls import path
from . import views


urlpatterns =[
    path('', views.home_view, name='home'),
    path('bubble/', views.bubble_view, name='bubble'),
    path('bubble/seoul', views.Seoul_view, name='bubble-Seoul'),
    path('bubble/gyeonggi', views.Gyeonggi_view, name='bubble-Gyeonggi'),
    path('bubble/gangwon', views.Gangwon_view, name='bubble-Gangwon'),
    path('bubble/incheon', views.Incheon_view, name='bubble-Incheon'),
    path('bubble/gyeongsang', views.Gyeongsang_view, name='bubble-Gyeongsang'),
    path('bubble/chungcheong', views.Chungcheong_view, name='bubble-Chungcheong'),
    path('bubble/daejeon', views.Daejeon_view, name='bubble-Daejeon'),
    path('bubble/jeolla', views.Jeolla_view, name='bubble-Jeolla'),
    path('bubble/ulsan', views.Ulsan_view, name='bubble-Ulsan'),
    path('bubble/gwangju', views.Gwangju_view, name='bubble-Gwangju'),
    path('bubble/daegu', views.Daegu_view, name='bubble-Daegu'),
    path('bubble/busan', views.Busan_view, name='bubble-Busan'),
    path('bubble/jeju', views.Jeju_view, name='bubble-Jeju'),
    path('slidedate/', views.Slidedate, name='slidedate'),
    path('slidedate/seoul', views.Seoul_view_date, name='slidedate-Seoul'),
    path('test/', views.test, name='test'),
]
