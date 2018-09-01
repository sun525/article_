"""Practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import json

from django.conf.urls import url, include
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
import xadmin as admin
from art.models import Tag, Art
from user import helper
from api_ import router

def toIndex(request):
    # 加载所有的分类
    # tags = Tag.objects.all()
    # annotate为每个tag对象增加一个字段(Count('art'))统计每种类型下文章数量
    tags = Tag.objects.annotate(arts=Count('art')).filter(arts__gte=1)
    # 读取分类id
    tag_id = request.GET.get('tag')

    # 加载所有文章
    if tag_id:
        tag_id = int(tag_id)
        # filter()过滤
        # exclude()排除
        arts = Art.objects.filter(tag_id=tag_id)
    else:
        arts = Art.objects.all()
    # 将文章进行分页处理
    # 分页器
    paginator = Paginator(arts, 10)
    page = request.GET.get('page')
    # 读取请求参数中的page参数,没有则默认为1
    page = int(page) if page else 1
    # 获取第page页的数据
    pager = paginator.page(page)

    # 获取登录用户的信息
    login_user = helper.getLoginInfo(request)

    # locals()是将当前函数的局部变量转成字典的key-value
    # {'request':request,'tags':tags}
    return render(request, 'index.html', locals())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^art/', include('art.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^', toIndex),
]

