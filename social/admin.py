from social.models import Message
from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    search_fields = ['content']
    list_display = ('content','date_sent')
    list_filter = ['date_sent']
    date_hierarchy = 'date_sent'

admin.site.register(Message,MessageAdmin)