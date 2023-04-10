from django.urls import path, include
from . import views # view파일을 include를 했다.==> view에 있는 landing을 이용하기 위해

urlpatterns = [
    path('', views.landing), # 아무것도 오지 않았을 때 view에 랜딩함,
    path('about_me/', views.about_me),

    path('blog/', include('blog.urls')),
]