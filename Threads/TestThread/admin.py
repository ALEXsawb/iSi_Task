from django.contrib import admin

#admin.site.register(Models)
from .models import ThreadModel, MessageModel


class ThreadModelAdmin(admin.ModelAdmin):
    list_display = ('participant1', 'participant2', 'created', 'updated')
    list_display_links = ('participant1', 'participant2')
    search_fields = ('participant1__name', 'participant2__name', 'participant2__pk', 'participant2__pk', 'created',
                     'updated')
    readonly_fields = ('participant1', 'participant2', 'created', 'updated')


class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('sender', 'thread', 'text', 'created', 'is_read')
    list_display_links = ('sender', 'thread')
    search_fields = ('sender', 'thread', 'is_read')
    list_editable = ('is_read', )
    #readonly_fields = ('sender', 'thread', 'created', 'text')


admin.site.register(ThreadModel, ThreadModelAdmin)
admin.site.register(MessageModel, MessageModelAdmin)
