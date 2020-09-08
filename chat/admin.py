from django.contrib import admin
from django.urls import path
from django.db import models
from .views import admin_chat_list, AdminChatRoom


class ChatRoom(models.Model):

    class Meta:
        app_label = 'chat'
        managed = False


class ChatAdmin(admin.ModelAdmin):
    model = ChatRoom

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)

        urlpatterns = [
            path('', admin_chat_list, name=view_name),
            path('<str:target>/', AdminChatRoom.as_view()),
        ]

        return urlpatterns


admin.site.register(ChatRoom, ChatAdmin)
