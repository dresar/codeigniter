from django import forms
from .models import InvitationTemplate


class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget untuk multiple file upload"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Custom field untuk multiple file upload"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class InvitationTemplateForm(forms.ModelForm):
    """Form untuk upload/edit template"""
    # File upload fields (tidak disimpan di model, hanya untuk processing)
    html_file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'accept': '.html'
        }),
        help_text="File HTML akan disimpan di templates/invited/"
    )
    
    # Multiple file fields
    css_files = MultipleFileField(
        required=False,
        help_text="Pilih satu atau lebih file CSS (akan di-rename menjadi style1.css, style2.css, dll)"
    )
    
    js_files = MultipleFileField(
        required=False,
        help_text="Pilih satu atau lebih file JavaScript (akan di-rename menjadi script1.js, script2.js, dll)"
    )
    
    image_files = MultipleFileField(
        required=False,
        help_text="Pilih satu atau lebih file image"
    )
    
    class Meta:
        model = InvitationTemplate
        fields = ['name', 'description', 'html_filename', 'preview_image', 'is_active', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3
            }),
            'html_filename': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'readonly': True
            }),
            'preview_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set multiple attribute untuk file inputs
        self.fields['css_files'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'accept': '.css',
            'multiple': True
        })
        self.fields['js_files'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'accept': '.js',
            'multiple': True
        })
        self.fields['image_files'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'accept': 'image/*',
            'multiple': True
        })
        
        # Jika edit, set html_filename dari instance
        if self.instance and self.instance.pk:
            self.fields['html_file'].required = False
            self.fields['html_file'].help_text = "Kosongkan jika tidak ingin mengubah file HTML"
