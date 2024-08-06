from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from authorization.forms import RegisterForm, SiteLogForm
from theater_info.core_utils import get_navigation_menu


def send_confirmation_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    mail_subject = 'Активация вашего аккаунта.'
    message = render_to_string('authorization/acc_active_email.html', {
        'user': user,
        'domain': settings.DOMAIN_NAME,
        'uid': uid,
        'token': token,
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


# Регистрация
def registration(request):
    menu = get_navigation_menu(request.user)
    if request.user.is_authenticated:
        return redirect('repertoire')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_confirmation_email(user)
            return HttpResponse('Пожалуйста, подтвердите свой адрес электронной почты, чтобы завершить регистрацию')
        else:
            messages.error(request, "Что-то пошло не так, проверьте введенные данные!")
    else:
        form = RegisterForm()
    context = {
        "menu": menu,
        "form": form,
    }
    return render(request, "authorization/registration.html", context=context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Благодарим вас за подтверждение по электронной почте. '
                            'Теперь вы можете войти в свою учетную запись.')
    else:
        return HttpResponse('Ссылка активации недействительна!')


# Вход
def site_login(request):
    menu = get_navigation_menu(request.user)
    form = SiteLogForm
    if request.user.is_authenticated:
        return redirect('main_page')
    if request.method == "POST":
        form = SiteLogForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        HttpResponse("Что-то пошло не так, проверьте введенные данные!")
    context = {
        "menu": menu,
        "form": form,
    }
    return render(request, "authorization/site_login.html", context=context)


# Выход
def site_logout(request):
    logout(request)
    return redirect('main_page')
