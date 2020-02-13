from django.contrib import admin
from django.urls import path
from django.db import models
from .views import adminChatList, adminChatRoom


class chatRoom(models.Model):

    class Meta:
        app_label = 'chat'
        managed = False


class chatAdmin(admin.ModelAdmin):
    model = chatRoom

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)

        urlpatterns = [
            path('', adminChatList, name=view_name),
            path('<str:target>/', adminChatRoom.as_view()),
        ]

        return urlpatterns


admin.site.register(chatRoom, chatAdmin)
