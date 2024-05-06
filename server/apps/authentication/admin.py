from django.contrib import admin
from server.apps.authentication.models import ChatUser


# Register your models here.
class ChatUserAdmin(admin.ModelAdmin):
    list_filter = ("date_joined",)
    list_display = (
        "username",
        "phone_number",
        "email",
    )


admin.site.register(ChatUser, ChatUserAdmin)
