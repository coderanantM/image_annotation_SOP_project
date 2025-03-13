from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import AnnotatedImage, AnnotationClass
from .forms import ImageUploadForm, RegisterForm, AnnotationClassForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'annotate/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'annotate/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def home(request):
    images = AnnotatedImage.objects.all()
    return render(request, 'annotate/home.html', {'images': images})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            print(f"Image saved at: {image.original_image.url}")  # Debugging
            return redirect('home')
    else:
        form = ImageUploadForm()
    return render(request, 'annotate/upload.html', {'form': form})

@login_required
def annotate_image(request, pk):
    image = get_object_or_404(AnnotatedImage, pk=pk)
    classes = AnnotationClass.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'create_class' in request.POST:
            class_form = AnnotationClassForm(request.POST)
            if class_form.is_valid():
                new_class = class_form.save(commit=False)
                new_class.user = request.user
                new_class.save()
                return redirect('annotate_image', pk=pk)
        else:
            annotation_data = request.POST.get('annotation_data')
            selected_class = request.POST.get('selected_class')
            # Save the annotation data and class to the database
            image.annotations = annotation_data
            image.save()
            return redirect('home')

    class_form = AnnotationClassForm()
    return render(request, 'annotate/annotate.html', {'image': image, 'classes': classes, 'class_form': class_form})

@login_required
@require_POST
def save_annotations(request, pk):
    image = AnnotatedImage.objects.get(pk=pk)
    image.annotations = request.POST.get('annotations')
    image.save()
    return JsonResponse({'status': 'success'})