import xadmin
from apps.message_form.models import Category
from apps.message_form.models import Article
from apps.message_form.models import Comment
from apps.message_form.models import UserProfile

class UserProfileAdmin(object):

    def queryset(self):

        qs = super(UserProfileAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(nick_name = self.request.user.nick_name)
        return qs
    # pass

class CategoryAdmin(object):
    list_display = ['id','name']
    search_fields = ["name"]
    readonly_fields = ["click_nums"]


class ArticleAdmin(object):
    style_fields = {
        "content": "ueditor"
    }
    list_display = ('id','title','author','hidden','publish_data')
    search_fields = ["content"]
    list_filter = ['category']
    readonly_fields = ["category","author","commment_nums","user_like_nums","click_nums"]

    def queryset(self):

        qs = super(ArticleAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(author = self.request.user)
        return qs

class CommentAdmin(object):
    search_fields = ["content"]
    list_filter = ['article']
    readonly_fields = ["article","user"]
    def queryset(self):

        qs = super(CommentAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(user = self.request.user)
        return qs
    pass

class GlobalSettings(object):
    site_title = "陶大科院圈后台管理系统"
    site_footer = "陶大科院圈"


# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Comment,CommentAdmin)
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)