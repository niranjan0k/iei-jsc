from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CarouselImage, Announcement, Event, EventPhoto,
    Download, Member, LeaderProfile, ContactMessage
)


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1
    max_num = 10
    fields = ['image', 'caption']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '-'
    preview.short_description = 'Preview'


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'sort_order', 'preview', 'created_at']
    list_editable = ['sort_order']
    ordering = ['sort_order']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '-'
    preview.short_description = 'Preview'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'link', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'content']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_date', 'photo_count', 'created_at']
    search_fields = ['name', 'description']
    inlines = [EventPhotoInline]
    date_hierarchy = 'event_date'

    def photo_count(self, obj):
        count = obj.photos.count()
        return format_html('<span style="color:#1a3a6e;font-weight:bold">{} photos</span>', count)
    photo_count.short_description = 'Photos'


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['name', 'file_type', 'file', 'created_at']
    search_fields = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'category', 'sort_order']
    list_editable = ['sort_order']
    list_filter = ['category']
    search_fields = ['name', 'designation']


@admin.register(LeaderProfile)
class LeaderProfileAdmin(admin.ModelAdmin):
    list_display = ['role', 'name', 'title']

    def has_add_permission(self, request):
        if LeaderProfile.objects.count() >= 2:
            return False
        return super().has_add_permission(request)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'received_at', 'is_read']
    list_filter = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'received_at']
    list_editable = ['is_read']

    def has_add_permission(self, request):
        return False
