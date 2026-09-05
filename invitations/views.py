from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Invitation, Gallery, RSVP, Guest
from .forms import (
    UserRegistrationForm, InvitationForm, GalleryForm, 
    RSVPForm, GuestForm
)


def home_view(request):
    """Home page - redirect to dashboard if logged in, else to login"""
    if request.user.is_authenticated:
        return redirect('invitations:dashboard')
    return redirect('invitations:login')


def register_view(request):
    """View untuk registrasi user baru"""
    if request.user.is_authenticated:
        return redirect('invitations:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Selamat datang.')
            return redirect('invitations:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'invitations/auth/register.html', {'form': form})


def login_view(request):
    """View untuk login user"""
    if request.user.is_authenticated:
        return redirect('invitations:dashboard')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.get_full_name() or user.username}!')
            return redirect('invitations:dashboard')
        else:
            messages.error(request, 'Username atau password salah.')
    
    return render(request, 'invitations/auth/login.html')


def logout_view(request):
    """View untuk logout"""
    logout(request)
    messages.info(request, 'Anda telah logout.')
    return redirect('invitations:login')


@login_required
def dashboard(request):
    """Dashboard utama user - list semua undangan"""
    invitations = Invitation.objects.filter(user=request.user)
    return render(request, 'invitations/dashboard.html', {
        'invitations': invitations
    })


@login_required
def invitation_create(request):
    """View untuk membuat undangan baru"""
    if request.method == 'POST':
        form = InvitationForm(request.POST, request.FILES)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.user = request.user
            invitation.save()
            messages.success(request, 'Undangan berhasil dibuat!')
            return redirect('invitations:invitation_detail_edit', pk=invitation.pk)
    else:
        form = InvitationForm()
    
    return render(request, 'invitations/invitation_form.html', {
        'form': form,
        'title': 'Buat Undangan Baru'
    })


@login_required
def invitation_edit(request, pk):
    """View untuk edit undangan"""
    invitation = get_object_or_404(Invitation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = InvitationForm(request.POST, request.FILES, instance=invitation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Undangan berhasil diperbarui!')
            return redirect('invitations:invitation_detail_edit', pk=invitation.pk)
    else:
        form = InvitationForm(instance=invitation)
    
    galleries = invitation.galleries.all()
    guests = invitation.guests.all()
    rsvps = invitation.rsvps.all()
    
    return render(request, 'invitations/invitation_form.html', {
        'form': form,
        'invitation': invitation,
        'galleries': galleries,
        'guests': guests,
        'rsvps': rsvps,
        'title': 'Edit Undangan'
    })


@login_required
def invitation_delete(request, pk):
    """View untuk hapus undangan"""
    invitation = get_object_or_404(Invitation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        invitation.delete()
        messages.success(request, 'Undangan berhasil dihapus!')
        return redirect('invitations:dashboard')
    
    return render(request, 'invitations/invitation_confirm_delete.html', {
        'invitation': invitation
    })


@login_required
def gallery_add(request, invitation_pk):
    """View untuk menambah foto gallery"""
    invitation = get_object_or_404(Invitation, pk=invitation_pk, user=request.user)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.invitation = invitation
            gallery.save()
            messages.success(request, 'Foto berhasil ditambahkan!')
            return redirect('invitations:invitation_detail_edit', pk=invitation.pk)
    else:
        form = GalleryForm()
    
    return render(request, 'invitations/gallery_form.html', {
        'form': form,
        'invitation': invitation
    })


@login_required
def gallery_delete(request, pk):
    """View untuk hapus foto gallery"""
    gallery = get_object_or_404(Gallery, pk=pk)
    invitation = gallery.invitation
    
    if gallery.invitation.user != request.user:
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('invitations:dashboard')
    
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'Foto berhasil dihapus!')
        return redirect('invitations:invitation_detail_edit', pk=invitation.pk)
    
    return render(request, 'invitations/gallery_confirm_delete.html', {
        'gallery': gallery
    })


@login_required
def guest_add(request, invitation_pk):
    """View untuk menambah guest"""
    invitation = get_object_or_404(Invitation, pk=invitation_pk, user=request.user)
    
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.invitation = invitation
            guest.save()
            messages.success(request, f'Guest "{guest.name}" berhasil ditambahkan!')
            return redirect('invitations:invitation_detail_edit', pk=invitation.pk)
    else:
        form = GuestForm()
    
    return render(request, 'invitations/guest_form.html', {
        'form': form,
        'invitation': invitation
    })


@login_required
def guest_delete(request, pk):
    """View untuk hapus guest"""
    guest = get_object_or_404(Guest, pk=pk)
    invitation = guest.invitation
    
    if guest.invitation.user != request.user:
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('invitations:dashboard')
    
    if request.method == 'POST':
        guest.delete()
        messages.success(request, 'Guest berhasil dihapus!')
        return redirect('invitations:invitation_detail_edit', pk=invitation.pk)
    
    return render(request, 'invitations/guest_confirm_delete.html', {
        'guest': guest
    })


def invitation_public(request, slug):
    """View untuk halaman publik undangan"""
    invitation = get_object_or_404(Invitation, slug=slug, is_published=True)
    
    # Ambil nama tamu dari query parameter
    guest_name = request.GET.get('to', '')
    
    # Ambil galleries
    galleries = invitation.galleries.all()
    
    # Ambil RSVP form
    rsvp_form = RSVPForm()
    
    # Jika ada guest_name, set sebagai default di form
    if guest_name:
        rsvp_form.fields['guest_name'].initial = guest_name
    
    context = {
        'invitation': invitation,
        'galleries': galleries,
        'rsvp_form': rsvp_form,
        'guest_name': guest_name,
    }
    
    # Jika ada template yang dipilih, gunakan template tersebut
    if invitation.template and invitation.template.is_active:
        template_path = invitation.template.get_html_template_path()
        if template_path:
            try:
                # Tambahkan CSS dan JS files dari template
                context['template_css_files'] = invitation.template.get_css_files()
                context['template_js_files'] = invitation.template.get_js_files()
                context['template_images'] = invitation.template.get_images()
                context['template_slug'] = invitation.template.slug
                return render(request, template_path, context)
            except Exception as e:
                # Jika template tidak ditemukan, fallback ke default
                import traceback
                print(f"Template error: {e}")
                traceback.print_exc()
                pass
    
    # Default template
    return render(request, 'invitations/invitation_public.html', context)


@require_POST
def rsvp_submit(request, slug):
    """View untuk submit RSVP"""
    invitation = get_object_or_404(Invitation, slug=slug, is_published=True)
    
    form = RSVPForm(request.POST)
    if form.is_valid():
        rsvp = form.save(commit=False)
        rsvp.invitation = invitation
        rsvp.save()
        messages.success(request, 'Terima kasih! RSVP Anda telah terkirim.')
        return redirect('invitations:invitation_detail', slug=slug)
    else:
        messages.error(request, 'Terjadi kesalahan. Silakan coba lagi.')
        return redirect('invitations:invitation_detail', slug=slug)


def checkin_view(request, slug):
    """View untuk check-in menggunakan QR Code"""
    invitation = get_object_or_404(Invitation, slug=slug, is_published=True)
    
    # Simpan check-in (bisa ditambahkan model CheckIn jika diperlukan)
    messages.success(request, f'Check-in berhasil untuk {invitation.groom_name} & {invitation.bride_name}!')
    
    return redirect('invitations:invitation_detail', slug=slug)
