from django.shortcuts import render # render는 사용자한테 보내는 거
from blog.models import Post

# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render( # 사용자한테 보여줘라, 최종적으로 보여 줄 html폴더
        request,
        'single_pages/landing.html', # 클라이언트한테 single_pages 밑에 있는 landing.html을 보여줘라
        {
            'recent_posts':recent_posts,
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html',
    )

