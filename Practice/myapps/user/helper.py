import json


def getLoginInfo(request) -> dict:
    '''
    获取登录用户的信息
    :param request: 请求对象
    :return:
    '''
    login_user = request.session.get('login_user')
    if login_user:
        login_user = json.loads(login_user)     # str -> dict

    return login_user

def addLoginSession(request, user):
    '''
    向session中添加信息
    :param request:
    :param user:
    :return:
    '''
    request.session['login_user'] = json.dumps({'id': user.id,
                                                'name': user.username,
                                                'photo': user.photo
                                                })