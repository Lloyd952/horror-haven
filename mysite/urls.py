from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

def redirect_to_blog(request):
    return redirect('blog:post_list')

urlpatterns = [
    path('', redirect_to_blog, name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
]
