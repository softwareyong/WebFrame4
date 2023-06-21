from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Sale

# Create your views here.

def index(request):
    # posts = Post.objects.all().order_by('-pk')
    # posts = Post.objects.all() # objects 하면 여기에 실제로 들어있는 데이터
                                # get, lastm first, all등을 통해서 원하는 데이터를 가져 올 수 있다.
                                # 리스트 형식으로 가져옴
                                # 이때가 데이터베이스를 가져오는 순간이다.
                                # 그래서 가져올 때 쿼리를 날려서
                                # pk를 역순으로 가져오기
    return render(
        request,
        'blogs/index.html', # 함수명이랑 html이랑 이름 안같아도 됨 자유
        {

        } # 데이터를 넘길 때 json형식으로, index.html에게 넘기기, index로 가셈 이제, 확인
    )

class ProductList(ListView): # 모델명: post_list.html, post_list라는 변수를 자동으로 넘겨줌
    model = Product
    ordering = '-pk'
    paginate_by = 3  # page마다 post 몇개 보여 줄 지
    template_name = 'blogs/product_list.html'


class ProductDetail(DetailView): # 모델명: post_detail.html, post라는 변수를 자동으로 넘겨줌
    model = Product
    template_name = 'blogs/product_detail.html'

class CartList(ListView):
    model = Sale
    paginate_by = 3  # page마다 post 몇개 보여 줄 지
    template_name = 'blogs/sale_list.html'
