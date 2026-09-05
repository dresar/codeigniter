from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
from django.core.files.storage import default_storage


class InvitationTemplate(models.Model):
    """Model untuk menyimpan template undangan"""
    name = models.CharField(max_length=200, verbose_name="Nama Template")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    
    # File template HTML (hanya filename, disimpan di templates/invited/)
    html_filename = models.CharField(max_length=255, blank=True, default='', verbose_name="File HTML Template")
    
    # Preview image (hanya di media)
    preview_image = models.ImageField(upload_to='templates/previews/', blank=True, null=True, 
                                     verbose_name="Preview Image")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='created_templates')
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_default = models.BooleanField(default=False, verbose_name="Template Default")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Invitation Template"
        verbose_name_plural = "Invitation Templates"
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while InvitationTemplate.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Jika ini adalah default, pastikan hanya satu default
        if self.is_default:
            InvitationTemplate.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        
        super().save(*args, **kwargs)
    
    def get_html_template_path(self):
        """Return path untuk template HTML"""
        if self.html_filename:
            return f'invited/{self.html_filename}'
        return None
    
    def get_css_files(self):
        """Return semua CSS files untuk template ini"""
        return self.css_files.all().order_by('order')
    
    def get_js_files(self):
        """Return semua JS files untuk template ini"""
        return self.js_files.all().order_by('order')
    
    def get_images(self):
        """Return semua image files untuk template ini"""
        return self.images.all().order_by('order')


class TemplateCSS(models.Model):
    """Model untuk CSS files template - hanya menyimpan path, file di static/templates/css/"""
    template = models.ForeignKey(InvitationTemplate, on_delete=models.CASCADE, related_name='css_files')
    filename = models.CharField(max_length=255, blank=True, default='', verbose_name="Nama File CSS")  # style1.css, style2.css, dll
    order = models.IntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Template CSS"
        verbose_name_plural = "Template CSS Files"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.template.name} - CSS {self.order}"
    
    def get_static_path(self):
        """Return path untuk static file"""
        return f"templates/css/{self.template.slug}/{self.filename}"
    
    def get_filename(self):
        """Return hanya nama file"""
        return self.filename


class TemplateJS(models.Model):
    """Model untuk JavaScript files template - hanya menyimpan path, file di static/templates/js/"""
    template = models.ForeignKey(InvitationTemplate, on_delete=models.CASCADE, related_name='js_files')
    filename = models.CharField(max_length=255, blank=True, default='', verbose_name="Nama File JS")  # script1.js, script2.js, dll
    order = models.IntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Template JS"
        verbose_name_plural = "Template JS Files"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.template.name} - JS {self.order}"
    
    def get_static_path(self):
        """Return path untuk static file"""
        return f"templates/js/{self.template.slug}/{self.filename}"
    
    def get_filename(self):
        """Return hanya nama file"""
        return self.filename


class TemplateImage(models.Model):
    """Model untuk image files template - disimpan di media/templates/images/"""
    template = models.ForeignKey(InvitationTemplate, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='templates/images/', verbose_name="Image")
    order = models.IntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Template Image"
        verbose_name_plural = "Template Images"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.template.name} - Image {self.order}"
