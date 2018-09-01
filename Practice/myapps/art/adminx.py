import xadmin as admin
from xadmin import views
from art.models import Tag, Art

# Register your models here.
class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 整体配置
    site_title = '美文后台管理系统'
    site_footer = '千锋教育python项目'
    menu_style = 'accordion'  # 菜单折叠
    # 搜索模型
    global_search_models = [Tag, Art]

    # 模型的图标(参考bootstrap图标插件)
    global_models_icon = {
        Art: "glyphicon glyphicon-book",
        Tag: "fa fa-cloud"
    }  # 设置models的全局图标


class TagAdmin:
    list_display = ['name', 'add_time']
    search_fields = ['name']

class ArtAdmin:
    list_display = ['title', 'author', 'summary', 'publish_date']
    search_fields = ['title', 'author']
    style_fields = {
        'content': 'ueditor'    # 设置content字段的样式
    }


admin.site.register(views.CommAdminView, GlobalSettings)
admin.site.register(views.BaseAdminView, BaseSetting)
admin.site.register(Tag, TagAdmin)
admin.site.register(Art, ArtAdmin)
