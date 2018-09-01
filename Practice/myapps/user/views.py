import json
import os
import uuid

from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Practice import settings
from user import helper
from user.forms import UserForm

# Create your views here.
from user.models import UserProfile


def regist(request):
    if request.method == 'POST':
        # 通过ModelForm模型表单类 验证数据并保存到数据库中
        userForm = UserForm(request.POST)
        if userForm.is_valid():  # 判断必要字段是否都有值
            user = userForm.save()  # 保存数据
            # 注册成功,将用户的id,用户名和头像地址写入session(同时将session数据存入redis缓存中)
            helper.addLoginSession(request, user)
            return redirect('/')

        # post提交时有验证错误,将验证错误转成json-->dict对象
        errors = json.loads(userForm.errors.as_json())
        print(errors)
    return render(request, 'user/regist.html', locals())

@csrf_exempt
def uploadPhoto(request) -> HttpResponse:
    # 上传头像 -> request.FILES 字典中 {'字段名': InMemoryUploadedFile}
    if request.method == 'POST':
        # uploadFile: InMemoryUploadedFile声明类型
        uploadFile: InMemoryUploadedFile = request.FILES.get('photoImg')  # 上传文件表单的字段名为photoImg

        # 生成新的文件名
        newFileName = str(uuid.uuid4()).replace('-', '')+'.'+uploadFile.name.split('.')[-1]

        # 确定生成新的文件的目录
        dirPath = os.path.join(settings.BASE_DIR, 'static/users/photo/')
        # 判断目录是否存在
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(os.path.join(dirPath, newFileName), 'wb') as f:
            for chunk in uploadFile.chunks():  # 分段写入新的文件中(缓存块)
                f.write(chunk)

        return JsonResponse({'status': 200,
                             'path': '/static/users/photo/' + newFileName})
    return JsonResponse({'status': 200,
                         'msg': '上传失败,目前请求只支持post!'})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        errors = {}
        if not username or len(username.strip()) < 8:
            errors['username'] = [{'message': '用户名不符合规定'}]
        if not password or len(password.strip()) < 8:
            errors['password'] = [{'message': '密码不符合规定'}]

        if not errors:
            # 验证通过
            qs = UserProfile.objects.filter(username=username)  # queryset查询结果
            if not qs.exists():
                errors['username'] = [{'message': '无此用户'}]
            else:
                user = qs.first()  # 读取查询结果中的第一条记录
                if not check_password(password, user.password):
                    errors['password'] = [{'message': '用户名或密码错误'}]
                else:
                    helper.addLoginSession(request, user)
                    return redirect('/')
    return render(request, 'user/login.html', locals())


def logout(request):
    login_user = helper.getLoginInfo(request)
    if login_user:
        # 从session中删除登录信息
        del request.session['login_user']
        # request.session.clear()
    return redirect('/')