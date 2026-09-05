from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os
import shutil
from .models import InvitationTemplate, TemplateCSS, TemplateJS, TemplateImage
from .forms import InvitationTemplateForm


@login_required
def template_list(request):
    """List semua template"""
    templates = InvitationTemplate.objects.filter(is_active=True)
    return render(request, 'invitation_templates/template_list.html', {
        'templates': templates
    })


@login_required
def template_create(request):
    """Upload template baru"""
    if request.method == 'POST':
        form = InvitationTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            # Process HTML file first - save ke templates/invited/
            html_file = request.FILES.get('html_file')
            if not html_file:
                form.add_error('html_file', 'File HTML wajib diisi')
                return render(request, 'invitation_templates/template_form.html', {
                    'form': form,
                    'title': 'Upload Template Baru'
                })
            
            html_filename = html_file.name
            html_content = html_file.read()
            
            # Save HTML ke templates/invited/ (TIDAK ke media)
            invited_dir = os.path.join(settings.BASE_DIR, 'templates', 'invited')
            os.makedirs(invited_dir, exist_ok=True)
            invited_path = os.path.join(invited_dir, html_filename)
            with open(invited_path, 'wb') as f:
                f.write(html_content)
            
            # Save template dengan html_filename
            template = form.save(commit=False)
            template.html_filename = html_filename
            template.created_by = request.user
            template.save()
            
            # Process multiple CSS files - save ke static/templates/css/ (TIDAK ke media)
            css_files = request.FILES.getlist('css_files')
            for css_file in css_files:
                existing_count = TemplateCSS.objects.filter(template=template).count()
                new_filename = f"style{existing_count + 1}.css"
                
                # Read file content
                css_content = css_file.read()
                
                # Save ke static/templates/css/ (TIDAK ke media)
                static_css_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'css', template.slug)
                os.makedirs(static_css_dir, exist_ok=True)
                static_css_path = os.path.join(static_css_dir, new_filename)
                with open(static_css_path, 'wb') as f:
                    f.write(css_content)
                
                # Simpan hanya filename di database
                TemplateCSS.objects.create(
                    template=template,
                    filename=new_filename,
                    order=existing_count + 1
                )
            
            # Process multiple JS files - save ke static/templates/js/ (TIDAK ke media)
            js_files = request.FILES.getlist('js_files')
            for js_file in js_files:
                existing_count = TemplateJS.objects.filter(template=template).count()
                new_filename = f"script{existing_count + 1}.js"
                
                # Read file content
                js_content = js_file.read()
                
                # Save ke static/templates/js/ (TIDAK ke media)
                static_js_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'js', template.slug)
                os.makedirs(static_js_dir, exist_ok=True)
                static_js_path = os.path.join(static_js_dir, new_filename)
                with open(static_js_path, 'wb') as f:
                    f.write(js_content)
                
                # Simpan hanya filename di database
                TemplateJS.objects.create(
                    template=template,
                    filename=new_filename,
                    order=existing_count + 1
                )
            
            # Process multiple image files - save ke media/templates/images/ (HANYA images di media)
            image_files = request.FILES.getlist('image_files')
            for image_file in image_files:
                existing_count = TemplateImage.objects.filter(template=template).count()
                
                # Save image ke media (ini benar, images tetap di media)
                image_instance = TemplateImage(template=template, order=existing_count + 1)
                image_instance.image.save(
                    f'templates/images/{template.slug}/{image_file.name}',
                    image_file,
                    save=True
                )
            
            messages.success(request, 'Template berhasil diupload!')
            return redirect('invitation_templates:template_list')
    else:
        form = InvitationTemplateForm()
    
    return render(request, 'invitation_templates/template_form.html', {
        'form': form,
        'title': 'Upload Template Baru'
    })


