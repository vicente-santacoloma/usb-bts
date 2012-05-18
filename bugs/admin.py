from bugs.models import Application, Component, Bug, Comment
from django.contrib import admin

class ComponentInline(admin.TabularInline):
    model = Component
    extra = 5

class ApplicationAdmin(admin.ModelAdmin):
    inlines = [ComponentInline]
    search_fields = ['name']
    
class ComponentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
class BugAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'date_reported', 'date_changed')
    search_fields = ['title']
    list_filter = ['date_reported']
    date_hierarchy = 'date_reported'
    
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Application,ApplicationAdmin)
admin.site.register(Component,ComponentAdmin)
admin.site.register(Bug,BugAdmin)
admin.site.register(Comment,CommentAdmin)

