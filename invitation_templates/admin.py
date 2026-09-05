from django.contrib import admin
from .models import InvitationTemplate, TemplateCSS, TemplateJS, TemplateImage


class TemplateCSSInline(admin.TabularInline):
    model = TemplateCSS
    extra = 0


class TemplateJSInline(admin.TabularInline):
    model = TemplateJS
    extra = 0


class TemplateImageInline(admin.TabularInline):
    model = TemplateImage
    extra = 0


@admin.register(InvitationTemplate)
class InvitationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'is_default', 'created_by', 'created_at')
    list_filter = ('is_active', 'is_default', 'created_at')
    search_fields = ('name', 'description', 'slug')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    inlines = [TemplateCSSInline, TemplateJSInline, TemplateImageInline]
    fieldsets = (
        ('Informasi Template', {
            'fields': ('name', 'slug', 'description', 'created_by')
        }),
        ('File Template', {
            'fields': ('html_filename', 'preview_image')
        }),
        ('Status', {
            'fields': ('is_active', 'is_default')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(TemplateCSS)
class TemplateCSSAdmin(admin.ModelAdmin):
    list_display = ('template', 'filename', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('template__name', 'filename')


@admin.register(TemplateJS)
class TemplateJSAdmin(admin.ModelAdmin):
    list_display = ('template', 'filename', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('template__name', 'filename')


@admin.register(TemplateImage)
class TemplateImageAdmin(admin.ModelAdmin):
    list_display = ('template', 'image', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('template__name',)
