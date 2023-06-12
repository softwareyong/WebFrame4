from django.contrib import admin
from .models import Post, Category, Tag, Comment# 모델이라 정의된 post클래스가 여기 올라옴

# Register your models here.
admin.site.register(Post) # 등록하기 ==> admin.site, 관리자사이트를 의미함, 여기서 post서비스를 올리겠다는 뜻
                         # 데이터베이스가 바뀌면 무조건 migration 작업을 해야함. ==> 한글 12쪽 보셈
                         # python manage.py makemigrations, 어 새로운 데이터베이스가 생겼네 
                         # 고거에 맞춰서 테이블을 생성함

admin.site.register(Comment)
# 슬러그 필드를
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)