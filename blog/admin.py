from django.contrib import admin
from .models import Post,Board,Topic
from markdownx.admin import MarkdownxModelAdmin
# from martor.widgets import AdminMartorWidget
# from django.db import models
# martor
# class PostAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': AdminMartorWidget},
#     }
# admin.site.register(Post, PostAdmin)
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Board)
admin.site.register(Topic)




