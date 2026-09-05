from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

try:
    import qrcode
    from PIL import Image
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False


class Invitation(models.Model):
    """Model untuk undangan pernikahan"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    
    # Template
    template = models.ForeignKey('invitation_templates.InvitationTemplate', 
                                on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='invitations', verbose_name="Template")
    
    # Detail Pasangan
    groom_name = models.CharField(max_length=200, verbose_name="Nama Mempelai Pria")
    bride_name = models.CharField(max_length=200, verbose_name="Nama Mempelai Wanita")
    parents_text = models.TextField(verbose_name="Nama Orang Tua (Custom Text)", 
                                    help_text="Contoh: Putra dari Bapak... dan Ibu...")
    instagram_username = models.CharField(max_length=100, blank=True, 
                                         verbose_name="Username Instagram")
    
    # Acara - Akad
    akad_date = models.DateField(verbose_name="Tanggal Akad")
    akad_time = models.TimeField(verbose_name="Waktu Akad")
    akad_location = models.CharField(max_length=500, verbose_name="Lokasi Akad")
    akad_maps_link = models.URLField(blank=True, verbose_name="Google Maps Link Akad")
    
    # Acara - Resepsi
    resepsi_date = models.DateField(verbose_name="Tanggal Resepsi")
    resepsi_time = models.TimeField(verbose_name="Waktu Resepsi")
    resepsi_location = models.CharField(max_length=500, verbose_name="Lokasi Resepsi")
    resepsi_maps_link = models.URLField(blank=True, verbose_name="Google Maps Link Resepsi")
    
    # Konten
    our_story = models.TextField(blank=True, verbose_name="Our Story")
    save_the_date_image = models.ImageField(upload_to='save_the_date/', blank=True, 
                                           verbose_name="Save the Date Image")
    
    # Wedding Gift
    gift_account_number = models.CharField(max_length=50, blank=True, 
                                          verbose_name="Nomor Rekening")
    gift_account_name = models.CharField(max_length=200, blank=True, 
                                        verbose_name="Nama Pemilik Rekening")
    gift_bank_name = models.CharField(max_length=100, blank=True, 
                                     verbose_name="Nama Bank")
    
    # Slug & Metadata
    slug = models.SlugField(max_length=255, unique=True, blank=True, 
                           verbose_name="Slug URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="Published")
    
    # QR Code untuk Check-in
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, 
                               verbose_name="QR Code Check-in")
    
    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.groom_name} & {self.bride_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug dari nama mempelai
            base_slug = slugify(f"{self.groom_name}-{self.bride_name}")
            slug = base_slug
            counter = 1
            while Invitation.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Generate QR Code jika belum ada
        if not self.qr_code:
            self.generate_qr_code()
        
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        """Generate QR Code untuk check-in"""
        if not QRCODE_AVAILABLE:
            return
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # URL untuk check-in
            checkin_url = f"https://invit.me/wedding/{self.slug}/checkin"
            qr.add_data(checkin_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            self.qr_code.save(
                f'qr_{self.slug}.png',
                ContentFile(buffer.read()),
                save=False
            )
        except Exception:
            # Jika gagal generate QR code, skip
            pass
    
    def get_absolute_url(self):
        return reverse('invitation_detail', kwargs={'slug': self.slug})


class Gallery(models.Model):
    """Model untuk gallery foto undangan"""
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, 
                                  related_name='galleries')
    image = models.ImageField(upload_to='gallery/', verbose_name="Foto")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    order = models.IntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Gallery - {self.invitation}"


class RSVP(models.Model):
    """Model untuk RSVP tamu"""
    STATUS_CHOICES = [
        ('attending', 'Akan Hadir'),
        ('not_attending', 'Tidak Bisa Hadir'),
        ('maybe', 'Mungkin Hadir'),
    ]
    
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, 
                                  related_name='rsvps')
    guest_name = models.CharField(max_length=200, verbose_name="Nama Tamu")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="No. Telepon")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='attending', verbose_name="Status Kehadiran")
    message = models.TextField(blank=True, verbose_name="Pesan/Ucapan")
    number_of_guests = models.IntegerField(default=1, verbose_name="Jumlah Tamu")
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"RSVP - {self.guest_name} ({self.status})"


class Guest(models.Model):
    """Model untuk guest management - generate link khusus"""
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, 
                                  related_name='guests')
    name = models.CharField(max_length=200, verbose_name="Nama Tamu")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="No. Telepon")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.invitation}"
    
    def get_guest_url(self):
        """Generate URL khusus untuk tamu"""
        return f"/wedding/{self.invitation.slug}?to={self.name}"
