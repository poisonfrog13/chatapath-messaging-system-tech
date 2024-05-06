from django.contrib import admin
from server.apps.chatapath.models import Message

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_filter = ("date", "is_unread")
    list_display = ("subject", "sender", "recipient", "date")


admin.site.register(Message, MessageAdmin)
