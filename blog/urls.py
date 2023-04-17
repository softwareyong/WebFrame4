from django.urls import path, include
from . import views # 블로그에 있는 view를 import

urlpatterns = [
    # path('', views.index), # 블로그에 들어와서 아무것도 치지 않았다면 view의 index를 보여줘라, server/blog/ 까지 온상태임, 만약에 /이거 붙이면 ==> server/ 이렇게로 바뀜
                            # '' 그냥 아무것도 안써야, server/blog/를 타고 왔기에 이주소로 남겨져 있음.

    path('', views.PostList.as_view()), #views.PostList쓰면 자동으로 가져옴
                                        # 근데 이거는 클래스라 동작으로 못해
                                        # 그래서 함수를 호출해준다 as_view

    path('<int:pk>/', views.PostDetail.as_view())
    # path('<int:pk>/', views.single_post_page), #pk라는 정수가 1개 들어온다는 뜻,
        # 프라이머리키에 따라서 보여주는 화면을 다르게 할꺼임
        # 따라서 views에 pk라는 전달인자를 1개 씀
        # def single_post_page(request, pk):
        # 정수가 들어오면 무조건 이렇게 됨

]