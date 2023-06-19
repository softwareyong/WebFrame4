from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Comment # 데이터 베이스를 접근하기 위해
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

def csrf_failure(request, reason=""):
    return redirect('/blog/')

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView): # form을 지원한다.
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # default template_name => post_form.html
    # template_name = 'blog/post_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
        # superuser나 스태프이상의 레벨이 있을 때, 글을 작성할 수 있도록, 일반유저는 안됨(아이디없는사람)
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user # 맞을경우, 현재 사용자명을 그대로 사용자한테 넣어준다.
            # not tag
            return super(PostCreate, self).form_valid(form) # form내용을 검증하는 상위 클래스로 보내준다.
        else:
            return redirect('/blog/') # 그렇지 않을겨우, 아무유저도 아니면, blog url로 다시 리다이렉션 시켜버린다.

class PostList(ListView): # 모델명: post_list.html, post_list라는 변수를 자동으로 넘겨줌
    model = Post
    ordering = '-pk'
    paginate_by = 2 # page마다 post 몇개 보여 줄 지

    # 추가 context-Category
    # 글 전부를 담아서 넘김
    def get_context_data(self, **kwargs): # template쪽으로 context가 넘어감
        context = super(PostList, self).get_context_data() # post_list
        context['categories'] = Category.objects.all() # 카테고리들을 저장함
        context['no_category_post_count'] = Post.objects.filter(category=None).count() # 분류되지 않는 카테고리에다가, 숫자를 저장함
        return context # -> post_list.html {post_list, categories, no_category_post_count}
class PostDetail(DetailView): # 모델명: post_detail.html, post라는 변수를 자동으로 넘겨줌
    model = Post
    # template_name = 'blog/single_post_page.html'
    # post라는 변수에 1개만 넘김
    def get_context_data(self, **kwargs):  # template쪽으로 context가 넘어감
        context = super(PostDetail, self).get_context_data()  # post_list
        context['categories'] = Category.objects.all()  # 카테고리들을 저장함
        context['no_category_post_count'] = Post.objects.filter(category=None).count()  # 분류되지 않는 카테고리에다가, 숫자를 저장함
        context['comment_form'] = CommentForm
        return context  # -> post_list.html {post, categories, no_category_post_count}

def category_page(request, slug):
    if slug == 'no_category': #/blog/category/no_category/
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else: # /blog/category/slug (프로그래밍, 문화-예술 등등)
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    # return으로 위에서 일부골라낸것만 보내고, 그리고 내가 원하는거 추가해서 보낸다.
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category, # 현재 분류에 대한 이름을 추가해서 보냈음. 지금 무슨 카테고리인지 알 수 있도록
        }
    )

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name= "blog/post_update_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk) # Post.objects.filter 현재 pk만 가져온다

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied # 로그인안된 상태에서 접근하려하면 승인에러

def delete_comment(request, pk):
    # Commnet라는 모델을 가져온 적이 없기에, 가져와야함
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment  # 자동으로 댓글 수정 폼에 내용 채워라?
    form_class = CommentForm
    # comment_form.html -> 이걸 자동으로 찾음. 안 만들면, 못 찾는다고 에러 뜸!

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# ListView에서 자동으로 이런것들을 전부 상속받았음
# class PostList(ListView): model=Post(Post.objects.all) # post_list.html
# def get_queryset(self):
#       post_list=Post.objects.all  이렇게됌.

class PostSearch(PostList):  # post_list.html
    paginated_by = None  # pagination 안하겠다

    def get_queryset(self):  # Post(Post.objects.all) 이게 불러와진다
        q = self.kwargs['q']
        post_list = Post.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return post_list

    def get_context_data(self, **kwargs): # 검색한 결과를 보여주기 위해서
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q'] # 검색어를 가져온다.
        context['search_info'] = f'Search:{q}({self.get_queryset().count()})'
        # search_info라는 값에다가 문자열을 넣어서 보내라, 추가적인 context, 전체 쿼리셋

        return context







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

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk) # 전달인자로 pk가 오면 여기에 해당하는 post 1개만 가져오기
#                                     # select에 조건문을 달아주는 개념임
#                                     # 이제 post를 넘겨줘야 한다.
#                                 # 넘겨주는 방법은?
#                                 # 밑에처럼 json형식으로 넘겨준다.
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post,
#         }
#     )