@login_required
def template_edit(request, pk):
    """Edit template"""
    template = get_object_or_404(InvitationTemplate, pk=pk)
    
    # Hanya creator atau superuser yang bisa edit
    if template.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Anda tidak memiliki akses untuk mengedit template ini.')
        return redirect('invitation_templates:template_list')
    
    if request.method == 'POST':
        form = InvitationTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            
            # Jika HTML file diupdate, save ke templates/invited/
            if 'html_file' in request.FILES:
                html_file = request.FILES['html_file']
                html_filename = html_file.name
                html_content = html_file.read()
                
                # Save HTML ke templates/invited/ (TIDAK ke media)
                invited_dir = os.path.join(settings.BASE_DIR, 'templates', 'invited')
                os.makedirs(invited_dir, exist_ok=True)
                invited_path = os.path.join(invited_dir, html_filename)
                with open(invited_path, 'wb') as f:
                    f.write(html_content)
                
                template.html_filename = html_filename
            else:
                # Jika tidak diupdate, tetap gunakan filename yang ada
                template.html_filename = template.html_filename or form.cleaned_data.get('html_filename', '')
            
            template.save()
            
            # Process additional CSS files - save ke static/templates/css/
            css_files = request.FILES.getlist('css_files')
            for css_file in css_files:
                existing_count = TemplateCSS.objects.filter(template=template).count()
                new_filename = f"style{existing_count + 1}.css"
                
                # Read file content
                css_content = css_file.read()
                
                # Save ke static/templates/css/ (TIDAK ke media)
                static_css_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'css', template.slug)
                os.makedirs(static_css_dir, exist_ok=True)
                static_css_path = os.path.join(static_css_dir, new_filename)
                with open(static_css_path, 'wb') as f:
                    f.write(css_content)
                
                # Simpan hanya filename di database
                TemplateCSS.objects.create(
                    template=template,
                    filename=new_filename,
                    order=existing_count + 1
                )
            
            # Process additional JS files - save ke static/templates/js/
            js_files = request.FILES.getlist('js_files')
            for js_file in js_files:
                existing_count = TemplateJS.objects.filter(template=template).count()
                new_filename = f"script{existing_count + 1}.js"
                
                # Read file content
                js_content = js_file.read()
                
                # Save ke static/templates/js/ (TIDAK ke media)
                static_js_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'js', template.slug)
                os.makedirs(static_js_dir, exist_ok=True)
                static_js_path = os.path.join(static_js_dir, new_filename)
                with open(static_js_path, 'wb') as f:
                    f.write(js_content)
                
                # Simpan hanya filename di database
                TemplateJS.objects.create(
                    template=template,
                    filename=new_filename,
                    order=existing_count + 1
                )
            
            # Process additional image files - save ke media/templates/images/
            image_files = request.FILES.getlist('image_files')
            for image_file in image_files:
                existing_count = TemplateImage.objects.filter(template=template).count()
                
                # Save image ke media (ini benar, images tetap di media)
                image_instance = TemplateImage(template=template, order=existing_count + 1)
                image_instance.image.save(
                    f'templates/images/{template.slug}/{image_file.name}',
                    image_file,
                    save=True
                )
            
            messages.success(request, 'Template berhasil diperbarui!')
            return redirect('invitation_templates:template_list')
    else:
        form = InvitationTemplateForm(instance=template)
        # Set initial html_filename untuk form
        if template.html_filename:
            form.fields['html_filename'].initial = template.html_filename
    
    css_files = template.get_css_files()
    js_files = template.get_js_files()
    images = template.get_images()
    
    return render(request, 'invitation_templates/template_form.html', {
        'form': form,
        'template': template,
        'css_files': css_files,
        'js_files': js_files,
        'images': images,
        'title': 'Edit Template'
    })


@login_required
def template_delete(request, pk):
    """Hapus template dan semua file terkait"""
    template = get_object_or_404(InvitationTemplate, pk=pk)
    
    # Hanya creator atau superuser yang bisa hapus
    if template.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Anda tidak memiliki akses untuk menghapus template ini.')
        return redirect('invitation_templates:template_list')
    
    if request.method == 'POST':
        try:
            # Hapus semua CSS files dari static/templates/css/template-slug/
            css_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'css', template.slug)
            if os.path.exists(css_dir) and os.path.isdir(css_dir):
                try:
                    # Hapus semua file di dalam folder dulu
                    for css in template.get_css_files():
                        if css.filename:
                            css_path = os.path.join(css_dir, css.filename)
                            if os.path.exists(css_path) and os.path.isfile(css_path):
                                try:
                                    os.remove(css_path)
                                except (PermissionError, OSError) as e:
                                    print(f"Error deleting CSS file {css_path}: {e}")
                    # Hapus folder jika sudah kosong
                    try:
                        if os.path.exists(css_dir) and not os.listdir(css_dir):
                            os.rmdir(css_dir)
                        elif os.path.exists(css_dir):
                            # Jika masih ada file lain, hapus dengan shutil
                            shutil.rmtree(css_dir)
                    except (PermissionError, OSError):
                        pass
                except Exception as e:
                    print(f"Error deleting CSS directory {css_dir}: {e}")
            
            # Hapus semua JS files dari static/templates/js/template-slug/
            js_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'js', template.slug)
            if os.path.exists(js_dir) and os.path.isdir(js_dir):
                try:
                    # Hapus semua file di dalam folder dulu
                    for js in template.get_js_files():
                        if js.filename:
                            js_path = os.path.join(js_dir, js.filename)
                            if os.path.exists(js_path) and os.path.isfile(js_path):
                                try:
                                    os.remove(js_path)
                                except (PermissionError, OSError) as e:
                                    print(f"Error deleting JS file {js_path}: {e}")
                    # Hapus folder jika sudah kosong
                    try:
                        if os.path.exists(js_dir) and not os.listdir(js_dir):
                            os.rmdir(js_dir)
                        elif os.path.exists(js_dir):
                            # Jika masih ada file lain, hapus dengan shutil
                            shutil.rmtree(js_dir)
                    except (PermissionError, OSError):
                        pass
                except Exception as e:
                    print(f"Error deleting JS directory {js_dir}: {e}")
            
            # Hapus HTML file dari templates/invited/
            if template.html_filename:
                html_path = os.path.join(settings.BASE_DIR, 'templates', 'invited', template.html_filename)
                if os.path.exists(html_path) and os.path.isfile(html_path):
                    try:
                        os.remove(html_path)
                    except (PermissionError, OSError) as e:
                        print(f"Error deleting HTML file {html_path}: {e}")
            
            # Hapus semua images dari media/templates/images/template-slug/
            # Hapus images via Django dulu (akan trigger file deletion)
            for image in template.get_images():
                if image.image:
                    try:
                        image.image.delete()  # Hapus via Django (akan hapus file juga)
                    except (PermissionError, OSError) as e:
                        print(f"Error deleting image {image.image.path}: {e}")
            
            # Hapus folder images jika sudah kosong
            images_dir = os.path.join(settings.MEDIA_ROOT, 'templates', 'images', template.slug)
            if os.path.exists(images_dir) and os.path.isdir(images_dir):
                try:
                    if not os.listdir(images_dir):
                        os.rmdir(images_dir)
                    else:
                        # Jika masih ada file lain, hapus dengan shutil
                        shutil.rmtree(images_dir)
                except (PermissionError, OSError):
                    pass
            
            # Hapus template dari database (akan cascade delete CSS, JS, Images records)
            template.delete()
            messages.success(request, 'Template dan semua file terkait berhasil dihapus!')
            
        except Exception as e:
            # Jika ada error, tetap hapus dari database tapi beri warning
            try:
                template.delete()
            except:
                pass
            messages.warning(request, f'Template dihapus dari database, tapi beberapa file mungkin masih ada. Error: {str(e)}')
        
        return redirect('invitation_templates:template_list')
    
    return render(request, 'invitation_templates/template_confirm_delete.html', {
        'template': template
    })


