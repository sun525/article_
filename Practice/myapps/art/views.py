from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from art import tasks
from art.models import Art

# Create your views here.
from user import helper
import redis_
from redis_ import rd

@cache_page(30)
def show(request, id):
    # 阅读art_id的文章
    login_user = helper.getLoginInfo(request)
    art = Art.objects.get(pk=id)

    # 写入到阅读排行中(Redis -> ReadTopRank)
    redis_.incrTopRank(id)

    readTopRank = redis_.getReadTopRank(7)  # [(<>,score)]

    return render(request, 'art/show.html', locals())

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'base.html', {'error_msg': error_msg})

    art_list = Art.objects.filter(Q(title__icontains=q)|Q(author__icontains=q))
    return render(request, 'art/search.html', {'error_msg': error_msg,
                                               'art_list': art_list})

def detail(request, id):
    art = Art.objects.get(pk=id)
    return render(request, 'art/detail.html', locals())

def qdArt(request, id):
    # 获取当前登录用户的信息
    login_user = helper.getLoginInfo(request)
    if not login_user:
        return JsonResponse({'msg': '请先登录', 'code': 101})

    # # 判断当前用户是否已抢过
    # uid = login_user.get('id')
    # if rd.hexists('qdArt', uid):
    #     return JsonResponse({'msg': '您已抢过,只能抢一本,不能继续',
    #                          'code': 205})

    tasks.qdTask.delay(login_user.get('id'), id)  # 延迟异步执行
    return JsonResponse({'msg': '正在抢读', 'code': 201})


def queryQDState(request, id):
    login_user = helper.getLoginInfo(request)
    if not login_user:
        return JsonResponse({'msg': '请先登录', 'code': 101})

    uid = login_user.get('id')
    # print(uid)
    if rd.hexists('qdArt', uid):
        # 一个用户抢两本书,查询最新的id的抢读状态,而不是之前抢读的状态
        qdId = rd.hget('qdArt', uid)  # 已抢的书id,  qdId和id可能不一样
        print(qdId)
        art = Art.objects.get(pk=id)
        print(art.title)
        return JsonResponse({'msg': '抢读成功',
                             'code': 200,
                             'art': {
                                 'title': art.title,
                                 'author': art.author,
                             }})
    if rd.hlen('qdArt') < 5:
        return JsonResponse({'msg': '正在抢读', 'code': 201})
    else:
        return JsonResponse({'msg': '抢读失败', 'code': 300})
