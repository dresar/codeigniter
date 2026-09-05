# Invitation App - Platform Undangan Pernikahan Digital

Aplikasi Django untuk membuat undangan pernikahan digital yang elegan dan modern.

## Fitur Utama

- ✅ **Sistem Autentikasi**: Registrasi dan login user (terpisah dari Django admin)
- ✅ **Dashboard User**: Manajemen undangan dengan CRUD lengkap
- ✅ **Formulir Undangan Lengkap**: 
  - Detail pasangan (nama mempelai, orang tua, Instagram)
  - Acara Akad & Resepsi (tanggal, waktu, lokasi, Google Maps)
  - Konten (Our Story, Gallery, Save the Date)
  - Wedding Gift (nomor rekening)
  - QR Code untuk check-in
- ✅ **Slug & Dynamic URL**: Setiap undangan memiliki slug unik (contoh: `/wedding/budi-ani`)
- ✅ **Guest Management**: Input nama tamu untuk generate link khusus dengan parameter `?to=NamaTamu`
- ✅ **RSVP System**: Tamu bisa konfirmasi kehadiran
- ✅ **Desain Modern**: Menggunakan Tailwind CSS dengan desain elegan dan mobile-responsive

## Teknologi

- **Backend**: Django 5.2.9
- **Frontend**: Tailwind CSS (via CDN)
- **Database**: SQLite (development)
- **Dependencies**: qrcode, Pillow

## Instalasi

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Create superuser** (optional, untuk Django admin):
```bash
python manage.py createsuperuser
```

4. **Run development server**:
```bash
python manage.py runserver
```

5. **Akses aplikasi**:
   - Home: http://127.0.0.1:8000/
   - Register: http://127.0.0.1:8000/register/
   - Login: http://127.0.0.1:8000/login/
   - Dashboard: http://127.0.0.1:8000/dashboard/
   - Admin: http://127.0.0.1:8000/admin/

## Struktur Aplikasi

```
invitations/
├── models.py          # Invitation, Gallery, RSVP, Guest models
├── views.py           # Auth, Dashboard CRUD, Public views
├── forms.py           # User registration, Invitation, RSVP forms
├── urls.py            # URL patterns
├── admin.py           # Django admin configuration
└── templates/
    ├── base.html                    # Base template dengan Tailwind CSS
    ├── auth/
    │   ├── login.html               # Halaman login
    │   └── register.html            # Halaman registrasi
    ├── dashboard.html               # Dashboard user
    ├── invitation_form.html         # Form create/edit undangan
    ├── invitation_public.html       # Halaman publik undangan (elegant design)
    └── ...                          # Template lainnya
```

## Cara Menggunakan

### 1. Registrasi & Login
- Daftar akun baru di `/register/`
- Login di `/login/`

### 2. Membuat Undangan
- Setelah login, klik "Buat Undangan Baru" di dashboard
- Isi semua informasi:
  - Detail pasangan
  - Acara Akad & Resepsi
  - Konten (Our Story, Save the Date)
  - Wedding Gift (jika ada)
- Simpan dan publish undangan

### 3. Menambah Gallery
- Di halaman edit undangan, klik "Tambah Foto"
- Upload foto dan tambahkan caption (opsional)

### 4. Guest Management
- Di halaman edit undangan, klik "Tambah Guest"
- Input nama tamu untuk generate link khusus
- Link akan otomatis menampilkan nama tamu di halaman undangan

### 5. Melihat Undangan Publik
- Setelah publish, undangan bisa diakses di: `/wedding/{slug}/`
- Contoh: `/wedding/budi-ani/`
- Dengan guest: `/wedding/budi-ani/?to=NamaTamu`

### 6. RSVP
- Tamu bisa mengisi form RSVP di halaman undangan
- Response akan muncul di dashboard user

## Models

### Invitation
- Detail pasangan, acara, konten, wedding gift
- Auto-generate slug dari nama mempelai
- Auto-generate QR code untuk check-in

### Gallery
- Multiple images per undangan
- Support caption dan ordering

### RSVP
- Konfirmasi kehadiran tamu
- Status: attending, not_attending, maybe
- Jumlah tamu dan pesan

### Guest
- Guest management untuk generate link khusus
- Token unik untuk setiap guest

## URL Patterns

- `/` - Home (redirect ke login/dashboard)
- `/register/` - Registrasi user
- `/login/` - Login user
- `/logout/` - Logout
- `/dashboard/` - Dashboard user
- `/invitation/create/` - Buat undangan baru
- `/invitation/{pk}/edit/` - Edit undangan
- `/wedding/{slug}/` - Halaman publik undangan
- `/wedding/{slug}/rsvp/` - Submit RSVP
- `/wedding/{slug}/checkin/` - Check-in via QR code

## Catatan

- QR Code akan otomatis di-generate saat undangan dibuat
- Slug di-generate otomatis dari nama mempelai (format: `groom-bride`)
- Jika slug sudah ada, akan ditambahkan angka di belakang
- Media files (gambar) disimpan di folder `media/`
- Pastikan folder `media/` memiliki permission write

## Development

Untuk development, pastikan:
- Django 5.x terinstall
- SQLite database (default)
- Static files di-serve otomatis di development mode
- Media files di-serve via URL patterns (sudah dikonfigurasi)

## Production

Untuk production:
- Set `DEBUG = False` di `settings.py`
- Konfigurasi `ALLOWED_HOSTS`
- Setup static files collection
- Setup media files storage (S3, dll)
- Gunakan database production (PostgreSQL, MySQL, dll)
- Setup SSL/HTTPS

## License

MIT License

