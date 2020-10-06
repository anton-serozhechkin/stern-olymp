from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404, JsonResponse
from .forms import UserForm, SignUpStudentForm, UserAnswerForm
from .models import *
from hashlib import sha256
from urllib.parse import urlencode, parse_qsl
import json
import datetime
from django.contrib.auth import logout
from .optional_methods import getting_student, getting_user_in_event, strftime, finish_time_olymp, create_new_user_answer


def auth_user(request):
    """
        signin/signup view
        using django authenticate mechanism
    """
    if request.method == 'POST':
        req = request.POST
        if 'password_login' in request.POST:
            username = req.get('username_login')
            password = req.get('password_login')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('payment')
            else:
                messages.info(request, 'Неверный логин или пароль')
                return redirect('auth_user')
        else:
            email = req.get('email', None)
            username = req.get('username', None)
            telephone_number = req.get('telephone_number', None)
            password = req.get('password', None)
            first_name = req.get('first_name', None)
            last_name = req.get('last_name', None)
            class_number = req.get('class_number', None)
            name_school = req.get('name_school', None)
            if not email or len(email) < 5:
                messages.info(request, 'Заполните поле электронная почта')
            elif not username or len(username) < 3:
                messages.info(request, 'Заполните поле логин')
            elif not telephone_number:
                messages.info(request, 'Заполните поле телефонный номер')
            elif not password:
                messages.info(request, 'Заполните поле пароль')
            elif not first_name:
                messages.info(request, 'Заполните поле имя')
            elif not last_name:
                messages.info(request, 'Заполните поле фамилия')
            elif not class_number or int(class_number) not in range(1, 12):
                messages.info(request, 'Заполните поле номер класса. Вводить нужно только сам номер(цифрой)')
            elif not name_school:
                messages.info(request, 'Заполните поле название школы')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Логин уже занят')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Электронная почта уже занята')
            else:
                new_user = User.objects.create_user(username=username, email=email,
                                                    first_name=first_name, last_name=last_name,
                                                    password=password)
                user = User.objects.get(username=username)
                class_number_get = ClassNumber.objects.get(name=class_number)
                student = Student.objects.create(user=new_user, telephone_number=telephone_number,
                                                 class_number=class_number_get, name_school=name_school)
                registration_text = settings.REGISTRATION_TEXT
                hello_text = registration_text.format(request.POST.get('username'), request.POST.get('password'))
                if settings.START_SETTING == "PRODUCTION":
                    send_mail(
                        'Регистрация на онлайн олимпиаду',
                        hello_text,
                        settings.EMAIL_HOST_USER,
                        [email, ],
                        fail_silently=False)
                event_for_user = Event.objects.get(classes__name=class_number_get)
                UserInEvent.objects.create(user=student, event=event_for_user,
                                           paid=False, date_registration=datetime.datetime.now())
                auth.login(request, user)
                return redirect('payment')
    return render(request, 'core/index.html', locals())


def redirect_index(request):
    return redirect('auth_user')


@login_required(login_url='/user/auth/')
def payment(request):
    """

    :param request: standard django param

    **Code**
        account - request username of current user

        desc - description of payment

        sum - dum of payment

        sign_string - collecting the necessary information for signature

        sign - readymade encrypted signature

    :return sign to unitpay server
    """
    student = UserInEvent.objects.get(user__user=request.user)
    if student.paid is False:
        if request.method == 'POST':
            account = request.user.username
            separator = '{up}'
            params = {
                'account': account,
                'desc': settings.DESC,
                'sum': settings.PRICE,
            }
            sign_string = separator.join(['{}'.format(value) for (key, value) in params.items()])
            sign_string += separator + settings.SECRET_KEY_PAYMENT
            sign = sha256(sign_string.encode('utf-8')).hexdigest()
            params.update({'signature': sign})
            params_string = urlencode(params)
            url = 'https://unitpay.ru/pay/{}?{}'
            return redirect(url.format(settings.MERCHANT_ID, params_string))
    else:
        return redirect(reverse('time_to_start', kwargs={'category_slug': student.event.category.slug, 'slug': student.event.slug}))
    return render(request, 'payment/payment.html', locals())


@login_required(login_url='/user/auth/')
def time_to_start(request, category_slug, slug):
    time_start = Event.objects.get(slug=slug).data_event
    if datetime.datetime.now().timestamp() < time_start.timestamp():
        return render(request, 'core/timer.html', {'time_to_start': json.dumps(strftime(time_start))})
    else:
        return redirect(reverse('start_olympiad', kwargs={'category_slug': category_slug, 'slug': slug}))


