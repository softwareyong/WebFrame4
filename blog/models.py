from django.db import models
from django.contrib.auth.models import User
import os

# 다대다 관계
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name # pk:고유번호

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name # pk:고유번호

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)# 30글자까지 title가능,char형으로
    hook_text = models.CharField(max_length=100, blank=True) # blank는 옵션
    content = models.TextField()# 넓게 쓸 수 있는 공간

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True) # 년,월,일로 구분해서 구분하겠다.

    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True==> 현재시간 자동 추가
    update_at = models.DateTimeField(auto_now=True) # 자동 입력

    # author
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # 이 사람과 연관된거 모두 제거 # on_delete=nodels.SET_NULL, on_delete=nodels.CASCADE
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # manytomany ==> 다대다관계
    tags = models.ManyToManyField(Tag, blank=True) # 없으면 자동으로 null이 됨, 그래서 안해도됨

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}' #pk:고유번호

    def get_absolute_url(self):
        return f'/blog/{self.pk}/' # blog밑에 자동적으로 주소 뒤에 붙은 걸 호출한다.

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'