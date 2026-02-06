from django.contrib import admin
from .models import Level, Subject, SubjectResource, StudentNote

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_id', 'title')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'semester')
    list_filter = ('level', 'semester')
    search_fields = ('name',)



@admin.register(SubjectResource)
class SubjectResourceAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category', 'download_url', 'upload_date')
    list_filter = ('category', 'subject__level')
    search_fields = ('subject__name',)

@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('title', 'content', 'user__username')
