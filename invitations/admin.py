from django.contrib import admin
from .models import Invitation, Gallery, RSVP, Guest


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('groom_name', 'bride_name', 'user', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('groom_name', 'bride_name', 'slug', 'user__username')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'qr_code')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Detail Pasangan', {
            'fields': ('groom_name', 'bride_name', 'parents_text', 'instagram_username')
        }),
        ('Acara Akad', {
            'fields': ('akad_date', 'akad_time', 'akad_location', 'akad_maps_link')
        }),
        ('Acara Resepsi', {
            'fields': ('resepsi_date', 'resepsi_time', 'resepsi_location', 'resepsi_maps_link')
        }),
        ('Konten', {
            'fields': ('our_story', 'save_the_date_image')
        }),
        ('Wedding Gift', {
            'fields': ('gift_account_number', 'gift_account_name', 'gift_bank_name')
        }),
        ('Metadata', {
            'fields': ('slug', 'is_published', 'qr_code', 'created_at', 'updated_at')
        }),
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('invitation', 'caption', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('invitation__groom_name', 'invitation__bride_name', 'caption')


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'invitation', 'status', 'number_of_guests', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('guest_name', 'email', 'phone', 'invitation__groom_name', 'invitation__bride_name')
    readonly_fields = ('submitted_at',)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'invitation', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'invitation__groom_name', 'invitation__bride_name')
    readonly_fields = ('token', 'created_at')