@login_required(login_url='/user/auth/')
def final(request, category_slug, slug):
    return render(request, 'core/final.html')


@login_required(login_url='/user/auth/')
def start_olympiad(request, category_slug, slug):
    student_in_event = getting_user_in_event(request.user)
    if student_in_event.paid is False:
        return redirect('payment')
    else:
        data = Event.objects.get(slug=slug)
        if 'start-modal-start' in request.POST:
            return redirect(reverse('question', kwargs={'category_slug': category_slug, 'slug': slug}))
    return render(request, 'core/start-olymp.html', locals())


@login_required(login_url='/user/auth/')
def question(request, category_slug, slug):
    student = getting_student(request.user)
    answered_questions = UserAnswer.objects.filter(student=request.user.student)
    questions = Question.objects.filter(event__slug=slug)[0:4]
    event = Event.objects.get(slug=slug)
    finish_time = finish_time_olymp(user=request.user, event=event)
    if finish_time.timestamp() < datetime.datetime.now().timestamp():
        return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
    end_olymp_user = json.dumps(strftime(finish_time))
    if questions.count() == answered_questions.count():
       return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
    list_answered_questions = []
    if answered_questions:
        for answered_question in answered_questions:
            list_answered_questions.append(answered_question.question.question)
        questions = Question.objects.filter(event__slug=slug).exclude(question__in=list_answered_questions)[0:4]
    if request.method == "POST":
        if request.POST.get('answer'):
            answer = request.POST.get('answer')
            question = Question.objects.get(pk=request.POST.get('id'))
            create_new_user_answer(event, question, answer, student)
        else:
            nothing_answer = 'Вы ничего не ответили'
        return redirect(reverse('question', kwargs={'category_slug': category_slug, 'slug': slug}))
    return render(request, 'core/olymp.html', locals())


def signout(request):
    logout(request)
    return redirect('auth_user')


def payment_check(request):
    """
    handler Unitay payment

    :param request: standard django param

    **Code**
        data - data from request UnitPay server

        method - status of payment

        payment - user from db
    :return json with message to user
    check this links:
    :https://github.com/unitpay/python-sdk
    :https://github.com/Underlor/unitpay_python_sdk

    """
    data = request.GET.copy()
    method = data.get('method')
    if method == 'check':
        try:
            student = getting_student(data.get('params[account]'))
            if student.paid:
                return json.dumps({'message': 'Вы уже оплатили олимпиаду'})
            else:
                return json.dumps({'message': 'Ожидание успешно'})
        except Student.DoesNotExist:
                return json.dumps({'message': 'Неверный обьект обработки. Пользователь не найден'})
    elif method == 'pay':
        try:
            student = getting_student(data.get('params[account]'))
            student.paid = True
            student.save()
            return json.dumps({'message': 'Оплата успешна'})
        except Student.DoesNotExist:
            return json.dumps({'message': 'Неверный обьект обработки. Пользователь не найден'})
    elif method == 'error':
        return json.dumps({'message': 'Произошла какая-то ошибка'})
    else:
        return json.dumps({'message': 'Метод не поддерживается'})


@login_required(login_url='/user/auth/')
def bad_payment(request):
    """
    :param request: standard django param

        will be called if the UnitPay server
        response on the board is negative
    """
    return render(request, 'payment/bad-payment.html')


def documents(request):
    return render(request, 'info/documents.html')


@login_required(login_url='/user/auth/')
def profile(request):
    user = User.objects.get(username=request.user.username)
    student = Student.objects.get(user=request.user)
    user_in_event = getting_user_in_event(request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = SignUpStudentForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            if user_form.has_changed():
                instance = user_form.save(commit=False)
                instance.username = user_form.cleaned_data['username']
                instance.last_name = user_form.cleaned_data['last_name']
                instance.first_name = user_form.cleaned_data['first_name']
                instance.email = user_form.cleaned_data['email']
                instance.save()
            if student_form.has_changed():
                instance = student_form.save(commit=False)
                instance.telephone_number = student_form.cleaned_data['telephone_number']
                instance.class_number = student_form.cleaned_data['class_number']
                instance.name_school = student_form.cleaned_data['name_school']
                instance.save()
            return redirect('profile')
        else:
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        student_form = SignUpStudentForm(instance=student)
    return render(request, 'profile/profile.html', locals())


@login_required(login_url='/user/auth/')
def succes_payment(request):
    user_in_event = getting_user_in_event(request.user)
    user_in_event.paid = True
    user_in_event.save()
    return render(request, 'payment/success-payment.html', locals())
