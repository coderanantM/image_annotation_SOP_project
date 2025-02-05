from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import AnnotatedImage
from .forms import ImageUploadForm, RegisterForm

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
    image = AnnotatedImage.objects.get(pk=pk)
    return render(request, 'annotate/annotate.html', {'image': image})

@login_required
@require_POST
def save_annotations(request, pk):
    image = AnnotatedImage.objects.get(pk=pk)
    image.annotations = request.POST.get('annotations')
    image.save()
    return JsonResponse({'status': 'success'})