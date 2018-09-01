from redis import Redis

# 创建Redis对象
rd = Redis('127.0.0.1', db=12)

# 自增id的阅读排行
def incrTopRank(id):
    rd.zincrby('ReadTopRank', id)

# 获得排名前top的文章
def getReadTopRank(top):
    # 返回元祖对象
    topRanks = rd.zrevrange('ReadTopRank', 0, top-1, withscores=True)

    try:
        from art.models import Art
    # topArts_ = Art.objects.in_bulk([int(id_.decode()) for id_, _ in topRanks])
    # return [(topArts_.get(int(id_.decode())), score) for id_, score in topRanks]
        return [(Art.objects.get(pk=id_.decode()), int(score)) for id_, score in topRanks]
    except:
        pass

