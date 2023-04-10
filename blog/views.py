from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post # 데이터 베이스를 접근하기 위해

# Create your views here.
class PostList(ListView): #ListView를 상속받을 꺼임, 원래있는 라이브러리 뷰지원하는
                        # 예는 모델명이: 모델명_list.html
                        # 으로 고정되어 있음.
                        # 근데 수동으로 바꿀 수 있음.
                        # template_name = 'blog/post_list.html' 이렇게 하면 바뀜
    model = Post
    ordinary = '-pk'
    # template_name = 'blog/post_list.html'

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     # posts = Post.objects.all() # objects 하면 여기에 실제로 들어있는 데이터
#                                 # get, lastm first, all등을 통해서 원하는 데이터를 가져 올 수 있다.
#                                 # 리스트 형식으로 가져옴
#                                 # 이때가 데이터베이스를 가져오는 순간이다.
#                                 # 그래서 가져올 때 쿼리를 날려서
#                                 # pk를 역순으로 가져오기
#     return render(
#         request,
#         'blog/post_list.html', # 함수명이랑 html이랑 이름 안같아도 됨 자유
#         {
#             'posts':posts,
#         } # 데이터를 넘길 때 json형식으로, index.html에게 넘기기, index로 가셈 이제, 확인
#     )
def single_post_page(request, pk):
    post = Post.objects.get(pk=pk) # 전달인자로 pk가 오면 여기에 해당하는 post 1개만 가져오기
                                    # select에 조건문을 달아주는 개념임
                                    # 이제 post를 넘겨줘야 한다.
                                # 넘겨주는 방법은?
                                # 밑에처럼 json형식으로 넘겨준다.
    return render(
        request,
        'blog/single_post_page.html',
        {
            'post':post,
        }
    )