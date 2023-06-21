
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('final4/', include('final4.urls')),
    path('admin/', admin.site.urls),
    path('', include('single_pages.urls')), # 없으면 싱글페이지 url로 가라
    path('blog/', include('blog.urls')),
    path("accounts/", include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 묶어줘라는 뜻 이주소는이제 ==> _media폴더로 간다.

