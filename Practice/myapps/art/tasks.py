import time
from Practice.celery import app
from redis_ import rd

@app.task
def qdTask(uid, aid):
    '''
    异步执行抢读的功能
    :param uid: 用户id
    :param aid: 文章id
    :return:
    '''
    # 判断qdArt的hash项是否已达到最大值(5本书)
    if rd.hlen('qdArt') == 5:
        return '抢读失败'

    # 将用户id和aid存入到hash中
    # qdArt可以被设计成:活动ID:adArt
    # 优化代码,避免抢多本
    rd.hset('qdArt', uid, aid)

    return '抢读成功'