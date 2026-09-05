# Sistem Template Undangan

## Overview

Sistem template memungkinkan user untuk mengupload template HTML custom untuk undangan pernikahan mereka. Template dapat dilengkapi dengan CSS, JavaScript, dan preview image.

## Struktur File

```
templates/
├── invited/              # Folder untuk HTML template (auto-generated)
│   └── example_template.html
│
invitation_templates/     # Aplikasi Django untuk manage template
├── models.py            # Model InvitationTemplate
├── views.py            # Views untuk CRUD template
├── forms.py            # Form untuk upload template
└── urls.py             # URL patterns

media/
└── templates/
    ├── html/           # HTML files (original upload)
    ├── css/            # CSS files
    ├── js/             # JavaScript files
    └── previews/       # Preview images
```

## Cara Menggunakan

### 1. Upload Template

1. Login ke aplikasi
2. Buka **Template Management** dari dashboard atau langsung ke `/templates/`
3. Klik **Upload Template Baru**
4. Isi form:
   - **Nama Template**: Nama untuk identifikasi
   - **Deskripsi**: Deskripsi template (opsional)
   - **File HTML Template**: File HTML template (required)
   - **File CSS**: File CSS custom (opsional)
   - **File JavaScript**: File JS custom (opsional)
   - **Preview Image**: Gambar preview template (opsional)
   - **Aktifkan template**: Centang untuk mengaktifkan
   - **Jadikan template default**: Centang untuk set sebagai default

### 2. Menggunakan Template di Undangan

1. Saat membuat/edit undangan, pilih template dari dropdown **Pilih Template**
2. Simpan undangan
3. Template akan otomatis digunakan saat undangan diakses

### 3. Format Template HTML

Template HTML harus menggunakan Django template syntax dengan context variables berikut:

#### Context Variables

- `invitation` - Object Invitation dengan fields:
  - `groom_name` - Nama mempelai pria
  - `bride_name` - Nama mempelai wanita
  - `parents_text` - Text nama orang tua
  - `instagram_username` - Username Instagram
  - `akad_date`, `akad_time`, `akad_location`, `akad_maps_link`
  - `resepsi_date`, `resepsi_time`, `resepsi_location`, `resepsi_maps_link`
  - `our_story` - Cerita pasangan
  - `save_the_date_image` - Image save the date
  - `gift_account_number`, `gift_account_name`, `gift_bank_name`
  - `qr_code` - QR code image
  - `slug` - Slug URL

- `galleries` - QuerySet dari Gallery objects
  - `image` - Image field
  - `caption` - Caption foto
  - `order` - Urutan

- `rsvp_form` - Form untuk RSVP
- `guest_name` - Nama tamu dari query parameter `?to=NamaTamu`

#### Template Variables untuk CSS/JS

- `template_css` - URL untuk CSS file (jika ada)
- `template_js` - URL untuk JavaScript file (jika ada)

### 4. Contoh Template HTML

Lihat file `templates/invited/example_template.html` untuk contoh template yang lengkap.

#### Contoh Sederhana:

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ invitation.groom_name }} & {{ invitation.bride_name }}</title>
    
    {% if template_css %}
    <link rel="stylesheet" href="{{ template_css }}">
    {% else %}
    <script src="https://cdn.tailwindcss.com"></script>
    {% endif %}
</head>
<body>
    <h1>{{ invitation.groom_name }} & {{ invitation.bride_name }}</h1>
    <p>{{ invitation.parents_text }}</p>
    
    <h2>Akad Nikah</h2>
    <p>{{ invitation.akad_date|date:"d F Y" }}</p>
    <p>{{ invitation.akad_time|time:"H:i" }} WIB</p>
    <p>{{ invitation.akad_location }}</p>
    
    {% if invitation.akad_maps_link %}
    <a href="{{ invitation.akad_maps_link }}">Google Maps</a>
    {% endif %}
    
    <!-- RSVP Form -->
    <form method="post" action="{% url 'invitations:rsvp_submit' invitation.slug %}">
        {% csrf_token %}
        {{ rsvp_form.guest_name }}
        {{ rsvp_form.status }}
        <button type="submit">Kirim RSVP</button>
    </form>
    
    {% if template_js %}
    <script src="{{ template_js }}"></script>
    {% endif %}
</body>
</html>
```

### 5. CSS dan JavaScript

#### CSS File

- Upload file CSS melalui form
- File akan disimpan di `media/templates/css/`
- Akses di template dengan variable `{{ template_css }}`
- Contoh: `<link rel="stylesheet" href="{{ template_css }}">`

#### JavaScript File

- Upload file JS melalui form
- File akan disimpan di `media/templates/js/`
- Akses di template dengan variable `{{ template_js }}`
- Contoh: `<script src="{{ template_js }}"></script>`

### 6. Preview Image

- Upload gambar preview untuk template
- Akan ditampilkan di list template
- Format: JPG, PNG, dll
- Recommended size: 800x600px

## API Endpoints

- `GET /templates/` - List semua template
- `GET /templates/create/` - Form upload template baru
- `POST /templates/create/` - Submit template baru
- `GET /templates/<id>/edit/` - Form edit template
- `POST /templates/<id>/edit/` - Update template
- `GET /templates/<id>/delete/` - Konfirmasi hapus
- `POST /templates/<id>/delete/` - Hapus template
- `GET /templates/<id>/preview/` - Preview template

## Model Fields

### InvitationTemplate

- `name` - Nama template
- `slug` - Slug URL (auto-generated)
- `description` - Deskripsi template
- `html_file` - File HTML template
- `css_file` - File CSS (optional)
- `js_file` - File JavaScript (optional)
- `preview_image` - Preview image (optional)
- `created_by` - User yang membuat template
- `is_active` - Status aktif
- `is_default` - Template default
- `created_at`, `updated_at` - Timestamps

## Tips

1. **Template HTML harus lengkap** - Include DOCTYPE, html, head, body tags
2. **Gunakan Django template filters** - Untuk format date, time, dll
3. **Mobile responsive** - Pastikan template responsive untuk mobile
4. **Test template** - Gunakan preview untuk test template sebelum publish
5. **Backup template** - Simpan backup template HTML sebelum upload
6. **CSS/JS naming** - Gunakan nama file yang unik untuk avoid conflicts

## Troubleshooting

### Template tidak muncul
- Pastikan template sudah diaktifkan (`is_active=True`)
- Pastikan file HTML sudah terupload dengan benar
- Cek console untuk error messages

### CSS/JS tidak load
- Pastikan file sudah terupload
- Cek URL di browser console
- Pastikan `STATIC_URL` dan `MEDIA_URL` sudah dikonfigurasi

### Template error
- Cek syntax Django template
- Pastikan semua context variables digunakan dengan benar
- Cek file `templates/invited/` apakah file HTML sudah ada

## Security Notes

- Hanya creator atau superuser yang bisa edit/hapus template
- File upload dibatasi ke format tertentu (HTML, CSS, JS, Images)
- Template HTML akan di-render oleh Django, pastikan tidak ada malicious code

