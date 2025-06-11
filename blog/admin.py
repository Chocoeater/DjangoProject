from django.contrib import admin

from blog.models import BlogRecord

# Register your models here.


@admin.register(BlogRecord)
class BlogRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "preview", "publication")
    search_fields = ("title", "content")
