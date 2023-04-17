from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)# 30글자까지 title가능,char형으로
    hook_text = models.CharField(max_length=100, blank=True) # blank는 옵션
    content = models.TextField()# 넓게 쓸 수 있는 공간

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True) # 년,월,일로 구분해서 구분하겠다.
    # 실

    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True==> 현재시간 자동 추가
    update_at = models.DateTimeField(auto_now=True) # 자동 입력
    # author

    def __str__(self):
        return f'[{self.pk}] {self.title}' #pk:고유번호

    def get_absolute_url(self):
        return f'/blog/{self.pk}/' # blog밑에 자동적으로 주소 뒤에 붙은 걸 호출한다.