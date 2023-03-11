from django.contrib import admin
from .models import Tutorial, Comment


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'user', 'slug', 'updated', 'score', 'img')
    search_fields = ('slug',)
    # list_filter = ('updated',)
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tut', 'body', 'created', 'is_reply', 'approve', 'reply')
    raw_id_fields = ('user', 'tut', 'reply')
