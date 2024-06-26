from django.contrib import admin
from chat.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "send_user_id", "receive_user_id", "datetime"]
    list_display_links = ('id', 'send_user_id')


admin.site.register(Message, MessageAdmin)