@login_required
def template_preview(request, pk):
    """Preview template"""
    template = get_object_or_404(InvitationTemplate, pk=pk, is_active=True)
    
    # Dummy data untuk preview
    context = {
        'template': template,
        'invitation': {
            'groom_name': 'John',
            'bride_name': 'Jane',
            'parents_text': 'Putra dari Bapak... dan Ibu...',
        }
    }
    
    # Render template HTML jika ada
    if template.html_filename:
        try:
            html_path = template.get_html_template_path()
            return render(request, html_path, context)
        except:
            pass
    
    return render(request, 'invitation_templates/template_preview.html', context)


@login_required
def delete_css_file(request, pk):
    """Hapus CSS file"""
    css_file = get_object_or_404(TemplateCSS, pk=pk)
    template = css_file.template
    
    if template.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('invitation_templates:template_edit', pk=template.pk)
    
    # Hapus file dari static folder
    css_path = os.path.join(settings.BASE_DIR, 'static', 'templates', 'css', template.slug, css_file.filename)
    if os.path.exists(css_path):
        os.remove(css_path)
    
    css_file.delete()
    messages.success(request, 'CSS file berhasil dihapus!')
    return redirect('invitation_templates:template_edit', pk=template.pk)


@login_required
def delete_js_file(request, pk):
    """Hapus JS file"""
    js_file = get_object_or_404(TemplateJS, pk=pk)
    template = js_file.template
    
    if template.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('invitation_templates:template_edit', pk=template.pk)
    
    # Hapus file dari static folder
    js_path = os.path.join(settings.BASE_DIR, 'static', 'templates', 'js', template.slug, js_file.filename)
    if os.path.exists(js_path):
        try:
            os.remove(js_path)
        except (PermissionError, OSError) as e:
            messages.warning(request, f'File JS dihapus dari database, tapi file fisik mungkin masih ada. Error: {str(e)}')
    
    # Hapus dari database
    js_file.delete()
    
    # Cek apakah folder kosong, jika ya hapus folder juga
    js_dir = os.path.join(settings.BASE_DIR, 'static', 'templates', 'js', template.slug)
    if os.path.exists(js_dir):
        try:
            if not os.listdir(js_dir):  # Jika folder kosong
                os.rmdir(js_dir)
        except:
            pass
    
    messages.success(request, 'JS file berhasil dihapus!')
    return redirect('invitation_templates:template_edit', pk=template.pk)


@login_required
def delete_image_file(request, pk):
    """Hapus image file"""
    image_file = get_object_or_404(TemplateImage, pk=pk)
    template = image_file.template
    
    if template.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('invitation_templates:template_edit', pk=template.pk)
    
    image_file.delete()
    messages.success(request, 'Image file berhasil dihapus!')
    return redirect('invitation_templates:template_edit', pk=template.pk)
