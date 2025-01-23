from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import subprocess

def homepage(request):
    return render(request, 'annotator/homepage.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'annotator/register.html', {'form': form})

def login_user(request):
    next_url = request.GET.get('next', 'annotate')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'annotator/login.html', {'form': form, 'next': next_url})

@login_required(login_url='login')
def annotate(request):
    # Launch the annotation tool
    subprocess.Popen(["digitalsreeni-image-annotator"])
    return render(request, 'annotator/annotate.html')
