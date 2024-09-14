from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'parent', 'created_time', 'is_enable']
    list_display_links = ['title']
    list_editable = ['is_enable']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']
    date_hierarchy = 'created_time'


class FileInLineAdmin(admin.StackedInline):
    model = File
    fields = ['title','file_type', 'file', 'is_enable']
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'is_enable']
    list_display_links = ['title']
    list_editable = ['is_enable']
    list_filter = ['is_enable']
    filter_horizontal = ['categories']
    search_fields = ['title']
    date_hierarchy = 'created_time'
    inlines = [FileInLineAdmin]
