from django.contrib import admin, messages
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'moderated', 'title', 'author')
    list_filter = ('moderated', )
    search_fields = ('title', 'author__username')
    actions = ['set_moderate']

    @admin.action(description='Отметить посты как модерированные')
    def set_moderate(self, request, queryset):
        queryset.update(moderated=True)
        messages.success(request, 'Выбранные посты были отмечены, как модерированные')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'moderated', 'text', 'author', 'post')
    list_filter = ('moderated', )
    search_fields = ('id', 'text', 'author__username', 'post__title')
    actions = ['set_moderate']

    @admin.action(description='Отметить комментарии как модерированные')
    def set_moderate(self, request, queryset):
        queryset.update(moderated=True)
        messages.success(request, 'Выбранные комментарии были отмечены, как модерированные')

