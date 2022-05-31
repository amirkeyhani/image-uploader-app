from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, SignupForm, UpdateUserForm, ProfileUpdateForm
from .models import Uploader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    images = Uploader.objects.all().order_by('-created_at')[:9]
    paginator = Paginator(images, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'images': images, 'page_obj': page_obj})


@login_required(login_url='login')
def image_uploader(request):
    if request.method == 'POST' and 'upload' in request.POST:
        name = 'name' in request.POST and request.POST['name']
        image = 'image' in request.FILES and request.FILES['image']
        profile = 'profile' in request.POST and request.POST['profile']

        uploader = Uploader(user=request.user, name=name,
                            image=image, profile=profile)
        uploader.save()
        messages.success(request, 'Your Image Uploaded Successfully!!')

    images = Uploader.objects.all().order_by('-created_at')[:9]
    paginator = Paginator(images, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'uploader.html',
                  {'images': images, 'page_obj': page_obj})


login_required(login_url='login')
def image_like(request, pk):
    uploader = Uploader.objects.get(pk=pk)
    uploader.like += 1
    uploader.save()
    return redirect('/')


@login_required(login_url='login')
def image_detail(request, pk):
    image = get_object_or_404(Uploader, pk=pk)
    comments = image.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.image = image
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'uploader.html',
                  {'image': image, 'comments': comments,
                   'new_comment': new_comment, 'comment_form': comment_form})


def signup(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            user.refresh_from_db()
            user.profile.first_name = fm.cleaned_data.get('first_name')
            user.profile.last_name = fm.cleaned_data.get('last_name')
            user.profile.email = fm.cleaned_data.get('email')
            user.save()
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Sign up Done, You are logged in!!')
                return redirect('/')
    else:
        fm = SignupForm()

    return render(request, 'signup.html', {'fm': fm})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back {request.user} !')
            return redirect('/')
        else:
            messages.info(request, 'Account does not exist, plz sign up!!')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        uu_form = UpdateUserForm(instance=request.user,
                                 data=request.POST)
        pu_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if uu_form.is_valid() and pu_form.is_valid():
            uu_form.save()
            pu_form.save()
            messages.success(request, 'Your Profile has been updated!')
    else:
        uu_form = UpdateUserForm(instance=request.user)
        pu_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profile.html',
                  {'uu_form': uu_form, 'pu_form': pu_form})


@login_required(login_url='login')
def user_profile(request, user):
    usr = User.objects.get(username=user)
    prof_img = Uploader.objects.filter(user=user)

    return render(request, 'user-profile.html',
                  {'user': usr, 'prof_img': prof_img})
