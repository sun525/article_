from rest_framework import serializers, viewsets
from art.models import Tag

# 声明Tag(ORM)模型对象的序列化(将对象转成某种格式(dict))
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'add_time')

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer