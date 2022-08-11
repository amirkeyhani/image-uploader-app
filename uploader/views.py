from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, SignupForm, UpdateUserForm, ProfileUpdateForm
from .models import Image, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator

from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db import IntegrityError
from django.core.mail import send_mail, EmailMultiAlternatives

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
import random
# Create your views here.


def index(request):
    if request.method == 'POST':
        otp = random.randint(1000, 9999)
        request.session['email_otp'] = otp
        user_email = request.user.email
        message = f'Your otp is {otp}'
        
        send_mail(
            'OTP Email Verification', 
            message, 
            settings.EMAIL_HOST_USER, 
            [user_email], 
            fail_silently=False, 
        )
        return redirect('email-verify')
    
    images = Image.objects.all().order_by('-created_at')[:9]
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

        uploader = Image(user=request.user, name=name,
                            image=image, profile=profile)
        uploader.save()
        messages.success(request, 'Your Image Uploaded Successfully!!')

    images = Image.objects.all().order_by('-created_at')[:9]
    paginator = Paginator(images, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'uploader.html',
                  {'images': images, 'page_obj': page_obj})


login_required(login_url='login')
def image_like(request, pk):
    uploader = Image.objects.get(pk=pk)
    uploader.like += 1
    uploader.save()
    return redirect('/')


@login_required(login_url='login')
def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
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


def activation_sent(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # user = authenticate(request, username=username, password=password)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        auth_login(request, user,
                   backend='django.contrib.auth.backends.ModelBackend')
        messages.success(
            request, 'Sign up Done. Your account has been created!, You are logged in!!')
        return redirect('/')
    else:
        return render(request, 'activation_invalid.html')


def email(request):
    send_mail(
        subject='Greetings',
        message='Hello, how are you?',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False
    )
    messages.success(request, 'email sent...')
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            user.refresh_from_db()
            user.profile.first_name = fm.cleaned_data.get('first_name')
            user.profile.last_name = fm.cleaned_data.get('last_name')
            user.profile.email = fm.cleaned_data.get('email')
            user.is_active = False
            user.save()
            
            username = fm.cleaned_data.get('username')
            email = fm.cleaned_data.get('email')
            # password = fm.cleaned_data.get('password1')
            htmly = get_template('email.html')
            d = {'username': username}
            subject, from_email, to = 'Welcome', settings.EMAIL_HOST_USER, email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(
                subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            # messages.success(
            #     request, 'Your account has been created! You\'re now able to log in')
            
            current_site = get_current_site(request)
            subject = 'Please activate your account.'
            message = render_to_string('activation_request.html', {
                                        'user': user,
                                        # 'domain': current_site.domain,
                                        # 'domain': get_current_site(request).domain,
                                        'domain': request.get_host(),
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        })
            user.email_user(subject, message)
            return redirect('activation_sent')
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

@login_required
def logout(request):
    # request.session.clear()
    auth.logout(request)
    return redirect('login')
    # return render(request, 'logout.html')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            uid = User.objects.get(email=email)
            host = request.get_host()
            url = f'http://{host}/change-password/{uid.profile.uuid}'
            
            send_mail(
                'Reset Password', 
                url, 
                settings.EMAIL_HOST_USER, 
                [email], 
                fail_silently=False,
            )
            return redirect('forget-password-done')
        else:
            messages.error(request, 'email address does not exist')
            
    return render(request, 'forget-password.html')
            
def change_password(request, uid):
    try:
        if Profile.objects.filter(uuid=uid).exists():
            if request.method == 'POST':
                pass1 = request.POST['password1']
                pass2 = request.POST['password2']
                if pass1 == pass2:
                    p = Profile.objects.get(uuid=uid)
                    u = p.user
                    user = User.objects.get(username=u)
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(request, 'Your Password has been reset successfully')
                    return redirect('login')
                else:
                    messages.error(request, 'Two passwords did not match')
                    
        else:
            return HttpResponse('Wrong reset password URL')
    except:
        raise HttpResponse('Reset password URL does not exist')
    return render(request, 'change-password.html')

def email_verification(request):
    if request.method == 'POST':
        u_otp = request.POST['otp']
        otp = request.session['email_otp']
        if int(u_otp) == otp:
            p = Profile.objects.get(user=request.user)
            p.email_verified = True
            p.save()
            messages.success(request, f'Your email {request.user.email} is verified now')
            return redirect('/')
        else:
            messages.error(request, 'Wrong OTP')
            
    return render(request, 'email-verified.html')

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
    prof_img = Image.objects.filter(user=user)

    return render(request, 'user-profile.html',
                  {'user': usr, 'prof_img': prof_img})
