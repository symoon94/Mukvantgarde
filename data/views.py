from django.http import HttpResponse
from django.shortcuts import render


def home_view(request, *args, **kwargs):
    return render(request, "data/home.html",{})

def bubble_view(request, *args, **kwargs):
    return render(request, "data/bubble.html",{})

def Seoul_view(request, *args, **kwargs):
    return render(request, "data/bubble/Seoul.html",{})

def Gyeonggi_view(request, *args, **kwargs):
    return render(request, "data/bubble/Gyeonggi.html",{})

def Gangwon_view(request, *args, **kwargs):
    return render(request, "data/bubble/Gangwon.html",{})

def Incheon_view(request, *args, **kwargs):
    return render(request, "data/bubble/Incheon.html",{})

def Gyeongsang_view(request, *args, **kwargs):
    return render(request, "data/bubble/Gyeongsang.html",{})

def Chungcheong_view(request, *args, **kwargs):
    return render(request, "data/bubble/Chungcheong.html",{})

def Daejeon_view(request, *args, **kwargs):
    return render(request, "data/bubble/Daejeon.html",{})

def Jeolla_view(request, *args, **kwargs):
    return render(request, "data/bubble/Jeolla.html",{})

def Ulsan_view(request, *args, **kwargs):
    return render(request, "data/bubble/Ulsan.html",{})

def Gwangju_view(request, *args, **kwargs):
    return render(request, "data/bubble/Gwangju.html",{})

def Daegu_view(request, *args, **kwargs):
    return render(request, "data/bubble/Daegu.html",{})

def Busan_view(request, *args, **kwargs):
    return render(request, "data/bubble/Busan.html",{})

def Jeju_view(request, *args, **kwargs):
    return render(request, "data/bubble/Jeju.html",{})

def Slidedate(request, *args, **kwargs):
    return render(request, "data/slidedate.html",{})

def Seoul_view_date(request, *args, **kwargs):
    return render(request, "data/slidedate/Seoul.html",{})

def tag_list_view(request, *args, **kwargs):
    return render(request, "data/tag_list.html",{})

def month_list_view(request, *args, **kwargs):
    return render(request, "data/month_list.html",{})

def test(request, *args, **kwargs):
    return render(request, "data/test2.html",{})
